import pytest

from novel2screenplay.schema import validate_screenplay


def valid_data():
    return {
        "schema_version": "1.0",
        "project": {
            "title": "雾城来信",
            "logline": "一封匿名信把主角带回旧案现场。",
            "genre": "悬疑",
            "target_format": "web_drama",
            "source": {
                "chapter_count": 3,
                "chapter_titles": [
                    "第1章 雨夜来信",
                    "第2章 旧站台",
                    "第3章 录音里的名字",
                ],
            },
        },
        "characters": [
            {
                "id": "CHAR_001",
                "name": "林澈",
                "role": "protagonist",
                "description": "收到匿名信的青年。",
                "arc": "从逃避过去到主动追查真相。",
            },
            {
                "id": "CHAR_002",
                "name": "神秘来信者",
                "role": "antagonist",
                "description": "用匿名信推动主角回到旧案现场的人。",
                "arc": "从隐藏在幕后到逐渐暴露真实目的。",
            },
        ],
        "locations": [
            {
                "id": "LOC_001",
                "name": "出租屋",
                "description": "主角收到匿名信的地方。",
            },
            {
                "id": "LOC_002",
                "name": "旧站台",
                "description": "十年前事件的核心地点。",
            },
        ],
        "acts": [
            {
                "act_number": 1,
                "title": "第一幕：来信与旧地",
                "purpose": "建立悬念，推动主角回到旧案现场。",
                "scenes": [
                    {
                        "scene_id": "S001",
                        "title": "雨夜来信",
                        "source_chapters": [1],
                        "heading": {
                            "int_ext": "INT",
                            "location": "出租屋",
                            "time": "夜",
                        },
                        "synopsis": "林澈在雨夜收到一封没有署名的信。",
                        "purpose": "用匿名信触发主角行动。",
                        "beats": [
                            "林澈回到出租屋",
                            "发现门缝里的匿名信",
                            "读到十年前站台的提示",
                        ],
                        "action": "雨水拍打窗户。林澈推门进屋，发现门缝里夹着一封信。",
                        "dialogue": [
                            {
                                "character": "林澈",
                                "parenthetical": "低声",
                                "line": "十年前的站台？你到底是谁？",
                            }
                        ],
                        "transition": "CUT TO:",
                        "revision_notes": [
                            "可以增加信纸上的视觉符号，让悬念更强。"
                        ],
                    }
                ],
            }
        ],
        "adaptation_notes": [
            "保留原小说的悬疑线。",
            "把小说叙述改成可拍摄的动作和对白。",
        ],
    }


def test_valid_schema_passes():
    validate_screenplay(valid_data())


def test_schema_rejects_missing_required_key():
    data = valid_data()
    del data["project"]["logline"]

    with pytest.raises(ValueError):
        validate_screenplay(data)


def test_schema_rejects_extra_field():
    data = valid_data()
    data["project"]["unexpected_field"] = "这个字段不应该存在"

    with pytest.raises(ValueError):
        validate_screenplay(data)


def test_schema_rejects_invalid_source_chapter_reference():
    data = valid_data()
    data["acts"][0]["scenes"][0]["source_chapters"] = [99]

    with pytest.raises(ValueError):
        validate_screenplay(data)