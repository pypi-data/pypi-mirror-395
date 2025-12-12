import os
import tkinter as tk
from pathlib import Path
from typing import Final

import typer
from beni import bcolor, bfile, bpath, brun, btask
from beni.bform import BForm
from beni.bfunc import syncCall

from ..common import secret

app: Final = btask.newSubApp('lib 工具')


@app.command()
@syncCall
async def update_version(
    path: Path = typer.Argument(Path.cwd(), help='workspace 路径'),
    isNotCommit: bool = typer.Option(False, '--no-commit', '-d', help='是否提交git'),
):
    '修改 pyproject.toml 版本号'
    file = path / 'pyproject.toml'
    btask.assertTrue(file.is_file(), '文件不存在', file)
    data = await bfile.readToml(file)
    latestVersion: str = data['project']['version']
    vAry = [int(x) for x in latestVersion.split('.')]
    versionList = [
        f'{vAry[0] + 1}.0.0',
        f'{vAry[0]}.{vAry[1] + 1}.0',
        f'{vAry[0]}.{vAry[1]}.{vAry[2] + 1}',
    ]

    class UpdateVersionForm(BForm):

        def __init__(self):
            super().__init__()
            self.versionVar = tk.StringVar(value=versionList[-1])
            self.title('bcmd 版本更新')
            self.addLabel('当前版本号', latestVersion)
            self.addRadioBtnList(
                '请选择新版本',
                versionList,
                var=self.versionVar,
            )
            self.addBtn('确定', self.destroy, focus=True)

        def getResult(self) -> str:
            return self.versionVar.get()

    newVersion: str = UpdateVersionForm().run()
    if not newVersion:
        btask.abort('用户取消操作')
    content = await bfile.readText(file)
    if f"version = '{latestVersion}'" in content:
        content = content.replace(f"version = '{latestVersion}'", f"version = '{newVersion}'")
    elif f'version = "{latestVersion}"' in content:
        content = content.replace(f'version = "{latestVersion}"', f'version = "{newVersion}"')
    else:
        raise Exception('版本号修改失败，先检查文件中定义的版本号格式是否正常')
    await bfile.writeText(file, content)

    # 执行一遍 uv.lock
    with bpath.changePath(path):
        await brun.run('uv lock')

    bcolor.printCyan(newVersion)
    if not isNotCommit:
        msg = f'更新版本号 {newVersion}'
        os.system(
            rf'TortoiseGitProc.exe /command:commit /path:{path} /logmsg:"{msg}"'
        )
    bcolor.printGreen('OK')


@app.command()
@syncCall
async def build(
    path: Path = typer.Argument(Path.cwd(), help='workspace 路径'),
    secretValue: str = typer.Option('', '--secret', '-s', help='密钥信息'),
):
    '发布项目'
    data = await secret.getPypi(secretValue)
    bpath.remove(path / 'dist')
    bpath.remove(
        *list(path.glob('*.egg-info'))
    )
    with bpath.changePath(path):
        _, code = await brun.run(f'uv build')
        btask.assertTrue(not code, '构建失败')
        _, code = await brun.run(f'uv publish -u {data['username']} -p {data['password']}')
        btask.assertTrue(not code, '发布失败')
    bcolor.printGreen('OK')
