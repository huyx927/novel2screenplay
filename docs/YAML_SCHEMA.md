# Novel2Screenplay YAML Schema 设计说明

## 1. 文档目的

本文档定义 Novel2Screenplay 工具输出的剧本 YAML Schema，并说明该 Schema 的设计原因。

Novel2Screenplay 的目标是帮助小说作者把 3 个章节以上的小说文本快速转换为结构化剧本初稿。这个剧本初稿不是最终成片剧本，而是一个方便作者继续编辑、修改和扩展的中间稿。

因此，本 Schema 的设计目标是：

1. 让输出结果对作者可读、可改。
2. 让输出结果对程序可校验、可继续处理。
3. 保留小说章节与剧本场景之间的对应关系。
4. 强制 AI 输出完整的剧本结构，而不是普通摘要。
5. 为后续扩展 Word 导出、PDF 导出、分场表、人物表和拍摄计划留下空间。

---

## 2. 顶层结构

剧本 YAML 的顶层结构如下：

```yaml
schema_version: "1.0"
project: {}
characters: []
locations: []
acts: []
adaptation_notes: []
```

顶层字段说明：

| 字段名 | 类型 | 是否必填 | 说明 |
|---|---|---:|---|
| `schema_version` | string | 是 | Schema 版本号，当前固定为 `"1.0"` |
| `project` | object | 是 | 项目信息，包括标题、类型、原小说来源 |
| `characters` | array | 是 | 人物表 |
| `locations` | array | 是 | 地点表 |
| `acts` | array | 是 | 剧本主体，按照“幕 → 场景”组织 |
| `adaptation_notes` | array | 是 | 整体改编说明和后续修改建议 |

### 设计原因

顶层结构采用“项目资料 + 人物 + 地点 + 幕场结构 + 改编说明”的形式，而不是简单地把小说章节逐段总结。

原因是剧本创作不仅需要情节，还需要人物、场景、动作、对白和戏剧目的。这样的结构可以让作者快速获得一个可编辑的剧本骨架。

---

## 3. `schema_version`

示例：

```yaml
schema_version: "1.0"
```

字段要求：

| 字段名 | 类型 | 约束 |
|---|---|---|
| `schema_version` | string | 当前固定为 `"1.0"` |

### 设计原因

`schema_version` 用于标记当前 YAML 结构版本。

未来如果工具增加新字段，例如镜头设计、预算标签、角色关系图、拍摄难度等，可以升级到：

```yaml
schema_version: "1.1"
```

这样旧版本文件和新版本文件可以被程序区分处理。

---

## 4. `project`

示例：

```yaml
project:
  title: "雾城来信"
  logline: "一封匿名信把主角带回旧案现场。"
  genre: "悬疑"
  target_format: "web_drama"
  source:
    chapter_count: 3
    chapter_titles:
      - "第1章 雨夜来信"
      - "第2章 旧站台"
      - "第3章 录音里的名字"
```

字段说明：

| 字段名 | 类型 | 是否必填 | 说明 |
|---|---|---:|---|
| `title` | string | 是 | 剧本项目标题 |
| `logline` | string | 是 | 一句话故事简介 |
| `genre` | string | 是 | 类型，例如悬疑、剧情、爱情、科幻等 |
| `target_format` | string | 是 | 目标剧本形式 |
| `source` | object | 是 | 原小说来源信息 |

`target_format` 的推荐取值包括：

```yaml
feature_film
short_film
web_drama
tv_episode
stage_play
audio_drama
other
```

`source` 字段说明：

| 字段名 | 类型 | 是否必填 | 说明 |
|---|---|---:|---|
| `chapter_count` | integer | 是 | 原小说章节数量，至少为 3 |
| `chapter_titles` | array | 是 | 原小说章节标题列表 |

### 设计原因

`project` 用于保存剧本项目的整体信息。

其中 `source.chapter_count` 和 `source.chapter_titles` 很重要，因为本工具的输入是小说章节。保留原章节信息可以让作者知道剧本初稿来自哪些章节，也方便后续检查是否遗漏原文内容。

