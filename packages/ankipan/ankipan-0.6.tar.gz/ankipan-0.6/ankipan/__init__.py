from pathlib import Path
from dataclasses import dataclass
import yaml
import functools

from dataclasses import dataclass
from typing import Tuple, Iterator, Union, Any, Callable, Optional, Dict, Iterable

PROJECT_ROOT = Path(__file__).parent.parent
ANKIPAN_ROOT = PROJECT_ROOT / 'ankipan'
DEFAULT_SERVER = 'ankipan_default'

COLLECTIONS_DIR = PROJECT_ROOT / '.collections'
COLLECTIONS_DIR.mkdir(parents=True, exist_ok=True)

PROMPT_HISTORY_DIR = PROJECT_ROOT / ".prompt_history"
PROMPT_HISTORY_DIR.mkdir(parents=True, exist_ok=True)

HTML_TEMPLATE_DIR = ANKIPAN_ROOT / 'html_templates'

USER_DATA_FILE = PROJECT_ROOT / '.user_data.yaml'
if USER_DATA_FILE.exists():
    with open(USER_DATA_FILE, 'r') as f:
        USER_DATA = yaml.safe_load(f)
else:
    USER_DATA = {}

@dataclass(slots=True)
class TextSegment:
    main_index: int
    text_segments: list
    word: str
    start_s: int = None
    end_s: int = None
    translation: str = None
    source_name: str = None

    @property
    def main_segment(self): return self.text_segments[self.main_index]

@dataclass(frozen=True, slots=True)
class SourcePath:
    """Represents a logical server/category/root path."""
    path: str

    def __post_init__(self):
        parts = [p for p in self.path.split("/") if p]
        norm = "/".join(parts)
        object.__setattr__(self, "path", norm)

    @property
    def parts(self) -> Tuple[str, ...]:
        return tuple(path for path in self.path.split("/") if path) if self.path else ()

    def __iter__(self) -> Iterator[str]:
        return iter(self.parts)

    def __len__(self) -> int:
        return len(self.parts)

    def __getitem__(self, idx: Union[int, slice]) -> Union[str, "SourcePath"]:
        if isinstance(idx, slice):
            return SourcePath("/".join(self.parts[idx]))
        return self.parts[idx]

    def __truediv__(self, child: str) -> "SourcePath":
        child = "/".join(p for p in child.split("/") if p)
        return SourcePath(f"{self.path}/{child}" if self.path else child)

    def __str__(self) -> str:
        return self.path

class PersistentStorage:
    @dataclass
    class RegisteredField:
        exposed_name: str
        serialize: Callable[[Any], Any]
        deserialize: Callable[[Any], Any]

    def __init__(self, json_path: Path):
        self.json_path = Path(json_path)
        self._registered_fields: Dict[str, PersistentStorage.RegisteredField] = {}
        self._is_loaded = False

    def _register_persistent_attribute(
        self,
        attr_name: str,
        *,
        serialize: Optional[Callable[[Any], Any]] = None,
        deserialize: Optional[Callable[[Any], Any]] = None
    ) -> None:
        """
        Register an *already existing* instance attribute for persistence.

        Parameters
        ----------
        attr_name : str
            The actual attribute on the instance, e.g. "_learning_lang".
        serialize : Callable, optional
            Function to custom-serialize variable for json storage.
            If not specified, just try to directly serialize data.
        deserialize : Callable, optional
            Function to custom-deserialize variable from json storage.
            If not specified, just adopt directly from json.
        """
        if not attr_name.startswith("_"):
            raise RuntimeError(f'Invalid persistent attribute name "{attr_name}", need to be specified as private by prepending a "_"')

        if serialize is None:
            serialize = lambda x: x
        if deserialize is None:
            deserialize = lambda x: x

        exposed_name = attr_name[1:] # remove prepended "_"
        cls = self.__class__
        if not hasattr(cls, exposed_name):
            def make_getter(private_name):
                def getter(self):
                    self._load_from_storage()
                    return getattr(self, private_name)
                return getter
            setattr(cls, exposed_name, property(make_getter(attr_name)))
        self._registered_fields[attr_name] = self.RegisteredField(
            serialize=serialize,
            deserialize=deserialize,
            exposed_name=exposed_name
        )

    def _load_from_storage(self) -> None:
        """Load JSON (once) and apply values to registered attributes."""
        if self._is_loaded:
            return

        data_from_file = {}
        if self.json_path.exists():
            data_from_file = load_json(self.json_path)

        for attr_name, field in self._registered_fields.items():
            if attr_name in data_from_file:
                loaded_value = field.deserialize(data_from_file[attr_name])
                setattr(self, attr_name, loaded_value)
        self._is_loaded = True

    @staticmethod
    def _ensure_loaded(method):
        """Decorator: make sure the object is loaded before calling the method."""
        @functools.wraps(method)
        def wrapper(self, *args, **kwargs):
            self._load_from_storage()
            return method(self, *args, **kwargs)
        return wrapper

    def as_dict(self, serialize: bool = True) -> Dict[str, Any]:
        """Return a JSON-serializable dict of all registered attributes."""
        self._load_from_storage()
        result = {}
        for attr_name, field in self._registered_fields.items():
            value = getattr(self, attr_name)
            if value is None:
                continue
            # TODO find intuitive way to show usages of two branches
            if serialize:
                result[attr_name] = field.serialize(value)
            else:
                result[field.exposed_name] = value
        return result

    def _save_storage(self) -> None:
        self._load_from_storage()
        data = self.as_dict()
        self.json_path.parent.mkdir(parents=True, exist_ok=True)
        save_json(self.json_path, data)

    def __str__(self) -> str:
        self._load_from_storage()
        lines = []
        for attr_name, field in self._registered_fields.items():
            value = getattr(self, attr_name)

            def format_value(x, indent=4):
                pad = " " * indent
                max_items = 15
                if isinstance(x, list):
                    if not x:
                        return "[]"
                    shown = x[:max_items]
                    items = ",\n".join(f"{pad}{repr(v)}" for v in shown)
                    if len(x) > max_items:
                        items += f",\n{pad}..."
                    return f"[\n{items}\n{pad[:-4]}]"
                if isinstance(x, dict):
                    if not x:
                        return "{}"
                    kvs = list(x.items())
                    shown = kvs[:max_items]
                    items = ",\n".join(
                        f"{pad}{repr(k)}: {format_value(v, indent + 4)}"
                        for k, v in shown
                    )
                    if len(kvs) > max_items:
                        items += f",\n{pad}..."
                    return f"{{\n{items}\n{pad[:-4]}}}"
                return repr(x)

            name = field.exposed_name
            if isinstance(value, (list, dict)) and value is not None and len(value) > 15:
                name = f"{name} ({len(value)})"
            lines.append(f"{name}: {format_value(value)}")

        return "\n".join(lines) if lines else "<no registered persistent attributes>"

    def __repr__(self) -> str:
        return self.__str__()

from .util import *
from .config import Config
from .html_templates._wrappers import HtmlWrappers, OngoingTask
from .client import Client
from .gpt_base import GPTBase, GPTQueue
from .anki_manager import AnkiManager
from .reader import Reader, File
from .card import Card
from .deck import Deck
from .collection import Collection
from .flashcard_fields import FieldBase, get_flashcard_field_registry
