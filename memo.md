
# 実行時のメモ

## リポジトリクローン
```
git clone --recursive https://github.com/Hiroaki-Masuzawa/genesis_choreonoid
```

## Image取得方法
いずれかを行えばよい．
### 真面目にビルド
```
cd genesis_choreonoid
./build.sh
```
<!-- ### repoから取得
たまに古いので注意．
```
docker pull repo.irsl.eiiris.tut.ac.jp/masuzawa_hiroaki_genesis_choreonoid:latest
docker tag repo.irsl.eiiris.tut.ac.jp/masuzawa_hiroaki_genesis_choreonoid:latest genesis_choreonoid:latest
``` -->

## 強化学習のお試し
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
## CHIDORIで学習
1. (初回のみ) パッケージクローン
    ```
    cd genesis_choreonoid/userdir/humanoid_research_k/rl_test
    git clone https://github.com/IRSL-tut/chidori_description
    cp conv_urdf.py chidori_description/urdf/.
    ```
1. dockerの起動
    ```
    ./run.sh
    ```
1. (初回のみ)URDFの変換
    ```
    cd humanoid_research_k/rl_test/chidori_description/urdf
    python3 conv_urdf.py
    cd /userdir
    ```
1. 学習コード実行
    ```
    python3 chidori_train.py
    ```
1. 学習結果で歩行
    ```
    python3 chidori_eval.py
    ```



