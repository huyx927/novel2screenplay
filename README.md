# Novel2Screenplay

Novel2Screenplay 是一款 AI 辅助小说转剧本工具。它面向希望将小说改编为剧本的作者，支持输入 3 个章节以上的小说文本，并输出结构化剧本 YAML 初稿。

本项目的目标不是一次性生成最终剧本，而是帮助作者快速得到一个可编辑、可校验、可继续打磨的剧本结构初稿。

本工具提供 demo 模式和 AI 模式。demo 模式不调用外部 API，它采用规则模板，把每个小说章节映射为一个剧本场景，用于验证章节识别、Schema 校验、YAML 导出和网页下载流程。真正的智能改编由 AI 模式完成，AI 模式会调用第三方 OpenAI-compatible API，根据小说内容生成更丰富的结构化剧本初稿。

---

## 1. 核心功能

- 自动识别小说章节。
- 校验输入是否至少包含 3 个章节。
- 支持网页端粘贴小说文本并生成剧本 YAML。
- 支持命令行从 TXT 文件生成 YAML。
- 支持 demo 模式，不需要 API Key 也能运行完整流程。
- 支持第三方 OpenAI-compatible API 的 AI 模式。
- 使用 YAML 作为最终输出格式，方便作者继续编辑。
- 使用 JSON Schema 思路对剧本数据进行本地校验。
- 提供 YAML Schema 设计文档。
- 提供示例输入和示例输出。
- 提供 pytest 自动测试。

---

## 2. 项目结构

```text
NOVEL2SCREENPLAY/
├── app.py
├── README.md
├── requirements.txt
├── pyproject.toml
├── .gitignore
├── .env.example
├── data/
│   └── sample_novel.txt
├── docs/
│   └── YAML_SCHEMA.md
├── examples/
│   ├── sample_output_demo.yaml
│   └── sample_output_ai.yaml
├── src/
│   └── novel2screenplay/
│       ├── __init__.py
│       ├── chapter_splitter.py
│       ├── schema.py
│       ├── yaml_exporter.py
│       ├── demo_converter.py
│       ├── converter.py
│       ├── cli.py
│       ├── prompts.py
│       └── llm_openai.py
└── tests/
    ├── test_chapter_splitter.py
    ├── test_schema.py
    ├── test_demo_converter.py
    ├── test_converter.py
    ├── test_cli.py
    └── test_openai_converter.py
```

如果 `sample_output_ai.yaml` 不存在，说明当前仓库只提交了 demo 示例输出。AI 示例输出需要可用的第三方 API 配置。

---

## 3. 核心模块说明

| 文件 | 作用 |
|---|---|
| `app.py` | Streamlit 网页入口 |
| `chapter_splitter.py` | 识别小说章节 |
| `schema.py` | 定义并校验剧本数据结构 |
| `yaml_exporter.py` | Python 字典与 YAML 文本互相转换 |
| `demo_converter.py` | 不调用 API 的演示转换器 |
| `converter.py` | 统一转换流程入口 |
| `cli.py` | 命令行入口 |
| `prompts.py` | AI 改编提示词 |
| `llm_openai.py` | 第三方 OpenAI-compatible API 调用逻辑 |
| `docs/YAML_SCHEMA.md` | YAML Schema 设计说明 |
| `data/sample_novel.txt` | 示例小说输入 |
| `examples/` | 示例 YAML 输出 |
| `tests/` | 自动测试 |

---

## 4. 安装环境

建议使用 Python 3.10 或更新版本。

### 4.1 克隆或下载项目

如果已经在本地打开项目，可以跳过这一步。

```bash
git clone <your-repository-url>
cd novel2screenplay
```

### 4.2 创建虚拟环境

Windows CMD：

```cmd
python -m venv .venv
.\.venv\Scripts\activate.bat
```

Windows PowerShell：

```powershell
python -m venv .venv
.\.venv\Scripts\Activate.ps1
```

macOS / Linux：

```bash
python -m venv .venv
source .venv/bin/activate
```

激活成功后，终端前面应该出现：

```text
(.venv)
```

