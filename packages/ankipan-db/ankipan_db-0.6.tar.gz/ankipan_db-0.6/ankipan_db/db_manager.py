from psycopg2 import pool, sql
import psycopg2
import hashlib
import random
from collections import Counter
import logging
from functools import partial, wraps
import time
import inspect
import heapq
from operator import itemgetter

from typing import Dict, Optional, Tuple, Dict, List

import ankipan_db
from ankipan import TextSegment

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

random.seed(42)

N_CONNS = 20

def with_pool_cursor(func):
    @wraps(func)
    def wrapper(self, *args, **kwargs):
        conn = self.get_safe_conn()
        try:
            with conn.cursor() as cur:
                return func(self, cur, *args, **kwargs)
        finally:
            self.db_pool.putconn(conn)
    return wrapper

def with_conditional_pool_conn(func):
    sig = inspect.signature(func)
    has_conn = 'conn' in sig.parameters

    @wraps(func)
    def wrapper(self, *args, **kwargs):
        if not has_conn:
            return func(self, *args, **kwargs)

        try:
            bound = sig.bind_partial(self, *args, **kwargs)
        except TypeError:
            return func(self, *args, **kwargs)

        already_has_conn = ('conn' in bound.arguments) and (bound.arguments['conn'] is not None)
        if already_has_conn:
            return func(self, *args, **kwargs)

        conn = self.get_safe_conn()
        try:
            call_kwargs = {k: v for k, v in bound.arguments.items() if k != 'self'}
            call_kwargs['conn'] = conn
            return func(self, **call_kwargs)
        finally:
            self.db_pool.putconn(conn)
    return wrapper

