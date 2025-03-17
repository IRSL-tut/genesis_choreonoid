/bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && export PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/xeus/bin:/opt/conda/bin  && catkin config --cmake-args -DBUILD_TEST=ON && catkin config --install && catkin build irsl_choreonoid irsl_choreonoid_ros cnoid_cgal irsl_sim_environments irsl_detection_msgs irsl_raspi_controller --no-status --no-notify -p 1 --verbose"

psutil pydantic tetgen mujoco lxml scikit-image pyglet opencv-python freetype-py numba moviepy


