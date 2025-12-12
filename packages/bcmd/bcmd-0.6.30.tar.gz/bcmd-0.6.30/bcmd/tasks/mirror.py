from __future__ import annotations

import platform
from typing import Final

import typer
from beni import bcolor, bfile, bpath, btask
from beni.bfunc import syncCall, isPlatformWindows, isPlatformLinux

app: Final = btask.app


@app.command()
@syncCall
async def mirror(
    disabled: bool = typer.Option(False, '--disabled', '-d', help="是否禁用"),
):
    '设置镜像'

    # 根据不同的系统平台，设置 pip 的配置文件路径
    if isPlatformWindows():
        file = bpath.user('pip/pip.ini')
    elif isPlatformLinux():
        file = bpath.user('.pip/pip.conf')
    else:
        btask.abort('暂时不支持该平台', platform.system())
        return

    if disabled:
        bpath.remove(file)
        bcolor.printRed('删除文件', file)
    else:
        content = _content.strip()
        await bfile.writeText(file, content)
        bcolor.printYellow(file)
        bcolor.printMagenta(content)
    bcolor.printGreen('OK')


# ------------------------------------------------------------------------------------

_content = '''
[global]
index-url = https://mirrors.aliyun.com/pypi/simple
'''
