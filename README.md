# Samonoid Species Phylogeny Analysis

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

## 

## [Report](./report.pdf)
+ [Appendix: saturation](./nucleotide_substitution) - BEAST2 substitution parameters

## [Brief Presentation](./presentation.pdf)

Updating in progress
