## 说明

`test` 子工程依赖 `glog`


```
file: build.property
DepsOn1:    glog/0.4.0@Vision:Debug:Static:gcc-5.4

# 本工程的安装目录
Install: trt/1.0.0@Vision
LibType: Static
BuildType: Debug
Compiler: gcc
CompilerVersion: 5.4

```

生成 `test.h` 和 `test.so`

在`CMakeLists.txt` 中配置安装路径
```
INSTALL(TARGETS test1
    LIBRARY DESTINATION package/lib)

INSTALL(FILES test.h
    DESTINATION package/include)
```

执行 `cmake ../ && make install` 之后, 将 `output/package` 连接到 `./package`

```
ln -s ./output/package ./package
```

此时再进行上传
```
make create
make upload
```
