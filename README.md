# Novel2Screenplay

AI 辅助小说转剧本工具：输入 3 个章节以上的小说文本，输出结构化剧本 YAML 初稿。

## 本地运行

```bash
python -m venv .venv
# Windows PowerShell: .\.venv\Scripts\Activate.ps1
# macOS/Linux: source .venv/bin/activate
pip install -r requirements.txt
pip install -e .
pytest -q
streamlit run app.py