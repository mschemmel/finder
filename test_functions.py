#!/usr/bin/env python3

from libs import flib

def test_occurences():
	"""find_occurences"""
	# test perfect match
	assert flib.find_occurences("ATGCTAGTCG","TAG",0) == [(4,0,"TAG","")]
	assert flib.find_occurences("ATGCTAGTCG","TAG",1) == [(4,0,"TAG",""),(7,1,"TcG","(8:A -> C)")]

def test_reverse_complement():
	"""reverse_complement"""
	assert flib.reverse_complement(dna = "ATGCGTA") == "TACGCAT"
