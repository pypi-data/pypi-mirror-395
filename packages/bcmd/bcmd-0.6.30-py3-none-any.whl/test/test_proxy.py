import pytest
from beni import btask


@pytest.mark.asyncio
async def test_proxy():
    result = btask.testCall('proxy', '--help')
    assert result.exit_code == 0
