import json
import logging

import typer
from rich.console import Console
from typing_extensions import Annotated

from pydevman.args import ARG_DST, ARG_FORCE_COVER_DST, ARG_QUIET, ARG_SRC, ARG_VERBOSE
from pydevman.helper.interactive import from_clipboard_or_file, to_clipboard_or_file
from pydevman.json.api import (
    api_dump_json_to_str,
    api_format_json_inline,
    api_parse_str_to_json,
)
from pydevman.log import config_log

app = typer.Typer()
console = Console()

ARG_RECURSIVE = Annotated[
    bool,
    typer.Option("--recursive", "-r", help="是否递归去转义", show_default="默认递归"),
]

ARG_DEL_HTML_TAG = Annotated[
    bool,
    typer.Option("--del-tag", help="是否递归去转义", show_default="默认递归"),
]


@app.command("parse", help="解析字符串为 json(默认递归去转义)")
def recursive_parse_json(
    src: ARG_SRC = None,
    dst: ARG_DST = None,
    recursive: ARG_RECURSIVE = False,
    del_tag: ARG_DEL_HTML_TAG = False,
    force: ARG_FORCE_COVER_DST = False,
    verbose: ARG_VERBOSE = False,
    quiet: ARG_QUIET = False,
):
    # TODO: 解决模板代码的问题
    # TODO: 解决日志配置的问题
    console.quiet = quiet
    if verbose:
        config_log(logging.DEBUG)
    dump_content = None
    try:
        origin_content = from_clipboard_or_file(src)
        dump_content = api_parse_str_to_json(
            origin_content, recursive=recursive, del_html_tag=del_tag
        )
        to_clipboard_or_file(dst, dump_content, force, quiet)
        console.print(dump_content)
    except AssertionError as e:
        console.print("断言错误", e)
    except json.JSONDecodeError as e:
        console.print("无法解析字符串为 json", e)
    except Exception as e:
        console.print("未知异常", e)
        console.print("使用 -v 详细输出")


@app.command("inline", help="将 json 变为单行")
def format_json_inline(
    src: ARG_SRC = None,
    dst: ARG_DST = None,
    force: ARG_FORCE_COVER_DST = False,
    verbose: ARG_VERBOSE = False,
    quiet: ARG_QUIET = False,
):
    console.quiet = quiet
    if verbose:
        config_log(logging.DEBUG)
    dump_content = None
    try:
        origin_content = from_clipboard_or_file(src)
        dump_content = api_format_json_inline(origin_content)
        to_clipboard_or_file(dst, dump_content, force, quiet)
        # FIXME 解决 console 无法打印列表的问题
        console.print(dump_content)
    except AssertionError as e:
        console.print("断言错误", e)
    except json.JSONDecodeError as e:
        console.print("无法解析字符串为 json", e)
    except Exception as e:
        console.print("未知异常", e)
        console.print("使用 -v 详细输出")


@app.command("dump", help="将 json 序列化")
def dump_json_to_str(
    src: ARG_SRC = None,
    dst: ARG_DST = None,
    force: ARG_FORCE_COVER_DST = False,
    verbose: ARG_VERBOSE = False,
    quiet: ARG_QUIET = False,
):
    console.quiet = quiet
    if verbose:
        config_log(logging.DEBUG)
    dump_content = None
    try:
        origin_content = from_clipboard_or_file(src)
        dump_content = api_dump_json_to_str(origin_content)
        to_clipboard_or_file(dst, dump_content, force, quiet)
        console.print(dump_content)
    except AssertionError as e:
        console.print("断言错误", e)
    except json.JSONDecodeError as e:
        console.print("无法解析字符串为 json", e)
    except Exception as e:
        console.print("未知异常", e)
        console.print("使用 -v 详细输出")


if __name__ == "__main__":
    app()
