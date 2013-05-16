# Tianyang Li 2013
# ty@li-tianyang.com


from __future__ import division


def single_reads(reads_pos):
    """
    estimate transcript length from IID single reads
    all of equal length
    
    $reads_pos is sorted from min to max
    """
    #TODO: use more complicated estimator?
    return (len(reads_pos) + 1) / (len(reads_pos) - 1) * (reads_pos[-1] - reads_pos[0])




