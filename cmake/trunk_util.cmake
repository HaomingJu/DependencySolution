# ROS 环境
## ROS message path
#ADD_SUBDIRECTORY(TODO)
FIND_PACKAGE(catkin REQUIRED COMPONENTS
    #TODO: other deps package
    roscpp
    std_msgs)

INCLUDE_DIRECTORIES(${catkin_INCLUDE_DIRS})
INCLUDE_DIRECTORIES(${CATKIN_DEVEL_PREFIX}/include)
catkin_package()


EXECUTE_PROCESS(COMMAND python ../.conan_cmd.py)
EXECUTE_PROCESS(COMMAND conan install ./.conanfile -pr=./.profile)

# Conan 依赖
if (EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
    INCLUDE(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    CONAN_BASIC_SETUP()
else()
    message(FATAL_ERROR "The file conanbuildinfo.cmake no exists")
endif()



