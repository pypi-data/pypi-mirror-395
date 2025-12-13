import ankipan_db
from ankipan import GPTBase, TextSegment

def test_get_lemma_percentiles():
    learning_lang = 'de'
    db = ankipan_db.DBManager(learning_lang)
    source_path = 'youtube'
    lemmas = ['sein', 'Test']
    res = db.get_lemma_percentiles(source_path, lemmas)
    print("res",res)

def mock_translate_text_segments(self, native_lang, learning_lang, example_sentences):
    """mock method to avoid gemini api calls"""
    for example_sentence in example_sentences:
        example_sentence.translation = f'Mock translation of "{example_sentence.main_segment}" from {learning_lang} to {native_lang}'

def test_get_cached_translation(monkeypatch):
    monkeypatch.setattr(
        GPTBase,
        "translate_text_segments",
        mock_translate_text_segments,
        raising=True,
    )

    ankipan_db.db_config['database'] = 'ankipan_test_db'
    native_lang = 'de'
    learning_lang = 'en'
    word = 'like'

    db = ankipan_db.DBManager(learning_lang)
    conn = db.get_safe_conn()
    with conn.cursor() as cur:
        cur.execute("delete from translations")
    conn.commit()

    gpt_base = GPTBase()
    segments_by_lemma_before_translation = db.get_segments_for_lemmas(
            ['source_root_1/entry_1_1', 'source_root_1/entry_1_3'],
            [word],
            'source_category_1',
            native_lang,
            ideal_sentences_length = 10,
            n_sentences=5,
        )
    print("segments_by_lemma_before_translation",segments_by_lemma_before_translation)
    example_sentences = [TextSegment(**sentence) for filename, sentences in segments_by_lemma_before_translation[word]['entries_from_known_sources']['source_root_1'].items()
                         for sentence in sentences]
    n_entries_filled = db.get_translations_from_cache(example_sentences, native_lang)
    assert n_entries_filled == 0

    gpt_base.translate_text_segments(
        native_lang, learning_lang,
        example_sentences
    )
    print("translations example_sentences",example_sentences)

    db.cache_translations(example_sentences, native_lang)
    with conn.cursor() as cur:
        cur.execute("select * from translations")
        print("translation", [a for a in cur.fetchall()])

    segments_by_lemma_after_translation = db.get_segments_for_lemmas(
            ['source_root_1/entry_1_1', 'source_root_1/entry_1_3'],
            [word],
            'source_category_1',
            native_lang,
            ideal_sentences_length = 10,
            n_sentences=5
        )

    print("segments_by_lemma_after_translation",segments_by_lemma_after_translation)

    # assert that we are now prioritizing sentences with existing translations instead of choosing at random again
    assert set(segments_by_lemma_before_translation[word]['entries_from_known_sources']['source_root_1'].keys()) == \
           set(segments_by_lemma_after_translation[word]['entries_from_known_sources']['source_root_1'].keys())
    assert set(segments_by_lemma_before_translation[word]['entries_from_unknown_sources']['source_root_1'].keys()) == \
           set(segments_by_lemma_after_translation[word]['entries_from_unknown_sources']['source_root_1'].keys())

    # see if we can get newly translated sentences from cache
    example_sentences = [TextSegment(**sentence) for filename, sentences in segments_by_lemma_before_translation[word]['entries_from_known_sources']['source_root_1'].items() for sentence in sentences]
    n_entries_filled = db.get_translations_from_cache(example_sentences, native_lang)
    assert n_entries_filled == 4 # example sentences contains 4 elements, of which 4 have an empty "translation" field

def test_get_cached_translation_prod():
    ankipan_db.db_config['database'] = 'ankipan_db'

    native_lang = 'en'
    learning_lang = 'jp'
    words = [
            '何','俺','言う','一',
            # '御前', '大', '返る', '王', '決める', '海賊', '勝手', '仲間', '次回', '後悔', '剣', '狩り', '豪'
            ]

    ideal_sentence_length = 20
    db = ankipan_db.DBManager(learning_lang, ideal_sentence_length=ideal_sentence_length)

    source_names = [
                'SUSHIRAMEN-Riku',
                'hajimesyacho'
                ]
    import time
    start = time.time()
    segments_by_lemma = db.get_segments_for_lemmas(
            source_names,
            words,
            'youtube',
            native_lang,
            ideal_sentences_length = 10,
            n_sentences=4,
            sigma=2,
            translation_weight = 1,
        )
    print("a", time.time() - start)
    return
    print("segments_by_lemma",segments_by_lemma)
    for lemma, segments in segments_by_lemma.items():
        print("segments['entries_from_known_sources']", lemma, segments['entries_from_known_sources'])
        assert all([source_name in segments['entries_from_known_sources'] for source_name in source_names])
        for type, sources in segments.items():
            for source, info in sources.items():
                for source_name, source_items in info.items():
                    for source_item in source_items:
                        assert abs(ideal_sentence_length - len(source_item['text_segments'][source_item['main_index']])) < 5
                        print("Sentence Length:", len(source_item['text_segments'][source_item['main_index']]), source_item['text_segments'][source_item['main_index']])
