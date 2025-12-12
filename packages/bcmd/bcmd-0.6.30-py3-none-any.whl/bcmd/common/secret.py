import tkinter as tk
from tkinter import messagebox
from typing import Any, TypedDict

from async_lru import alru_cache
from beni import bcrypto, btask
from beni.bform import BForm


class PypiSecret(TypedDict):
    username: str
    password: str


@alru_cache
async def getPypi(value: str = '') -> PypiSecret:
    return _getData(
        '请输入 PYPI 密钥信息',
        value or 'QbuF2mV/lqovtF5dskZGD7qHknYbNuF2QseWRtWxLZTPrC/jL1tcxV8JEKaRjLsu46PxJZ7zepJwggnUTIWnEAoV5VtgP2/hbuzxxHha8817kR5c65H9fXm8eOal7DYXsUoGPQMnm59UWNXUKjmIaP4sn9nySFlRYqa8sEZSbYQ4N0NL35Dpj1e3wyQxJ+7h2jwKAz50Hh8G4yAM3/js9+NUe4ymts+UXcwsP3ADIBMkzjnFc0lEYg2d+fw0A74XWCvoZPoGqHZR/THUOVNAYxoGgDzP4SPIk1XsmtpxvfO/DpJd/Cg/0fB3MYagGKI1+m6Bxqhvd1I/lf0YbM5y4E4=',
    )


class QiniuSecret(TypedDict):
    bucket: str
    baseUrl: str
    ak: str
    sk: str


@alru_cache
async def getQiniu(value: str = '') -> QiniuSecret:
    return _getData(
        '请输入 七牛云 密钥信息',
        value or 'vNroFKeKklrdcJ89suFm+iyuJsq/cyUB5+QWoeeiMc/J0oSLF9cg5rqbK1IRxF0cCQ8KmkQQhdVa+PI6kuTBhoSH6IviVTylzAOrJywEccz9jWkJkW28Y9Vo4ePZmfWf/j7wdxNB144z234KD8IxJn4lR2A0L9JN5kk1o1/hpcydXL74FNtt03lYL/E3WVcvpUfw37mri2HMYOfUw81dRwW35/hMuQjtq1BBrKrIsSKTHH44tROMcgyvt+Qy292AtDBcsYiZxBKhQtBFPMq/vUs=',
    )


def _getData(title: str, content: str) -> Any:

    class PasswordForm(BForm):
        result: dict[str, Any] = {}

        def __init__(self):
            super().__init__(title=title)
            self.passwordVar = tk.StringVar(value='')
            ary = content.split(' ')
            if len(ary) > 1:
                self.addLabel('提示', ary[0])
            self.addEntry('密码', self.passwordVar, width=30, password=True, focus=True, command=self.onBtn)
            self.addBtn('确定', self.onBtn)

        def onBtn(self):
            try:
                self.result.update(
                    bcrypto.decryptJson(content, self.passwordVar.get())
                )
                self.destroy()
            except:
                messagebox.showerror('密码错误', '密码错误，请重新输入')

        def getResult(self):
            return self.result

    result = PasswordForm().run()

    if result is None:
        btask.abort('用户取消操作')
    else:
        return result
