import webbrowser
from typing import Final

import pyperclip
import typer
from beni import bcolor, btask
from beni.bfunc import crcStr, syncCall

app: Final = btask.newSubApp('Amazon 工具')


@app.command()
@syncCall
async def open_asin_list(
    asin: list[str] = typer.Argument(None, help='支持多个 ASIN 使用空格间隔，如果不填写则使用剪贴板内容')
):
    '根据 ASIN 打开多个 Amazon 多个产品页'
    asin = asin or []
    if not asin:
        content = pyperclip.paste().strip()
        for line in content.splitlines():
            line = line.strip()
            if line:
                asin.extend(line.split(' '))
        asin = [x for x in asin if x]
    btask.assertTrue(asin, '没有提供任何 ASIN')
    for x in asin:
        webbrowser.open_new_tab(f'https://www.amazon.com/dp/{x}')


@app.command()
@syncCall
async def make_part_number():
    '根据 SKU 生成 Part Number，这里使用粘贴板里的内容作为参数，每行代表1个SKU'
    content = pyperclip.paste().replace('\r', '')
    ary = content.split('\n')
    resultList: list[str] = []
    for item in ary:
        item = item.strip()
        result = ''
        if item and '-' in item:
            key = '-'.join(item.split('-')[:-1])
            result = crcStr(key).upper()
        resultList.append(result)
        print(item, '=>', result)
    outputContent = '\n'.join(resultList)
    pyperclip.copy(outputContent)
    bcolor.printGreen('Part Number 已复制到剪贴板')
    bcolor.printGreen('OK')