---

## 5. `characters`

示例：

```yaml
characters:
  - id: "CHAR_001"
    name: "林澈"
    role: "protagonist"
    description: "收到匿名信的青年。"
    arc: "从逃避过去到主动追查真相。"
```

字段说明：

| 字段名 | 类型 | 是否必填 | 说明 |
|---|---|---:|---|
| `id` | string | 是 | 人物编号，例如 `CHAR_001` |
| `name` | string | 是 | 人物名称 |
| `role` | string | 是 | 人物功能 |
| `description` | string | 是 | 人物简介 |
| `arc` | string | 是 | 人物弧光或变化过程 |

`role` 的推荐取值包括：

```yaml
protagonist
antagonist
supporting
mentor
love_interest
comic_relief
other
```

### 设计原因

剧本不是小说摘要。剧本需要清楚说明人物在故事中的功能。

所以人物字段不仅保存名字，还保存：

```text
人物功能
人物简介
人物变化
```

这样作者可以快速判断角色是否有行动目标、是否承担戏剧冲突、是否有成长或转变。

---

## 6. `locations`

示例：

```yaml
locations:
  - id: "LOC_001"
    name: "旧站台"
    description: "十年前事件发生的核心地点。"
```

字段说明：

| 字段名 | 类型 | 是否必填 | 说明 |
|---|---|---:|---|
| `id` | string | 是 | 地点编号，例如 `LOC_001` |
| `name` | string | 是 | 地点名称 |
| `description` | string | 是 | 地点说明 |

### 设计原因

影视剧本与小说不同，剧本必须考虑空间和场景。

把地点单独提取出来有几个好处：

1. 作者可以快速看到故事主要发生在哪里。
2. 后续可以扩展成拍摄地点表。
3. 后续可以统计场景数量和拍摄难度。
4. 同一地点可以在多个场景中复用。

---

## 7. `acts`

示例：

```yaml
acts:
  - act_number: 1
    title: "第一幕：事件触发与悬念建立"
    purpose: "建立人物处境、核心悬念和主角的初始行动方向。"
    scenes: []
```

字段说明：

| 字段名 | 类型 | 是否必填 | 说明 |
|---|---|---:|---|
| `act_number` | integer | 是 | 第几幕，从 1 开始 |
| `title` | string | 是 | 幕标题 |
| `purpose` | string | 是 | 这一幕的戏剧功能 |
| `scenes` | array | 是 | 场景列表 |

### 设计原因

小说通常按章节组织，但剧本更常按戏剧结构组织。

使用 `acts` 可以把小说章节转换成更适合剧本创作的结构。例如：

```text
第一幕：建立人物和悬念
第二幕：冲突升级
第三幕：真相揭示和选择
```

当前工具的 demo 模式可以采用“一章对应一场”的简单策略；AI 模式则可以把一个章节拆成多个场景，或者把多个章节合并成一个场景。

---

## 8. `scenes`

示例：

```yaml
scenes:
  - scene_id: "S001"
    title: "雨夜来信"
    source_chapters: [1]
    heading:
      int_ext: "INT"
      location: "出租屋"
      time: "夜"
    synopsis: "林澈在雨夜收到一封没有署名的信。"
    purpose: "用匿名信触发主角行动。"
    beats:
      - "林澈回到出租屋"
      - "发现门缝里的匿名信"
      - "读到十年前站台的提示"
    action: "雨水拍打窗户。林澈推门进屋，发现门缝里夹着一封信。"
    dialogue:
      - character: "林澈"
        parenthetical: "低声"
        line: "十年前的站台？你到底是谁？"
    transition: "CUT TO:"
    revision_notes:
      - "可以增加信纸上的视觉符号，让悬念更强。"
```

字段说明：

