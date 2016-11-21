import math
import numpy as np
import os.path
import csv
import itertools
from ROOT import TFile, TGraphErrors, gRandom
from array import array

__author__ = "Matthew Bales"
__credits__ = ["Matthew Bales"]
__license__ = "GPL"
__maintainer__ = "Matthew Bales"
__email__ = "matthew.bales@gmail.com"


def even_sample_over_log(start, stop, num_steps):
    """Make a range of even samples over a log distribution."""
    log_start = math.log10(start)
    log_stop = math.log10(stop)
    log_step = (log_stop - log_start) / (num_steps - 1)

    l = []
    for i in range(0, num_steps):
        l += [pow(10., log_start + i * log_step), ]

    return l


# For ensuring floating point error loss is minimized around a local mean
def careful_mean(data):
    """Takes extra care to minimize a potential floating point certainty loss"""
    temp_mean = np.mean(data)
    mean = 0.
    for x in data:
        mean += x - temp_mean
    mean /= len(data)
    mean += temp_mean
    return mean


def careful_std(phi_array, use_bessel_correction=True):
    """Takes extra care to minimize a potential floating point certainty loss"""
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
    """Returns result which ensures that datum is within one period.
        I.E. reduce_periodic(1.5*math.pi) => -.5*math.pi"""
    period = period_upper - period_lower
    answer = x

    fract_part, int_part = math.modf((x - period_lower) / period)

    if x > period_upper:
        answer = fract_part * period + period_lower
    elif x < period_lower:
        answer = fract_part * period + period_upper
    return answer


def reduce_periodics(data, period_lower=-math.pi, period_upper=math.pi):
    """Returns result which ensures that data is within one period.
        I.E. reduce_periodic(1.5*math.pi) => -.5*math.pi"""
    temp_mean = careful_mean(data)
    mean = 0.
    for i in xrange(len(data)):
        data[i] = reduce_periodic(data[i], period_lower + temp_mean, period_upper + temp_mean)
        mean += data[i]
    mean /= len(data)

    return mean


def file_exits_and_not_zombie(file_path):
    """Checks for existence of ROOT file and ensures it is not a zombie and has its keys"""
    if os.path.isfile(file_path):
        f = TFile(file_path)
        if f.IsZombie() or f.GetSeekKeys() == 0:
            f.Close()
            return False
        else:
            f.Close()
            return True
    else:
        return False


def chunk_list(the_list, chunks):
    """Takes list and creates a list of lists with appropriate number of chunks."""
    return [the_list[x:x + chunks] for x in xrange(0, len(the_list), chunks)]


def flatten_list(the_list):
    """Flattens list of lists to just a list"""
    return [item for sub_list in the_list for item in sub_list]


def delimited_text_to_TGraphErrors(file_path, delim='\t'):
    """convert delimited text data to ROOT TGraphErrors data"""
    f = open(file_path, 'rt')

    line = f.readline()
    if line.startswith("#"):
        titles = line[1:]
    else:
        titles = file_path
        f.seek(0)

    # x = []
    # y = []
    # xE = []
    # yE = []
    data = []
    try:
        test_columns, reader = itertools.tee(csv.reader(f, delimiter=delim))
        columns = len(next(test_columns))
        del test_columns
        for a in reader:
            data.append(a)
            # if columns == 2:
            #     for a,b in reader:
            #         x.append(a)
            #         y.append(b)
            #         xE.append(0)
            #         yE.append(0)
            # elif columns == 3:
            #     for a,b,c in reader:
            #         x.append(a)
            #         y.append(b)
            #         yE.append(c)
            #         xE.append(0)
            # elif columns == 4:
            #     for a,b,c,d in reader:
            #         x.append(a)
            #         y.append(b)
            #         xE.append(c)
            #         yE.append(d)
    finally:
        f.close()

    if columns == 2:
        a, b = zip(*data)
        a = [float(i) for i in a]
        b = [float(i) for i in b]
        x = array("d", a)
        y = array("d", b)
        out_graph = TGraphErrors(len(x), x, y)

    elif columns == 3:
        a, b, c = zip(*data)
        a = [float(i) for i in a]
        b = [float(i) for i in b]
        c = [float(i) for i in c]
        x = array("d", a)
        y = array("d", b)
        y_error = array("d", c)
        out_graph = TGraphErrors(len(x), x, y, ROOT.nullptr, y_error)

    elif columns == 4:
        a, b, c, d = zip(*data)
        a = [float(i) for i in a]
        b = [float(i) for i in b]
        c = [float(i) for i in c]
        d = [float(i) for i in d]
        x = array("d", a)
        y = array("d", b)
        x_error = array("d", c)
        y_error = array("d", d)
        out_graph = TGraphErrors(len(x), x, y, x_error, y_error)
    else:
        print "Too many columns"
        return None
    out_graph.SetName(file_path.split('/')[-1])
    out_graph.SetTitle(titles)
    return out_graph


def skip_comment_lines(opened_file, comment_delim='#'):
    """Skips comment lines designated by a comment delimiter."""
    pos = opened_file.tell()
    for line in opened_file:
        if line[0] != comment_delim:
            opened_file.seek(pos)  # Go back
            return
        else:
            pos = opened_file.tell()
    return


def get_hist_dim(hist):
    """Get ROOT TH1 dimensions in list format."""
    return [hist.GetNbinsX(), hist.GetBinLowEdge(1),
            hist.GetBinWidth(hist.GetNbinsX()) + hist.GetBinLowEdge(hist.GetNbinsX())]
