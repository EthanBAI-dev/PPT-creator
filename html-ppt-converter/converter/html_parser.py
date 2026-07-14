"""
HTML 解析器 — 解析 HTML 文件，提取幻灯片结构和元素数据。
借鉴 dom-to-pptx 的 DOM 遍历与样式提取思路。
"""
import re
from pathlib import Path
from bs4 import BeautifulSoup, Tag

SLIDE_SELECTORS = [
    'div.slide', 'section.slide', '[data-slide]',
    '.slide', 'section[class*="slide"]'
]


class SlideElement:
    """单个幻灯片元素的数据容器"""
    def __init__(self, tag: str, text: str, attrs: dict, styles: dict,
                 bbox: dict = None):
        self.tag = tag
        self.text = text.strip() if text else ''
        self.attrs = attrs
        self.styles = styles
        self.bbox = bbox or {'x': 0, 'y': 0, 'w': 0, 'h': 0}

    def __repr__(self):
        return f'<SlideElement {self.tag} text="{self.text[:30]}">'


class SlideData:
    """单张幻灯片的数据"""
    def __init__(self, index: int, title: str = '',
                 elements: list = None, raw_html: str = ''):
        self.index = index
        self.title = title
        self.elements = elements or []
        self.raw_html = raw_html

    def __repr__(self):
        return f'<SlideData #{self.index} title="{self.title}" elems={len(self.elements)}>'


class HtmlParser:
    """解析 HTML 文件，提取 Slide 列表"""

    @staticmethod
    def find_slides(soup: BeautifulSoup) -> list[Tag]:
        """智能查找所有幻灯片容器"""
        for selector in SLIDE_SELECTORS:
            slides = soup.select(selector)
            if slides:
                return slides
        # 回退: 查找 body 的直接子元素中的块级容器
        body = soup.find('body') or soup
        candidates = body.find_all(['div', 'section', 'article'],
                                   recursive=False)
        if candidates:
            return candidates
        return []

    @staticmethod
    def extract_title(element: Tag) -> str:
        """从幻灯片元素中提取标题"""
        for tag in ['h1', 'h2', 'h3', '.title', '.slide-title']:
            title_el = element.select_one(tag)
            if title_el and title_el.get_text(strip=True):
                return title_el.get_text(strip=True)
        return ''

    @staticmethod
    def extract_elements(element: Tag) -> list[SlideElement]:
        """递归提取幻灯片中的结构化元素（去重）"""
        elements = []
        # 跳过纯容器元素，只提取叶节点
        CONTAINER_TAGS = {'div', 'section', 'article', 'main', 'header',
                          'footer', 'nav', 'aside', 'figure', 'figcaption'}
        LEAF_TAGS = {'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'p', 'li',
                     'span', 'blockquote', 'pre', 'code', 'td', 'th',
                     'label', 'caption', 'dt', 'dd'}

        for child in element.children:
            if not isinstance(child, Tag):
                continue
            if child.name in ['style', 'script', 'meta', 'link']:
                continue

            tag = child.name or 'div'

            # 提取样式
            styles = {}
            if child.get('style'):
                for rule in child['style'].split(';'):
                    if ':' in rule:
                        k, v = rule.split(':', 1)
                        styles[k.strip()] = v.strip()

            # 叶节点或标题 → 直接添加
            if tag in LEAF_TAGS or tag.startswith('h'):
                text = child.get_text(strip=True)
                if text:  # 跳过空文本
                    elements.append(SlideElement(
                        tag=tag, text=text,
                        attrs=child.attrs, styles=styles
                    ))

            # 容器元素 → 不添加自身（避免 get_text 抓取子元素文本导致重复）
            # 而是递归提取其子元素
            elif tag in CONTAINER_TAGS or tag in ['ul', 'ol']:
                sub = HtmlParser.extract_elements(child)
                elements.extend(sub)

            # 列表项 <li> 已经是叶节点，上面已覆盖
            # 图片/其他元素
            elif tag == 'img':
                src = child.get('src', '')
                alt = child.get('alt', '')
                elements.append(SlideElement(
                    tag='img', text=alt,
                    attrs={'src': src, 'alt': alt}, styles=styles
                ))
            else:
                # 其他标签：尝试提取文本
                text = child.get_text(strip=True)
                if text:
                    elements.append(SlideElement(
                        tag=tag, text=text,
                        attrs=child.attrs, styles=styles
                    ))

        return elements

    @staticmethod
    def extract_css_vars(soup: BeautifulSoup) -> dict:
        """提取 CSS 自定义属性和关键样式变量"""
        vars_ = {}
        for style_tag in soup.find_all('style'):
            text = style_tag.string or ''
            # 匹配 :root { --xxx: yyy } 或 body { --xxx: yyy }
            for m in re.finditer(r'--([\w-]+)\s*:\s*([^;}]+)', text):
                vars_[m.group(1)] = m.group(2).strip()
        return vars_

    def parse_file(self, html_path: str) -> list[SlideData]:
        """解析单个 HTML 文件，返回幻灯片列表"""
        path = Path(html_path)
        if not path.exists():
            raise FileNotFoundError(f'HTML 文件不存在: {html_path}')

        raw = path.read_text('utf-8')
        soup = BeautifulSoup(raw, 'lxml')
        css_vars = self.extract_css_vars(soup)
        slide_tags = self.find_slides(soup)

        if not slide_tags:
            # 整个文档当作一张幻灯片
            title = self.extract_title(soup)
            elements = self.extract_elements(soup)
            return [SlideData(0, title=title, elements=elements, raw_html=raw)]

        slides = []
        for i, tag in enumerate(slide_tags):
            title = self.extract_title(tag)
            elements = self.extract_elements(tag)
            slides.append(SlideData(
                index=i,
                title=title,
                elements=elements,
                raw_html=str(tag)
            ))
        return slides

    def parse_directory(self, dir_path: str) -> dict[str, list[SlideData]]:
        """批量解析目录下所有 HTML 文件"""
        base = Path(dir_path)
        if not base.is_dir():
            raise NotADirectoryError(f'目录不存在: {dir_path}')

        result = {}
        for html_file in sorted(base.glob('*.html')):
            try:
                slides = self.parse_file(str(html_file))
                result[html_file.name] = slides
            except Exception as e:
                result[html_file.name] = f'[解析失败] {e}'
        return result
