# Tianyang Li 2013
# ty@li-tianyang.com


from __future__ import division

from math import exp


def expected_len(cov_param, read_len):
    """
    $cov_param
        (number of reads) / (effective isoform length)
    """
    return sum(exp(i * cov_param) for i in xrange(read_len)) - read_len