# 本docker作成時のメモ書き
## 作成時のポリシー
- [genesisのDokcerfile](https://github.com/Hiroaki-Masuzawa/genesis_choreonoid/blob/fba95fffe1424cb71dae0e75e0ac2587217d9e86/Dockerfile.add_genesis#L22)を参考にCUDA, cuDNN, torchのバージョンを選定
    - pytochについては[ここ](https://pytorch.org/get-started/previous-versions/)で検索をする．
- 最初は自前でgenesis -> ros -> chorenoidの順で入れていたが，後から[irsl_base](https://github.com/IRSL-tut/irsl_docker_base/), [irsl_system](https://github.com/IRSL-tut/irsl_docker_irsl_system)のdockerfileを使いros -> chorenoid -> genesisの順に変更

## 起きたエラーと対処について 
- numpyのバージョンについて　(最新だと固定不要になったためメモだけ残す)
    - numpyのバージョンが2.x.xだとgenesisが動作しないため，それに依存するライブラリを調べてバージョン固定でインストールした．
        - pipの依存関係はpipdeptreeでわかる．(参考 : https://qiita.com/tttmurakami/items/b407dc4cc558564882bf )
- コード実行時に"import genesis"とすると"ImportError: /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libmeshlab-common.so: undefined symbol: _ZdlPvm, version Qt_5"とエラーが出力される．
    - インストール順で発生したりしなかったりしたため，環境変数とエラーが出た共有ライブラリの参照を比較．(pipとaptのリストも比較したが特段情報がなかった)
        1. genesis -> ros -> chorenoidの時（インポートでエラーが出ない）
            ```
            $ set|grep PATH
            CMAKE_PREFIX_PATH=/choreonoid_ws/install:/opt/ros/one
            JUPYTER_PATH=/jupyter
            LD_LIBRARY_PATH=/choreonoid_ws/install/lib:/opt/ros/one/lib:/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/opt/xeus/lib
            PATH=/choreonoid_ws/install/bin:/opt/ros/one/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/xeus/bin:/user_scripts
            PKG_CONFIG_PATH=/choreonoid_ws/install/lib/pkgconfig:/opt/ros/one/lib/pkgconfig
            PYTHONPATH=/choreonoid_ws/install/lib/python3/dist-packages:/opt/ros/one/lib/python3/dist-packages:/choreonoid_ws/install/lib/choreonoid-2.3/python
            ROS_PACKAGE_PATH=/choreonoid_ws/install/share:/opt/ros/one/share
            ```
            ```
            $ ldd /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libmeshlab-common.so
            linux-vdso.so.1 (0x00007ffc6cd21000)
            libQt5OpenGL.so.5 => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libQt5OpenGL.so.5 (0x000071be86c00000)
            libQt5Widgets.so.5 => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libQt5Widgets.so.5 (0x000071be86000000)
            libQt5Xml.so.5 => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libQt5Xml.so.5 (0x000071be85a00000)
            libexternal-glew.so => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libexternal-glew.so (0x000071be870bb000)
            libQt5Gui.so.5 => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libQt5Gui.so.5 (0x000071be84e00000)
            libQt5Core.so.5 => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libQt5Core.so.5 (0x000071be84400000)
            libGL.so.1 => /usr/lib/x86_64-linux-gnu/libGL.so.1 (0x000071be87018000)
            libstdc++.so.6 => /usr/lib/x86_64-linux-gnu/libstdc++.so.6 (0x000071be869d4000)
            libm.so.6 => /usr/lib/x86_64-linux-gnu/libm.so.6 (0x000071be86f31000)
            libgcc_s.so.1 => /usr/lib/x86_64-linux-gnu/libgcc_s.so.1 (0x000071be86f11000)
            libc.so.6 => /usr/lib/x86_64-linux-gnu/libc.so.6 (0x000071be85dd7000)
            libpthread.so.0 => /usr/lib/x86_64-linux-gnu/libpthread.so.0 (0x000071be86f0a000)
            libz.so.1 => /usr/lib/x86_64-linux-gnu/libz.so.1 (0x000071be86eee000)
            libicui18n.so.56 => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libicui18n.so.56 (0x000071be83c00000)
            libicuuc.so.56 => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libicuuc.so.56 (0x000071be83600000)
            libicudata.so.56 => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libicudata.so.56 (0x000071be81a00000)
            libdl.so.2 => /usr/lib/x86_64-linux-gnu/libdl.so.2 (0x000071be86ee7000)
            libgthread-2.0.so.0 => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libgthread-2.0.so.0 (0x000071be86ee1000)
            libglib-2.0.so.0 => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libglib-2.0.so.0 (0x000071be8689d000)
            /lib64/ld-linux-x86-64.so.2 (0x000071be8728c000)
            libGLdispatch.so.0 => /usr/lib/x86_64-linux-gnu/libGLdispatch.so.0 (0x000071be85d1f000)
            libGLX.so.0 => /usr/lib/x86_64-linux-gnu/libGLX.so.0 (0x000071be86eab000)
            libpcre.so.3 => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libpcre.so.3 (0x000071be85cab000)
            libX11.so.6 => /usr/lib/x86_64-linux-gnu/libX11.so.6 (0x000071be858c0000)
            libxcb.so.1 => /usr/lib/x86_64-linux-gnu/libxcb.so.1 (0x000071be86e81000)
            libXau.so.6 => /usr/lib/x86_64-linux-gnu/libXau.so.6 (0x000071be86e7b000)
            libXdmcp.so.6 => /usr/lib/x86_64-linux-gnu/libXdmcp.so.6 (0x000071be86e73000)
            libbsd.so.0 => /usr/lib/x86_64-linux-gnu/libbsd.so.0 (0x000071be86e59000)
            libmd.so.0 => /usr/lib/x86_64-linux-gnu/libmd.so.0 (0x000071be86890000)
            ```
        2. ros -> chorenoid -> genesisの時（インポートでエラーが発生）
            ```
            $ set|grep PATH
            CMAKE_PREFIX_PATH=/choreonoid_ws/install:/opt/ros/one
            JUPYTER_PATH=/jupyter
            LD_LIBRARY_PATH=/choreonoid_ws/install/lib:/opt/ros/one/lib:/usr/lib/x86_64-linux-gnu:/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/usr/local/nvidia/lib:/usr/local/nvidia/lib64:/opt/xeus/lib
            LIBRARY_PATH=/usr/local/cuda/lib64/stubs
            PATH=/choreonoid_ws/install/bin:/opt/ros/one/bin:/usr/local/nvidia/bin:/usr/local/cuda/bin:/usr/local/sbin:/usr/local/bin:/usr/sbin:/usr/bin:/sbin:/bin:/opt/xeus/bin:/user_scripts
            PKG_CONFIG_PATH=/choreonoid_ws/install/lib/pkgconfig:/opt/ros/one/lib/pkgconfig
            PYTHONPATH=/choreonoid_ws/install/lib/python3/dist-packages:/opt/ros/one/lib/python3/dist-packages:/choreonoid_ws/install/lib/choreonoid-2.3/python
            ROS_PACKAGE_PATH=/choreonoid_ws/install/share:/opt/ros/one/share
            ```
            ```
            $ ldd /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libmeshlab-common.so
            linux-vdso.so.1 (0x00007ffce2d05000)
            libQt5OpenGL.so.5 => /usr/lib/x86_64-linux-gnu/libQt5OpenGL.so.5 (0x000070096e98b000)
            libQt5Widgets.so.5 => /usr/lib/x86_64-linux-gnu/libQt5Widgets.so.5 (0x000070096e2ca000)
            libQt5Xml.so.5 => /usr/lib/x86_64-linux-gnu/libQt5Xml.so.5 (0x000070096e284000)
            libexternal-glew.so => /usr/local/lib/python3.10/dist-packages/pymeshlab/lib/libexternal-glew.so (0x000070096e1af000)
            libQt5Gui.so.5 => /usr/lib/x86_64-linux-gnu/libQt5Gui.so.5 (0x000070096dacf000)
            libQt5Core.so.5 => /usr/lib/x86_64-linux-gnu/libQt5Core.so.5 (0x000070096d570000)
            libGL.so.1 => /usr/lib/x86_64-linux-gnu/libGL.so.1 (0x000070096d4e9000)
            libstdc++.so.6 => /usr/lib/x86_64-linux-gnu/libstdc++.so.6 (0x000070096d2bd000)
            libm.so.6 => /usr/lib/x86_64-linux-gnu/libm.so.6 (0x000070096d1d6000)
            libgcc_s.so.1 => /usr/lib/x86_64-linux-gnu/libgcc_s.so.1 (0x000070096d1b6000)
            libc.so.6 => /usr/lib/x86_64-linux-gnu/libc.so.6 (0x000070096cf8c000)
            libpng16.so.16 => /usr/lib/x86_64-linux-gnu/libpng16.so.16 (0x000070096cf51000)
            libz.so.1 => /usr/lib/x86_64-linux-gnu/libz.so.1 (0x000070096cf35000)
            libharfbuzz.so.0 => /usr/lib/x86_64-linux-gnu/libharfbuzz.so.0 (0x000070096ce66000)
            libmd4c.so.0 => /usr/lib/x86_64-linux-gnu/libmd4c.so.0 (0x000070096ce54000)
            libdouble-conversion.so.3 => /usr/lib/x86_64-linux-gnu/libdouble-conversion.so.3 (0x000070096ce3d000)
            libicui18n.so.70 => /usr/lib/x86_64-linux-gnu/libicui18n.so.70 (0x000070096cb0e000)
            libicuuc.so.70 => /usr/lib/x86_64-linux-gnu/libicuuc.so.70 (0x000070096c913000)
            libpcre2-16.so.0 => /usr/lib/x86_64-linux-gnu/libpcre2-16.so.0 (0x000070096c889000)
            libzstd.so.1 => /usr/lib/x86_64-linux-gnu/libzstd.so.1 (0x000070096c7ba000)
            libglib-2.0.so.0 => /usr/lib/x86_64-linux-gnu/libglib-2.0.so.0 (0x000070096c680000)
            /lib64/ld-linux-x86-64.so.2 (0x000070096eae6000)
            libGLdispatch.so.0 => /usr/lib/x86_64-linux-gnu/libGLdispatch.so.0 (0x000070096c5c6000)
            libGLX.so.0 => /usr/lib/x86_64-linux-gnu/libGLX.so.0 (0x000070096c592000)
            libfreetype.so.6 => /usr/lib/x86_64-linux-gnu/libfreetype.so.6 (0x000070096c4ca000)
            libgraphite2.so.3 => /usr/lib/x86_64-linux-gnu/libgraphite2.so.3 (0x000070096c4a3000)
            libicudata.so.70 => /usr/lib/x86_64-linux-gnu/libicudata.so.70 (0x000070096a885000)
            libpcre.so.3 => /usr/lib/x86_64-linux-gnu/libpcre.so.3 (0x000070096a80d000)
            libX11.so.6 => /usr/lib/x86_64-linux-gnu/libX11.so.6 (0x000070096a6cd000)
            libbrotlidec.so.1 => /usr/lib/x86_64-linux-gnu/libbrotlidec.so.1 (0x000070096a6bf000)
            libxcb.so.1 => /usr/lib/x86_64-linux-gnu/libxcb.so.1 (0x000070096a695000)
            libbrotlicommon.so.1 => /usr/lib/x86_64-linux-gnu/libbrotlicommon.so.1 (0x000070096a672000)
            libXau.so.6 => /usr/lib/x86_64-linux-gnu/libXau.so.6 (0x000070096a66a000)
            libXdmcp.so.6 => /usr/lib/x86_64-linux-gnu/libXdmcp.so.6 (0x000070096a662000)
            libbsd.so.0 => /usr/lib/x86_64-linux-gnu/libbsd.so.0 (0x000070096a64a000)
            libmd.so.0 => /usr/lib/x86_64-linux-gnu/libmd.so.0 (0x000070096a63d000)
            ```
        libQt5xxxx.soなどの一部の共有ライブラリのファイルがLD_LIBRARY_PATHによって違っていたため起きていたと推測．LD_LIBRARY_PATHを変えると他に影響が出て，かつ，あたりの範囲が不明なのでソースでインストールすることにした．