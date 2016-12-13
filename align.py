# Alice Yue; Last modified 20161208

# Input: Original alignment (nexus)
# Output: Organized, seperated, and combined alignments; muscle alignments

import numpy as np
import os, subprocess

#basic biopython imports
from Bio import Alphabet
from Bio import Nexus
from Bio.Alphabet import generic_dna
from Bio.Seq import Seq
from Bio.SeqRecord import SeqRecord as sr
#from StringIO import StringIO

#for dealing with alignment files
from Bio import AlignIO as aio
from Bio.Align import MultipleSeqAlignment as msa
#from Bio.Align.Applications import MuscleCommandline as muscl

#for making phylogeny from alignments; optional, will do on commandline seperately
#from Bio.Align.Applications import MuscleCommandline
#from Bio.Phylo.Applications import PhymlCommandline as phyml
#from Bio.Phylo.Applications import RaxmlCommandline as raxml

#for processing phylogeny files; optional
from Bio.Phylo.Consensus import *
from Bio import Phylo as phy
#from Tkinter import *
#from ete3 import Tree

### Import original alignment ===============================
al = ['align/o', 'align/m']
form = ['nexus', 'phylip', 'fasta']

# Import alignment
align_path = "align.txt"
align = aio.read(open(align_path), form[0])
# align_array = np.array([list(rec) for rec in align], np.character) # alignment as arrays

### Get gene indices =========================
with open('talign.txt') as f:
	content = f.readlines()
del content[-1]
g = [i.split('=', 1)[0] for i in content]
g = [s.strip('\tCHARSET') for s in g]
g = [s.strip() for s in g]
index = [i.split('=', 1)[1] for i in content]
index = [s.strip(';\n') for s in index]
index = [s.strip() for s in index]
start = [i.split('-', 1)[0] for i in index]
end = [i.split('-', 1)[1] for i in index]
end = [s.strip(' ;') for s in end]

geneOrder = ['Cytb', 'CO1', 'CO2', 'CO3', 'ATP6', 'ATP8', 'ND1', 'ND2', 'ND3', 'ND4', 'ND4L', 'ND5', 'ND6', '12S',
             '16S', 'mtDNA_tRNA', '18S', 'CT', 'Epend', 'GH1c', 'GH1d', 'GH2c', 'GH2d', 'HMG1', 'ITS1', 'ITS2', 'LDH',
             'MetA', 'MetB', 'RAG', 'Tnfa', 'Transf', 'VIT']

### Split genes and save as seperate files =========================
# Make directories
if not os.path.exists('align'):
	os.makedirs('align')
for a in al:
	if not os.path.exists(a):
		os.makedirs(a)
	for f in form:
		if not os.path.exists(a + '/' + f):
			os.makedirs(a + '/' + f)

# Remove species without any data / all gaps as .phy and .nex file
for i in range(len(g)):
	a = align[:, int(start[i]) - 1:int(end[i]) - 1]
	na = np.array([list(rec) for rec in a], np.character)
	na[na == '?'] = '-'
	ni = np.where(~np.all(na == '-', axis=1) == True)
	ni = list(itertools.chain.from_iterable(ni))
	na = na[ni, :]
	na = [''.join(x) for x in na]
	a0 = sr(Seq(na[0], generic_dna), id=a[ni[0], :].name)
	if len(na) > 1:
		a1 = sr(Seq(na[1], generic_dna), id=a[ni[1], :].name)
		a0 = [a0, a1]
	if len(na) > 2:
		for j in range(2, len(ni)):
			a1 = sr(Seq(na[j], generic_dna), id=a[ni[j], :].name)
			a0.append(a1)
	a0 = msa(a0)
	for f in form:
		aio.write(a0, al[0] + '/' + f + '/align_' + g[i] + '.' + f, f)
for f in form:
	aio.write(align, al[0] + '/' + f + '/align.' + f, f)

f = form[0]
with open("talign.txt") as file:
	with open(al[0] + '/' + f + '/align.' + f, "w") as f1:
		f1.write("begin sets;\n")
		for line in file:
			f1.write(line)
		f1.write("end;\n")

### Make alignments with Muscle, and new gap penalties (FASTA) ==============================
openGap = '-15'
extendGap = '-7'
f0 = form[2]

for i in range(len(g)):
	input = al[0] + '/' + f0 + '/align_' + g[i] + '.' + f0
	output = al[1] + '/' + f0 + '/align_' + g[i] + '.' + f0
	subprocess.call(['chmod', '+x', 'soft/muscle3.8.31_i86linux64'])
	subprocess.call(
		['soft/muscle3.8.31_i86linux64', '-in', input, '-out', output, '-gapopen', openGap, '-gapextend', extendGap])
