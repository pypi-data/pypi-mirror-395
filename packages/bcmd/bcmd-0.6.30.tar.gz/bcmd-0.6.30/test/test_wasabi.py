from uuid import uuid4

import pytest
from beni import bfile, bpath, btask


@pytest.mark.asyncio
async def test_wasabi():
    with bpath.useTempPath() as tempPath:
        target = tempPath / uuid4().hex
        file = target / uuid4().hex
        content = uuid4().hex
        password = uuid4().hex
        await bfile.writeText(file, content)

        result = btask.testCall('wasabi', 'zip', target.as_posix(), '--password', password)
        assert result.exit_code == 0
        assert target.is_file(), '生成加密文件失败'

        newPassword = uuid4().hex
        result = btask.testCall('wasabi', 'change-pass', target.as_posix(), '--password', password, '--new-password', newPassword)
        assert result.exit_code == 0
        assert target.is_file(), '修改密码失败'

        result = btask.testCall('wasabi', 'unzip', target.as_posix(), '--password', newPassword)
        assert result.exit_code == 0
        assert target.is_dir(), '解密文件失败'
        assert await bfile.readText(file) == content, '解密文件内容不一致'
