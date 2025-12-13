"""Cache management for Duplifinder."""

import hashlib
import json
import time
import logging
from pathlib import Path
from typing import Any, Dict, Optional, Tuple

from .config import Config

class CacheManager:
    """Manages file caching to speed up scans."""

    def __init__(self, cache_path: Path, config: Optional[Config] = None):
        self.cache_path = cache_path
        self.config = config
        self.data: Dict[str, Any] = {}
        self.config_hash = self._compute_config_hash(config) if config else None
        self.load()

    def load(self):
        """Load cache from disk."""
        if self.cache_path.exists():
            try:
                with open(self.cache_path, "r", encoding="utf-8") as f:
                    loaded_data = json.load(f)

                    # Check config hash
                    if self.config_hash and loaded_data.get("_config_hash") != self.config_hash:
                        logging.info("Configuration changed; invalidating cache.")
                        self.data = {}
                    else:
                        self.data = loaded_data
            except Exception as e:
                logging.warning(f"Failed to load cache: {e}. Starting fresh.")
                self.data = {}

        # Set current config hash in data
        if self.config_hash:
            self.data["_config_hash"] = self.config_hash

    def save(self):
        """Save cache to disk."""
        try:
            with open(self.cache_path, "w", encoding="utf-8") as f:
                json.dump(self.data, f)
        except Exception as e:
            logging.warning(f"Failed to save cache: {e}")

    def get(self, file_path: str, file_hash: str) -> Optional[Any]:
        """Retrieve cached result if hash matches."""
        entry = self.data.get(str(file_path))
        if entry and entry.get("hash") == file_hash:
            return entry.get("data")
        return None

    def set(self, file_path: str, file_hash: str, data: Any):
        """Update cache entry."""
        self.data[str(file_path)] = {
            "hash": file_hash,
            "timestamp": time.time(),
            "data": data
        }

    @staticmethod
    def compute_hash(file_path: Path) -> Optional[str]:
        """Compute MD5 hash of a file."""
        try:
            hasher = hashlib.md5()
            with open(file_path, "rb") as f:
                # Read in chunks to avoid memory issues
                for chunk in iter(lambda: f.read(4096), b""):
                    hasher.update(chunk)
            return hasher.hexdigest()
        except Exception:
            return None

    def _compute_config_hash(self, config: Config) -> str:
        """Compute a hash of relevant configuration options."""
        # Relevant fields that affect AST parsing / definition finding
        relevant = {
            "types_to_search": sorted(list(config.types_to_search)),
            "exclude_patterns": sorted(list(config.exclude_patterns)),
            "exclude_names": sorted(list(config.exclude_names)),
            # Add other fields if they affect parsing
        }
        return hashlib.md5(json.dumps(relevant, sort_keys=True).encode("utf-8")).hexdigest()
