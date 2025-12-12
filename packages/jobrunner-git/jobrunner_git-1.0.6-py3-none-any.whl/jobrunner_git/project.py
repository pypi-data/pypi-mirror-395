from __future__ import annotations

import logging
from subprocess import DEVNULL, CalledProcessError, check_output

logger = logging.getLogger(__name__)


def run(*args: str) -> str | None:
    try:
        return check_output(args, encoding="utf-8", stderr=DEVNULL).strip()
    except CalledProcessError as err:
        logger.warning("error: %s", err)
        return None


def workspaceProject() -> tuple[str, bool]:
    head = run("git", "rev-parse", "HEAD")
    if not head:
        raise NotImplementedError

    top = run("git", "rev-parse", "--show-toplevel")
    status = run("git", "status", "-s", "--porcelain")
    dirty = "*" if status else ""
    return f"{top}:{head}{dirty}" if top else head, True
