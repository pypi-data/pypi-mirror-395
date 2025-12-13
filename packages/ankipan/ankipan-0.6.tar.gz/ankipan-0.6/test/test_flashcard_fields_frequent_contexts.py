import pytest

from ankipan import HtmlWrappers, OngoingTask

field_name = 'frequent_contexts'

def test_flashcard_fields_example_sentences(generate_test_environment, request, data_dir, client_call_recorder):
    testenv = generate_test_environment(
        field_names=[field_name],
        extract_kwargs={"lemma_counts": {"応援": 1}},
    )
    with pytest.raises(RuntimeError):
        testenv.collection.collect_field_data(testenv.deck_name)

    testenv.collection.trigger_fields(testenv.deck_name)
    assert isinstance(testenv.get_flashcard_field(field_name), OngoingTask)

    testenv.reload()
    assert isinstance(testenv.get_flashcard_field(field_name), OngoingTask)

    testenv.collection.collect_field_data(testenv.deck_name,poll_interval=10 if request.config.getoption("--update") else 0)
    assert isinstance(testenv.get_flashcard_field(field_name), HtmlWrappers.CardSection)
    testenv.collection.save()

    with open(data_dir / '.field.html', 'w', encoding='utf-8') as f:
        f.write(testenv.first_card.backside)
