from __future__ import annotations

from dataclasses import dataclass
from typing import Any

from novel2screenplay.chapter_splitter import Chapter, require_min_chapters, split_chapters
from novel2screenplay.demo_converter import build_demo_screenplay
from novel2screenplay.schema import validate_screenplay
from novel2screenplay.yaml_exporter import to_yaml


@dataclass(frozen=True)
class ConversionResult:
    """Result returned by the conversion pipeline."""

    title: str
    mode: str
    chapters: list[Chapter]
    data: dict[str, Any]
    yaml_text: str


def convert_novel_text(
    text: str,
    title: str = "未命名改编项目",
    mode: str = "demo",
    model: str | None = None,
    base_url: str | None = None,
    max_chars_per_chapter: int = 3500,
) -> ConversionResult:
    """Convert raw novel text into screenplay data and YAML text."""
    clean_title = title.strip() or "未命名改编项目"
    normalized_mode = mode.strip().lower()

    chapters = split_chapters(text)
    require_min_chapters(chapters, minimum=3)

    if normalized_mode == "demo":
        screenplay_data = build_demo_screenplay(
            chapters=chapters,
            title=clean_title,
        )
    elif normalized_mode == "ai":
        from novel2screenplay.llm_openai import convert_with_openai

        screenplay_data = convert_with_openai(
            chapters=chapters,
            title=clean_title,
            model=model,
            base_url=base_url,
            max_chars_per_chapter=max_chars_per_chapter,
        )
    else:
        raise ValueError("mode 只能是 'demo' 或 'ai'。")

    validate_screenplay(screenplay_data)
    yaml_text = to_yaml(screenplay_data)

    return ConversionResult(
        title=clean_title,
        mode=normalized_mode,
        chapters=chapters,
        data=screenplay_data,
        yaml_text=yaml_text,
    )