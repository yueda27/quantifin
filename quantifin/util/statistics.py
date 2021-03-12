from statistics import stdev, mean
from scipy.stats import skew as scipy_skew

def coefficient_of_variation(iterable):
    return round(stdev(iterable) / mean(iterable), 4)

skew = scipy_skew





'''TODO:
    kurtosis
    geometric mean
    arithmetric mean
'''