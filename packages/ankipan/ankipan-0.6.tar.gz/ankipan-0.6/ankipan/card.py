import functools
from jinja2 import Environment, FileSystemLoader, select_autoescape, Template
import logging
from typing import Dict, List, Iterable, Any, Optional, Callable, Union
from html import escape
from dataclasses import asdict
from pathlib import Path
import time
import uuid

from ankipan import HTML_TEMPLATE_DIR, HtmlWrappers, TextSegment, OngoingTask, PersistentStorage

logger = logging.getLogger(__name__)

class Card(PersistentStorage):
    """
    Flashcard object.
    Values are lazy-loaded from json to prevent a collection with many cards from cluttering memory.

    Parameters
    ----------
    word: Word of the flashcard
    json_path: path to local json path with all fields (saves compute for many cards)
    anki_id: optional, filled when card is synced with anki
    deck_example_sentences: optional, filled if the corresponding deck was created from raw text.
    """

    def __init__(
        self,
        word: str,
        json_path: Union[str, Path],
        deck_example_sentences: Optional[List[TextSegment]] = None):
        self.word = word

        super().__init__(json_path)

        self._anki_id = None
        self._deck_example_sentences = deck_example_sentences or []
        self._flashcard_fields = {}
        self._note_tag = None

        self._register_persistent_attribute("_anki_id")
        self._register_persistent_attribute(
            "_deck_example_sentences",
            serialize=lambda lst: [asdict(x) for x in lst],
            deserialize=lambda data: [TextSegment(**x) for x in (data or [])],
        )
        def deserialize_flashcard_fields(data: Dict[str, Any]) -> Dict[str, Union[HtmlWrappers.CardSection, OngoingTask]]:
            if not data:
                return {}
            result = {}
            for field_name, payload in data.items():
                result[field_name] = HtmlWrappers.from_dict(payload)
            return result
        self._register_persistent_attribute(
            "_flashcard_fields",
            serialize=lambda d: {k: v.as_dict() for k, v in d.items()},
            deserialize=deserialize_flashcard_fields,
        )
        self._register_persistent_attribute("_note_tag")

        self._was_modified = False

    @PersistentStorage._ensure_loaded
    def set_anki_id(self, value: Optional[int]):
        if value is not None and not isinstance(value, int):
            raise TypeError("anki_id must be an integer.")
        self._anki_id = value
        self._was_modified = True

    @PersistentStorage._ensure_loaded
    def set_flashcard_field(
        self,
        name: str,
        value: Union[HtmlWrappers.CardSection, OngoingTask]):
        if not isinstance(name, str):
            raise TypeError(f"Field name must be a string, got {type(name)} instead: {name}")
        if not isinstance(value, (HtmlWrappers.CardSection, OngoingTask)):
            raise TypeError(f"Flashcard field must be a CardSection or OngoingTask, got {type(value)} instead: {value}")

        old_val = self._flashcard_fields.get(name)
        if (isinstance(old_val, HtmlWrappers.CardSection) and isinstance(value, HtmlWrappers.CardSection)) \
            and old_val and old_val.as_dict()[1] != value.as_dict()[1]:
            logger.warning(f"Changed existing flashcard_fields[{name}] CardSection for {self.word}, keeping new one.")
        self._flashcard_fields[name] = value
        self._was_modified = True

    def pop_flashcard_field(self, field_name):
        assert field_name in self._flashcard_fields
        self._flashcard_fields.pop(field_name)
        self._was_modified = True

    def save(self):
        if not self.json_path.exists() or self._was_modified:
            self._save_storage()

    @property
    @PersistentStorage._ensure_loaded
    def note_tag(self) -> str:
        if not self._note_tag:
            self._note_tag = uuid.uuid4().hex
            self._was_modified = True
        return self._note_tag

    @property
    @PersistentStorage._ensure_loaded
    def frontside(self):
        env = Environment(
            loader=FileSystemLoader(str(HTML_TEMPLATE_DIR)),
            autoescape=select_autoescape(["html", "xml"]),
            trim_blocks=True,
            lstrip_blocks=True,
        )

        def _render_filter(s):
            try:
                return env.from_string(str(s)).render()
            except Exception:
                return s
        env.filters["render"] = _render_filter
        template = env.get_template("flashcard_frontside.html")
        return template.render(
            word=self.word,
            uid=int(time.time() * 1000),
        )

    @property
    @PersistentStorage._ensure_loaded
    def backside(self):
        """Generate flashcard HTML."""
        with open(HTML_TEMPLATE_DIR / "static.html", "r", encoding="utf-8") as f:
            static = f.read()
        css_files = HTML_TEMPLATE_DIR.glob("*.css")
        css = "\n".join(css_file.read_text(encoding="utf-8") for css_file in css_files)
        js_files = HTML_TEMPLATE_DIR.glob("*.js")
        js = "\n".join(js_file.read_text(encoding="utf-8") for js_file in js_files)

        with open(HTML_TEMPLATE_DIR / "flashcard_backside.html", "r", encoding="utf-8") as f:
            template = Template(f.read())

        content = [field for field in self.flashcard_fields.values()]
        return template.render(
            static_content=static,
            css_content=css,
            js_content=js,
            flashcard_content="<br>".join([str(section) for section in content if section]),
            note_tag=self.note_tag,
        )

    def __str__(self):
        return '\n'.join([
            f'Card object for word: "{self.word}":\n',
            f'json_path: {self.json_path}']) + '\n' + super().__str__()
