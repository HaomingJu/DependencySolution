## 介绍

旨在解决C++库的依赖关系.

通过对Conan进行封装，将常用命令封装成与 `cmake/make` 相关, 降低使用难度.

诸如有: `make create` `make upload` `make graph`

## 本地运行环境

Python2.7 + pip + Conan + CMake

在 Ubuntu16.0.4 LTS 中 Python2.7为标准配置.

安装 CMake & pip
```
sudo apt-get install cmake
sudo apt-get install python-pip
```
安装conan
```
pip install conan
```

## 远程服务器[可选]

以 Artifactory CE 版 Docker 镜像为依托建立Conan仓库.



## 命令说明
**make** => 正常编译.

**make create** => 将工程根目录下的 `package/` 文件夹中内容打包.

**make upload** => 将由 `make create` 创建的依赖包上传到JFrogURL指定的地址中.

**make graph** => 绘制出该包的依赖图 `file.html`, 并尝试展示.
