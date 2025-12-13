"""CLI wrapper that dispatches to the bundled caj2pdf.exe."""

from __future__ import annotations

import subprocess
import sys
from pathlib import Path


def _find_executable() -> Path:
    """Locate the bundled caj2pdf.exe inside the installed package."""
    return Path(__file__).resolve().parent / "bin" / "caj2pdf.exe"


def main() -> int:
    exe_path = _find_executable()
    if not exe_path.exists():
        sys.stderr.write("caj2pdf.exe not found in installed package.\n")
        return 1

    cmd = [str(exe_path)] + sys.argv[1:]
    try:
        result = subprocess.run(cmd, check=False)
    except OSError as exc:
        sys.stderr.write(f"Failed to launch caj2pdf.exe: {exc}\n")
        return 1

    return int(result.returncode)


if __name__ == "__main__":
    raise SystemExit(main())
