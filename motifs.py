#!/usr/bin/env python3
import os
import sys
import argparse
import datetime
import re
from tqdm import tqdm



def import_sequences(filepath):
    sequences = {}
    header = ""

    # open sequence file and populate dictionary
    with open(filepath, "r") as fle:
        for line in fle:
            if not line.strip():
                continue
            if line.startswith(">"):
                header = line.replace(">", "").strip()
                sequences[header] = ""
            else:
                sequences[header] += line.strip().upper()
    return sequences


def is_degenerated(to_check):
    if any(x not in ["A","T","G","C"] for x in to_check):
        return True
    else:
        return False

def degenerated_of(deg): 
    transform = deg
    
    # https://www.bioinformatics.org/sms/iupac.html
    dg = {"R": "AG",
          "Y": "CT",
          "S": "GC",
          "W": "AT",
          "K": "GT",
          "M": "AC",
          "B": "CGT",
          "D": "AGT",
          "H": "ACT",
          "V": "ACG",
          "N": "ATGC"}
    
    # detect all non nucleotides in sequence
    non_nucleotides = list(filter(lambda a :  True if a in list(dg.keys()) else False, transform))
                                           
    # replace them with possible nucleotides as regex notation
    for flse in non_nucleotides:
        transform = transform.replace(flse,"[{}]".format(dg[flse]))
    
    return transform

def findall(base, pattern):
    binding_sites_per_target = {}
    
    # loop through all targets
    for id_target, seq_target in tqdm(base.items()):
        binding_sites = {}

        for id_query, seq_query in pattern.items():

            # check if query sequence is longer than target
            if len(seq_query) > len(seq_target):
                continue
            
            # check if query sequence is degenerated
            if is_degenerated(seq_query):
                seq_query_deg = degenerated_of(seq_query)
                matches = [i.start() for i in re.finditer(seq_query_deg, seq_target)]
            else:
                matches = [i.start() for i in re.finditer(seq_query, seq_target)]
              
            if matches:
                # merge id and seq of query in 'hit' variable
                # for later use in 'illustrate' function
                hits = "{}_{}".format(id_query,seq_query)

                # populate bindin_sites
                binding_sites[hits] = matches
                
                #store all binding_sites
                binding_sites_per_target[id_target] = binding_sites

    return binding_sites_per_target

def illustrate(template, summary):
    for target, binding_sites in summary.items():
        yield ">{}:{}\n{}".format(target, str(len(template[target])), template[target])
        for query, sites in binding_sites.items():
            id_ = query.split("_")[0]
            sequence = query.split("_")[1]
            for site in sites:
                yield " " * site + sequence + ":" + id_ + ":" + "(" + str(len(sequence)) + ")" + ":" + str(site) + ":" + str(site + len(sequence))

def now():
    return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def save_mapping(templ, align, filepath):
    with open(filepath, "a") as fle:
        fle.write("\n".join(illustrate(templ, align)))

def save_report(template, align, filepath):
    with open(filepath, "a") as fle:
        fle.write("{}\t{}\t{}\t{}\t{}\t{}\t{}\n".format("target", "target_length", "query","query_seq", "query_length", "start", "stop"))
        for k, v in align.items():
            for a, b in v.items():
                id_ = a.split("_")[0]
                sequence = a.split("_")[1]
                for item in b:
                    fle.write("\t".join(map(str, [k, len(template[k]), id_, sequence, len(sequence), int(item), int(item) + len(sequence)])) + "\n")

def main():
    # handle command line options
    parser = argparse.ArgumentParser(description="Program to find all occurences of queries in template sequences.")
    parser.add_argument("-t", "--targets", help="Path to your target fasta file")
    parser.add_argument("-q", "--query", help="Path to your query fasta file")
    parser.add_argument("-o", "--output", help="Path to your output directory")
    parser.add_argument("-p", "--project", help="Project ID")
    args = parser.parse_args()

    # check if all necessary filepaths are provided
    # check targets and query
    if args.targets:
        if args.query:
            pass
        else:
            print("Please provide a valid path for your query file.")
            sys.exit(0)
    else:
        print("Please provide a valid path for your target file.")
        sys.exit(0)

    # check output
    if args.output:
        out_dir = args.output
    else:
        out_dir = os.getcwd()

    # check project
    if args.project:
        out_dir = os.path.join(out_dir, args.project)
        if os.path.isdir(out_dir):
            answer = input("WARNING: Project folder already exists. Overwrite [y/n]?").strip()
            if answer == "y":
                for ff in os.listdir(out_dir):
                    os.remove(os.path.join(out_dir, ff))
            elif answer == "n":
                print("WARNING: Run cancelled")
                sys.exit(0)
            else:
                print("WARNING: Please use 'y' or 'n' to answer.")
                sys.exit(0)
        else:
            os.mkdir(out_dir)
    else:
        print("WARNING: You need to specify a project name (-p)")
        sys.exit(0)


    # set output paths
    out_mapping = os.path.join(out_dir, "mapping.txt").replace("\\", "/")
    out_report = os.path.join(out_dir, "summary.txt").replace("\\", "/")

    # import fasta files
    print("{}\t{}".format(now(), "Import target and query file"))
    target = import_sequences(args.targets)
    query = import_sequences(args.query)
    print("-" * 30)
    print("{} target sequences".format(len(target)))
    print("{} query sequences".format(len(query)))
    print("-" * 30)

    # do matching
    print("{}\tSearch for motifs".format(now()))
    matches = findall(target, query)
    
    # save output
    print("{}\tSave output in project folder".format(now()))
    save_mapping(target, matches, out_mapping)
    save_report(target, matches, out_report)

    print("{}\tRun finished".format(now()))
    print("{} {}".format("Results successfully stored in :", out_dir))

if __name__ == "__main__":
    main()
