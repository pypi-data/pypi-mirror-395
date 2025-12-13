from datetime import datetime
import re
import logging
import threading
import time
from collections import defaultdict, deque
import uuid
import os
import sys
import traceback

from typing import List, Dict, Tuple, Deque, Optional

from ankipan import Config, TextSegment, PROMPT_HISTORY_DIR

logger = logging.getLogger(__name__)

logger = logging.getLogger(__name__)

language_mapping = {
    'de': 'german',
    'en': 'english',
    'jp': 'japanese',
    'fr': 'french'
}

class GPTBase:
    """
    Base abstraction for text generation/translation backends.

    Usage notes:
    - Remote vs. local: set `collection.use_server_gpt = False` to bypass the
      Ankipan server and run translations locally via this class.
    - Gemini API: call `ankipan.Config.set_gemini_api_key("<YOUR_API_KEY>")`
      before using Gemini-backed translations.
    - Local Ollama: install and run Ollama locally (default http://127.0.0.1:11434),
      then set `ankipan.Config.set_ollama_model_name("<model_name>")` (e.g.
      "llama3"). With `use_server_gpt=False`, GPTBase will call that local model
      instead of the hosted server.
    """
    def __init__(self):
        self.ollama_model_name = Config.get_ollama_model_name()
        if self.ollama_model_name:
            from ollama import Client
            self.client = Client(host='http://127.0.0.1:11434')  # default Ollama API

        self.model_deterministic = None
        self.ResourceExhaustedException = None
        import google.generativeai as genai
        from google.api_core import exceptions as google_exceptions
        self.ResourceExhaustedException = google_exceptions.ResourceExhausted
        genai.configure(api_key=Config.get_gemini_api_key())
        self.model_deterministic = genai.GenerativeModel(
            "gemini-2.5-flash",
            generation_config={"temperature": 0.1}
        )

    def _prompt_gpt(self, prompt: str, prompt_type: str, wait_time: int = 10) -> str:
        def save_response(response_text: str):
            timestamp_day = datetime.now().strftime('%Y-%m-%d')
            timestamp_time = datetime.now().strftime('%H-%M-%S')
            history_path = PROMPT_HISTORY_DIR / f'{prompt_type}_{timestamp_day}_{timestamp_time}.txt'
            with open(history_path, 'w', encoding='utf-8') as f:
                f.write(prompt +
                        '\n_____________________________________________________________________________________________________________\n\n' +
                        response_text)

        def try_gemini() -> str | None:
            if not self.model_deterministic:
                return None
            try:
                return self.model_deterministic.generate_content(prompt).text
            except self.ResourceExhaustedException as e:
                logger.info(f"Gemini quota exceeded (429): {e}. Will retry or fall back...")
                return None
            except Exception as e:
                logger.warning(f"Unexpected Gemini error: {e}")
                return None

        def try_ollama() -> str | None:
            if not (self.client and self.ollama_model_name):
                return None
            try:
                response = self.client.chat(
                    model=self.ollama_model_name,
                    messages=[{'role': 'user', 'content': prompt}]
                )
                content = response['message']['content']
                return content.split('</think>')[-1].strip()
            except Exception as e:
                # Ollama typically raises ConnectionError, HTTPError, or generic Exception when queue is full
                logger.info(f"Ollama queue full or rate-limited: {e}. Retrying in 10s...")
                return None

        max_attempts = 10
        for attempt in range(1, max_attempts + 1):
            response_text = None
            if self.model_deterministic:
                response_text = try_gemini()
                if response_text is not None:
                    save_response(response_text)
                    return response_text
            if self.client and self.ollama_model_name:
                response_text = try_ollama()
                if response_text is not None:
                    save_response(response_text)
                    return response_text
            if attempt < max_attempts:
                logger.info(f"Both backends unavailable (attempt {attempt}/{max_attempts}). Waiting {wait_time}s before retry...")
                time.sleep(wait_time)
            else:
                raise Exception(
                    "All LLM backends exhausted after multiple retries. "
                    "Gemini may be quota-limited; Ollama may be at OLLAMA_NUM_PARALLEL/MAX_QUEUE limit."
                )
        raise Exception("Unexpected exit from LLM retry loop")

    def translate_text_segments(
        self,
        native_lang: str,
        learning_lang: str,
        example_sentences: List[TextSegment],
        max_batch_size: int = 20,
        max_depth: int = 3,
    ) -> List[str]:
        """
        Given a list of TextSegment, return a list of translations in the same order.
        """
        if not example_sentences:
            return []

        def translate_batch(batch: List[TextSegment], depth: int) -> List[str]:
            """Translate exactly this batch or split if the model response is misaligned."""
            try:
                response = self._prompt_translation(native_lang, learning_lang, batch)
                parsed = self._parse_translation_response(response)

                if len(parsed) == len(batch):
                    return parsed

                if depth >= max_depth or len(batch) == 1:
                    raise RuntimeError(
                        f"Failed to translate batch of size {len(batch)} at depth {depth}"
                    )
            except ValueError: # gemini hatespeech detector
                pass

            mid = len(batch) // 2
            left = translate_batch(batch[:mid], depth + 1)
            right = translate_batch(batch[mid:], depth + 1)
            return left + right

        translations: List[str] = []
        for start in range(0, len(example_sentences), max_batch_size):
            batch = example_sentences[start:start + max_batch_size]
            translations.extend(translate_batch(batch, depth=0))

        return translations

    def _prompt_translation(self, native_lang, learning_lang, example_sentences: List[TextSegment]):
        formatted_sentences = []
        words = set()
        for example_sentence in example_sentences:
            words.add(example_sentence.word)
            formatted_sentences.append('- ' + ' '.join([text_segment if i != example_sentence.main_index else f'[{text_segment}]'
                                        for i, text_segment in enumerate(example_sentence.text_segments)]))

        formatted_sentences_str = '\n'.join(formatted_sentences)
        prompt = f'''We have a set of text snippets, which we would like to translate from {language_mapping[learning_lang]} to {language_mapping[native_lang]}.
While we provide some context, we are only interested in the main part of the snippet that is wrapped in [] braces.
This means that we only want the translation of the text in the [] braces, and nothing else, the surrounding text is just used for context but should not be included in the translation.

We also want to add an concise explanation of how and why certain words are used in the original text.
Here, we care about really detailed nuances in the translation from {language_mapping[learning_lang]} to {language_mapping[native_lang]}.
We want to fully understand all the nuances of the translation and why specific words make sense in this context.
This is especially relevant, if some of the words in the original text don't have a direct translation counterpart that conveys the exact same nuances in {language_mapping[native_lang]}.
This additional explanation should be short and concise, and be added in () braces after the translation, which should be written as free text.

The answer must follow exactly the following formatting:

- <translation> (<translation_explanation>)
- <translation> (<translation_explanation>)
- <translation> (<translation_explanation>)
...

What would that look like for the following text segments?

{formatted_sentences_str}

    '''
        return self._prompt_gpt(prompt, 'translation')

    def _parse_translation_response(self, prompt_response):
        _BULLET_RE = re.compile(r"""
            ^\s*[-•]\s*
            (?P<translation>.*?)
            (?:\s*\((?P<comment>[^()]*)\)\s*)?$
        """, re.MULTILINE | re.VERBOSE)
        items = []
        for m in _BULLET_RE.finditer(prompt_response):
            items.append(
                f'{m.group("translation").strip()}<br>'
                f'{("(" + (m.group("comment") or "").strip() + ")") if m.group("comment") else ""}'
            )
        return items

