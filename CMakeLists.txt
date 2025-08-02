cmake_minimum_required(VERSION 3.10)
project(FuzzyScan)

set(CMAKE_CXX_STANDARD 17)

include_directories(
    third_party/imgui
    third_party/imgui/backends
    third_party/ssdeep
    ${CMAKE_SOURCE_DIR}/third_party/glfw/include
    /mingw64/include
)

link_directories(${CMAKE_SOURCE_DIR}/third_party/glfw/lib
/mingw64/lib
)

add_executable(fuzzyscan
    src/main.cpp
    src/fuzzy.cpp
    third_party/imgui/imgui.cpp
    third_party/imgui/imgui_draw.cpp
    third_party/imgui/imgui_tables.cpp
    third_party/imgui/imgui_widgets.cpp
    third_party/imgui/backends/imgui_impl_win32.cpp
    third_party/imgui/backends/imgui_impl_opengl3.cpp
)

set(FUZZY_LIB_PATH "${CMAKE_SOURCE_DIR}/third_party/ssdeep/fuzzy.lib")

target_link_libraries(fuzzyscan
    PRIVATE
    opengl32
    glu32
    user32
    gdi32
    shell32
    dwmapi
    glfw3
    "${FUZZY_LIB_PATH}"
)
