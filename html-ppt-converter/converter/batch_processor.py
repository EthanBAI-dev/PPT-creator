"""
批处理处理器 — 支持多线程批量转换 HTML 文件为 PPTX + 截图。
借鉴 html_to_ppt 的多线程并行处理架构。
"""
import os
import sys
import asyncio
import json
import time
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from typing import Optional

from .html_parser import HtmlParser
from .pptx_builder import PptxBuilder
from .screenshot_engine import ScreenshotEngine, save_screenshot

# 编码兼容处理
if sys.stdout.encoding and sys.stdout.encoding.upper() != 'UTF-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


class ConversionResult:
    """单个文件的转换结果"""
    def __init__(self, filename: str, status: str = 'pending',
                 pptx_path: str = '', screenshots: list = None,
                 error: str = '', duration: float = 0):
        self.filename = filename
        self.status = status      # success / failed / skipped
        self.pptx_path = pptx_path
        self.screenshots = screenshots or []
        self.error = error
        self.duration = duration

    def to_dict(self):
        return {
            'filename': self.filename,
            'status': self.status,
            'pptx_path': self.pptx_path,
            'screenshot_count': len(self.screenshots),
            'error': self.error,
            'duration': f'{self.duration:.1f}s'
        }


class BatchProcessor:
    """批量转换处理器"""

    def __init__(self, workers: int = None, output_dir: str = './output',
                 png_dpi: int = 200, jpg_quality: int = 95):
        self.workers = workers or os.cpu_count() or 4
        self.output_dir = Path(output_dir)
        self.png_dpi = png_dpi
        self.jpg_quality = jpg_quality
        self.parser = HtmlParser()

    def _convert_single(self, html_path: Path, output_base: Path,
                        format_pptx: bool, format_png: bool,
                        format_jpg: bool, format_pdf: bool,
                        resolution: tuple, crop_area: tuple) -> ConversionResult:
        """转换单个 HTML 文件"""
        filename = html_path.name
        result = ConversionResult(filename=filename)
        start = time.time()

        try:
            # 1. 解析 HTML
            slides = self.parser.parse_file(str(html_path))
            if not slides:
                raise RuntimeError('未找到任何幻灯片')

            # 2. 构建 PPTX（如果启用）
            pptx_path = ''
            if format_pptx:
                builder = PptxBuilder()
                for slide_data in slides:
                    builder.build_slide_from_data(slide_data)
                pptx_name = html_path.stem + '.pptx'
                pptx_path = str(output_base / 'pptx' / pptx_name)
                builder.save(pptx_path)

            # 3. 截图导出（如果启用）
            screenshots = []
            if format_png or format_jpg or format_pdf:
                # 使用 Playwright 截图
                loop = asyncio.new_event_loop()
                asyncio.set_event_loop(loop)
                try:
                    engine = ScreenshotEngine(
                        width=1920, height=1080, scale=2
                    )
                    for i, slide_data in enumerate(slides):
                        fmt = 'PNG'
                        if format_jpg:
                            fmt = 'JPG'
                        elif format_pdf:
                            fmt = 'PDF'

                        ext_map = {'PNG': '.png', 'JPG': '.jpg', 'PDF': '.pdf'}
                        ext = ext_map.get(fmt, '.png')
                        shot_name = f'{html_path.stem}-slide-{i + 1:03d}{ext}'
                        shot_path = str(output_base / 'screenshots' / shot_name)

                        # 截图：构造完整HTML文档，确保布局正确
                        raw_fragment = slide_data.raw_html.strip()
                        if not raw_fragment:
                            raw_fragment = '<div class="slide"><p>空幻灯片</p></div>'

                        html_to_render = (
                            '<!DOCTYPE html><html><head><meta charset="UTF-8">'
                            '<meta name="viewport" content="width=1920, initial-scale=1">'
                            '<style>'
                            '*,*::before,*::after{box-sizing:border-box;margin:0;padding:0}'
                            'html,body{width:1920px;height:1080px;overflow:hidden;'
                            'background:#faf7f2;font-family:-apple-system,BlinkMacSystemFont,'
                            '"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif}'
                            '.slide{display:flex;flex-direction:column;'
                            'justify-content:center;align-items:center;'
                            'position:relative;width:1920px;height:1080px;'
                            'overflow:hidden;padding:60px 80px;'
                            'background:inherit;color:#2d2d2d}'
                            '.slide>*{max-width:100%;}'
                            'h1{font-size:42px;font-weight:700;margin-bottom:16px;color:#e8695a}'
                            'h2{font-size:32px;font-weight:600;margin-bottom:12px}'
                            'h3{font-size:24px;font-weight:600;margin-bottom:8px}'
                            'p{font-size:18px;line-height:1.6;margin-bottom:10px;color:#444}'
                            'ul,ol{padding-left:32px;font-size:18px;line-height:1.8;color:#444}'
                            'li{margin-bottom:4px}'
                            '</style></head><body>'
                            f'{raw_fragment}'
                            '</body></html>'
                        )

                        shot_bytes = loop.run_until_complete(
                            engine.capture_slide(html_to_render)
                        )

                        # 后处理
                        save_screenshot(
                            shot_bytes,
                            shot_path,
                            output_format=fmt,
                            resolution=resolution,
                            crop_area=crop_area
                        )
                        screenshots.append(shot_path)
                finally:
                    loop.run_until_complete(engine.close())
                    loop.close()

            result.status = 'success'
            result.pptx_path = pptx_path
            result.screenshots = screenshots

        except Exception as e:
            result.status = 'failed'
            result.error = str(e)

        result.duration = time.time() - start
        return result

    def process_directory(self, input_dir: str, output_dir: str = None,
                          format_pptx: bool = True,
                          format_png: bool = True,
                          format_jpg: bool = False,
                          format_pdf: bool = False,
                          resolution: tuple = None,
                          crop_area: tuple = None) -> list[ConversionResult]:
        """
        批量处理目录中的所有 HTML 文件

        参数:
            input_dir: HTML 文件目录
            output_dir: 输出目录（默认为 self.output_dir）
            format_pptx: 是否生成 PPTX
            format_png: 是否生成 PNG 截图
            format_jpg: 是否生成 JPG 截图
            format_pdf: 是否生成 PDF 截图
            resolution: (width, height) 截图目标分辨率
            crop_area: (left, top, right, bottom) 截取范围
        """
        input_path = Path(input_dir)
        if not input_path.is_dir():
            raise NotADirectoryError(f'输入目录不存在: {input_dir}')

        out_base = Path(output_dir) if output_dir else self.output_dir
        out_base.mkdir(parents=True, exist_ok=True)

        html_files = sorted(input_path.glob('*.html'))
        if not html_files:
            print(f'⚠  目录中没有 HTML 文件: {input_dir}')
            return []

        print(f'📂 发现 {len(html_files)} 个 HTML 文件，使用 {self.workers} 个线程并行处理...')
        results = []

        with ThreadPoolExecutor(max_workers=self.workers) as executor:
            futures = {
                executor.submit(
                    self._convert_single, h, out_base,
                    format_pptx, format_png, format_jpg, format_pdf,
                    resolution, crop_area
                ): h.name for h in html_files
            }

            for future in as_completed(futures):
                name = futures[future]
                try:
                    result = future.result()
                    results.append(result)
                    status_icon = '✅' if result.status == 'success' else '❌'
                    print(f'  {status_icon} {name} - {result.status} ({result.duration:.1f}s)')
                except Exception as e:
                    results.append(ConversionResult(
                        filename=name, status='failed', error=str(e)
                    ))
                    print(f'  ❌ {name} - failed: {e}')

        # 按文件名排序
        results.sort(key=lambda r: r.filename)

        # 生成报告
        self._generate_report(results, out_base)
        return results

    def _generate_report(self, results: list[ConversionResult],
                         output_dir: Path):
        """生成转换报告"""
        total = len(results)
        success = sum(1 for r in results if r.status == 'success')
        failed = total - success

        report = {
            'summary': {
                'total': total,
                'success': success,
                'failed': failed,
                'timestamp': time.strftime('%Y-%m-%d %H:%M:%S')
            },
            'details': [r.to_dict() for r in results]
        }

        report_path = output_dir / 'conversion_report.json'
        with open(report_path, 'w', encoding='utf-8') as f:
            json.dump(report, f, ensure_ascii=False, indent=2)

        print(f'\n📊 转换报告: {report_path}')
        print(f'   总计: {total} | ✅ 成功: {success} | ❌ 失败: {failed}')

        # 列出输出目录结构
        for subdir in ['pptx', 'screenshots']:
            d = output_dir / subdir
            if d.exists():
                files = list(d.iterdir())
                print(f'   📁 {subdir}/: {len(files)} 个文件')
