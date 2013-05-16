# Tianyang Li 2013
# ty@li-tianyang.com


from __future__ import division

from math import exp


def expected_len(cov_param, read_len):
    """
    $cov_param
        number of reads / effective isoform length
    """
    return (exp(cov_param * read_len) - 1) / (exp(cov_param) - 1) - read_len


