"""
截图引擎 — 使用 Playwright 渲染 HTML 并截取高保真截图。
支持自定义分辨率、格式和截取范围。
借鉴 slide-gen 和 lovstudio/html2pptx 的 Playwright 截图方案。
修正：使用元素 clip 精确截取，移除 full_page，确保内容居中。
"""
import os
import sys
from pathlib import Path
from io import BytesIO
from PIL import Image
from typing import Optional

# 编码兼容处理 (Windows cp932)
if sys.stdout.encoding and sys.stdout.encoding.upper() != 'UTF-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')


class ScreenshotEngine:
    """基于 Playwright 的 HTML 截图引擎"""

    def __init__(self, width=1920, height=1080, scale=2):
        self.width = width
        self.height = height
        self.scale = scale
        self._browser = None
        self._page = None

    async def _ensure_browser(self):
        """确保浏览器实例已启动"""
        if self._browser is None:
            from playwright.async_api import async_playwright
            self._pw = await async_playwright().start()
            self._browser = await self._pw.chromium.launch(
                headless=True,
                args=['--no-sandbox', '--disable-setuid-sandbox']
            )

    async def _ensure_page(self):
        """确保页面已创建"""
        if self._page is None:
            await self._ensure_browser()
            self._page = await self._browser.new_page(
                viewport={'width': self.width, 'height': self.height},
                device_scale_factor=self.scale
            )

    async def capture_slide(self, html_content: str, selector: str = '.slide',
                            output_path: str = None) -> Optional[bytes]:
        """
        截取单张幻灯片的截图。
        使用元素 clip 精确截取 .slide 元素区域，确保内容铺满画布且居中。
        """
        await self._ensure_page()
        await self._page.set_content(html_content, wait_until='networkidle')

        # 等待字体和图片加载
        await self._page.wait_for_timeout(2000)

        # 查找幻灯片元素并用 clip 精确截取
        el = await self._page.query_selector(selector)
        if el:
            clip = await el.bounding_box()
            if clip:
                # clip 截取：精确对准 .slide 元素，不自带额外边距
                screenshot_bytes = await self._page.screenshot(
                    clip=clip, full_page=False
                )
            else:
                # fallback: 没有有效 clip 时截取 viewport
                screenshot_bytes = await self._page.screenshot(full_page=False)
        else:
            # fallback: 找不到 .slide 元素时截取整个 viewport
            screenshot_bytes = await self._page.screenshot(full_page=False)

        if output_path:
            Path(output_path).parent.mkdir(parents=True, exist_ok=True)
            with open(output_path, 'wb') as f:
                f.write(screenshot_bytes)

        return screenshot_bytes

    async def capture_slides_from_html(self, html_path: str,
                                       output_dir: str = None,
                                       selector: str = '.slide') -> list[str]:
        """从 HTML 文件中截取所有幻灯片"""
        html_path = Path(html_path)
        if not html_path.exists():
            raise FileNotFoundError(f'HTML 文件不存在: {html_path}')

        # 读取 HTML
        with open(html_path, 'r', encoding='utf-8') as f:
            html_content = f.read()

        # 使用 Playwright
        await self._ensure_page()
        await self._page.set_content(html_content, wait_until='networkidle')
        await self._page.wait_for_timeout(2000)

        slide_elements = await self._page.query_selector_all(selector)
        output_paths = []

        for i, slide_el in enumerate(slide_elements):
            clip = await slide_el.bounding_box()
            if clip:
                screenshot_bytes = await self._page.screenshot(clip=clip)
            else:
                screenshot_bytes = await self._page.screenshot(full_page=False)

            if output_dir:
                out_dir = Path(output_dir)
                out_dir.mkdir(parents=True, exist_ok=True)
                out_path = str(out_dir / f'slide-{i + 1:03d}.png')
                with open(out_path, 'wb') as f:
                    f.write(screenshot_bytes)
                output_paths.append(out_path)

        return output_paths

    async def close(self):
        """关闭浏览器"""
        if self._page:
            await self._page.close()
            self._page = None
        if self._browser:
            await self._browser.close()
            self._browser = None
        if hasattr(self, '_pw'):
            await self._pw.stop()

    def __del__(self):
        """析构时确保资源释放"""
        try:
            import asyncio
            loop = asyncio.get_event_loop()
            if loop.is_running():
                loop.create_task(self.close())
        except RuntimeError:
            pass


def process_screenshot(image_bytes: bytes,
                       output_format: str = 'PNG',
                       resolution: tuple = None,
                       crop_area: tuple = None) -> bytes:
    """
    后处理截图:
    - output_format: 'PNG', 'JPG', 'PDF'
    - resolution: (width, height) 目标分辨率
    - crop_area: (left, top, right, bottom) 截取范围
    """
    img = Image.open(BytesIO(image_bytes))

    # 裁剪
    if crop_area:
        img = img.crop(crop_area)

    # 缩放
    if resolution:
        img = img.resize(resolution, Image.LANCZOS)

    # 输出
    buf = BytesIO()
    fmt = output_format.upper()
    if fmt == 'JPG':
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(buf, format='JPEG', quality=95)
    elif fmt == 'PDF':
        if img.mode == 'RGBA':
            img = img.convert('RGB')
        img.save(buf, format='PDF', resolution=100.0)
    else:
        img.save(buf, format='PNG')

    return buf.getvalue()


def save_screenshot(image_bytes: bytes, output_path: str,
                    output_format: str = 'PNG',
                    resolution: tuple = None,
                    crop_area: tuple = None):
    """保存处理后截图到文件"""
    data = process_screenshot(
        image_bytes, output_format, resolution, crop_area
    )
    out_path = Path(output_path)
    out_path.parent.mkdir(parents=True, exist_ok=True)

    # 确保扩展名正确
    ext_map = {'PNG': '.png', 'JPG': '.jpg', 'PDF': '.pdf'}
    expected_ext = ext_map.get(output_format.upper(), '.png')
    if not out_path.suffix.lower() == expected_ext:
        out_path = out_path.with_suffix(expected_ext)

    with open(out_path, 'wb') as f:
        f.write(data)
    return str(out_path)
