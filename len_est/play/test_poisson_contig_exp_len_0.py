#!/usr/bin/env python


# Tianyang Li 2013
# ty@li-tianyang.com


from __future__ import division

import getopt
import sys
from math import exp
from random import random

from utils.select_high_cov_frags_0 import expected_len


def sim_len(cov_lambda, read_len):
    prob_read = 1 - exp(-cov_lambda)
    
    cur_len = 0
    cur_space = 1
    
    while random() >= prob_read:
        cur_space += 1
    while cur_space < read_len:
        cur_len += cur_space
        cur_space = 1
        while random() >= prob_read:
            cur_space += 1
    
    return cur_len
    

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                '',
                                ['lambda=', 'runs=', 'read-len='])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
        
    cov_lambda = None
    sim_runs = None
    read_len = None
    
    for o, a in opts:
        if o == '--lambda':
            cov_lambda = float(a)
        if o == '--runs':
            sim_runs = int(a)
        if o == '--read-len':
            read_len = int(a)
    
    if cov_lambda == None:
        print >> sys.stderr, "missing lambda for coverage"
        sys.exit(1)
    if sim_runs == None:
        print >> sys.stderr, "missing number of runs"
        sys.exit(1)
    if read_len == None:
        print >> sys.stderr, "missing read length"
        sys.exit(1)
        
    print "formula: %f" % expected_len(cov_lambda, read_len)
    print "    sim: %f" % (sum(sim_len(cov_lambda, read_len) 
                               for _ in xrange(sim_runs)) / sim_runs)
    

if __name__ == '__main__':
    main()



