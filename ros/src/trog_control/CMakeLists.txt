cmake_minimum_required(VERSION 2.8.3)
project(trog_control)

find_package(catkin REQUIRED COMPONENTS
  roboteq_driver
  roboteq_msgs
  controller_manager
  diff_drive_controller
  roboteq_driver
  roboteq_msgs
)
find_package(Boost REQUIRED COMPONENTS chrono)

include_directories(
  include
  ../roboteq/roboteq_driver/include/
  ${catkin_INCLUDE_DIRS}
  ${Boost_INCLUDE_DIRS}
  )

catkin_package(
  INCLUDE_DIRS include
  LIBRARIES trog_hardware roboteq_controller
  DEPENDS Boost
)

  

## Declare a C++ library
add_library(trog_hardware src/trog_hardware.cpp)
target_link_libraries(trog_hardware
  ${catkin_LIBRARIES}
  ${Boost_LIBRARIES}
  )

add_executable(trog_control_node src/trog_control_node.cpp)

target_link_libraries(
  trog_control_node
  ${catkin_LIBRARIES}
  trog_hardware
)

