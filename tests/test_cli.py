from novel2screenplay.cli import main


def test_cli_writes_yaml_file(tmp_path):
    input_path = tmp_path / "novel.txt"
    output_path = tmp_path / "screenplay.yaml"

    input_path.write_text(
        """
第1章 雨夜来信
林澈收到一封没有署名的信。信上写着：十年前的站台，有人还在等你。

第2章 旧站台
他回到十年前分别的站台。荒草覆盖铁轨，候车室里只剩下一盏坏掉的灯。

第3章 录音里的名字
录音笔里传出熟悉的声音。那个名字像一把钥匙，打开了他一直回避的过去。
""",
        encoding="utf-8",
    )

    exit_code = main(
        [
            str(input_path),
            "--title",
            "雾城来信",
            "--mode",
            "demo",
            "--output",
            str(output_path),
        ]
    )

    assert exit_code == 0
    assert output_path.exists()

    yaml_text = output_path.read_text(encoding="utf-8")

    assert "schema_version" in yaml_text
    assert "雾城来信" in yaml_text
    assert "source_chapters" in yaml_text