from statistics import stdev, mean

def coefficient_of_variation(iterable):
    return round(stdev(iterable) / mean(iterable), 4)