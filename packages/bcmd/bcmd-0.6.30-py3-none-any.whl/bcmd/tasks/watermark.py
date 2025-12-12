import json
import math
import tkinter as tk
from datetime import datetime
from typing import Final

from beni import bcolor, bpath, btask
from beni.bform import BForm
from beni.bfunc import syncCall
from beni.btype import XPath
from PIL import Image, ImageDraw, ImageFont

app: Final = btask.app


@app.command()
@syncCall
async def watermark(
):
    '图片添加水印，图片路径支持指定目录（使用该目录下所有图片文件批量处理，非递归）'
    result = _BuildForm().run()
    if result is None:
        btask.abort('用户取消操作')
    imagePath, text, color, textAlpha, fontSize, angle, spacingX, spacingY = result

    # 由于图片路径可能是多选，这里需要解析成列表
    try:
        fileList = [bpath.get(x) for x in json.loads(imagePath)]
    except:
        fileList = [bpath.get(imagePath)]

    # 创建一个输出的目录名称
    outputFolderName = f"watermark_{datetime.now().strftime('%d%m%y_%H%M%S')}"

    # 开始逐个文件操作
    for file in fileList:
        try:
            outputFile = file.parent / outputFolderName / file.name
            if not outputFile.parent.exists():
                bpath.make(outputFile.parent)
            _add_text_watermark(
                image_path=file,
                output_path=outputFile,
                text=text,
                color=color,
                opacity=int(textAlpha),
                font_size=int(fontSize),
                angle=float(angle),
                spacing_x=int(spacingX),
                spacing_y=int(spacingY),
            )
            bcolor.printGreen(f'处理文件成功：{file}')
        except Exception as ex:
            print(ex)
            bcolor.printRed(f'处理文件失败：{file}')


class _BuildForm(BForm):
    def __init__(self):
        super().__init__(title='图片添加水印')
        self.varImgPath = tk.StringVar(value=r'')
        self.varText = tk.StringVar(value='文字水印')
        self.varColor = tk.StringVar(value='#FF0000')
        self.varTextAlpha = tk.IntVar(value=80)
        self.varAngle = tk.IntVar(value=30)
        self.varFontSize = tk.StringVar(value='36')
        self.varSpacingX = tk.StringVar(value='100')
        self.varSpacingY = tk.StringVar(value='100')
        self.addChoisePath('图片文件', self.varImgPath, isMulti=True, width=15)
        self.addEntry('水印文字', self.varText, width=28)
        self.addColorChooser('文字颜色', self.varColor)
        self.addEntry('文字大小', self.varFontSize, width=10)
        self.addScale('文字透明度', self.varTextAlpha, from_=0, to=100, length=200)
        self.addScale('文字旋转', self.varAngle, from_=0, to=359, length=200)
        self.addEntry('水平间距', self.varSpacingX, width=10)
        self.addEntry('垂直间距', self.varSpacingY, width=10)
        self.addBtn('确定', self.onBtn)

    def onBtn(self):
        self.quit()

    def getResult(self):
        return self.varImgPath.get(), self.varText.get(), self.varColor.get(), self.varTextAlpha.get(), self.varFontSize.get(), self.varAngle.get(), self.varSpacingX.get(), self.varSpacingY.get()


def _parse_color(color: str, alpha: int):
    assert color.startswith('#'), "仅支持十六进制颜色格式，如 '#0099FF' 或 '#FF7700AA'"
    hexc = color.lstrip('#')
    if len(hexc) in (3, 4):
        hexc = ''.join(c * 2 for c in hexc)
    if len(hexc) == 6:
        r = int(hexc[0:2], 16)
        g = int(hexc[2:4], 16)
        b = int(hexc[4:6], 16)
        return (r, g, b, int(alpha))
    if len(hexc) == 8:
        r = int(hexc[0:2], 16)
        g = int(hexc[2:4], 16)
        b = int(hexc[4:6], 16)
        a = int(hexc[6:8], 16)
        return (r, g, b, a)


