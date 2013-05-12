# Tianyang Li 2013
# ty@li-tianyang.com


from __future__ import division

from random import randint


def unif_stat(samples):
    #XXX: how to get this statistic??
    pass


def pval(samples):
    """
    $sample  sorted samples from min to max
    
    len(sample) >= 3
    """
    
    # number of simulation to get p-value
    SIM_NUM = 1000  # TODO: change this?
    
    n_extreme = 0
    
    my_stat = unif_stat(samples)
    
    # number of locations that can be randomly distributed
    n_rand_loc = len(samples) - 2
    rand_range = samples[-1] - samples[0]
    
    for _ in xrange(SIM_NUM):
        rand_samples = [0]
        for _ in xrange(n_rand_loc):
            rand_samples.append(randint(0, rand_range))
        rand_samples.append(rand_range)
        if unif_stat(rand_samples) >= my_stat:
            n_extreme += 1
    
    return n_extreme / SIM_NUM





