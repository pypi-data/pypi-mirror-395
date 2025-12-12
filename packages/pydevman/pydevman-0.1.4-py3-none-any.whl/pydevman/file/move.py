import logging
import re
from pathlib import Path

from pydevman.common import (
    assert_path_exist_and_is_dir,
    assert_path_exist_and_is_file,
    assert_path_not_exist_and_is_file,
)

log = logging.getLogger(__name__)


def _move_file(src: Path, dst: Path, dry: bool):
    assert_path_exist_and_is_file(src)
    assert_path_not_exist_and_is_file(dst)
    log.debug(f"(dry={dry})移动文件({not dry}: {src} -> {dst}")
    if not dry:
        src.rename(dst)


def move_match_pattern_file(
    src: Path,
    dst: Path = None,
    pattern: str = None,
    dry: bool = True,
    max_cnt: int = 16,
) -> bool:
    """移动指定的文件名"""
    # 校验
    assert_path_exist_and_is_dir(src)
    assert_path_exist_and_is_dir(dst)
    assert pattern is not None
    # 操作
    log.debug(f"提取文件到目录: {src}")
    pat = re.compile(pattern, re.IGNORECASE)
    total_cnt = 0
    for src_path in src.rglob("*"):
        total_cnt += 1
        if total_cnt > max_cnt:
            continue
        if src_path.is_file() and pat.search(src_path.stem):
            dst_path = dst.joinpath(src_path.name)
            _move_file(src_path, dst_path, dry)
    # 总结
    log.debug(f"总共移动文件({not dry}): {total_cnt} 个(最大移动文件为 {max_cnt})")
    return total_cnt


def move_prefix_ext(
    src: Path, dst: Path, *, prefix: re.Pattern, ext: list[str] = None, dry: bool = True
):
    ext_set = set([e.lower() for e in ext])
    cnt = exist = not_match = 0
    for file in src.rglob("*"):
        if not file.is_file():
            continue
        # log.debug(file, prefix.match(file.stem), file.suffix.lower() in ext_set)
        if file.suffix.lower() in ext_set and prefix.match(file.stem):
            dst_file = dst.joinpath(file.name)
            log.debug(f"移动({not dry}) {file} -> {dst_file}")
            if not dst_file.exists():
                cnt += 1
                if not dry:
                    file.rename(dst_file)
            else:
                exist += 1
                log.debug(f"{file} -> {dst_file} 文件已存在，无法移动")
        else:
            log.debug(f"文件={file} 不匹配")
            not_match += 1
    log.debug(
        f"总共移动文件数量={cnt}, 无法移动的文件数量={exist}, 不匹配文件数量={not_match}"
    )
