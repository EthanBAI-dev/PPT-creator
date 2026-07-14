# Accumulate-PPTs

🌐 [中文](#) · [English](README.en.md)

> **「AI 打一句话,一份能直接讲的论文 PPT 落地。」**
> *Type one sentence. Get a presentation-ready paper deck.*

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![GitHub Pages](https://img.shields.io/badge/Demo-GitHub%20Pages-success)](https://luoqianshi.github.io/Accumulate-PPTs/)
[![Skills](https://img.shields.io/badge/Agent%20Skills-3-purple)](#-能力矩阵)
[![PRs Welcome](https://img.shields.io/badge/PRs-welcome-brightgreen.svg)](#-贡献)
[![Made with HTML](https://img.shields.io/badge/Made%20with-HTML5%20%2B%20Vanilla%20JS-orange)]()

<p align="center">
  <img src="assets/accmulate-ppts.png" alt="Accumulate-PPTs" width="85%">
</p>

---

## 30 秒看懂

`Accumulate-PPTs` 是面向**研究生与高校大学生**的 HTML 幻灯片工作流仓库,把"读论文 → 做汇报 → 答辩演练"这条最常见的痛点路径,封装成 3 个可被 AI Agent 直接调用的 SKILL。你给一句中文 prompt,Agent 就能在 5–20 分钟内产出一份苹果风/Notion 风的单文件 HTML 演示文稿,既能浏览器直接放映,也能嵌入个人主页长期展示。

- 论文精读 / 答辩组会:用 `html-paper-slides`
- 学生干部述职 / 社团汇报:用 `html-work-report-slides`
- 通用主题分享:用 `html-slides`

**和 PowerPoint / Gamma / Notion Slides 的本质差异**:我们交付的是**离线单文件 HTML**,在 AI Agent 工作流中可重复、可版本管理、可一键部署到 GitHub Pages 形成个人作品集。

---

## 立即试用

```bash
git clone https://github.com/luoqianshi/Accumulate-PPTs.git
cd Accumulate-PPTs
```

用 Claude Code / TRAE / CodeBuddy 等任意支持 Skills 的 AI IDE 打开,然后把这句话发给 Agent:

```markdown
请你使用 html-paper-slides 技能(skills\html-paper-slides\SKILL.md),
帮我为 ./raw/my-paper.pdf 制作一份 HTML 格式的论文汇报 PPT,
最终文件存放在 paper-slides 目录下。
```

5–15 分钟后,`paper-slides/` 下会出现一份可浏览器放映的单文件 HTML 演示文稿,首页会通过 `index.html` 自动收录到演示画廊中。

---

## 能力矩阵

仓库内置 3 个 SKILL,覆盖研究生与大学生最常见的三类汇报场景:

| SKILL | 典型场景 | 输入 | 交付物 | 典型耗时 |
|------|----------|------|--------|----------|
| [`html-paper-slides`](skills/html-paper-slides/SKILL.md) | 论文精读 · 答辩组会 · 研究进展汇报 | 一篇 PDF 论文 | 单文件 HTML deck + 首屏缩略图 | 8–15 min |
| [`html-work-report-slides`](skills/html-work-report-slides/SKILL.md) | 学生干部述职 · 社团/部门年度总结 · 班委汇报 | Markdown 大纲 / 草稿 | 苹果风 / Notion 风单文件 HTML | 10–20 min |
| [`html-slides`](skills/html-slides/SKILL.md) | 课程展示 · 读书分享 · 通用主题 | Markdown / 自由文本 | 通用 HTML 幻灯片 | 5–15 min |

所有产出统一为**离线单文件 HTML**:无外部依赖、可直接 `open file://` 播放、键盘翻页、淡入动画、CSS Grid 响应式排版,适合 GitHub Pages / Vercel / Netlify 一键部署。

---

## Showcase · 真实论文 PPT 演示

下面 7 份演示文稿均使用 `html-paper-slides` 在 AI Agent 协助下完成,可直接点击预览:

<table>
  <tr>
    <td align="center" width="50%">
      <a href="paper-slides/Attention_Is_All_You_Need.html">
        <img src="assets/thumbnails/Attention_Is_All_You_Need.png" alt="Attention Is All You Need" width="100%">
      </a>
      <br><b>Attention Is All You Need</b>
      <br><sub>Transformer 经典论文 · 多头自注意力 · 机器翻译 SOTA</sub>
    </td>
    <td align="center" width="50%">
      <a href="paper-slides/DETRs_Beat_YOLOs_on_Real-time_Object_Detection.html">
        <img src="assets/thumbnails/DETRs_Beat_YOLOs_on_Real-time_Object_Detection.png" alt="RT-DETR" width="100%">
      </a>
      <br><b>DETRs Beat YOLOs on Real-time Object Detection</b>
      <br><sub>CVPR 2024 Oral · RT-DETR · 端到端实时检测</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <a href="paper-slides/YOLO-Master_Presentation.html">
        <img src="assets/thumbnails/YOLO-Master_Presentation.png" alt="YOLO-Master" width="100%">
      </a>
      <br><b>YOLO-Master: MoE-Accelerated YOLO</b>
      <br><sub>专业化解码器 · MoE 加速 · 实时检测</sub>
    </td>
    <td align="center" width="50%">
      <a href="paper-slides/YOLOv12_Attention-Centric.html">
        <img src="assets/thumbnails/YOLOv12_Attention-Centric.png" alt="YOLOv12" width="100%">
      </a>
      <br><b>YOLOv12: Attention-Centric Real-Time Detectors</b>
      <br><sub>Area Attention · R-ELAN · 注意力中心化</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <a href="paper-slides/YOLO26_Unified_Real-Time_Vision.html">
        <img src="assets/thumbnails/YOLO26_Unified_Real-Time_Vision.png" alt="YOLO26" width="100%">
      </a>
      <br><b>Ultralytics YOLO26: Unified Real-Time Vision</b>
      <br><sub>DFL-free · MuSGD · 多任务统一</sub>
    </td>
    <td align="center" width="50%">
      <a href="paper-slides/smooth-tail_learning.html">
        <img src="assets/thumbnails/smooth-tail_learning.png" alt="smooth-tail" width="100%">
      </a>
      <br><b>Boosting Long-tailed Object Detection</b>
      <br><sub>ICCV 2023 · 平滑尾部 · 逐步学习</sub>
    </td>
  </tr>
  <tr>
    <td align="center" width="50%">
      <a href="paper-slides/Dialogue_Director.html">
        <img src="assets/thumbnails/Dialogue_Director.png" alt="Dialogue Director" width="100%">
      </a>
      <br><b>Dialogue Director</b>
      <br><sub>对话可视化 · 三智能体 · 电影知识整合</sub>
    </td>
    <td align="center" width="50%">
      <i>更多论文演示持续更新中 · 见 <a href="https://luoqianshi.github.io/Accumulate-PPTs/">在线画廊</a></i>
    </td>
  </tr>
</table>

> 在线画廊:https://luoqianshi.github.io/Accumulate-PPTs/

---

## 核心工作流:raw → ingest → HTML PPT

本仓库的差异化在于把"论文精读"和"演示文稿生成"统一到一条**可复现、可版本化**的工作流上:

```
┌──────────┐    ┌──────────┐    ┌────────────────┐
│   raw    │ →  │  ingest  │ →  │  HTML PPT      │
│ 原始材料 │    │ 结构化MD │    │ 单文件HTML演示 │
└──────────┘    └──────────┘    └────────────────┘
  PDF / 网页       信息卡 +        paper-slides/
  补充材料          重点摘要         output/
                   汇报大纲
```

### 1. `raw/` —— 原始材料归档
保存论文 PDF、补充材料、网页链接、作者信息、数据集说明、代码仓库地址和临时摘录。不追求排版,只要求材料完整、来源清晰、文件命名可追踪。建议按论文主题或文件名保存,并记录标题、年份、会议/期刊、作者、论文链接、代码链接、数据来源。

### 2. `ingest/` —— Markdown 重点提取
论文理解与内容压缩的核心层。将 `raw/` 中的材料整理为结构化 Markdown,重点提取:**研究问题与动机、核心贡献、方法框架、关键模块、实验设置、核心指标、消融结论、可视化证据、局限性、可复现实践**和**适合放进 PPT 的讲述主线**。每份中间稿应形成"论文信息卡 + 重点摘要 + 方法拆解 + 实验结论 + 汇报大纲"结构,便于直接转为 HTML PPT。

### 3. `HTML PPT` —— 演示成品入库
将 `ingest/` 的结构化内容转化为单文件演示文稿。论文类成品优先放入 `paper-slides/`,课程、练习或通用内容可放入 `output/`。生成时应保留清晰的章节流:**封面 → 摘要 → 引言 → 方法 → 实验 → 消融 → 结论与展望**,并通过卡片、流程图、对比表、指标高亮、导航控件强化阅读节奏。成品入库后,**必须同步更新 `slides-manifest.json`**,确保 `index.html` 画廊可以正确展示标题、路径、简介、类型与主题色。随后运行 `python skills/html-paper-slides/scripts/generate-thumbnails.py` 生成首屏缩略图,画廊卡片便会直接展示真实幻灯片封面。

### 质量检查清单
在进入下一阶段前建议确认:
- `raw/` 是否可追溯到原始来源
- `ingest/` 是否已经提炼出足够支撑 8–15 页汇报的主线
- HTML PPT 是否可以单文件打开、键盘翻页、视觉层级清晰
- `slides-manifest.json` 是否覆盖 `paper-slides/` 下的全部 HTML 文件
- `assets/thumbnails/` 是否已包含对应缩略图且 `thumbnail` 字段已正确写入 manifest

---

## 项目结构

```
Accumulate-PPTs/
├── index.html            # HTML Slides Gallery 导航页(由 GitHub Pages 自动部署)
├── slides-manifest.json  # paper-slides 演示文稿清单
├── README.md             # 中文 README(默认)
├── README.en.md          # 英文 README
├── LICENSE               # MIT 协议
├── paper-slides/         # 论文精读、答辩与研究汇报类 HTML PPT 成品
│   ├── Attention_Is_All_You_Need.html
│   ├── DETRs_Beat_YOLOs_on_Real-time_Object_Detection.html
│   └── ... (更多论文演示)
├── skills/               # 幻灯片制作技能、脚本与模板文档
│   ├── html-paper-slides/        # 论文精读 / 答辩汇报场景
│   │   ├── SKILL.md
│   │   ├── scripts/
│   │   │   ├── pdf_extractor.py   # 从论文 PDF 中提取核心配图
│   │   │   └── generate-thumbnails.py  # 为 HTML 幻灯片生成首屏缩略图
│   │   └── templates/
│   │       └── presentation.html  # 论文汇报场景专用 HTML 幻灯片模板
│   ├── html-work-report-slides/  # 学生工作述职 / 社团汇报场景
│   │   └── SKILL.md
│   └── html-slides/              # 通用 HTML 幻灯片制作技能
│       ├── SKILL.md
│       └── templates/
│           └── presentation.html
├── assets/               # 通用静态资源
│   ├── thumbnails/       # HTML 幻灯片首屏缩略图(自动生成)
│   ├── design-prompts/   # 风格设计提示词集合
│   ├── accmulate-ppts.png
│   └── favicon.png
├── raw/                  # 原始论文与素材,保留 PDF 等一手资料
├── ingest/               # 摄取后的 Markdown 中间稿与提取素材
└── output/               # 通用 HTML PPT 输出区,适合草稿、课程或非论文类演示
```

---

## 快速开始

### 1. 准备环境

```bash
git clone https://github.com/luoqianshi/Accumulate-PPTs.git
cd Accumulate-PPTs
```

- 删除 `paper-slides/` 目录下的所有 `.html` 文件
- 将 `slides-manifest.json` 文件中的 `slides` 数组清空(以上为作者个人使用数据)
- (可选)安装缩略图生成依赖:`pip install playwright && playwright install chromium`

### 2. 选择场景,启动 AI Agent

用 `Claude Code` / `TRAE` / `CodeBuddy` 等 AI IDE 打开当前项目。

**论文汇报场景:**

```markdown
请你使用 html-paper-slides 技能(skills\html-paper-slides\SKILL.md),
帮我为 [给定你要制作的 PDF 格式的论文的文件路径] 制作一份
HTML 格式的 PPT,最终文件存放在 paper-slides 目录下。
```

**学生工作述职场景:**

```markdown
请你使用 html-work-report-slides 技能(skills\html-work-report-slides\SKILL.md),
帮我制作一份 HTML 格式的学生工作述职报告 PPT,最终文件存放在 output 目录下。
```

**通用主题场景:**

```markdown
请你使用 html-slides 技能(skills\html-slides\SKILL.md),
围绕 [给定主题] 制作一份 HTML 格式的演示文稿。
```

### 3. 生成缩略图,自动收录到画廊

```bash
python skills/html-paper-slides/scripts/generate-thumbnails.py
```

完成后,新的 HTML PPT 会以**真实首屏封面**出现在 `index.html` 画廊中。推送至 GitHub 后,GitHub Actions 会自动部署至 GitHub Pages。

---

## 技术栈

- **HTML5 + CSS3** —— 演示文稿主体
- **Vanilla JavaScript** —— 分页引擎、键盘交互、淡入动画(无框架依赖)
- **CSS Grid / Flexbox** —— 16:9 响应式布局
- **CSS Variables** —— 主题色与字体变量化管理
- **Google Fonts** —— Noto Sans SC(中文)+ Inter(英文/数字)
- **Playwright (Python)** —— 自动生成 HTML PPT 首屏缩略图
- **GitHub Actions** —— 自动部署 `index.html` 至 GitHub Pages

---

## 与同类方案对比

| 维度 | PowerPoint | Gamma | Notion Slides | **Accumulate-PPTs** |
|------|-----------|-------|---------------|---------------------|
| 上手成本 | 中等(需学排版) | 低(网页拖拽) | 低(Notion 内) | **一句话**(对 Agent 说话) |
| 论文配图自动提取 | 不支持 | 不支持 | 不支持 | **支持**(`pdf_extractor.py`) |
| AI Agent 工作流 | 需手动配合 | 半自动 | 不支持 | **原生支持** |
| 离线单文件 | `.pptx` | 仅网页 | 仅网页 | **单文件 HTML** |
| 版本管理 / 复现 | 一般 | 困难 | 困难 | **Git 友好** |
| 部署成本 | Microsoft 365 | 订阅 | Notion | **GitHub Pages 免费** |
| 可定制模板 | 完全自由 | 受限 | 受限 | **完全自由(纯 HTML/CSS)** |
| 商用 License | 订阅制 | 订阅制 | 订阅制 | **MIT 完全开源** |

> **定位金句**:PowerPoint 是图形工具,Gamma 是 AI 网页产品,Accumulate-PPTs 是 **"让图形工具这层消失"** 的 Agent 技能。

---

## Limitations · 当前局限

我们追求 80 分的稳定可用,而非 100 分的完美:

1. **PDF 配图存在冗余提取**:首版生成后建议手动删除冗余图片,后续会引入视觉语言模型做精选
2. **多模态模型效果更佳**:推荐使用 KIMI K2.6、Minimax M3等原生多模态模型,纯文本模型会丢失论文配图
3. **当前版本为高质量初稿**:建议在初稿生成后与 Agent 进行多轮对话精修,例如"第 5 页方法图换成架构图" / "页脚加学校 logo"
4. **不直接从 LaTeX 源生成**:若需 LaTeX 高保真,请使用 Beamer;本仓库主打"用 PDF/Markdown 就能上手"
5. **缩略图依赖 Playwright**:首次运行需 `pip install playwright && playwright install chromium`,无图形环境(headless 服务器)需补 `--with-deps` 步骤

---

## License

本项目以 **MIT 协议**完全开源,个人和商用均免费,无需事先授权。
详见 [LICENSE](LICENSE) 文件。
---

## 致谢

- [html-presentation](https://github.com/juanjuanjie/html-presentation) —— 原始 HTML 幻灯片模板与播放引擎参考仓库
- [Claude Code](https://claude.com/claude-code) · [CodeBuddy](https://www.codebuddy.ai/) · [TRAE](https://www.trae.ai/) —— AI Agent 平台
- 所有开源论文作者与开源社区

---

## 联系方式

欢迎 Star、Fork、提 Issue 与 PR。如希望交流研究生学习 / 论文阅读 / Agent 工作流,可通过以下渠道找到我:

| 平台 | 账号 / 链接 |
|------|------------|
| GitHub | [@luoqianshi](https://github.com/luoqianshi) |
| 在线画廊 | [luoqianshi.github.io/Accumulate-PPTs](https://luoqianshi.github.io/Accumulate-PPTs/) |

---

## Star History

如果这个仓库对你有帮助,欢迎点一个 Star 支持我们继续迭代:

<a href="https://star-history.com/#luoqianshi/Accumulate-PPTs&Date">
  <img src="https://api.star-history.com/svg?repos=luoqianshi/Accumulate-PPTs&type=Date" alt="Star History Chart" width="600">
</a>

---

*Last Updated: 2026-06-13 · v1.0 · 累计收录论文演示 7 份*
