import asyncio
import os
import random
from enum import StrEnum
from pathlib import Path
from typing import Final, List, Tuple

import httpx
import typer
from beni import bcolor, bfile, bhttp, binput, block, bpath, btask
from beni.bbyte import BytesReader, BytesWriter
from beni.bfunc import syncCall
from beni.btype import Null, XPath
from PIL import Image, ImageDraw, ImageFont

app: Final = btask.newSubApp('图片工具集')


class _OutputType(StrEnum):
    '输出类型'
    normal = '0'
    replace_ = '1'
    crc_replace = '2'


@app.command()
@syncCall
async def convert(
    path: Path = typer.Option(None, '--path', '-p', help='指定目录或具体图片文件，默认当前目录'),
    src_format: str = typer.Option('jpg|jpeg|png', '--src-format', '-s', help='如果path是目录，指定源格式，可以指定多个，默认值：jpg|jpeg|png'),
    dst_format: str = typer.Option('webp', '--dst-format', '-d', help='目标格式，只能是单个'),
    rgb: bool = typer.Option(False, '--rgb', help='转换为RGB格式'),
    quality: int = typer.Option(85, '--quality', '-q', help='图片质量，0-100，默认85'),
    output_type: _OutputType = typer.Option(_OutputType.normal, '--output-type', help='输出类型，0：普通输出，1：删除源文件，2：输出文件使用CRC32命名并删除源文件'),
):
    '图片格式转换'
    path = path or Path(os.getcwd())
    fileList: list[Path] = []
    if path.is_file():
        fileList.append(path)
    elif path.is_dir():
        extNameList = [x for x in src_format.strip().split('|')]
        fileList = [x for x in bpath.listFile(path, True) if x.suffix[1:].lower() in extNameList]
    if not fileList:
        return bcolor.printRed(f'未找到图片文件（{path}）')
    for file in fileList:
        with Image.open(file) as img:
            if rgb:
                img = img.convert('RGB')
            with bpath.useTempFile() as tempFile:
                img.save(tempFile, format=dst_format, quality=quality)
                outputFile = file.with_suffix(f'.{dst_format}')
                if output_type == _OutputType.crc_replace:
                    outputFile = outputFile.with_stem(await bfile.crc(tempFile))
                bpath.copy(tempFile, outputFile)
                if output_type in [_OutputType.replace_, _OutputType.crc_replace]:
                    if outputFile != file:
                        bpath.remove(file)
                bcolor.printGreen(f'{file} -> {outputFile}')


# ------------------------------------------------------------------------------------

