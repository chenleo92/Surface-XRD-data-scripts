#!/usr/bin/python2
# To use this script, open terminal, type "python thisscript.py xyzfile", then you will get the output in terminal.
# First parameter as xyz filename, second name as lattice constant

from __future__ import print_function
import csv,sys
filename=sys.argv[1]
lc=float(sys.argv[2])
with open(filename) as xyzfile:
    n=1
    for line in xyzfile.readlines()[3:]:
        array = line.split()
        print("add_atom(" + "id='"+array[0]+str(n)+"'"+","+"el='"+array[0]+"'"+','+'x='+str(float(array[1])/lc)+','+'y='+str(float(array[2])/lc) + ',' + 'z='+str(float(array[3])/lc) +")")
        n +=1
