import asyncio
import getpass
import json
from pathlib import Path
from typing import Final

import pyperclip
import typer
from beni import bcolor, bcrypto, bfile, bpath, btask
from beni.bfunc import syncCall
from beni.binput import genPassword
from rich.console import Console

app: Final = btask.newSubApp('加密（v2）')


@app.command()
@syncCall
async def encrypt_text():
    '加密文本（使用剪贴板内容）'
    content = pyperclip.paste()
    assert content, '剪贴板内容不能为空'
    bcolor.printGreen(content)
    password = genPassword()
    result = bcrypto.encryptText(content, password)
    pyperclip.copy(result)
    print('密文已复制到剪贴板')
    bcolor.printYellow(result)


@app.command()
@syncCall
async def decrypt_text():
    '解密文本（使用剪贴板内容）'
    content = pyperclip.paste().strip()
    bcolor.printYellow(content)
    while True:
        try:
            password = getpass.getpass('输入密码：')
            result = bcrypto.decryptText(content, password)
            print('解密成功')
            bcolor.printGreen(result)
            return
        except KeyboardInterrupt:
            break
        except BaseException:
            pass


@app.command()
@syncCall
async def encrypt_json():
    '生成JSON密文（使用剪贴板内容）'
    content = pyperclip.paste()
    try:
        data = json.loads(content)
    except:
        return btask.abort('错误：剪贴板内容必须是JSON格式', content)
    Console().print_json(data=data, indent=4, ensure_ascii=False, sort_keys=True)
    password = genPassword()
    result = bcrypto.encryptJson(data, password)
    pyperclip.copy(result)
    print('密文已复制到剪贴板')
    bcolor.printYellow(result)


@app.command()
@syncCall
async def decrypt_json():
    '还原JSON密文内容（使用剪贴板内容）'
    content = pyperclip.paste().strip()
    bcolor.printYellow(content)
    while True:
        try:
            password = getpass.getpass('输入密码：')
            data = bcrypto.decryptJson(content, password)
            Console().print_json(data=data, indent=4, ensure_ascii=False, sort_keys=True)
            return
        except KeyboardInterrupt:
            break
        except BaseException:
            pass


@app.command()
@syncCall
async def encrypt_file(
    file: Path = typer.Argument(..., help='指定需要加密的文件')
):
    '加密文件（文件路径使用剪贴板内容）'
    assert file.is_file(), '文件不存在'
    password = genPassword()
    await bcrypto.encryptFile(file, password)
    bcolor.printGreen('OK')


@app.command()
@syncCall
async def decrypt_file(
    file: Path = typer.Argument(..., help='指定需要解密的文件')
):
    '解密文件（文件路径使用剪贴板内容）'
    assert file.is_file(), '文件不存在'
    password = getpass.getpass('输入密码：')
    await bcrypto.decryptFile(file, password)
    bcolor.printGreen('OK')


@app.command()
@syncCall
async def encrypt_path(
    path: Path = typer.Argument(..., help='指定需要加密的目录'),
):
    '加密目录下所有的文件（目录路径使用剪贴板内容）'
    path = path or Path(os.getcwd())
    assert path.is_dir(), '目录不存在'
    password = genPassword()
    errorSet: set[str] = set()

    async def handleFile(file: Path):
        try:
            content = await bfile.readText(file)
            assert not content.startswith(bcrypto.FLAG), '文件已加密'
            content = bcrypto.encryptText(content, password)
            await bfile.writeText(file, content)
        except:
            errorSet.add(str(file))

    fileList = sorted(bpath.listFile(path, True))
    await asyncio.gather(*[handleFile(f) for f in fileList])

    for file in fileList:
        if str(file) in errorSet:
            bcolor.printRed(file)
        else:
            print(file)


@app.command()
@syncCall
async def decrypt_path(
    path: Path = typer.Argument(..., help='指定需要解密的目录'),
):
    '解密目录下所有的文件（目录路径使用剪贴板内容）'
    path = path or Path(os.getcwd())
    assert path.is_dir(), '目录不存在'
    password = getpass.getpass('输入密码：')
    errorSet: set[str] = set()

    async def handleFile(file: Path):
        try:
            content = await bfile.readText(file)
            assert content.startswith(bcrypto.FLAG), '文件未加密'
            content = bcrypto.decryptText(content, password)
            await bfile.writeText(file, content)
        except:
            errorSet.add(str(file))

    fileList = sorted(bpath.listFile(path, True))
    await asyncio.gather(*[handleFile(f) for f in fileList])

    for file in fileList:
        if str(file) in errorSet:
            bcolor.printRed(file)
        else:
            print(file)
