# Tianyang Li 2013
# ty@li-tianyang.com


from __future__ import division

from random import randint

from scipy.stats import ks_2samp


def unif_stat(samples, lower, higher):
    """
    test statistic assuming $samples are IID samples
    from a discrete distribution on [$lower, $upper]
    """
    #XXX: how to get this statistic??
    pass


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
    
    my_stat = unif_stat(samples)
    
    for _ in xrange(SIM_NUM):

        rand_samples = [randint(lower, higher) for _ in xrange(len(samples))]
        rand_samples.sort()
        
        if unif_stat(rand_samples) >= my_stat:
            n_extreme += 1
    
    return n_extreme / SIM_NUM