### 4.3 安装依赖

```bash
python -m pip install -r requirements.txt
python -m pip install -e .
```

---

## 5. 运行网页应用

运行：

```bash
python -m streamlit run app.py
```

浏览器打开后，可以直接使用默认示例文本测试。

### demo 模式

默认勾选：

```text
演示模式：不调用第三方 API
```

这个模式不需要 API Key，可以直接生成 YAML。

### AI 模式

取消勾选：

```text
演示模式：不调用第三方 API
```

然后填写或从 `.env` 自动读取：

```text
第三方 API Base URL
模型名
```

AI 模式需要提前配置 `.env`。

---

## 6. 第三方 API 配置

本项目支持 OpenAI-compatible API。也就是说，只要第三方平台兼容 OpenAI 的 Chat Completions 调用格式，就可以尝试使用。

### 6.1 创建 `.env`

复制模板文件：

Windows CMD：

```cmd
copy .env.example .env
```

macOS / Linux：

```bash
cp .env.example .env
```

### 6.2 填写 `.env`

打开 `.env`，填写你的真实配置：

```txt
OPENAI_API_KEY=your_real_api_key
OPENAI_BASE_URL=https://your-third-party-api.example.com/v1
OPENAI_MODEL=your-model-name
```

说明：

- `OPENAI_API_KEY`：第三方平台提供的 API Key。
- `OPENAI_BASE_URL`：第三方平台的 API Base URL，通常以 `/v1` 结尾。
- `OPENAI_MODEL`：第三方平台提供的模型名。

注意：

```text
.env 文件包含私密 API Key，不要提交到 GitHub。
```

本项目的 `.gitignore` 已经忽略 `.env`。

---

## 7. 命令行使用

### 7.1 demo 模式生成 YAML

```bash
python -m novel2screenplay.cli data/sample_novel.txt --title 手稿改编计划 --mode demo --output examples/sample_output_demo.yaml
```

这个命令会读取：

```text
data/sample_novel.txt
```

并生成：

```text
examples/sample_output_demo.yaml
```

### 7.2 AI 模式生成 YAML

```bash
python -m novel2screenplay.cli data/sample_novel.txt --title 手稿改编计划 --mode ai --max-chars-per-chapter 800 --output examples/sample_output_ai.yaml
```

如果 `.env` 配置正确，程序会调用第三方 API 生成更丰富的剧本 YAML。

### 7.3 临时指定模型和 Base URL

也可以在命令行中临时指定：

```bash
python -m novel2screenplay.cli data/sample_novel.txt --title 手稿改编计划 --mode ai --base-url https://your-third-party-api.example.com/v1 --model your-model-name --max-chars-per-chapter 800 --output examples/sample_output_ai.yaml
```

---

## 8. 运行测试

运行全部测试：

```bash
python -m pytest -q
```

如果全部正常，会看到类似：

```text
17 passed
```

测试数量可能因为后续修改略有不同，只要最终显示全部通过即可。

---

## 9. YAML 输出格式

本项目输出的是结构化 YAML，核心结构如下：

```yaml
schema_version: "1.0"
project:
  title: "手稿改编计划"
  logline: "主角发现一份手稿，并尝试将其改编成短剧。"
  genre: "剧情"
  target_format: "web_drama"
  source:
    chapter_count: 3
    chapter_titles:
      - "第1章 新编辑的第一天"
characters:
  - id: "CHAR_001"
    name: "主角"
    role: "protagonist"
    description: "承载主要行动线的人物。"
    arc: "从被动完成任务到主动理解改编。"
locations:
  - id: "LOC_001"
    name: "资料室"
    description: "主角发现手稿的地方。"
acts:
  - act_number: 1
    title: "第一幕：发现与尝试"
    purpose: "建立主角目标与改编任务。"
    scenes:
      - scene_id: "S001"
        title: "发现手稿"
        source_chapters: [1]
        heading:
          int_ext: "INT"
          location: "资料室"
          time: "日"
        synopsis: "主角发现一份被遗忘的手稿。"
        purpose: "触发改编行动。"
        beats:
          - "进入资料室"
          - "发现手稿"
          - "决定尝试改编"
        action: "主角翻开泛黄的纸页，停在第一页。"
        dialogue:
          - character: "主角"
            parenthetical: "轻声"
            line: "也许这就是我要找的故事。"
        transition: "CUT TO:"
        revision_notes:
          - "可以补充更明确的视觉细节。"
adaptation_notes:
  - "后续可以强化人物目标和戏剧冲突。"
```

