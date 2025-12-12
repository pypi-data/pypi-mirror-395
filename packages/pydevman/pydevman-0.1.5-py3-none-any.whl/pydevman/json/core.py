"""
Author: Jacky Lee
Date: 2025-10-22
Description: 递归解析 json 代码
"""

import json
import logging
from abc import ABC, abstractmethod
from typing import Union

log = logging.getLogger(__name__)


class AbstractHandler(ABC):
    @abstractmethod
    def handle_dict(self, arg: dict): ...

    @abstractmethod
    def handle_list(self, arg: list): ...

    @abstractmethod
    def handle_str(self, arg: str): ...

    @abstractmethod
    def handle_int(self, arg: int): ...

    @abstractmethod
    def handle_float(self, arg: float): ...

    @abstractmethod
    def handle_bool(self, arg: bool): ...

    @abstractmethod
    def handle_none(self, arg): ...

    @abstractmethod
    def handle(self, arg): ...


class DefaultHandler(AbstractHandler):
    def handle_dict(self, arg):
        log.debug("handle dict...")
        return arg

    def handle_list(self, arg):
        log.debug("handle list...")
        return arg

    def handle_str(self, arg):
        log.debug("handle str...")
        return arg

    def handle_int(self, arg):
        log.debug("handle int...")
        return arg

    def handle_float(self, arg):
        log.debug("handle float...")
        return arg

    def handle_none(self, arg):
        log.debug("handle none...")
        return arg

    def handle(self, arg):
        log.debug("handle default ...")
        if arg is None:
            return self.handle_none(arg)
        if isinstance(arg, list):
            return self.handle_list(arg)
        elif isinstance(arg, dict):
            return self.handle_dict(arg)
        elif isinstance(arg, str):
            return self.handle_str(arg)
        # isinstance(False, int) >> true
        # isinstance(True, int) >> true
        # issubclass(bool, int) >> true
        elif isinstance(arg, int):
            return self.handle_int(arg)
        elif isinstance(arg, float):
            return self.handle_float(arg)
        else:
            raise TypeError(
                "Argument is not any of List, Object, String, Number or None."
            )


class RecursiveHandler(DefaultHandler):
    """递归解析,参数为 dict, list, str, int, float, None 中的一种"""

    def handle_dict(self, arg):
        _di = {}
        for k, v in arg.items():
            _di[k] = self.handle(v)
        return _di

    def handle_list(self, arg):
        _list = []
        for _, item in enumerate(arg):
            tmp = self.handle(item)
            _list.append(tmp)
        return _list

    def handle_str(self, arg) -> Union[dict, list, str, int, float, None]:
        try:
            # 如果可以被解析
            shallow_parsed = json.loads(arg)
        except json.JSONDecodeError:
            return arg
        deep_parsed = self.handle(shallow_parsed)
        return deep_parsed


class DelHtmlTagHandler(DefaultHandler):
    def handle_str(self, arg):
        import bs4

        return bs4.BeautifulSoup(arg, "html.parser").get_text()


class JsonProcessor:
    def __init__(self):
        self.handlers: list[AbstractHandler] = []

    def register(self, handler: AbstractHandler):
        self.handlers.append(handler)

    def process(self, text: str):
        try:
            _text = json.loads(text)
        except json.JSONDecodeError as e:
            log.error(f'无法解析字符串, text="{text}"')
            raise e

        for handler in self.handlers:
            _text = handler.handle(_text)
        return _text

    def dump_readable(self, obj: Union[str, dict, list]):
        return json.dumps(obj, indent=2, ensure_ascii=False)

    def dump_inline(self, obj: Union[str, dict, list]):
        return json.dumps(obj, ensure_ascii=False)
