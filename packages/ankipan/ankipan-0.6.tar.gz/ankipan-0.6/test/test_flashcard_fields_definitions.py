import pytest

from ankipan import HtmlWrappers, Collection, get_flashcard_field_registry

# (learning_lang, native_lang, probe_word)
LANG_CASES = [
    ("jp", "de", "応援"),
    ("de", "en", "können"),
]


lang_word_field = []
for learning_lang, native_lang, probe_word in LANG_CASES:
    reg = get_flashcard_field_registry(Collection("test", learning_lang, native_lang))
    for field_name in (name for name in reg.keys() if name.startswith("definitions_")):
        lang_word_field.append((learning_lang, native_lang, probe_word, field_name))

@pytest.mark.parametrize("learning_lang,native_lang,probe_word,field_name", lang_word_field)
def test_definition_field(generate_test_environment, request, data_dir, learning_lang, native_lang, probe_word, field_name):
    if not field_name:
        pytest.skip(f"No definition fields for {learning_lang}/{native_lang}")

    testenv = generate_test_environment(
        learning_lang=learning_lang,
        native_lang=native_lang,
        extract_kwargs={"lemma_counts": {probe_word: 1}},
    )
    field_cls = get_flashcard_field_registry(testenv.collection)[field_name]
    testenv.collection.set_flashcard_fields(field_cls.exposed_fields)

    testenv.collection.collect_field_data(
        testenv.deck_name,
        poll_interval=10 if request.config.getoption("--update") else 0,
    )

    for exposed_field_name in field_cls.exposed_fields:
        assert isinstance(testenv.get_flashcard_field(exposed_field_name), HtmlWrappers.CardSection)
    testenv.reload()
    for exposed_field_name in field_cls.exposed_fields:
        assert isinstance(testenv.get_flashcard_field(exposed_field_name), HtmlWrappers.CardSection)

    with open(data_dir / f".field.{learning_lang}.{field_name}.html", "w", encoding="utf-8") as f:
        f.write(testenv.first_card.backside)
