import datetime
import os
from tqdm import tqdm
from collections import defaultdict

def sequences(filepath: str) -> dict:
	assert len(filepath) > 0
	header = ""
	sequences = {}
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

def find_occurences(text: str, pattern: str, threshold: int) -> list: 
	occurences = []
	for i in range(len(text) - len(pattern) + 1):
		match = True
		mismatch = 0
		for j in range(len(pattern)):
			if text[j+i] != pattern[j]:
				mismatch += 1
				if mismatch > int(threshold):
					match = False
					break
		if match:
			occurences.append(i)
	return occurences

def search(text: dict, pattern: dict, threshold: int):
	hits = {}
	# loop through all targets
	for id_target, seq_target in tqdm(text.items()):
		per_target = {}
		# loop through all queries
		for id_query, seq_query in pattern.items():
			assert len(seq_query) < len(seq_target), "Query longer than target"
			occ = find_occurences(seq_target, seq_query, threshold) 
			if occ:
				per_target[f"{id_query}_{seq_query}"] = occ
		if bool(per_target):
			hits[id_target] = per_target
	return hits

def illustrate(template, summary):
	for target, binding_sites in summary.items():
		yield f'>{target}:{str(len(template[target]))}\n{template[target]}'
		for query, sites in binding_sites.items():
			id_, sequence = query.split("_")
			for site in sites:
				yield f'{"":>{int(site)}}{sequence}:{id_}:({str(len(sequence))}):{str(site)}:{str(int(site)+len(sequence))}'


def reverse_complement(dna:str) -> str:
	nuc = {"T":"A","A":"T","G":"C","C":"G"}
	return "".join([nuc[x] for x in dna])[::-1]

def now():
	return str(datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))

def save_mapping(templ, align, filepath):
	assert len(filepath) > 0
	if os.path.isfile(filepath):
		os.remove(filepath)
	with open(filepath, "a") as fle:
		fle.write("\n".join(illustrate(templ, align)))

