# Tianyang Li 2013
# ty@li-tianyang.com


import re
from collections import namedtuple

from sort_0 import cmp_to_key


"""
$start $end (integers)
same as python convetion
"""
class Exon(namedtuple('Exon', ['start', 'end', 'strand'])):
    def __hash__(self):
        return hash((self.start, self.end))
    

def exon_cmp(x, y):
    if x.start == y.start:
        return x.end - y.end
    return x.start - y.start


ExonKey = cmp_to_key(exon_cmp)


"""
$gene_id (string)
ID of gene locus

$exons (list)
"""
Isoform = namedtuple('Isoform',
                     ['exons', 'chrom', 'id', 'gene_id'])


"""
$isoforms (dictionary)

$exons (list)
"""
class GeneLocus(object):
    __slots__ = ['id', 'isoforms', 'chrom', 'exons']
    
    def __init__(self, gl_id, isoforms, chrom, exons):
        self.id = gl_id
        self.isoforms = isoforms
        self.chrom = chrom
        self.exons = exons


def get_loci(gtf_file):
    """
    return a dict $gene_loci
    
        gene_loci[gene_id] (dict of isoforms)
            -> [isof_id]
                -> Isoform
         
    """
    
    with open(gtf_file, 'r') as fin:
        
        gene_loci = {}
        
        get_gene_id = re.compile(r' gene_id "(\S+)"')
        get_isof_id = re.compile(r'transcript_id "(\S+)"')
        
        for line in fin:
            
            line = line.strip().split("\t")
            
            if line[2] == 'exon':
                # to use with ENCODE download
                line[0] = "chr%s" % line[0]
            
                line_attrb = line[-1].split("; ")
                
                gene_id = get_gene_id.match(line_attrb[0]).group(1)
                
                isof_id = get_isof_id.match(line_attrb[1]).group(1)
                
                (gene_loci
                 .setdefault(gene_id, GeneLocus(gl_id=gene_id,
                                                chrom=line[0],
                                                isoforms={},
                                                exons=None))
                 .isoforms.setdefault(isof_id, Isoform(exons=[],
                                                       chrom=line[0],
                                                       id=isof_id,
                                                       gene_id=gene_id))
                 .exons.append(Exon(start=int(line[3]) - 1,
                                    end=int(line[4]) - 1,
                                    strand=line[6])))
        
        for gl in gene_loci.itervalues():
            
            for isof in gl.isoforms.itervalues():
                isof.exons.sort(key=ExonKey)
            
            gl.exons = set([])
            for isof in gl.isoforms.itervalues():
                for exon in isof.exons:
                    gl.exons.add(exon)
            gl.exons = list(gl.exons)
            gl.exons.sort(key=ExonKey)
                
        return gene_loci
            
            
    
    
