# PanChIP
**Pan-ChIP-seq Analysis of Protein Colocalization Using Peak Sets**

[![PyPI version](https://badge.fury.io/py/PanChIP.svg)](https://badge.fury.io/py/PanChIP)
[![DOI](https://zenodo.org/badge/424777555.svg)](https://zenodo.org/badge/latestdoi/424777555)

<br/>

The current version of PanChIP supports the hg38 genome assembly.

## Prerequisites
Python 3, BEDTools

## Installation
**Installation by PyPI**
```shell
pip3 install panchip
```

**Installation by Bioconda**
```shell
conda install bioconda::panchip
```

## Input
```shell
PanChIP Analysis: a directory with only 6-column BED files
PanChIP Filter: a 6-column BED file

We recommend most PanChIP users to utilize BED files with constant non-zero fifth column values (e.g., 1, 500, 1000).
```

## Usage

### panchip <command> [options]

```shell
Commands:
    init            Initialization of the PanChIP library
    analysis        Analysis of a list peak sets
    filter          Filtering library for quality control
Run panchip <command> -h for help on a specific command.

PanChIP: Pan-ChIP-seq Analysis of Peak Sets

positional arguments:
  command     Subcommand to run

optional arguments:
  -h, --help  show this help message and exit
  --version   show program's version number and exit
```

### panchip init [-h] library_directory

```shell

Initialization of the PanChIP library

positional arguments:
  library_directory  Directory wherein PanChIP library will be stored. > 13.6
                     GB of storage required.

optional arguments:
  -h, --help         show this help message and exit
```

### panchip analysis [-h] [-t THREADS] [-r REPEATS] library_directory input_directory output_directory

```shell

Analysis of a list peak sets

positional arguments:
  library_directory  Directory wherein PanChIP library was stored.
  input_directory    Input directory wherein peak sets in the format of .bed
                     files are located.
                     (.bed6 format with numeric scores in 5th column required)
  output_directory   Output directory wherein output files will be stored.

optional arguments:
  -h, --help         show this help message and exit
  -t THREADS         Number of threads to use. (default: 1)
  -r REPEATS         Number of repeats to perform. (default: 1)
```

### panchip filter [-h] [-t THREADS] library_directory input_file output_directory

```shell

Filtering library for quality control

positional arguments:
  library_directory  Directory wherein PanChIP library was stored.
  input_file         Path to the input .bed file.
                     (.bed6 format with numeric scores in 5th column required)
  output_directory   Output directory wherein output files will be stored.

optional arguments:
  -h, --help         show this help message and exit
  -t THREADS         Number of threads to use. (default: 1)
```

## Primary Citation

Please cite the original PanChIP paper for works that utilized the PanChIP software.

- **Sanidas I, Lee H, Rumde PH, Boulay G, Morris R, Golczer G, Stanzione M, Hajizadeh S, Zhong J, Ryan MB, Corcoran RB, Drapkin BJ, Rivera MN, Dyson NJ, and Lawrence MS. Chromatin-bound RB targets promoters, enhancers, and CTCF-bound loci, and is redistributed by cell cycle progression. _Molecular Cell_ 82.18 (2022).**

## Extended Citation

The development of PanChIP was possible thanks to many groundbreaking works of fellow researchers. We highly recommend users to cite the Cistrome Data Browser as well.

- **Zheng R, Wan C, Mei S, Qin Q, Wu Q, Sun H, Chen C-H, Brown M, Zhang X, Meyer CA, and Liu XS. Cistrome Data Browser: expanded datasets and new tools for gene regulatory analysis. _Nucleic Acids Research_ 47.D1, D729–D735 (2019).**

While the design of PanChIP is different from that of BART, we suggest users to also try out the BART software. PanChIP measures the overlap between peak sets, while BART assesses the predictability of profiles based on the library.

- **Wang Z, Civelek M, Miller CL, Sheffield NC, Guertin MJ, and Zang C. BART: a transcription factor prediction tool with query gene sets or epigenomic profiles. _Bioinformatics_ 34.16, 2867–2869 (2018).**
