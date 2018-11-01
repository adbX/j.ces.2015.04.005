#!/bin/bash

# Helper script to make OpenQBMM, to be run as part of building the Docker image

source /opt/openfoam6/etc/bashrc
cd /app/OpenQBMM
./Allwmake
