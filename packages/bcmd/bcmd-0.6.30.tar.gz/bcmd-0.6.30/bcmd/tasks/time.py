import time
from datetime import datetime as Datetime
from datetime import timezone
from typing import Final
from zoneinfo import ZoneInfo

import typer
from beni import bcolor, btask
from beni.bfunc import splitLines, syncCall
from beni.btype import Null

app: Final = btask.app


@app.command('time')
@syncCall
async def showtime(
    args: list[str] = typer.Argument(None),
):
    '''
    格式化时间戳\n
    beni time\n
    beni time 1632412740\n
    beni time 1632412740.1234\n
    beni time 2021-9-23\n
    beni time 2021-9-23 09:47:00\n
    '''
    args = args or []
    btask.assertTrue(len(args) <= 2, '参数过多')
    value1: str | None = args[0] if len(args) >= 1 else None
    value2: str | None = args[1] if len(args) >= 2 else None
    timestamp: float = Null
    if not value1:
        timestamp = time.time()
    else:
        try:
            timestamp = float(value1)
        except:
            try:
                if value2:
                    timestamp = Datetime.strptime(f'{value1} {value2}', '%Y-%m-%d %H:%M:%S').timestamp()
                else:
                    timestamp = Datetime.strptime(f'{value1}', '%Y-%m-%d').timestamp()
            except:
                pass
    if not timestamp:
        bcolor.printRed('参数无效\n')
        bcolor.printRed('使用示例：')
        msgAry = splitLines(str(showtime.__doc__))[1:]
        bcolor.printRed('\n'.join(msgAry))
        return
    print()
    bcolor.printMagenta(timestamp)
    print()
    # localtime = time.localtime(timestamp)
    # tzname = time.tzname[(time.daylight and localtime.tm_isdst) and 1 or 0]
    # bcolor.printx(time.strftime('%Y-%m-%d %H:%M:%S %z', localtime), tzname, colors=[Fore.YELLOW])
    # print()
    datetime_utc = Datetime.fromtimestamp(timestamp, tz=timezone.utc)
    tzname_list = [
        'Australia/Sydney',
        'Asia/Tokyo',
        'Asia/Shanghai',
        'Asia/Kolkata',
        'Africa/Cairo',
        'Europe/London',
        'America/Sao_Paulo',
        'America/New_York',
        'America/Chicago',
        'America/Los_Angeles',
    ]
    for tzname in tzname_list:
        datetime_tz = datetime_utc.astimezone(ZoneInfo(tzname))
        dstStr = ''
        dst = datetime_tz.dst()
        if dst:
            dstStr = f'(DST+{dst})'
        if tzname == 'Asia/Shanghai':
            bcolor.printYellow(f'{datetime_tz} {tzname} {dstStr}')
        else:
            print(f'{datetime_tz} {tzname} {dstStr}')
