# ## goal of script is to take large 'cyc' download from e.g. metacyc and make a simple, small XML file with the pathways that one is actually interested in. ###
##import packages, etc. 
#from elementtree.ElementTree import Element, SubElement, parse, fromstring
import elementtree.ElementTree as etree
import sys
import getopt
import re
#set defaults
verbose = False
filem = 'metabolic-reactions.sbml'
filep = 'pathways.dat'
fileout = 'enzymes_out.xml'
#the list of reactions you are interested in. Names must match exactly! locate these in pathway file beforehand.
pathways_oi = ['CALVIN-PWY', 'PWY-241','TCA']

##get opt
fileins, andsecond = getopt.getopt(sys.argv[1:], 'p:m:o:l:hv')


def usage():
    print """python file.py -p pathways.dat -m metabolic-reactions.sbml
-p pathways.dat                 file with pathway information (cyc format)
-m metabolic-reactions.sbml     file with enzyme infos (sbml format)
-o enzymes_out.xml              output xml file
-l CALVIN-PWY,PWY-241,TCA       comma separated list of exact 'UNIQUE - ID's from pathway file
-v                              verbose
-h                              prints this"""
    exit()


for (opt, arg) in fileins:
    if opt == '-p':
        filep = arg
    elif opt == '-m':
        filem = arg
    elif opt == '-o':
        fileout = arg
    elif opt == '-l':
        pathways_oi = arg.split(',')
    elif opt == '-v':
        verbose = True
    elif opt == '-h':
        usage()
    else:
        print 'unrecognized option: ' + str(opt)
        usage()


## read in pathways.dat
#mfile=open(filem)
reading = False
pathdict = {}
pfile = open(filep)
for line in pfile:
    #if at start of pathway, add pathdict dictionary key, start looking for enzymes
    if line.startswith('UNIQUE-ID'):
        x = line.rstrip().replace('UNIQUE-ID - ', '')
        #print x
        if x in pathways_oi:
            pathdict[x] = []
            reading = True
            pathways_oi.remove(x)
    #if pathway over, stop looking for enzymes
    elif line.startswith('//'):
        reading = False
        if len(pathways_oi) == 0:
            break
    #if an enzyme, save ID under pathway key
    elif reading and line.startswith('REACTION-LIST'):
        y = line.rstrip().replace('REACTION-LIST - ', '')
        pathdict[x].append(y)
# live output
if verbose:
    for i in pathdict:
        print i + ':'
        print pathdict[i]
pfile.close()

### opening and cleaning of metabolic reactions file
mfile = open(filem)
instring = mfile.read()
mfile.close()
#elimnate xmlns, which tags everyname in whole file
instring = re.sub('xmlns="\S*"', '', instring)
#eliminate any characters that can't be converted to utf-8
newstring = ''
for i in instring:
    try:
        y = i.encode('utf-8')
    except Exception:
        pass
    newstring += y
#parse xml
tree2 = etree.fromstring(newstring)
#pick out reactions with infos
tree3 = etree.ElementTree(tree2)
#set up destination format
outtree = etree.Element('root')
for i in pathdict:
    j = etree.SubElement(outtree,'pathway')
    j.attrib['name'] = i
    for nodes in tree3.getiterator(tag='reaction'):
        try:
            x = nodes.attrib['name']
            if x in pathdict[i]:
                j.append(nodes)
                #print ('appended?')
        except Exception:
            pass

fintree = etree.ElementTree(outtree)
fintree.write(fileout,encoding='utf-8')

