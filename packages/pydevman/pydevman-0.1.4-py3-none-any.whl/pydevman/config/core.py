from os import PathLike
from typing import Dict, Union

from dynaconf import Dynaconf


def create_config(arg: Union[PathLike, Dict], env: str = None):
    """单文件配置导入，可以导入 json,toml,yaml 等文件"""
    if isinstance(arg, Dict):
        return Dynaconf(settings=arg)
    assert isinstance(arg, PathLike), "只能是单文件"
    if env is None:
        return Dynaconf(
            # root_path=root_path,
            settings_files=arg,
            # merge_enabled=True,
        )
    return Dynaconf(
        # root_path=root_path,
        environments=True,
        default_env=env,
        settings_files=arg,
        # merge_enabled=True,
    )


def merge_config(config: Dynaconf, arg: Union[PathLike, Dict], env: str = None):
    """TODO: 合并两个配置"""
    raise NotImplementedError


def merge_dict(base_dict, new_dict):
    """TODO: 合并两个字典"""
    raise NotImplementedError
