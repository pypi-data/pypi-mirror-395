import logging
from pathlib import Path

import pyperclip
from rich.console import Console

from pydevman.common import assert_path_exist_and_is_file

log = logging.getLogger(__name__)
console = Console()


def from_clipboard_or_file(src: Path) -> str:
    if src is None:
        return pyperclip.paste()
    assert_path_exist_and_is_file(src)
    return src.read_text()


def to_clipboard_or_file(dst: Path, content: str, force: bool, quiet=False) -> bool:
    # 写入剪贴板
    console.quiet = quiet
    if dst is None:
        pyperclip.copy(content)
        console.print("已复制到剪贴板")
        return
    # dst 非空,路径
    if dst.exists() and force:
        dst.write_text(content)
        console.print(f"已写入文件 {dst.name}")
    else:
        console.print(f"目标文件 {dst.name} 已存在，使用 -f 强制输出")
