![GitHub](https://img.shields.io/github/license/mschemmel/motifs)
<img src="https://img.shields.io/badge/python-3.4--3.8-9cf.svg?style=flat">
[![Build Status](https://travis-ci.org/mschemmel/motifs.svg?branch=master)](https://travis-ci.org/mschemmel/motifs)

# motifs

A python script to locate motifs in nucleotide sequences. The underlying idea was to identify binding sites that comprise only a few nucleotides in target sequences, such as those required for miRNA or primer binding sites. Of course, it can also be used as a general tool to identify partial regions in nucleotide sequences. The identification of degenerated sequences as query is also supported. Queries that are longer than the target will not be considered.

<p align="center">
<img src="/images/illustrate_mapping.png">
</p>

## Getting Started
It is written in python3.

## Prerequisites
It uses the package ['tqdm'](https://github.com/tqdm/tqdm) to track progress. If it is not already installed, you can easily do this with:
```
pip3 install tqdm 
```

## Usage
```
python3 motifs.py -t template.fa -q query.fa -o /your/output/path -p myproject
```
### Arguments:

    -t path to template file
    -q path to query file
    -o path to output folder
    -p name of your project

If the output path (-o) is not specified, the current working directory is used. All other arguments are required.
## Test

The 'data' folder contains several files with arbitrarily generated nucleotide sequences (non-degenerated & degenerated) for testing purposes. Try them out using:

```
python3 motifs.py -t ./data/template1000.fa -q ./data/query100.fa -p testrun
```
## Output
The output is structured into two files:

 * mapping.txt
    * contains a simple text based visualization of template sequences with at least one hit
 * summary.txt:
    * contains a tabular conclusion of all template sequences with at least on hit and their location

## Feedback
If you have any feedback or comments, please send me a mail or open an issue on github.
