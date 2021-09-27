import datetime
import os
import pyfastx

def find_occurences(text: str, pattern: str, threshold: int) -> list: 
	assert len(pattern) <= len(text)
	assert int(threshold) < len(pattern)
	occurences = []
	for i in range(len(text) - len(pattern) + 1):
		match = True
		number_of_mismatches = 0
		pattern_match_seq, mismatch_variant_record = [],[]
		for j in range(len(pattern)):
			if text[j+i] != pattern[j]:
				number_of_mismatches += 1
				pattern_match_seq.append(text[j+i].lower())
				mismatch_variant_record.append(f"({j+i}:{pattern[j]} -> {text[j+i]})")
				if number_of_mismatches > int(threshold):
					match = False
					break
			else:
				pattern_match_seq.append(text[j+i].upper())
		if match:
			occurences.append((i,number_of_mismatches, "".join(pattern_match_seq), " ".join(mismatch_variant_record)))
	return occurences

def reverse_complement(dna: str) -> str:
	nuc = {"T":"A","A":"T","G":"C","C":"G","N":"N"}
	return "".join([nuc[x] for x in dna])[::-1]

class Seek():
	def __init__(self, target_path, query_path):
		self.target_path = target_path
		self.query_path = query_path


	def search(self, threshold: int, revcomp: bool):
		for id_target, seq_target, comment_target in pyfastx.Fastx(self.target_path):
			per_target = {}
			for id_query, seq_query, comment_query in pyfastx.Fastx(self.query_path):
				name = f"{id_query}_{comment_query}"
				per_target["f"] = find_occurences(seq_target, seq_query, threshold)
				if revcomp:					
					per_target["r"] = find_occurences(reverse_complement(seq_target), seq_query, threshold)
				if per_target:
					len_query = len(seq_query)
					for direction,hits in per_target.items():
						for hit in hits:
							yield f"{id_target}\t{hit[0]}\t{hit[0]+len_query}\t{len_query}\t{direction}\t{hit[1]}\t{seq_query}\t{name}\t{hit[2]}\t{hit[3]}"



