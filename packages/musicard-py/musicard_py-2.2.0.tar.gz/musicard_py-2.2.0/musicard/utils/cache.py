"""
Caching system for Musicard
"""

import hashlib
from pathlib import Path
from typing import Any, Dict, Optional, Union

try:
    import diskcache as dc
except ImportError:
    dc = None
from PIL import Image


class MusicardCache:
    """Caching system for images, fonts, and generated cards."""

    def __init__(
        self,
        cache_dir: Optional[Union[str, Path]] = None,
        size_limit: int = 500 * 1024 * 1024,
    ):  # 500MB
        """Initialize cache.

        Args:
            cache_dir: Cache directory path (default: ~/.musicard/cache)
            size_limit: Maximum cache size in bytes
        """
        if dc is None:
            # Fallback if diskcache is not available
            self.cache = None
            self.image_cache = None
            self.font_cache = None
            return

        if cache_dir is None:
            home = Path.home()
            cache_dir = home / ".musicard" / "cache"
        else:
            cache_dir = Path(cache_dir)

        cache_dir.mkdir(parents=True, exist_ok=True)

        self.cache = dc.Cache(str(cache_dir), size_limit=size_limit)
        self.image_cache = dc.Cache(
            str(cache_dir / "images"), size_limit=size_limit // 2
        )
        self.font_cache = dc.Cache(str(cache_dir / "fonts"), size_limit=size_limit // 4)

    def _get_image_key(self, url_or_path: str) -> str:
        """Generate cache key for image."""
        return hashlib.md5(url_or_path.encode(), usedforsecurity=False).hexdigest()  # nosec B324

    def get_image(self, url_or_path: str) -> Optional[Image.Image]:
        """Get cached image."""
        if self.image_cache is None:
            return None
        key = self._get_image_key(url_or_path)
        return self.image_cache.get(key)

    def set_image(self, url_or_path: str, image: Image.Image) -> None:
        """Cache image."""
        if self.image_cache is None:
            return
        key = self._get_image_key(url_or_path)
        self.image_cache.set(key, image)

    def get_font(self, font_path: str, size: int) -> Optional[Any]:
        """Get cached font."""
        if self.font_cache is None:
            return None
        key = f"{font_path}_{size}"
        return self.font_cache.get(key)

    def set_font(self, font_path: str, size: int, font: Any) -> None:
        """Cache font."""
        if self.font_cache is None:
            return
        key = f"{font_path}_{size}"
        self.font_cache.set(key, font)

    def get_card(self, params: Dict[str, Any]) -> Optional[Image.Image]:
        """Get cached generated card."""
        if self.cache is None:
            return None
        # Create a hash of the parameters
        param_str = str(sorted(params.items()))
        key = hashlib.md5(param_str.encode(), usedforsecurity=False).hexdigest()  # nosec B324
        return self.cache.get(key)

    def set_card(self, params: Dict[str, Any], image: Image.Image) -> None:
        """Cache generated card."""
        if self.cache is None:
            return
        param_str = str(sorted(params.items()))
        key = hashlib.md5(param_str.encode(), usedforsecurity=False).hexdigest()  # nosec B324
        self.cache.set(key, image)

    def clear(self) -> None:
        """Clear all caches."""
        if self.cache:
            self.cache.clear()
        if self.image_cache:
            self.image_cache.clear()
        if self.font_cache:
            self.font_cache.clear()

    def stats(self) -> Dict[str, Any]:
        """Get cache statistics."""
        if self.cache is None:
            return {"caching_disabled": True}

        return {
            "main_cache": {
                "size": len(self.cache) if self.cache else 0,
                "hits": self.cache.hits if self.cache else 0,
                "misses": self.cache.misses if self.cache else 0,
            },
            "image_cache": {
                "size": len(self.image_cache) if self.image_cache else 0,
                "hits": self.image_cache.hits if self.image_cache else 0,
                "misses": self.image_cache.misses if self.image_cache else 0,
            },
            "font_cache": {
                "size": len(self.font_cache) if self.font_cache else 0,
                "hits": self.font_cache.hits if self.font_cache else 0,
                "misses": self.font_cache.misses if self.font_cache else 0,
            },
        }


# Global cache instance
cache = MusicardCache()
