#!/usr/bin/env python


# Tianyang Li 2013
# ty@li-tianyang.com


"""
plot 
    X - isoform len
    Y - max(read_pos) - min(read_pos)
"""


from __future__ import division

import matplotlib
matplotlib.rcParams['backend'] = 'Qt4Agg' 

import sys
import getopt


def pval2colorval(pval):
    if pval <= 0.4:
        return 1 / 3
    if pval <= 0.8:
        return 2 / 3
    return 1
    

def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:], '',
                                   ['adjusted-pval=',
                                    'all-val'])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    
    adjusted_pvals_file = None
    all_vals_file = None
    
    for o, a in opts:
        if o == '--adjusted-pval':
            adjusted_pvals_file = a
        if o == '--all-val':
            all_vals_file = a

    if not adjusted_pvals_file:
        print >> sys.stderr, "missing adjusted pval file"
        sys.exit(1)
    if not all_vals_file:
        print >> sys.stderr, "missing all val file"
        sys.exit(1)
        
    MAX_LEN = 6000
    
    """
    $isof_pvals[$isof_len][$contig_len] is the 
    """
    isof_pvals = [[0 for _ in xrange(MAX_LEN)] 
                  for _ in xrange(MAX_LEN + 1)] 
    
        
if __name__ == '__main__':
    main()


        


