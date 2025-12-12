# PY pydevman MAN

开发者的 python 工具集

## 如何安装

```sh
pip install pydevman
# 或者
uv add pydevman
```

```sh
# 测试命令
pydevman echo hello
# 查看所有子应用
pydevman --help
# 查看某个子应用的所有命令
pydevman json --help
# 查看某个子应用某个命令的使用方法
pydevman json parse --help
```

## 子应用 ECHO

此应用主要用于测试使用

## 子应用 JSON

此应用主要和 json 相关

```sh
# 将剪贴板中的内容递归解析，并输出到剪贴板
pydevman json parse
```

类似的工具 [jq 1.8 Manual](https://jqlang.org/manual/)

## 子应用 FILE
