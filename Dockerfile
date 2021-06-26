FROM ubuntu:16.04 

WORKDIR /app
ADD . /app

RUN \
  apt-get update \
  && apt-get install -y build-essential software-properties-common curl\
  && add-apt-repository ppa:deadsnakes/ppa \
  && apt-get update

# Install Python and various packages needed to run the Python scripts
RUN \
  apt-get install -y python3.7 \
  && curl https://bootstrap.pypa.io/get-pip.py -o get-pip.py \
  && python3.7 get-pip.py \
  && apt-get install -y python-tk \
  && pip3 install matplotlib==3.0 \
  && pip3 install scipy==1.4

# Install OpenFOAM v6
RUN \
  apt-get install -y wget \
  && apt-get install -y software-properties-common \
  && apt-get install apt-transport-https \
  && sh -c "wget -O - http://dl.openfoam.org/gpg.key | apt-key add -" \
  && add-apt-repository http://dl.openfoam.org/ubuntu \
  && apt-get update \
  && apt-get install -y openfoam6 \
  && echo "source /opt/openfoam6/etc/bashrc" >> ~/.bashrc

# Update the submodule for OpenQBMM and build it
ENV OpenFOAM_Install_Dir /opt/openfoam6
ENV Project_Dir /app
RUN \
  apt-get install -y git
RUN \
  git submodule init \
  && git submodule update
RUN \
  apt-get install -y curl \
  && /bin/bash -xec /app/build.sh

# Misc
RUN \
  apt-get install -y vim

ENTRYPOINT /bin/bash
