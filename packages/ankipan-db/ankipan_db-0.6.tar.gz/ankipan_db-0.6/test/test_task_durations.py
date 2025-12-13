import os
import statistics
import time

import pytest

import ankipan_db
from ankipan_db import NGramCollector


CANDIDATE_JP_LEMMAS = ["何", "する", "ある", "人", "時", "行く", "来る"]
SOURCE_CATEGORY = "youtube"
IDEAL_SENTENCE_LENGTH = 12
TOLERANCE_SECONDS = 3.0


@pytest.fixture(scope="module")
def jp_db():
    return ankipan_db.DBManager("jp")


def _pick_existing_lemma(db: ankipan_db.DBManager, candidates):
    """Return the first lemma from candidates that exists in the DB, or skip."""
    conn = db.get_safe_conn()
    try:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT lemma FROM lemmas WHERE lemma = ANY(%s::text[]) ORDER BY lemma LIMIT 1",
                (candidates,),
            )
            row = cur.fetchone()
            if not row:
                cur.execute("SELECT lemma FROM lemmas ORDER BY id LIMIT 1")
                row = cur.fetchone()
            if row:
                return row[0]
    finally:
        db.db_pool.putconn(conn)
    pytest.skip("No lemmas found in database")


def _average_duration(samples):
    return statistics.mean(samples) if samples else 0.0


def test_get_segments_for_lemma_duration(jp_db):
    lemma = _pick_existing_lemma(jp_db, CANDIDATE_JP_LEMMAS)
    # Warm-up to avoid first-call overhead skewing averages.
    jp_db.get_segments_for_lemma(
        [],
        lemma,
        SOURCE_CATEGORY,
        ideal_sentence_length=IDEAL_SENTENCE_LENGTH,
        native_lang="en",
        n_sentences=4,
        sigma=2,
    )

    durations = []
    for _ in range(3):
        start = time.perf_counter()
        jp_db.get_segments_for_lemma(
            [],
            lemma,
            SOURCE_CATEGORY,
            ideal_sentence_length=IDEAL_SENTENCE_LENGTH,
            native_lang="en",
            n_sentences=4,
            sigma=2,
        )
        durations.append(time.perf_counter() - start)

    avg = _average_duration(durations)
    assert abs(avg - ankipan_db.GET_SEGMENTS_FOR_LEMMA_EXPECTED_AVERAGE_SECONDS) < TOLERANCE_SECONDS, (
        f"Average duration {avg:.2f}s for get_segments_for_lemma (lemma='{lemma}') exceeded tolerance "
        f"of ±{TOLERANCE_SECONDS}s around expected {ankipan_db.GET_SEGMENTS_FOR_LEMMA_EXPECTED_AVERAGE_SECONDS}s"
    )


def test_frequent_contexts_duration(jp_db):
    lemma = _pick_existing_lemma(jp_db, CANDIDATE_JP_LEMMAS)
    # Warm-up to avoid first-call overhead skewing averages.
    NGramCollector.get_frequent_contexts_for_lemma(jp_db, lemma)

    durations = []
    for _ in range(3):
        start = time.perf_counter()
        NGramCollector.get_frequent_contexts_for_lemma(jp_db, lemma)
        durations.append(time.perf_counter() - start)

    avg = _average_duration(durations)
    assert abs(avg - ankipan_db.FREQUENT_CONTEXTS_EXPECTED_AVERAGE_SECONDS) < TOLERANCE_SECONDS, (
        f"Average duration {avg:.2f}s for frequent contexts (lemma='{lemma}') exceeded tolerance "
        f"of ±{TOLERANCE_SECONDS}s around expected {ankipan_db.FREQUENT_CONTEXTS_EXPECTED_AVERAGE_SECONDS}s"
    )
