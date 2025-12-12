import logging
from pathlib import Path

from send2trash import send2trash

from pydevman.common import assert_path_exist_and_is_dir, is_empty_directory

log = logging.getLogger(__name__)


def del_empty_dir(path: Path, dry):
    if not is_empty_directory(path):
        return
    log.debug(f"删除空目录({not dry}): 目标文件夹='{path}'")
    if not dry:
        send2trash(path)


def del_empty_dir_recursive(dst: Path, dry: bool):
    assert_path_exist_and_is_dir(dst)
    log.debug(f"遍历目录: 目标文件夹='{dst}'")
    for path in dst.iterdir():
        del_empty_dir(path, dry)


def del_dir(dst: Path, dry: bool):
    # 校验
    assert_path_exist_and_is_dir(dst)
    # 记录
    log.debug(f"删除到回收站({not dry}): 目标文件夹='{dst}'")
    # 操作
    if not dry:
        send2trash(dst)
