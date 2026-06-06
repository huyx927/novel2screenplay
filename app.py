from __future__ import annotations

import streamlit as st

from novel2screenplay.chapter_splitter import split_chapters


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
    st.success("章节数量符合要求，可以进入后续剧本转换流程。")

for chapter in chapters:
    with st.expander(f"{chapter.number}. {chapter.title}"):
        preview = chapter.content[:500]
        st.write(preview if preview else "该章节正文为空。")