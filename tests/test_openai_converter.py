from novel2screenplay.converter import convert_novel_text
from novel2screenplay.demo_converter import build_demo_screenplay
from novel2screenplay.llm_openai import _build_client, _parse_json_object, _schema_for_prompt


def sample_text() -> str:
    return """
第1章 雨夜来信
林澈收到一封没有署名的信。信上写着：十年前的站台，有人还在等你。

第2章 旧站台
他回到十年前分别的站台。荒草覆盖铁轨，候车室里只剩下一盏坏掉的灯。

第3章 录音里的名字
录音笔里传出熟悉的声音。那个名字像一把钥匙，打开了他一直回避的过去。
"""


def test_schema_for_prompt_contains_required_keys():
    schema_text = _schema_for_prompt()

    assert "schema_version" in schema_text
    assert "project" in schema_text
    assert "characters" in schema_text
    assert "locations" in schema_text
    assert "acts" in schema_text
    assert "adaptation_notes" in schema_text


def test_build_client_uses_provider_compatible_user_agent():
    client = _build_client(
        base_url="https://example.com/v1",
        api_key="test-key",
    )

    assert client.default_headers["User-Agent"] == "python-httpx/0.28.1"


def test_parse_json_object_from_extra_text():
    raw_text = """
模型输出如下：
{
  "schema_version": "1.0",
  "project": {
    "title": "测试项目"
  }
}
以上是结果。
"""

    data = _parse_json_object(raw_text)

    assert data["schema_version"] == "1.0"
    assert data["project"]["title"] == "测试项目"


def test_convert_novel_text_ai_mode_can_be_mocked(monkeypatch):
    from novel2screenplay import llm_openai

    def fake_convert_with_openai(
        chapters,
        title,
        model=None,
        base_url=None,
        max_chars_per_chapter=3500,
    ):
        assert model == "fake-model"
        assert base_url == "https://fake.example.com/v1"
        assert max_chars_per_chapter == 500
        return build_demo_screenplay(chapters=chapters, title=title)

    monkeypatch.setattr(
        llm_openai,
        "convert_with_openai",
        fake_convert_with_openai,
    )

    result = convert_novel_text(
        text=sample_text(),
        title="雾城来信",
        mode="ai",
        model="fake-model",
        base_url="https://fake.example.com/v1",
        max_chars_per_chapter=500,
    )

    assert result.mode == "ai"
    assert result.title == "雾城来信"
    assert len(result.chapters) == 3
    assert "schema_version" in result.yaml_text
    assert "雾城来信" in result.yaml_text
