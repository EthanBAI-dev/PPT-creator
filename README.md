# PPT-creator

基于七角色协作的智能 PPT 生成与优化工具，支持主题生成、模板推荐、内容填充、AI 智能配图、文本润色和 PPTX 文件生成。适用于学术汇报、商业演示、培训课件、产品发布等多种场景。

## 功能特性

- **智能 PPT 生成**：通过七角色协作工作流，从零生成高质量 PPT
- **网页设计分析**：分析网页截图，提取设计系统（配色、排版、组件风格）
- **设计系统转换**：将网页设计分析结果转换为路演视频可用的品牌风格配置
- **多场景适配**：支持商业计划、学术汇报、产品发布、培训课件等多种场景
- **跨平台兼容**：支持 Windows / macOS / Linux，自动处理编码兼容性问题

## 环境要求

| 依赖 | 版本要求 |
|------|---------|
| Python | >= 3.9 |
| python-pptx | >= 0.6.21 |
| Pillow | >= 10.0.0 |
| requests | >= 2.31.0 |

## 快速开始

### 1. 克隆项目

```bash
git clone <repository-url>
cd PPT-creator
```

### 2. 安装依赖

```bash
pip install -r requirements.txt
```

### 3. 验证安装

```bash
python -c "from PIL import Image; from pptx import Presentation; import requests; print('All dependencies installed successfully')"
```

## 使用指南

### 生成 PPT 演示文稿

1. 准备 JSON 格式的 PPT 数据（参考 [内容结构规范](skills/01-ppt-generator/ppt-generator/references/ppt_structure_guide.md)）

2. 运行生成脚本：

```bash
python skills/01-ppt-generator/ppt-generator/scripts/generate_pptx.py \
  --input ./ppt_data.json \
  --output ./output/presentation.pptx
```

**参数说明**：
- `--input` / `-i`：输入 JSON 文件路径（必需）
- `--output` / `-o`：输出 PPTX 文件路径（必需）

### 分析网页设计

```bash
python skills/05-web-design-analyzer/web-design-analyzer/scripts/analyze_design.py \
  --image ./screenshot.png \
  --output ./output/design_system.json
```

**参数说明**：
- `--image`：网页截图文件路径（必需，支持 PNG/JPG/JPEG）
- `--model`：OpenAI 模型名称（可选，默认 gpt-4o）
- `--output`：输出 JSON 文件路径（可选，默认输出到终端）

> **注意**：使用此功能需要配置 OpenAI API Key，通过环境变量 `OPENAI_API_KEY` 或 `COZE_OPENAI_VISION_API_<skill_id>` 设置。

### 转换为路演品牌风格

```bash
python skills/05-web-design-analyzer/web-design-analyzer/scripts/convert_to_roadshow_style.py \
  --input ./design_system.json \
  --output ./output/brand_style.json
```

**参数说明**：
- `--input` / `-i`：设计系统 JSON 文件路径（必需）
- `--output` / `-o`：输出品牌风格 JSON 路径（默认 ./output/brand_style.json）

## 项目结构

```
PPT-creator/
├── skills/                                    # 技能模块（核心功能）
│   ├── 01-ppt-generator/                      # PPT 生成技能
│   │   └── ppt-generator/
│   │       ├── SKILL.md                       # 技能定义与工作流说明
│   │       ├── scripts/
│   │       │   └── generate_pptx.py           # PPTX 文件生成脚本
│   │       ├── references/
│   │       │   ├── ppt_structure_guide.md     # PPT 结构规范与数据格式
│   │       │   └── visual_design_guide.md     # AI 智能配图指南
│   │       └── assets/
│   │           └── ppt_templates/             # PPT 样式模板配置
│   │               └── README.md
│   └── 05-web-design-analyzer/                # 网页设计分析技能
│       └── web-design-analyzer/
│           ├── SKILL.md                       # 技能定义与使用说明
│           ├── scripts/
│           │   ├── analyze_design.py          # 网页设计分析脚本
│           │   └── convert_to_roadshow_style.py  # 路演风格转换脚本
│           └── references/
│               ├── api-spec.md                # OpenAI Vision API 规范
│               └── roadshow-export-guide.md   # 路演视频风格导出指南
│
├── project_content/                           # 项目内容目录（新增模块存放处）
│   └── README.md                              # 目录用途与存放规范
│
├── output/                                    # PPT 输出目录（生成文件统一存放处）
│   └── README.md                              # 输出文件说明与规范
│
├── docs/
│   ├── reference/
│   │   └── project_reference_template.md      # 通用项目参考手册模板
│   └── styles/
│       ├── README.md                          # PPT 视觉风格总览
│       ├── dark-tech.html                     # 深色科技风 配色参考
│       ├── warm-elegant.html                  # 暖色系 配色参考
│       ├── mint-fresh.html                    # 薄荷清新风 配色参考
│       ├── cyber-neon.html                    # 霓虹赛博风 配色参考
│       └── minimal-clean.html                 # 极简纯净风 配色参考
│
├── ai-agent/
│   └── ppt-generation-blueprint.json          # AI Agent 标准化执行指令
│
├── assets/
│   └── style-previews/                        # PPT 风格预览 SVG 图片
│
├── requirements.txt                           # Python 依赖清单
├── README.md                                  # 项目说明文档（本文件）
└── .gitignore                                 # Git 忽略规则
```

