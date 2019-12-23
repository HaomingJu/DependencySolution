CMAKE_MINIMUM_REQUIRED(VERSION 3.0)

# 工程名称
PROJECT(Trunk)

# 设定编译类型: Release / Debug
SET(BUILD_TYPE Release)
MESSAGE("BUILD_TYPE: ${BUILD_TYPE}")

# 获取编译指令集类型
SET(ARCH ${CMAKE_SYSTEM_PROCESSOR})
MESSAGE("ARCH: ${ARCH}")

# 编译选项, 是否引入 ROS 环境
OPTION(WITH_ROS "With 'Robot Operating System'" OFF)
MESSAGE("WITH_ROS: ${WITH_ROS}")

# Uncomment this line, when "[abi:cxx11]" error happen
#ADD_DEFINITIONS(-D_GLIBCXX_USE_CXX11_ABI=0)

SET(CMAKE_INSTALL_PREFIX ${CMAKE_SOURCE_DIR}/output)

# 引入非常变动脚本
#SET(CMAKE_CXX_COMPILER_VERSION 6)

INCLUDE(${CMAKE_CURRENT_SOURCE_DIR}/cmake/utils.cmake)

