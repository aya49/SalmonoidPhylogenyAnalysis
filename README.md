# Salmonoid Species Phylogeny Analysis

The code in this repository builds a pipeline that takes align.txt (original nexus alignment) & talign.txt (the assumptions CHARSET portion of align.txt i.e. which DNA index is which gene) and does the following.
Note: Data can be found [here](https://www.ncbi.nlm.nih.gov/pubmed/23071608).

## 1. Prepare Alignments
  1. [align.py](./align.py): organize, seperate, combine alignments from different genes. Does the same with muscle alignments for comparison1

## 2. Build Phylogeny using RAxML and BEAST2
  1. [raxml.py](./raxml.py) creates raxml phylogeny from alignments made from previous step.
  2. [raxml_lh.py](./raxml_lh.py) extracts likelihood and substitution rates from each raxml tree made by raxml.py.

Note: beast takes (.xml) files as input; these should be made using (.nexus) alignments on the beast GUI application BEAUti.

Note: [raxml_template.sh](./raxml_template.sh) and [beast_template.sh](./beast_template.sh) are templates for the bash versions (.sh) of running raxml and beast commandline programs. They may also be embedded into (.pbs) files for submission as jobs on a cluster.

Note: we recommend running beast on a command line, as working directories cannot be defined directly.

## 3. Extract the best trees from raxML and BEAST output into a single file
  3. [supertree.py](./supertree.py) extracts the best trees from raxML output and copies them into a single file. This file is later used as input for ASTRAL, in order to create a supertree.
  4. [spname.py](./spname.py) extracts the best tree from a temporary file containing the dictionary and best tree obtained from the BEAST output. The appropraitely labelled trees are then copied to a file to be used as for ASTRAL. 

Note: ASTRAL was run on command line. The ASTRAL output is a newick file containing the supertree with its nodes labelled with correponding confidence levels. 
###### The following command was used:
    java -jar astral.4.10.12.jar -i inputfile -o outputfile 2> logfile

Note: ecceTERA was run on command line. Two sets of costs were used for (Dupliaction, HGT, Loss). The costs used were (2,3,1), which was the prescribed default and (2,1,2). The latter choice of cost was to reduce the cost HGT as compared to Duplication and Loss, thus increasing the probability of transfer/introgression. 
###### The following command was used:
    ./ecceTERA_linux64 species.file=address_to_species_file gene.file=address_to_gene_file dupli.cost=2 HGT.cost=1 loss.cost=2 dated=0 print.reconciliations=1 sylvx.reconciliation=true

## [Report](./report.pdf)
+ [Appendix: saturation](./nucleotide_substitution) - BEAST2 substitution parameters

## [Brief Presentation](./presentation.pdf)

Updating in progress
