CMAKE_MINIMUM_REQUIRED(VERSION 3.0)

# 工程名称
PROJECT(TODO)

# 设定编译类型: Release / Debug
SET(BUILD_TYPE Release)
MESSAGE("BUILD_TYPE: ${BUILD_TYPE}")

# 获取编译指令集类型
SET(ARCH ${CMAKE_SYSTEM_PROCESSOR})
MESSAGE("ARCH: ${ARCH}")

# Uncomment this line, when "[abi:cxx11]" error happen
#ADD_DEFINITIONS(-D_GLIBCXX_USE_CXX11_ABI=0)

# Conan 依赖
INCLUDE(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
CONAN_BASIC_SETUP()

# ROS 环境
## ROS message path
ADD_SUBDIRECTORY(TODO) 
FIND_PACKAGE(catkin REQUIRED COMPONENTS
    #TODO: other deps package
    roscpp
    std_msgs
    )
INCLUDE_DIRECTORIES(${catkin_INCLUDE_DIRS})
INCLUDE_DIRECTORIES(${CATKIN_DEVEL_PREFIX}/include)
catkin_package()
