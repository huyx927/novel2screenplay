import pytest

from novel2screenplay.converter import convert_novel_text


def sample_text() -> str:
    return """
第1章 雨夜来信
林澈收到一封没有署名的信。信上写着：十年前的站台，有人还在等你。

第2章 旧站台
他回到十年前分别的站台。荒草覆盖铁轨，候车室里只剩下一盏坏掉的灯。

第3章 录音里的名字
录音笔里传出熟悉的声音。那个名字像一把钥匙，打开了他一直回避的过去。
"""


def test_convert_novel_text_demo_mode_outputs_yaml():
    result = convert_novel_text(
        text=sample_text(),
        title="雾城来信",
        mode="demo",
    )

    assert result.title == "雾城来信"
    assert result.mode == "demo"
    assert len(result.chapters) == 3
    assert result.data["project"]["title"] == "雾城来信"
    assert "schema_version" in result.yaml_text
    assert "雾城来信" in result.yaml_text


def test_convert_novel_text_rejects_too_few_chapters():
    text = """
第1章 只有一章
这里是唯一一章的内容。
"""

    with pytest.raises(ValueError):
        convert_novel_text(text=text, title="章节不足", mode="demo")


def test_convert_novel_text_rejects_unknown_mode():
    with pytest.raises(ValueError):
        convert_novel_text(
            text=sample_text(),
            title="雾城来信",
            mode="unknown",
        )