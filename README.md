![GitHub](https://img.shields.io/github/license/mschemmel/motifs)
<img src="https://img.shields.io/badge/python-3.6--3.9-9cf.svg?style=flat">
[![Build Status](https://travis-ci.org/mschemmel/motifs.svg?branch=master)](https://travis-ci.org/mschemmel/motifs)

# motifs

A python script to locate motifs in nucleotide sequences using a naive matching approach. The underlying idea was to identify binding sites that comprise only a few nucleotides in target sequences, such as those required for miRNA or primer binding sites. Of course, it can also be used as a general tool to identify partial regions in nucleotide sequences. It is not intended to work with large datasets, but rather as a downstream tool for detailed analysis after general mapping tools as for example bowtie.  

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
python3 motifs.py -t template.fa -q query.fa -o /your/output/path 
```
### Arguments:
| Parameter | Description | Default |
| --------- | ----------- | --------|
| `-t` (`--target`) | path to template file ||
| `-q` (`--query`) | path to query file ||
| `-o` (`--output`) | path to output folder ||
| `-m` (`--mismatch`) | number of mismatches allowed | 0 |

If the output path (-o) is not specified, the current working directory is used.
## Test

The 'data' folder contains files with arbitrarily generated nucleotide sequences for testing purposes. Try them out using:

```
python3 motifs.py -t ./data/template.fa -q ./data/query.fa --mismatch 2
```
## Output
The output is structured into a mapping file:

| File | Description |
| ---- | ----------- |
| mapping.txt | contains a simple text based visualization of template sequences with at least one hit |

## Feedback
If you have any feedback or comments, please send me a mail or open an issue on github.
