import csv
import itertools
import srkdata
import srkmisc
from ROOT import TFile, gDirectory, TH1, gROOT, TH1D

__author__ = "Matthew Bales"
__credits__ = ["Matthew Bales"]
__license__ = "GPL"
__maintainer__ = "Matthew Bales"
__email__ = "matthew.bales@gmail.com"


def read_delimited_txt(txt_file_path, delimiter='\t', quotechar='"', skipchar='#'):
    """Reads in data from a text file in delimited formats."""
    txt_file = open(txt_file_path, 'rt')
    data = []
    try:
        reader = csv.reader(txt_file, delimiter=delimiter, quotechar=quotechar)
        for row in reader:
            if not row[0].startswith(skipchar):
                data.append(row)
    finally:
        txt_file.close()
    return data


def delimited_text_to_data(file_path, delim='\t'):
    """Reads in data from a text file in delimited formats."""
    f = open(file_path, 'rt')

    line = f.readline()
    titles = ""
    if line.startswith("#"):
        titles = line[1:]
    else:
        f.seek(0)

    data = []
    try:
        test_columns, reader = itertools.tee(csv.reader(f, delimiter=delim))
        columns = len(next(test_columns))
        del test_columns
        for a in reader:
            data.append([float(x) for x in a])
    finally:
        f.close()

    if columns == 2:
        data_out = zip(*data)

    elif columns == 3:
        data_out = zip(*data)

    elif columns == 4:
        data_out = zip(*data)
    else:
        print "Too many columns"
        return None

    if titles == "":
        return data_out
    else:
        return data_out, titles.split(';', 1)


def make_txt_from_hist(file_path, histogram, titles=("", "", "")):
    """Converts a TH1 histogram to a text file."""
    f = open(file_path, 'w')
    if titles[0] != "" or titles[1] != "" or titles[2] != "":
        f.write("#" + titles[0] + ";" + titles[1] + ";" + titles[2])
    for i in xrange(histogram.GetNbinsX()):
        out_str = "%f\t%f\t%f" % (
        histogram.GetBinCenter(i + 1), histogram.GetBinContent(i + 1), histogram.GetBinError(i + 1))
        f.write(out_str)
        if i != histogram.GetNbinsX() - 1:
            f.write("\n")
    f.close()


def make_txt_hist_from_root_file(file_path_txt, rid, is_parallel, draw_string, hist_dim, cut_string="",
                                 option_string="", titles=("", "", "")):
    """Given a draw/cut string, take an SRK ROOT results file and create a histogram from it."""

    if is_parallel:
        letter = 'P'
    else:
        letter = 'A'
    file_path = srkdata.srkglobal.results_dir + "Results_RID" + str(rid) + "_" + letter + ".root"

    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return

    root_file = TFile(file_path, "READ")
    hit_tree = gDirectory.Get('hitTree')
    gROOT.cd()

    histogram = TH1D("tempHist", "tempHist", hist_dim[0], hist_dim[1], hist_dim[2])
    total_draw_string = draw_string + " >> tempHist"
    hit_tree.Draw(total_draw_string, cut_string, option_string)

    make_txt_from_hist(file_path_txt, histogram, titles)

    root_file.Close()

    return
