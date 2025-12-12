import logging
import tempfile
from pathlib import Path
from typing import Callable

import inquirer

from pydevman.query.cache import JsonCache

DEFAULT_TMP_CACHE = Path(tempfile.gettempdir(), "pydevman.global.cache.json")

log = logging.getLogger(__name__)


class QueryCache:
    def __init__(self, path: Path = None):
        self.path = path or DEFAULT_TMP_CACHE
        self.cache = JsonCache(self.path)
        log.debug(f"创建缓存 {self.path}")

    def clear_cache(self): ...

    def query_list(self, func: str, name: str, msg: str, validate: Callable = None):
        choices = self.cache.arg_get_list(func, name)
        if choices:
            res = inquirer.list_input(msg, choices=choices, other=True)
        else:
            res = inquirer.text(msg)
        # if validate and validate(res):
        if validate is None or validate(res):
            self.cache.arg_upsert(func, name, res)
        return res

    def query_check(self, func: str, name: str, msg: str):
        choices = self.cache.arg_get_list(func, name)
        res = inquirer.checkbox(msg, choices=choices, other=True)
        self.cache.arg_upsert_list(func, name, res)
        return res


def confirm() -> bool:
    while True:
        flag = input("是否继续(y/n)...").strip().lower()  # 获取用户输入并处理为小写
        if flag.startswith("y"):  # 如果以'y'开头
            log.info("继续执行...")
            return True
        elif flag.startswith("n"):  # 如果以'n'开头
            log.info("退出程序...")
            return False
        log.info("无效输入，请输入'y'或'n'。")  # 提示用户输入无效，继续询问
