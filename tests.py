#!/usr/bin/env python3

import unittest
import libs.molib  

class Test_motif(unittest.TestCase):
	def test_occurences(self):
		"""find_occurences"""
		# test perfect match
		self.assertEqual(libs.molib.find_occurences("ATGCTAGTCGTAG","TAG",0),[4,10],"Should be 4 and 10")
		# test mismatch
		self.assertEqual(libs.molib.find_occurences("ATGCTAGTCGTAG","TAG",1),[4,7,10],"Should be 4, 7 and 10")

	def test_import_sequences(self):
		"""import_sequences"""
		self.assertEqual(len(libs.molib.sequences("./data/template.fa")),100,"Should be 100")
	
	def test_reverse_complement(self):
		"""reverse_complement"""
		self.assertEqual(libs.molib.reverse_complement("ATGCGTA"),"TACGCAT","Should be TACGCAT")

if __name__ == "__main__":
	unittest.main(argv=[''], verbosity=1, exit=False)
