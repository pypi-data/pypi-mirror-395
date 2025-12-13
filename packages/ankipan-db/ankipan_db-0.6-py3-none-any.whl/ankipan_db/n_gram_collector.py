from __future__ import annotations
from dataclasses import dataclass
from typing import List, Tuple, Dict, Iterable, Set, Optional
import math
import re

from psycopg2.extensions import connection as Connection


class NGramCollector:
    MAX_LEFT = 20
    MAX_RIGHT = 20
    MIN_SEGMENTS = 5
    TOP_K = 5
    BEAM_WIDTH = 3
    MIN_RETENTION = 0.20
    RETENTION_START_LEN = 2
    COLLAPSE_BY_BRANCH = True
    MAX_OCCS = 500_000  # max number of occurrences to consider per query

    @classmethod
    def get_text_segments_for_lemma(
        cls,
        conn: Connection,
        lemma: str,
        *,
        source_root_id: Optional[int] = None,
        limit: Optional[int] = None,
    ) -> list[tuple[int, str]]:
        sql_text = """
            SELECT DISTINCT ts.id, ts.text
            FROM words AS w
            JOIN lemmas AS l ON l.id = w.lemma_id
            JOIN words_in_text_segments AS wits ON wits.word_id = w.id
            JOIN text_segments AS ts ON ts.id = wits.text_segment_id
            WHERE l.lemma = %s
        """
        params: list[object] = [lemma]
        if source_root_id is not None:
            sql_text += " AND ts.source_id = ANY (SELECT id FROM source_descendants(%s))"
            params.append(source_root_id)
        sql_text += " ORDER BY ts.id"
        if limit is not None:
            sql_text += " LIMIT %s"
            params.append(limit)
        with conn.cursor() as cur:
            cur.execute(sql_text, params)
            return cur.fetchall()

    @classmethod
    def get_wordforms_for_lemma(cls, conn: Connection, lemma: str) -> list[str]:
        sql_text = """
            SELECT DISTINCT w.word
            FROM words AS w
            JOIN lemmas AS l ON l.id = w.lemma_id
            WHERE l.lemma = %s
            ORDER BY w.word
        """
        with conn.cursor() as cur:
            cur.execute(sql_text, (lemma,))
            rows = cur.fetchall()
        return [r[0] for r in rows]

    @staticmethod
    def _find_occurrences(
        text: str,
        word: str,
        enforce_word_boundaries: bool,
    ) -> Iterable[Tuple[int, int]]:
        if not word:
            return
        if enforce_word_boundaries:
            # lookahead to allow overlapping matches if needed; we still treat each match as [start, end)
            pat = re.compile(rf"(?=(?<!\w){re.escape(word)}(?!\w))", flags=re.UNICODE)
            for m in pat.finditer(text):
                s = m.start()
                yield s, s + len(word)
        else:
            start, L = 0, len(word)
            while True:
                i = text.find(word, start)
                if i == -1:
                    break
                yield i, i + L
                start = i + 1

    @dataclass(frozen=True)
    class Occ:
        seg_id: int
        start: int
        end: int
        text: str
        wf: str

    @dataclass
    class Node:
        left: str
        right: str
        occs: List["NGramCollector.Occ"]

        @property
        def support(self) -> int:
            # number of distinct segments
            return len({o.seg_id for o in self.occs})

        def dominant_wordform(self) -> str:
            counts: Dict[str, int] = {}
            for o in self.occs:
                counts[o.wf] = counts.get(o.wf, 0) + 1
            # tie-break by wordform lexicographically for determinism
            return max(counts.items(), key=lambda kv: (kv[1], kv[0]))[0]

    @staticmethod
    def _is_stricter_extension(
        child: "NGramCollector.Node",
        parent: "NGramCollector.Node",
    ) -> bool:
        if child is parent:
            return False
        return (
            child.left.endswith(parent.left)
            and child.right.startswith(parent.right)
            and (len(child.left) > len(parent.left) or len(child.right) > len(parent.right))
        )

    @classmethod
    def _collapse_same_branch_by_right(
        cls,
        nodes: List["NGramCollector.Node"],
    ) -> List["NGramCollector.Node"]:
        grouped: Dict[str, List[NGramCollector.Node]] = {}
        for n in nodes:
            grouped.setdefault(n.right, []).append(n)
        kept: List[NGramCollector.Node] = []
        for right, group in grouped.items():
            group.sort(key=lambda n: (len(n.left), n.support), reverse=True)
            chosen: List[NGramCollector.Node] = []
            for n in group:
                if any(cls._is_stricter_extension(c, n) for c in chosen):
                    continue
                chosen.append(n)
            kept.extend(chosen)
        return kept

    @classmethod
    def most_common_contexts_from_segments(
        cls,
        segments: List[Tuple[int, str]],
        wordforms: List[str],
        enforce_word_boundaries: bool,
        *,
        max_left: int = MAX_LEFT,
        max_right: int = MAX_RIGHT,
        min_segments: int = MIN_SEGMENTS,
        top_k: int = TOP_K,
        beam_width: int = BEAM_WIDTH,
        min_retention: float = MIN_RETENTION,
        retention_start_len: int = RETENTION_START_LEN,
        collapse_by_branch: bool = COLLAPSE_BY_BRANCH,
        max_occs: Optional[int] = None,
    ) -> List[Tuple[str, int, str]]:
        if not all(isinstance(w, str) for w in wordforms):
            raise TypeError("wordforms must be list[str]")

        if max_occs is None:
            max_occs = cls.MAX_OCCS
        if max_occs <= 0:
            raise ValueError("max_occs must be positive")

        # collect occurrences, but cap at max_occs for very frequent lemmas
        seen_positions: Set[Tuple[int, int, int]] = set()
        occs: List[NGramCollector.Occ] = []

        for seg_id, text in segments:
            if len(occs) >= max_occs:
                break
            for wf in wordforms:
                if len(occs) >= max_occs:
                    break
                for s, e in cls._find_occurrences(text, wf, enforce_word_boundaries):
                    pos = (seg_id, s, e)
                    if pos in seen_positions:
                        continue
                    seen_positions.add(pos)
                    occs.append(cls.Occ(seg_id=seg_id, start=s, end=e, text=text, wf=wf))
                    if len(occs) >= max_occs:
                        break

        if not occs:
            return []

        root = cls.Node("", "", occs)
        visited: Set[Tuple[str, str]] = {("", "")}
        frontier: List[NGramCollector.Node] = [root]
        terminals: List[NGramCollector.Node] = []

        def expand(node: NGramCollector.Node, side: str) -> List[NGramCollector.Node]:
            L, R = len(node.left), len(node.right)
            depth = L + R
            parent_support = node.support
            buckets: Dict[str, List[NGramCollector.Occ]] = {}

            for o in node.occs:
                if side == "L":
                    idx = o.start - L - 1
                    if idx >= 0:
                        buckets.setdefault(o.text[idx], []).append(o)
                else:
                    idx = o.end + R
                    if idx < len(o.text):
                        buckets.setdefault(o.text[idx], []).append(o)

            if not buckets:
                return []

            if depth >= retention_start_len:
                gate = max(min_segments, math.ceil(min_retention * parent_support))
            else:
                gate = min_segments

            children: List[NGramCollector.Node] = []
            for ch, bucket in buckets.items():
                sup = len({oo.seg_id for oo in bucket})
                if sup < gate:
                    continue
                left = ch + node.left if side == "L" else node.left
                right = node.right if side == "L" else node.right + ch
                key = (left, right)
                if key in visited:
                    continue
                visited.add(key)
                children.append(cls.Node(left, right, bucket))

            children.sort(
                key=lambda n: (n.support, len(n.left) + len(n.right)),
                reverse=True,
            )
            return children[:beam_width]

        while frontier:
            next_frontier: List[NGramCollector.Node] = []
            for node in frontier:
                grew = False
                if len(node.left) < max_left:
                    kids = expand(node, "L")
                    if kids:
                        grew = True
                        next_frontier.extend(kids)
                if len(node.right) < max_right:
                    kids = expand(node, "R")
                    if kids:
                        grew = True
                        next_frontier.extend(kids)
                if (len(node.left) + len(node.right)) >= 1 and not grew:
                    terminals.append(node)

            # deduplicate within this layer, keep strongest support
            dedup_layer: Dict[Tuple[str, str], NGramCollector.Node] = {}
            for n in next_frontier:
                k = (n.left, n.right)
                if k not in dedup_layer or n.support > dedup_layer[k].support:
                    dedup_layer[k] = n
            frontier = list(dedup_layer.values())

        candidates = (
            cls._collapse_same_branch_by_right(terminals)
            if collapse_by_branch
            else terminals
        )
        candidates.sort(
            key=lambda n: (n.support, len(n.left) + len(n.right)),
            reverse=True,
        )

        return [
            (f"{n.left}{n.dominant_wordform()}{n.right}", n.support, n.dominant_wordform())
            for n in candidates[:top_k]
        ]

    @classmethod
    def get_frequent_contexts_for_lemma(
        cls,
        db: "DBManager",
        lemma: str,
    ) -> list[tuple[str, int, str]]:
        """
        Fetch segments and wordforms for a lemma and return its most frequent contexts.
        """
        conn: Optional[Connection] = None
        try:
            conn = db.get_safe_conn()
            segments = cls.get_text_segments_for_lemma(conn, lemma=lemma)
            wordforms = cls.get_wordforms_for_lemma(conn, lemma=lemma)
            return cls.most_common_contexts_from_segments(
                segments,
                wordforms,
                enforce_word_boundaries=(db.lang not in ["jp"]),  # adjust if you want 'zh', 'ko' too
                max_left=cls.MAX_LEFT,
                max_right=cls.MAX_RIGHT,
                min_segments=cls.MIN_SEGMENTS,
                top_k=cls.TOP_K,
                beam_width=cls.BEAM_WIDTH,
                min_retention=cls.MIN_RETENTION,
                retention_start_len=cls.RETENTION_START_LEN,
                collapse_by_branch=cls.COLLAPSE_BY_BRANCH,
                max_occs=cls.MAX_OCCS,
            )
        finally:
            if getattr(db, "db_pool", None) and conn is not None:
                db.db_pool.putconn(conn)
