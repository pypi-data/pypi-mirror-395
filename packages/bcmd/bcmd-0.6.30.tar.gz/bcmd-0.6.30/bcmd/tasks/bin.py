from datetime import datetime
from pathlib import Path
from typing import Final

import typer
from beni import bcolor, bfile, bpath, btask, bzip
from beni.bfunc import splitLines, syncCall
from beni.bqiniu import QiniuBucket
from beni.btype import Null
from prettytable import PrettyTable

from ..common import secret

app: Final = btask.newSubApp('bin 工具')

_PREFIX = 'bin/'


@app.command()
@syncCall
async def download(
    names: list[str] = typer.Argument(None, help="支持多个"),
    file: Path = typer.Option(None, '--file', '-f', help="文件形式指定参数，行为单位"),
    output: Path = typer.Option(Path.cwd(), '--output', '-o', help="本地保存路径"),
    secretValue: str = typer.Option('', '--secret', '-s', help='密钥信息'),
):
    '从七牛云下载执行文件'
    bucket: QiniuBucket = Null
    if file:
        content = await bfile.readText(Path(file))
        names.extend(
            splitLines(content)
        )
    for target in names:
        binFile = output / target
        if binFile.exists():
            bcolor.printYellow(f'已存在 {binFile}')
        else:
            key = f'bin/{target}.zip'
            bucket = bucket or await _getBucket(secretValue)
            await bucket.downloadPrivateFileUnzip(key, output)
            bcolor.printGreen(f'added  {binFile}')


@app.command('list')
@syncCall
async def getList(
    secretValue: str = typer.Option('', '--secret', '-s', help='密钥信息'),
):
    '列出可下载的文件'
    bucket = await _getBucket(secretValue)
    datas = (await bucket.getFileList(_PREFIX, limit=1000))[0]
    datas = [x for x in datas if x.key != _PREFIX and x.key.endswith('.zip')]
    datas.sort(key=lambda x: x.time, reverse=True)
    table = PrettyTable()
    table.add_column(
        bcolor.yellow('文件名称'),
        [x.key[len(_PREFIX):-len('.zip')] for x in datas],
        'l',
    )
    table.add_column(
        bcolor.yellow('上传时间'),
        [datetime.fromtimestamp(x.time / 10000000).strftime('%Y-%m-%d %H:%M:%S') for x in datas],
    )
    print()
    print(table.get_string())


@app.command()
@syncCall
async def upload(
    file: Path = typer.Argument(..., help="本地文件路径"),
    force: bool = typer.Option(False, '--force', '-f', help="强制覆盖"),
    secretValue: str = typer.Option('', '--secret', '-s', help='密钥信息'),
):
    '上传'
    bucket = await _getBucket(secretValue)
    key = f'{_PREFIX}{file.name}.zip'
    if not force:
        if await bucket.getFileStatus(key):
            btask.abort('云端文件已存在，可以使用 --force 强制覆盖')
    with bpath.useTempFile() as f:
        bzip.zipFile(f, file)
        await bucket.uploadFile(key, f)
    bcolor.printGreen('OK')


@app.command()
@syncCall
async def remove(
    key: str = typer.Argument(..., help="云端文件key"),
    secretValue: str = typer.Option('', '--secret', '-s', help='密钥信息'),
):
    bucket = await _getBucket(secretValue)
    await bucket.deleteFiles(f'{_PREFIX}{key}.zip')
    bcolor.printGreen('OK')


# ------------------------------------------------------------------------------------


async def _getBucket(secretValue: str):
    return QiniuBucket(**await secret.getQiniu())
