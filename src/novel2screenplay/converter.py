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
) -> ConversionResult:
    """Convert raw novel text into screenplay data and YAML text.

    Pipeline:
    1. Split raw novel text into chapters.
    2. Check that the input has at least 3 chapters.
    3. Generate screenplay data.
    4. Validate screenplay data against the YAML Schema.
    5. Export validated data to YAML.
    """
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
        raise NotImplementedError("AI 模式将在下一阶段接入 OpenAI。")
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