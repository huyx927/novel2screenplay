from __future__ import annotations

from copy import deepcopy
import json
import os
import re
from typing import Any

from dotenv import load_dotenv
from openai import OpenAI, OpenAIError

from novel2screenplay.chapter_splitter import Chapter
from novel2screenplay.prompts import SYSTEM_PROMPT, build_user_prompt
from novel2screenplay.schema import SCREENPLAY_SCHEMA, validate_screenplay


def _format_chapters_for_prompt(
    chapters: list[Chapter],
    max_chars_per_chapter: int,
) -> str:
    """Format chapters for the model prompt and optionally truncate long chapters."""
    parts: list[str] = []

    for chapter in chapters:
        content = chapter.content.strip()

        if max_chars_per_chapter > 0:
            content = content[:max_chars_per_chapter]

        parts.append(
            f"## 第 {chapter.number} 章：{chapter.title}\n"
            f"{content}"
        )

    return "\n\n".join(parts)


def _schema_for_prompt() -> str:
    """Return a compact JSON Schema string for the prompt."""
    schema = deepcopy(SCREENPLAY_SCHEMA)
    schema.pop("$schema", None)
    schema.pop("title", None)

    return json.dumps(schema, ensure_ascii=False, indent=2)


def _get_required_env(
    name: str,
    placeholder_values: set[str] | None = None,
) -> str:
    """Read and validate a required environment variable."""
    placeholder_values = placeholder_values or set()
    value = os.getenv(name, "").strip()

    if not value or value in placeholder_values:
        raise RuntimeError(f"缺少有效配置：{name}。请检查你的 .env 文件。")

    return value


def _build_client(base_url: str, api_key: str) -> OpenAI:
    """Build an OpenAI-compatible client for third-party APIs."""
    return OpenAI(
        api_key=api_key,
        base_url=base_url,
        default_headers={"User-Agent": "python-httpx/0.28.1"},
    )


def _is_response_format_unsupported(exc: Exception) -> bool:
    """Check whether the provider rejected response_format."""
    message = str(exc).lower()

    keywords = [
        "response_format",
        "json_object",
        "unsupported",
        "not support",
        "not supported",
        "extra inputs",
        "extra fields",
        "invalid parameter",
        "unknown parameter",
    ]

    return any(keyword in message for keyword in keywords)


def _remove_thinking_blocks(text: str) -> str:
    """Remove reasoning blocks that some third-party models may return."""
    return re.sub(r"<think>.*?</think>", "", text, flags=re.DOTALL | re.IGNORECASE).strip()


def _strip_markdown_fences(text: str) -> str:
    """Remove common markdown fences from model output."""
    cleaned = text.strip()

    if cleaned.startswith("```"):
        cleaned = re.sub(r"^```(?:json)?", "", cleaned.strip(), flags=re.IGNORECASE).strip()
        cleaned = re.sub(r"```$", "", cleaned.strip()).strip()

    return cleaned


def _find_json_object_text(text: str) -> str:
    """Extract the first complete JSON object from text."""
    cleaned = _strip_markdown_fences(_remove_thinking_blocks(text))

    try:
        json.loads(cleaned)
        return cleaned
    except json.JSONDecodeError:
        pass

    start = cleaned.find("{")
    if start == -1:
        raise RuntimeError("模型返回内容中没有找到 JSON 对象。")

    in_string = False
    escape = False
    depth = 0

    for index in range(start, len(cleaned)):
        char = cleaned[index]

        if escape:
            escape = False
            continue

        if char == "\\":
            escape = True
            continue

        if char == '"':
            in_string = not in_string
            continue

        if in_string:
            continue

        if char == "{":
            depth += 1
        elif char == "}":
            depth -= 1

            if depth == 0:
                return cleaned[start:index + 1]

    raise RuntimeError("模型返回的 JSON 对象不完整。")


def _parse_json_object(text: str) -> dict[str, Any]:
    """Parse model output into a JSON object."""
    json_text = _find_json_object_text(text)

    try:
        data = json.loads(json_text)
    except json.JSONDecodeError as exc:
        raise RuntimeError(f"模型返回的内容不是合法 JSON：{exc}") from exc

    if not isinstance(data, dict):
        raise RuntimeError("模型返回的 JSON 顶层必须是对象。")

    return data


def _create_chat_completion(
    client: OpenAI,
    model: str,
    messages: list[dict[str, str]],
    use_response_format: bool,
):
    """Call Chat Completions with optional JSON mode."""
    kwargs: dict[str, Any] = {
        "model": model,
        "messages": messages,
    }

    if use_response_format:
        kwargs["response_format"] = {"type": "json_object"}

    return client.chat.completions.create(**kwargs)


def _call_model(
    client: OpenAI,
    model: str,
    messages: list[dict[str, str]],
) -> str:
    """Call third-party OpenAI-compatible Chat Completions API."""
    try:
        completion = _create_chat_completion(
            client=client,
            model=model,
            messages=messages,
            use_response_format=True,
        )
    except OpenAIError as exc:
        if not _is_response_format_unsupported(exc):
            raise RuntimeError(f"第三方 API 调用失败：{exc}") from exc

        completion = _create_chat_completion(
            client=client,
            model=model,
            messages=messages,
            use_response_format=False,
        )

    try:
        content = completion.choices[0].message.content
    except Exception as exc:
        raise RuntimeError(f"无法读取模型返回内容：{exc}") from exc

    if not content:
        raise RuntimeError("模型返回内容为空。")

    if not isinstance(content, str):
        raise RuntimeError("模型返回内容不是字符串，无法解析为 JSON。")

    return content


def convert_with_openai(
    chapters: list[Chapter],
    title: str,
    model: str | None = None,
    base_url: str | None = None,
    max_chars_per_chapter: int = 3500,
) -> dict[str, Any]:
    """Convert chapters to screenplay data using a third-party OpenAI-compatible API."""
    load_dotenv()

    api_key = _get_required_env(
        "OPENAI_API_KEY",
        placeholder_values={"your_api_key_here"},
    )

    selected_base_url = (base_url or os.getenv("OPENAI_BASE_URL", "")).strip()
    if not selected_base_url or selected_base_url == "https://your-third-party-api.example.com/v1":
        raise RuntimeError("缺少有效配置：OPENAI_BASE_URL。请在 .env 中填写第三方 API 地址。")

    selected_model = (model or os.getenv("OPENAI_MODEL", "")).strip()
    if not selected_model or selected_model == "your-model-name":
        raise RuntimeError("缺少有效配置：OPENAI_MODEL。请在 .env 中填写第三方模型名。")

    chapters_text = _format_chapters_for_prompt(
        chapters=chapters,
        max_chars_per_chapter=max_chars_per_chapter,
    )

    user_prompt = build_user_prompt(
        title=title,
        chapter_count=len(chapters),
        chapters_text=chapters_text,
        schema_text=_schema_for_prompt(),
    )

    client = _build_client(
        base_url=selected_base_url,
        api_key=api_key,
    )

    messages = [
        {"role": "system", "content": SYSTEM_PROMPT},
        {"role": "user", "content": user_prompt},
    ]

    raw_text = _call_model(
        client=client,
        model=selected_model,
        messages=messages,
    )

    data = _parse_json_object(raw_text)

    validate_screenplay(data)

    return data
