import math
import numpy as np
import os.path
from ROOT import TFile

__author__ = 'mjbales'


def even_sample_over_log(start, stop, num_steps):
    log_start = math.log10(start)
    log_stop = math.log10(stop)
    log_step = (log_stop - log_start) / (num_steps - 1)

    l = []
    for i in range(0, num_steps):
        l += [pow(10., log_start + i * log_step), ]

    return l


# For ensuring floating point error loss is minimized around a local mean
def careful_mean(phi_array):
    temp_mean = np.mean(phi_array)
    mean = 0.
    for x in phi_array:
        mean += x - temp_mean
    mean /= len(phi_array)
    mean += temp_mean
    return mean


def careful_std(phi_array, use_bessel_correction=True):
    mean = careful_mean(phi_array)
    stdev = 0.

    for x in phi_array:
        stdev += math.pow(x - mean, 2)

    if use_bessel_correction:
        stdev /= len(phi_array) - 1.
    else:
        stdev /= float(len(phi_array))

    stdev = math.sqrt(stdev)
    return stdev


def reduce_periodic(x, period_lower=-math.pi, period_upper=math.pi):
    period = period_upper - period_lower
    answer = x

    fract_part, int_part = math.modf((x - period_lower) / period)

    if x > period_upper:
        answer = fract_part * period + period_lower
    elif x < period_lower:
        answer = fract_part * period + period_upper
    return answer


def reduce_periodics(data, period_lower=-math.pi, period_upper=math.pi):
    temp_mean = careful_mean(data)
    mean = 0.
    for i in xrange(len(data)):
        data[i] = reduce_periodic(data[i], period_lower + temp_mean, period_upper + temp_mean)
        mean += data[i]
    mean /= len(data)

    return mean


def file_exits_and_not_zombie(file_path):
    if os.path.isfile(file_path):
        f = TFile(file_path)
        if f.IsZombie():
            f.Close()
            return False
        else:
            f.Close()
            return True
    else:
        return False



