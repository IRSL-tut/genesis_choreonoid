#!/bin/bash

.irsl_docker_irsl_system/run.sh --image irsl_system:cuda_12.1.0-cudnn8-devel-ubuntu22.04_one_genesis -w ${PWD}/userdir "$@"