def fatal_from_thread(context: str) -> None:
    """
    Log full traceback and immediately terminate the process.
    This is meant to be called from non-main threads on unrecoverable errors.
    """
    tb = traceback.format_exc()
    print(f"FATAL in {context}:\n{tb}", file=sys.stderr, flush=True)
    logger.critical("FATAL in %s:\n%s", context, tb)
    root_logger = logging.getLogger()
    for handler in root_logger.handlers:
        try:
            handler.flush()
        except Exception:
            pass
    os._exit(1)

class _GPTWorkItem:
    def __init__(self, learning_lang: str, native_lang: str, segment: TextSegment):
        self.learning_lang = learning_lang
        self.native_lang = native_lang
        self.segment = segment

class GPTQueue:
    def __init__(
        self,
        max_batch_size: int = 20,
        batch_wait_seconds: float = 5.0,
    ):
        self.gpt_base = GPTBase()
        self.max_batch_size = max_batch_size
        self.batch_wait_seconds = batch_wait_seconds

        self.queues: dict[Tuple[str, str], Deque[_GPTWorkItem]] = defaultdict(deque)
        self.queue_first_enqueue_time: dict[Tuple[str, str], float] = {}
        self.queue_last_enqueue_time: dict[Tuple[str, str], float] = {}

        self.tasks: Dict[str, Dict] = {}
        self.lock = threading.Lock()
        self._stop_event = threading.Event()
        self._worker_thread: Optional[threading.Thread] = None

    def start_thread(self):
        with self.lock:
            if self._worker_thread and self._worker_thread.is_alive():
                return
            if self._stop_event.is_set():
                raise RuntimeError("Translation queue is shutting down")
            worker = threading.Thread(target=self._worker_loop, daemon=True)
            self._worker_thread = worker
        worker.start()

    def stop_thread(self, wait: bool = False):
        self._stop_event.set()
        worker = self._worker_thread
        if wait and worker and worker.is_alive():
            worker.join()
        if worker and not worker.is_alive():
            with self.lock:
                if self._worker_thread is worker:
                    self._worker_thread = None

    def shutdown(self, wait: bool = False):
        self.stop_thread(wait=wait)

    def register_task(
        self,
        learning_lang: str,
        native_lang: str,
        segments: List[TextSegment],
    ) -> str:
        if self._stop_event.is_set():
            raise RuntimeError("Translation queue is shutting down")
        task_id = str(uuid.uuid4())
        with self.lock:
            self.tasks[task_id] = {
                "learning_lang": learning_lang,
                "native_lang": native_lang,
                "segments": segments,
            }

        missing = 0
        for seg in segments:
            if not seg.translation:
                self.enqueue(learning_lang, native_lang, seg)
                missing += 1
        logger.debug("register_task: task_id=%s enqueued_missing=%d", task_id, missing)
        return task_id

    def enqueue(self, learning_lang: str, native_lang: str, segment: TextSegment):
        if self._stop_event.is_set():
            raise RuntimeError("Translation queue is shutting down")
        with self.lock:
            key = (learning_lang, native_lang)
            queue = self.queues[key]
            was_empty = len(queue) == 0
            queue.append(_GPTWorkItem(learning_lang, native_lang, segment))
            now = time.time()
            self.queue_last_enqueue_time[key] = now
            if was_empty:
                self.queue_first_enqueue_time[key] = now
            logger.debug(
                "enqueue: key=%s len=%d first_wait=%.3fs last_enq=%.3fs",
                key,
                len(queue),
                now - self.queue_first_enqueue_time.get(key, now),
                now,
            )

    def get_task_status(self, task_id: str):
        with self.lock:
            task = self.tasks.get(task_id)
        if task is None:
            logger.debug("get_task_status: task_id=%s -> missing", task_id)
            return "missing"

        pending = [seg for seg in task["segments"] if not seg.translation]
        if not pending:
            logger.debug("get_task_status: task_id=%s -> done", task_id)
            return "done"
        if self._stop_event.is_set():
            logger.debug("get_task_status: task_id=%s -> cancelled (shutdown)", task_id)
            return "cancelled"
        logger.debug("get_task_status: task_id=%s -> pending", task_id)
        return "pending"

    def pop_task(self, task_id: str):
        with self.lock:
            self.tasks.pop(task_id, None)
        logger.debug("pop_task: task_id=%s removed", task_id)

    def enqueue_and_wait_for_tasks(self, learning_lang, native_lang, text_segments) -> None:
        tr_task_id = self.register_task(learning_lang,
                                        native_lang,
                                        text_segments)
        while True:
            status = self.get_task_status(tr_task_id)
            if status == "done":
                self.pop_task(tr_task_id)
                return
            if status in {"cancelled", "missing"}:
                self.pop_task(tr_task_id)
                raise RuntimeError(f"GPT Queue task id {tr_task_id} not found")
            time.sleep(1)

    def _worker_loop(self):
        logger.info("GPTQueue worker thread started")
        try:
            while not self._stop_event.is_set():
                now = time.time()
                with self.lock:
                    keys = list(self.queues.keys())
                logger.debug("worker: tick, active_keys=%s", keys)

                for key in keys:
                    if self._stop_event.is_set():
                        break

                    with self.lock:
                        q = self.queues.get(key)
                        if not q:
                            continue
                        queue_len = len(q)
                        first_enq = self.queue_first_enqueue_time.get(key, 0.0)
                        last_enq = self.queue_last_enqueue_time.get(key, first_enq)

                    if queue_len == 0:
                        continue

                    wait_elapsed = now - first_enq
                    since_last_enq = now - last_enq
                    should_process = (
                        queue_len >= self.max_batch_size
                        or wait_elapsed >= self.batch_wait_seconds
                    )

                    if not should_process:
                        logger.debug(
                            "worker: deferring key=%s len=%d wait_elapsed=%.3fs "
                            "threshold=%.3fs since_last_enq=%.3fs",
                            key,
                            queue_len,
                            wait_elapsed,
                            self.batch_wait_seconds,
                            since_last_enq,
                        )
                        continue

                    with self.lock:
                        q = self.queues.get(key)
                        if not q:
                            logger.debug("worker: queue for key=%s disappeared", key)
                            continue
                        batch: List[_GPTWorkItem] = []
                        while q and len(batch) < self.max_batch_size:
                            batch.append(q.popleft())
                        remaining = len(q)

                    if not batch:
                        logger.debug("worker: empty batch for key=%s", key)
                        continue

                    learning_lang, native_lang = key
                    flat_segments = [item.segment for item in batch]
                    logger.info(
                        "worker: processing key=%s batch_size=%d queue_remaining=%d",
                        key,
                        len(flat_segments),
                        remaining,
                    )
                    try:
                        translations = self.gpt_base.translate_text_segments(
                            native_lang=native_lang,
                            learning_lang=learning_lang,
                            example_sentences=flat_segments,
                            max_batch_size=self.max_batch_size,
                        )
                        for translation, seg in zip(translations, flat_segments):
                            seg.translation = translation
                    except Exception:
                        fatal_from_thread(f"GPTQueue worker for key={key}")

                    with self.lock:
                        q = self.queues.get(key)
                        if not q:
                            self.queue_first_enqueue_time.pop(key, None)
                            self.queue_last_enqueue_time.pop(key, None)

                if self._stop_event.wait(0.05):
                    break

            logger.info("GPTQueue worker thread exiting (stop_event=%s)", self._stop_event.is_set())
        except Exception:
            fatal_from_thread("GPTQueue worker outer loop")