| 字段名 | 类型 | 是否必填 | 说明 |
|---|---|---:|---|
| `scene_id` | string | 是 | 场景编号，例如 `S001` |
| `title` | string | 是 | 场景标题 |
| `source_chapters` | array | 是 | 该场景来源于原小说哪些章节 |
| `heading` | object | 是 | 场景头 |
| `synopsis` | string | 是 | 场景梗概 |
| `purpose` | string | 是 | 场景戏剧目的 |
| `beats` | array | 是 | 场景节拍 |
| `action` | string | 是 | 可拍摄的动作描写 |
| `dialogue` | array | 是 | 对白列表 |
| `transition` | string | 是 | 转场方式 |
| `revision_notes` | array | 是 | 修改建议 |

### 设计原因

`scenes` 是整个 YAML Schema 的核心。

小说文本往往包含大量叙述、心理描写和背景信息，而剧本需要转化为：

```text
场景
动作
对白
冲突
节拍
转场
```

因此每个场景都需要 `purpose` 和 `beats`。这样可以防止 AI 只是复述小说，而是让它明确：

```text
这一场戏为什么存在？
这一场戏如何推动剧情？
这一场戏给下一场留下什么问题？
```

---

## 9. `source_chapters`

示例：

```yaml
source_chapters: [1, 2]
```

### 设计原因

`source_chapters` 是小说转剧本任务中非常关键的字段。

它解决的是“可追溯性”问题：

```text
这个剧本场景来自原小说哪一章？
```

这样作者可以方便地对照原文检查：

1. 是否遗漏了重要情节。
2. 是否错误合并了章节。
3. 是否把某一章改编得过度。
4. 是否需要补充或删减场景。

在 demo 模式中，通常是一章对应一场：

```yaml
source_chapters: [1]
```

在 AI 模式中，一个场景也可以来自多个章节：

```yaml
source_chapters: [2, 3]
```

---

## 10. `heading`

示例：

```yaml
heading:
  int_ext: "INT"
  location: "出租屋"
  time: "夜"
```

字段说明：

| 字段名 | 类型 | 是否必填 | 说明 |
|---|---|---:|---|
| `int_ext` | string | 是 | 内景或外景 |
| `location` | string | 是 | 场景地点 |
| `time` | string | 是 | 时间 |

`int_ext` 的允许值：

```yaml
INT
EXT
INT/EXT
```

### 设计原因

`heading` 对应传统剧本中的场景标题，例如：

```text
INT. 出租屋 - 夜
EXT. 旧站台 - 清晨
```

它可以帮助作者快速判断每场戏的拍摄环境。

---

## 11. `dialogue`

示例：

```yaml
dialogue:
  - character: "林澈"
    parenthetical: "低声"
    line: "十年前的站台？你到底是谁？"
```

字段说明：

| 字段名 | 类型 | 是否必填 | 说明 |
|---|---|---:|---|
| `character` | string | 是 | 说话人物 |
| `parenthetical` | string | 是 | 语气、动作或状态说明，可以为空字符串 |
| `line` | string | 是 | 对白内容 |

### 设计原因

小说改编剧本时，一个关键难点是把叙述性文字改成对白和动作。

所以本 Schema 强制 `dialogue` 使用结构化形式，而不是把对白混在 `action` 里。这样后续可以很容易扩展为标准剧本格式。

---

## 12. `adaptation_notes`

示例：

```yaml
adaptation_notes:
  - "保留原小说的悬疑线。"
  - "把小说叙述改成可拍摄的动作和对白。"
```

### 设计原因

AI 生成的剧本初稿通常不应该被视为最终稿。`adaptation_notes` 用于记录整体改编建议，例如：

1. 哪些情节被合并。
2. 哪些人物关系需要加强。
3. 哪些场景需要补充视觉细节。
4. 哪些对白需要进一步打磨。

这让作者可以把 AI 输出当作可继续修改的创作材料。

---

## 13. 完整 YAML 示例

下面是一个简化后的完整示例：

