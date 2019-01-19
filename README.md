# Trog
Trog is a pilot mobile battery energy storage system that works in integration with the grid to deliver on-demand energy. Trog, or Troggie, is part of [CAEV](http://smartgrid.ucla.edu/CAEV/). Troggie's name is a play on the word troglodyte (i.e. a person who lived in a cave). 

Troggie is pictured [here](documentation/images/troggie.png). A demonstration video can be seen [here](https://www.youtube.com/watch?v=KBPcC1sAmNI&feature=youtu.be)



ToDo List
========

#### Software
* [ ] Configure move_base parameters
* [ ] Get GPS readings

#### Hardware
* [ ] Connect IMU to Jetson via USB hub
* [ ] Get Touch Screen Monitor



What can Troggie Do?
========

Currently, Troggie is capable of indoor and outdoor navigation. Troggie can navigate autonomously ***within known maps***. 
Meaning, in order to begin autonomous navigation, a map must first be made. Please refer to [trog_bringup](./ros/src/trog_bringup)
for more detailed instructions. 

Components
========
This is an overview of the key components of Troggie:

- Velodyne VLP-16 LiDAR
- Jetson TX2 Developer Kit
- SparkFun 9DoF Razor IMU M0
- RoboteQ SDC2130 - 2x20A 30V Motor Controller with Encoder Input
- Garmin 18x GPS
- Samsung 850 EVO 250GB 2.5-Inch SATA III Internal SSD
- 24V LiFeMnPO4 Prismatic Battery 100Ah
- Superdroid IG52-DB4, 4WD All Terrain Heavy Duty Robot Platform (with customized upper deck)
