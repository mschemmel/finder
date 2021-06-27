![GitHub](https://img.shields.io/github/license/mschemmel/motifs)
<img src="https://img.shields.io/badge/python-3.9-9cf.svg?style=flat">
![example workflow](https://github.com/mschemmel/finder/actions/workflows/python-app.yml/badge.svg)
# finder

A python script to locate read alignments in nucleotide sequences using a naive matching approach. I know, slow, but the project startet initially to learn more about the read alignment problem. A long-term goal consists of the implementation of Boyer-Moore. The underlying idea was to identify binding sites that comprise only a few nucleotides in target sequences, such as those required for miRNA or primer binding sites. Of course, it can also be used as a general tool to identify partial regions in nucleotide sequences. Because of its lacking performance, it is not intended to work with large datasets, but rather as a downstream tool for detailed analysis. 
<p align="center">
<img src="/images/illustrate_mapping.png">
</p>

## Usage
```
python3 finder.py -t template.fa -q query.fa -o /your/output/path 
```
### Arguments:
| Parameter | Description | Default |
| --------- | ----------- | --------|
| `-t` (`--target`) | path to template file ||
| `-q` (`--query`) | path to query file ||
| `-o` (`--output`) | path to output folder ||
| `-m` (`--mismatch`) | number of mismatches allowed | 0 |
| `-s` (`--save`) | Save output to file | False |
| `-r` (`--rev`) | Search also in reverse complement of target sequence | False |

If the output path (-o) is not specified, the current working directory is used.
## Test

The 'data' folder contains files with arbitrarily generated nucleotide sequences for testing purposes. Try them out using:

```
python3 finder.py -t ./data/template.fa -q ./data/query.fa --mismatch 2
```
## Output
The output is structured into a mapping file (__in progress__):

| File | Description |
| ---- | ----------- |
| mapping.txt | contains a simple text based visualization of template sequences with at least one hit |

## Feedback
If you have any feedback or comments, please send me a mail or open an issue on github.
