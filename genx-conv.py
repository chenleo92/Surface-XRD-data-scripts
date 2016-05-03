
#!/usr/bin/python2
# To use this script, open terminal, type "python thisscript.py xyzfile", then you will get the output in terminal

from __future__ import print_function
import csv,sys
with open(sys.argv[1]) as xyzfile:
    for line in xyzfile.readlines()[3:]:
        array = line.split()
        print("add_atom(" + "id='"+array[0]+"'"+","+"el='"+array[0]+"'"+','+'x='+array[1]+','+'y='+array[2] + ',' + 'z='+array[3] +")")
