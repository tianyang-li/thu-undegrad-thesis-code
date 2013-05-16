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
    
    print "#eff_start, eff_end, cov_lambda, cov_e_len, est_len, est_start, est_end, pval(reads_pos, eff_start, eff_end - 1)"
    
    # TODO: consider splicing???
    for gl in gene_loci.itervalues():
        if gl.chrom in chroms:
            if len(gl.isoforms) == 1:
                isof = gl.isoforms.values()[0]
                if len(isof.exons) == 1:
                    # TODO: tolerate errors in $start and $end?
                    
                    exon = isof.exons[0]
                    
                    if exon.start + 75 < exon.end:
                        
                        # TODO: make checking for gaps faster?
                        reads_connected = False
                        prev_pos = None
                        for col in bam.pileup(isof.chrom,
                                              exon.start,
                                              exon.end):
                            if prev_pos != None:
                                if col.pos != prev_pos + 1:
                                    reads_connected = False
                                    break
                            else:
                                reads_connected = True
                                
                            prev_pos = col.pos
                        
                        if reads_connected:
                            reads = [rd for rd in bam.fetch(isof.chrom,
                                                            exon.start,
                                                            exon.end)]
                            
                            if len(reads) > 1:
                                
                                no_splice = True
                                for rd in reads:
                                    if rd.alen > 75:
                                        no_splice = False
                                        break
                                
                                # TODO: check isoform doesn't lie within another?
                                if no_splice:
                                    reads_pos = [rd.pos for rd in reads]
                                    reads_pos.sort()
                                    
                                    if (reads_pos[-1] + 75 < exon.end
                                        and reads_pos[0] >= exon.start):
                                        
                                        counts = [0 for _ in xrange(exon.start, exon.end - 75)]
                                        
                                        for pos in reads_pos:
                                            counts[pos - exon.start] += 1
                                        
                                        for c in counts:
                                            print c,
                                        print 
                                    
            
if __name__ == '__main__':
    main()
