# Tianyang Li 2013
# ty@li-tianyang.com


import re


def get_loci(gtf_file):
    with open(gtf_file, 'r') as fin:
        get_gene_id = re.compile(r'gene_name "(\S+)"')
        for line in fin:
            gene_str = line.strip().split("\t")[-1].split("; ")[3]
            gene_id = get_gene_id.match(gene_str).group(1)
    
    
