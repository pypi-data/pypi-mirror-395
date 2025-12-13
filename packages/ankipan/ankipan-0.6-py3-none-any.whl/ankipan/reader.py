
import re
import pysubs2
import os
from collections import Counter
from concurrent.futures import ThreadPoolExecutor, as_completed
from tqdm.notebook import tqdm
from pathlib import Path
from typing import Union, Dict, Iterable, List, Optional, Tuple
import pickle
import logging
import chardet
import re
from bs4 import BeautifulSoup
import unicodedata
from langdetect import detect
from langdetect.lang_detect_exception import LangDetectException
import threading, itertools, math
import fitz

_tls = threading.local()

from ankipan import PROJECT_ROOT

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

hanta_map = {
    'de': 'morphmodel_ger.pgz'
}
_nlp_hanta = None

stanza_map = {
    'jp': 'ja'
}

STANZA_DELIMITER = '\n\n'

ASCII_PUNCT = r"!\"#\$%&'\(\)\*\+,\-./:;<=>\?@\[\]\\\^_`{\|\}~"
# General + Supplemental + CJK punct + Fullwidth punct (subset)
UNI_PUNCT_BLOCKS = "\u2000-\u206F\u2E00-\u2E7F\u3000-\u303F\uFF01-\uFF65"

ALLOWED = rf"\w\s{UNI_PUNCT_BLOCKS}{ASCII_PUNCT}"
pattern = re.compile(rf"[^{ALLOWED}]")

torch_ = None

