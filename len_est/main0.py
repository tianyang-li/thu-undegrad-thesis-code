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
from utils.uniform_test_0 import pval
from utils import len_est_0


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

        if gl.chrom not in chroms:
            continue
        
        exon_overlap = False
        
        #TODO: split ovrelaping exons into smaller sections???
        for i in xrange(len(gl.exons) - 1):
            if gl.exons[i].end > gl.exons[i + 1].start:
                exon_overlap = True
                break
            
        if exon_overlap:
            continue
        
        if len(gl.exons) != 1:
            continue
        
        exon = gl.exons[0]
        
        if exon.start + 75 > exon.end:
            continue
        
        reads = [r for r in bam.fetch(gl.chrom, exon.start, exon.end)]

        if not reads:
            continue
        
        no_splice = True
        for r in reads:
            if r.alen > 75:
                no_splice = False
        if not no_splice:
            continue

        reads_pos = [r.pos for r in reads]
        if len(reads_pos) < 2:
            continue
        reads_pos.sort()
        
        if (reads_pos[0] < exon.start
            or reads_pos[-1] + 75 >= exon.end):
            continue
        
        eff_len = exon.end - exon.start - 75
        eff_start = exon.start
        eff_end = exon.end - 75
        cov_lambda = len(reads_pos) / eff_len
        
        counts = [0 for _ in xrange(eff_end - eff_start)]
        for pos in reads_pos:
            counts[pos - eff_start] += 1
        counts_str = ",".join("%d" % c for c in counts)
        
        cur_pval = pval(reads_pos, eff_start, eff_end)
        
        est_len = len_est_0.single_reads(reads_pos)
        
        print eff_start, eff_end, eff_len, cov_lambda, reads_pos[0], reads_pos[-1], counts_str, cur_pval, est_len
        
        
            
if __name__ == '__main__':
    main()
