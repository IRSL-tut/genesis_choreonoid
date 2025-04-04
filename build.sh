set -x

UBUNTU_VER=22.04
ROS_DISTRO=one
BASEIMAGE_TAG=12.1.0-cudnn8-devel-ubuntu${UBUNTU_VER}
CUDA_IMAGE=nvidia/cuda:${BASEIMAGE_TAG}
IRSL_BASE_IMAGE_NAME=repo.irsl.eiiris.tut.ac.jp/irsl_base:cuda_${BASEIMAGE_TAG}_${ROS_DISTRO}
IRSL_SYSTEM_IMAGE_NAME=irsl_system:cuda_${BASEIMAGE_TAG}_${ROS_DISTRO}
OUTPUT_IMAGE_NAME=irsl_system:cuda_${BASEIMAGE_TAG}_${ROS_DISTRO}_genesis

DOCKER_OPT='--progress plain'

# make irsl_base
# cd .irsl_docker_base && 
# DOCKER_FILES="Dockerfile.add_glvnd Dockerfile.add_virtualgl Dockerfile.add_one Dockerfile.add_vcs Dockerfile.add_entrypoint" \
# INPUT_IMAGE=${CUDA_IMAGE} \
# OUTPUT_IMAGE=${IRSL_BASE_IMAGE_NAME} \
# ./build_sequential.sh && 
# cd ..

# make irsl_system
cd .irsl_docker_irsl_system/
INPUT_IMAGE=${IRSL_BASE_IMAGE_NAME} BUILD_ROS=${ROS_DISTRO} BUILD_UBUNTU=${UBUNTU_VER} ./build.sh ${IRSL_SYSTEM_IMAGE_NAME}
cd ..

docker build . ${DOCKER_OPT} --build-arg BASE_IMAGE=${IRSL_SYSTEM_IMAGE_NAME} -f Dockerfile.add_genesis -t ${OUTPUT_IMAGE_NAME} 
