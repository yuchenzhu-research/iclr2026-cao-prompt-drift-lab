from __future__ import annotations

import os
import tempfile
from pathlib import Path


def configure_headless_matplotlib_env() -> None:
    """
    Route matplotlib/fontconfig cache writes to a writable temp location.

    This keeps figure scripts fast and reliable in locked-down environments where
    HOME-backed cache directories are not writable.
    """

    base = Path(
        os.environ.get("REPRO_FIG_CACHE_DIR")
        or Path(tempfile.gettempdir()) / "repro_figure_cache"
    )
    mpl_dir = base / "matplotlib"
    fontconfig_dir = base / "fontconfig"
    xdg_cache_home = base / "xdg-cache"

    for path in (mpl_dir, fontconfig_dir, xdg_cache_home):
        path.mkdir(parents=True, exist_ok=True)

    os.environ.setdefault("MPLCONFIGDIR", str(mpl_dir))
    os.environ.setdefault("XDG_CACHE_HOME", str(xdg_cache_home))
    os.environ.setdefault("FONTCONFIG_PATH", "/opt/homebrew/etc/fonts")
    os.environ.setdefault("FC_CACHEDIR", str(fontconfig_dir))
