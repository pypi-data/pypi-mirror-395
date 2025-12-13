import logging
import time
import traceback
import uuid
from concurrent.futures import ThreadPoolExecutor
from dataclasses import asdict
from threading import Lock

import pytest

from ankipan import TextSegment
from ankipan.gpt_base import GPTBase, GPTQueue


class MockGPTBase:
    def __init__(self):
        self.calls = []  # list of dicts: {"pair": (learning,native), "size": int}

    def translate_text_segments(self, *, native_lang, learning_lang, example_sentences, max_batch_size):
        self.calls.append({
            "pair": (learning_lang, native_lang),
            "size": len(example_sentences),
        })
        return [f"trans:{seg.word}" for seg in example_sentences]


def _make_seg(word: str) -> TextSegment:
    return TextSegment(main_index=0, text_segments=[word], word=word)


def _wait_for(predicate, timeout=2.0, interval=0.01):
    start = time.time()
    while time.time() - start < timeout:
        if predicate():
            return True
        time.sleep(interval)
    return False


def test_batches_exceeding_max_size_are_split_and_processed():
    gpt_base = MockGPTBase()
    q = GPTQueue(max_batch_size=3, batch_wait_seconds=0.05)
    q.gpt_base = gpt_base
    q.start_thread()
    try:
        segs = [_make_seg(f"w{i}") for i in range(7)]
        for s in segs:
            q.enqueue("jp", "en", s)

        assert _wait_for(lambda: all(s.translation for s in segs)), "Timeout waiting for translations"

        # All translations should be set and match the gpt_base outputs
        assert [s.translation for s in segs] == [f"trans:w{i}" for i in range(7)]

        # The queue must never process more than max_batch_size at once
        sizes = [c["size"] for c in gpt_base.calls]
        assert sum(sizes) == 7
        assert max(sizes) <= 3
        assert any(sz == 3 for sz in sizes)
    finally:
        q.stop_thread(wait=True)


def test_under_batch_size_waits_then_processes():
    gpt_base = MockGPTBase()
    q = GPTQueue(max_batch_size=10, batch_wait_seconds=0.05)
    q.gpt_base = gpt_base
    q.start_thread()
    try:
        segs = [_make_seg("a"), _make_seg("b")]
        for s in segs:
            q.enqueue("jp", "en", s)

        assert _wait_for(lambda: all(s.translation for s in segs)), "Timeout waiting for translations"

        # Only one call should have been made with both items (since below batch size, processed by time)
        sizes = [c["size"] for c in gpt_base.calls]
        assert sizes == [2]
        assert [s.translation for s in segs] == ["trans:a", "trans:b"]
    finally:
        q.stop_thread(wait=True)


def test_register_task_status_and_pop():
    gpt_base = MockGPTBase()
    q = GPTQueue(max_batch_size=3, batch_wait_seconds=0.05)
    q.gpt_base = gpt_base
    q.start_thread()
    try:
        segs = [_make_seg("x"), _make_seg("y"), _make_seg("z")]
        segs[1].translation = "pretranslated"  # Already done; should not be enqueued

        task_id = q.register_task("jp", "en", segs)

        # Should complete once remaining segments are translated
        assert _wait_for(lambda: q.get_task_status(task_id) == "done"), "Task did not complete in time"

        status = q.get_task_status(task_id)
        assert status == "done"
        assert [seg.translation for seg in segs] == ["trans:x", "pretranslated", "trans:z"]

        # Only two segments should have been sent to the translator
        assert sum(c["size"] for c in gpt_base.calls) == 2

        # Pop the task and ensure it is no longer tracked
        q.pop_task(task_id)
        status_after = q.get_task_status(task_id)
        assert status_after == "missing"
    finally:
        q.stop_thread(wait=True)


def test_multiple_language_pairs_are_queued_independently():
    gpt_base = MockGPTBase()
    q = GPTQueue(max_batch_size=2, batch_wait_seconds=0.05)
    q.gpt_base = gpt_base
    q.start_thread()
    try:
        jp_en = [_make_seg("j1"), _make_seg("j2")]
        fr_en = [_make_seg("f1"), _make_seg("f2")]

        for s in jp_en:
            q.enqueue("jp", "en", s)
        for s in fr_en:
            q.enqueue("fr", "en", s)

        assert _wait_for(lambda: all(s.translation for s in jp_en + fr_en)), "Timeout waiting for translations"

        # Verify translations align with the gpt_base outputs
        assert [s.translation for s in jp_en] == ["trans:j1", "trans:j2"]
        assert [s.translation for s in fr_en] == ["trans:f1", "trans:f2"]

        # Ensure we saw calls for both language pairs
        pairs = {(c["pair"], c["size"]) for c in gpt_base.calls}
        assert (("jp", "en"), 2) in pairs
        assert (("fr", "en"), 2) in pairs
    finally:
        q.stop_thread(wait=True)


