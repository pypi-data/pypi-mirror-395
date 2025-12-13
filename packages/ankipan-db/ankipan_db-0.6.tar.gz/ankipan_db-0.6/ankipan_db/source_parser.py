from pathlib import Path
import psycopg2
from psycopg2 import sql, errors
import random
from itertools import islice
from psycopg2.extras import execute_values
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Iterable
import time
import logging
import json
from functools import wraps

from ankipan import Reader

from ankipan_db import DBManager, db_config, PROJECT_ROOT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def retry_on_deadlock(max_attempts=5, initial_backoff=0.1, max_backoff=20.0):
    """
    Retry the decorated function if it raises psycopg2.errors.DeadlockDetected.
    """
    def decorator(fn):
        @wraps(fn)
        def wrapped(*args, **kwargs):
            backoff = initial_backoff
            for attempt in range(1, max_attempts + 1):
                try:
                    return fn(*args, **kwargs)
                except errors.DeadlockDetected:
                    if attempt == max_attempts:
                        logger.error("Deadlock persisted after %d attempts", max_attempts)
                        raise
                    sleep = backoff + random.random() * backoff
                    logger.warning("Deadlock detected; retrying in %.2fs (attempt %d/%d)",
                                   sleep, attempt, max_attempts)
                    time.sleep(sleep)
                    backoff = min(backoff * 2, max_backoff)
        return wrapped
    return decorator