完整 Schema 设计说明见：

```text
docs/YAML_SCHEMA.md
```

---

## 10. 示例文件

### 示例输入

```text
data/sample_novel.txt
```

### demo 示例输出

```text
examples/sample_output_demo.yaml
```

### AI 示例输出

```text
examples/sample_output_ai.yaml
```

如果 AI 示例不存在，说明当前仓库没有提交 AI 生成结果。用户可以自行配置第三方 API 后生成。

---

## 11. 设计思路

本项目采用分层设计：

```text
输入层：小说文本
解析层：章节识别
转换层：demo 转换器或 AI 转换器
校验层：YAML Schema 校验
导出层：YAML 文本导出
界面层：Streamlit 网页和 CLI 命令行
```

这样设计的好处是：

1. demo 模式和 AI 模式可以复用同一套转换流程。
2. 网页和命令行可以复用同一个 `convert_novel_text()` 入口。
3. AI 输出不会被直接信任，必须经过本地 Schema 校验。
4. YAML 输出既适合作者阅读，也适合程序继续处理。
5. 后续可以扩展 Word、PDF、分场表、人物表等导出功能。

---

## 12. 常见问题

### 12.1 为什么要求至少 3 个章节？

题目要求工具能处理 3 个章节以上的小说文本，所以程序会检查章节数量。如果少于 3 章，会提示用户补充更多章节。

### 12.2 为什么要有 demo 模式？

demo 模式不调用 API，可以保证项目在没有 API Key、第三方平台不可用或网络异常时仍然能完整演示：

```text
章节识别 → 剧本结构生成 → Schema 校验 → YAML 导出
```

### 12.3 为什么不直接让 AI 输出 YAML？

直接输出 YAML 容易出现格式错误、字段缺失或额外解释文字。

本项目采用：

```text
AI 输出 JSON
→ 本地解析
→ Schema 校验
→ 导出 YAML
```

这样更稳定。

### 12.4 第三方 API 报 `Your request was blocked` 怎么办？

这通常是第三方平台拦截请求，不一定是项目代码错误。可以检查：

1. `OPENAI_API_KEY` 是否正确。
2. `OPENAI_BASE_URL` 是否正确。
3. `OPENAI_MODEL` 是否是平台支持的模型名。
4. 账号是否有额度或模型权限。
5. 平台是否限制 IP 或请求内容。
6. 尝试降低 `--max-chars-per-chapter`。

### 12.5 为什么要写 `docs/YAML_SCHEMA.md`？

因为题目要求额外定义剧本 YAML Schema，并说明设计原因。该文档用于解释输出结构、字段含义、设计取舍和后续扩展方向。

---

## 13. 开发阶段记录

本项目按照以下阶段逐步完成：

1. 初始化项目结构。
2. 实现章节识别。
3. 定义剧本 YAML Schema。
4. 实现 demo 模式转换器。
5. 加入统一转换入口和命令行工具。
6. 接入第三方 OpenAI-compatible API。
7. 补充 YAML Schema 文档。
8. 添加示例输入和示例输出。
9. 完善 README 和使用说明。

---

## 14. 后续可扩展方向

后续可以继续扩展：

- YAML 转 Word 剧本。
- YAML 转 PDF 剧本。
- 生成分场表。
- 生成角色表。
- 生成拍摄地点表。
- 支持多种剧本格式。
- 支持更长小说的分批处理。
- 增加人工编辑界面。
- 增加导入和导出项目功能。

---

## 15. 许可证

本项目用于学习和课程作业展示。实际使用第三方 API 时，请遵守对应平台的服务条款和费用规则。