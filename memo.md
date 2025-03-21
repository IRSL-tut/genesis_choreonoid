<!-- /bin/bash -c "source /opt/ros/${ROS_DISTRO}/setup.bash && export PATH=/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/xeus/bin:/opt/conda/bin  && catkin config --cmake-args -DBUILD_TEST=ON && catkin config --install && catkin build irsl_choreonoid irsl_choreonoid_ros cnoid_cgal irsl_sim_environments irsl_detection_msgs irsl_raspi_controller --no-status --no-notify -p 1 --verbose"
psutil pydantic tetgen mujoco lxml scikit-image pyglet opencv-python freetype-py numba moviepy
 -->

# リポジトリクローン
```
git clone https://github.com/Hiroaki-Masuzawa/genesis_choreonoid
```

# Image取得方法
いずれかを行えばよい．
## 真面目にビルド
```
cd genesis_choreonoid
./build.sh
```
## repoから取得
たまに古いので注意．
```
docker pull repo.irsl.eiiris.tut.ac.jp/masuzawa_hiroaki_genesis_choreonoid:latest
docker tag repo.irsl.eiiris.tut.ac.jp/masuzawa_hiroaki_genesis_choreonoid:latest genesis_choreonoid:latest
```

# 強化学習のお試し
1. docker 起動
    ```
    cd genesis_choreonoid
    ./run.sh
    ```
1. (初回のみ) パッケージクローン
    ```
    git clone https://github.com/Hiroaki-Masuzawa/humanoid_research_k.git -b add_gs_sample
    cd humanoid_research_k
    git clone https://github.com/IRSL-tut/humanoid_research.git
    ```
1. 学習コード実行
    ```
    cd /userdir/humanoid_research_k/rl_test
    python3 kawada_train.py
    ```
1. 学習結果で歩行
    ```
    python3 kawada_eval.py
    ```
