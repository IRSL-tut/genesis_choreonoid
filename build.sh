#!/bin/bash

set -e

ROS_DISTRO_="one"
CUR_UBUNTU="22.04"

DOCKER_OPT='--progress plain'

_REPO=${REPO:-repo.irsl.eiiris.tut.ac.jp/}
XEUS_IMG=${_REPO}xeus:${CUR_UBUNTU}

TARGET_IMG="genesis_choreonoid"


DOCKER_FILE=Dockerfile.build_system.vcstool

set -x

echo "Build Image: ${TARGET_IMG}"

docker build . --progress=plain -f Dockerfile.make_base  \
       -t build_temp/build_system:0

# -e がirsl_entrypoint.shやirsl_enryrc に残るのでmake_baseにコピペで対処
# docker build .irsl_docker_base/. ${DOCKER_OPT} -f .irsl_docker_base/Dockerfile.add_entrypoint \
#         --build-arg BASE_IMAGE=build_temp/build_system:0 \
#         -t build_temp/build_system:1

docker build .irsl_docker_irsl_system/. ${DOCKER_OPT} -f .irsl_docker_irsl_system/Dockerfile.add_xeus  \
       --build-arg BASE_IMAGE=build_temp/build_system:0 --build-arg BUILD_IMAGE=${XEUS_IMG} \
       -t build_temp/build_system:2

docker build .irsl_docker_irsl_system/. ${DOCKER_OPT} -f .irsl_docker_irsl_system/Dockerfile.add_extra_files  \
       --build-arg BASE_IMAGE=build_temp/build_system:2 \
       -t build_temp/build_system:3

docker build .irsl_docker_irsl_system/. ${DOCKER_OPT} -f .irsl_docker_irsl_system/${DOCKER_FILE} \
       --build-arg BASE_IMAGE=build_temp/build_system:3 \
       -t ${TARGET_IMG}