class DBManager:
    def __init__(self, lang):
        logger.info("DBManager initializing...")
        if any(i is None for i in ankipan_db.db_config.values()):
            raise RuntimeError('Invalid .env file')
        self.db_pool = pool.ThreadedConnectionPool(
            minconn=1,
            maxconn=N_CONNS,
            options=f"-c search_path={lang}",
            **ankipan_db.db_config,
        )
        self.lang = lang

    def get_safe_conn(self, max_attempts=N_CONNS + 1, delay=0.05):
        last = None
        backoff = delay
        for _ in range(max_attempts):
            conn = self.db_pool.getconn()
            returned = False
            try:
                if getattr(conn, "closed", 0):
                    raise psycopg2.InterfaceError("connection already closed")
                conn.rollback()
                with conn.cursor() as cur:
                    cur.execute("SELECT 1")
                return conn
            except (psycopg2.OperationalError, psycopg2.InterfaceError) as e:
                last = e
                try:
                    self.db_pool.putconn(conn, close=True)
                    returned = True
                except Exception:
                    pass
                time.sleep(backoff)
                backoff = min(backoff * 2, 0.5)
                continue
            except Exception:
                try:
                    self.db_pool.putconn(conn)
                    returned = True
                except Exception:
                    pass
                raise
            finally:
                if not returned and False:
                    self.db_pool.putconn(conn)
        raise last

    # TODO maybe try to prefer already-translated text segments to reduce computational load
    @with_pool_cursor
    def get_segments_for_lemma(
        self,
        cur,
        relative_source_paths: List[str],
        lemma: str,
        source_category: str,
        ideal_sentence_length: int,
        native_lang: str = None,
        n_sentences: int = 8,
        sigma: float = 5,
        n_neighbours: int = 1,
        prune_mult: float = 4.0,
        debug: bool = False,
    ) -> dict:
        """
        - Selects n_sentences from known and unknown sources, returned as text segments of length>=1 and length<=1+n_neighbours*2
        - Computes gaussian weight in SQL (float8-safe, underflow-clamped)
        - Weighted sampling w/o replacement via Efraimidis–Spirakis (key = -ln(U)/w)
        - Diversity: round-robin across source_root (change partition if you want per-video)
        - Optional neighbour expansion (id ± k) constrained to same source_id (in SQL)
        - Two passes (KNOWN includes; UNKNOWN excludes); then balance to reach n_sentences
        Returns:
        {
            "entries_from_known_sources": [TextSegment, ...],
            "entries_from_unknown_sources": [TextSegment, ...],
        }
        """

        def _category_id() -> int:
            cur.execute(
                "SELECT id FROM sources WHERE name=%s AND nesting_level=0",
                (source_category,),
            )
            row = cur.fetchone()
            if not row:
                raise RuntimeError(f'Source Category "{source_category}" not defined in db')
            return row[0]

        def _descendant_ids(paths: Optional[List[str]]) -> List[int]:
            if not paths:
                return []
            out: List[int] = []
            for p in paths:
                parts = [source_category] + [x for x in p.strip("/").split("/") if x]
                cur.execute("SELECT source_id_from_path(VARIADIC %s)", (parts,))
                r = cur.fetchone()
                if not r:
                    raise RuntimeError(f'Path "{p}" not found under "{source_category}"')
                root_id = r[0]
                cur.execute("SELECT id FROM source_descendants(%s)", (root_id,))
                out.extend(sid for (sid,) in cur.fetchall())
            return out

        def _set_pg_seed(tag: str) -> None:
            # Ensure identical inputs (lemma, paths, native lang, etc.) yield identical ordering.
            norm_paths = sorted(relative_source_paths or [])
            seed_input = "\x1f".join(
                [
                    lemma or "",
                    native_lang or "",
                    source_category or "",
                    ",".join(norm_paths),
                    tag,
                ]
            )
            digest = hashlib.sha256(seed_input.encode("utf-8")).digest()
            seed_float = int.from_bytes(digest[:8], "big") / float(1 << 64)
            cur.execute("SELECT setseed(%s)", (seed_float,))

        def _sql_pick_weighted_rr(
            *,
            lemma: str,
            cat_id: int,
            include_ids: Optional[List[int]] = None,
            exclude_ids: Optional[List[int]] = None,
            ideal_len: int,
            sigma: float,
            limit_n: int,
            n_neighbours: int,
            prune_mult: float,
        ) -> List[dict]:
            """
            Weighted random sample with diversity (done in SQL):
            - Compute weight = exp(-(Δ^2)/(2σ^2)) (float8-safe, exponent clamped at -700)
            - key = -ln(U)/weight (smaller is better)
            - Round-robin: rn_per_root = row_number() over (source_root order by key)
            - ORDER BY rn_per_root, key LIMIT limit_n
            - Expand neighbours via LATERAL generate_series (id±k) within same source_id
            """
            sql = """
            WITH cat AS (SELECT %(cat_id)s::int AS id),

            cand AS (
            SELECT
                ts.id   AS tseg_id,
                ts.text AS text,
                COALESCE(ts.len, char_length(ts.text))::int AS length,
                ts.source_id       AS source_id,
                src.name           AS source_name,
                src.metadata       AS metadata,
                ts.start_s         AS start_s,
                ts.end_s           AS end_s,
                (
                WITH RECURSIVE up AS (
                    SELECT s.id, s.parent_id, s.name
                    FROM sources s WHERE s.id = ts.source_id
                    UNION ALL
                    SELECT p.id, p.parent_id, p.name
                    FROM sources p JOIN up u ON p.id = u.parent_id
                )
                SELECT u2.name
                FROM up u2
                WHERE u2.parent_id = (SELECT id FROM cat)  -- strict 2nd level under category
                LIMIT 1
                ) AS source_root,

                CASE
                WHEN %(sigma)s::float8 > 0.0 THEN
                    EXP(
                    GREATEST(
                        -0.5::float8 * POWER(
                        (COALESCE(ts.len, char_length(ts.text))::float8 - %(ideal)s::float8)
                        / NULLIF(%(sigma)s::float8, 0.0),
                        2
                        ),
                        -700.0::float8
                    )
                    )
                ELSE 1.0::float8
                END AS weight

            FROM lemmas l
            JOIN words w               ON w.lemma_id = l.id
            JOIN words_in_text_segments wits ON wits.word_id = w.id
            JOIN text_segments ts      ON ts.id = wits.text_segment_id
            JOIN sources src           ON src.id = ts.source_id
            WHERE l.lemma = %(lemma)s
                AND ts.source_id = ANY (SELECT id FROM source_descendants((SELECT id FROM cat)))
                AND (%(has_includes)s = FALSE OR ts.source_id = ANY (%(include_ids)s))
                AND (%(has_excludes)s = FALSE OR ts.source_id <> ALL (%(exclude_ids)s))
                AND (
                %(sigma)s::float8 <= 0.0 OR
                ABS(COALESCE(ts.len, char_length(ts.text))::int - %(ideal)s::int)
                    <= CEIL(%(sigma)s::float8 * %(prune_mult)s)
                )
            ),

            randomized AS (
            SELECT
                c.*,
                -- Efraimidis–Spirakis key; guard U and weight against extremes
                (-LN(LEAST(GREATEST(random(), 1e-12), 1.0 - 1e-12))
                / GREATEST(c.weight, 1e-300)) AS key
            FROM cand c
            ),

            ranked AS (
            SELECT
                *,
                ROW_NUMBER() OVER (
                PARTITION BY source_root
                ORDER BY key ASC, tseg_id DESC
                ) AS rn_per_root
            FROM randomized
            ),

            picked AS (
            SELECT *
            FROM ranked
            ORDER BY rn_per_root ASC, key ASC, tseg_id DESC
            LIMIT %(limit_n)s
            ),

            neigh AS (
            SELECT
                p.*,
                arr.ids    AS neighbour_ids,
                arr.texts  AS neighbour_texts,
                arr.starts AS neighbour_starts,
                arr.ends   AS neighbour_ends,
                GREATEST(array_position(arr.ids, p.tseg_id) - 1, 0) AS main_index
            FROM picked p
            JOIN LATERAL (
                SELECT
                array_agg(n.id      ORDER BY n.id) AS ids,
                array_agg(n.text    ORDER BY n.id) AS texts,
                array_agg(n.start_s ORDER BY n.id) AS starts,
                array_agg(n.end_s   ORDER BY n.id) AS ends
                FROM generate_series(p.tseg_id - %(k)s, p.tseg_id + %(k)s) g(id)
                JOIN text_segments n
                ON n.id = g.id
                AND n.source_id = p.source_id
            ) arr ON TRUE
            )

            SELECT
            tseg_id, source_id, source_name, source_root,
            start_s, end_s, metadata, length,
            neighbour_texts, neighbour_starts, neighbour_ends,
            main_index
            FROM neigh;
            """
            params = {
                "lemma": lemma,
                "cat_id": cat_id,
                "ideal": ideal_len,
                "sigma": float(sigma),
                "has_includes": bool(include_ids),
                "include_ids": include_ids or [],
                "has_excludes": bool(exclude_ids),
                "exclude_ids": exclude_ids or [],
                "limit_n": int(limit_n),
                "k": int(n_neighbours),
                "prune_mult": float(prune_mult),
            }
            cur.execute(sql, params)
            cols = [d[0] for d in cur.description]
            return [dict(zip(cols, row)) for row in cur.fetchall()]

        cat_id = _category_id()
        half = n_sentences // 2
        include_ids = _descendant_ids(relative_source_paths)
        if len(relative_source_paths) > 0:
            _set_pg_seed("known")
            known = _sql_pick_weighted_rr(
                lemma=lemma, cat_id=cat_id,
                include_ids=include_ids or None,
                ideal_len=ideal_sentence_length, sigma=sigma,
                limit_n=n_sentences, n_neighbours=n_neighbours,
                prune_mult=prune_mult,
            )
        else:
            known = []
        _set_pg_seed("unknown")
        unknown = _sql_pick_weighted_rr(
            lemma=lemma, cat_id=cat_id,
            exclude_ids=include_ids or None,
            ideal_len=ideal_sentence_length, sigma=sigma,
            limit_n=n_sentences, n_neighbours=n_neighbours,
            prune_mult=prune_mult,
        )
        # Balance: aim ~half unknown; if unknown is short, keep more known (and vice versa)
        u_avail, k_avail = len(unknown), len(known)
        desired_u = min(u_avail, max(half, n_sentences - k_avail))
        desired_k = min(k_avail, n_sentences - desired_u)
        total = desired_k + desired_u
        if total < n_sentences:
            need = n_sentences - total
            k_rem = max(0, k_avail - desired_k)
            u_rem = max(0, u_avail - desired_u)
            while need > 0 and (k_rem > 0 or u_rem > 0):
                if k_rem >= u_rem and k_rem > 0:
                    desired_k += 1; k_rem -= 1
                elif u_rem > 0:
                    desired_u += 1; u_rem -= 1
                need -= 1

        final_known = [(entry, True) for entry in known[:desired_k]]
        final_unknown = [(entry, False) for entry in unknown[:desired_u]]
        res = {'source_category': source_category, "segments": {}}

        combined = final_known + final_unknown
        total_for_shallow_sources = Counter(
            r['source_root']
            for r, is_known in combined
            if r['source_root'] == r['source_name']
        )

        counter_for_shallow_sources = Counter()
        for r, is_known in combined:
            source_root = r['source_root']
            source_name = r['source_name']
            display_source_name: str
            if source_root == source_name:
                counter_for_shallow_sources[source_root] += 1
                current_idx = counter_for_shallow_sources[source_root]
                total = total_for_shallow_sources[source_root]
                display_source_name = f"entry {current_idx}/{total}"
            else:
                display_source_name = source_name

            ts = TextSegment(
                word=lemma,
                text_segments=r["neighbour_texts"] or [""],
                main_index=r["main_index"] if r["main_index"] is not None else 0,
                start_s=r.get("start_s"),
                end_s=r.get("end_s"),
                translation=None,
                source_name=display_source_name,
            )

            key = 'entries_from_known_sources' if is_known else 'entries_from_unknown_sources'
            res["segments"].setdefault(key, {}).setdefault(source_root, []).append(ts)
        return res

    def cache_translations(self, text_segments: List[TextSegment], native_lang: str):
        """
        Insert cache rows into translations(lang, hash, translation) based on the
        concatenated window (' ' join) of each TextSegment's text_segments.
        """
        if not text_segments:
            return

        def _digest_for_segments(text_segments: List[str]) -> bytes:
            # Must match the SQL aggregation: single spaces, exact text
            s = ' '.join(text_segments)
            return hashlib.sha256(s.encode('utf-8')).digest()

        rows = []
        for ts in text_segments:
            if not getattr(ts, 'translation', None):
                continue
            # use provided hash if already present on the object (e.g., from get_segments_for_lemmas),
            # otherwise compute it
            h = getattr(ts, 'hash', None)
            if h is None:
                h = _digest_for_segments(ts.text_segments)
            elif isinstance(h, memoryview):
                h = bytes(h)
            rows.append((native_lang, h, ts.translation))

        if not rows:
            return

        conn = self.get_safe_conn()
        try:
            with conn.cursor() as cur:
                cur.executemany(
                    """
                    INSERT INTO translations (lang, hash, translation)
                    VALUES (%s, %s, %s)
                    ON CONFLICT (lang, hash) DO NOTHING
                    """,
                    rows
                )
            conn.commit()
        finally:
            self.db_pool.putconn(conn)

    @with_pool_cursor
    def get_translations_from_cache(
        self,
        cur,
        example_sentences: List[TextSegment],
        native_lang: str,
    ) -> Dict[int, str]:
        """
        Returns all translations that are found in cache (list index -> translation string)
        """
        import hashlib

        if not example_sentences:
            return {}

        idxs = list(range(len(example_sentences)))
        originals = [' '.join(s.text_segments) for s in example_sentences]
        digests = [hashlib.sha256(o.encode("utf-8")).digest() for o in originals]

        cur.execute(
            """
            WITH input(idx, digest) AS (
            SELECT * FROM unnest(%s::int[], %s::bytea[])
            )
            SELECT i.idx, t.translation
            FROM input i
            JOIN translations t
            ON t.lang = %s
            AND t.hash = i.digest
            """,
            (idxs, digests, native_lang),
        )

        result: Dict[int, str] = {}
        for idx, translation in cur.fetchall():
            result[idx] = translation
        return result

    @with_pool_cursor
    def get_synonym_explanations_from_cache(
        self,
        cur,
        words,
    ) -> int:
        """
        Collect cached synonym explanations
        """
        cur.execute(
            """
            SELECT lemma, explanation
            FROM synonym_explanations
            WHERE lemma = ANY(%s)
            """,
            (words,),
        )
        return dict(cur.fetchall())

    def cache_synonym_explanations(
        self,
        lemma,
        explanation,
    ) -> int:
        """
        Collect cached synonym explanations
        """
        conn = self.get_safe_conn()
        try:
            with conn.cursor() as cur:
                cur.execute(
                    """
                    INSERT INTO synonym_explanations (lemma, explanation)
                    VALUES (%s, %s)
                    ON CONFLICT DO NOTHING
                    """,
                    (lemma, explanation),
                )
                conn.commit()
        finally:
            self.db_pool.putconn(conn)

    @with_pool_cursor
    def get_available_source_categories(self, cur) -> List[str]:
        sql_roots = """
            SELECT so.name
            FROM   sources so
            WHERE parent_id IS NULL
        """
        params = []
        cur.execute(sql_roots, tuple(params))
        return [source_category[0] for source_category in cur.fetchall()]

    @with_pool_cursor
    def get_invalid_source_paths(self, cur, source_paths: List[str]):
        invalid = []
        for source_path in source_paths:
            cur.execute(f"SELECT {self.lang}.source_id_from_path(VARIADIC %s)", (source_path.split('/'),))
            if len([i for i in cur.fetchone()]) == 0:
                invalid.append(source_path)
        return invalid

    @with_pool_cursor
    def get_source_list(self, cur, source_path: str):
        path_parts = source_path.split('/')
        cur.execute(f"SELECT {self.lang}.source_id_from_path(VARIADIC %s)", (path_parts,))
        root_id = cur.fetchone()[0]
        cur.execute("SELECT metadata, lemma_counts FROM sources WHERE id = %s", (root_id,))
        root_meta, lemma_counts = cur.fetchone()
        if lemma_counts and len(lemma_counts) > 10_000:
            lemma_counts = heapq.nlargest(10_000, lemma_counts.items(), key=itemgetter(1))
        cur.execute(
            """
            SELECT name
            FROM   sources
            WHERE  parent_id = %s
            ORDER  BY name
            """, (root_id,))
        children = []
        for name in cur.fetchall():
            children.append(name[0])
        return root_meta, lemma_counts, children

    def get_source_tree_for_id(self, cur, root_id: int) -> dict[int, tuple[int | None, str]]:
        """
        Returns {id: (parent_id, name, is_leaf)} for all nodes under `root_id`
        (including the root itself).
        """
        cur.execute(
            """
            WITH RECURSIVE tree AS (
                SELECT id, parent_id, name, is_leaf
                FROM sources
                WHERE id = %s
                UNION ALL
                SELECT s.id, s.parent_id, s.name, s.is_leaf
                FROM sources s
                JOIN tree t ON s.parent_id = t.id
            )
            SELECT id, parent_id, name, is_leaf
            FROM tree;
            """,
            (root_id,),
        )
        return {row_id: (parent_id, name, is_leaf) for row_id, parent_id, name, is_leaf in cur.fetchall()}

    @with_pool_cursor
    def get_lemma_percentiles(self, cur, source_path, lemmas):
        cur.execute(f"SELECT {self.lang}.source_id_from_path(VARIADIC %s)", (source_path.split('/'),))
        root_id = cur.fetchone()[0]
        print("root_id",root_id)
        cur.execute("SELECT lemma_counts FROM sources WHERE id = %s", (root_id,))
        lemma_counts = cur.fetchone()[0]
        print("lemma_counts",lemma_counts)
        counter = Counter(lemma_counts)
        common = [word for word, count in counter.most_common()]
        return {lemma: (common.index(lemma) / len(counter) if counter[lemma] != 1 else 1.0)
                 for lemma in lemmas if lemma in common}

    def delete_source(self, cur, root_id: int) -> dict[str, int]:
        q1 = f"""
            WITH d AS (SELECT id FROM {self.lang}.source_descendants(%s)),
                seg AS (SELECT ts.id FROM {self.lang}.text_segments ts JOIN d ON ts.source_id = d.id)
            DELETE FROM {self.lang}.words_in_text_segments w
            USING seg
            WHERE w.text_segment_id = seg.id;
        """

        q2 = f"""
            WITH d AS (SELECT id FROM {self.lang}.source_descendants(%s))
            DELETE FROM {self.lang}.text_segments ts
            USING d
            WHERE ts.source_id = d.id;
        """

        q3 = f"""
            WITH d AS (
                SELECT s.id, s.nesting_level
                FROM {self.lang}.source_descendants(%s) AS d(id)
                JOIN {self.lang}.sources s ON s.id = d.id
            )
            DELETE FROM {self.lang}.sources s
            USING d
            WHERE s.id = d.id;
        """

        cur.execute(q1, (root_id,))
        deleted_wits = cur.rowcount
        cur.execute(q2, (root_id,))
        deleted_segments = cur.rowcount
        cur.execute(q3, (root_id,))
        deleted_sources = cur.rowcount

    @with_conditional_pool_conn
    def make_schema(self, conn=None):
        schema = self.lang

        commands = [
            f"CREATE SCHEMA IF NOT EXISTS {schema};",
            "CREATE EXTENSION IF NOT EXISTS pgcrypto;",

            f"""
            CREATE TABLE {schema}.translations (
            lang text NOT NULL,
            hash bytea NOT NULL,
            translation text NOT NULL,
            PRIMARY KEY (lang, hash)
            );
            """,
            f"""
            CREATE TABLE {schema}.synonym_explanations (
            lemma TEXT PRIMARY KEY,
            explanation TEXT NOT NULL
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS {schema}.lemmas (
                id SERIAL PRIMARY KEY,
                lemma TEXT NOT NULL UNIQUE
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS {schema}.words (
                id SERIAL PRIMARY KEY,
                word TEXT NOT NULL,
                pos VARCHAR(20),
                xpos VARCHAR(20),
                lemma_id INTEGER NOT NULL REFERENCES {schema}.lemmas(id),
                UNIQUE(word, pos)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS {schema}.sources (
                id SERIAL PRIMARY KEY,
                parent_id INT REFERENCES {schema}.sources(id) ON DELETE CASCADE,
                name TEXT NOT NULL,
                metadata jsonb,
                lemma_counts jsonb,
                nesting_level INT NOT NULL,
                is_leaf BOOL NOT NULL,
                UNIQUE (parent_id, name)
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS {schema}.text_segments (
                id SERIAL PRIMARY KEY,
                "index" INTEGER NOT NULL,
                text TEXT NOT NULL,
                start_s INTEGER,
                end_s INTEGER,
                source_id INTEGER NOT NULL REFERENCES {schema}.sources(id) ON DELETE CASCADE,
                len INTEGER GENERATED ALWAYS AS (char_length(text)) STORED
            );
            """,
            f"""
            CREATE TABLE IF NOT EXISTS {schema}.words_in_text_segments (
                word_id INTEGER NOT NULL REFERENCES {schema}.words(id),
                text_segment_id INTEGER NOT NULL REFERENCES {schema}.text_segments(id) ON DELETE CASCADE
            );
            """,

            # UNIQUE indexes needed for ON CONFLICT
            # (sources has UNIQUE(parent_id, name), lemmas has UNIQUE(lemma), words has UNIQUE(word,pos) already)
            f'CREATE UNIQUE INDEX IF NOT EXISTS uq_text_segments_source_index '
            f'  ON {schema}.text_segments (source_id, "index");',

            f'CREATE UNIQUE INDEX IF NOT EXISTS uq_wits '
            f'  ON {schema}.words_in_text_segments (word_id, text_segment_id);',

            f"""
            CREATE OR REPLACE FUNCTION {schema}.source_descendants(root_id int)
            RETURNS TABLE(id int)
            LANGUAGE sql
            SET search_path = {schema}
            AS $$
                WITH RECURSIVE d(id) AS (
                    SELECT id FROM {schema}.sources WHERE id = $1
                    UNION ALL
                    SELECT s.id FROM {schema}.sources s JOIN d ON s.parent_id = d.id
                )
                SELECT id FROM d;
            $$;
            """,
            f"""
            CREATE OR REPLACE FUNCTION {schema}.source_id_from_path(VARIADIC p_names text[])
            RETURNS int
            LANGUAGE plpgsql
            SET search_path = {schema}
            AS $$
            DECLARE
                part text;
                pid  int := NULL;
            BEGIN
                FOREACH part IN ARRAY p_names LOOP
                    SELECT id INTO pid
                    FROM   {schema}.sources
                    WHERE  parent_id IS NOT DISTINCT FROM pid
                    AND    name = part
                    LIMIT 1;
                    IF pid IS NULL THEN
                        RAISE EXCEPTION 'Path element "%" not found', part;
                    END IF;
                END LOOP;
                RETURN pid;
            END;
            $$;
            """,
            f"""
            CREATE OR REPLACE FUNCTION {schema}.lemmas_with_counts(root_id int)
            RETURNS TABLE(lemma text, cnt int)
            LANGUAGE sql
            SET search_path = {schema}
            AS $$
                SELECT l.lemma,
                    COUNT(*) AS cnt
                FROM   {schema}.source_descendants(root_id) d
                JOIN   {schema}.text_segments ts   ON ts.source_id = d.id
                JOIN   {schema}.words_in_text_segments wits ON wits.text_segment_id = ts.id
                JOIN   {schema}.words w    ON w.id = wits.word_id
                JOIN   {schema}.lemmas l   ON l.id = w.lemma_id
                GROUP  BY l.lemma
                ORDER  BY cnt DESC;
            $$;
            """,
            f"""
            CREATE OR REPLACE VIEW {schema}.source_root_lookup AS
            WITH RECURSIVE link(id, root_id, root_name) AS (
                SELECT id, id AS root_id, name AS root_name
                FROM   {schema}.sources
                WHERE  parent_id IS NULL
                UNION ALL
                SELECT s.id, l.root_id, l.root_name
                FROM   {schema}.sources s
                JOIN   link l ON s.parent_id = l.id
            )
            SELECT * FROM link;
            """,

            f"CREATE INDEX IF NOT EXISTS idx_lemmas_lemma ON {schema}.lemmas (lemma);",
            f"CREATE INDEX IF NOT EXISTS idx_words_lemma_id ON {schema}.words (lemma_id);",
            f"CREATE INDEX IF NOT EXISTS idx_text_segments_source_id ON {schema}.text_segments (source_id);",
        ]

        with conn.cursor() as cur:
            for cmd in commands:
                cur.execute(cmd)
        conn.commit()
