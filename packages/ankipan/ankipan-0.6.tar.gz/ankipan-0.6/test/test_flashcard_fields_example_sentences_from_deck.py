import pytest

from typing import List

from ankipan import HtmlWrappers, OngoingTask, TextSegment, GPTBase

field_name = "example_sentences_from_deck"

@pytest.mark.parametrize("learning_lang, lemma", [("jp", "応援"), ("de", "überraschen")])
def test_flashcard_fields_example_sentences_from_deck_no_deck_sentences(
        generate_test_environment,
        learning_lang,
        lemma):
    testenv = generate_test_environment(
        field_names=[field_name],
        learning_lang=learning_lang,
        extract_kwargs={"lemma_counts": {lemma: 1}},
    )
    testenv.collection.trigger_fields(testenv.deck_name)
    assert isinstance(
        testenv.get_flashcard_field(field_name),
        HtmlWrappers.CardSection
    )

@pytest.mark.parametrize('use_server_gpt',[True, False])
def test_flashcard_fields_example_sentences_from_deck(generate_test_environment, request, data_dir, use_server_gpt, client_call_recorder, mock_gpt_translations):
    testenv = generate_test_environment(
        field_names=[field_name],
        extract_kwargs={"string": 'オヤビン応援ダンス'},
        collection_kwargs = {'use_server_gpt': use_server_gpt}
    )
    if use_server_gpt:
        with pytest.raises(RuntimeError):
            testenv.collection.collect_field_data(testenv.deck_name)

    testenv.collection.trigger_fields(testenv.deck_name)
    if use_server_gpt:
        assert isinstance(testenv.get_flashcard_field(field_name), OngoingTask)
    else:
        assert testenv.get_flashcard_field(field_name) is None
    testenv.reload()
    if use_server_gpt:
        assert isinstance(testenv.get_flashcard_field(field_name), OngoingTask)
    else:
        assert testenv.get_flashcard_field(field_name) is None

    testenv.collection.collect_field_data(testenv.deck_name,poll_interval=10 if request.config.getoption("--update") else 0)
    assert isinstance(testenv.get_flashcard_field(field_name), HtmlWrappers.CardSection)
    testenv.collection.save()

    with open(data_dir / '.field.html', 'w', encoding='utf-8') as f:
        f.write(testenv.first_card.backside)