#!/usr/bin/env python3

import unittest
import molib  

class Test_motif(unittest.TestCase):
	def test_occurences(self):
		"""find_occurences"""
		self.assertEqual(molib.find_occurences("ATGCTAGTCGTAG","TAG",0),[4,10],"Should be 4")

	def test_import_sequences(self):
		"""import_sequences"""
		self.assertEqual(len(molib.sequences("./data/template10.fa")),10,"Should be 10")
	
	def test_reverse_complement(self):
		"""reverse_complement"""
		self.assertEqual(molib.reverse_complement("ATGCGTA"),"TACGCAT","")

if __name__ == "__main__":
	unittest.main(argv=[''], verbosity=1, exit=False)
