#!/usr/bin/env python


# Tianyang Li 2013
# ty@li-tianyang.com


"""
heat map of reads distribution
"""


from __future__ import division

import matplotlib
matplotlib.rcParams['backend'] = 'Qt4Agg' 

import sys
import getopt
from itertools import izip_longest, izip

import matplotlib.pyplot as plt
from statsmodels.distributions import ECDF


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], '', [])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    
    if len(args) != 1:
        print >> sys.stderr, "specifying wrong input file"
        sys.exit(1)
    
    file_in = args[0]
    
    counts_data = []
    
    with open(file_in, 'r') as fin:
        for line in fin:
            if line[0] == "#":
                continue
            
            counts = map(int, line.strip().split(" ")[-3].split(","))
            counts_data.append(counts)
    
    MAX_LEN = 6000
    
    reads_distr = [[0 for _ in xrange(MAX_LEN + 1)] 
                   for _ in xrange(MAX_LEN + 1)]
    
    for dat in counts_data:
        if len(dat) > MAX_LEN:
            continue
        new_tmp = [c + tmp for c, tmp in 
                   izip_longest(dat, reads_distr[len(dat)], fillvalue=0)]
        reads_distr[len(dat)] = new_tmp
    
    for rd, i in izip(reads_distr[1:], xrange(1, MAX_LEN + 1)):
        tmp_sum = sum(rd)
        
        if tmp_sum == 0:
            continue
        
        new_tmp = map(lambda x: x / tmp_sum * i, rd)
        reads_distr[i] = new_tmp
    
    reads_vals = []
    
    for rd in reads_distr:
        reads_vals.extend(val for val in rd if val > 0)
    
    rv_distr = ECDF(reads_vals)
    
    for rd, i in izip(reads_distr[1:], xrange(1, MAX_LEN + 1)):
        new_tmp = list(rv_distr(rd))
        reads_distr[i] = new_tmp
    
    fig, ax = plt.subplots()
    ax.imshow(reads_distr)
    plt.xlabel("position on isoform")
    plt.ylabel("isoform length")
    plt.show()    

    
if __name__ == '__main__':
    main()


