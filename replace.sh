#!/bin/bash
# This file is to replace exported non-standard atom name XYZ file to standard names to show in visualization software like Jmol.
cat $1 |sed s/ge/Ge/g |sed s/o2m/O/g |sed s/sr2p/Sr/g |sed s/zr/Zr/g |sed s/ti4p/Ti/g >$2
