import pytest

from ankipan import Reader

@pytest.mark.parametrize(
    "lang,input_text,expected",
    [
        ('de', 'Woher genau\\h', 'Woher genau'),
        ('de', 'Woher\ngenau\n\n', 'Woher\ngenau\n\n'),
        ('de', 'Heute Abend gehen wir, weil es "Alles kann passieren"- Donnerstag ist.', 'Heute Abend gehen wir, weil es "Alles kann passieren"- Donnerstag ist.'),
        ('de', '''Spielen wir Halo, gucken wir Battlestar,
schmeißen wir ein paar Mentos in Diätcola?''', '''Spielen wir Halo, gucken wir Battlestar,
schmeißen wir ein paar Mentos in Diätcola?'''),
    ]
)
def test_clean_string(lang, input_text, expected):
    r = Reader(lang)
    res = r.clean_string(input_text, r.sub_filter_expressions)
    assert res == expected

@pytest.mark.parametrize(
    "lang,input_text,expected",
    [
        ('de', '''Heute Abend gehen wir, weil es
"Alles kann passieren"- Donnerstag ist.''',
'''Heute Abend gehen wir, weil es "Alles kann passieren"- Donnerstag ist.''')]
)
def test_parse_sub(lang, input_text, expected):
    r = Reader(lang)
    assert r.parse_subs(f'1\n00:01:10,960 --> 00:01:12,299\n{input_text}')[0] == expected
