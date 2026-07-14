#!/usr/bin/env python3
"""
HTML-PPT 转换器 — 主入口
批量导入 HTML-PPT 文件 → 可编辑 PPTX + 自定义截图导出

借鉴项目:
  - slide-gen (0-AI-UG/slide-gen): OOXML 重建思路
  - dom-to-pptx (atharva9167j/dom-to-pptx): DOM 样式引擎
  - html_to_ppt (CHENJIAMIAN/html_to_ppt): 批处理架构
  - lovstudio/html2pptx: Playwright 截图方案
"""
import sys
import os
import argparse
from pathlib import Path

# 编码兼容处理 (Windows cp932)
if sys.stdout.encoding and sys.stdout.encoding.upper() != 'UTF-8':
    import io
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')

# 添加项目路径
sys.path.insert(0, str(Path(__file__).parent))

from converter.batch_processor import BatchProcessor


def parse_resolution(value: str) -> tuple:
    """解析分辨率参数，如 '1920x1080' → (1920, 1080)"""
    try:
        w, h = value.lower().split('x')
        return (int(w), int(h))
    except (ValueError, AttributeError):
        raise argparse.ArgumentTypeError(
            f'无效分辨率格式: {value}，请使用 WIDTHxHEIGHT 格式，如 1920x1080'
        )


def parse_crop_area(value: str) -> tuple:
    """解析截取范围，如 '100,100,1000,800' → (100, 100, 1000, 800)"""
    try:
        parts = [int(x.strip()) for x in value.split(',')]
        if len(parts) != 4:
            raise ValueError
        return tuple(parts)
    except (ValueError, AttributeError):
        raise argparse.ArgumentTypeError(
            f'无效截取范围: {value}，请使用 left,top,right,bottom 格式，如 100,100,1000,800'
        )


def main():
    parser = argparse.ArgumentParser(
        description='HTML-PPT 转换器 — 批量导入 HTML-PPT → 可编辑 PPTX + 截图导出',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog='''
使用示例:
  # 批量转换目录下所有 HTML 文件为 PPTX + PNG 截图
  python app.py -i ./input -o ./output

  # 仅生成 PPTX
  python app.py -i ./input -o ./output --no-png

  # 生成 PPTX + JPG 截图 (指定分辨率)
  python app.py -i ./input -o ./output --jpg --resolution 3840x2160

  # 生成 PPTX + PDF 截图 + 指定截取范围
  python app.py -i ./input -o ./output --pdf --crop 50,50,1870,1030

  # 单文件转换
  python app.py -i ./input/presentation.html -o ./output

  # 使用 8 个线程并行处理
  python app.py -i ./input -o ./output --workers 8
'''
    )
    parser.add_argument('-i', '--input', required=True,
                        help='输入 HTML 文件或目录')
    parser.add_argument('-o', '--output', default='./output',
                        help='输出目录 (默认: ./output)')
    parser.add_argument('--workers', type=int, default=None,
                        help='并行工作线程数 (默认: CPU 核心数)')

    # 输出格式控制
    format_group = parser.add_argument_group('输出格式')
    format_group.add_argument('--no-pptx', action='store_true',
                              help='跳过 PPTX 生成')
    format_group.add_argument('--no-png', action='store_true',
                              help='跳过 PNG 截图')
    format_group.add_argument('--jpg', action='store_true',
                              help='同时导出 JPG 截图')
    format_group.add_argument('--pdf', action='store_true',
                              help='同时导出 PDF 截图')

    # 截图设置
    shot_group = parser.add_argument_group('截图设置')
    shot_group.add_argument('--resolution', type=parse_resolution,
                            default=None,
                            help='截图分辨率，如 1920x1080')
    shot_group.add_argument('--crop', type=parse_crop_area,
                            default=None,
                            help='截取范围，如 left,top,right,bottom')

    args = parser.parse_args()

    # 确定输入模式
    input_path = Path(args.input)
    if not input_path.exists():
        print(f'❌ 输入路径不存在: {args.input}')
        sys.exit(1)

    # 创建处理器
    processor = BatchProcessor(
        workers=args.workers,
        output_dir=args.output,
    )

    # 执行转换
    if input_path.is_file():
        if input_path.suffix.lower() != '.html':
            print(f'❌ 输入文件不是 HTML 文件: {args.input}')
            sys.exit(1)

        # 单文件模式：放入临时目录处理
        import tempfile
        import shutil
        with tempfile.TemporaryDirectory() as tmpdir:
            shutil.copy2(str(input_path), tmpdir)
            results = processor.process_directory(
                input_dir=tmpdir,
                output_dir=args.output,
                format_pptx=not args.no_pptx,
                format_png=not args.no_png,
                format_jpg=args.jpg,
                format_pdf=args.pdf,
                resolution=args.resolution,
                crop_area=args.crop,
            )
    elif input_path.is_dir():
        results = processor.process_directory(
            input_dir=args.input,
            output_dir=args.output,
            format_pptx=not args.no_pptx,
            format_png=not args.no_png,
            format_jpg=args.jpg,
            format_pdf=args.pdf,
            resolution=args.resolution,
            crop_area=args.crop,
        )
    else:
        print(f'❌ 输入路径类型异常: {args.input}')
        sys.exit(1)

    # 最终结果
    success = sum(1 for r in results if r.status == 'success')
    failed = sum(1 for r in results if r.status == 'failed')

    print(f'\n{"="*50}')
    print(f'🎯 转换完成! 成功: {success} / 失败: {failed}')
    if failed > 0:
        print(f'   失败文件:')
        for r in results:
            if r.status == 'failed':
                print(f'     - {r.filename}: {r.error}')
    print(f'📁 输出目录: {os.path.abspath(args.output)}')


if __name__ == '__main__':
    main()
