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
      match_seq = []
      mismatch_record = []
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
        desc = f"{id_query}_{seq_query}_for"
        occ = self.find_occurences(seq_target, seq_query, threshold) 
        if not occ:
          desc = f"{id_query}_{seq_query}_rev"
          occ = self.find_occurences(seq_target, self.reverse_complement(seq_query), threshold) 
        if occ:
          lp = len(seq_query)
          for h in occ:
            yield f"{id_target}\t{h[0]}\t{h[0]+lp}\t{lp}\t{h[2]}\t{id_query}\t{seq_query}\t{h[1]}\t{h[3]}"

  def illustrate(self, template: dict , summary: dict):
    for target, binding_sites in summary.items():
      yield f'>{target}:{str(len(template[target]))}\n{template[target]}'
      for query, sites in binding_sites.items():
        id_, sequence, direction = query.split("_")
        for site in sites:
          yield f'{"":>{int(site)}}{sequence}:{id_}:({direction}):({str(len(sequence))}):{str(site)}:{str(int(site)+len(sequence))}'


  def reverse_complement(self, dna: str) -> str:
    nuc = {"T":"A","A":"T","G":"C","C":"G"}
    return "".join([nuc[x] for x in dna])[::-1]


  def save_mapping(self, template: dict, alignment: dict, filepath: str):
    assert len(filepath) > 0
    if os.path.isfile(filepath):
      os.remove(filepath)
    with open(filepath, "a") as fle:
      fle.write("\n".join(illustrate(template, alignment)))

