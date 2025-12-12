from pathlib import Path
from typing import Final

import fitz
import typer
from beni import bcolor, bfile, btask
from beni.bfunc import syncCall

app: Final = btask.newSubApp('PDF相关')


@app.command()
@syncCall
async def output_images(
    target: Path = typer.Option(Path.cwd(), '--target', help='PDF文件路径或多个PDF文件所在的目录'),
):
    '保存 PDF 文件里面的图片'

    # 列出需要检查的PDF文件
    pdfFileList: list[Path] = []
    if target.is_dir():
        pdfFileList = list(target.glob('*.pdf'))
    elif target.is_file():
        pdfFileList = [target]
    else:
        raise ValueError("目标路径不存在")

    for pdf_file in pdfFileList:
        pdf_document = fitz.open(pdf_file)
        output_dir = pdf_file.with_name(pdf_file.stem + '-PDF图片文件')
        for page_num in range(len(pdf_document)):
            page = pdf_document.load_page(page_num)
            images = page.get_images(full=True)
            for img_index, img in enumerate(images):
                xref = img[0]
                base_image = pdf_document.extract_image(xref)
                image_bytes = base_image["image"]
                image_ext = base_image["ext"]
                image_filename = f"page{page_num + 1}_img{img_index + 1}.{image_ext}"
                image_path = output_dir / image_filename
                output_dir.mkdir(exist_ok=True)
                bcolor.printGreen(image_path)
                await bfile.writeBytes(image_path, image_bytes)
