#!/usr/bin/python
# python parser module to analyse Features in sRbowtie alignments (guided by a GFF3 file)
# version 0.9
# Usage FeaturesParser.py  <1:index source> <2:extraction directive> <3:output> <4:GFF3 guide file> <5:6:7 filePath:FileExt:FileLabel> <.. ad  lib>

import sys
from smRtools import *
from collections import *

IndexSource = sys.argv[1]
ExtractionDirective = sys.argv[2]
if ExtractionDirective == "--do_not_extract_index":
  genomeRefFormat = "fastaSource"
elif  ExtractionDirective == "--extract_index":
  genomeRefFormat = "bowtieIndex"
Output = sys.argv[3]
GFF3_file = sys.argv[4]
Triplets = [sys.argv[5:][i:i+3] for i in xrange(0, len(sys.argv[5:]), 3)]
MasterListOfGenomes = {}
FeatureDict = defaultdict(dict)

for [filePath, FileExt, FileLabel] in Triplets:
  MasterListOfGenomes[FileLabel] = HandleSmRNAwindows (filePath, FileExt, IndexSource, genomeRefFormat) 
  FeatureDict[FileLabel] = MasterListOfGenomes[FileLabel].CountFeatures(GFF3=GFF3_file)


header = ["Feature"]
for [filePath, FileExt, FileLabel] in Triplets:
  header.append(FileLabel)



F = open (sys.argv[3], "w")
print >> F, "\t".join(header)
for feature in  FeatureDict[header[1]]:
  line=[feature]
  for sample in header[1:]:
    count = str (FeatureDict[sample][feature])
    line.append(count)
  print >> F,  "\t".join(line )
print >>F, "_______________"
print >>F, MasterListOfGenomes[header[1]].alignedReads
F.close()
