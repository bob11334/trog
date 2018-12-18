# Trog Mapping
Trog uses Gmapping SLAM to build a map. This performs both localization and mapping. There are two launch files. The first `slam.launch` should be used to create maps, and the second, `known_map.launch`, should be used for loading an existing map and localizing within it. 


## Creating a Map
First run the following command to begin mapping

    roslaunch trog_mapping slam.launch

After you are satistfied with you map, to save it run

    rosrun mapserver mapsaver -f <name of map>

This will save a `.yaml` and `.pgm` file in the `./maps` directory. 

## Loading from an exsiting map
Simply run 
    
    roslaunch trog_mapping known_map.launch map_name:=<map to load>

This will load the requested map and start amcl for localization within that map.
