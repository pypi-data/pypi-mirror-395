import getpass
import os
from pathlib import Path
from typing import Final

from beni import bcolor, bcrypto, bexecute, bfile, bpath, btask
from beni.bfunc import syncCall
from typer import Argument, Option

app: Final = btask.newSubApp('项目相关')


@app.command()
@syncCall
async def init(
    path: Path = Argument(Path.cwd(), help='workspace 路径'),
    deep: int = Option(3, '--deep', '-d', help='探索深度'),
):
    '找出项目执行初始化 pnpm install 和 uv sync --all-extras'

    initSubFolder(path, deep)


@app.command()
@syncCall
async def https_cert(
    path: Path = Argument(Path.cwd(), help='https证书路径'),
    no_commit: bool = Option(False, '--no-commit', help='不执行提交操作'),
):
    '更新 https 证书，将证书文件加密并且改名为 {domain}.key 或 {domain}.pem，将下载下来的文件直接放到目录后执行'
    fileList = list(path.glob('**/*.key')) + list(path.glob('**/*.pem'))
    fileList = list(filter(lambda x: x.stem != '{domain}', fileList))
    btask.assertTrue(fileList, '没有找到需要处理的证书文件')

    # 处理密码输入
    while True:
        password = getpass.getpass('请输入密码：')
        if not password:
            continue
        repassword = getpass.getpass('请重复输入密码：')
        if password == repassword:
            break
        else:
            bcolor.printRed('两次密码输入不一样')

    # 文件加密处理
    for file in fileList:
        content = await bfile.readText(file)
        content = bcrypto.encryptText(content, password)
        toFile = file.parent / f'{{domain}}{file.suffix}'
        bcolor.printGreen('更新文件', toFile)
        await bfile.writeText(toFile, content)
        bcolor.printYellow('删除文件', file)
        bpath.remove(file)

    if not no_commit:
        await bexecute.run(f'TortoiseGitProc.exe /command:commit /path:{path}/ /logmsg:"更新https证书文件"')


def initSubFolder(path: Path, deep: int):
    uvLockFile = path / 'uv.lock'
    pnpmLockFile = path / 'pnpm-lock.yaml'
    if uvLockFile.exists():
        with bpath.changePath(path):
            os.system('uv sync --all-extras')
    elif pnpmLockFile.exists():
        with bpath.changePath(path):
            os.system('pnpm install')
    elif deep > 1:
        for subPath in bpath.listDir(path):
            initSubFolder(subPath, deep - 1)
