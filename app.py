from __future__ import annotations

import os

from dotenv import load_dotenv
import streamlit as st

from novel2screenplay.chapter_splitter import split_chapters
from novel2screenplay.converter import convert_novel_text


load_dotenv()

SAMPLE_TEXT = """
第1章 雨夜来信
雨一直下到深夜。林澈回到出租屋时，门缝里夹着一封没有署名的信。信纸只有一句话：十年前的站台，有人还在等你。

第2章 旧站台
第二天清晨，林澈坐上去往雾城的慢车。旧站台早已停用，铁轨旁长满荒草。他在候车室的长椅下发现一枚生锈的钥匙。

第3章 录音里的名字
钥匙打开了站台仓库里的铁盒。盒子里有一支录音笔。林澈按下播放键，里面传出母亲失踪前的声音，她反复念着一个陌生人的名字。
""".strip()


st.set_page_config(page_title="Novel2Screenplay", page_icon="🎬", layout="wide")

st.title("🎬 Novel2Screenplay")
st.write("把 3 个章节以上的小说文本转换为结构化剧本 YAML 初稿。")

if "generated_yaml" not in st.session_state:
    st.session_state.generated_yaml = None

with st.sidebar:
    st.header("项目设置")
    project_title = st.text_input("项目标题", value="雾城来信")

    st.header("生成模式")
    use_demo = st.checkbox("演示模式：不调用第三方 API", value=True)

    base_url = st.text_input(
        "第三方 API Base URL",
        value=os.getenv("OPENAI_BASE_URL", ""),
        disabled=use_demo,
    )

    model = st.text_input(
        "模型名",
        value=os.getenv("OPENAI_MODEL", ""),
        disabled=use_demo,
    )

    max_chars = st.slider(
        "AI 模式：每章最多发送字符数",
        min_value=800,
        max_value=8000,
        value=3500,
        step=100,
        disabled=use_demo,
    )

    if use_demo:
        st.caption("当前使用演示模式，不需要 API Key。")
    else:
        st.caption("当前使用 AI 模式，需要本地 .env 中配置 OPENAI_API_KEY。")

novel_text = st.text_area(
    "请粘贴小说文本",
    value=SAMPLE_TEXT,
    height=320,
)

chapters = split_chapters(novel_text)

st.subheader("章节识别结果")
st.info(f"当前识别到 {len(chapters)} 个章节。题目要求至少 3 个章节。")

if len(chapters) < 3:
    st.warning("章节数量不足。请至少输入 3 个章节。")
else:
    st.success("章节数量符合要求，可以生成剧本 YAML。")

for chapter in chapters:
    with st.expander(f"{chapter.number}. {chapter.title}"):
        preview = chapter.content[:500]
        st.write(preview if preview else "该章节正文为空。")

st.divider()

st.subheader("生成剧本 YAML")

button_label = "生成演示剧本 YAML" if use_demo else "生成 AI 剧本 YAML"

if st.button(button_label, type="primary"):
    try:
        mode = "demo" if use_demo else "ai"

        with st.spinner("正在生成剧本 YAML，请稍候..."):
            result = convert_novel_text(
                text=novel_text,
                title=project_title,
                mode=mode,
                model=model,
                base_url=base_url,
                max_chars_per_chapter=max_chars,
            )

        st.session_state.generated_yaml = result.yaml_text

        st.success("剧本 YAML 生成成功。")
        st.caption(f"已识别章节数：{len(result.chapters)}，生成模式：{result.mode}")

    except Exception as exc:
        st.session_state.generated_yaml = None
        st.error(f"生成失败：{exc}")

if st.session_state.generated_yaml:
    st.code(st.session_state.generated_yaml, language="yaml")

    file_name = "screenplay_demo.yaml" if use_demo else "screenplay_ai.yaml"

    st.download_button(
        label=f"下载 {file_name}",
        data=st.session_state.generated_yaml.encode("utf-8"),
        file_name=file_name,
        mime="text/yaml",
    )