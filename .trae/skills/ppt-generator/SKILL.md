---
name: ppt-generator
description: 基于 AI 的智能 PPT 生成工具。AI 自主完成需求分析、内容策划、文本创作、视觉设计，最后通过 python-pptx 脚本输出 .pptx 文件。适用于学术汇报、商业演示、产品发布等场景。
---

# PPT 生成器

## 任务目标

- **核心**：AI 利用自身语言能力完成 PPT 全流程创作，脚本仅用于最终的 PPTX 文件生成
- **能力**：需求分析、内容策划、文本创作、配图建议、文件生成
- **触发条件**：用户需要制作/优化 PPT，或基于主题生成演示文稿

## 操作步骤

### 标准流程：AI 自主生成 PPT

#### 第 1 步：AI 分析需求（无需脚本）

AI 自主分析用户需求，明确以下信息：
- **主题**：PPT 的核心主题和目标
- **受众**：投资人 / 客户 / 学生 / 管理层等
- **场景**：商务汇报 / 学术会议 / 产品发布 / 培训等
- **页数**：建议 10-20 页
- **风格**：专业商务 / 创意活泼 / 简约科技等

输出：PPT 结构大纲（封面、目录、3-5 个核心章节、结束页）

#### 第 2 步：AI 策划内容（无需脚本）

AI 根据大纲，为每页规划：
- 布局类型（参考 [ppt_structure_guide.md](../../../skills/01-ppt-generator/ppt-generator/references/ppt_structure_guide.md)）
- 每页标题和副标题
- 内容要点（3-5 条/页）
- 配图占位标注 `[图片：xxx]` 或 `[图表：xxx]`

输出：页面级内容规划

#### 第 3 步：AI 撰写文本（无需脚本）

AI 撰写每页精炼内容，遵循 PPT 写作原则：
- 标题不超过 20 字，要点不超过 20 字
- 一页一主题，聚焦核心信息
- 使用主动语态，数字和关键概念突出
- 标注 `[图片：xxx]` 占位

输出：完整 PPT 文本内容

#### 第 4 步：AI 整理 JSON 数据（AI 生成 JSON，脚本消费）

AI 将所有内容整理为结构化 JSON，格式需严格遵循 [ppt_structure_guide.md](../../../skills/01-ppt-generator/ppt-generator/references/ppt_structure_guide.md) 规范：

```json
{
  "metadata": {
    "title": "...",
    "author": "...",
    "subject": "...",
    "keywords": "..."
  },
  "slides": [
    {
      "layout": "TitleSlide",
      "title": "...",
      "content": ["..."],
      "notes": "..."
    }
  ]
}
```

#### 第 5 步：AI 调用脚本生成 PPTX

将 JSON 保存到临时文件，然后调用 `generate_pptx.py` 生成 PPTX：

```bash
python skills/01-ppt-generator/ppt-generator/scripts/generate_pptx.py \
  --input ./ppt_data.json \
  --output ./output/presentation.pptx
```

最后告知用户文件生成位置。

### 可选流程

| 模式 | 说明 | 执行步骤 |
|------|------|---------|
| **快速大纲** | 仅生成大纲和布局建议 | 步骤 1 → 2，输出大纲 |
| **内容填充** | 用户已有大纲，填充详细内容 | 步骤 2 → 3 → 4 → 5 |
| **文本优化** | 优化现有文本内容 | AI 直接润色，步骤 4 → 5 |
| **快速生成** | 跳过确认，直接完成 | 步骤 1 → 2 → 3 → 4 → 5 |

## 参考资源

- [PPT 结构规范](../../../skills/01-ppt-generator/ppt-generator/references/ppt_structure_guide.md)：生成 JSON 时必须参考
- [AI 配图指南](../../../skills/01-ppt-generator/ppt-generator/references/visual_design_guide.md)：配图建议时参考
- [生成脚本](../../../skills/01-ppt-generator/ppt-generator/scripts/generate_pptx.py)：仅步骤 5 调用

## 注意事项

- **AI 优先**：内容创作、文本润色、配图建议全部由 AI 自主完成，不依赖脚本
- **脚本最小化**：`generate_pptx.py` 仅在最终生成 .pptx 时调用
- **路径规范**：JSON 临时文件放在项目根目录，输出文件放在 `./output/` 目录
- **示例**：JSON 文件命名如 `ppt_data.json`，输出文件如 `./output/presentation.pptx`
