---
name: "html-work-report-slides"
description: "学生工作述职报告PPT、干部述职、社团汇报、班委汇报、学生会年度总结、部门工作报告、HTML演示文稿、年终述职、任期总结、学生组织述职汇报PPT"
---

# HTML 演示文稿生成器

生成苹果风/Notion 风的 HTML 演示文稿，用于学生干部述职、社团/部门年度工作汇报、班委总结等学生组织场景。

---

## 核心样式规范（必须严格遵循）

### 配色方案
| 用途 | 颜色值 | 说明 |
|------|--------|------|
| 主背景色 | `#ffffff` | 纯白色 |
| 主文字色 | `#000000` | 纯黑色 |
| 标题文字色 | `#3966A2` | 微深蓝色 |
| 强调文字色 | `#132843` | 深蓝色 |
| 次要文字色 | `#6191D3` | 浅蓝色 |

### 字体规范
```
系统字体优先（零外部依赖）：
font-family: 'Inter', 'Noto Sans SC', -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif
标题权重: 700-800
正文权重: 400-500
```

### 布局规范
- 页面比例: 16:9（padding: 5vh 7vw）
- 使用 CSS Grid/Flexbox 弹性布局
- 字号使用 clamp() 响应式缩放

---

## HTML 模板

### 必需组件
1. **Slide Engine** — 分页切换逻辑
2. **Progress Bar** — 顶部进度条（体现汇报节奏）
3. **Dots** — 右侧导航点
4. **Animations** — 淡入动画（`.anim:nth-child(n)` 递增延迟）

### 可复用组件
| 组件 | 类名 | 述职场景用途 |
|------|------|------|
| 卡片 | `.card`, `.card-grid` | 工作项目/成果展示块 |
| 徽章 | `.badge` | 职位标签、学期/年度标注 |
| 高亮条 | `.highlight-bar` | 核心数据/关键成就强调 |
| 对比栏 | `.vs-col` | 目标 vs 完成、上期 vs 本期对比 |
| 步骤流 | `.steps .step` | 工作推进时间线、流程复盘 |
| 引用框 | `.quote-block` | 成员/用户反馈金句、领导评价摘录 |
| 圆圈图 | `.ipo-circle` | 输入—过程—产出（IPO）工作模型 |
| 列表 | `.bullet-list li::before` | 工作清单、问题清单、计划清单 |
| 数据大字 | `.stat-number` | 活动场次、参与人数、满意度等核心数字 |
| 发光效果 | `.glow .glow-purple/.glow-yellow` | 封面/过渡页装饰背景 |
| 封面元数据 | `.cover-tag` | 职位、任期、学院/组织名称标注 |
| 图标 | `.icon` | 64×64 白色图标 |

> **述职报告数据可视化原则**：核心数字优先用 `.stat-number` 大字显示，辅以 `.highlight-bar` 作对比说明；避免在单张幻灯片堆砌超过 2 组数据对比。

---

## 工作流程

1. **理解述职材料**：收集汇报人提供的工作记录、数据报表、活动照片等原始素材，整理形成结构化草稿 `述职人_述职报告.md`，重点提炼：任期概览、核心成果数据、典型案例、问题与反思、下期规划。
2. **内容规划**：根据分页规划建议，将内容拆分为 **12～20 页**，每页聚焦单一叙事焦点，遵循"结论先行——数据支撑——案例佐证"的逻辑顺序。
3. **结构设计**（见下方分页规划建议）
4. **填充内容**：根据模板组件填充具体内容，数据型内容优先用卡片+大字展示，叙述型内容用高亮条+列表展示，反思型内容用引用框展示。
5. **预览调整**：生成后检查视觉节奏——封面→总览→正文→收尾应形成清晰的"开门见山→言之有据→有始有终"叙事弧。
6. **输出文件**：使用 `write_to_file` 工具保存为 `.html` 文件至当前工作区。

---

## 分页规划建议

> 述职报告的核心逻辑：**我做了什么（事实）→ 做得怎样（数据）→ 为什么这样做（思考）→ 接下来怎么做（规划）**。结构应服务于这条主线，切忌流水账式罗列。

