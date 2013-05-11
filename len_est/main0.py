#!/usr/bin/env python


# Tianyang Li 2013
# ty@li-tianyang.com


import sys
import getopt

import pysam

from utils.build_gene_loci_0 import get_loci


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
    
    for gl in gene_loci.itervalues():
        if gl.chrom in chroms:
            if len(gl.isoforms) == 1:
                isof = gl.isoforms.values()[0]
                if len(isof.exons) == 1:
                    # TODO: tolerate errors in $start and $end?
                    
                    isof_covered = True
                    prev_pos = None
                    for col in bam.pileup(isof.chrom,
                                          isof.exons[0].start,
                                          isof.exons[0].end):
                        if prev_pos != None:
                            if col.pos != prev_pos + 1:
                                isof_covered = False
                                break
                        prev_pos = col.pos
                    
                    if isof_covered:
                        reads = [rd for rd in bam.fetch(isof.chrom,
                                                        isof.exons[0].start,
                                                        isof.exons[0].end)]
                    
    
    
        
if __name__ == '__main__':
    main()
