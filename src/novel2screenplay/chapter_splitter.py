from __future__ import annotations

from dataclasses import dataclass
import re


@dataclass(frozen=True)
class Chapter:
    """A detected novel chapter."""

    number: int
    title: str
    content: str


CHAPTER_PATTERN = re.compile(
    r"(?m)^\s*(第\s*[0-9一二三四五六七八九十百千]+\s*[章节回卷集].*|Chapter\s+\d+.*)\s*$",
    re.IGNORECASE,
)


def split_chapters(text: str) -> list[Chapter]:
    """Split novel text into chapters.

    Supports common Chinese headings such as 第1章, 第一章, 第三回,
    and English headings such as Chapter 1.
    """
    normalized = text.replace("\r\n", "\n").replace("\r", "\n").strip()
    if not normalized:
        return []

    matches = list(CHAPTER_PATTERN.finditer(normalized))
    if not matches:
        return [Chapter(number=1, title="未分章文本", content=normalized)]

    chapters: list[Chapter] = []
    for index, match in enumerate(matches):
        start = match.end()
        end = matches[index + 1].start() if index + 1 < len(matches) else len(normalized)
        title = match.group(1).strip()
        content = normalized[start:end].strip()
        chapters.append(Chapter(number=index + 1, title=title, content=content))

    return chapters


def require_min_chapters(chapters: list[Chapter], minimum: int = 3) -> None:
    """Raise a friendly error if the input has too few chapters."""
    if len(chapters) < minimum:
        raise ValueError(f"需要至少 {minimum} 个章节，目前只识别到 {len(chapters)} 个。")