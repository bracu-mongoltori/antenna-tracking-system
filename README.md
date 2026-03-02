# Install Dependencies
```
sudo apt install libqt5serialport5-dev libasio-dev ros-humble-diagnostic-updater
cd src/sbg_ros2_driver/
rosdep update
rosdep install --from-path .
cd ../ublox/
rosdep install --from-path .

```

# For running witmotion
```
ros2 launch witmotion_ros wt905_launch.py
```

# For running z9p gps
```
ros2 launch ublox_gps ublox_gps_node_zedf9p-launch.py
```
