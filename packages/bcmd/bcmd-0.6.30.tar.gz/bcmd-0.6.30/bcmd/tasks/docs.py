import datetime
import json
import pickle
import tkinter as tk
from contextlib import asynccontextmanager
from pathlib import Path
from tkinter import messagebox
from typing import Any, Final
from uuid import uuid4

import paramiko
from beni import bcolor, bcrypto, bfile, bpath, brun, btask, bzip
from beni.bform import BForm
from beni.bfunc import syncCall
from typer import Argument, Option

app: Final = btask.newSubApp('Vitepress 网站相关')
conf: dict[str, Any] = {}
isUpload: bool = False
password: str = ''
now = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

projectPath = bpath.get('')
docsPath = bpath.get('')
vitepressDistPath = bpath.get('')
distPath = bpath.get('')
deployPath = bpath.get('')
zipFile = bpath.get('')


@app.command()
@syncCall
async def build(
    path: Path = Argument(Path.cwd(), help='workspace 路径'),
    build_cmd: str = Option('docs:build', help='vitepress 构建命令'),
):
    '发布'
    with bpath.useTempPath(True) as tempPath:
        await init(path)
        await userInput()
        await vitepressBuild(tempPath / 'site', build_cmd)
        await makeDeploy(tempPath / 'deploy')
        for file in bpath.listPath(tempPath):
            await bzip.sevenZip(zipFile, file)
        if isUpload:
            await upload()
    bcolor.printGreen('OK')


async def init(path: Path):
    global projectPath, docsPath, vitepressDistPath, distPath, deployPath, zipFile

    # 初始化目录路径
    projectPath = path
    docsPath = projectPath / 'docs'
    vitepressDistPath = docsPath / '.vitepress/dist'
    distPath = projectPath / 'dist'
    deployPath = projectPath / 'deploy'

    # 清空打包用到的目录
    bpath.remove(distPath)
    bpath.make(distPath)
    bpath.remove(vitepressDistPath)

    # 更新配置
    projectTomlFile = projectPath / 'project.toml'
    if not projectTomlFile.exists():
        btask.abort('部署文件不存在', projectTomlFile)
    conf.update(await bfile.readToml(projectTomlFile))

    # 整理特殊的字段
    zipFile = distPath / f'{conf['domain']}_{now}.7z'
    conf['upload_file_name'] = zipFile.name
    conf['temp_path'] += f'/{uuid4()}'


async def userInput():
    global isUpload, password

    class BuildForm(BForm):
        def __init__(self):
            super().__init__(title='发布网站')
            self.varIsUpload = tk.BooleanVar(value=True)
            self.varPassword = tk.StringVar(value='')
            self.addLabel('网站', conf['domain'])
            self.addCheckBox('上传服务器', '', self.varIsUpload)
            self.addEntry('请输入密码', self.varPassword, width=20, command=self.onBtn, password=True, focus=True)
            self.addBtn('确定', self.onBtn)

        def onBtn(self):
            password = self.varPassword.get()
            try:
                bcrypto.decryptJson(conf['server_info'], password)
                self.destroy()
            except:
                messagebox.showerror('密码错误', '密码错误，请重新输入')

        def getResult(self):
            return self.varIsUpload.get(), self.varPassword.get()

    result = BuildForm().run()
    if not result:
        btask.abort('用户取消操作')
    isUpload, password = result

    # 将里面加密的内容解密
    for k, v in conf.items():
        if str(v).startswith(bcrypto.FLAG):
            conf[k] = bcrypto.decryptText(v, password)


async def vitepressBuild(outputPath: Path, build_cmd: str):
    with bpath.changePath(projectPath):
        await brun.run('pnpm install')
        await brun.run(f'pnpm {build_cmd}')
        bpath.copy(vitepressDistPath, outputPath)


async def makeDeploy(outputPath: Path):
    bpath.copy(deployPath, outputPath)

    # 删除配置里面加密和删除非字符串的配置，剩下的内容用于替换文件名和文件内容
    dataDict: dict[str, Any] = pickle.loads(pickle.dumps(conf))
    for k in list(dataDict.keys()):
        v = dataDict[k]
        if not isinstance(v, str):
            del dataDict[k]

    # 文件名以及内容调整
    fileList = bpath.listFile(outputPath, True)
    for file in fileList:

        # 替换文件名
        toFile = str(file)
        for k, v in dataDict.items():
            toFile = toFile.replace(f'{{{k}}}', str(v))
        if toFile != str(file):
            file.rename(toFile)
            file = bpath.get(toFile)

        # 替换文件内容
        content = await bfile.readText(file)
        oldContent = content
        if content.startswith(bcrypto.FLAG):
            content = bcrypto.decryptText(content, password)
        for k, v in dataDict.items():
            content = content.replace(f'{{{k}}}', str(v))
        if oldContent != content:
            await bfile.writeText(file, content)

    # 将 Scrips 里面的文件都抽离到 dist 目录
    scriptsPath = outputPath / 'Scripts'
    for file in bpath.listFile(scriptsPath):
        bpath.move(file, distPath / f'{conf['domain']}_{now}_{file.stem}{file.suffix}')
    bpath.remove(scriptsPath)


@asynccontextmanager
async def sshClient():
    client = paramiko.SSHClient()
    client.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    with bpath.useTempFile() as tempFile:
        await bfile.writeText(tempFile, conf['server_key'])
        client.connect(
            **json.loads(conf['server_info']),
            key_filename=str(tempFile),
        )
        yield client
        client.close()


async def upload():
    async with sshClient() as client:

        def executeCmd(cmd: str):
            _, stdout, _ = client.exec_command(f"bash -lc '{cmd}'")
            print(stdout.read().decode())

        sftp = client.open_sftp()
        for file in bpath.listFile(distPath):
            executeCmd(f'mkdir -p {conf['temp_path']}')
            sftp.put(str(file), f'{conf['temp_path']}/{file.name}')
        shFile = list(distPath.glob('*.sh'))[0]
        executeCmd(f'sh {conf['temp_path']}/{shFile.name}')
        executeCmd(f'rm -rf {conf['temp_path']}')
        sftp.close()
