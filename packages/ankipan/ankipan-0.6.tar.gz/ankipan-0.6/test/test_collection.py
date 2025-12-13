import shutil

from ankipan import Collection

def test_add_deck(data_dir):
    shutil.rmtree(data_dir / 'testcollection')
    collection = Collection('testcollection', learning_lang='jp', native_lang='en', data_dir=data_dir )

    example_string = '世はまさに大海賊時代！'
    words = collection.extract_lemmas(string=example_string)
    words.set_new_words(['世'], known_words=['大', '時代'])
    collection.add_deck(words, 'testsource')

    assert collection.ignoring_words == ['海賊']
    assert collection.known_words == ['大', '時代']
    assert list(collection.cards.keys()) == ['世']
    assert collection.cards['世'].deck_example_sentences[0].text_segments[0] == example_string
    collection.save()

    collection = Collection('testcollection', data_dir=data_dir) # load from local storage
    assert collection.ignoring_words == ['海賊']
    assert collection.known_words == ['大', '時代']
    assert list(collection.cards.keys()) == ['世']
    assert collection.cards['世'].deck_example_sentences[0].text_segments[0] == example_string