class Reader():
    def __init__(self, learning_lang):
        self.learning_lang = learning_lang
        self.corpus_occurrences_ = None
        self._pipelines = {}
        self._pipelines_lock = threading.Lock()
        self._pipeline_run_locks = {}

    @property
    def torch(self):
        global torch_
        if not torch_:
            import torch
            torch_ = torch
        return torch_

    def make_stanza_pipeline(self, device_id: Optional[int]):
        import stanza
        use_gpu = device_id is not None
        stanza_lang_name = stanza_map.get(self.learning_lang, self.learning_lang)
        if use_gpu:
            self.torch.cuda.set_device(device_id)
        kwargs = dict(
            processors="tokenize,pos,lemma",
            use_gpu=use_gpu,
            tokenize_mode="A",
            download_method=None,
            tokenize_no_ssplit=True
        )
        if use_gpu:
            kwargs["device"] = device_id
        try:
            return stanza.Pipeline(stanza_lang_name, **kwargs)
        except (stanza.pipeline.core.LanguageNotDownloadedError,
                stanza.resources.common.ResourcesFileNotFoundError,
                FileNotFoundError, ValueError):
            print(f"Downloading stanza model for {stanza_lang_name}...")
            stanza.download(stanza_lang_name)
            return stanza.Pipeline(stanza_lang_name, **kwargs)

    def _get_shared_pipeline(self, device_id: Optional[int]):
        key = device_id if device_id is not None else "cpu"
        with self._pipelines_lock:
            p = self._pipelines.get(key)
            if p is None:
                p = self.make_stanza_pipeline(device_id)
                self._pipelines[key] = p
                if key not in self._pipeline_run_locks:
                    self._pipeline_run_locks[key] = threading.Lock()
        return p

    @property
    def corpus_occurrences(self):
        if self.corpus_occurrences_ is None:
            try:
                # TODO: Dependency to parent folder not good
                with open(f'{PROJECT_ROOT}/corpus_resources/{self.learning_lang}.pkl', "rb") as f:
                    self.corpus_occurrences_ = pickle.load(f)
            except:
                self.corpus_occurrences_ = Counter()
        return self.corpus_occurrences_

    def collect_file_paths(self, path, exclude_paths = None, file_match_pattern = None, dir_match_pattern = None):
        compiled_file_pattern = re.compile(file_match_pattern) if file_match_pattern else None
        compiled_dir_pattern = re.compile(dir_match_pattern) if dir_match_pattern else None
        if not exclude_paths:
            exclude_paths = set()
        else:
            exclude_paths = {os.path.normcase(Path(path).as_posix()) for path in exclude_paths}
        def allowed(p: Path) -> bool:
            path_normed = os.path.normcase(p.as_posix())
            if path_normed in exclude_paths:
                logger.info(f'Skipping path {p}, listed in exclude paths')
                return False
            if compiled_file_pattern and not compiled_file_pattern.match(p.name):
                logger.info(f'Skipping path {p}, matches compiled_file_pattern')
                return False
            return True

        file_paths = set()
        path = Path(path)

        if path.is_file():
            cleaned_path = Path(path).relative_to(path.parent)
            if allowed(cleaned_path):
                file_paths.add(path)

        elif path.is_dir():
            for root, dirs, files in os.walk(path):
                if compiled_dir_pattern:
                    dirs[:] = [d for d in dirs if compiled_dir_pattern.fullmatch(d)]
                    if not compiled_dir_pattern.fullmatch(Path(root).name):
                        continue
                for filename in files:
                    if compiled_file_pattern and not compiled_file_pattern.fullmatch(filename):
                        continue
                    cleaned_path = Path(root, filename).relative_to(path.parent)
                    if allowed(cleaned_path):
                        file_paths.add(Path(root, filename))
        else:
            raise RuntimeError(f'Path does not exist: "{path}"')
        return file_paths

    def detect_languages(self, file_contents, n_chunks = 10):
        """
        Currently used to assert integrity of files (only one language used)

        """
        part_length = len(file_contents) // n_chunks
        parts = [file_contents[i * part_length:(i + 1) * part_length] for i in range(n_chunks)]

        detected_languages = set()
        for part in parts:
            try:
                lang = detect(part)
                detected_languages.add(lang)
            except LangDetectException:
                continue
        return detected_languages

    def clean_string(self, string, chars_to_filter=None):
        ESCAPE_PATTERN = re.compile(r"\\[A-Za-z0-9_]+")
        # https://www.unicode.org/reports/tr44/tr44-34.html#General_Category_Values
        REMOVE_CATEGORIES = {
            "Cc", "Cf", "Cs", "Co", "Cn",
            "Zl", "Zp",
        }
        string = string.replace("\\N", "\n").replace("\\n", "\n")
        string = ESCAPE_PATTERN.sub("", string)
        result_chars = []
        for c in string:
            cat = unicodedata.category(c)
            if c == "\n":
                result_chars.append(c)
            elif cat not in REMOVE_CATEGORIES:
                result_chars.append(c)

        string = "".join(result_chars)
        if chars_to_filter:
            for char_to_filter in chars_to_filter:
                replacement = " "
                if isinstance(char_to_filter, tuple):
                    char_to_filter, replacement = char_to_filter
                string = re.sub(char_to_filter, replacement, string)
        return string

    @staticmethod
    def prepare_stanza_input(raw_text, index_separators, secondary_separators, lookahead=24):
        text = raw_text
        for sep in index_separators:
            text = text.replace(sep, f"{sep}{STANZA_DELIMITER}")
        stanzas = text.split(STANZA_DELIMITER)

        def split_soft(s: str, L: int, look: int = 24) -> list[str]:
            s = s.strip()
            if L is None or L <= 0 or len(s) <= L:
                return [s] if s else []
            out, i, n = [], 0, len(s)
            while n - i > L:
                window = s[i:i+L+1]
                left_ws = [m.start() for m in re.finditer(r"\s", window)]
                if left_ws:
                    cut = i + left_ws[-1]
                else:
                    m = re.search(r"\s", s[i+L:i+L+look+1])
                    cut = (i + L + m.start()) if m else (i + L)
                head = s[i:cut].rstrip()
                if head:
                    out.append(head)
                i = cut
                while i < n and s[i].isspace():
                    i += 1
            tail = s[i:].strip()
            if tail:
                out.append(tail)
            return out

        final = []
        for s in stanzas:
            if not s:
                continue
            tokens = re.split(f"({'|'.join(map(re.escape, secondary_separators))})", s) if secondary_separators else [s]
            out, buf = [], ""
            for t in tokens:
                buf += t
            if buf.strip():
                out.append(buf.strip())
            for piece in out:
                final.extend(split_soft(piece, len(piece), lookahead))
        return STANZA_DELIMITER.join(final)

    def open_files(self,
                   file_paths: List[Union[str, Path]],
                   replace_chars: List[str] = None,
                   source_name: str = None,
                   assert_coherence: bool = False,
                   index_separators: Iterable[str] = None,
                   secondary_separators: Iterable[str] = None):

        """
        Extract raw text from list of files.

        Valid formats:
        - Any raw text (.txt etc.)
        - Subtitles (.ass, .srt)
        - Websites (.html)

        Parameters:
        -----------

        file_paths: list of files to process
        replace_chars: List of characters to be removed when processing
        source_name: Allows for special parcing of content on specific websites in parse_html
            Currently only have rule for ['wikipedia']
        assert_coherence: check if files have sentences in more than one language, skip if that is the case.
        index_separators: Custom delimiter to text into small segments.
            Only relevant if we want to create example sentences from this in the db.
            Subtitles are already segmented in small chunks by default.
            If left empty, a custom segmentation of newlines, dots and commas will be used.

        """

        index_separators_ = index_separators if index_separators else ['\n', '.', '。', '!', '?']
        secondary_separators_ = secondary_separators if secondary_separators else [',', ';', '、']
        files = []
        processed_words = {} # caching past results

        for file_path in file_paths:
            logger.debug(f'Opening file {file_path}')
            file_path = Path(file_path)
            with open(file_path, 'rb') as f:
                raw_data = f.read()
            encoding_result = chardet.detect(raw_data)
            encoding = encoding_result['encoding']
            if not encoding:
                encoding = 'utf-8'
            try:
                raw_file_contents = raw_data.decode(encoding, errors='replace')
            except LookupError as e:
                raise RuntimeError(f'Decode error: {e}')
            file_contents = None
            sub_timestamps = None

            logger.debug(f'Reading file {file_path}')
            if file_path.suffix in ['.ass', '.srt']:
                if index_separators:
                    raise RuntimeError('index_separators not used when parsing subs')
                try:
                    file_contents, sub_timestamps = self.parse_subs(raw_file_contents, replace_chars=replace_chars)
                except Exception as e:
                    logger.error(f'Error: "{file_path}": {type(e).__name__} - {e}')
            elif file_path.suffix in ['.pdf']:
                try:
                    file_contents = self.parse_pdf(file_path)
                except Exception as e:
                    logger.warning(f'Reading pdf file "{file_path}" failed, skipping...')
            else:
                if file_path.suffix in ['.html']:
                    raw_file_contents = self.parse_html(raw_file_contents, source_name = source_name)
                file_contents = self.prepare_stanza_input(self.clean_string(raw_file_contents,
                                                                            replace_chars),
                                                                            index_separators_,
                                                                            secondary_separators_)

            if file_contents:
                if assert_coherence and len(file_contents) > 500: # TODO: Find more efficient way to ignore parts of the file that have a different language than the learning one
                    langs = self.detect_languages(file_contents)
                    if len(langs)>1:
                        logger.error(f"Skipping file {file_path}, Multiple languages detected: {langs}")
                        continue
                files.append(File(self.learning_lang,
                                  file_contents,
                                  processed_words=processed_words,
                                  path=file_path,
                                  sub_timestamps=sub_timestamps))
        return sorted(files, key=lambda x: x.path.name)

    def process_files(self, files, save_pos_data=False, n_threads=5, save_sentence_mapping=False, silent=False):
        try:
            n_devices = self.torch.cuda.device_count()
            has_cuda = self.torch.cuda.is_available() and n_devices > 0
        except Exception:
            has_cuda, n_devices = False, 0

        if has_cuda:
            gpu_ids = list(range(n_devices))
            per_gpu = max(1, math.ceil(n_threads / n_devices))
            pool = list(itertools.chain.from_iterable([[d]*per_gpu for d in gpu_ids]))
        else:
            pool = [None] * n_threads

        device_iter = itertools.cycle(pool)
        device_assign_lock = threading.Lock()

        def _device_key(dev_id):
            return dev_id if dev_id is not None else "cpu"

        def _process_file(file):
            if not hasattr(_tls, "device_id"):
                with device_assign_lock:
                    _tls.device_id = next(device_iter)

            device_id = _tls.device_id
            key = _device_key(device_id)
            pipeline = self._get_shared_pipeline(device_id)
            run_lock = self._pipeline_run_locks[key]

            with run_lock:
                file.analyze_lemmas(pipeline, save_pos_data=save_pos_data, save_sentence_mapping=save_sentence_mapping)

        with ThreadPoolExecutor(max_workers=n_threads) as ex:
            futures = [ex.submit(_process_file, f) for f in files]
            for fut in tqdm(as_completed(futures), total=len(futures), desc="Extracting lemmas", disable=silent):
                fut.result()

    def parse_html(self, file_contents: str, source_name = None) -> str:
        """
        Clean html files to extract text (relevant for scraped pages)

        """
        soup = BeautifulSoup(file_contents, 'lxml')
        if source_name == 'wikipedia':
            if soup.find('meta', attrs={'http-equiv': 'Refresh'}):
                return ""
            body_content_div = soup.find('div', id='bodyContent')
            text = ""
            if body_content_div:
                paragraphs = body_content_div.find_all('p')
                for paragraph in paragraphs:
                    text += paragraph.get_text() + "\n"
            clean_text = re.sub(r'\[.*?\]', '', text)
            clean_text = re.sub(r'[^\x00-\x7F]+', '', clean_text)
        else:
            clean_text = soup.get_text()
        return clean_text.strip()

    sub_filter_expressions = {
        'jp': [r'《', r'》', r'（.*?）', r'\[.*\]', r'\{.*?\}', r'\(.*?\)', '\u3000', '\n', '“','”','「','」',
            r'\\N', r'\n', '…', '→', '〉', '〈', '‥', '⁉', r'[\u2460-\u2473]', '‪', '‬', r'\r', r'  '],
        'de': [r'\{.*?\}', r'\\N'],
    }

    def parse_subs(self, file_contents: str, replace_chars: list[str] | None = None):
        try:
            subs = pysubs2.SSAFile.from_string(file_contents)
        except Exception:
            subs = pysubs2.SSAFile.from_string(file_contents, format="srt")

        def is_jp_dialogue(text: str) -> bool:
            non_dialogue = [r'---', r'翻译:', r'www\.', '字幕組', '校对', '后期', '广告', '制作成员']
            if any(re.search(p, text) for p in non_dialogue):
                return False
            # if re.search(r'[\u3000\u3040-\u30ff\u4e00-\u9fff]+', text):
            #     return True
            return True

        segment_texts: list[str] = []
        sub_timestamps: list[tuple[int, int]] = []

        for line in subs:
            raw = line.text
            cleaned = self.clean_string(raw, self.sub_filter_expressions.get(self.learning_lang, []) + (replace_chars or []))
            if self.learning_lang == 'jp' and not is_jp_dialogue(cleaned):
                continue
            cleaned = cleaned.replace("\r\n", " ").replace("\n", " ").strip()
            cleaned = re.sub(r"\s+", " ", cleaned)
            if not cleaned:
                continue
            start_sec = round(line.start / 1000)
            end_sec   = round(line.end  / 1000)
            segment_texts.append(cleaned)
            sub_timestamps.append((start_sec, end_sec))
        final_text = STANZA_DELIMITER.join(segment_texts).strip()
        return final_text, sub_timestamps

    def parse_pdf(self, pdf_path):
        parts = []
        with fitz.open(pdf_path) as doc:
            for page in doc:
                txt = page.get_text("text", sort=True)
                txt = re.sub(r"[ \t]+", " ", txt)
                txt = re.sub(r"\n", "", txt).strip()
                parts.append(txt)
        return "".join(parts)

