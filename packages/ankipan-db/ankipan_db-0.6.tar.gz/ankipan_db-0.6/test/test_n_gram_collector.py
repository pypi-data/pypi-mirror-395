import ankipan_db
from ankipan import Translator, TextSegment


def test_get_n_grams(monkeypatch):
    lang = 'jp'
    db = ankipan_db.DBManager(lang)
    conn = db.get_safe_conn()

    lemma = '境'

    segments = ankipan_db.NGramCollector.get_text_segments_for_lemma(
        conn, lemma=lemma,
        # limit=100
    )
    wordforms = ankipan_db.NGramCollector.get_wordforms_for_lemma(
        conn, lemma=lemma
    )
    res = ankipan_db.NGramCollector.most_common_contexts_from_segments(
        segments,
        wordforms,
        enforce_word_boundaries = lang not in ['jp'])

    for i in res:
        print(i)
