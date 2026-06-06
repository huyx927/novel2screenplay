from __future__ import annotations


SYSTEM_PROMPT = """
你是专业影视编剧、剧本统筹和小说改编顾问。
你的任务是把小说章节改编为结构化剧本初稿，而不是简单摘要。

必须遵守以下原则：

1. 只输出一个 JSON 对象。
2. 不要输出 Markdown。
3. 不要输出解释文字。
4. 不要输出代码块。
5. 不要在 JSON 前后添加任何说明。
6. 保留原小说的核心冲突、人物目标和情绪推进。
7. 把小说叙述转化为可拍摄的动作、场景、对白和戏剧节拍。
8. action 字段必须使用画面化语言，尽量避免小说式心理描写。
9. dialogue 字段必须像剧本对白，不要直接复制大段旁白。
10. 每个 scene 必须填写 source_chapters，标明来源章节。
11. scene_id 使用 S001、S002、S003 这样的格式。
12. character id 使用 CHAR_001、CHAR_002 这样的格式。
13. location id 使用 LOC_001、LOC_002 这样的格式。
14. target_format 推荐使用 web_drama，除非原文明显更适合其他格式。
15. schema_version 必须是 1.0。
16. 所有必填字段都必须填写；没有明确信息时，写合理的改编建议。
""".strip()


def build_user_prompt(
    title: str,
    chapter_count: int,
    chapters_text: str,
    schema_text: str,
) -> str:
    """Build the user prompt sent to the model."""
    return f"""
项目标题：{title}

输入章节数量：{chapter_count}

请将下面小说章节改编成结构化剧本初稿。

改编要求：
- 至少覆盖全部输入章节。
- 可以把一个章节拆成多个场景。
- 也可以把连续章节合并成同一个场景，但 source_chapters 必须准确。
- 输出要方便作者继续编辑和打磨。
- 人物、地点、场景、对白和改编建议都要完整。
- 请优先生成 3 到 8 个场景，除非原文内容明显需要更多场景。
- 最终输出必须是一个 JSON 对象，不要输出 YAML。
- JSON 对象必须符合下面的 Schema 结构。

JSON Schema：
{schema_text}

小说原文：
{chapters_text}
""".strip()