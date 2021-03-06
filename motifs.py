#!/usr/bin/env python3
import os
import sys
import argparse
import datetime
import re
from tqdm import tqdm

class Sequences:
	def __init__(self, filepath):
		self.filepath = filepath

	def import_sequences(self):
		assert len(self.filepath) > 0
		sequences = {}
		header = ""

		# open sequence file and populate dictionary
		with open(self.filepath, "r") as fle:
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
	non_nucleotides = list(filter(lambda a :	True if a in list(dg.keys()) else False, transform))
	
	transform = "".join([flse for non_nucleotides in transform.replace(flse,f'[{dg[flse]}]')])
	# replace them with possible nucleotides as regex notation
	#for flse in non_nucleotides:
	#	transform = transform.replace(flse,f'[{dg[flse]}]')
	
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
				# merge id and seq of query in 'hits' variable
				# for later use in 'illustrate' function
				hits = f'{id_query}_{seq_query}'
				
				# populate binding_sites
				binding_sites[hits] = matches
				
				#store all binding_sites
				binding_sites_per_target[id_target] = binding_sites

	return binding_sites_per_target

def illustrate(template, summary):
	for target, binding_sites in summary.items():
		yield f'>{target}:{str(len(template[target]))}\n{template[target]}'
		for query, sites in binding_sites.items():
			id_, sequence = query.split("_")
			for site in sites:
				yield f'{"":>{int(site)}}{sequence}:{id_}:({str(len(sequence))}):{str(site)}:{str(int(site)+len(sequence))}'

def now():
	return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def save_mapping(templ, align, filepath):
	assert len(filepath) > 0
	with open(filepath, "a") as fle:
		fle.write("\n".join(illustrate(templ, align)))

def save_report(template, align, filepath):
	assert len(filepath) > 0
	with open(filepath, "a") as fle:
		fle.write(f'target\ttarget_length\tquery\tquery_seq\tquery_length\tstart\tstop\n')
		for k, v in align.items():
			for a, b in v.items():
				id_, sequence = a.split("_")
				for item in b:
					fle.write("\t".join(map(str, [k, len(template[k]), id_, sequence, len(sequence), int(item), int(item) + len(sequence)])) + "\n")

def main():
	# handle command line options
	parser = argparse.ArgumentParser(description="Program to find all occurences of queries in template sequences.")
	parser.add_argument("-t", "--targets", help="Path to your target fasta file")
	parser.add_argument("-q", "--query", help="Path to your query fasta file")
	parser.add_argument("-o", "--output", help="Path to your output directory")
	args = parser.parse_args()

	# check if all necessary filepaths are provided
	# check targets and queries
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

	# set output paths
	out_mapping = os.path.join(out_dir, "mapping.txt").replace("\\", "/")
	out_report = os.path.join(out_dir, "summary.txt").replace("\\", "/")

	# import fasta files
	print(f'{now()}\tImport target and query file')
	target = Sequences(args.targets).import_sequences()
	query = Sequences(args.query).import_sequences()
	print(f'{"-" * 30}')
	print(f'{len(target)} target sequences')
	print(f'{len(query)} query sequences')
	print(f'{"-" * 30}')

	# do matching
	print(f'{now()}\tSearch for motifs')
	matches = findall(target, query)
	
	# save output
	print(f'{now()}\tSave output in project folder')
	save_mapping(target, matches, out_mapping)
	save_report(target, matches, out_report)

	print(f'{now()}\tRun finished')
	print(f'Results successfully stored in: {out_dir}')

if __name__ == "__main__":
	main()