def _add_text_watermark(
    image_path: XPath,
    text: str = "Watermark",
    color: str = "#FFFFFF",
    opacity: int = 80,
    font_size: int = 36,
    angle: float = 30.0,
    spacing_x: int = 100,
    spacing_y: int = 100,
    font_path: str | None = None,
    output_path: XPath | None = None,
):
    """
    在整张图片上绘制重复的文字水印（对角或倾斜网格）。

    参数:
    - image_path: 原图片路径（会被读取）
    - text: 水印文字，默认 "Watermark"
    - color: 文字颜色，支持 '#RRGGBB' 或 RGB(A) 元组，默认白色
    - font_size: 字号，默认 36
    - angle: 文字倾斜角度（度），默认 30
    - spacing_x: 横向文字之间的间距（像素），默认 100
    - spacing_y: 纵向文字之间的间距（像素），默认 100
    - opacity: 文字透明度（0-255），默认 80（较淡）
    - font_path: 可选字体文件路径（.ttf），若为空将尝试常见系统字体或内置默认字体
    - output_path: 保存路径；若为 None 则覆盖原图
    """
    img = Image.open(image_path).convert("RGBA")
    w, h = img.size

    # 优化抗锯齿：固定超采样倍数
    supersample = 2
    scaled_font_size = font_size * supersample

    # 选择字体(使用放大的字号)
    font = None
    if font_path:
        try:
            font = ImageFont.truetype(font_path, scaled_font_size)
        except Exception:
            font = None
    if font is None:
        try:
            font = ImageFont.truetype("msyh.ttf", scaled_font_size)
        except Exception:
            try:
                font = ImageFont.truetype("Microsoft YaHei.ttf", scaled_font_size)
            except Exception:
                try:
                    font = ImageFont.truetype("msyh.ttc", scaled_font_size)
                except Exception:
                    try:
                        font = ImageFont.truetype("arial.ttf", scaled_font_size)
                    except Exception:
                        try:
                            font = ImageFont.truetype("DejaVuSans.ttf", scaled_font_size)
                        except Exception:
                            font = ImageFont.load_default()

    rgba = _parse_color(color, opacity)

    # 放大后画布尺寸（对角线 * supersample）
    diag = int(math.hypot(w, h))
    tile_size = (diag * supersample, diag * supersample)
    tile = Image.new("RGBA", tile_size, (0, 0, 0, 0))
    draw = ImageDraw.Draw(tile)

    # 文字尺寸(放大环境)
    text_bbox = draw.textbbox((0, 0), text, font=font)
    text_w = text_bbox[2] - text_bbox[0]
    text_h = text_bbox[3] - text_bbox[1]

    step_x = text_w + spacing_x * supersample
    step_y = text_h + spacing_y * supersample

    # 网格绘制
    y = 0
    while y < tile_size[1] + step_y:
        x = 0
        while x < tile_size[0] + step_x:
            draw.text((x, y), text, font=font, fill=rgba)
            x += step_x
        y += step_y

    # 旋转并裁剪回放大后的原图区域
    rotated = tile.rotate(angle, expand=True)
    rx, ry = rotated.size
    left = (rx - w * supersample) // 2
    top = (ry - h * supersample) // 2
    crop = rotated.crop((left, top, left + w * supersample, top + h * supersample))

    # 缩小到原图尺寸，获得平滑效果
    lanczos = Image.Resampling.LANCZOS
    watermark_layer = crop.resize((w, h), lanczos)

    # 合成
    watermarked = Image.alpha_composite(img, watermark_layer)

    save_path = output_path if output_path else image_path
    if str(save_path).lower().endswith((".jpg", ".jpeg")):
        watermarked = watermarked.convert("RGB")
    save_path = bpath.get(save_path)
    if not save_path.parent.exists():
        bpath.make(save_path.parent)
    watermarked.save(save_path)

    # 资源释放
    img.close()
    tile.close()
    rotated.close()
    crop.close()
    watermark_layer.close()
