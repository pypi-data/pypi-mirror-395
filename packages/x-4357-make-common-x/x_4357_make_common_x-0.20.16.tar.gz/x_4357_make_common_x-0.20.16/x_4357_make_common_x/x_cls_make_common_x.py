from __future__ import annotations

import json
import logging
import sys
from contextlib import suppress
from dataclasses import dataclass
from pathlib import Path
from typing import Final

from .run_reports import REPORTS_DIR_NAME

_LOGGER = logging.getLogger("x_make")
_UTILITIES: Final[tuple[str, ...]] = (
    "run_reports",
    "json_board",
    "x_env_x",
    "x_http_client_x",
    "x_logging_utils_x",
    "x_subprocess_utils_x",
)


def _emit_stdout(message: str) -> bool:
    try:
        print(message)
    except (OSError, RuntimeError):
        return False
    return True


def _emit_stderr(message: str) -> bool:
    try:
        print(message, file=sys.stderr)
    except (OSError, RuntimeError):
        return False
    return True


def _info(*parts: object) -> None:
    msg = " ".join(str(part) for part in parts)
    with suppress(Exception):
        _LOGGER.info("%s", msg)
    if not _emit_stdout(msg):
        with suppress(Exception):
            sys.stdout.write(msg + "\n")


def _error(*parts: object) -> None:
    msg = " ".join(str(part) for part in parts)
    with suppress(Exception):
        _LOGGER.error("%s", msg)
    if not _emit_stderr(msg):
        with suppress(Exception):
            sys.stderr.write(msg + "\n")


@dataclass(slots=True)
class CommonDiagnostics:
    utilities: tuple[str, ...]
    ctx_present: bool
    reports_dir: str
    reports_dir_exists: bool

    def to_payload(self) -> dict[str, object]:
        return {
            "utilities": list(self.utilities),
            "ctx_present": self.ctx_present,
            "reports_dir": self.reports_dir,
            "reports_dir_exists": self.reports_dir_exists,
        }


class XClsMakeCommonX:
    """Lightweight diagnostics provider for the shared helpers package."""

    def __init__(self, ctx: object | None = None) -> None:
        self._ctx = ctx

    def diagnostics(self) -> CommonDiagnostics:
        reports_dir_path = Path.cwd() / REPORTS_DIR_NAME
        return CommonDiagnostics(
            utilities=_UTILITIES,
            ctx_present=self._ctx is not None,
            reports_dir=str(reports_dir_path),
            reports_dir_exists=reports_dir_path.is_dir(),
        )

    def run(self) -> CommonDiagnostics:
        diagnostics = self.diagnostics()
        _info(
            "x_make_common_x ready",
            f"utilities={', '.join(diagnostics.utilities)}",
            f"ctx={'present' if diagnostics.ctx_present else 'absent'}",
            f"reports_dir={diagnostics.reports_dir}",
            f"reports_dir_exists={diagnostics.reports_dir_exists}",
        )
        return diagnostics


def main() -> CommonDiagnostics:
    return XClsMakeCommonX().run()


if __name__ == "__main__":
    try:
        diagnostics = main()
        payload = json.dumps(diagnostics.to_payload(), indent=2)
        _info(payload)
    except Exception as exc:
        _error("x_make_common_x diagnostics failed:", exc)
        raise SystemExit(1) from exc


x_cls_make_common_x = XClsMakeCommonX
