import pytest

from ankipan import HtmlWrappers, OngoingTask

@pytest.mark.parametrize('use_server_gpt',[True, False])
def test_flashcard_fields_example_sentences(generate_test_environment, request, data_dir, use_server_gpt, client_call_recorder, mock_gpt_translations):
    exposed_field_names = ["example_sentences/ankipan_default/youtube",
                           "example_sentences/ankipan_default/syosetu.com"]
    testenv = generate_test_environment(
        field_names=exposed_field_names,
        example_sentence_sources=["ankipan_default/youtube/hajimesyacho"],
        extract_kwargs={"lemma_counts": {"応援": 1}},
        collection_kwargs = {'use_server_gpt': use_server_gpt}
    )

    if use_server_gpt:
        with pytest.raises(RuntimeError):
            testenv.collection.collect_field_data(testenv.deck_name)

    testenv.collection.trigger_fields(testenv.deck_name)
    for exposed_field_name in exposed_field_names:
        assert isinstance(testenv.get_flashcard_field(exposed_field_name), OngoingTask)

    testenv.reload()
    for exposed_field_name in exposed_field_names:
        assert isinstance(testenv.get_flashcard_field(exposed_field_name), OngoingTask)

    testenv.collection.collect_field_data(testenv.deck_name,poll_interval=10 if request.config.getoption("--update") else 0)
    for exposed_field_name in exposed_field_names:
        assert isinstance(testenv.get_flashcard_field(exposed_field_name), HtmlWrappers.CardSection)
    testenv.collection.save()

    with open(data_dir / '.field.html', 'w', encoding='utf-8') as f:
        f.write(testenv.first_card.backside)
