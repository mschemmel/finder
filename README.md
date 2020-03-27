# motifs

A small python script to locate motifs in nucleotide sequences. The underlying idea was to identify binding sites that comprise only a few nucleotides in target sequences, such as those required for miRNA or primer binding sites. Of course, it can also be used as a general tool to identify partial regions in nucleotide sequences. The only requirement is a 100 % match of the sequences, the identification of degenerated sequences is not yet supported.

## Getting Started
It is written in python3.

## Prerequisites
It uses the package ['tqdm'](https://github.com/tqdm/tqdm) to track progress. If it is not already installed, you can easily do this with:
```{bash}
pip3 install tqdm 
```

## Usage
```{python}
python3 motifs.py -t template.fa -q query.fa -o /your/output/path -p myproject
```
### Arguments:

    -t path to template file
    -q path to query file
    -o path to output folder
    -p name of your project

If the output path (-o) is not specified, the current working directory is used. All other arguments are required.
## Test

The 'data' folder contains two files (template.fa; query.fa) with arbitrarily generated nucleotide sequences for testing purposes. Try them out using:

```{python}
python3 motifs.py -t ./data/template.fa -q ./data/query.fa -p testrun
```
## Output
The output is structured into two files:

 * mapping.txt
    * contains a simple text based visualization of template sequences with at least one hit
 * summary.txt:
    * contains a tabular conclusion of all template sequences with at least on hit and their location

