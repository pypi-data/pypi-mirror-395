import logging
from abc import ABC, abstractmethod
from collections import OrderedDict
from pathlib import Path

from pydevman.common import assert_path_exist_and_is_dir
from pydevman.file.iter import iter_dirs, iter_files
from pydevman.helper.table import build_table

log = logging.getLogger(__name__)


class BaseStat(ABC):
    def __init__(self, max_depth: int = 16):
        self._max_depth = max_depth
        self.res = {}

    @abstractmethod
    def handle_path(self, path: Path) -> bool: ...

    # 遍历
    def stat_paths(self, root: Path):
        for file in iter_files(root, self._max_depth):
            if self.handle_path(file) is False:
                break

    def build_table(self): ...


class SuffixStat(BaseStat):
    def __init__(self, suffix_set: set[str], max_cnt: int = 4096, max_depth: int = 16):
        super().__init__(max_depth=max_depth)
        self._max_cnt = max_cnt
        self._cur_cnt = 0
        self._suffix_set = suffix_set
        self._res = {}

    def _match_suffix(self, suffix: str):
        if self._suffix_set is None:
            return True
        return suffix in self._suffix_set

    def handle_path(self, path):
        self._cur_cnt += 1
        if self._cur_cnt > self._max_cnt:
            return False
        _suffix = path.suffix
        if path.is_file() and self._match_suffix(_suffix):
            cur = self._res.setdefault(_suffix, 0)
            self._res[_suffix] = cur + 1
        return True

    def build_table(self):
        header = ["文件类型", "数量"]
        rows = [(k, str(v)) for k, v in self._res.items()]
        rows.append(("TOTAL", str(self._cur_cnt)))
        table = build_table("根据 SUFFIX 计数", header, rows)
        return table


def api_stat_prefix(root: Path, ext: list[str], max_depth: int = 16):
    res = {}
    ext_set = set(e.lower() for e in ext)

    for file in iter_files(root, max_depth):
        file: Path
        if file.suffix.lower() in ext_set:
            prefix = file.stem.split("_")[0]
            val = res.get(prefix, 0)
            res[prefix] = val + 1

    header = ["前缀 PREFIX", "数目"]
    rows = [(k, str(v)) for k, v in res.items()]
    table = build_table("根据目录统计文件", header, rows)
    log.info(table)


def api_stat_info_in_dir(path: Path) -> tuple[int, int]:
    assert path.is_dir()
    file_cnt = dir_cnt = other_cnt = 0
    for item in path.iterdir():
        if item.is_file():
            file_cnt += 1
        elif item.is_dir():
            dir_cnt += 1
        else:
            other_cnt += 1
    return file_cnt, dir_cnt, other_cnt


def api_stat_cnt(root: Path, max_depth: int = 16):
    res: dict[Path, tuple] = OrderedDict()

    def adder(path: Path, f, d, o):
        parts = path.relative_to(root).parts
        for i in range(len(parts)):
            _path = root.joinpath(*parts[:i])
            _f, _d, _o = res.get(_path, (0, 0, 0))
            res[_path] = (f + _f, d + _d, o + _o)

    for dir in iter_dirs(root, max_depth=max_depth):
        f, d, o = api_stat_info_in_dir(dir)
        res[dir] = (f, d, o)
        adder(dir, f, d, o)
    header = ["路径", "文件数", "目录数", "其他文件"]
    rows = [
        (str(k.relative_to(root)), str(f), str(d), str(o))
        for k, (f, d, o) in res.items()
    ]
    table = build_table("根据目录统计文件", header, rows)
    log.info(table)


def stat(src: Path, max_depth: int = 4):
    """统计文件夹个数大小，文件个数大小"""
    assert_path_exist_and_is_dir(src)
    # 用队列解决
    total_file = 0
    total_folder = 0
    queue = [(src, 0)]
    while queue:
        p, level = queue.pop()
        if level > max_depth:  # 如果递归深度大于最大深度，跳出递归
            continue
        try:
            for p in p.iterdir():
                if p.is_dir():
                    total_folder += 1
                    queue.append((p, level + 1))  # 递归进入下一层
                else:
                    total_file += 1
        except PermissionError:
            log.info(f"无权限访问，跳过... {p}")
            continue
        except Exception as e:
            log.error("未知错误...")
            log.exception(e)
    # print(f"文件夹 : {src} ")
    # print(f"文件数量   : {total_file}")
    # print(f"文件夹数量 : {total_folder}")
    return src, total_file, total_folder


class CounterStat(BaseStat):
    def __init__(self, suffix_set: set[str], max_cnt: int = 4096, max_depth: int = 16):
        super().__init__(max_depth=max_depth)
        self._max_cnt = max_cnt
        self._cur_cnt = 0
        self._suffix_set = suffix_set
        self._res = {}

    def handle_path(self, path):
        self._cur_cnt += 1
        if self._cur_cnt > self._max_cnt:
            return False
        _suffix = path.suffix
        if path.is_file():
            cur = self._res.setdefault(_suffix, 0)
            self._res[_suffix] = cur + 1
        return True

    def build_table(self):
        header = ["文件类型", "数量"]
        rows = [(k, str(v)) for k, v in self._res.items()]
        rows.append(("TOTAL", str(self._cur_cnt)))
        table = build_table("根据 SUFFIX 计数", header, rows)
        return table
