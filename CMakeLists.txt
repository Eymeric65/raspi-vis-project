cmake_minimum_required(VERSION 3.10)

# Project name
project(CameraCaptureLibcamera)

# Find OpenCV and GStreamer packages
find_package(OpenCV REQUIRED)
find_package(PkgConfig REQUIRED)
#pkg_check_modules(GSTREAMER REQUIRED gstreamer-1.0)
#pkg_check_modules(GSTREAMER_APP REQUIRED gstreamer-app-1.0)

# Include directories
include_directories(${OpenCV_INCLUDE_DIRS})
include_directories(${GSTREAMER_INCLUDE_DIRS})
include_directories(${GSTREAMER_APP_INCLUDE_DIRS})

# Source file
set(SOURCE_FILES opencv-test-vid.cpp)

# Add executable
add_executable(${PROJECT_NAME} ${SOURCE_FILES})

# Link libraries
target_link_libraries(${PROJECT_NAME} ${OpenCV_LIBS})
target_link_libraries(${PROJECT_NAME} ${GSTREAMER_LIBRARIES})
target_link_libraries(${PROJECT_NAME} ${GSTREAMER_APP_LIBRARIES})