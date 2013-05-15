#!/usr/bin/env python


# Tianyang Li 2013
# ty@li-tianyang.com


from __future__ import division

import getopt
import sys
from random import randint


def my_stat(samples, unif_range):
    """
    chi square?
    """
    counts = [0 for _ in xrange(unif_range)]
    for s in samples:
        counts[s - 1] += 1
    freq = len(samples) / unif_range
    return sum((c - freq) ** 2 / freq for c in counts)
    

def my_pval(samples, unif_range):
    """
    parametric bootstrap
    """
    sample_stat = my_stat(samples, unif_range)
    
    SIM_RUN = 1000
    
    n_extreme = 0
    
    for _ in xrange(SIM_RUN):
        bs_samples = [randint(1, unif_range) for _ in xrange(len(samples))]
        if sample_stat <= my_stat(bs_samples, unif_range):
            n_extreme += 1
    
    return n_extreme / SIM_RUN    


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   '',
                                   ['range=', 'samples='])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    
    sim_range = None
    n_samples = None
    
    for o, a in opts:
        if o == '--range':
            sim_range = int(a)
        if o == '--samples':
            n_samples = int(a)
    
    if sim_range == None:
        print >> sys.stderr, "missing range for distribution"
        sys.exit(1)
    if n_samples == None:
        print >> sys.stderr, "missing number of samples"
        sys.exit(1)
    
    unif = [randint(1, sim_range) for _ in xrange(n_samples)]
    
    non_unif = [randint(1, int(sim_range / 2)) 
                for _ in xrange(int(n_samples / 2))]
    non_unif.extend([randint(1, sim_range) 
                     for _ in xrange(n_samples - int(n_samples / 2))])
    
    print "    unif: %f" % my_pval(unif, sim_range)
    print "non-unif: %f" % my_pval(non_unif, sim_range)


if __name__ == '__main__':
    main()    

