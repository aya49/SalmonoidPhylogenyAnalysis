# Alice Yue; Last modified 20161208

# Before running this code, please run align.py to get all the input alignments ready!
# Input: Alignments (phylip)
# Output: RAxML bootstrap trees, majority consensus trees

import os, subprocess

### Set and create directories where raxml files will be saved ========================================
#o for original alignment, m for muscle alignments
al = ['align/o', 'align/m'] #path of alignments (input)
rax = ['raxml/o', 'raxml/m'] #path of raxml files (output)

if not os.path.exists('raxml'):
    os.makedirs('raxml')
for r in rax:
	if not os.path.exists(r):
		os.makedirs(r)
	if not os.path.exists(r + '/consensus'):
		os.makedirs(r + '/consensus')
	if not os.path.exists(r + '/bootstrap'):
		os.makedirs(r + '/bootstrap')
	if not os.path.exists(r + '/consensus/fig'):
		os.makedirs(r + '/consensus/fig')



### Run raxml from console ================================================
model = 'GTRGAMMA' #substitution model to be used
bs = '1000' #number of bootstraps

#IMPORTANT: install raxml first!
fo = 'phylip'
for j in range(len(rax)):
	input = [i for i in os.listdir(al[j] + '/' + fo) if '.' + fo in i]
	for i in input:
		filename = i.split('.', 1)[0]
		inpath = al[j] + '/' + fo + '/' + i
		bootpath = rax[j] + '/bootstrap/RAxML_bootstrap.' + filename
		#run raxml
		subprocess.call(['raxmlHPC', '-f', 'a', '-x', '12345', '-p', '123456', '-#', bs, '-m', model, '-s', inpath, '-n', filename, '-w', os.path.abspath(rax[j] + '/bootstrap')])
		#run raxml majority consensus trees
		subprocess.call(['raxmlHPC', '-J', 'MR', '-m', model, '-z', bootpath, '-n', bootpath, '-w', os.path.abspath(rax[j] + '/consensus')])

#do majority consensus trees seperately
#for j in range(1):
#	input = [i for i in os.listdir(rax[j] + '/' + 'bootstrap') if 'bootstrap' in i]
#	for i in input:
#		filename = i.split('.', 1)[1]
#		bootpath = rax[j] + '/bootstrap/' + i
#		subprocess.call(['raxmlHPC', '-J', 'MR', '-m', model, '-z', bootpath, '-n', filename, '-w', os.path.abspath(rax[j] + '/consensus2/')])
