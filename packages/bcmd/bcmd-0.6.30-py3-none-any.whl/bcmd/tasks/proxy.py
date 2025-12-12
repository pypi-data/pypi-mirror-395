from typing import Final

import pyperclip
import typer
from beni import bcolor, btask
from beni.bfunc import (isPlatformLinux, isWindowsCmd, isWindowsPowershell,
                        splitLines, syncCall)

app: Final = btask.app


@app.command()
@syncCall
async def proxy(
    port: int = typer.Argument(15236, help="代理服务器端口"),
):

    if isWindowsCmd():
        tips = 'Windows CMD'
        template = templateWindowsCmd
    elif isWindowsPowershell():
        tips = 'Windows PowerShell'
        template = templateWindowsPowershell
    elif isPlatformLinux():
        tips = 'Linux'
        template = templateLinux
    else:
        btask.abort('不支持当前终端，请手动设置代理环境变量')
        return

    lineAry = splitLines(template.format(port))
    lineAry.append('')  # 空行
    lineAry.append('curl https://google.com.hk')
    msg = '\n'.join(lineAry)
    bcolor.printMagenta('\r\n' + msg)
    msg += '\n'  # 多增加一个换行，直接粘贴的时候相当于最后一行也执行完
    pyperclip.copy(msg)
    print()
    bcolor.printYellow(f'当前平台：{tips}')
    bcolor.printYellow(f'代码已复制，需要手动执行')


# ------------------------------------------------------------------------------------


templateWindowsCmd = '''
    set http_proxy=http://localhost:{0}
    set https_proxy=http://localhost:{0}
    set all_proxy=http://localhost:{0}
'''

templateWindowsPowershell = '''
    $env:http_proxy="http://localhost:{0}"
    $env:https_proxy="http://localhost:{0}"
    $env:all_proxy="http://localhost:{0}"
'''

templateLinux = '''
    export http_proxy="http://localhost:{0}"
    export https_proxy="http://localhost:{0}"
    export all_proxy="http://localhost:{0}"
'''
