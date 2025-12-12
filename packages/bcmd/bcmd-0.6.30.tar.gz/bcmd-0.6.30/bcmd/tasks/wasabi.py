import getpass
import stat
from pathlib import Path
from typing import Final

import typer
from beni import bcolor, bcrypto, bfile, bpath, btask, bzip
from beni.bfunc import shuffleSequence, syncCall
from beni.binput import genPassword

app: Final = btask.newSubApp('Wasabi 工具')

SEP = f'{chr(852)}{chr(322)}{chr(470)}'.encode()
MAX_ENCRYPT_SIZE = 199 * 1024


@app.command()
@syncCall
async def unzip(
    target: Path = typer.Argument(Path.cwd(), help='加密文件'),
    password: str = typer.Option('', '--password', '-p', help='密码'),
):
    '解压缩加密文件成目录'
    assert target.is_file(), f'不是文件 {target}'
    password = password or getpass.getpass('请输入密码: ')
    with bpath.useTempFile() as tempFile:
        data = await bfile.readBytes(target)
        if SEP not in data:
            data = bcrypto.decrypt(data, password)
        else:
            partA, partB = data.split(SEP)
            partA = bcrypto.decrypt(partA, password)
            data = partA + partB
        data = shuffleSequence(data)
        await bfile.writeBytes(tempFile, data)
        tempPath = target.with_suffix('.tmp')
        await bzip.sevenUnzip(tempFile, tempPath)

        # 调整文件权限，完全擦除
        target.chmod(stat.S_IWRITE)
        await bpath.removeSecure(target)

        bpath.move(tempPath, target)
        bcolor.printGreen('OK')


@app.command()
@syncCall
async def zip(
    target: Path = typer.Argument(Path.cwd(), help='输出目录'),
    password: str = typer.Option('', '--password', '-p', help='密码'),
):
    '将目录压缩成加密文件'
    target = target.absolute()
    assert target.is_dir(), f'不是目录 {target}'
    password = password or genPassword()
    with bpath.useTempFile() as tempFile:
        await bzip.sevenZipFolder(tempFile, target)
        data = await bfile.readBytes(tempFile)
        bpath.remove(tempFile)  # 为了安全所以立即删除
        data = shuffleSequence(data)
        if len(data) < MAX_ENCRYPT_SIZE:
            data = bcrypto.encrypt(data, password)
        else:
            partA, partB = data[:MAX_ENCRYPT_SIZE], data[MAX_ENCRYPT_SIZE:]
            partA = bcrypto.encrypt(partA, password)
            data = partA + SEP + partB
        tempZipFile = target.with_suffix('.tmp')
        await bfile.writeBytes(tempZipFile, data)

        # 调整目录权限，完全擦除
        target.chmod(stat.S_IWRITE)
        for file in target.glob('**/*'):
            file.chmod(stat.S_IWRITE)
        await bpath.removeSecure(target)

        bpath.move(tempZipFile, target)

    bcolor.printGreen('OK')


@app.command()
@syncCall
async def change_pass(
    file: Path = typer.Argument(Path.cwd(), help='加密文件'),
    password: str = typer.Option('', '--password', '-p', help='密码'),
    new_password: str = typer.Option('', '--new-password', '-n', help='新密码'),
):
    with bpath.useTempPath() as tempPath:
        target = tempPath / file.name
        bpath.copy(file, target)
        unzip(target, password)
        zip(target, new_password)
        bpath.copy(target, file)
