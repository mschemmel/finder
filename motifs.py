#!/usr/bin/env python3
import os
import sys
import argparse
import moformat as mf
import molib as ml

def main():
	# handle command line options
	parser = argparse.ArgumentParser(description = "Program to find all occurences of queries in template sequences.")
	parser.add_argument("-t", "--target", help = "Path to your target fasta file")
	parser.add_argument("-q", "--query", help = "Path to your query fasta file")
	parser.add_argument("-m", "--mismatch", default = 0, help = "Number of mismatches allowed")
	parser.add_argument("-o", "--output", help = "Path to your output directory")
	args = parser.parse_args()

	# check if all necessary filepaths are provided
	# check targets and queries
	if args.target:
		if args.query:
			pass
		else:
			print(f"[ {mf.Colors.ERROR}ERROR{mf.Colors.NC} ] Please provide a valid path for your query file.")
			sys.exit(0)
	else:
		print(f"[ {mf.Colors.ERROR}ERROR{mf.Colors.NC} ] Please provide a valid path for your target file.")
		sys.exit(0)

	# check output
	if args.output:
		out_dir = args.output
	else:
		out_dir = os.getcwd()

	# set output paths
	out_mapping = os.path.join(out_dir, "mapping.txt").replace("\\", "/")
	out_report = os.path.join(out_dir, "summary.txt").replace("\\", "/")

	# set number of mismatches allowed
	mismatch = args.mismatch
	
	# import fasta files
	print(f'{ml.now()}\tImport target and query file')
	target = ml.sequences(args.target)
	query = ml.sequences(args.query)
	print(f'{"-" * 30}')
	print(f'{len(target)} target sequences')
	print(f'{len(query)} query sequences')
	print(f'{"-" * 30}')

	# do matching
	print(f'{ml.now()}\tSearch for motifs')
	matches = ml.search(target, query, mismatch)
	
	for k,v in matches.items():
		print(f"{k}:{v}")

	# save output
	print(f'{ml.now()}\tSave output in project folder')
	ml.save_mapping(target, matches, out_mapping)

	print(f'{ml.now()}\tRun finished')
	print(f'[ {mf.Colors.OK}OK {mf.Colors.NC} ] Results successfully stored in: {out_dir}')

if __name__ == "__main__":
	main()
