# Author: Jacky Lee
# Datetime: 2025-08-06 17:47:59
# Description: 将 format-json 转换为 inline-json，并复制到剪贴板


import json
import pprint

import inquirer
import pyperclip


def inline():
    pprint.pp("将格式化的 json 转为 单行json，并复制到剪贴板")
    KEY = "json-path"
    questions = [
        inquirer.Path(
            name=KEY,
            message="请给出需要一行的文件路径",
            path_type=inquirer.Path.FILE,
            exists=True,
        )
    ]
    answer = inquirer.prompt(questions)
    try:
        json_str_format = json.load(open(answer.get(KEY), "r"))
        json_str_inline = json.dumps(json_str_format)
        pyperclip.copy(json_str_inline)
        pprint.pp("成功复制到剪贴板")
    except Exception:
        pprint.pp("执行失败")


if __name__ == "__main__":
    inline()
