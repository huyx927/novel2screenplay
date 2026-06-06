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

## AI 模式配置：第三方 OpenAI-compatible API

本项目支持两种模式：

- `demo`：不调用 API，使用本地演示转换器生成 YAML。
- `ai`：调用第三方 OpenAI-compatible API，把小说章节改编为剧本 YAML。

### 配置 `.env`

复制模板：

```bash
copy .env.example .env

然后在 `.env` 中配置你的 API 密钥、基础 URL 和模型名称。
注意：.env中包含私密信息，建议在版本控制中忽略。

命令行运行ai模式：
python -m novel2screenplay.cli data/sample_novel.txt --title 雾城来信 --mode ai --max-chars-per-chapter 1200 --output outputs/ai_demo.yaml

网页运行：
python -m streamlit run app.py
打开页面后，取消勾选“演示模式”，即可使用 AI 模式。