class Parser:
    def __init__(self, lang, db = None):
        self.lang = lang
        if not db:
            self.db = DBManager(lang)
        else:
            self.db = db
        self.reader = Reader(lang)

    def add_source_category(self, source_category_name, metadata = None):
        sql = f"""
        WITH existing AS (
        SELECT id
        FROM {self.lang}.sources
        WHERE parent_id IS NULL AND name = %s
        ),
        ins AS (
        INSERT INTO {self.lang}.sources (parent_id, name, metadata, nesting_level, is_leaf)
        SELECT NULL, %s, %s, 0, %s
        WHERE NOT EXISTS (SELECT 1 FROM existing)
        RETURNING id
        )
        SELECT id FROM ins
        UNION ALL
        SELECT id FROM existing;
        """
        conn = self.db.get_safe_conn()
        if metadata is None:
            metadata = {}
        with conn, conn.cursor() as cur:
            cur.execute(sql, (source_category_name, source_category_name, json.dumps(metadata), False))
            conn.commit()
            source_category_id = cur.fetchone()[0]
        self.db.db_pool.putconn(conn)
        return source_category_id

    def add_source(self,
                   path,
                   source_category_name: str,
                   overwrite=False,
                   source_root_name=None,
                   n_threads=5,
                   index_separators: Iterable[str] = None,
                   replace_chars: Iterable[str] = None,
                   chunk_size: int = 1000,
                   file_match_pattern = None,
                   dir_match_pattern = None,
                   assert_coherence: bool = False,
                   db_workers: int = 3):

        logger.info(f'Adding source {path}')
        path = Path(path)
        if not path.exists():
            raise RuntimeError(f'Path {path} does not exist.')

        setup_conn = self.db.get_safe_conn()
        try:
            with setup_conn:
                with setup_conn.cursor() as cur:
                    cur.execute(
                        "SELECT id FROM sources WHERE name = %s AND nesting_level = 0",
                        (source_category_name,),
                    )
                    row = cur.fetchone()
                    if not row:
                        raise RuntimeError(
                            f'Source Category "{source_category_name}" not defined in db'
                        )
                    source_category_id = row[0]

                    if source_root_name is None:
                        source_root_name = Path(path).stem

                    cur.execute(
                        "SELECT name FROM sources WHERE parent_id = %s", (source_category_id,)
                    )
                    existing_root_sources = [name for (name,) in cur.fetchall()]

                    if path.is_dir():
                        if source_root_name not in existing_root_sources:
                            cur.execute(
                                """
                                INSERT INTO sources (parent_id, name, metadata, nesting_level, is_leaf)
                                VALUES (%s, %s, %s, %s, %s)
                                RETURNING id
                                """,
                                (source_category_id, source_root_name, None, 1, False),
                            )
                        else:
                            cur.execute(
                                "SELECT id FROM sources WHERE name = %s AND parent_id = %s",
                                (source_root_name, source_category_id),
                            )
                        source_root_id = cur.fetchone()[0]
                        is_leaf = False
                    else:
                        source_root_id = source_category_id
                        is_leaf = True

                    if overwrite:
                        self.db.delete_source(cur, source_root_id)
                        cur.execute(
                            """
                            INSERT INTO sources (parent_id, name, metadata, nesting_level, is_leaf)
                            VALUES (%s, %s, %s, %s, %s)
                            ON CONFLICT (parent_id, name) DO UPDATE SET name = EXCLUDED.name
                            RETURNING id
                            """,
                            (source_category_id, source_root_name, None, 1, is_leaf),
                        )
                        source_root_id = cur.fetchone()[0]
                    source_tree = self.db.get_source_tree_for_id(cur, source_root_id)
        finally:
            self.db.db_pool.putconn(setup_conn)

        imported_files = set()
        parent_ids = {parent_id for parent_id, _, _ in source_tree.values()}
        for node_id, (parent_id, name, is_leaf) in source_tree.items():
            if node_id not in parent_ids and is_leaf:
                parts = []
                current_id = node_id
                while current_id != source_category_id and current_id in source_tree:
                    parent_id, nm, _ = source_tree[current_id]
                    parts.append(nm)
                    current_id = parent_id
                imported_files.add(Path("/".join(reversed(parts))))

        file_paths = list(
            self.reader.collect_file_paths(
                path,
                file_match_pattern=file_match_pattern,
                exclude_paths=imported_files,
                dir_match_pattern=dir_match_pattern,
            )
        )

        if len(file_paths) == 0:
            logger.info(f"Source already fully imported")
            return
        logger.info(f"Files to import: {len(file_paths)} (already in DB: {len(imported_files)})")
        if not file_paths:
            logger.info(f'Source "{source_root_name}" filtered out or already fully imported.')
            return

        file_paths_chunks = [
            file_paths[i : i + chunk_size] for i in range(0, len(file_paths), chunk_size)
        ]
        logger.info(f"Processing {len(file_paths_chunks)} chunks")
        disk_root = Path(path).resolve()

        max_outstanding = max(db_workers * 2, 4)

        @retry_on_deadlock(max_attempts=5)
        def _db_task(files_batch):
            conn = self.db.get_safe_conn()
            try:
                with conn.cursor() as c:
                    c.execute(sql.SQL("SET LOCAL search_path TO {}, public")
                              .format(sql.Identifier(self.lang)))
                self.add_files_to_db(files_batch, source_root_id, disk_root, conn)
            finally:
                self.db.db_pool.putconn(conn)

        with ThreadPoolExecutor(max_workers=db_workers, thread_name_prefix="db-writer") as writer:
            futures = []
            for chunk in file_paths_chunks:
                files = self.reader.open_files(
                    chunk,
                    index_separators=index_separators,
                    replace_chars=replace_chars,
                    source_name=source_root_name,
                    assert_coherence=assert_coherence,
                )
                self.reader.process_files(files, save_pos_data=True, n_threads=n_threads)
                futures.append(writer.submit(_db_task, files))

                # mild backpressure
                if len(futures) >= max_outstanding:
                    futures.pop(0).result()

            # collect & re-raise any exceptions
            for f in as_completed(futures):
                f.result()

        logger.info(f'Finished adding source "{source_root_name}"')

    def add_files_to_db(self, files, source_root_id, disk_root, conn):
        schema = self.lang
        logger.info(f"add_files_to_db: Adding {len(files)} files to db")

        def chunked(it, size):
            it = iter(it)
            while True:
                batch = list(islice(it, size))
                if not batch:
                    break
                yield batch

        disk_root = Path(disk_root).resolve()
        cache: dict[tuple[int,str],int] = {}  # dir node cache

        def ensure_dir(cur, parent_id: int, name: str, level: int) -> int:
            key = (parent_id, name)
            if key in cache:
                return cache[key]
            cur.execute(
                sql.SQL("""
                INSERT INTO {}.sources (parent_id, name, metadata, lemma_counts, nesting_level, is_leaf)
                VALUES (%s, %s, %s, %s, %s, %s)
                ON CONFLICT (parent_id, name) DO NOTHING
                RETURNING id""").format(sql.Identifier(schema)),
                (parent_id, name, json.dumps({}), json.dumps({}), level, False)
            )
            row = cur.fetchone()
            if row:
                new_id = row[0]
            else:
                cur.execute(
                    sql.SQL("SELECT id FROM {}.sources WHERE parent_id = %s AND name = %s")
                    .format(sql.Identifier(schema)),
                    (parent_id, name))
                new_id = cur.fetchone()[0]
            cache[key] = new_id
            return new_id

        try:
            with conn.cursor() as cur:
                cur.execute(
                    sql.SQL("SET LOCAL search_path TO {}, public")
                    .format(sql.Identifier(schema))
                )

                unique_lemmas = set()
                word_rows = {}
                all_text_segments = []
                words_in_text_segments = []
                for file in files:
                    path = Path(file.path).resolve()
                    parent = source_root_id

                    base = disk_root if disk_root.is_dir() else disk_root.parent
                    try:
                        rel = path.parent.relative_to(base).parts
                    except ValueError:
                        rel = ()

                    for lvl, part in enumerate(rel, start=2):
                        parent = ensure_dir(cur, parent, part, lvl)

                    leaf_level = len(rel) + (2 if disk_root.is_dir() else 1)
                    leaf_name = path.name
                    cur.execute(
                        sql.SQL("""
                        INSERT INTO {}.sources (parent_id, name, metadata, lemma_counts, nesting_level, is_leaf)
                        VALUES (%s, %s, %s, %s, %s, %s)
                        ON CONFLICT (parent_id, name) DO NOTHING
                        RETURNING id
                        """).format(sql.Identifier(schema)), (parent, leaf_name, json.dumps({}), json.dumps(dict(file.lemma_counts)), leaf_level, True)
                    )
                    row = cur.fetchone()
                    leaf_id = row[0] if row else None
                    if not leaf_id:
                        cur.execute(
                            sql.SQL("SELECT id FROM {}.sources WHERE parent_id = %s AND name = %s")
                            .format(sql.Identifier(schema)),
                            (parent, leaf_name)
                        )
                        leaf_id = cur.fetchone()[0]
                    for i, tokens in enumerate(file.text_segment_components):
                        start_s, end_s = (file.sub_timestamps[i] if file.sub_timestamps else (None, None))
                        all_text_segments.append((start_s, end_s, file.stanza_segments[i].text, i, leaf_id))
                        for tok in tokens:
                            w, p, xp, l = tok["word"], tok["pos"], tok["xpos"], tok["lemma"]
                            unique_lemmas.add(l)
                            word_rows[(w, p)] = (xp, l)
                            words_in_text_segments.append(((w, p), (leaf_id, i)))

                lemma_id_by_lemma = {}
                if unique_lemmas:
                    vals = sorted(unique_lemmas)  # stable order helps
                    for batch in chunked(vals, 5000):
                        execute_values(
                            cur,
                            sql.SQL("""
                                INSERT INTO {}.lemmas (lemma)
                                VALUES %s
                                ON CONFLICT (lemma) DO NOTHING
                            """).format(sql.Identifier(schema)),
                            [(l,) for l in batch],
                            fetch=False,
                        )
                    for batch in chunked(vals, 5000):
                        cur.execute(
                            sql.SQL("SELECT lemma, id FROM {}.lemmas WHERE lemma = ANY(%s)")
                            .format(sql.Identifier(schema)),
                            (batch,),
                        )
                        lemma_id_by_lemma.update(cur.fetchall())

                word_id_by_key = {}
                if word_rows:
                    word_vals = [(w, p, xp, lemma_id_by_lemma[l]) for (w, p), (xp, l) in word_rows.items()]
                    for batch in chunked(word_vals, 5000):
                        execute_values(
                            cur,
                            sql.SQL("""
                                INSERT INTO {}.words (word, pos, xpos, lemma_id)
                                VALUES %s
                                ON CONFLICT (word, pos) DO NOTHING
                            """).format(sql.Identifier(schema)),
                            batch,
                            fetch=False,
                        )

                    for batch in chunked(word_rows.keys(), 5000):
                        rows = execute_values(
                            cur,
                            sql.SQL("""
                                SELECT w.id, v.word, v.pos
                                FROM (VALUES %s) AS v(word, pos)
                                JOIN {}.words w USING (word, pos)
                            """).format(sql.Identifier(schema)),
                            batch,
                            fetch=True,
                        )
                        for wid, w, p in rows:
                            word_id_by_key[(w, p)] = wid

                segment_id_by_key = {}
                if all_text_segments:
                    for batch in chunked(all_text_segments, 2000):
                        rows = execute_values(
                            cur,
                            sql.SQL("""
                                INSERT INTO {}.text_segments (start_s, end_s, text, "index", source_id)
                                VALUES %s
                                ON CONFLICT (source_id, "index")
                                DO UPDATE SET
                                text   = EXCLUDED.text,
                                start_s = COALESCE(EXCLUDED.start_s, {}.text_segments.start_s),
                                end_s   = COALESCE(EXCLUDED.end_s,   {}.text_segments.end_s)
                                RETURNING id, source_id, "index"
                            """).format(sql.Identifier(schema), sql.Identifier(schema), sql.Identifier(schema)),
                            batch,
                            fetch=True,
                        )
                        for tsid, sid, idx in rows:
                            segment_id_by_key[(sid, idx)] = tsid

                if words_in_text_segments:
                    tuples = []
                    for (w, p), (sid, idx) in words_in_text_segments:
                        wid  = word_id_by_key.get((w, p))
                        tsid = segment_id_by_key.get((sid, idx))
                        if wid and tsid:
                            tuples.append((wid, tsid))

                    for batch in chunked(tuples, 10000):
                        execute_values(
                            cur,
                            sql.SQL("""
                                INSERT INTO {}.words_in_text_segments (word_id, text_segment_id)
                                VALUES %s
                                ON CONFLICT (word_id, text_segment_id) DO NOTHING
                            """).format(sql.Identifier(schema)), batch, fetch=False)
            conn.commit()
            logger.info("Finished adding entries to db")

        except Exception:
            conn.rollback()
            logger.exception("DB batch failed; rolled back.")
            raise

    def remove_source(self, source_root_name, conn_ = None):
        if not conn_:
            conn = self.db.get_safe_conn()
        else:
            conn = conn_
        with conn.cursor() as cur:
            cur.execute("SELECT id FROM sources WHERE parent_id IS NULL AND name = %s", (source_root_name,))
            source_root_id_raw = cur.fetchone()
            if source_root_id_raw:
                self.db.delete_source(cur, source_root_id_raw[0])
            else:
                logger.error(f'No source with the name {source_root_name} in db, not deleting anything.')
        conn.commit()

    def sync_dir(self,
                 sources_path: str,
                 source_category: str,
                 overwrite = False,
                 n_threads = 5,
                 db_workers = 5,
                 index_separators: Iterable[str] = None,
                 replace_chars=None,
                 start_at: str = None,
                 assert_coherence: bool = False,
                 chunk_size = 5000,
                 file_match_pattern = None,
                 dir_match_pattern = None):
        """
        Parse lemmas from path with text data using the ankimelon.Reader.collect_file_paths() method

        Parameters
        ----------
        sources_path: '/' separated Path to a file or directory with textfiles
        source_category: name of subcategory
        overwrite (optional): overwrite existing data
        n_threads (optional): number of threads to parse with
        index_separators (optional): custom separates for source (see help(ankimelon.Reader.open_files))
        replace_chars (optional): List of characters to be removed when processing
        start_at (optional): If parsing was previously interrupted, specify name of file to start with

        """
        starting = False
        paths = [i for i in Path(sources_path).iterdir()]
        for i, path in enumerate(paths):
            if start_at:
                if start_at == path.stem:
                    starting = True
                if not starting:
                    logger.info(f'Skipping source "{path.stem}" because start_at "{start_at}" hat not yet been reached')
                    continue
            logger.info(f'Adding source {i}/{len(paths)}')
            while True:
                try:
                    logger.info(f"Adding {path} to {source_category}")
                    self.add_source(path,
                                    source_category,
                                    n_threads = n_threads,
                                    db_workers=db_workers,
                                    index_separators=index_separators,
                                    replace_chars=replace_chars,
                                    chunk_size=chunk_size,
                                    assert_coherence=assert_coherence,
                                    file_match_pattern = file_match_pattern,
                                    dir_match_pattern = dir_match_pattern)
                    break
                except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                    logger.error(f"sync fail: {e}")

                    logger.error(f"Operational error for {path}:\n\n{e}")
                    time.sleep(300)
                    self.db = DBManager(self.lang)

        setup_conn = self.db.get_safe_conn()
        try:
            with setup_conn:
                with setup_conn.cursor() as cur:
                    logger.info(f'Aggregating lemma frequencies for {source_category}')
                    cur.execute(
                        "SELECT id FROM sources WHERE name = %s AND nesting_level = 0",
                        (source_category,))
                    source_category_id = cur.fetchone()[0]
                    cur.execute(
                        """
                        WITH RECURSIVE down AS (
                            SELECT id, parent_id, is_leaf, lemma_counts
                            FROM sources
                            WHERE id = %s
                        UNION ALL
                            SELECT s.id, s.parent_id, s.is_leaf, s.lemma_counts
                            FROM sources s
                            JOIN down d ON s.parent_id = d.id
                        ),
                        leaves AS (
                            SELECT id
                            FROM down
                            WHERE is_leaf
                        ),
                        pairs AS (
                            SELECT l.id AS leaf_id, l.id AS ancestor_id
                            FROM leaves l
                        UNION ALL
                            SELECT p.leaf_id, s.parent_id AS ancestor_id
                            FROM pairs p
                            JOIN sources s ON s.id = p.ancestor_id
                            JOIN down    d ON d.id = s.parent_id
                        ),
                        counts AS (
                            SELECT
                                p.ancestor_id AS id,
                                j.key,
                                SUM( (j.value)::numeric )::bigint AS total
                            FROM pairs p
                            JOIN down leaf ON leaf.id = p.leaf_id
                            JOIN LATERAL jsonb_each(COALESCE(leaf.lemma_counts, '{}'::jsonb)) AS j(key, value) ON TRUE
                            GROUP BY p.ancestor_id, j.key
                        ),
                        ranked AS (
                            SELECT
                                id, key, total,
                                ROW_NUMBER() OVER (PARTITION BY id ORDER BY total DESC, key ASC) AS rn
                            FROM counts
                        ),
                        top_counts AS (
                            SELECT id, key, total
                            FROM ranked
                            WHERE rn <= 10000
                        ),
                        agg AS (
                            SELECT
                                id,
                                jsonb_object_agg(key, to_jsonb(total)) AS lemma_counts
                            FROM top_counts
                            GROUP BY id
                        )
                        UPDATE sources s
                        SET lemma_counts = a.lemma_counts
                        FROM agg a
                        JOIN down d ON d.id = a.id
                        WHERE s.id = a.id
                        AND d.is_leaf = FALSE
                        RETURNING s.id, a.lemma_counts;
                        """,
                        (source_category_id,),
                    )

        finally:
            self.db.db_pool.putconn(setup_conn)
        logger.info(f'Finish sync_dir for {source_category}')
