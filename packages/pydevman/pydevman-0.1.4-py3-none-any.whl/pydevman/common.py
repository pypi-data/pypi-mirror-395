from pathlib import Path


def assert_path_not_exist(path: Path):
    assert path is not None, "参数不能为 None"
    assert isinstance(path, Path), "入参必须是路径"
    # src 必须不存在
    assert not path.exists(), f"${path} 必须不存在，但是该路径存在"


def assert_path_exist(path: Path):
    assert path is not None, "参数不能为 None"
    # src 必须存在
    assert path.exists(), f"${path} 必须存在，但是该路径不存在"


def assert_path_exist_and_is_file(file_path: Path):
    assert_path_exist(file_path)
    # src 必须是文件
    assert file_path.is_file(), f"${file_path} 文件必须是文件"


def assert_path_not_exist_and_is_file(file_path: Path):
    assert_path_not_exist(file_path)
    # src 必须是文件
    assert file_path.is_file(), f"${file_path} 文件必须是文件"


def assert_path_exist_and_is_dir(dir_path: Path):
    assert_path_exist(dir_path)
    # src 必须是文件夹
    assert dir_path.is_dir(), f"${dir_path} 文件必须是文件夹"


def assert_path_not_exist_and_is_dir(dir_path: Path):
    assert_path_not_exist(dir_path)
    # src 必须是文件夹
    assert dir_path.is_dir(), f"${dir_path} 文件必须是文件夹"


def is_empty_directory(dir: Path) -> bool:
    if not dir.is_dir():
        return False
    empty = True
    for item in dir.iterdir():
        # 递归查询子目录
        empty = empty and is_empty_directory(item)
    return empty


def is_dot_path(path: Path) -> bool:
    assert_path_exist(path)
    return path.name.startswith(".")
