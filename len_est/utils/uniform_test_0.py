# Tianyang Li 2013
# ty@li-tianyang.com


from __future__ import division

from random import randint


def unif_stat(samples, lower, higher):
    """
    test statistic assuming $samples are IID samples
    from a discrete distribution on [$lower, $higher]
    
    $samples is sorted from min to max
    """
    #TODO: use somethin better than chi square?
    counts = [0 for _ in xrange(lower, higher + 1)]
    for s in samples:
        counts[s - lower] += 1
    freq = len(samples) / (higher - lower + 1)
    return sum((c - freq) ** 2 / freq for c in counts)


def pval(samples, lower, higher):
    """
    give p-value for whether $samples are IID samples
    from discrete distribution on [$lower, $higher]
    
    $sample  sorted samples from min to max
    
    parametric bootstrap p-value
    """
    
    # number of simulation to get p-value
    SIM_NUM = 1000  # TODO: change this?
    
    n_extreme = 0
    
    my_stat = unif_stat(samples, lower, higher)
    
    for _ in xrange(SIM_NUM):

        rand_samples = [randint(lower, higher) for _ in xrange(len(samples))]
        rand_samples.sort()
        
        if unif_stat(rand_samples, lower, higher) >= my_stat:
            n_extreme += 1
    
    return n_extreme / SIM_NUM





