import enum
import re


class MatchStrategy(enum, str):
    EQUAL = "equal"
    INCLUDE = "include"
    PREFIX = "prefix"
    SUFFIX = "suffix"
    REGEX = "regex"


STR_LAST_NUM_PATTERN = re.compile(r"(\d+)(?=\D*$)")
DEFAULT_NUM_FILL_FORMAT = "{}-({})"


def match_by_strategy(pattern: str, string: str, strategy: str) -> bool:
    if strategy == MatchStrategy.EQUAL:
        return pattern.lower() == string.lower()
    if strategy == MatchStrategy.INCLUDE:
        return pattern.lower() in string.lower()
    if strategy == MatchStrategy.PREFIX:
        return string.lower().startswith(pattern.lower())
    if strategy == MatchStrategy.SUFFIX:
        return string.lower().endswith(pattern.lower())
    if strategy == MatchStrategy.REGEX:
        return re.match(pattern, string) is not None
    raise NotImplementedError("未定义错误")


def match_str_last_num(string: str):
    """匹配最后一个字符串"""
    _match = re.search(STR_LAST_NUM_PATTERN, string)
    if _match:
        _match.group()
    _num = _match.group()
    if _num is None:
        return
    return _num


def increment_str_last_num(
    s: str, format: str = DEFAULT_NUM_FILL_FORMAT, default_num: int = 1
) -> str:
    num_s = match_str_last_num(s)
    if num_s is None:
        return format.format(s, default_num)
    # 存在前导零
    num = int(num_s)
    increment_str = str(num + 1).zfill(len(num_s))
    # FIXME: sub 类似 match ，但是这里是 search
    s2 = STR_LAST_NUM_PATTERN.sub(increment_str, s)
    return s2
