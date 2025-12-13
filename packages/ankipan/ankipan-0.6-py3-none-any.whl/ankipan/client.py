from __future__ import annotations
import logging
from dataclasses import asdict
import requests
from time import sleep
from concurrent.futures import ThreadPoolExecutor, as_completed
import requests

from typing import *

from ankipan import Config, TextSegment, SourcePath

logger = logging.getLogger(__name__)

DEFAULT_TIMEOUT: float = 60

class Client:
    @classmethod
    def _servers(cls) -> Dict[str, str]:
        servers = Config.load_servers()
        if not servers:
            raise RuntimeError("No servers configured. Use ankipan.Config.add_server(...).")
        return servers

    @classmethod
    def _pick_server(cls, server: str | None) -> Tuple[str, str]:
        servers = cls._servers()
        if server is None:
            if len(servers) != 1:
                raise RuntimeError('More than one server in servers.yaml config, please specify')
            server = next(iter(servers.keys()))
        if server not in servers:
            known = ", ".join(sorted(servers)) or "(none)"
            raise KeyError(f"Unknown server '{server}'. Known: {known}")
        return server, servers[server]

    @staticmethod
    def _post(base_url: str, path: str, payload: dict) -> requests.Response:
        url = f"{base_url.rstrip('/')}{path}"
        try:
            return requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT)
        except requests.exceptions.Timeout:
            return requests.post(url, json=payload, timeout=DEFAULT_TIMEOUT)

    @staticmethod
    def _split_server_and_path(full_path: str) -> tuple[str, Optional[str]]:
        s = (full_path or "").strip("/")
        if not s:
            raise ValueError("Malformed source path, expected '<server>/<category>/...'.")
        parts = s.split("/", 1)
        server = parts[0]
        remainder = parts[1] if len(parts) > 1 else None
        return server, remainder

    @classmethod
    def available_example_sentence_source_categories(
        cls,
        learning_lang: str,
        *,
        max_workers: int | None = None) -> Dict[str, List[str]]:
        servers = cls._servers()
        payload = {"lang": learning_lang}
        res: Dict[str, dict] = {}
        if not servers:
            return res

        def fetch(server: str, address: str) -> Dict[str, List[str]]:
            try:
                resp = cls._post(address, "/available_source_categories", payload)
            except Exception as e:
                logger.warning("Address '%s' unavailable for sources: %s", address, e)
                return {}

            if getattr(resp, "status_code", None) != 200:
                logger.warning("Address '%s' to fetch sources not available: Code %s, %s",
                    address, getattr(resp, "status_code", "?"), resp.text)
                return {}
            try:
                return {server: resp.json()}
            except Exception as e:
                logger.warning("Address '%s' returned invalid JSON for sources: %s", address, e)
                return {}

        workers = max_workers or min(32, max(1, len(servers)))
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(fetch, s, a) for s, a in servers.items()]
            for fut in as_completed(futs):
                res.update(fut.result())
        return res

    @classmethod
    def source_list(
        cls,
        learning_lang: str,
        source_path: SourcePath
    ) -> Tuple[Dict[str, Any], Dict[str, int], List[str]]:
        """
        Parameters
        ----------
        learning_lang : Name of language the user wants to learn.
        source_path : Native language of the user for translations and explanations.

        Returns
        -------
        metadata: Dict[str, Any]
            metadata of source node
        lemma_counts: Dict[str, int]
            (aggregated) lemma counts of source node
            picking most frequent 10.000 if there are more than that
        children: List[str]
            List of child names

        """
        servers = cls._servers()
        server = source_path[0]

        if server not in servers:
            known = ', '.join(sorted(servers)) or '(none)'
            raise KeyError(f'Unknown server "{server}". Known: {known}')

        payload = {'lang': learning_lang, 'source_path': '/'.join(source_path[1:])}
        resp = cls._post(servers[server], '/source_list', payload)

        if resp.status_code == 404:
            raise RuntimeError(f'Path not found on {server}: {source_path}')
        resp.raise_for_status()

        data = resp.json()
        metadata, lemma_counts, children = data
        return metadata, lemma_counts, children

    @classmethod
    def get_invalid_source_paths(
        cls,
        learning_lang: str,
        source_paths: List[SourcePath]
    ) -> Tuple[Dict[str, Any], Dict[str, int], List[str]]:
        """
        Get list of invalid source paths
        """
        relative_source_paths_by_server = {}
        for source_path in source_paths:
            relative_source_paths_by_server.setdefault(source_path[0], []).append('/'.join(source_path[1:]))

        def fetch(server, relative_source_paths):
            payload = {'lang': learning_lang, 'source_paths': relative_source_paths}
            resp = cls._post(cls._servers()[server], '/get_invalid_source_paths', payload)
            if resp.status_code != 200:
                raise RuntimeError(f'get_invalid_source_paths failing with {resp.status_code}')
            return resp.json()

        workers = min(32, max(1, len(relative_source_paths_by_server)))
        invalid_paths = []
        with ThreadPoolExecutor(max_workers=workers) as ex:
            futs = [ex.submit(fetch, server, relative_source_paths)
                    for server, relative_source_paths in relative_source_paths_by_server.items()]
            for fut in as_completed(futs):
                invalid_paths.extend(fut.result())
        return invalid_paths
    # TODO parallelize server accesses
    @classmethod
    def get_lemma_percentiles(
        cls,
        learning_lang: str,
        source_paths: List[SourcePath],
        lemmas: List[str]
        ) -> Dict[str, float]:
        servers = cls._servers()

        percentiles_by_source = {}
        for source_path in source_paths:
            server = source_path[1]
            if server not in servers:
                known = ", ".join(sorted(servers)) or "(none)"
                raise KeyError(f"Unknown server '{server}' in path '{source_path}'. Known: {known}")
            payload = {
                    "learning_lang": learning_lang,
                    "lemmas": lemmas,
                    "source_path": "/".join(source_path[2:])}
            resp = cls._post(servers[server], "/get_lemma_percentiles", payload)
            if resp.status_code != 200:
                logger.warning(f'Could not fetch lemma count for {source_path}')
            else:
                percentiles_by_source[str(source_path)] = resp.json()
        return percentiles_by_source

    # TODO disable until we figure out how to filter out nonsense
    # @classmethod
    # def cache_translations(
    #     cls,
    #     server: str,
    #     learning_lang: str,
    #     native_lang: Optional[str],
    #     translations_by_text_segments: list):
    #     _, base = cls._pick_server(server)
    #     resp = cls._post(
    #         base,
    #         "/cache_translations",
    #         {
    #             "learning_lang": learning_lang,
    #             "native_lang": native_lang,
    #             "translations_by_text_segments": translations_by_text_segments,
    #         },
    #     )
    #     if resp.status_code != 200:
    #         logger.debug(f'Translation caching failed with status code {resp.status_code}: {resp.text}')

    @classmethod
    def collect_tasks(
        cls,
        server: str,
        task_ids: str
    ) -> Dict[str, dict]:
        """POST /task_collection. Returns dict of finished tasks."""
        _, base = cls._pick_server(server)
        resp = cls._post(base, "/task_collection", {"task_ids": task_ids})
        resp.raise_for_status()
        return resp.json()

    @classmethod
    def trigger_sentences(
        cls,
        server: str,
        learning_lang: str,
        native_lang: str,
        source_category: str,
        lemma: str,
        relative_source_paths: Dict[str, List[str]],
        use_server_gpt = True,
        # translation_weight: int = 1000,
    ) -> str:
        """POST /trigger_sentences. Returns a single task_id."""
        _, base = cls._pick_server(server)
        resp = cls._post(
            base,
            "/trigger_sentences",
            {
                "source_category": source_category,
                "lemma": lemma,
                "relative_source_paths": relative_source_paths,
                "learning_lang": learning_lang,
                "native_lang": native_lang,
                "use_server_gpt": use_server_gpt,
                # 'translation_weight': translation_weight,
            },
        )
        resp.raise_for_status()
        return resp.json()["task_id"]


    @classmethod
    def trigger_translations(
        cls,
        server: str,
        learning_lang: str,
        native_lang: str,
        text_segments: List["TextSegment"]) -> str:
        """POST /trigger_translations. Returns task_id."""
        _name, ip = cls._pick_server(server)
        resp = cls._post(
            ip,
            "/trigger_translations",
            {
                "learning_lang": learning_lang,
                "native_lang": native_lang,
                "text_segments": [asdict(text_segment) for text_segment in text_segments if not text_segment.translation],
            },
        )
        resp.raise_for_status()
        return resp.json()["task_id"]

    @classmethod
    def trigger_frequent_contexts(
        cls,
        server: str,
        lemma: str,
        lang,
    ) -> str:
        """POST /frequent_contexts. Returns task_id."""
        _, base = cls._pick_server(server)
        resp = cls._post(base, "/frequent_contexts", {
            "lemma": lemma,
            "learning_lang": lang,
        })
        resp.raise_for_status()
        return resp.json()["task_id"]

    @classmethod
    def trigger_synonym_explanations(
        cls,
        server: str,
        synonyms_by_words: Dict[str, List[str]],
        learning_lang: str,
    ) -> str:
        """POST /synonym_explanations. Returns task_id."""
        _, base = cls._pick_server(server)
        resp = cls._post(base, "/synonym_explanations", {
            "synonyms_by_words": synonyms_by_words,
            "learning_lang": learning_lang,
        })
        resp.raise_for_status()
        return resp.json()["task_id"]

    @classmethod
    def collect_synonym_explanations(
        cls,
        server: str,
        task_id: str,
    ) -> Dict[str, List[List]] | Dict[str, List[tuple]]:
        """GET /synonym_explanations/status/<task_id> with polling.
        Returns a dict: {word: explanation}"""
        _, base = cls._pick_server(server)
        return cls._poll_status_until_terminal(
            base, f"/synonym_explanations/status/{task_id}"
        )