class File:
    def __init__(self,
                 learning_lang,
                 content: str,
                 processed_words: Dict[str, str] = None,
                 path = None,
                 sub_timestamps: List[Tuple[int, int]] = None):
        self.learning_lang = learning_lang
        self.path = path
        self.content = content
        self.processed_words = processed_words if processed_words else {}
        self.sub_timestamps = sub_timestamps # text indices -> time on screen
        self.stanza_segments = None
        self.lemma_word_index_mapping = {}

        # Variables to be written to when we are adding this source to the main db (TODO: move this from ankipan to ankipan_db)
        self.text_segment_components = []
        self.lemma_counts = Counter()

    @property
    def nlp_hanta(self):
        global _nlp_hanta
        if _nlp_hanta is None:
            try:
                from HanTa import HanoverTagger as ht
                _nlp_hanta = ht.HanoverTagger(hanta_map[self.learning_lang]) if self.learning_lang in hanta_map.keys() else None
            except ImportError:
                logger.warning('HanTa parser not installed, recommended for lemmatizing german text (pip install hanta)')
                _nlp_hanta = False
        return _nlp_hanta


    def parse_stanza_segments(self,
                              nlp_stanza,
                              content: str,
                              batch_max_chars: int): # see https://stanfordnlp.github.io/stanza/tokenize.html#options

        sentences_concat = []
        i, n = 0, len(content)
        while i < n:
            if n - i <= batch_max_chars:
                cut = n
            else:
                j = content.find(STANZA_DELIMITER, i + batch_max_chars)
                cut = n if j == -1 else j + len(STANZA_DELIMITER)
            chunk = content[i:cut]
            if chunk:
                try:
                    doc = nlp_stanza(chunk)
                except torch_.cuda.OutOfMemoryError as e:
                    raise
                sentences_concat.extend(doc.sentences)
            i = cut
        return sentences_concat

    def analyze_lemmas(self, nlp_stanza, save_pos_data=False, save_sentence_mapping=False, *, batch_max_chars=1000):
        logger.debug(f'Analyzing lemmas for {self.path}')
        self.stanza_segments = self.parse_stanza_segments(
            nlp_stanza,
            self.content,
            batch_max_chars)
        for segment_idx, stanza_segment in enumerate(self.stanza_segments):
            metadata = []
            # TODO: collect words in list first, then fetch available lemmas from db
            for token_idx, stanza_token in enumerate(stanza_segment.words):
                word = stanza_token.text
                pos = stanza_token.pos
                xpos = stanza_token.xpos
                if (word, pos) in self.processed_words:
                    self.lemma_counts[self.processed_words[(word, pos)]['lemma']] = self.lemma_counts.get(self.processed_words[(word, pos)]['lemma'], 0) + 1
                    if save_pos_data:
                        metadata.append({
                            'word': word,
                            'lemma': self.processed_words[(word, pos)]['lemma'],
                            'pos': pos,
                            'xpos': self.processed_words[(word, pos)]['xpos']})
                else:
                    lemma = None
                    if self.learning_lang=='jp':
                        # we primarily care about words with kanjis in them (hence [\u4E00-\u9FD0])
                        if stanza_token.lemma and re.search(r'[\u4E00-\u9FD0]+', stanza_token.lemma) and re.search(r'[\u4E00-\u9FD0]+', stanza_token.text):
                            lemma = stanza_token.lemma
                    elif pos in ["NOUN", "VERB", "ADJ", "ADV", "AUX", "PROPN"] and \
                         (xpos) != 'NE' and stanza_token.lemma:
                        if self.learning_lang=='de' and self.nlp_hanta != False:
                            try:
                                hanta_lemmas = self.nlp_hanta.tag_sent([token.text for token in stanza_segment.words])
                                hanta_lemma = hanta_lemmas[token_idx] if token_idx < len(hanta_lemmas)-1 and hanta_lemmas[token_idx][0] == stanza_token.text else \
                                            self.nlp_hanta.tag_sent([stanza_token.text])[0]
                                lemma = hanta_lemma[1] if len(hanta_lemma)>=3 else stanza_token.lemma
                            except IndexError as e:
                                print(f"Hanta Error: {e}")
                                lemma = stanza_token.lemma
                        else:
                            lemma = stanza_token.lemma
                    if lemma:
                        self.lemma_counts[lemma] = self.lemma_counts.get(lemma, 0) + 1
                        if save_pos_data:
                            metadata.append({
                                'word': word,
                                'lemma': lemma,
                                'pos': pos,
                                'xpos': xpos})
                        if word not in self.processed_words:
                            self.processed_words[(word, pos)] = {'lemma': lemma, 'xpos': xpos}
                        if save_sentence_mapping:
                            self.lemma_word_index_mapping.setdefault(lemma, {}).setdefault(word, []).append(segment_idx)
                # print("======================= DEBUG =============================")
                # print("stanza_token.lemma",stanza_token.lemma)
                # print("stanza_token.text",stanza_token.text)
                # print("stanza_token.pos",pos, stanza_token.pos)
                # print("stanza_token.xpos",xpos, stanza_token.xpos)
                # print("hanta_lemma",hanta_lemma)
            if save_pos_data:
                self.text_segment_components.append(metadata)
