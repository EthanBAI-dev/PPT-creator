---
name: web-design-analyzer
description: AI 驱动的网页设计分析工具。AI 利用视觉理解能力分析网页截图，提取设计系统（色彩、排版、组件风格），生成结构化数据和 Coding Prompt。适用于 UI/UX 设计师和前端工程师需要从现有网页设计中提取设计规范的场景。
---

# Web Design Analyzer

## 任务目标

- **核心**：AI 利用视觉理解能力分析网页截图，提取完整设计系统
- **能力**：
  - 识别网页视觉风格（Vibe & Style）
  - 提取精确色彩系统（Hex Code + Tailwind 类名）
  - 分析排版系统（字体类型、字重、行高）
  - 识别组件特征（圆角、阴影、边框）
  - 生成结构化 JSON 数据和 Coding Prompt
  - 导出为路演视频品牌风格配置
- **触发条件**：用户上传网页截图并要求分析设计，或需要将网页设计风格应用于路演视频

## 操作步骤

### 标准流程：AI 分析网页设计

#### 第 1 步：AI 自主分析（无需脚本）

用户上传网页截图后，AI 直接利用视觉理解能力分析图片，提取以下信息：

**视觉风格**
- 用 3 个关键词描述整体风格（如 Swiss Style, Bento Grid, Cyberpunk）
- 描述情绪传达（如 Trustworthy, Playful, Strict）

**色彩系统**
- 提取主色、辅助色、背景色、强调色
- 标注准确的 Hex Code
- 建议最接近的 Tailwind CSS 颜色类名

**排版系统**
- 识别字体类型（Serif, Sans-serif, Monospace）
- 估算标题与正文的字重和行高比例

**组件特征**
- 圆角（Border Radius）：具体数值或 Tailwind 类
- 阴影/深度（Shadow/Depth）：描述层级
- 边框（Border）：粗细及颜色

输出：结构化设计系统数据

#### 第 2 步：生成设计系统 JSON

AI 将分析结果整理为结构化 JSON：

```json
{
  "style_name": "风格名称",
  "colors": [
    {"role": "primary", "hex": "#...", "tailwind": "slate-900"},
    {"role": "secondary", "hex": "#...", "tailwind": "indigo-500"}
  ],
  "typography": "字体描述",
  "components": "组件特征描述"
}
```

#### 第 3 步：生成 Coding Prompt

AI 根据提取的设计规范，生成可直接用于前端开发的 Coding Prompt。示例：

```
Create a Hero section using Tailwind CSS. Use background color [HEX],
text color [HEX]. The design style should be [STYLE NAME], featuring
[COMPONENT FEATURES]. Font should feel like [FONT STYLE]...
```

### 可选分支

#### 分支 A：导出为路演视频风格

如果用户需要将设计系统用于路演视频，调用转换脚本：

```bash
python skills/05-web-design-analyzer/web-design-analyzer/scripts/convert_to_roadshow_style.py \
  --input ./design_system.json \
  --output ./output/brand_style.json
```

参考 [roadshow-export-guide.md](../../../skills/05-web-design-analyzer/web-design-analyzer/references/roadshow-export-guide.md) 了解映射规则。

#### 分支 B：脚本辅助分析（AI 视觉不可用时）

如果 AI 无法直接分析图片，可回退到调用 `analyze_design.py` 脚本：

```bash
python skills/05-web-design-analyzer/web-design-analyzer/scripts/analyze_design.py \
  --image ./screenshot.png \
  --output ./output/design_system.json
```

需配置 OpenAI API Key（环境变量 `OPENAI_API_KEY` 或 `COZE_OPENAI_VISION_API_<skill_id>`）。

## 参考资源

- [API 规范](../../../skills/05-web-design-analyzer/web-design-analyzer/references/api-spec.md)：调试 API 时参考
- [路演导出指南](../../../skills/05-web-design-analyzer/web-design-analyzer/references/roadshow-export-guide.md)：导出路演风格时参考
- [分析脚本](../../../skills/05-web-design-analyzer/web-design-analyzer/scripts/analyze_design.py)：分支 B 回退时调用
- [转换脚本](../../../skills/05-web-design-analyzer/web-design-analyzer/scripts/convert_to_roadshow_style.py)：导出路演风格时调用

## 注意事项

- **AI 优先**：AI 优先使用自身视觉能力分析图片，脚本仅作为补充手段
- **图片要求**：确保截图清晰，建议 PNG/JPEG 格式，分辨率不低于 1280×720
- **输出路径**：生成的文件统一放在 `./output/` 目录
- **协同流程**：分析结果可直接用于前端代码生成，或通过转换脚本用于路演视频
