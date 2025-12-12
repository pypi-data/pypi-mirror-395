import csv
from itertools import islice
from typing import Generator, Iterable


def generate_csv_row(stream: Iterable, skip: int) -> Generator[dict, None, None]:
    """生成 csv 内容

    Args:
        stream (Iterable): 文件流或字符串列表
        skip (int): 跳过的行数

    Yields:
        dict: 生成字典内容
    """
    _iter = islice(stream, skip, None)
    _dict = csv.DictReader(_iter)
    for _line_dict in _dict:
        yield _line_dict