def test_server_style_task_flow_with_cache_and_registry():
    gpt_base = MockGPTBase()
    q = GPTQueue(max_batch_size=2, batch_wait_seconds=0.01)
    q.gpt_base = gpt_base
    q.start_thread()
    executor = ThreadPoolExecutor(max_workers=2)
    try:
        class gpt_baseDB:
            def __init__(self):
                self.cached_hits = {1: "cached"}
                self.cache_calls = []

            def get_translations_from_cache(self, segments, native_lang):
                return dict((idx, tr) for idx, tr in self.cached_hits.items() if idx < len(segments))

            def cache_translations(self, segments, native_lang):
                self.cache_calls.append([(seg.word, seg.translation) for seg in segments])

        db_mapping = {"jp": gpt_baseDB()}

        def enqueue_and_wait_for_translation_tasks(learning_lang, native_lang, text_segments):
            cached = db_mapping[learning_lang].get_translations_from_cache(text_segments, native_lang)
            for idx, tr in cached.items():
                text_segments[idx].translation = tr
            tr_task_id = q.register_task(learning_lang, native_lang, text_segments)

            while True:
                status = q.get_task_status(tr_task_id)
                if status == "done":
                    q.pop_task(tr_task_id)
                    to_cache = [ts for i, ts in enumerate(text_segments) if i not in cached]
                    db_mapping[learning_lang].cache_translations(to_cache, native_lang)
                    return [asdict(seg) for seg in text_segments]
                time.sleep(0.01)

        task_registry = {}
        task_lock = Lock()
        logger = logging.getLogger("test.gpt_queue")

        def start_task(target, *args, **kwargs):
            task_id = str(uuid.uuid4())
            with task_lock:
                task_registry[task_id] = {"status": "queued", "result": None, "error": None}

            def runner():
                with task_lock:
                    task_registry[task_id]["status"] = "running"
                try:
                    result = target(*args, **kwargs)
                except Exception:  # pragma: no cover - exercised via assertions
                    tb = traceback.format_exc()
                    with task_lock:
                        task_registry[task_id]["status"] = "error"
                        task_registry[task_id]["error"] = tb
                    logger.exception("Background task %s failed", task_id)
                else:
                    with task_lock:
                        task_registry[task_id]["status"] = "done"
                        task_registry[task_id]["result"] = result

            executor.submit(runner)
            return task_id

        def task_collection(task_ids):
            resp = {}
            for task_id in task_ids:
                with task_lock:
                    entry = task_registry.get(task_id)
                if entry is None:
                    resp.setdefault("erroneous", {})[task_id] = "404: Task not found"
                    continue
                status = entry["status"]
                if status == "done":
                    with task_lock:
                        entry = task_registry.pop(task_id, entry)
                    resp.setdefault("success", {})[task_id] = entry["result"]
                elif status == "error":
                    with task_lock:
                        entry = task_registry.pop(task_id, entry)
                    resp.setdefault("erroneous", {})[task_id] = entry.get("error")
            return resp

        segs = [_make_seg("alpha"), _make_seg("beta"), _make_seg("gamma")]
        task_id = start_task(enqueue_and_wait_for_translation_tasks, "jp", "en", segs)

        # Pending tasks should not appear in the response
        assert task_collection([task_id]) == {}

        def task_done():
            with task_lock:
                entry = task_registry.get(task_id)
                return entry and entry["status"] == "done"

        assert _wait_for(task_done), "Timeout waiting for background task completion"

        resp = task_collection([task_id])
        assert set(resp.keys()) == {"success"}
        result = resp["success"][task_id]
        assert [item["translation"] for item in result] == ["trans:alpha", "cached", "trans:gamma"]

        # Cached hit should not be sent back to GPT and only uncached segments get cached now
        assert gpt_base.calls == [{"pair": ("jp", "en"), "size": 2}]
        assert db_mapping["jp"].cache_calls == [[("alpha", "trans:alpha"), ("gamma", "trans:gamma")]]

        # Task is removed from registry once task_collection returns it
        with task_lock:
            assert task_id not in task_registry
    finally:
        executor.shutdown(wait=True)
        q.stop_thread(wait=True)

def test_translation_prompt_parsing():
    gpt_base = GPTBase()
    res = gpt_base._parse_translation_response("""
<think>
Alright, so I need to translate these Japanese text snippets into English. The main focus is on the parts wrapped in square brackets. Each translation should be followed by an optional comment if there's any nuance or something worth explaining for a language learner.

First, looking at each segment:

1. "シャンクスは左腕を犠牲にして助け出した。" – This translates directly to "Shanks sacrificed his left arm and saved him." No real nuances here; it's pretty straightforward.

2. "[「東の海（イーストブルー）」のフーシャ村に住む少年モンキーDルフィは、]" → "The boy Monkey D. Luffy living in the village of Fusha in the East Blue Sea." Maybe mention that "Fusha" is a proper noun and "East Blue" is a region in the One Piece universe.

3. "[彼が遺した「ひとつなぎの大秘宝（ワンピース）」をめぐり、]" → "About the one piece of treasure left by him, the Great Big Treasure." The term "one piece" is translated as "One Piece," which is a famous manga title, so it's better to explain that it's the name of a popular series.

4. The next ones repeat similar phrases about Gol D. Roger and the Pirate King title. Translating them straightforwardly without extra comments makes sense since they're consistent.

5. Phrases like "ゴム人間" are interesting because "gum man" might not make much sense, but in context, it's a rubber human, which is Luffy's ability. So explaining that "ゴム" means rubber and how it affects his body could be helpful for understanding his powers.

6. Some sentences mention being thrown into the sea or helping someone out, which are pretty direct without needing extra comments unless there’s a specific term to explain.

I should go through each snippet one by one, extract the bracketed part, translate it, and add a comment only if I think it's necessary for understanding nuances or cultural context. Keeping the comments brief but informative enough for someone learning English and Japanese.
</think>

- Shanks sacrificed his left arm and saved him.
- The boy Monkey D. Luffy lives in the village of Fusha in the East Blue Sea.
- About the one piece of treasure left by Gol D. Roger, known as "One Piece."
- He ate the "Gomu Gomu no Mi," a devil fruit that turns his body into rubber, making him stretch and shrink at will.
- Shanks helped save Luffy from drowning and being eaten by a huge fish.
- The boy Monkey D. Luffy lives in Fusha Village in the East Blue Sea.
- Luffy ate the "Gomu Gomu no Mi," becoming a rubber human with stretchable limbs.
- He was thrown into the sea after Shanks saved him from drowning and near being eaten by a giant fish.

""")
    assert len(res) == 8
