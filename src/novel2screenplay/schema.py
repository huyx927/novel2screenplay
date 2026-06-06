from __future__ import annotations

from jsonschema import Draft202012Validator


NON_EMPTY_STRING = {"type": "string", "minLength": 1}


SCREENPLAY_SCHEMA: dict = {
    "$schema": "https://json-schema.org/draft/2020-12/schema",
    "title": "Novel2Screenplay YAML Schema",
    "type": "object",
    "additionalProperties": False,
    "required": [
        "schema_version",
        "project",
        "characters",
        "locations",
        "acts",
        "adaptation_notes",
    ],
    "properties": {
        "schema_version": {
            "type": "string",
            "const": "1.0",
        },
        "project": {
            "type": "object",
            "additionalProperties": False,
            "required": ["title", "logline", "genre", "target_format", "source"],
            "properties": {
                "title": NON_EMPTY_STRING,
                "logline": NON_EMPTY_STRING,
                "genre": NON_EMPTY_STRING,
                "target_format": {
                    "type": "string",
                    "enum": [
                        "feature_film",
                        "short_film",
                        "web_drama",
                        "tv_episode",
                        "stage_play",
                        "audio_drama",
                        "other",
                    ],
                },
                "source": {
                    "type": "object",
                    "additionalProperties": False,
                    "required": ["chapter_count", "chapter_titles"],
                    "properties": {
                        "chapter_count": {
                            "type": "integer",
                            "minimum": 3,
                        },
                        "chapter_titles": {
                            "type": "array",
                            "minItems": 3,
                            "items": NON_EMPTY_STRING,
                        },
                    },
                },
            },
        },
        "characters": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "name", "role", "description", "arc"],
                "properties": {
                    "id": {
                        "type": "string",
                        "pattern": "^CHAR_[0-9]{3,}$",
                    },
                    "name": NON_EMPTY_STRING,
                    "role": {
                        "type": "string",
                        "enum": [
                            "protagonist",
                            "antagonist",
                            "supporting",
                            "mentor",
                            "love_interest",
                            "comic_relief",
                            "other",
                        ],
                    },
                    "description": NON_EMPTY_STRING,
                    "arc": NON_EMPTY_STRING,
                },
            },
        },
        "locations": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["id", "name", "description"],
                "properties": {
                    "id": {
                        "type": "string",
                        "pattern": "^LOC_[0-9]{3,}$",
                    },
                    "name": NON_EMPTY_STRING,
                    "description": NON_EMPTY_STRING,
                },
            },
        },
        "acts": {
            "type": "array",
            "minItems": 1,
            "items": {
                "type": "object",
                "additionalProperties": False,
                "required": ["act_number", "title", "purpose", "scenes"],
                "properties": {
                    "act_number": {
                        "type": "integer",
                        "minimum": 1,
                    },
                    "title": NON_EMPTY_STRING,
                    "purpose": NON_EMPTY_STRING,
                    "scenes": {
                        "type": "array",
                        "minItems": 1,
                        "items": {
                            "type": "object",
                            "additionalProperties": False,
                            "required": [
                                "scene_id",
                                "title",
                                "source_chapters",
                                "heading",
                                "synopsis",
                                "purpose",
                                "beats",
                                "action",
                                "dialogue",
                                "transition",
                                "revision_notes",
                            ],
                            "properties": {
                                "scene_id": {
                                    "type": "string",
                                    "pattern": "^S[0-9]{3,}$",
                                },
                                "title": NON_EMPTY_STRING,
                                "source_chapters": {
                                    "type": "array",
                                    "minItems": 1,
                                    "items": {
                                        "type": "integer",
                                        "minimum": 1,
                                    },
                                },
                                "heading": {
                                    "type": "object",
                                    "additionalProperties": False,
                                    "required": ["int_ext", "location", "time"],
                                    "properties": {
                                        "int_ext": {
                                            "type": "string",
                                            "enum": ["INT", "EXT", "INT/EXT"],
                                        },
                                        "location": NON_EMPTY_STRING,
                                        "time": NON_EMPTY_STRING,
                                    },
                                },
                                "synopsis": NON_EMPTY_STRING,
                                "purpose": NON_EMPTY_STRING,
                                "beats": {
                                    "type": "array",
                                    "minItems": 1,
                                    "items": NON_EMPTY_STRING,
                                },
                                "action": NON_EMPTY_STRING,
                                "dialogue": {
                                    "type": "array",
                                    "items": {
                                        "type": "object",
                                        "additionalProperties": False,
                                        "required": ["character", "parenthetical", "line"],
                                        "properties": {
                                            "character": NON_EMPTY_STRING,
                                            "parenthetical": {
                                                "type": "string",
                                            },
                                            "line": NON_EMPTY_STRING,
                                        },
                                    },
                                },
                                "transition": NON_EMPTY_STRING,
                                "revision_notes": {
                                    "type": "array",
                                    "items": NON_EMPTY_STRING,
                                },
                            },
                        },
                    },
                },
            },
        },
        "adaptation_notes": {
            "type": "array",
            "minItems": 1,
            "items": NON_EMPTY_STRING,
        },
    },
}


_validator = Draft202012Validator(SCREENPLAY_SCHEMA)


def _format_error_path(error) -> str:
    """Convert a jsonschema error path into readable text."""
    path = ".".join(str(part) for part in error.absolute_path)
    return path or "<root>"


def _validate_cross_references(data: dict) -> None:
    """Validate relationships that plain JSON Schema cannot easily express."""
    chapter_count = data["project"]["source"]["chapter_count"]
    chapter_titles = data["project"]["source"]["chapter_titles"]

    if len(chapter_titles) != chapter_count:
        raise ValueError(
            "YAML Schema 校验失败：project.source.chapter_titles 的数量 "
            "必须等于 project.source.chapter_count。"
        )

    seen_scene_ids: set[str] = set()

    for act in data["acts"]:
        for scene in act["scenes"]:
            scene_id = scene["scene_id"]
            if scene_id in seen_scene_ids:
                raise ValueError(f"YAML Schema 校验失败：scene_id 重复：{scene_id}")
            seen_scene_ids.add(scene_id)

            for chapter_number in scene["source_chapters"]:
                if chapter_number > chapter_count:
                    raise ValueError(
                        f"YAML Schema 校验失败：场景 {scene_id} 引用了不存在的章节 "
                        f"{chapter_number}，当前总章节数为 {chapter_count}。"
                    )


def validate_screenplay(data: dict) -> None:
    """Validate generated screenplay data against the screenplay schema."""
    errors = sorted(
        _validator.iter_errors(data),
        key=lambda error: list(error.absolute_path),
    )

    if errors:
        first_error = errors[0]
        error_path = _format_error_path(first_error)
        raise ValueError(f"YAML Schema 校验失败：{error_path}: {first_error.message}")

    _validate_cross_references(data)