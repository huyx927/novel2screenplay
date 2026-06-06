import pytest

from novel2screenplay.chapter_splitter import split_chapters, require_min_chapters


def test_split_chinese_chapters():
    text = """
第1章 雨夜来信
林澈收到一封没有署名的信。

第二章 旧站台
他回到十年前分别的站台。

第3回 录音里的名字
录音笔里传出熟悉的声音。
"""
    chapters = split_chapters(text)

    assert len(chapters) == 3
    assert chapters[0].title == "第1章 雨夜来信"
    assert "没有署名" in chapters[0].content
    assert chapters[1].number == 2


def test_split_english_chapters():
    text = "Chapter 1\nA letter arrives.\n\nChapter 2\nA train leaves."
    chapters = split_chapters(text)

    assert len(chapters) == 2
    assert chapters[1].title == "Chapter 2"


def test_require_min_chapters_raises():
    with pytest.raises(ValueError):
        require_min_chapters(split_chapters("第1章 开始\n只有一章"), minimum=3)