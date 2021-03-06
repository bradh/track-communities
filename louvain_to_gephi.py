#
# Copyright 2016 Sotera Defense Solutions Inc.
#
# Licensed under the Apache License, Version 2.0 (the "License”);
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
# 
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

#!/usr/bin/env python

import os

os.system("mkdir louvain_to_gephi")
os.system("cat output/giraph_1/part-m* > output/giraph_1/output")

f = open('output/giraph_1/output','r')
o = open('louvain_to_gephi/community_itr_1.nodes','w')

for line in f:
  vals = line.split('\t')
  o.write(vals[0].strip() + '\t' + vals[1].strip() + '\n')
f.close()
o.close()

f = open('edgelist.tsv','r')
o = open('louvain_to_gephi/graph_itr_0.edges','w')

for line in f:
  if len(line.split('\t')) == 3:
    source,weight,edgelist = line.split('\t')
    edgelist = edgelist.strip().split(',')
    for e in edgelist:
      o.write('\t'.join((source,e.split(':')[0],e.split(':')[1])) + '\n')

o.close()
f.close()

# Here's the looping piece

i = 1
pm = 'output/mapreduce_'+str(i)
pg = 'output/giraph_'+str(i+1)
while os.path.exists(pm):
  os.system("cat " + pg + "/part* > " + pg + "/output")
  os.system("cat " + pm + "/part* > " + pm + "/output")
  
  f = open(pg + '/output','r')
  o = open('louvain_to_gephi/community_itr_' + str(i+1) + '.nodes','w')

  for line in f:
    vals = line.split('\t')
    o.write(vals[0].strip() + '\t' + vals[1].strip() + '\n')
  f.close()
  o.close()

  f = open(pm + '/output','r')
  o = open('louvain_to_gephi/graph_itr_' + str(i) + '.edges','w')
  for line in f:
    if len(line.split('\t')) == 3:
      source,weight,edgelist = line.split('\t')
      edgelist = edgelist.strip().split(',')
      for e in edgelist:
        o.write('\t'.join((source,e.split(':')[0],e.split(':')[1])) + '\n')
      if int(weight) != 0:
        o.write('\t'.join((source,source,weight,'\n')))
    elif len(line.split('\t')) == 2:
      source, weight = line.split('\t')
      weight = weight.strip()
      if int(weight) != 0:
        o.write('\t'.join((source,source,weight,'\n')))
  o.close()
  f.close()
  
  i = i + 1
  pm = 'output/mapreduce_'+str(i)
  pg = 'output/giraph_'+str(i+1)

