## 1. 介绍

旨在解决C++库的递归依赖关系.

通过对Conan进行封装，将常用命令封装成与 `cmake/make` 相关, 降低使用难度.

诸如有: `make create` `make upload` `make graph`

## 2. 本地运行环境

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
# Conan version 1.21.0
```

## 3. 远程服务器[可选]

以 Artifactory CE 版 Docker 镜像为依托建立Conan仓库.
```
# 拉取最新 Artifactory Docker 镜像
sudo docker pull docker.bintray.io/jfrog/artifactory-cpp-ce:latest

# 构建系统并运行
sudo docker run --name artifactory-5.0.0 -d -p 8081:8081  docker.bintray.io/jfrog/artifactory-cpp-ce
```
Reference: [Installing with Docker](https://www.jfrog.com/confluence/display/RTF/Installing+with+Docker)


## 4. 使用说明

用户在使用时可以将该工程除 `.git/` 之外的所有文件拷贝到自己的工程文件夹中, 作为 `Init Commit` .

**4.1 配置是否包含 ROS 环境**

```
file: CMakeLists.txt
…
# 编译选项, 是否引入 ROS 环境
OPTION(WITH_ROS "With 'Robot Operating System'" OFF)
MESSAGE("WITH_ROS: ${WITH_ROS}")
…

```
默认为不包含 `OFF` 状态, 如果需要 `ROS` 环境请置为 `ON`

**4.2 配置远程仓库地址以及用户名密码**
将 `build.property.template` 复制为 `build.property`

所有敏感修改均在 `build.property` 中进行, 且不进行Git追踪

```
file: build.property

# Conan - Artifactory
JFrogURL: http://192.168.3.186:8081/artifactory/api/conan/conan-local
UserName: haoming
Password: juhaoming1994115

```
`JFrogURL` -> 远程 Artifactory 地址
`UserName` -> 在 Artifactory 注册的用户名
`Password` -> 密码

建议将此文件置入 `.gitignore` 中, 不作为追踪文件.

将 去除掉密码后的 `build.property.example` 上传

**4.3 设置依赖**
模板为:
```
DepsOnN: libName/libVersion@Namespace:BuildType:LibType:Compiler-CompilerVersion
```
其中部分字段有固定可选项:
```
BuildType: Debug or Release
LibType: Static or Shared
```

例如：

```
file: build.property

DepsOn1:    glog/0.4.0@Vison:Debug:Static:gcc-5.4
DepsOn2:    gflag/2.2.2@Vison:Debug:Static:gcc-5.4

```

设置完成依赖之后, 在之后的编译中将会自动下载这些依赖并与 `Target` 关联

**4.4 下载依赖 & 编译**
```
mkdir build/ && cd build/

cmake ../

make -j4
```
在 `cmake ../` 的过程中, 自动将依赖下载下来, 如下图
```
.conanfile: Installing package
Requirements
  gflag/2.2.2@Vision/Debug-Static-Linux-x86_64-gcc-5.4 from 'JFrogURL' - Downloaded
  glog/0.4.0@Vision/Debug-Static-Linux-x86_64-gcc-5.4 from 'JFrogURL' - Downloaded
Packages
  gflag/2.2.2@Vision/Debug-Static-Linux-x86_64-gcc-5.4:3d8c85c54f7fd2f6b48e52cc88af1bf81a02a93d - Download
  glog/0.4.0@Vision/Debug-Static-Linux-x86_64-gcc-5.4:5a90c1431f2e75760038cccba0a7d63595994658 - Download

```

**4.5 包上传**
当需要上传自己的包时, 只需要遵循规则就可以将依赖递归连接.

有某个工程 `trt` 依赖 `glog`, 则有依赖关系

```
trt ---> glog ---> gflag
```
工程 `trt` 产出 `*.h` / `*.a` 供其他人员使用. 

将编译好的 `*.h/a` 文件放入 `package/` 文件夹中.

配置 `build.property` 文件

```
…
#DepsOn1:    glog/0.4.0@Vision:Debug:Static:gcc-5.4

# 本工程的安装目录
Install: trt/1.0.0@Vision
LibType: Static
BuildType: Debug
Compiler: gcc
CompilerVersion: 5.4
…

```
在 `build/` 执行命令序 `cmake ../` `make create` `make upload` 即可

```
Uploading to remote 'JFrogURL':
Uploading trt/1.0.0@Vision/Debug-Static-Linux-x86_64-gcc-5.4 to remote 'JFrogURL'
Compressing conan_sources.tgz completed [67 files]
Uploading conan_sources.tgz completed [145.92k]
Uploading conanfile.py completed [0.59k]
Uploading conanmanifest.txt completed [5.45k]
Uploaded conan recipe 'trt/1.0.0@Vision/Debug-Static-Linux-x86_64-gcc-5.4' to 'JFrogURL': http://192.168.3.186:8081/artifactory/api/conan/conan-local
Uploading package 1/1: 39b03c85bed0a1cb56951913b822c680576d0a4a to 'JFrogURL'
Compressing conan_package.tgz completed [6 files]
Uploading conaninfo.txt completed [0.66k]
Uploading conanmanifest.txt completed [0.40k]
Built target upload

```



## 5. 命令说明
`make` => 正常编译.

`make create` => 将工程根目录下的 `package/` 文件夹中内容打包.

`make upload` => 将由 `make create` 创建的依赖包上传到JFrogURL指定的地址中.

`make graph` => 绘制出该包的依赖图 `file.html`, 并尝试展示.