@app.command()
@syncCall
async def tiny(
    path: Path = typer.Option(None, '--path', help='指定目录或具体图片文件，默认当前目录'),
    optimization: int = typer.Option(25, '--optimization', help='指定优化大小，如果没有达到优化效果就不处理，单位：%，默认25'),
    isKeepOriginal: bool = typer.Option(False, '--keep-original', help='保留原始图片'),
):

    keyList = [
        'MB3QmtvZ8HKRkXcDnxhWCNTXzvx6cNF3',
        '7L7X2CJ35GM1bChSHdT14yZPLx7FlpNk',
        'q8YLcvrXVW2NYcr5mMyzQhsSHF4j7gny',
    ]
    random.shuffle(keyList)

    class _TinyFile:

        _endian: Final = '>'
        _sep = BytesWriter(_endian).writeStr('tiny').writeUint(9527).writeUint(709394).toBytes()

        @property
        def compression(self):
            return self._compression

        @property
        def isTiny(self):
            return self._isTiny

        @property
        def file(self):
            return self._file

        def __init__(self, file: XPath):
            self._file = file
            self._compression: float = 0.0
            self._isTiny: bool = False

        def getSizeDisplay(self):
            size = bpath.get(self._file).stat().st_size / 1024
            return f'{size:,.2f}KB'

        async def updateInfo(self):
            fileBytes = await bfile.readBytes(self._file)
            self._compression = 0.0
            self._isTiny = False
            blockAry = fileBytes.split(self._sep)
            if len(blockAry) > 1:
                info = BytesReader(self._endian, blockAry[1])
                size = info.readUint()
                if size == len(blockAry[0]):
                    self._compression = round(info.readFloat(), 2)
                    self._isTiny = info.readBool()

        async def _flushInfo(self, compression: float, isTiny: bool):
            self._compression = compression
            self._isTiny = isTiny
            content = await self._getPureContent()
            info = (
                BytesWriter(self._endian)
                .writeUint(len(content))
                .writeFloat(compression)
                .writeBool(isTiny)
                .toBytes()
            )
            content += self._sep + info
            await bfile.writeBytes(self._file, content)

        async def _getPureContent(self):
            content = await bfile.readBytes(self._file)
            content = content.split(self._sep)[0]
            return content

        @block.limit(1)
        async def runTiny(self, key: str, compression: float, isKeepOriginal: bool):
            content = await self._getPureContent()
            async with httpx.AsyncClient() as client:
                response = await client.post(
                    'https://api.tinify.com/shrink',
                    auth=('api', key),
                    content=content,
                    timeout=30,
                )
                response.raise_for_status()
                result = response.json()
                outputCompression = round(result['output']['ratio'] * 100, 2)
                if outputCompression < compression:
                    # 下载文件
                    url = result['output']['url']
                    with bpath.useTempFile() as tempFile:
                        await bhttp.download(url, tempFile)
                        await _TinyFile(tempFile)._flushInfo(outputCompression, True)
                        outputFile = bpath.get(self._file)
                        if isKeepOriginal:
                            outputFile = outputFile.with_stem(f'{outputFile.stem}_tiny')
                        bpath.move(tempFile, outputFile, True)
                        bcolor.printGreen(f'{outputFile}（{outputCompression - 100:.2f}% / 压缩 / {self.getSizeDisplay()}）')
                else:
                    # 不进行压缩
                    await self._flushInfo(outputCompression, False)
                    bcolor.printMagenta(f'{self._file} （{outputCompression - 100:.2f}% / 不处理 / {self.getSizeDisplay()}）')

    btask.assertTrue(0 < optimization < 100, '优化大小必须在0-100之间')
    compression = 100 - optimization
    await block.setLimit(_TinyFile.runTiny, len(keyList))

    # 整理文件列表
    fileList = []
    path = path or Path(os.getcwd())
    if path.is_file():
        fileList.append(path)
    elif path.is_dir():
        fileList = [x for x in bpath.listFile(path, True) if x.suffix[1:].lower() in ['jpg', 'jpeg', 'png']]
    else:
        btask.abort('未找到图片文件', path)
    fileList.sort()

    # 将文件列表整理成 _TinyFile 对象
    fileList = [_TinyFile(x) for x in fileList]
    await asyncio.gather(*[x.updateInfo() for x in fileList])

    # 过滤掉已经处理过的图片
    for i in range(len(fileList)):
        file = fileList[i]
        if file.compression == 0:
            # 未处理过的图片，进行图片的压缩处理
            pass
        elif not file.isTiny and file.compression < compression:
            # 之前测试的压缩率不符合要求，不过现在符合了，进行图片的压缩处理
            pass
        else:
            # 要忽略掉的文件
            if file.isTiny:
                bcolor.printYellow(f'{file.file}（{file.compression - 100:.2f}% / 已压缩 / {file.getSizeDisplay()}）')
            else:
                bcolor.printMagenta(f'{file.file}（{file.compression - 100:.2f}% / 不处理 / {file.getSizeDisplay()}）')

            fileList[i] = Null
    fileList = [x for x in fileList if x]

    # 开始压缩
    taskList = [
        x.runTiny(keyList[i % len(keyList)], compression, isKeepOriginal)
        for i, x in enumerate(fileList)
    ]
    await asyncio.gather(*taskList)


