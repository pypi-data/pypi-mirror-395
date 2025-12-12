import json
from typing import Final

import pyperclip
from beni import bcolor, btask
from beni.bfunc import syncCall
from rich.console import Console

app: Final = btask.app


@app.command('json')
@syncCall
async def format_json():
    '格式化 JSON （使用复制文本）'
    content = pyperclip.paste()
    try:
        Console().print_json(content, indent=4, ensure_ascii=False, sort_keys=True)
        data = json.loads(content)
        pyperclip.copy(
            json.dumps(data, indent=4, ensure_ascii=False, sort_keys=True)
        )
    except:
        bcolor.printRed('无效的 JSON')
        bcolor.printRed(content)
