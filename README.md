# An Oracle-Guided Approach to Constrained Controller Synthesis Under Uncertainty

This artifact supplements the article *An Oracle-Guided Approach to Constrained Controller Synthesis Under Uncertainty*.

Contents of the artifact:
- paynt.tar: the Docker image containing the tools and benchmarks discussed in the article, as well as scripts for their automated evaluation
- LICENSE: the license file
- README.md: this readme

## Reproducing the experiments

### Using the Docker and quick start

Load the image `paynt.tar` into your Docker environment using:
```
docker load -i paynt.tar
```

If you get a permission error, make sure to precede docker commands with `sudo` to acquire root privileges. Upon loading the image, you can run the container with:
```
docker run -v `pwd`/output:/opt/paynt/experiments-jair/output --rm -it paynt:0.1.3
```

`--rm` creates a disposable container that will be deleted upon exit. `-v` will mount the folder `output` in your current directory to the corresponding folder within the container where the experiment results will be stored. This will allow you to inspect logs even after the container has stopped. Executing the command above will place you in `/synthesis/paynt` folder, from which exeriments can be run using
```
./experiments-jair/benchmark.sh 
```

The evaluating script has additional options (described below) that allow you to replicate subsets of results presented in the paper. As a quick start, try option `-4` to obtain log files for data in Table 4:
```
./experiments-jair/benchmark.sh -4
```
The output is created in `/synthesis/paynt/experiments-jair/output`, which is mounted to `$PWD/output` on the host device.

You can exit the container via `exit` or `^D`. Upon finishing your review, you can remove the image from the Docker environment using:
```
docker rmi paynt:0.1.3
```

The Dockerfile used to create the image can be found in /synthesis/Dockerfile or at [PAYNT GitHub](https://github.com/randriu/synthesis).

### What can be replicated

The evaluating script `./experiments-jair/benchmark.sh` allows the generation of log files for PAYNT for experiments presented in Tables 1, 2 and 4 as well as for the case studies in section Q1. Original log files are also included.

### Executing the evaluation script

Running the benchmark script `./experiments-jair/benchmark.sh` without additional flags will evaluate experiments from the tables (this is equivalent to running with the falg `-t`). The following options allow you to replicate subsets of experiments. The name of the folder generated for the corresponding experiment is given in the parantheses. Note you can only use one flag at a time!
- `-1` generate log files for Table 1 (jair24-cpomdp)
- `-2` generate log files for Table 2 (jair24-dec-pomdp)
- `-4` generate log files for Table 4 (jair24-method-ar, jair24-method=cegis, jair24-method-hybrid)
- `-c` generate log files for case studies (jair24-case-studies)
- `-t` generate log files for Table 1, Table 2 and Table 4
- `-a` generate log files for Table 1, Table 2 and Table 4 and case studies

The script creates log files in `experiments-jair/results/output` in sub-folders corresponding to the name of the experiment. When executing the script repeatedly, it detects whether the log files already exist, so you can run the experiments in any order and *can abort long ones without loss of progress*. To re-run the experiments, simply delete the corresponding log files or use option `-o` to force the overwrite.

In case the script encounters an error, it generates an error message and proceeds with the evaluation.

The original results were obtained on a PC equipped with i5-12600k @4.9GHz and 64GB of RAM (note that the memory usage should not go over 16GB).

The original log files that were used when preparing the submission can be found in `experiments-jair/original-logs`.

---


## Using the tool outside the scope of the artifact

In the paper we consider an open source tool PAYNT. Note that PAYNT is built on top of Storm/StormPy. The links below document the installation process for both of the tools.

- PAYNT
    - source: https://github.com/randriu/synthesis
- Storm
    - source: https://github.com/moves-rwth/storm
    - documentation: https://www.stormchecker.org/
    - StormPy (Storm Python API): https://moves-rwth.github.io/stormpy/


## Models

The models considered in our experiments are located in `PAYNT_ROOT/archive/jair24-synthesis`. We consider models from various sources:

- POMDPs from Tony Cassandra's webpage https://pomdp.org/
- Dec-POMDPs from the MASPlan webpage http://masplan.org/problem_domains
- Models from our previous work "PAYNT: A Tool for Inductive Synthesis of Probabilistic Programs by Roman Andriushchenko, Milan Ceska, Sebastian Junges, Joost-Pieter Katoen and Simon Stupinsky" and "Inductive Synthesis of Finite-State Controllers for POMDPs by Roman Andriushchenko, Milan Ceska, Sebastian Junges, Joost-Pieter Katoen, UAI 2022" in PRISM format

To learn more about the PRISM format for creating stochastic models and their specifications visit: https://www.prismmodelchecker.org/manual/ThePRISMLanguage/Introduction


### The evaluation scripts

The evaluation scripts are available at https://github.com/TheGreatfpmK/PAYNT-2024-journal-artifact.

Requirements:
- Python3.8 or higher

Place all of the files of the repository to folder called `experiments-jair` in the root folder of PAYNT, i.e.,
```
cp -r DIR_POMDP_BENCHMARKS/* PAYNT_ROOT/experiments-jair/
```

Run the experiments using
```
./experiments-jair/benchmark.sh 
```

See above for more options.
