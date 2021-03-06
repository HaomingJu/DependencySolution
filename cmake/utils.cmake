# ROS 环境
## ROS message path
if(WITH_ROS)
    #ADD_SUBDIRECTORY(TODO: include message define file folder)
    FIND_PACKAGE(catkin REQUIRED COMPONENTS
        #TODO: other deps package
        roscpp
        std_msgs)
    INCLUDE_DIRECTORIES(${catkin_INCLUDE_DIRS})
    INCLUDE_DIRECTORIES(${CATKIN_DEVEL_PREFIX}/include)
    catkin_package()
endif()


EXECUTE_PROCESS(COMMAND cp ../conan/conanfile.py ./conanfile.py)
EXECUTE_PROCESS(COMMAND python ../conan/conan_cmd.py OUTPUT_VARIABLE LIBINSTALLINFO)
EXECUTE_PROCESS(COMMAND conan install ./.conanfile -pr=./.profile -r JFrogURL)

STRING(REPLACE "\n" "" LIBINSTALLINFO ${LIBINSTALLINFO})
MESSAGE("Install:${LIBINSTALLINFO}")

# Conan 依赖
if (EXISTS "${CMAKE_BINARY_DIR}/conanbuildinfo.cmake")
    INCLUDE(${CMAKE_BINARY_DIR}/conanbuildinfo.cmake)
    CONAN_BASIC_SETUP()
else()
    message(FATAL_ERROR "The file conanbuildinfo.cmake no exists")
endif()

FOREACH(CONAN_SUBLIB_DIRS ${CONAN_LIB_DIRS})
    INSTALL(DIRECTORY ${CONAN_SUBLIB_DIRS}/
        DESTINATION lib)
ENDFOREACH(CONAN_SUBLIB_DIRS)


ADD_CUSTOM_TARGET(create
    COMMAND conan create ./ ${LIBINSTALLINFO} --profile .profile
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR})

ADD_CUSTOM_TARGET(upload
    COMMAND conan upload ${LIBINSTALLINFO} --all -r JFrogURL
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR})

ADD_CUSTOM_TARGET(remove
    COMMAND conan remove ${LIBINSTALLINFO}
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR})

ADD_CUSTOM_TARGET(graph
    COMMAND conan info ./ --graph=file.html
    COMMAND x-www-browser ./file.html
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR})

ADD_CUSTOM_TARGET(search
    COMMAND conan search
    WORKING_DIRECTORY ${CMAKE_BINARY_DIR})
