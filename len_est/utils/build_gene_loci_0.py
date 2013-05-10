# Tianyang Li 2013
# ty@li-tianyang.com


import re
from collections import namedtuple


"""
$start $end
same as python convetion
"""
Exon = namedtuple('Exon', ['start', 'end'])


Isoform = namedtuple('Isoform', ['exons'])


def get_loci(gtf_file):
    """
    return a dict $gene_loci
    
        gene_loci[gene_id] = list of gene_id's isoforms
         
    """
    with open(gtf_file, 'r') as fin:
        
        get_gene_id = re.compile(r' gene_id "(\S+)"')
        get_isof_id = re.compile(r'transcript_id "(\S+)"')
        
        for line in fin:
            
            line = line.strip().split("\t")
            
            if line[2] == 'exon':
            
                line_attrb = line[-1].split("; ")
                
                gene_id = get_gene_id.match(line_attrb[0]).group(1)
                
                isof_id = get_isof_id.match(line_attrb[1]).group(1)
                
                print gene_id, isof_id
                
                
            
            
    
    