---

## PPT 视觉风格预览

项目提供 5 种预设 PPT 视觉风格，点击图片可查看完整的配色参考与 accessibility 合规说明。

| 风格 | 预览 | 适用场景 |
|------|------|---------|
| **深色科技风** `dark-tech` | [![深色科技风预览](assets/style-previews/dark-tech.svg)](docs/styles/dark-tech.html) | 技术分享、开发者大会、产品发布 |
| **暖色系** `warm-elegant` | [![暖色系预览](assets/style-previews/warm-elegant.svg)](docs/styles/warm-elegant.html) | 商务汇报、教育培训、项目管理 |
| **薄荷清新风** `mint-fresh` | [![薄荷清新风预览](assets/style-previews/mint-fresh.svg)](docs/styles/mint-fresh.html) | 环保/健康主题、创意工作坊 |
| **霓虹赛博风** `cyber-neon` | [![霓虹赛博风预览](assets/style-previews/cyber-neon.svg)](docs/styles/cyber-neon.html) | 游戏开发、NFT/元宇宙、极客活动 |
| **极简纯净风** `minimal-clean` | [![极简纯净风预览](assets/style-previews/minimal-clean.svg)](docs/styles/minimal-clean.html) | 设计作品集、学术报告、企业官网 |

所有风格的完整配色方案、色值代码、渐变方案及应用示例见 [docs/styles/](docs/styles/)。

---

## 模块功能说明

### ppt-generator（PPT 生成器）

通过七角色协作工作流生成高质量 PPT：

| 角色 | 职责 |
|------|------|
| 主题分析师 | 分析需求，生成 PPT 结构大纲 |
| 模板设计师 | 推荐布局和风格方案 |
| 内容策划师 | 规划页面结构和信息呈现方式 |
| 文本创作者 | 撰写精炼的 PPT 内容 |
| 视觉设计师 | 提供 AI 智能配图建议 |
| 优化编辑师 | 语言润色、结构优化、内容精炼 |
| PPT 构建师 | 将内容整理为结构化数据，生成 PPTX 文件 |

### web-design-analyzer（网页设计分析器）

- 自动识别网页视觉风格
- 提取精确的色彩系统（Hex Code + Tailwind 类名）
- 分析排版系统（字体类型、字重、行高）
- 识别组件特征（圆角、阴影、边框）
- 生成结构化 JSON 数据和可直接使用的 Coding Prompt
- 支持导出为路演视频品牌风格配置

## 常见问题

### Q1：安装依赖时报错怎么办？

确保使用 Python 3.9 或更高版本，并尝试升级 pip：

```bash
pip install --upgrade pip
pip install -r requirements.txt
```

### Q2：如何获取 OpenAI API Key？

1. 访问 [OpenAI Platform](https://platform.openai.com/)
2. 登录后进入 API Keys 页面
3. 创建新的 API Key
4. 设置环境变量：`set OPENAI_API_KEY=your_key_here`（Windows）或 `export OPENAI_API_KEY=your_key_here`（macOS/Linux）

### Q3：如何在日本语 Windows 系统上运行？

本项目已内置编码兼容处理，可自动适配 `cp932`（Shift-JIS）编码环境。如遇到编码问题，请确保：

- 使用 UTF-8 编码保存输入文件
- 终端支持 UTF-8 输出（或使用 PowerShell 7+）

### Q4：生成的 PPT 可以自定义样式吗？

当前版本使用默认样式（Calibri 字体、36pt 标题、20pt 正文）。自定义样式功能正在规划中，详见 [模板配置说明](skills/01-ppt-generator/ppt-generator/assets/ppt_templates/README.md)。

## 开发指南

### 添加新的 Skill 模块

1. 在 `skills/` 目录下创建新的 Skill 文件夹
2. 参考现有 SKILL.md 格式编写技能定义文件
3. 将脚本放置在 `scripts/` 子目录中
4. 将参考文档放置在 `references/` 子目录中
5. 在 `project_content/` 中记录新增模块的概要信息
6. 如有新的 Python 依赖，同步更新 `requirements.txt`

### 编码规范

- Python 代码遵循 [PEP 8](https://peps.python.org/pep-0008/) 编码规范
- 脚本文件包含文件头注释（功能说明、依赖、使用方法）
- 关键函数包含清晰的文档字符串（docstring）
- 敏感信息（API Key、密码等）严禁提交到版本控制

## 许可证

本项目仅供学习和研究使用。
