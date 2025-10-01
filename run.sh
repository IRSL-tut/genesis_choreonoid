#!/bin/bash

REPO=repo.irsl.eiiris.tut.ac.jp/
UBUNTU_VER=22.04
ROS_DISTRO=one
BASEIMAGE_TAG=12.1.0-cudnn8-devel-ubuntu${UBUNTU_VER}
CUDA_IMAGE=nvidia/cuda:${BASEIMAGE_TAG}
REPO=repo.irsl.eiiris.tut.ac.jp/
# IRSL_TAG=_latest
IRSL_TAG=''
IRSL_BASE_IMAGE_NAME=${REPO}irsl_base:cuda_${BASEIMAGE_TAG}_${ROS_DISTRO}
IRSL_SYSTEM_IMAGE_NAME=${REPO}irsl_system:cuda_${BASEIMAGE_TAG}_${ROS_DISTRO}
OUTPUT_IMAGE_NAME=${REPO}genesis_with_irsl${IRSL_TAG}:cuda_${BASEIMAGE_TAG}_${ROS_DISTRO}

.irsl_docker_irsl_system/run.sh --image ${OUTPUT_IMAGE_NAME} -w ${PWD}/userdir "$@"