input = al[0] + '/' + f0 + '/align.' + f0
output = al[1] + '/' + f0 + '/align.' + f0
subprocess.call(['soft/muscle3.8.31_i86linux64', '-in', input, '-out', output, '-gapopen', openGap, '-gapextend', extendGap])

#save new alignments in other formats
mfilenames = os.listdir(al[1] + '/' + f0)
mpaths = [al[1] + '/' + f0 + '/' + f for f in mfilenames]
for i in range(len(mpaths)):
	a0 = aio.read(open(mpaths[i]), f0)
	mfilename = os.path.splitext(mfilenames[i])[0]
	aio.convert(mpaths[i], 'fasta', al[1] + '/phylip/' + mfilename + '.phylip', 'phylip')
	aio.convert(mpaths[i], 'fasta', al[1] + '/nexus/' + mfilename + '.nexus', 'nexus', alphabet=Alphabet.generic_dna)
a0 = aio.read(open(al[1] + '/' + f0 + '/align.' + f0), f0)
aio.convert(mpaths[i], 'fasta', al[1] + '/phylip/align.phylip', 'phylip')
aio.convert(mpaths[i], 'fasta', al[1] + '/nexus/align.nexus', 'nexus', alphabet=Alphabet.generic_dna)

### Convert Zahra's files to phylip =============================
# directory = os.getcwd() + '/beast/mus'
# faspaths = os.listdir(directory)
# for i in faspaths:
# 	i1 = directory + '/' + i
#	a = aio.read(directory + '/' + i, 'fasta')
#	i2 = i1.strip('.fas')
#	aio.write(a, i2 + '.phy', 'phylip')



### Make combined nexus files with missing as (?) instead of (-) =======================
fo = form[0]

for nexpath_ in al:
	nexpath = nexpath_ + '/' + fo
	nexpaths = [nexpath + '/' + f for f in os.listdir(nexpath) if '.' + fo in f]
#	nexpaths = [f for f in nexpaths if 'Mitochondrial' not in f and 'Nuclear' not in f and 'Coding' not in f and '_all' not in f]
	nexp = []
	for i in geneOrder:
		h = [f for f in nexpaths if i in f]
		nexp.append(h[0])
	nexpm = []
	for i in geneOrder[0:16]:
		h = [f for f in nexpaths if i in f]
		nexpm.append(h[0])
	nexpn = []
	for i in geneOrder[16:]:
		h = [f for f in nexpaths if i in f]
		nexpn.append(h[0])

	#save in all three concatenations
	nexi = [(fname, Nexus.Nexus.Nexus(fname)) for fname in nexp]
	combined = Nexus.Nexus.combine(nexi)
	combined.write_nexus_data(filename=open(nexpath + '/' + 'align_all.nexus', 'w'))
	nexi = [(fname, Nexus.Nexus.Nexus(fname)) for fname in nexpm]
	combined = Nexus.Nexus.combine(nexi)
	combined.write_nexus_data(filename=open(nexpath + '/' + 'align_allmit.nexus', 'w'))
	nexi = [(fname, Nexus.Nexus.Nexus(fname)) for fname in nexpn]
	combined = Nexus.Nexus.combine(nexi)
	combined.write_nexus_data(filename=open(nexpath + '/' + 'align_allnuc.nexus', 'w'))

for nexpath_ in al:
	nexpath = nexpath_ + '/' + fo
	f = open(nexpath + '/align_all.' + fo, 'r').read()

	# add assumptions to include concatenated genes; below are given.
#	if nexpath_ == al[0]:
#		f = f.replace('begin sets;', 'begin sets;\n' +
#		              'charset Mitochondrial = 1-16848;\n' +
#		              'charset mtDNA_Coding =  1-11400;\n' +
#		              'charset Nuclear = 15582-31508;\n')
#	else:
#		f = f.replace('begin sets;', 'begin sets;\n' +
#		              'charset Mitochondrial = 1-15581;\n' +
#		              'charset mtDNA_Coding =  1-12588;\n' +
#		              'charset Nuclear = 16849-29393;\n')

	#save file
	s = open(nexpath + '/align_all_.' + fo, 'w')
	s.write(f)
	s.close()
	# os.remove(nexpath + '/align_all.' + fo) #optional: delete original file if fixed

	a0 = aio.read(open(nexpath + '/align_all_.' + fo), fo)
	for f0 in form[1:]:
		aio.write(a0, nexpath_ + '/' + f0 + '/align_all_.' + f0, f0)



### TEST: read tre files, print images
# tree = phy.read('RAxML_bestTree.align_Cytb_red.tre', 'newick')
# oldstdout = sys.stdout
# sys.stdout = open('RAxML_bestTree.align_Cytb_red.txt', 'w')
# phy.draw_ascii(tree)
# sys.stdout = oldstdout







# ---------------------------------------
