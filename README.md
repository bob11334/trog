# Trog
Trog is a pilot mobile battery energy storage system that works in integration with the grid to deliver on-demand energy. Trog, or Troggie, is part of [CAEV](http://smartgrid.ucla.edu/CAEV/). Troggie's name is a play on the word troglodyte (i.e. a person who lived in a cave). 

Troggie is pictured [here](documentation/images/troggie.png). A demonstration video can be seen [here](https://www.youtube.com/watch?v=KBPcC1sAmNI&feature=youtu.be)



ToDo List
========

#### Software
* [ ] Configure move_base parameters
* [ ] Get GPS readings


#### Hardware
* [ ] Get Touch Screen Monitor
* [ ] Connect IMU to Jetson via serial port (using Serial1 not Serial_HARDWARE)


User Guide
===
This launches ROS and all necessary nodes. **This must be run before anything.**

    # Get robot up and running
    $ roslaunch trog_bringup bringup.launch

### Teleoperation
In order to remotely operate Troggie, run the follwing command.  control layout will be displayed to your terminal.

    # Teleop
    $  rosrun teleop_twist_keyboard teleop_twist_keyboard.py /cmd_vel:=/trog_velocity_controller/cmd_vel
 
### Mapping
To begin mapping. Please refer to `trog_mapping` for more detailed instructions.
   
    # Begin mapping
    $ roslaunch trog_mapping create_map.launch

### Autnomous navigation
To operate Troggie autonomously within a known map. Please refer to `trog_2dnav` for more detailed instructions.

    # Autonomous navigation within a known map
    $ roslaunch trog_2dnav known_map.launch



