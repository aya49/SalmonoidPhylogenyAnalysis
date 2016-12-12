# cmpt711

The code in this repository builds a pipeline that takes align.txt & talign.txt (the assumptions CHARSET portion of align.txt) and does the following:

Preparing alignments:
1. align.phy: organize, seperate, combine alignments from different genes. Does the same with muscel alignments for comparison.

Build phylogeny
1. raxml.phy: creates raxml phylogeny from alignments made from previous step.
2. beast
Note: bash versions (.sh) files are also available for raxml and beast and lists all files needed to be processed such that they can be seperated and run on different machines if necessary. They may also be embedded into (.pbs) files for submission as jobs on a cluster.