| 位置 | 页面主题 | 内容要点 | 建议页数 |
|------|---------|---------|---------|
| **封面** | 述职报告封面 | 报告标题 + 述职人姓名 + 职位/部门 + 任期区间 + 学院/组织全称 | 1 页 |
| **目录** | 汇报框架总览 | 用模块化卡片或步骤流呈现全文四大板块，让听众建立预期 | 1 页 |
| **任期概览** | 一句话定义这段任期 | 用 1 句核心句描述任期主题，配 3～4 个关键数字（活动数/参与人次/获奖数等）以 `.stat-number` 大字展示 | 1 页 |
| **工作回顾** | 主要工作版块分述 | 按职能板块（如：活动策划 / 日常运营 / 对外联络）分组，每组用卡片网格呈现 2～4 项代表性工作，标注时间与成果 | 3～5 页 |
| **亮点案例** | 1～2 个典型项目深度复盘 | 用 IPO 圆圈图或步骤流复盘：背景→执行→成果，附核心数据与成员/用户反馈引用 | 1～2 页 |
| **数据成果** | 量化成果全景 | 用对比栏呈现目标 vs 完成、同期对比；用 `.highlight-bar` 标注超额完成或突破历史的项目 | 1～2 页 |
| **问题与反思** | 诚实的自我评估 | 结构化呈现 2～3 个不足之处，每项配"现象描述→原因分析→改进方向"三层结构，忌空洞检讨 | 1～2 页 |
| **下期规划** | 面向未来的承诺 | 分短期（下学期）/ 中期（任期末）两个时间维度，每维度 2～3 个可量化目标，使用步骤流或卡片展示 | 1～2 页 |
| **致谢/结尾** | 温度收尾 | 简洁感谢合作伙伴、指导老师、团队成员；可引用一句鼓励性的金句或团队口号作收尾 | 1 页 |

---

## 述职报告特有设计原则

1. **数字即信任**：每一项工作主张必须有数字支撑，无法量化的成果用时间线或案例代替；禁止出现"努力开展了""积极推动了"等无实质内容的表述。
2. **克制的情绪表达**：引用框 `.quote-block` 用于成员真实反馈，而非自我赞美；致谢页保持温暖克制，避免煽情。
3. **对比即成长**：数据成果页必须有参照系（目标值 / 上期值 / 行业均值），孤立数字无法说明问题。
4. **问题不回避**：问题与反思页是述职报告建立可信度的核心；结构化呈现问题比回避问题更能赢得听众信任。
5. **规划要可追踪**：下期规划中的目标应尽量 SMART 化（具体、可衡量、可实现、相关、有时限），便于下次述职对账。
6. **视觉节奏控制**：工作回顾页信息密度最高，前后应各有一页"呼吸页"（任期概览 / 亮点案例）作节奏缓冲。
7. **标题使用微深蓝色（#3966A2），关键数据/结论使用深蓝色（#132843）强调**。
8. **封面页使用 `.badge` + `.cover-tag` 标注职位与任期**，增加专业感与仪式感。
9. **保留左右键前后翻页功能，但不显示显式翻页控制器**。
10. **每页内容控制在 4～6 个信息单元以内，避免信息过载**。

---

## 生成命令

```html
<!-- 输出到当前工作区 -->
<!-- 使用 write_to_file 工具保存为 .html 文件 -->
```

---

## ⚠️ 已知问题 & 解决方案（必须遵循）

### 问题1：字体无法加载（404）
- **原因**：`<link>` 标签加载 Google Fonts，在 `file://` 协议下被浏览器安全策略拦截
- **解决**：使用纯系统字体 `font-family: 'Inter', 'Noto Sans SC', -apple-system, 'PingFang SC', 'Microsoft YaHei', sans-serif`，零外部依赖

### 问题2：翻页后内容空白
- **原因**：JS 用 `element.style.xxx = '...'` 设置 inline style 切换页面，但这些 inline style 无法被 CSS 正确覆盖，导致新页面保持 `opacity: 0`
- **解决**：
  1. CSS 的 `.slide.active` 三个关键属性必须加 `!important`：`opacity`、`visibility`、`transform`
  2. JS 翻页函数**禁止使用 inline style**，只操作 `classList.add/remove('active')` 和 `classList.add('exit-up')`，完全由 CSS transition 处理动画

---

## HTML转PPTX转换

### 转换原理

