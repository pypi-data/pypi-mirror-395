from contextlib import asynccontextmanager
from pathlib import Path
from typing import Literal

import img2pdf
import pytest
from beni import bfile, bpath, btask
from PIL import Image


@pytest.mark.asyncio
async def test_pdf_output_images():
    async with _createTempPdfFile() as pdfFile:
        result = btask.testCall('pdf', 'output-images', '--target', pdfFile.as_posix())
        assert result.exit_code == 0
        outputImagesPath = pdfFile.parent / f'{pdfFile.stem}-PDF图片文件'
        assert outputImagesPath.is_dir()
        assert len(list(outputImagesPath.glob('*.png'))) == 1
        assert len(list(outputImagesPath.glob('*.jpeg'))) == 1


@asynccontextmanager
async def _createTempPdfFile():

    def create_color_block_image(
            file: Path,
            color: tuple[int, int, int],
            size: tuple[int, int] = (500, 500),
            image_format: Literal['JPEG', 'PNG'] = 'JPEG'
    ):
        image = Image.new('RGB', size, color)
        image.save(file, format=image_format)
        image.close()
        return file

    with bpath.useTempPath(True) as tempPath:
        # 创建色块图片
        fileList = [
            create_color_block_image(tempPath / 'blue.png', (0, 0, 255), image_format='PNG'),
            create_color_block_image(tempPath / 'red.jpeg', (255, 0, 0), image_format='JPEG'),
        ]

        # 生成PDF文件
        pdfFile = tempPath / 'output.pdf'
        await bfile.writeBytes(pdfFile, img2pdf.convert(fileList))  # type: ignore

        yield pdfFile
