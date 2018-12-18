#!/bin/bash

# Helper script to make OpenQBMM, to be run as part of building the Docker image
source ${OpenFOAM_Install_Dir}/etc/bashrc
cd ${Project_Dir}/OpenQBMM
./Allwmake
