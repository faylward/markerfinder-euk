import os, sys, subprocess, re, shlex, pandas, glob, operator, argparse
import numpy as np
from natsort import natsorted, ns
from collections import defaultdict
from operator import itemgetter
from Bio import SeqIO
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord

# this is a script for merging RNAP protein files that were generated using markerfinder_v2. 

inputfolder1 = sys.argv[1]
inputfolder2 = sys.argv[2]
outputfolder = sys.argv[3]

cog85 = ["COG0085.faa", "RNAPbeta.faa"]
cog86 = ["COG0086.faa", "RNAPbetaprime.faa"]

cog85seqs = []
cog86seqs = []

taxon_list = []

for folder in [inputfolder1, inputfolder2]:
	for i in os.listdir(folder):
		if i in cog85:
			handle = os.path.join(folder, i)
			for record in SeqIO.parse(handle, "fasta"):
				
				name = record.id
				underscore = name.split("_")					
				taxon = underscore[0]
				taxon_list.append(taxon)
				
				newname = taxon +"_COG0085" 
				record.id = newname
				cog85seqs.append(record)
				
		if i in cog86:
			handle = os.path.join(folder, i)
			for record in SeqIO.parse(handle, "fasta"):
			
				name = record.id
				underscore = name.split("_")					
				taxon = underscore[0]
				taxon_list.append(taxon)
			
				newname = taxon +"_COG0086" 
				record.id = newname
				cog86seqs.append(record)
			
SeqIO.write(cog85seqs, os.path.join(outputfolder, "COG0085.combined.faa"), "fasta")
SeqIO.write(cog86seqs, os.path.join(outputfolder, "COG0086.combined.faa"), "fasta")

taxon_set = set(taxon_list)


print("Generating alignments with Muscle5...")
align_dict = defaultdict(list)
full_dict = {}
for i in os.listdir(outputfolder):
	if i.endswith(".faa"):
		filename = os.path.join(outputfolder, i)
		alignment = re.sub(".faa", ".aln", filename)
		cog = re.sub(".combined.faa", "", i)
		#print "Aligning and trimming "+ cog +" and adding it to the concatenated alignment"
		cmd = "muscle5.1.linux_intel64 -super5 "+ filename +" -output "+ alignment 
		#print(cmd)
		cmd2 = shlex.split(cmd)
		subprocess.call(cmd2, stdout=open("log_file.txt", "a"), stderr=open("log_file.txt", "a"))

		seq_dict = SeqIO.to_dict(SeqIO.parse(alignment, "fasta"))
		values = list(seq_dict.values())
		first = values[0]
		length = len(first.seq)
		
		for taxon in taxon_set:
			entry = taxon +"_"+ cog
			print(entry)
			if entry in seq_dict:
				align_dict[taxon].append(str(seq_dict[entry].seq))
			else:
				placeholder = "X" * length
				align_dict[taxon].append(placeholder)

outlist = []
for i in align_dict:
	record = SeqRecord(Seq("".join(align_dict[i])), id=i)
	record.description = "concatenated alignment "
	outlist.append(record)

SeqIO.write(outlist, "concat_alignment.aln", "fasta")




