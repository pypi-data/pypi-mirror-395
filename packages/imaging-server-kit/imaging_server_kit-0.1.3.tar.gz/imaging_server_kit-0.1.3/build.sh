#!/bin/bash

docker build --build-arg PYTHON_VERSION=3.9 -t imaging-server-kit .

# echo "Building image for Python 3.9, GPU-compatible..."
# docker build -t imaging-server-kit:gpu --file Dockerfile-GPU .