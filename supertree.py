#Isolate the best trees from the raxML bootstrap output.
#Output a single file containing the best trees for each gene, one tree per line.
#Different files for nuclear data and mitochondrial data.


from os import listdir
from os.path import join, isfile
import glob

path = '/home/aniket/PycharmProjects/Salmons/DATA/phylogenies/raxML_trees/bootstrap=1000_original/All/'
#Replace the above path by the relevant one on your system

file = open("best_ml", "a")         #create a file to output the best trees
#bs_paths = open("bs_paths", "w")

for filename in [f for f in listdir(path) if isfile(join(path, f))]:
    if "bestTree" in filename:
        print filename
        nwkFile = open((path+filename), "r+")
        content = nwkFile.read()
        file.write(str(content))
        nwkFile.close()
    #if "bestTree" in filename:
    #    print filename
    #    bs_paths.write(str(path+filename))
    #    bs_paths.write("\n")

file.close()


#bs_paths.close()

 