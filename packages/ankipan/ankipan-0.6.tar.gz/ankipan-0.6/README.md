# Ankipan

Ankipan is a project to democratize language learning in a decentralized way.

It allows you to choose which domains you want to be more fluent in, and creates a custom learning curriculum that aims to get you to your goal as effectively and efficiently as possible.
First, specify what kind of fields you would like on your flashcard: What definitions from open online dictionaries do you prefer? What kind of example sentences would you like to have on your flashcards to use a reference? (e.g. youtube subtitles, wikipedia, open news corpora etc.)
Then, you can parse any text you are interested in from a wide variety of formats. (text, subtitle, pdf, html, or a source from an ankipan database)
Ankipan generates a frequency-sorted list of root words, and provides you with tools to choose which words you would like to learn and generates the corresponding Anki flashcards for you.
Inside of Anki, you can color-tag the example sentences that are the most useful for you, and the flashcard will remember them and expand those sentence fields for you the next time you review the card.
Example sentences contain gpt-generated translations and explanations, which you can currently either generate with with the `ankipan_default` db server that I am privately hosting, or by utilizing your own google gemini API key or local ollama installation if there are currently too many GPT requests (see `ankipan/gpt_base.py`).

<p align="center">
  <img src="/docs/anki_screenshot_1.png" width="45%"/>
  <img src="/docs/anki_screenshot_2.png" width="45%"/>
</p>

New fields can easily be added in a modular way by creating a new file in the `ankipan/flashcard_fields` directory.
Ankipan can connect to any number of servers containing a pre-parsed db of different text sources, e.g. to collect example sentences or utilize GPT resources for translations/explanations and other fields. (`ankipan.Config.add_server(name, url)`, for hosting a server see https://gitlab.com/ankipan/ankipan_db)

## Getting started

### 1. Prerequisites

- Download and install anki from https://apps.ankiweb.net/
- Create an account on their website
- Install the ankiconnect plugin (In anki, open Tools -> Add Ons -> Get Add-Ons -> paste code 2055492159, see https://ankiweb.net/shared/info/2055492159)
- Open the app and login, keep anki open when syncing databases

### 2. Installation

- Using pip:

```bash
pip install ankipan
```

- From source:

```bash
git clone git@gitlab.com:ankipan/ankipan.git
cd ankipan
pip install .
```

### 3. (Optional) Install lemmatizers to parse your own texts

- Download pytorch from https://pytorch.org/get-started/locally/ (for stanza lemma parsing)
- install dependencies:

```bash
pip install stanza HanTa
```

## Usage

See notebooks in `/examples`

## Notes

- Current lemmatization is done via the `stanza` library in the reader.py module. While this works mostly fine, the library still just uses a statistical model to estimate the likely word roots (lemmas) of the different pieces of sentences. It sometimes makes mistakes, which requires the users to manually filter them in the `select_new_words` overview, or suspend the card later on in anki.
