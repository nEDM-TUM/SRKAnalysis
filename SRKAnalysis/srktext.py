import math
import numpy as np
import os.path
import csv
import itertools
import srkdata
import srkmisc
from ROOT import TFile,  gDirectory, TH1, gROOT,TH1D
from array import array

def delimited_text_to_data(file_path, delim='\t'):
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
            data.append([ float(x) for x in a ])
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


def make_txt_from_hist(file_path, histogram, titles=["", "", ""]):
    f=open(file_path, 'w')
    if titles[0] != "" or titles[1] != "" or titles[2] != "":
        f.write("#"+titles[0]+";"+titles[1]+";"+titles[2])
    for i in xrange(histogram.GetNbinsX()):
        out_str="%f\t%f\t%f" % (histogram.GetBinCenter(i+1),histogram.GetBinContent(i+1),histogram.GetBinError(i+1))
        f.write(out_str)
        if i != histogram.GetNbinsX()-1:
            f.write("\n")
    f.close()



def make_txt_hist_from_root_file(file_path_txt, rid, is_parallel, draw_string, hist_dim,cut_string = "", option_string="", titles=["","",""]):

    srk_sys = srkdata.SRKSystems()
    srk_sys.read_settings_file()

    if is_parallel:
        letter = 'P'
    else:
        letter = 'A'
    file_path = srkdata.SRKSystems.results_dir+"Results_RID"+str(rid)+"_"+letter+".root"

    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return

    root_file = TFile(file_path, "READ")
    hit_tree = gDirectory.Get('hitTree')
    gROOT.cd()

    histogram = TH1D("tempHist","tempHist",hist_dim[0],hist_dim[1],hist_dim[2])
    total_draw_string = draw_string+" >> tempHist"
    hit_tree.Draw(total_draw_string,cut_string,option_string)

    make_txt_from_hist(file_path_txt, histogram, titles)

    root_file.Close()

    return
