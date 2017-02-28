#The following code helps replace the numbers in the BEAST output trees with corresponding species names.

import re
import operator

fh = open("/home/aniket/PycharmProjects/Salmons/DATA/phylogenies/BEAST trees/original/Nucl/temp.tre","r")
#The file 'temp.tre' contains the list of number-species name pairs.
#We use this list as a dictionary to identify and insert the appropriate species names in the tree.
#The file also contains the best trees from the BEAST output (i.e. tree STATE_0).

print "Reading file\n"

def find_parens(s):
    toret = {}
    pstack = []

    for i, c in enumerate(s):
        if c == '[':
            pstack.append(i)
        elif c == ']':
            if len(pstack) == 0:
                raise IndexError("No matching closing parens at: " + str(i))
            toret[pstack.pop()] = i

    if len(pstack) > 0:
        raise IndexError("No matching opening parens at: " + str(pstack.pop()))

    return toret

new_dict = {}
count = 1
ten = 0
hundred = 0
delimit = 0
for line in fh:
    if ';' not in line and delimit == 0:
        elem = line.split(" ")
        if count/100: hundred = 1
        if hundred == 0:
            if count / 10: ten = 1
            if ten == 0:
                number = int(elem[3])
                text = str(elem[4]).replace(',', ' ')
                text = text.replace('\n', '')
                print number, "-", text
                new_dict[number] = text
            else:
                number = int(elem[2])
                text = str(elem[3]).replace(',', ' ')
                text = text.replace('\n', '')
                print number, "-", text
                new_dict[number] = text
        else:
            number = int(elem[1])
            text = str(elem[2]).replace(',', ' ')
            text = text.replace('\n', '')
            print number, "-", text
            new_dict[number] = text
    elif ';' in line:
        delimit += 1
    if delimit == 2:
        text = line
        if len(line)>1:
            for key in new_dict.keys():
                text = str(text).replace('(' + str(key) + ':', '(' + new_dict[key] + ':')
                text = str(text).replace(',' + str(key) + ':', ',' + new_dict[key] + ':')
                text = text.replace(' ','')

            dict = find_parens(text)
            sorted_dict = sorted(dict.items(), key=operator.itemgetter(0), reverse=True)
            print sorted_dict

            for key in sorted_dict:
                str = text[key[0]: key[1] + 1]
                text = text.replace(str, '')

            print text

            new_file = open("/home/aniket/PycharmProjects/Salmons/DATA/phylogenies/BEAST trees/original/Nucl/output.tre","a")
            new_file.write(text)
            new_file.close()

    count+=1

fh.close()

