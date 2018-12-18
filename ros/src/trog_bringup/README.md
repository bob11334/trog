# Trog Bringup

This package is meant to create a simple, single interface for launch troggie. The current launch file supports two options: `create_map` and `use_move_base`.

## Teleoperation
The simplest start up option is using Trog with teleoperation.

    roslaunch trog_bringup bringup.launch teleop:=true

Troggie will now be able to be controlled according to the following control layout:

    Reading from the keyboard  and Publishing to Twist!
    ---------------------------
    Moving around:
      u    i    o
      j    k    l
      m    ,    .

    q/z : increase/decrease max speeds by 10%
    w/x : increase/decrease only linear speed by 10%
    e/c : increase/decrease only angular speed by 10%
    anything else : stop

Additionaly, the SLAM node starts by default. Therefore, this is a good option for creating a map. 

## Creating a Map

As mentioned above, the SLAM node will start by default. Therefore, in order to create a map, following the above instructions for teleoperation, until you are content with your map.

## Driving Autonomously

In order to let Troggie start driving autonomously, we must launch the move base node along with either the SLAM option or using a premade map.

If you already have a premade map, run

    roslaunch trog_bringup bringup.launch use_move_base:=true create_map:=false map_name:=<name of map> 

Sometimes, you may want to teleop Troggie around while performing SLAM and then begin navigation in your newly mapped environment. If that is the case, run

    roslaunch trog_bringup bringup.launch use_move_base:=true teleop:=true create_map:=true 