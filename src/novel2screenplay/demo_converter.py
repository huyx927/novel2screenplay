from __future__ import annotations

from novel2screenplay.chapter_splitter import Chapter


def _one_line(text: str) -> str:
    """Compress text into a single readable line."""
    return " ".join(text.split())


def _preview(text: str, limit: int = 120) -> str:
    """Return a short content preview for synopsis generation."""
    cleaned = _one_line(text)
    if not cleaned:
        return "本章正文较少，需要作者补充具体情节。"

    if len(cleaned) <= limit:
        return cleaned

    return cleaned[:limit] + "..."


def _guess_time(text: str) -> str:
    """Guess scene time from chapter content."""
    content = text

    if any(word in content for word in ["深夜", "夜里", "夜晚", "夜色", "半夜"]):
        return "夜"

    if any(word in content for word in ["清晨", "早晨", "黎明"]):
        return "清晨"

    if any(word in content for word in ["黄昏", "傍晚", "夕阳"]):
        return "傍晚"

    return "日"


def _location_name(chapter: Chapter) -> str:
    """Create a draft location name for the chapter."""
    return f"{chapter.title}的核心地点"


def build_demo_screenplay(
    chapters: list[Chapter],
    title: str = "未命名改编项目",
) -> dict:
    """Build a deterministic screenplay draft without calling AI.

    This demo converter is intentionally simple:
    every source chapter becomes one screenplay scene.
    Later, the AI converter will generate richer scenes, characters, and dialogue.
    """
    if len(chapters) < 3:
        raise ValueError(f"演示转换需要至少 3 个章节，目前只有 {len(chapters)} 个。")

    locations = []
    scenes = []

    for chapter in chapters:
        location_id = f"LOC_{chapter.number:03d}"
        location_name = _location_name(chapter)
        scene_time = _guess_time(chapter.content)

        locations.append(
            {
                "id": location_id,
                "name": location_name,
                "description": f"根据《{chapter.title}》提炼出的主要行动空间。",
            }
        )

        scenes.append(
            {
                "scene_id": f"S{chapter.number:03d}",
                "title": f"场景{chapter.number}：{chapter.title}",
                "source_chapters": [chapter.number],
                "heading": {
                    "int_ext": "INT/EXT",
                    "location": location_name,
                    "time": scene_time,
                },
                "synopsis": f"本场根据《{chapter.title}》改编：{_preview(chapter.content)}",
                "purpose": "将小说叙述转化为具有明确目标、冲突和推进作用的戏剧场景。",
                "beats": [
                    "建立场景氛围和人物当前目标",
                    "让人物发现线索、遭遇阻碍或做出选择",
                    "以新的问题或行动方向推动下一场",
                ],
                "action": (
                    f"镜头进入《{chapter.title}》的核心情境。"
                    "人物在环境压力下行动，关键细节被转化为可拍摄的画面。"
                ),
                "dialogue": [
                    {
                        "character": "主角",
                        "parenthetical": "压低声音",
                        "line": "这件事不能再拖下去了。",
                    },
                    {
                        "character": "对手或同伴",
                        "parenthetical": "停顿",
                        "line": "你确定要继续查下去吗？",
                    },
                ],
                "transition": "CUT TO:",
                "revision_notes": [
                    "演示模式生成的是结构化初稿，后续可用 AI 模式细化人物动机、动作和对白。",
                    "建议作者根据原小说补充更具体的视觉细节。",
                ],
            }
        )

    return {
        "schema_version": "1.0",
        "project": {
            "title": title,
            "logline": "主角被一个意外事件卷入核心矛盾，并被迫面对隐藏的真相。",
            "genre": "剧情 / 悬疑",
            "target_format": "web_drama",
            "source": {
                "chapter_count": len(chapters),
                "chapter_titles": [chapter.title for chapter in chapters],
            },
        },
        "characters": [
            {
                "id": "CHAR_001",
                "name": "主角",
                "role": "protagonist",
                "description": "承载主要行动线的人物，负责推动观众进入故事核心矛盾。",
                "arc": "从被动卷入事件，到主动做出选择并追寻真相。",
            },
            {
                "id": "CHAR_002",
                "name": "对手或同伴",
                "role": "supporting",
                "description": "推动冲突、提供信息或制造阻碍的人物。",
                "arc": "与主角的目标形成张力，迫使主角改变行动策略。",
            },
            {
                "id": "CHAR_003",
                "name": "隐藏真相相关人物",
                "role": "antagonist",
                "description": "与故事秘密或核心冲突有关的人物。",
                "arc": "从缺席或隐藏，到逐渐显露其对事件的影响。",
            },
        ],
        "locations": locations,
        "acts": [
            {
                "act_number": 1,
                "title": "第一幕：事件触发与悬念建立",
                "purpose": "建立人物处境、核心悬念和主角的初始行动方向。",
                "scenes": scenes,
            }
        ],
        "adaptation_notes": [
            "演示模式采用“一章对应一场”的稳定策略，便于验证流程和展示结果。",
            "正式 AI 模式可以把一个章节拆成多场，也可以把多个章节合并成一场。",
            "剧本改编重点不是复述小说，而是把叙述转化为动作、对白、冲突和节拍。",
        ],
    }