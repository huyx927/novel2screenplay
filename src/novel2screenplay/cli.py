from __future__ import annotations

import argparse
from pathlib import Path

from novel2screenplay.converter import convert_novel_text


def build_parser() -> argparse.ArgumentParser:
    """Build the command line argument parser."""
    parser = argparse.ArgumentParser(
        description="Convert 3 or more novel chapters into screenplay YAML."
    )

    parser.add_argument(
        "input",
        help="输入小说 TXT 文件路径，文件需要使用 UTF-8 编码。",
    )

    parser.add_argument(
        "--title",
        default="未命名改编项目",
        help="剧本项目标题。",
    )

    parser.add_argument(
        "--mode",
        choices=["demo", "ai"],
        default="demo",
        help="转换模式。demo 不调用 API，ai 会调用第三方 OpenAI-compatible API。",
    )

    parser.add_argument(
        "--model",
        default=None,
        help="第三方模型名。不填则读取 .env 中的 OPENAI_MODEL。",
    )

    parser.add_argument(
        "--base-url",
        default=None,
        help="第三方 API Base URL。不填则读取 .env 中的 OPENAI_BASE_URL。",
    )

    parser.add_argument(
        "--max-chars-per-chapter",
        type=int,
        default=3500,
        help="AI 模式下每章最多发送的字符数，用于控制输入长度。",
    )

    parser.add_argument(
        "--output",
        default="screenplay.yaml",
        help="输出 YAML 文件路径。",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command line converter."""
    parser = build_parser()
    args = parser.parse_args(argv)

    try:
        input_path = Path(args.input)
        output_path = Path(args.output)

        text = input_path.read_text(encoding="utf-8")

        result = convert_novel_text(
            text=text,
            title=args.title,
            mode=args.mode,
            model=args.model,
            base_url=args.base_url,
            max_chars_per_chapter=args.max_chars_per_chapter,
        )

        output_path.parent.mkdir(parents=True, exist_ok=True)
        output_path.write_text(result.yaml_text, encoding="utf-8")

        print(f"转换成功：{output_path}")
        print(f"项目标题：{result.title}")
        print(f"识别章节数：{len(result.chapters)}")
        print(f"转换模式：{result.mode}")
        return 0

    except Exception as exc:
        print(f"转换失败：{exc}")
        return 1


if __name__ == "__main__":
    raise SystemExit(main())