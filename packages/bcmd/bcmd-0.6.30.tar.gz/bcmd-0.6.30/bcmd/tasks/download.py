import asyncio
import os
from pathlib import Path
from typing import Final
from urllib.parse import urlparse
from uuid import uuid4

import pyperclip
import typer
from beni import bcolor, bfile, bhttp, binput, bpath, btask
from beni.bfunc import splitLines, syncCall

app: Final = btask.app


@app.command()
@syncCall
async def download(
    url_file: Path = typer.Option(None, '--file', '-f', help='需要下载的url文件路径，默认使用剪贴板内容'),
    save_path: Path = typer.Option(None, '--path', '-p', help='下载存放目录，默认当前目录'),
    keep_directory: bool = typer.Option(False, '--keep', '-k', help='保持原始目录结构，默认不保持'),
):
    '下载资源资源文件'
    save_path = save_path or Path(os.getcwd())

    if url_file:
        if not url_file.exists():
            btask.abort('指定文件不存在', url_file)
        content = await bfile.readText(url_file)
    else:
        content = pyperclip.paste()
    urlSet = set(splitLines(content))

    for i, url in enumerate(urlSet):
        print(f'{i + 1}. {url}')
    print(f'输出目录：{save_path}')
    await binput.confirm('是否确认？')

    fileSet: set[Path] = set()
    retryUrlSet: set[str] = set()

    async def download(url: str):
        urlPath = urlparse(url).path
        if keep_directory:
            file = bpath.get(save_path, '/'.join([x for x in urlPath.split('/') if x]))
        else:
            file = save_path / Path(urlPath).name
        if file in fileSet:
            file = file.with_stem(f'{file.stem}--{uuid4()}')
        fileSet.add(file)
        try:
            bcolor.printGreen(url)
            await bhttp.download(url, file)
        except:
            retryUrlSet.add(url)
            bcolor.printRed(url)

    await asyncio.gather(*[download(x) for x in urlSet])

    for i in range(4):
        if i > 0:
            print(f'等待重试第 {i} 次')
            await asyncio.sleep(3)
        await asyncio.gather(*[download(x) for x in urlSet])
        if not retryUrlSet:
            break
        urlSet = set(retryUrlSet)
        retryUrlSet.clear()

    if retryUrlSet:
        pyperclip.copy('\n'.join(retryUrlSet))
        bcolor.printYellow('部分下载失败，失败部分已复制到剪贴板')
    else:
        bcolor.printGreen('OK')
