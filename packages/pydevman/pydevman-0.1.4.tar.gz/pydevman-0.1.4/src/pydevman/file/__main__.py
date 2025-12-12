"""
create_time: 2025-06-23 17:19:11
author: Jacky Lee
"""

import logging
import re
from pathlib import Path

import inquirer
import typer
from rich.console import Console

from pydevman.args import ARG_SRC
from pydevman.file.copy import copytree
from pydevman.file.delete import del_dir, del_empty_dir_recursive
from pydevman.file.move import move_match_pattern_file, move_prefix_ext
from pydevman.file.stat import SuffixStat, api_stat_cnt, api_stat_prefix

# from pydevman.query.query import query_check, query_list

console = Console()
app = typer.Typer()

log = logging.getLogger(__name__)


@app.command("stat-suffix", help="统计: 根据文件后缀统计文件")
def stat_suffix_query_interaction(src: ARG_SRC):
    # func = "stat-suffix"
    # src = query_list(func, "src", "请输入源文件夹目录")
    # suffix = query_check(func, "suffix", "请输入文件名后缀(非拓展名)")
    console.rule("根据 suffix 文件计数")
    # api_stat_suffix(Path(src), suffix)
    stat = SuffixStat(None)
    stat.stat_paths(src)
    table = stat.build_table()
    console.print(table)


@app.command("stat-cnt", help="统计: 统计文件夹中每个文件的数目")
def stat_cnt_query():
    func = "stat-cnt"
    src = query_list(func, "src", "请输入源文件夹目录")
    console.rule("根据目录统计递归文件")
    api_stat_cnt(Path(src))


@app.command("stat-prefix", help="统计: 根据 PREFIX 统计文件")
def stat_prefix_query():
    func = "stat-prefix"
    src = query_list(func, "src", "请输入源文件夹目录")
    ext = query_check(func, "ext", "请输入文件拓展名")
    console.rule("根据目录统计递归文件前缀")
    api_stat_prefix(Path(src), ext)


@app.command("copy-dir", help="删除: 删除 dst 文件夹内容并复制 src 内容")
def copy_dir_query():
    func = "copy-dir"
    console.rule("复制文件夹 SRC -> DST")
    src = query_list(func, "src", "请输入源文件夹目录")
    dst = query_list(func, "dst", "请输入目标文件夹目录")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    console.rule("高危操作，请谨慎操作⚠️")
    console.log(f"源文件夹='{src}' -> 目标文件夹='{dst}'")
    copytree(Path(src), Path(dst), dry)


@app.command("del-dir", help="删除: 删除 dst 文件夹内容到回收站")
def del_dir_query():
    console.rule("删除文件夹内容")
    func = "del-dir"
    dst = query_list(func, "dst", "请输入目标文件夹目录")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    del_dir(Path(dst), dry)


@app.command("del-empty-dir", help="删除: 删除目录中的空文件夹")
def del_empty_dir_query():
    func = "del-empty-dir"
    console.rule("删除空文件夹")
    dst = query_list(func, "dst", "请输入目标文件夹目录")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    del_empty_dir_recursive(Path(dst), dry)


@app.command("move-prefix-ext", help="删除: 按照文件末尾移动文件")
def move_prefix_ext_query():
    func = "move-prefix-ext"

    src = query_list(func, "src", "请输入源文件夹目录")
    dst = query_list(func, "dst", "请输入目标文件夹目录")
    prefix = query_list(func, "prefix", "请输入文件前缀")
    ext = query_check(func, "ext", "请输入文件拓展名")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    move_prefix_ext(
        Path(src), Path(dst), prefix=re.compile(prefix, re.I), ext=ext, dry=dry
    )


@app.command("move-pattern-dst", help="删除: 将文件移动到根目录")
def move_pattern_dst_query():
    func = "del-dir"
    src = query_list(func, "src", "请输入源文件夹目录")
    dst = Path(query_list(func, "dst", "请输入目标文件夹目录"))
    pattern = query_list(func, "pattern", "请输入正则表达式")
    dry = inquirer.confirm("是否 DRY-RUN 模式", default=True)
    move_match_pattern_file(Path(src), Path(dst), re.compile(pattern), dry)


if __name__ == "__main__":
    app()
