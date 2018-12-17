# How to connect a Velodyne LiDAR to an Ubuntu Machine
  1. Add an ethernet interface. (Do not set device. Ubuntu will automatically configure this)
  2. Set IP address to 192.168.1.1/200. (192.168.1.201 is reserved)

## Possible bugs

If connected and data is all zero, could be using **Wrong AC Adapter**

If connected, data is correct, but rostopic echo is empty, **disable other network connections**

When trying to view data in RVIZ and you see "Fixed frame (map) does not exist"), 
Call `$ rosrun rviz rviz -f velodyne` instead
