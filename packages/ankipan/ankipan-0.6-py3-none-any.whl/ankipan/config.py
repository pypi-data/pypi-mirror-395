# ankipan/config.py
from __future__ import annotations
import os
import logging
from pathlib import Path
from typing import Optional, Dict, Any

import yaml  # pip install pyyaml

from ankipan import PROJECT_ROOT

logger = logging.getLogger(__name__)

class Config:
    @classmethod
    def servers_path(cls) -> Path: return PROJECT_ROOT / "servers.yaml"
    @classmethod
    def api_key_path(cls) -> Path: return PROJECT_ROOT / ".gemini_api_key"
    @classmethod
    def ollama_model_name_path(cls) -> Path: return PROJECT_ROOT / ".ollama_model_name"

    @staticmethod
    def _ensure_dir(p: Path) -> None: p.mkdir(parents=True, exist_ok=True)

    @staticmethod
    def _atomic_write_text(path: Path, data: str, *, mode: int = 0o600) -> None:
        Config._ensure_dir(path.parent)
        tmp = path.with_suffix(path.suffix + ".tmp")
        tmp.write_text(data, encoding="utf-8")
        os.replace(tmp, path)
        try: os.chmod(path, mode)
        except PermissionError: pass

    @staticmethod
    def _read_yaml_dict(path: Path) -> Dict[str, Any]:
        if not path.exists(): return {}
        try:
            obj = yaml.safe_load(path.read_text(encoding="utf-8"))
            return obj if isinstance(obj, dict) else {}
        except yaml.YAMLError as e:
            logger.warning("Invalid YAML at %s: %s (using empty config)", path, e)
            return {}

    @staticmethod
    def _write_yaml(path: Path, obj: Dict[str, Any]) -> None:
        data = yaml.safe_dump(obj, sort_keys=True, allow_unicode=True, indent=2)
        Config._atomic_write_text(path, data)

    @classmethod
    def load_servers(cls) -> Dict[str, Any]:
        """Return the whole servers registry dict, or {} if file missing/empty."""
        return cls._read_yaml_dict(cls.servers_path())

    @classmethod
    def save_servers(cls, registry: Dict[str, Any]) -> None:
        cls._write_yaml(cls.servers_path(), registry)

    @classmethod
    def add_server(cls, name: str, base_url: str) -> None:
        name = (name or "").strip()
        base_url = (base_url or "").strip()
        if not name: raise ValueError("Server name cannot be empty.")
        if not base_url: raise ValueError("base_url cannot be empty.")
        reg = cls.load_servers()
        reg[name] = base_url
        cls.save_servers(reg)

    @classmethod
    def remove_server(cls, name: str) -> None:
        reg = cls.load_servers()
        del reg[name]
        cls.save_servers(reg)

    @classmethod
    def get_server_ip(cls, name) -> str:
        reg = cls.load_servers()
        try:
            return reg[name]  # type: ignore[index]
        except Exception:
            available = ", ".join(sorted(reg.keys())) or "(none)"
            raise KeyError(f"Unknown server '{name}'. Available: {available}")

    @classmethod
    def set_gemini_api_key(cls, value: str) -> None:
        value = (value or "").strip()
        if not value: raise ValueError("API key cannot be empty.")
        if value[:2] != 'AI' or len(value) != 39:
            raise ValueError('Invalid Gemini API key format, please make sure you get it from the correct source (https://ai.google.dev/gemini-api/docs/api-key)')
        cls._atomic_write_text(cls.api_key_path(), value + "\n")

    @classmethod
    def get_gemini_api_key(cls) -> Optional[str]:
        env_value = os.getenv("GEMINI_API_KEY")
        if env_value: return env_value.strip()
        p = cls.api_key_path()
        return p.read_text(encoding="utf-8").strip() if p.exists() else None

    @classmethod
    def clear_gemini_api_key(cls) -> None:
        try: cls.api_key_path().unlink()
        except FileNotFoundError: pass

    @classmethod
    def set_ollama_model_name(cls, value: str) -> None:
        value = (value or "").strip()
        if not value: raise ValueError("API key cannot be empty.")
        cls._atomic_write_text(cls.ollama_model_name_path(), value + "\n")

    @classmethod
    def get_ollama_model_name(cls) -> Optional[str]:
        p = cls.ollama_model_name_path()
        return p.read_text(encoding="utf-8").strip() if p.exists() else None

    @classmethod
    def clear_ollama_model_name(cls) -> None:
        try: cls.ollama_model_name_path().unlink()
        except FileNotFoundError: pass
