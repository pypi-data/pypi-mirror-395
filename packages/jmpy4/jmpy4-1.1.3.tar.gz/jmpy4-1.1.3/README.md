# jmpy

![](https://img.shields.io/badge/python-3.0-brightgreen)

## 简介

将python代码一键加密为so或pyd。支持单个文件加密，整个项目加密。

Fork from: https://github.com/Boris-code/jmpy.git

支持多进程，修复 bug

## 安装

    pip install jmpy4

## 使用方法

    jmpy -i "xxx project dir" [-o output dir] -w 8

加密后的文件默认存储在 dist/project_name/ 下

## Tips

加密过程会产生如下警告，不影响使用，可以忽略

    'build\bdist.win-amd64' does not exist -- can't clean it