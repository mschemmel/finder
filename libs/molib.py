import datetime
import os
import pyfastx

class Seek():
  def __init__(self, target_path, query_path):
    self.target_path = target_path
    self.query_path = query_path

  def find_occurences(self, text: str, pattern: str, threshold: int) -> list: 
    occurences = []
    for i in range(len(text) - len(pattern) + 1):
      match = True
      mismatch = 0
      match_seq, mismatch_record = [],[]
      for j in range(len(pattern)):
        if text[j+i] != pattern[j]:
          mismatch += 1
          match_seq.append(text[j+i].lower())
          mismatch_record.append(f"({j+i}:{pattern[j]} -> {text[j+i]})")
          if mismatch > int(threshold):
            match = False
            break
        else:
          match_seq.append(text[j+i].upper())
      if match:
        occurences.append((i,"".join(match_seq), mismatch, " ".join(mismatch_record)))
    return occurences

  def search(self, threshold: int):
    for id_target, seq_target in pyfastx.Fasta(self.target_path, build_index=False):
      per_target = {}
      for id_query, seq_query in pyfastx.Fasta(self.query_path, build_index = False):
        assert len(seq_query) < len(seq_target), "Query longer than target"
        direction = 0 # Forward 5'-3'
        occ = self.find_occurences(seq_target, seq_query, threshold) 
        if not occ:
          direction = 1 # Reverse 3'-5'
          occ = self.find_occurences(seq_target, self.reverse_complement(seq_query), threshold) 
        if occ:
          lp = len(seq_query)
          for h in occ:
            yield f"{id_target}\t{h[0]}\t{h[0]+lp}\t{lp}\t{h[2]}\t{direction}\t{id_query}\t{seq_query}\t{h[1]}\t{h[3]}"

  def reverse_complement(self, dna: str) -> str:
    nuc = {"T":"A","A":"T","G":"C","C":"G"}
    return "".join([nuc[x] for x in dna])[::-1]


