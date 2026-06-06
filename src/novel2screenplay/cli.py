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
        help="转换模式。当前阶段请使用 demo，AI 模式将在下一阶段接入。",
    )

    parser.add_argument(
        "--output",
        default="screenplay.yaml",
        help="输出 YAML 文件路径。",
    )

    return parser


def main(argv: list[str] | None = None) -> int:
    """Run the command line converter.

    Return 0 on success and 1 on failure.
    """
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