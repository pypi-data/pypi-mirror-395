import pytest

from ankipan import HtmlWrappers, OngoingTask

# TODO
@pytest.mark.xfail
def test_anki_functions(generate_test_environment, request, data_dir, client_call_recorder, mock_gpt_translations):
    exposed_field_names = ["example_sentences/ankipan_default/syosetu.com", "example_sentences/ankipan_default/youtube"]
    testenv = generate_test_environment(
        field_names=exposed_field_names,
        extract_kwargs={"lemma_counts": {"応援": 1}},
        example_sentence_sources=["ankipan_default/syosetu.com/【web版】最強の魔導士。ひざに矢をうけてしまったので田舎の衛兵になる.ja.txt"],
    )

    testenv.collection.trigger_fields(testenv.deck_name)
    testenv.collection.collect_field_data(testenv.deck_name,poll_interval=10 if request.config.getoption("--update") else 0)

    testenv.first_card._flashcard_fields["example_sentences/ankipan_default/syosetu.com"].content.content = \
        testenv.first_card._flashcard_fields["example_sentences/ankipan_default/syosetu.com"].content.content[0:3]
    print(testenv.first_card._flashcard_fields["example_sentences/ankipan_default/syosetu.com"])

    testenv.collection.sync_with_anki('testsource')
    with open(data_dir / '.field.html', 'w', encoding='utf-8') as f:
        f.write(testenv.first_card.backside)
