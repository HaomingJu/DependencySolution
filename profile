[settings]
    # TODO: 指定编译环境与指令集
    os=Linux
    arch=x86_64
    # TODO: 指定上传文件所用编译器与编译器版本
    compiler=gcc
    compiler.version=5.4
    # TODO: 指定上传文件的编译类型 Release or Debug
    build_type=Release

    os_build=Linux
    arch_build=x86_64
    compiler.libcxx=libstdc++

[options]

[build_requires]
    # TODO: 指定该项目所依赖包路径. 诸如
    # gflag/0.4.0@Common/Trunk

[env]
    # TODO: 指定编译器路径
    CC=/usr/bin/gcc-5
    CXX=/usr/bin/g++-5
