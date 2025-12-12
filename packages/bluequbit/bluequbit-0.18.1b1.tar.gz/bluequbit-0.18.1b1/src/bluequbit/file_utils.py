from __future__ import annotations

import logging
import shutil
from functools import partial
from pathlib import Path

logger = logging.getLogger(__name__)


def has_extension(src: str, ext: str) -> bool:
    actual_extension = Path(src).suffix
    return ext == actual_extension


def copy_if(src: str, dst: str, *, include_ext_patterns: tuple[str, ...]) -> None:
    if any(has_extension(src, ext) for ext in include_ext_patterns):
        logger.debug("Copying %s to %s", src, dst)
        shutil.copy2(src, dst)


def copy_files(
    *,
    src: str,
    dst: str,
    include_ext_patterns: tuple[str, ...],
    exclude_ext_patterns: tuple[str, ...] = (),
) -> None:
    if not isinstance(include_ext_patterns, tuple):
        raise TypeError(
            f"include_ext_patterns should be {tuple} not {type(include_ext_patterns)}"
        )
    shutil.copytree(
        str(src),
        str(dst),
        dirs_exist_ok=True,
        copy_function=partial(copy_if, include_ext_patterns=include_ext_patterns),
        ignore=shutil.ignore_patterns(
            "*venv*",
            "__pycache__",
            ".git",
            ".ipynb_checkpoints",
            ".DS_Store",
            ".*",
            *exclude_ext_patterns,
        ),
    )
    logger.info(
        "Copied %s (excluding %s) files from %s to %s",
        include_ext_patterns,
        exclude_ext_patterns,
        src,
        dst,
    )
