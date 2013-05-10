#!/usr/bin/env python


# Tianyang Li 2013
# ty@li-tianyang.com


import sys
import getopt

from utils.build_gene_loci_0 import get_loci


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   '',
                                   ['gtf='])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    
    gtf_file = None
    
    for o, a in opts:
        if o == '--gtf':
            gtf_file = a
    
    if not gtf_file:
        print >> sys.stderr, "missing GTF file"
        sys.exit(1)
        
    gene_loci = get_loci(gtf_file)
    for gl in gene_loci.itervalues():
        if len(gl.isoforms) == 1:
            print gl
    
        
if __name__ == '__main__':
    main()