将 HTML 述职报告（`.slide` 结构）逐页解析为 python-pptx 的 `Slide` 对象。核心思路：

1. **读取 HTML + CSS**：分析每页 `.slide` 的布局结构（卡片网格、步骤流、时间线、数据大字等）
2. **布局映射**：HTML 布局 → PPTX 形状（矩形、圆角矩形、文本框、圆形）
3. **样式映射**：CSS 颜色/字号/间距 → python-pptx 的 `RGBColor` / `Pt` / `Inches`
4. **逐页构建**：每页调用 `prs.slides.add_slide()` 独立创建

### 关键步骤

```python
from pptx import Presentation
from pptx.util import Inches, Pt
from pptx.dml.color import RGBColor
from pptx.enum.text import PP_ALIGN
from pptx.enum.shapes import MSO_SHAPE

# 1. 创建 16:9 演示文稿
prs = Presentation()
prs.slide_width = Inches(13.333)
prs.slide_height = Inches(7.5)

# 2. 使用空白布局
slide = prs.slides.add_slide(prs.slide_layouts[6])

# 3. 绘制背景/形状
shape = slide.shapes.add_shape(MSO_SHAPE.ROUNDED_RECTANGLE, left, top, width, height)
shape.fill.solid()
shape.fill.fore_color.rgb = RGBColor(0xF8, 0xFA, 0xFD)

# 4. 添加文本框
txBox = slide.shapes.add_textbox(left, top, width, height)
tf = txBox.text_frame
p = tf.paragraphs[0]
p.text = "标题文字"
p.font.size = Pt(28)
p.font.color.rgb = RGBColor(0x39, 0x66, 0xA2)
p.font.bold = True
p.font.name = 'Microsoft YaHei'
```

### 组件映射表

| HTML 组件 | PPTX 实现 |
|-----------|----------|
| `.card` | `MSO_SHAPE.ROUNDED_RECTANGLE` + 文本框覆盖 |
| `.stat-number` | 大号 `Pt(36)` 文本框，颜色 `#132843`，居中对齐 |
| `.steps` | 多个圆角矩形 + `MSO_SHAPE.OVAL` 编号圆 + 文本框 |
| `.timeline` | 竖线矩形 + 小圆点 + 文本排列 |
| `.highlight-bar` | 圆角矩形背景 + 左侧细条 accent 线 |
| `.badge` | 小圆角矩形 `Pt(10-11)` + 居中文本 |
| `.cover` | `slide.background.fill` 深蓝 + 白色/浅蓝文本 |
| `.glow` | 大椭圆 `MSO_SHAPE.OVAL` 半透明填充 |

### 已知限制

1. **无动画**：pptx 不支持 CSS transition/animation，所有页面为静态快照
2. **无交互**：进度条、导航点、键盘/滚轮翻页均不适用
3. **渐变有限**：python-pptx 的渐变（`fill.gradient()`）实现复杂，`.step-num` 圆形使用纯色替代渐变
4. **圆角差异**：pptx 的 `ROUNDED_RECTANGLE` 圆角半径固定，无法精确匹配 CSS `border-radius`
5. **字体大小**：CSS `clamp()` 响应式字号只能取中间值近似为固定 `Pt`
6. **卡片悬停**：`.card:hover` 效果无法在静态 PPTX 中体现
7. **布局弹性**：CSS Grid/Flexbox 的弹性间距需手动计算为固定 `Inches` 值
8. **中文编码**：Python 脚本中包含中文文本时建议使用 Unicode 转义或确保文件 UTF-8 编码，避免语法解析错误

### 转换命令示例

```bash
# 生成 PPTX
python html_to_pptx.py

# 脚本入口
# input:  HTML 文件（硬编码路径或命令行参数）
# output: .pptx 文件，保存至 output 目录
```

### 质量评估标准

| 维度 | 评估 |
|------|------|
| 页面对应 | 100%（14/14 页 1:1 映射） |
| 内容完整性 | 高（所有文本、卡片、数据完整保留） |
| 配色一致性 | 高（#ffffff / #3966A2 / #132843 / #6191D3 精确匹配） |
| 布局还原度 | 中高（卡片网格、steps、timeline 结构保留，细节间距需微调） |
| 缺失项 | 动画/交互/渐变/弹性间距
