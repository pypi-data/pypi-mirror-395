"""
create_time: 2025-03-20
author: Jacky Lee
description: 文件夹复制操作
1. 首先删除目标文件夹
2. 然后复制源文件夹
"""

# ⚠️高危操作
# TODO 测试如果 DST 存在文件不删除，直接复制过去会怎么样
import logging
import shutil
from pathlib import Path

from send2trash import send2trash

from pydevman.common import assert_path_exist_and_is_dir

log = logging.getLogger(__name__)


def copytree(src: Path, dst: Path, dry: bool):
    """复制文件夹

    Args:
        src (Path): 源文件夹
        dst (Path): 目标文件夹
        dry (bool): 是否干运行
    """
    log.debug(f"dry={dry}")
    if dry:
        return
    assert_path_exist_and_is_dir(src)

    if dst.exists():
        log.debug(f"目标文件夹='{dst}': 删除到回收站")
        send2trash(dst)
    try:
        shutil.copytree(src, dst, dirs_exist_ok=True)
        log.debug(f"目标文件夹='{dst}': 复制完成")
    except FileExistsError:
        log.debug(f"目标文件夹='{dst}': 已经存在同名文件，复制失败")


def copytree_struct(src: Path, dst: Path, max_depth: int = 4, file: bool = True):
    """复制文件夹结构，文件内容为 0 KB

    Args:
        src (Path): 源文件夹
        dst (Path): 目标文件夹
        max_depth (int, optional): 默认递归深度. 默认是 4.
        file (bool, optional): 是否复制文件. 默认是 True.
    """
    # 校验：防止 dst 覆盖 src
    assert src.exists(), f"{src} 源文件夹不存在，请检查路径"
    assert not dst.exists(), f"{dst} 目标文件夹已存在，请检查路径"
    # 创建空目录
    dst.mkdir(parents=True)
    log.debug(f"准备复制 {src} -> {dst}, max_depth={max_depth}, file={file}")

    # if not confirm():
    #     log.info("退出程序...")
    #     return
    queue = [(src, 0)]
    while queue:
        dir, level = queue.pop()
        if level > max_depth:  # 如果递归深度大于最大深度，跳出递归
            continue
        try:
            for p in dir.iterdir():
                # 文件夹
                parts = p.relative_to(src).parts
                dst_path = dst.joinpath(*parts)
                if p.is_dir():
                    queue.append((p, level + 1))  # 递归进入下一层
                    dst_path.mkdir()
                    continue
                # 文件
                if p.is_file() and file:
                    log.info(f"复制 {p} -> {dst_path}")
                    dst_path.touch()
        except PermissionError:
            log.info(f"无权限访问，跳过... {p}")
            continue
