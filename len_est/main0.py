#!/usr/bin/env python


# Tianyang Li 2013
# ty@li-tianyang.com


"""
analyze single Illumina 75 bp reads
"""


from __future__ import division

import sys
import getopt

import pysam

from utils.build_gene_loci_0 import get_loci
from utils.select_high_cov_frags_0 import expected_len
from utils.len_est_0 import single_reads
from utils.uniform_test_0 import pval


def main():
    try:
        opts, args = getopt.getopt(sys.argv[1:],
                                   '',
                                   ['gtf=', 'bam='])
    except getopt.GetoptError as err:
        print >> sys.stderr, str(err)
        sys.exit(1)
    
    gtf_file = None
    bam_file = None
    
    for o, a in opts:
        if o == '--gtf':
            gtf_file = a
        if o == '--bam':
            bam_file = a
    
    if not gtf_file:
        print >> sys.stderr, "missing GTF file"
        sys.exit(1)
    if not bam_file:
        print >> sys.stderr, "missing BAM file"
        sys.exit(1)
        
    gene_loci = get_loci(gtf_file)

    bam = pysam.Samfile(bam_file, 'rb')
    chroms = set(bam.references)
    
    # TODO: consider splicing???
    for gl in gene_loci.itervalues():
        if gl.chrom in chroms:
            
            gl.exons = set([])
            for isof in gl.isoforms.itervalues():
                for exon in isof.exons:
                    gl.exons.add(exon)
            gl.exons = list(gl.exons)
            gl.exons.sort(key=lambda e: e.start)
                                    
            
if __name__ == '__main__':
    main()
