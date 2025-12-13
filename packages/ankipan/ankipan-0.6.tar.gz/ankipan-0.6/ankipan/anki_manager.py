import requests
import json
import logging

from typing import Iterable

logger = logging.getLogger(__name__)

class AnkiManager:
    def __init__(self, address='http://localhost:8765'):
        self.address = address

    def _invoke(self, action, **params):
        request_json = json.dumps({'action': action, 'params': params, 'version': 6})
        logger.info("AnkiConnect invoke action=%s keys=%s", action, list(params.keys()))
        response = requests.post(self.address, data=request_json)
        return response.json()

    def create_deck(self, deck_name):
        return self._invoke('createDeck', deck=deck_name)

    def delete_deck(self, deck_name):
        return self._invoke('deleteDeck', decks=[deck_name])

    def get_deck_names(self):
        return self._invoke('deckNames')['result']

    def add_note(self, anki_deck_name, front, back, model_name="Basic"):
        note = {
            "deckName": anki_deck_name,
            "modelName": model_name,
            "fields": {
                "Front": front,
                "Back": back
            },
            "options": {"allowDuplicate": False},
            "tags": []
        }
        return self._invoke('addNote', note=note)

    def add_notes(self, anki_deck_name, new_cards: Iterable['Card'], *, batch_size: int = 20):
        new_cards = list(new_cards)
        logger.info("add_notes deck=%s count=%d batch_size=%d", anki_deck_name, len(new_cards), batch_size)
        if not new_cards:
            return []

        added_ids: list[int | str] = []
        for i in range(0, len(new_cards), batch_size):
            batch = new_cards[i:i + batch_size]
            notes_to_add = [{
                "deckName": anki_deck_name,
                "modelName": "Basic",
                "fields": {
                    "Front": card.frontside,
                    "Back": card.backside
                },
                "options": {"allowDuplicate": False},
                "tags": [card.note_tag]
            } for card in batch]
            res = self._invoke('addNotes', notes=notes_to_add)
            # TODO: Warning: Notes already exist in other deck, not adding here.
            if res['error'] is not None:
                if 'cannot create note because it is a duplicate' in res['error']:
                    logger.error('Unable to sync with Ankiconnect because the anki collection that is currently open in the desktop app already contains the same cards from a different deck. Anki does not allow duplicate card frontsides, so users must use the same anki collection/profile for each ankipan collection.')
                raise RuntimeError(f"All anki add_notes errors: {res['error']}")
            batch_ids = res['result'] if isinstance(res['result'], list) else [res['result']]
            added_ids.extend(batch_ids)
            logger.info("add_notes batch %d-%d added=%d", i + 1, i + len(batch), len(batch_ids))
        return added_ids

    def find_notes(self, query):
        return self._invoke('findNotes', query=query)['result']

    def get_notes_info(self, note_ids):
        return self._invoke('notesInfo', notes=note_ids)['result']

    def update_note(self, note_id, card):
        logger.info("update_note id=%s word=%s", note_id, getattr(card, "word", "?"))
        note_info = self.get_notes_info([note_id])
        existing_tags = note_info[0].get("tags", []) if note_info else []
        note = {
            "id": note_id,
            "fields": {"Front": card.frontside, "Back": card.backside},
        }
        tags = existing_tags[:] if existing_tags else []
        if card.note_tag not in tags:
            tags.append(card.note_tag)
        if tags:
            note["tags"] = tags
        return self._invoke('updateNoteFields', note=note)

    def delete_notes(self, note_ids):
        return self._invoke('deleteNotes', notes=note_ids)

    def sync(self):
        return self._invoke('sync')

    def get_notes_for_anki_deck(self, anki_deck_name):
        note_ids = self.find_notes(f'"deck: {anki_deck_name}"')
        logger.info("notes_for_deck deck=%s note_ids=%d", anki_deck_name, len(note_ids))
        return self.get_notes_info(note_ids)

    def sync_deck(self, deck_name, cards, overwrite = False):
        existing_notes = self.get_notes_for_anki_deck(deck_name)
        if not existing_notes and deck_name not in self.get_deck_names():
            self.create_deck(deck_name)
        existing_anki_ids = {note['noteId'] for note in existing_notes}
        logger.info(
            "sync_deck deck=%s total_cards=%d existing_notes=%d overwrite=%s",
            deck_name, len(cards), len(existing_notes), overwrite,
        )
        if overwrite:
            deleted_notes = self.delete_notes(list(existing_anki_ids))
        cards_to_update = [card for card in cards if card.anki_id and card.anki_id in existing_anki_ids]
        new_cards = [card for card in cards if not card.anki_id or card.anki_id not in existing_anki_ids]
        logger.info(
            "sync_deck deck=%s to_update=%d to_add=%d",
            deck_name, len(cards_to_update), len(new_cards),
        )
        if cards_to_update:
            for card in cards_to_update:
                self.update_note(card.anki_id, card)
        if new_cards:
            anki_ids = self.add_notes(deck_name, new_cards, batch_size=50)
            for card, anki_id in zip(new_cards, anki_ids):
                if anki_id and anki_id != 'error':
                    card.set_anki_id(anki_id)

    # TODO
    # def sync_images(self, images_path: Path):
    #     def send_request(action, **params):
    #         response = requests.post('http://localhost:8765', json={"action": action, "version": 6, "params": params})
    #         response.raise_for_status()  # This will raise an HTTPError if the HTTP request returned an unsuccessful status code.
    #         return response.json()
    #     anki_media_root = send_request('getMediaDirPath')['result']
    #     anki_media_files = set(os.listdir(anki_media_root))
    #     deck_images = set(os.listdir(images_path))
    #     for img in anki_media_files-deck_images:
    #         os.remove(Path(anki_media_root, img))
    #     for img in deck_images-anki_media_files:
    #         shutil.copy(Path(images_path, img), anki_media_root)
