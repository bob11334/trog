cmake_minimum_required(VERSION 2.8.3)
project(roboteq_driver)

find_package(catkin REQUIRED COMPONENTS roboteq_msgs roscpp serial)

catkin_package(CATKIN_DEPENDS roboteq_msgs roscpp serial
  INCLUDE_DIRS include
  LIBRARIES roboteq_controller)


add_library(roboteq_controller src/controller.cpp src/channel.cpp)
add_dependencies(roboteq_controller ${PROJECT_NAME}_script)
target_link_libraries(roboteq_controller ${catkin_libraries} ${PROJECT_NAME}_script)

# Build and install binary driver.
include_directories(include ${catkin_INCLUDE_DIRS})
add_subdirectory(mbs)
add_subdirectory(src)

# Mark other files for installation (e.g. launch and bag files, etc.)
install(DIRECTORY launch
  DESTINATION ${CATKIN_PACKAGE_SHARE_DESTINATION}
  )

install(TARGETS roboteq_controller
  ARCHIVE DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  LIBRARY DESTINATION ${CATKIN_PACKAGE_LIB_DESTINATION}
  RUNTIME DESTINATION ${CATKIN_GLOBAL_BIN_DESTINATION}
  )

install(DIRECTORY include/${PROJECT_NAME}
  DESTINATION ${CATKIN_PACKAGE_INCLUDE_DESTINATION}
  )

