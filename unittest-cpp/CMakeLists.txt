cmake_minimum_required(VERSION 3.14)
project(unittest-cpp)

# GoogleTest requires at least C++14
set(CMAKE_CXX_STANDARD 14)
set(CMAKE_CXX_STANDARD_REQUIRED ON)

include(FetchContent)
FetchContent_Declare(
  googletest
  URL https://github.com/google/googletest/archive/ff233bdd4cac0a0bf6e5cd45bda3406814cb2796.zip
)
# For Windows: Prevent overriding the parent project's compiler/linker settings
set(gtest_force_shared_crt ON CACHE BOOL "" FORCE)
FetchContent_MakeAvailable(googletest)

enable_testing()

# Define test executable name and source file
set(TEST_EXECUTABLE_NAME hello_test)
set(TEST_SOURCE_FILE hello_test.cc)

add_executable(${TEST_EXECUTABLE_NAME} ${TEST_SOURCE_FILE})
target_link_libraries(${TEST_EXECUTABLE_NAME} GTest::gtest_main)

include(GoogleTest)
gtest_discover_tests(${TEST_EXECUTABLE_NAME})