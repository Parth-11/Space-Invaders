cmake_minimum_required(VERSION 3.26.4)

project(Space-Invaders)

add_executable(Space-Invaders ${SRC})

target_include_directories(Space-Invaders PUBLIC ${PROJECT_BINARY_DIR})

#           DOWNLOAD ALL THE SUBMODULES
find_package(Git QUIET)
if(GIT_FOUND AND EXISTS "${PROJECT_SOURCE_DIR}/.git")
#Update submodules as needed
    option(GIT_SUBMODULE "Check submodules during build" ON)
    if(GIT_SUBMODULE)
        message(STATUS "Submodule update")
        execute_process(COMMAND ${GIT_EXECUTABLE} Submodule update --init --recursive
                        WORKING_DIRECTORY ${CMAKE_CURRENT_SOURCE_DIR}
                        RESULT_VARIABLE GIT_SUBMOD_RESULT)
        if(NOT GIT_SUBMOD_RESULT EQUAL "0")
            message(FATAL_ERROR "git submodule update --init failed with ${GIT_SUBMOD_RESULT}, please checkout submodules")
        endif()
    endif()
endif()

#           Check all the submodules
if(NOT EXISTS "${PROJECT_SOURCE_DIR}/external/glfw/CMakeLists.txt")
    message(FATAL_ERROR "The glfw submodules was not downloaded! GIT_SUBMODULE was turned off or failed. Please ")
endif()


add_subdirectory(external/glfw)

target_include_directories(${PROJECT_NAME} PUBLIC "external/glfw/include")

target_link_directories(${PROJECT_NAME} PRIVATE "external/glfw/src")

target_link_libraries(${PROJECT_NAME} glfw)

