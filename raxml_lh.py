# Alice Yue; Last modified 20161208

# Before running this code, please run raxml.py to get all the input raxml info files ready!
# Input: RAxML Info files after creating trees in raxml
# Output: summary of likelihood scores and inferred substitution rates

import os
import numpy as np
#from ete3 import Tree
#from Bio import Phylo
#import pylab as pl

al = ['align/o', 'align/m']
form = ['nexus', 'phylip', 'fasta']
rax = ['raxml/o', 'raxml/m']

input = [i for i in os.listdir(rax[0] + '/bootstrap') if '_info.' in i]
input = [rax[0] + '/bootstrap/' + i for i in input]
row = ['o/' + i for i in input]
input2 = [i for i in os.listdir(rax[1] + '/bootstrap') if '_info.' in i]
input2 = [rax[1] + '/bootstrap/' + i for i in input2]

m = np.zeros((len(input),7))
m2 = np.zeros((len(input2),7))

#input.append(input2)
row.append(['m/' + i for i in input2])

#column values: values to be extracted
col = ['Likelihood', 'rate A<>C','A<>G', 'A<>T', 'C<>G', 'C<>T', 'G<>T']

#print row and column values seperately to file for confirmation
thefile = open('raxml/row.txt', 'w')
for item in row:
  print>>thefile, item
thefile = open('raxml/col.txt', 'w')
for item in col:
  print>>thefile, item

for i in range(len(input)):
	inpath = input[i]

	with open(inpath) as file:
		rate0 = []
		for line in file:
			line = line.rstrip()  # remove '\n' at end of line
			if 'Final ML Optimization Likelihood' in line:
				rate0.append(float(line.split(': ')[1]))
			if '<->' in line:
				rate0.append(float(line.split(': ')[1]))
		if len(rate0) != 0:
			m[i,:] = rate0

for i in range(len(input2)):
	inpath = input2[i]

	with open(inpath) as file:
		rate0 = []
		for line in file:
			line = line.rstrip()  # remove '\n' at end of line
			if 'Final ML Optimization Likelihood' in line:
				rate0.append(float(line.split(': ')[1]))
			if '<->' in line:
				rate0.append(float(line.split(': ')[1]))
		if len(rate0) != 0:
			m2[i,:] = rate0


np.savetxt("raxml/results.csv", m, delimiter=",")
np.savetxt("raxml/results2.csv", m2, delimiter=",")

#nput = [i for i in os.listdir(rax[0] + '/consensus') if '_info.' in i]
#npath = [rax[0] + '/consensus/' + i for i in input]
#nput2 = [i for i in os.listdir(rax[1] + '/consensus') if '_info.' in i]
#inpath2 = [rax[0] + '/consensus/' + i for i in input2]
#input.append(input2)
#input.append(input2)

#for r in rax:
#	input = [i for i in os.listdir(r + '/consensus')]
#	for i in input:
#		inpath = r + '/consensus/' + i
#		outpath = r + '/consensus/fig/' + i + '.png'
#		tree = Phylo.read(inpath, 'newick', comments_are_confidence=True)
#		Phylo.draw(tree, font_size=0.1)
#		pl.savefig(outpath)



