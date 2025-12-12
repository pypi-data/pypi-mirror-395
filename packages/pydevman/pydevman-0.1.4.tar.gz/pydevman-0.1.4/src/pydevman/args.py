from pathlib import Path

import typer
from typing_extensions import Annotated

ARG_SRC = Annotated[
    Path, typer.Argument(help="源文件路径", show_default="默认从剪贴板读取")
]
ARG_DST = Annotated[
    Path, typer.Argument(help="目标文件路径", show_default="默认输出到剪贴板")
]

ARG_FORCE_COVER_DST = Annotated[
    bool,
    typer.Option(
        "--force", "-f", help="是否强制覆盖 DST 目录", show_default="默认不强制"
    ),
]

ARG_VERBOSE = Annotated[
    bool, typer.Option("--verbose", "-v", help="详细输出", show_default=False)
]

ARG_QUIET = Annotated[
    bool, typer.Option("--quiet", "-q", help="静默输出", show_default=False)
]
