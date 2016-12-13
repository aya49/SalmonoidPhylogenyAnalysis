#!/bin/bash
# -# number of bootstraps
# -m model type

raxmlHPC -f a -x 12345 -p 123456 -# 1000 -m GTRGAMMA -s path/to/alignment/file.phylip -n outputname -w /absolute/directory/where/raxml/outputs/its/files
