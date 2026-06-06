from novel2screenplay.chapter_splitter import split_chapters
from novel2screenplay.demo_converter import build_demo_screenplay
from novel2screenplay.schema import validate_screenplay
from novel2screenplay.yaml_exporter import from_yaml, to_yaml


def sample_chapters():
    text = """
第1章 雨夜来信
林澈收到一封没有署名的信。信上写着：十年前的站台，有人还在等你。

第2章 旧站台
他回到十年前分别的站台。荒草覆盖铁轨，候车室里只剩下一盏坏掉的灯。

第3章 录音里的名字
录音笔里传出熟悉的声音。那个名字像一把钥匙，打开了他一直回避的过去。
"""
    return split_chapters(text)


def test_demo_converter_outputs_valid_screenplay_data():
    chapters = sample_chapters()
    data = build_demo_screenplay(chapters, title="雾城来信")

    validate_screenplay(data)

    assert data["schema_version"] == "1.0"
    assert data["project"]["title"] == "雾城来信"
    assert data["project"]["source"]["chapter_count"] == 3
    assert len(data["acts"][0]["scenes"]) == 3


def test_demo_converter_keeps_source_chapter_references():
    chapters = sample_chapters()
    data = build_demo_screenplay(chapters, title="雾城来信")

    scenes = data["acts"][0]["scenes"]

    assert scenes[0]["scene_id"] == "S001"
    assert scenes[0]["source_chapters"] == [1]
    assert scenes[1]["scene_id"] == "S002"
    assert scenes[1]["source_chapters"] == [2]
    assert scenes[2]["scene_id"] == "S003"
    assert scenes[2]["source_chapters"] == [3]


def test_yaml_export_round_trip_stays_valid():
    chapters = sample_chapters()
    data = build_demo_screenplay(chapters, title="雾城来信")

    yaml_text = to_yaml(data)
    loaded = from_yaml(yaml_text)

    validate_screenplay(loaded)

    assert "schema_version" in yaml_text
    assert "雾城来信" in yaml_text
    assert loaded["project"]["title"] == "雾城来信"