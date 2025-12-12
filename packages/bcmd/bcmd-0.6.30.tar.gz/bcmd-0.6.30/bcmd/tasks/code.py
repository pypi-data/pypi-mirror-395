import asyncio
import os
from pathlib import Path
from typing import Final

import typer
from beni import bfile, bpath, btask
from beni.bcolor import printGreen, printMagenta, printYellow
from beni.bfunc import syncCall

app: Final = btask.newSubApp('code 工具')


@app.command()
@syncCall
async def tidy_tasks(
    tasks_path: Path = typer.Argument(Path.cwd(), help="tasks 路径"),
):
    '整理 task 项目中的 tasks/__init__.py'

    initFile = tasks_path / '__init__.py'
    btask.assertTrue(initFile.is_file(), '文件不存在', initFile)
    files = bpath.listFile(tasks_path)
    files = [x for x in files if not x.name.startswith('_')]
    contents = [f'from . import {x.stem}' for x in files]
    contents.insert(0, '# type: ignore')
    contents.append('')
    content = '\n'.join(contents)
    oldContent = await bfile.readText(initFile)
    if oldContent != content:
        await bfile.writeText(
            initFile,
            content,
        )
        printYellow(initFile)
        printMagenta(content)
    printGreen('OK')


@app.command()
@syncCall
async def tidy_modules(
    modules_path: Path = typer.Argument(Path.cwd(), help="modules_path 路径"),
):
    '整理 fastapi 项目中的 modules/__init__.py'

    importContents: list[str] = []
    managerContents: list[str] = []

    xxdict: dict[str, set[Path]] = {}
    for file in sorted(modules_path.glob('**/*Manager.py')):
        if file.parent == modules_path:
            subName = '.'
        elif file.parent.parent == modules_path:
            subName = f'.{file.parent.stem}'
        else:
            continue
        xxdict.setdefault(subName, set()).add(file)
    for subName in sorted(xxdict.keys()):
        files = sorted(xxdict[subName])
        importContents.append(f'from {subName} import {", ".join([x.stem for x in files])}')
    managerContents.extend([f'    {x.stem},' for x in sorted([y for x in xxdict.values() for y in x])])

    managerContents = [x for x in managerContents if x]
    contents = [
        '\n'.join(importContents),
        'managers = [\n' + '\n'.join(managerContents) + '\n]',
    ]
    content = '\n\n'.join(contents) + '\n'
    file = modules_path / '__init__.py'
    printYellow(str(file))
    printMagenta(content)
    await bfile.writeText(file, content)
    printGreen('OK')


@app.command()
@syncCall
async def gen_init_py(
    workspace_path: Path = typer.Argument(Path.cwd(), help='workspace 路径'),
):
    '递归生成 __init__.py 文件'

    ignoreSubDirs = [
        '.git',
        'venv',
        'node_modules',
        '.pytest_cache',
        '__pycache__',
        '.vscode',
    ]
    folderList = bpath.listDir(workspace_path, True)
    # 剔除子目录是这些的文件 .git venv ...
    folderList = [x for x in folderList if not any([y in x.parts for y in ignoreSubDirs])]
    for folder in folderList:
        pyInitFile = folder / '__init__.py'
        if not pyInitFile.exists():
            printYellow(pyInitFile)
            await bfile.writeText(pyInitFile, '')
    printGreen('OK')


@app.command()
@syncCall
async def to_lf(
    path: Path = typer.Option(None, '--path', help='指定目录或具体图片文件，默认当前目录'),
):
    '将所有文件转换为 LF 格式'
    ignoreSubDirs = [
        '.git',
        'venv',
        'node_modules',
        '.pytest_cache',
        '__pycache__',
    ]
    path = path or Path(os.getcwd())
    files = bpath.listFile(path, True)
    # 剔除子目录是这些的文件 .git venv ...
    files = [x for x in files if not any([y in x.parts for y in ignoreSubDirs])]

    async def convertFile(file: Path):
        try:
            content = await bfile.readText(file)
            if '\r\n' in content:
                content = content.replace('\r\n', '\n')
                await bfile.writeText(file, content)
                printYellow(file)
        except:
            pass

    await asyncio.gather(*[convertFile(file) for file in files])
    printGreen('OK')
