# An extended quadrature-based moment method with log-normal kernel density functions

["An extended quadrature-based moment method with log-normal kernel density functions"](https://dx.doi.org/10.1016/j.ces.2015.04.005) details a refinement to the extended quadrature-based moment method by introducing the log-normal kernel density function. We arrived at this article while trying to reproduce results from another [article](https://dx.doi.org/10.1016/j.jcp.2016.08.017). This article cited the use of the OpenQBMM framework which we did not know how to use properly. Exploring the content of the OpenQBMM library revealed references this paper and in order to better understand OpenQBMM we worked to reproduce the results herein.

The quadrature-based moment method (QBMM) is a way to handle the so-called 'population balance equations'. These deal with the evolution of a population of elements which have one or more internal properties which may evolve over time as well. For example, the droplet size in an aerosol. Droplets can merge, split, increase in size or decrease in size each of which contributes a term to the equations of motion for these particle's and their internal variables. It was discovered that transforming the equations of motion to evolve moments of the internal distribution rather than the internal distribution itself provided some performance benefits. This article and in turn the [OpenQBMM](https://github.com/OpenQBMM/OpenQBMM) library is an extension of this method.

## Build Instructions

### Requirements

With the provided Dockerfile, you can get started quickly using docker. If you are using docker, you can skip this section.

In the future however, this may not work smoothly as dependencies change and this method requires the OpenFOAM people to support their package as an ubuntu repository. Both docker and travis use the following ubuntu dependencies before OpenFOAM and OpenQBMM can be installed:

* `wget` (for getting an external repository)
* `software-properties-common` (for getting an external repository)
* `apt-transport-https` (for getting an external repository)
* `git` (for interacting with OpenQBMM source code)
* `build-essential`
* `python`
* `python-tk`
* `python3-pip`
* `matplotlib`
* `scipy`
* `openfoam6` (from the http://dl.openfoam.org/ubuntu repository)

OpenFOAM and OpenQBMM can be built from source as well. Please see OpenFOAM's [installation documentation](https://openfoam.org/download/source/). After OpenFOAM has been installed, Provided you have sourced the associated environment file `source ${OpenFOAM_Install_Dir}/etc/bashrc`, you should be ready to build and run OpenQBMM.

### Building with docker

Docker already contains the necessary instructions to build this software package. Simply do:

    docker build -t ${DOCKER_IMAGE_NAME} .

### Running with docker

To launch the docker container, get to a command line and be able to start the simulations:

    docker run -it --rm -v $(pwd):/Scratch ${DOCKER_IMAGE_NAME}

#### Initial setup

Make sure that OpenFOAM is installed, and that the environment file `${OpenFOAM_Install_Dir}/etc/bashrc` has been sourced. Then you should be ready to build run and produce output.

#### Run everything script.

Run the `run.sh` script to build, run all necessary computational experiments, and produce all of the visualizations.

Please be aware of the computational requirements you can read here [computational requirements](computational_effort.md).

More details for what is run in this script follow.

#### Building with linux

Assuming OpenFOAM is built and available in the environment, you can now run the `build.sh` script to build OpenFOAM.

#### Scripts for Computational Experiments

The computational experiments backing each of the Figures and Tables each have a catch-all script which executes them. You can execute any of these scripts in isolation from each other and produce the plot for that given figure afterwards.

* `Tables2and3andFigure1.py` This script produces visualization as well
* `RunCases.sh`
* `Figures12and13.py` This script produces visualization as well
* `Figure14.py` This script produces visualization as well

Output from these scripts can be found in the directories `caseXNY`, printed to the screen for tables and saved in `.png` files in the current directory.

The figures we produced on our machine are located in the `expected_output` directory.

#### Scripts for Visualizations

Some Figures are produced by analyzing data from some of the computational experiments above. The following scripts perform this analysis and produce thos plots.

* `Create_Inversion_Plots.sh`
* `Create_Comparison_Plots.sh`

Output from these scripts are in the form of `.png` files written to the main directory.

The figures we produced on our machine are located in the `expected_output` directory.

## Reproduction Notes

We kept track of our progress and issues inside `notes.txt`. We also have a jupyter notebook showing this progress over time `ReproducibilityPlot.ipynb`

## Acknowledgement of the Authors

We want to acknowledge the authors Alberto Passalacqua and Ehsan Madidi Kandjani for their fine work on this experiment. We succeeded in reproducing most aspects of this paper where we were unable to for many others. Their high quality work and generous communication allowed this to happen.
