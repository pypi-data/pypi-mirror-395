from typing import Final

import pyperclip
import typer
from beni import bcolor, btask
from beni.bfunc import syncCall

app: Final = btask.app


@app.command()
@syncCall
async def upgrade(
    name: str = typer.Argument('bcmd', help='要更新的包名'),
):
    '使用 uv 官方源更新指定包到最新版本'
    cmd = f'uv tool upgrade {name} --index https://pypi.org/simple'
    pyperclip.copy(cmd + '\n')
    bcolor.printGreen(cmd)
    bcolor.printGreen('已复制到剪贴板（需要手动执行）')
    bcolor.printGreen('OK')
