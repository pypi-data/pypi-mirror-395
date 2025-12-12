import asyncio

from beni import btask

from .tasks import *


def run():
    btask.options.lock = 0  # 允许多开
    asyncio.run(btask.main())
