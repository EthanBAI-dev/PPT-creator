# HTML-PPT 转换器

将 HTML 格式演示文稿批量转换为可编辑的 PPTX 文件，支持自定义截图导出（PNG/JPG/PDF）。

## 项目借鉴来源

本项目的实现借鉴了以下 GitHub 开源项目的核心思路：

| 项目 | Stars | 借鉴内容 |
|------|-------|---------|
| **[slide-gen](https://github.com/0-AI-UG/slide-gen)** | 新项目 | OOXML 重建架构：在浏览器渲染后提取 DOM 元素坐标和样式，重建为原生 PowerPoint 对象，输出可编辑文本而非截图 |
| **[dom-to-pptx](https://github.com/atharva9167j/dom-to-pptx)** | ⭐164 | DOM 样式引擎：遍历 DOM 树计算 computed style，将 Flex/Grid 布局数学映射为 PowerPoint 形状 |
| **[html_to_ppt](https://github.com/CHENJIAMIAN/html_to_ppt)** | 新项目 | 多线程批处理架构：ThreadPoolExecutor 并行处理，worker 数可配置 |
| **[lovstudio/html2pptx](https://github.com/lovstudio/html2pptx-skill)** | 新项目 | Playwright 截图方案：1920×1080@2× Retina 截图，CSS 保真度最大化 |

## 环境要求

- Python >= 3.9
- Chrome/Chromium 浏览器（Playwright 自动管理）

## 安装

```bash
# 1. 安装 Python 依赖
pip install -r requirements.txt

# 2. 安装 Playwright Chromium 浏览器
python -m playwright install chromium
```

## 快速开始

### 批量转换目录下所有 HTML 文件

```bash
python app.py -i ./input -o ./output
```

这将生成：
- `./output/pptx/*.pptx` — 可编辑的 PowerPoint 文件
- `./output/screenshots/*.png` — 高清截图
- `./output/conversion_report.json` — 转换报告

### 仅生成 PPTX（不截图）

```bash
python app.py -i ./input -o ./output --no-png
```

### 生成 PPTX + JPG 截图 + 指定分辨率

```bash
python app.py -i ./input -o ./output --jpg --resolution 3840x2160
```

### 单文件转换

```bash
python app.py -i ./input/presentation.html -o ./output
```

### 指定截取范围

```bash
python app.py -i ./input -o ./output --crop 50,50,1870,1030
```

### 并行处理

```bash
python app.py -i ./input -o ./output --workers 8
```

## 命令行参数

| 参数 | 说明 |
|------|------|
| `-i, --input` | 输入 HTML 文件或目录（必需） |
| `-o, --output` | 输出目录（默认: ./output） |
| `--workers` | 并行工作线程数（默认: CPU 核心数） |
| `--no-pptx` | 跳过 PPTX 生成 |
| `--no-png` | 跳过 PNG 截图 |
| `--jpg` | 同时导出 JPG 截图 |
| `--pdf` | 同时导出 PDF 截图 |
| `--resolution` | 截图分辨率，如 1920x1080 |
| `--crop` | 截取范围，如 left,top,right,bottom |

## 输入 HTML 格式要求

支持的幻灯片选择器（按优先级）：
1. `div.slide` / `section.slide`
2. `[data-slide]` 属性
3. `.slide` 类
4. Body 的直接子元素

示例 HTML 结构：

```html
<!DOCTYPE html>
<html>
<head>
  <style>
    .slide { width: 1920px; height: 1080px; padding: 60px; }
  </style>
</head>
<body>
  <div class="slide">
    <h1>封面标题</h1>
    <p>内容段落</p>
  </div>
  <div class="slide">
    <h1>第二页</h1>
    <ul>
      <li>要点 1</li>
      <li>要点 2</li>
    </ul>
  </div>
</body>
</html>
```

## 输出说明

```
output/
├── pptx/
│   ├── presentation1.pptx       # 可编辑的 PowerPoint
│   └── presentation2.pptx
├── screenshots/
│   ├── presentation1-slide-001.png
│   ├── presentation1-slide-002.png
│   └── presentation2-slide-001.png
└── conversion_report.json       # 转换结果报告
```

## 运行测试

```bash
cd html-ppt-converter
python tests/test_converter.py
```

测试覆盖：
- ✅ HTML 解析成功率测试
- ✅ PPTX 可编辑完整性测试（文本修改、结构保留）
- ✅ 截图格式转换测试（PNG/JPG/PDF）
- ✅ 分辨率调整与裁剪功能测试
- ✅ 批处理调度与报告生成测试

## 技术架构

```
HTML 文件
    │
    ▼
┌─────────────────┐
│  HtmlParser      │  ← 解析 DOM，提取标题/元素/样式
│  (BeautifulSoup) │
└────────┬────────┘
         │
    ┌────┴────┐
    │         │
    ▼         ▼
┌────────┐ ┌──────────────┐
│PptxBuilder│ │ScreenshotEngine│ ← Playwright 渲染
│(python-pptx)│ │(Playwright)   │
│ 可编辑OOXML│ │ 高保真截图     │
└────┬───┘ └──────┬───────┘
     │            │
     ▼            ▼
 ┌──────┐  ┌──────────┐
 │.pptx │  │.png/.jpg │
 │      │  │/.pdf     │
 └──────┘  └──────────┘
```

## 常见问题

### Q: Playwright 安装失败？
确保 Python 版本 >= 3.9，然后重试：
```bash
pip install playwright --upgrade
python -m playwright install chromium
```

### Q: 生成的 PPTX 文字不可编辑？
PPTX 生成采用 OOXML 重建模式，文本以原生文本框形式存在，在 PowerPoint/Keynote/LibreOffice 中均可直接编辑。

### Q: 截图模糊？
使用 `--resolution` 参数指定更高分辨率，如 `--resolution 3840x2160`。内置 2× Retina 缩放。

### Q: 只支持特定的 HTML 结构？
转换器支持多种幻灯片选择器自动检测。如果 HTML 使用自定义选择器，可修改 `html_parser.py` 中的 `SLIDE_SELECTORS`。