@app.command()
@syncCall
async def merge(
    path: Path = typer.Argument(Path.cwd(), help='workspace 路径'),
    force: bool = typer.Option(False, '--force', '-f', help='强制覆盖'),
):
    '合并多张图片'

    def _get_watermark_font(font_size: int) -> ImageFont.FreeTypeFont:
        font_candidates = [
            'arial.ttf',                  # Windows
            'Arial.ttf',                  # macOS（部分系统可能区分大小写）
            'Helvetica.ttc',              # macOS
            'DejaVuSans.ttf',             # Linux
            'FreeSans.ttf',               # 某些Linux发行版
            'LiberationSans-Regular.ttf'  # RHEL系发行版
        ]
        for font_name in font_candidates:
            try:
                return ImageFont.truetype(font_name, font_size)
            except (IOError, OSError):
                continue
        raise Exception('No font found!')

    def _add_watermark(image: Image.Image, text: str, position: Tuple[float, float]) -> Image.Image:
        """添加圆形背景水印"""
        draw = ImageDraw.Draw(image)
        font_size = 100
        font = _get_watermark_font(font_size)

        # 计算文本尺寸并确定圆形参数
        text_bbox = draw.textbbox(position, text, font=font)
        text_width = text_bbox[2] - text_bbox[0]
        text_height = text_bbox[3] - text_bbox[1]

        # 计算圆形参数（直径取文本宽高的最大值 + 边距）
        diameter = max(text_width, text_height) + 20  # 10像素边距
        radius = diameter // 2

        # 计算圆形中心坐标（保持与原矩形左上角一致）
        circle_center = (
            position[0] + text_width // 2 + 5,  # 原位置向右偏移边距
            position[1] + text_height // 2 + 5  # 原位置向下偏移边距
        )

        # 绘制圆形背景
        ellipse_box = (
            circle_center[0] - radius,
            circle_center[1] - radius,
            circle_center[0] + radius,
            circle_center[1] + radius
        )
        draw.ellipse(ellipse_box, fill='#B920D9')

        # 绘制居中文字
        draw.text(
            circle_center,
            text,
            (255, 255, 255),
            font=font,
            anchor="mm"  # 设置锚点为水平垂直居中
        )
        return image

    def _merge_images(image_paths: List[Path], output_path: Path) -> None:
        images = [Image.open(img_path) for img_path in image_paths]
        max_width = max(img.width for img in images)
        total_height = sum(img.height for img in images)
        merged_image = Image.new('RGB', (max_width, total_height))
        y_offset = 0
        for idx, img in enumerate(images):
            merged_image.paste(img, (0, y_offset))
            _add_watermark(merged_image, f'{idx + 1}', (22, y_offset + 17))
            y_offset += img.height
        # 修改保存参数为 WebP 格式
        merged_image.save(
            output_path,
            format='JPEG',
            quality=80,        # 质量参数（0-100），推荐 80-90 之间
            method=6,          # 压缩方法（0-6），6 为最佳压缩
            lossless=False,    # 不使用无损压缩（更小的文件体积）
        )

    image_files = [x for x in bpath.listFile(path) if x.suffix in ('.png', '.jpg', '.jpeg', '.webp', '.bmp')]
    output_image = path / f'merge_{path.name}.jpg'  # 修改文件扩展名为 webp
    if output_image in image_files:
        if not force:
            print(output_image)
            await binput.confirm(f'生成文件已经存在，是否覆盖？')
        image_files.remove(output_image)
    image_files.sort(key=lambda x: x.as_posix())
    _merge_images(image_files, output_image)
    bcolor.printMagenta(output_image)
    bcolor.printGreen('OK')


# @app.command()
# @syncCall
# async def xone():
#     def showGui():
#         app = TkForm()
#         app.title('图片操作')
#         entry = app.addEntry('保存文件', tk.StringVar(value=r'C:\project\docs\source\docs\public\icon.webp'), width=60)
#         app.addEntry('输入密码', tk.StringVar(), password=True, width=60, command=lambda: messagebox.showerror('错误', '密码错误'))

#         scrolltextVar = tk.StringVar(value='xxiioo')
#         app.addScrolledText('测试信箱', scrolltextVar)

#         radioVarScale = app.addRadioBtnList(
#             '缩放操作',
#             [
#                 '保持',
#                 '缩放比',
#                 '指定宽度',
#                 '指定高度',
#             ],
#             onChanged=lambda x: onScaleValueChanged(x),
#             var=tk.StringVar(value='保持'),
#         )

#         scaleValueEntry = app.addEntry('缩放参数', tk.StringVar(), width=10, justify=tk.CENTER)

#         app.addChoisePath('选择文件', tk.StringVar(), isDir=True)

#         radioVarFormat = app.addRadioBtnList(
#             '格式转换',
#             [
#                 '保持',
#                 'PNG',
#                 'JPEG',
#                 'WEBP',
#             ],
#             var=tk.StringVar(value='保持'),
#         )
#         app.addCheckBox('去除透明', '去除透明', tk.BooleanVar(value=True))
#         app.addCheckBox('TinyPng', 'TinyPng', tk.BooleanVar())
#         app.addCheckBoxList('其他选项', [
#             ('去除透明', tk.BooleanVar()),
#             ('TinyPng', tk.BooleanVar(value=True)),
#         ])

#         def onScaleValueChanged(value: str):
#             match value:
#                 case '保持':
#                     setWidgetEnabled(scaleValueEntry, False)
#                 case _:
#                     setWidgetEnabled(scaleValueEntry, True)

#         app.addBtn('确定', lambda: onBtn())

#         def onBtn():
#             nonlocal result
#             app.destroy()

#         result: str = ''
#         app.run()
#         return result

#     showGui()
