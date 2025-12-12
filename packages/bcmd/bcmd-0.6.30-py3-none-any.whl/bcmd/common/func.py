import importlib.resources
from contextlib import contextmanager
from pathlib import Path

from beni import btask


def checkFileOrNotExists(file: Path):
    btask.assertTrue(file.is_file() or not file.exists(), f'必须是文件 {file}')


def checkPathOrNotExists(folder: Path):
    btask.assertTrue(folder.is_dir() or not folder.exists(), f'必须是目录 {folder}')


@contextmanager
def useResources(name: str):
    with importlib.resources.path('bcmd.resources', name) as target:
        yield target
