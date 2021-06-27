#!/usr/bin/env python3
import os
import sys
import argparse
import libs.fformat as ff
import libs.flib as fl

def main():
	# handle command line options
	parser = argparse.ArgumentParser(description = "Program to find all occurences of queries in template sequences.")
	parser.add_argument("-t", "--target", help = "Path to your target fasta file")
	parser.add_argument("-q", "--query", help = "Path to your query fasta file")
	parser.add_argument("-m", "--mismatch", default = 0, help = "Number of mismatches allowed")
	parser.add_argument("-o", "--output", help = "Path to your output directory")
	parser.add_argument("-s", "--save", action='store_true', help = "Save output to file?")
	parser.add_argument("-r", "--rev", action='store_true', help = "Save output to file?")
	args = parser.parse_args()

	# check if all necessary filepaths are provided
	# check targets and queries
	if args.target:
		if args.query:
			pass		
		else:
			print(f"[ {ff.Colors.ERROR}ERROR{mf.Colors.NC} ] Please provide a valid path for your query file.")
			sys.exit(0)
	else:
		print(f"[ {ff.Colors.ERROR}ERROR{mf.Colors.NC} ] Please provide a valid path for your target file.")
		sys.exit(0)

	# check output
	if args.output:
		out_dir = args.output
	else:
		out_dir = os.getcwd()

	# set output 
	out_mapping = os.path.join(out_dir, "mapping.txt").replace("\\", "/")
	out_report = os.path.join(out_dir, "summary.txt").replace("\\", "/")

	# set number of mismatches allowed
	mismatch = args.mismatch
	
	# run 
	print(f'{ff.now()}\tSearch for motifs')
	print(f'{"-" * 50}\n')
	matches = fl.Seek(args.target, args.query).search(args.mismatch, args.rev)
	if args.save:
		if os.path.isfile(out_report):
			os.remove(out_report)
		with open(out_report, "a") as out:
			for match in matches:
				out.write(f"{match}\n")
		# save output
		# TODO: save mapping in html report
		print(f'{ff.now()}\tSave output in project folder')
	else:
		for match in matches:
			print(match)
	
	
	print(f'\n{"-" * 50}')
	print(f'{ff.now()}\tRun finished')
	print(f'[ {ff.Colors.OK}OK {ff.Colors.NC} ] Results successfully stored in: {out_dir}')

if __name__ == "__main__":
	main()