```yaml
schema_version: "1.0"
project:
  title: "雾城来信"
  logline: "一封匿名信把主角带回旧案现场。"
  genre: "悬疑"
  target_format: "web_drama"
  source:
    chapter_count: 3
    chapter_titles:
      - "第1章 雨夜来信"
      - "第2章 旧站台"
      - "第3章 录音里的名字"
characters:
  - id: "CHAR_001"
    name: "林澈"
    role: "protagonist"
    description: "收到匿名信的青年。"
    arc: "从逃避过去到主动追查真相。"
locations:
  - id: "LOC_001"
    name: "出租屋"
    description: "主角收到匿名信的地方。"
acts:
  - act_number: 1
    title: "第一幕：事件触发"
    purpose: "建立主角处境和核心悬念。"
    scenes:
      - scene_id: "S001"
        title: "雨夜来信"
        source_chapters: [1]
        heading:
          int_ext: "INT"
          location: "出租屋"
          time: "夜"
        synopsis: "林澈收到一封没有署名的信。"
        purpose: "触发主角行动。"
        beats:
          - "林澈回家"
          - "发现匿名信"
          - "决定前往旧站台"
        action: "林澈推门进屋，雨水顺着伞尖落在地板上。他看到门缝里的信。"
        dialogue:
          - character: "林澈"
            parenthetical: "低声"
            line: "十年前的站台？"
        transition: "CUT TO:"
        revision_notes:
          - "可以补充信件上的视觉线索。"
adaptation_notes:
  - "后续可以强化人物动机。"
```

---

## 14. 为什么选择 YAML

本项目选择 YAML 作为最终输出格式，而不是直接输出纯文本剧本，原因如下：

1. YAML 比 JSON 更适合人阅读和编辑。
2. YAML 可以保留清晰的层级结构。
3. YAML 方便作者手动修改。
4. YAML 可以被程序重新读取和校验。
5. YAML 适合作为后续导出 Word、PDF、分场表的中间格式。

程序内部仍然使用 Python 字典和 JSON Schema 做校验，最后再导出 YAML。这样可以同时保证：

```text
程序稳定性
作者可编辑性
```

---

## 15. 为什么需要 Schema 校验

如果完全依赖 AI 输出，可能出现以下问题：

1. 缺少必填字段。
2. 字段名不一致。
3. 把数字写成字符串。
4. 场景没有来源章节。
5. 人物表为空。
6. 输出了一段解释文字而不是结构化剧本。

因此，本项目在生成 YAML 之前会先调用：

```python
validate_screenplay(data)
```

校验内容包括：

1. 顶层字段是否完整。
2. 每个对象是否包含必填字段。
3. 是否出现 Schema 以外的字段。
4. `chapter_count` 是否至少为 3。
5. `source_chapters` 是否引用了存在的章节。
6. `scene_id`、`CHAR_001`、`LOC_001` 等编号格式是否正确。

只有通过校验的数据才会被导出为 YAML。

---

## 16. 当前 Schema 的边界

当前 Schema 主要面向“剧本初稿生成”，不是完整的影视工业制片系统。

它暂时不包含：

1. 镜头号。
2. 分镜图。
3. 预算。
4. 拍摄周期。
5. 演员档期。
6. 服化道清单。
7. 版权合同信息。

这些内容可以在后续版本中扩展。

---

## 17. 后续可扩展方向

未来可以在保持兼容的基础上增加：

```yaml
shots: []
props: []
costumes: []
music_cues: []
production_notes: []
estimated_duration: ""
```

也可以新增导出功能：

1. YAML 转 Word 剧本。
2. YAML 转 PDF 剧本。
3. YAML 转人物关系表。
4. YAML 转分场表。
5. YAML 转拍摄计划表。

---

## 18. 总结

本 YAML Schema 的核心思想是：

```text
用结构化方式连接小说章节和剧本场景。
```

它既保留小说来源，又强制输出剧本所需的基本元素：

```text
人物
地点
幕
场景
动作
对白
节拍
改编建议
```

因此，它适合作为 AI 小说转剧本工具的稳定中间格式，也方便作者在初稿基础上继续创作。