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


EXECUTE_PROCESS(COMMAND python ../.conan_cmd.py OUTPUT_VARIABLE LIBINSTALLINFO)
EXECUTE_PROCESS(COMMAND conan install ./.conanfile -pr=./.profile)
STRING(REPLACE "\n" "" LIBINSTALLINFO ${LIBINSTALLINFO})
MESSAGE("Install:${LIBINSTALLINFO}")

# Conan 依赖
if (EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
    INCLUDE(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    CONAN_BASIC_SETUP()
else()
    message(FATAL_ERROR "The file conanbuildinfo.cmake no exists")
endif()

ADD_CUSTOM_TARGET(create
    COMMAND conan create ../ ${LIBINSTALLINFO} --profile .profile
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR})

ADD_CUSTOM_TARGET(upload
    COMMAND conan upload ${LIBINSTALLINFO} --all
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR})
