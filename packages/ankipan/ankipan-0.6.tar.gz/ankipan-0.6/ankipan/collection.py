from pathlib import Path
import logging
import shutil
from collections.abc import Iterable
import signal
import time
from concurrent.futures import ThreadPoolExecutor, as_completed, Future
import threading
import inspect
import signal
import threading

from typing import Union, Dict, Iterable, List, Set

from ankipan import TextSegment, SourcePath, Client, \
                    Deck, Card, Reader, AnkiManager, PersistentStorage, \
                    COLLECTIONS_DIR, OngoingTask, GPTQueue, HtmlWrappers
from ankipan.flashcard_fields import get_flashcard_field_registry
from ankipan.util import *


logger = logging.getLogger(__name__)

class Collection(PersistentStorage):
    def __init__(self,
                 name: str,
                 learning_lang: str = None,
                 native_lang: str = None,
                 *,
                 use_server_gpt: bool = True,
                 force_overwrite = False,
                 data_dir = COLLECTIONS_DIR):
        """
        Load new or existing collection.
        A collection can hold 0 to n decks.
        A deck can hold 1 to n flashcards.
        Flashcards have 1 to n fields, which refers to information on the backside (dictionary definitions, example sentences etc.)

        Parameters
        ----------
        name : Name of collection.
            Creates new collection for new names, loads existing collection for existing names.
        learning_lang : Name of language the user wants to learn.
        native_lang : Native language of the user for translations and explanations.

        """
        self.name = name
        self.data_dir = data_dir
        self.collection_dir = data_dir / name
        self.collection_dir.mkdir(parents=True, exist_ok=True)

        super().__init__(self.collection_dir / "metadata.json")

        self._learning_lang = None
        self._native_lang = None
        self._flashcard_fields = []
        self._example_sentence_sources = []
        self._known_words = []
        self._ignoring_words = []
        self._use_server_gpt = use_server_gpt

        self._register_persistent_attribute("_learning_lang")
        self._register_persistent_attribute("_native_lang")
        self._register_persistent_attribute("_flashcard_fields")
        self._register_persistent_attribute(
            "_example_sentence_sources",
            serialize=lambda xs: [str(x) for x in xs],
            deserialize=lambda xs: [SourcePath(x) for x in (xs or [])],
        )
        self._register_persistent_attribute("_known_words")
        self._register_persistent_attribute("_ignoring_words")

        self._register_persistent_attribute("_use_server_gpt")
        if self.collection_dir.exists() and force_overwrite:
            shutil.rmtree(self.collection_dir)
        if not self.json_path.exists():
            if not (learning_lang and native_lang):
                raise RuntimeError("learning_lang and native_lang kwargs required when initializing new collection")
            self._learning_lang = learning_lang
            self._native_lang = native_lang
        else:
            if learning_lang or native_lang:
                raise RuntimeError(f'Initializing existing database "{name}", specified kwargs would be ignored')
            self._load_from_storage()

        self.decks: Dict[str, List[Card]] = {}
        decks_dir = self.collection_dir / "decks"
        if decks_dir.exists():
            for deck_path in decks_dir.iterdir():
                if not deck_path.is_dir():
                    continue
                deck_name = deck_path.stem
                for card_path in deck_path.iterdir():
                    if not card_path.is_file():
                        continue
                    self.decks.setdefault(deck_name, []).append(
                        Card(card_path.stem, json_path=card_path)
                    )
        else:
            decks_dir.mkdir(parents=True, exist_ok=True)

        self.reader = Reader(self.learning_lang)
        self.anki_manager = AnkiManager()
        # pass permanent variables as reference so fields can work with them
        self.gpt_queue = GPTQueue()
        self.flashcard_field_registry = get_flashcard_field_registry(self, gpt_queue=self.gpt_queue)

    @property
    def cards(self):
        return {card.word: card for cards in self.decks.values() for card in cards}

    def print_available_flashcard_fields(self):
        for field_name, field_collector in self.flashcard_field_registry.items():
            if len(field_collector.exposed_fields) == 1:
                print(f"'{field_collector.exposed_fields[0]}',")
            else:
                if len(field_collector.exposed_fields) > 0:
                    print(f"\n{field_name}:")
                    for sub_field in field_collector.exposed_fields:
                        print(f"    '{sub_field}',")

    def print_available_example_sentence_sources(self, source_path = None) -> Dict[str, Callable[..., Any]]:
        print(self.flashcard_field_registry['example_sentences'].available_sources(source_path))

    def set_use_server_gpt(self, value: bool):
        assert isinstance(value, bool)
        self._use_server_gpt = value

    def _modify_list(self, target_list, items: List[Any], warning_msg: str = None, add = False, deduplicate = True):
        if add:
            for item in items:
                if (not deduplicate) or (item not in target_list):
                    target_list.append(item)
                else:
                    if warning_msg:
                        logger.warning(warning_msg.format(item))
        else:
            target_list.clear()
            if deduplicate:
                seen = set()
                for item in items:
                    if item not in seen:
                        target_list.append(item)
                        seen.add(item)
            else:
                target_list.extend(items)

    def set_flashcard_fields(self,
                             field_names: List[str],
                             add = False):
        invalid_entries = [
            field_name for field_name in field_names
            if field_name not in self.flashcard_field_registry.valid_field_names
        ]
        if invalid_entries:
            raise RuntimeError(f'Invalid flashcard fields specified: {invalid_entries}\nPlease check available fields with `Collection.print_available_flashcard_fields`')
        self._modify_list(
            self._flashcard_fields,
            field_names,
            warning_msg = 'Flashcard Field "{}" already in Collection.flashcard_fields, skipping...',
            add = add
        )
        self.save()

    def set_example_sentence_sources(self, example_sentence_sources: List[str], add = False):
        """
        Path starts with the server name, then specifies path to the target source.
        Tracks example sentence sources that the user would like to favor when studying (e.g. particular youtubers, movies etc.)

        Parameters
        ----------
        example_sentence_sources : list of strings
            List of sources to collect example sentences from.
            When flashcards are generated, example sentences for all root categories from all paths will be considered, where specified sources will be prioritized and highlighted.

        Example
        -------
            If we are interested in the two youtubers "ankipan_default/youtube/sushiramen" and "ankipan_default/youtube/hajimesyacho", then flashcards will contain a "youtube" example sentence section,
            where the specified youtubers are included alongside other sources from youtube (~evenly split among specified youtubers, ~50%-50% split between specified and other youtubers).
            Not specifying any preference will cause the youtube example sentence section to only contain random youtubers with suitable sentences (for more details see `get_segments_for_lemma` in ankipan_db).
        """
        invalid_source_paths = Client.get_invalid_source_paths(self.learning_lang, [SourcePath(source_path) for source_path in example_sentence_sources])
        unspecified_fields = []
        specified_example_sentence_fields = {'/'.join(field.split('/')[1:]) for field in self.flashcard_fields if field.startswith('example_sentences/')}
        for source_path in example_sentence_sources:
            if not any([source_path.startswith(field) for field in specified_example_sentence_fields]):
                unspecified_fields.append(source_path)
        if invalid_source_paths or unspecified_fields:
            raise RuntimeError(
                f"Some of the specified example sentence source paths are invalid: {invalid_source_paths}\n" if invalid_source_paths else ""
                f"Some of the fields of the specified example sentence source paths are not yet specified as flashcard fields (call Collection.set_flashcard_fields with the missing fields first): {unspecified_fields}\n" if unspecified_fields else ""
                f"Find valid paths with (collection.print_available_example_sentence_sources(<optional_path>))"
            )
        self._modify_list(
            self._example_sentence_sources,
            [SourcePath(source_path) for source_path in example_sentence_sources],
            warning_msg='Source Path "{}" already in Collection.example_sentence_sources, skipping...',
            add=add,
        )
        self.save()

    def set_known_words(self, words: Iterable[str], add=False):
        self._modify_list(
            self._known_words,
            words,
            warning_msg='Known word "{}" already in Collection.known_words, skipping...',
            add=add,
        )

    def set_ignoring_words(self, words: Iterable[str], add=False):
        self._modify_list(
            self._ignoring_words,
            words,
            warning_msg='Ignoring word "{}" already in Collection.ignoring_words, skipping...',
            add=add,
        )

    def extract_lemmas(self,
                        paths: Union[Union[str, Path], Iterable[Union[str, Path]]] = None,
                        *,
                        source_path: str = None,
                        string: str = None,
                        lemma_counts: Dict[str, int] = None) -> Deck:
        """
        Collect words from specified source.

        Parameters
        ----------
        path: Path to a file or directory with textfiles to be added to the collection
            Uses stanza lemma parsing from reader.py to parse source files into wordcount dictionary

        kwargs (only consiered if path is not provided):
            source_path: Path of source in db to fetch lemmas from (see Collection.print_available_example_sentence_sources(<optional_path>), does not require stanza)
            string: String to be parsed directly without reading a file
            lemma_counts: Dict of words and lemma_counts, directly adopted as Deck object

        """
        if not (isinstance(paths, list) or isinstance(paths, set)):
            if isinstance(paths, str) or isinstance(paths, Path):
                paths = [paths]
            elif not paths == None:
                raise RuntimeError(f'Unknown type passed as path: {paths}')
        deck = Deck(self.learning_lang, self.native_lang,
                    learning_collection_words = set(self.cards.keys()),
                    known_collection_words = self.known_words,
                    ignoring_collection_words = self.ignoring_words,
                    example_sentence_fields = [SourcePath(field_name) for field_name in self.flashcard_fields if field_name.startswith('example_sentences/')])
        if paths:
            for path in paths:
                deck.add(path=path)
        elif string:
            deck.add(string=string)
        elif lemma_counts:
            deck.add(lemma_counts=lemma_counts)
        elif source_path:
            source = self.flashcard_field_registry['example_sentences'].available_sources(source_path)
            lemma_counts = source.lemma_counts
            if not lemma_counts:
                raise RuntimeError(f'No lemma counts received for "{source_path}", please check server.')
            deck.source_words.update(lemma_counts)
        return deck

    def add_deck(self,
            deck: Deck,
            deck_name: str):
        """
        Add new deck from new words in Deck to current collection.
        Changes made to the new words and known words in the Deck object are adopted into the collection.

        Parameters
        ----------
        words: Words from Deck
        deck_name: Name of source you are adding, e.g. movie or series title

        """

        if not deck_name:
            raise RuntimeError('deck_name is a mandatory field')
        if deck_name in self.decks:
            raise RuntimeError('source with same name already in collection')

        self.set_known_words(set(deck.known_words) - set(self.known_words), add=True)
        self.set_ignoring_words(set(deck.ignoring_words) - set(self.ignoring_words), add=True)
        self.decks[deck_name] = []
        for lemma in deck.new_words:
            deck_example_sentences = []
            for file in deck.added_files:
                example_sentences = [
                    TextSegment(
                        main_index = index - max(0, index-1),
                        text_segments = [seg.text for seg in file.stanza_segments[max(0, index-1): index+2]],
                        word = word,
                        source_name = file.path.stem if file.path else f'{deck_name} {index+1}/{len(file.stanza_segments)}'
                    ) for word, indices in file.lemma_word_index_mapping.get(lemma, {}).items() for index in indices
                ]
                deck_example_sentences.extend(example_sentences)
            self.decks[deck_name].append(Card(lemma,
                                              deck_example_sentences = deck_example_sentences,
                                              json_path = self.data_dir / self.name / 'decks' / deck_name / f'{lemma}.json'))
        self.save()

    def remove_deck(self, deck_name: str):
        # TODO: consider caching mechanism so downloaded info isn't destroyed
        if deck_name not in self.decks: raise RuntimeError(f'Deck "{deck_name}" not present in collection')
        for card in self.decks.pop(deck_name):
            shutil.remove(card.json_path)

    def estimate_known_words(self):
        estimate_known_words(self.flashcard_field_registry['example_sentences'].available_sources, self.known_words)
        self.save()

    def get_cards_with_missing_data(self, cards, field_name, force_update = False) -> List[Card]:
        return cards if force_update else [card for card in cards if field_name not in card.flashcard_fields]

    # TODO: ignores existing sources and overwrites everything for some reason
    def trigger_fields(self,
                       deck_name: str,
                       force_update: bool = False):
        for exposed_field_name in self.flashcard_fields:
            kwargs = {"force_update": force_update}
            field_name = SourcePath(exposed_field_name)[0]
            field_cls = self.flashcard_field_registry[field_name]
            if not field_cls.implements_trigger:
                continue
            if '/' in exposed_field_name:
                kwargs["field_path"] = SourcePath(exposed_field_name)
            cards_to_trigger = self.get_cards_with_missing_data(
                self.decks[deck_name],
                str(kwargs.get("field_path", exposed_field_name)),
                force_update=force_update
            )
            if not cards_to_trigger:
                logger.info(f'No cards need a trigger for {kwargs.get("field_path", exposed_field_name)}')
                continue
            field_cls.trigger_fields(cards_to_trigger, **kwargs)
            logger.info(f'Triggered computation of field "{kwargs.get("field_path", exposed_field_name)}" for {len(cards_to_trigger)} card(s).')
        self.save()

    def collect_field_data(self,
                           deck_name: str,
                           force_update: bool = False,
                           poll_interval: float = 60.0):
        if not self.use_server_gpt:
            self.gpt_queue.start_thread()
        stop_event = threading.Event()
        interrupted = False
        previous_sigint_handler = signal.getsignal(signal.SIGINT)

        def _handle_sigint(signum, frame):
            print("[collect_field_data] Interrupting...")
            stop_event.set()
            import _thread
            _thread.interrupt_main()

        signal.signal(signal.SIGINT, _handle_sigint)

        def _collect_non_trigger(cards, exposed_field_name):
            field_cls = self.flashcard_field_registry[SourcePath(exposed_field_name)[0]]
            collect_kwargs = {"force_update": force_update}
            if "stop_event" in inspect.signature(field_cls.collect_data).parameters:
                collect_kwargs["stop_event"] = stop_event
            field_cls.collect_data(cards, exposed_field_name, **collect_kwargs)

        try:
            trigger_jobs = []
            trigger_progress = {}
            non_trigger_jobs = []
            # Partition work by trigger requirement
            for exposed_field_name in self.flashcard_fields:
                field_cls = self.flashcard_field_registry[SourcePath(exposed_field_name)[0]]
                cards = list(self.decks[deck_name])
                if field_cls.implements_trigger:
                    missing_trigger = []
                    pending_cards = []
                    for card in cards:
                        val = card.flashcard_fields.get(exposed_field_name)
                        if isinstance(val, (OngoingTask, HtmlWrappers.CardSection)):
                            pending_cards.append(card)
                        else:
                            missing_trigger.append(card.word)
                    if missing_trigger:
                        raise RuntimeError(
                            f'Field "{exposed_field_name}" has cards with missing triggered fields, '
                            f"run collection.trigger_fields first: {missing_trigger}"
                        )
                    if pending_cards:
                        trigger_jobs.append((exposed_field_name, pending_cards))
                        trigger_progress[exposed_field_name] = {
                            "initial": len(pending_cards),
                            "last_remaining": len(pending_cards),
                        }
                else:
                    cards_to_collect = self.get_cards_with_missing_data(cards, exposed_field_name, force_update=force_update)
                    if cards_to_collect:
                        non_trigger_jobs.append((exposed_field_name, cards_to_collect))
            if not trigger_jobs and not non_trigger_jobs:
                return
            executor = None
            futures = []
            try:
                if non_trigger_jobs:
                    max_workers = max(1, min(len(non_trigger_jobs), 5))
                    executor = ThreadPoolExecutor(max_workers=max_workers)
                    for exposed_field_name, cards in non_trigger_jobs:
                        future = executor.submit(_collect_non_trigger, cards, exposed_field_name)
                        futures.append(future)
                    for future in as_completed(futures):
                        future.result()
            finally:
                if executor:
                    executor.shutdown(wait=True, cancel_futures=False)
            while trigger_jobs and not stop_event.is_set():
                completed = []
                for exposed_field_name, cards in trigger_jobs:
                    field_cls = self.flashcard_field_registry[SourcePath(exposed_field_name)[0]]
                    collect_kwargs = {"force_update": force_update}
                    if "stop_event" in inspect.signature(field_cls.collect_data).parameters:
                        collect_kwargs["stop_event"] = stop_event
                    remaining_before = len(field_cls.get_cards_with_ongoing_task(cards, exposed_field_name))
                    try:
                        changed = field_cls.collect_data(cards, exposed_field_name, **collect_kwargs)
                    except Exception as exc:
                        initial = trigger_progress.get(exposed_field_name, {}).get("initial", len(cards))
                        raise RuntimeError(
                            f'[collect_field_data] Field "{exposed_field_name}" failed. '
                            f"initial={initial}, remaining_before={remaining_before}, changed_this_iter={changed if 'changed' in locals() else 'n/a'}"
                        ) from exc
                    remaining = len(field_cls.get_cards_with_ongoing_task(cards, exposed_field_name))
                    initial = trigger_progress[exposed_field_name]["initial"]
                    collected_total = initial - remaining
                    collected_iter = max(0, remaining_before - remaining)
                    trigger_progress[exposed_field_name]["last_remaining"] = remaining
                    logger.info(
                        "[collect_field_data] %s: collected_iter=%d collected_total=%d remaining=%d initial=%d",
                        exposed_field_name,
                        collected_iter,
                        collected_total,
                        remaining,
                        initial,
                    )
                    if remaining == 0:
                        completed.append((exposed_field_name, cards))
                        logger.info(f'[collect_field_data] Finished collecting "{exposed_field_name}"')
                for job in completed:
                    trigger_jobs.remove(job)
                if trigger_jobs and not stop_event.is_set():
                    stop_event.wait(poll_interval)

        except KeyboardInterrupt:
            stop_event.set()
            interrupted = True
            raise
        finally:
            if not interrupted:
                self.save()
            signal.signal(signal.SIGINT, previous_sigint_handler)
            if self.use_server_gpt:
                self.gpt_queue.stop_thread()


    # TODO: add "full_overwrite" kwarg, which bulk-removes and readds card instead of updating one by one (faster)
    def sync_with_anki(self, deck_name: str, overwrite: bool = False):
        """
        Sync collection data with Anki via AnkiConnect.
        Requires Anki (and AnkiConnect) running and logged in.
        https://apps.ankiweb.net/
        https://ankiweb.net/shared/info/2055492159/
        """
        deck = self.decks.get(deck_name, [])

        required = set(self.flashcard_fields)
        cards_with_missing_sections: dict[str, list[str]] = {}
        for card in deck:
            have = set(field_name for field_name, field in getattr(card, "flashcard_fields", {}).items() if not isinstance(field, OngoingTask))
            for field in (required - have):
                cards_with_missing_sections.setdefault(field, []).append(card.word)

        if cards_with_missing_sections:
            lines = []
            for field, words in sorted(cards_with_missing_sections.items()):
                lines.append(f"- {field}: {len(words)} missing → [{', '.join(words)}]")
            raise RuntimeError(
                "Some cards are missing data for fields defined in Collection.flashcard_fields; "
                "run Collection.trigger_fields(<deck_name>) and Collection.collect_fields(<deck_name>) first.\n" + "\n".join(lines)
            )

        if deck:
            logger.info("Syncing Anki for deck=%s cards=%d", deck_name, len(deck))
            print("Syncing Anki for words:", [c.word for c in deck])
            self.anki_manager.sync_deck(deck_name, deck, overwrite=overwrite)
            self.anki_manager.sync()

    def save(self):
        """
        Write all collection data to `self.data_dir`.

        """
        logger.info(f'Saving collection data to {self.collection_dir.absolute()}')
        self._save_storage()
        for card in self.cards.values():
            card.save()

    # TODO: Implement safety mechanism to not accidentally lose massive amounts of data
    # TODO: Implement function to recreate database based on current anki database state in case of loss
    def delete_collection(self, name):
        """
        Delete collection from database
        Currently ignores whether collection is present in database or not

        """
        if input('Are you sure? type "yes"') == 'yes':
            shutil.rmtree(self.data_dir / name)

    def __str__(self):
        deck_overview = f'Decks ({len(self.decks)}):\n'
        for deck_name, cards in self.decks.items():
            deck_overview += f'  {deck_name}: {len(cards)} cards\n'
        return super().__str__() + '\n' + deck_overview
