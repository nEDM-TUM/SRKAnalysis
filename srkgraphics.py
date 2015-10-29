from ROOT import TFile, TTree, gDirectory, gROOT,gStyle
import srkdata
import srkmisc
import matplotlib.pyplot as plt
from matplotlib.legend_handler import HandlerLine2D
from pylab import rcParams
import numpy as np
import rootnotes
import rootprint

__author__ = 'mjbales'


def idt(x):
    return x


def line_color_iter(num_lines):
    return iter(plt.cm.rainbow(np.linspace(0,1,num_lines)))


def make_plot_from_database(rids_lines, columns, titles=None, legend_titles=None, lambda_func=[idt,idt,idt,idt]):

    if titles is None:
        titles = [columns[1]+' vs '+ columns[0],columns[0],columns[1]]
    data = srkdata.get_plot_data_from_database_mult(rids_lines, columns)
    make_plot_from_data(data, titles, legend_titles, lambda_func)


def make_plot_from_data(data, titles=None, legend_titles=None, lambda_func=[idt,idt,idt,idt]):

    rcParams['figure.figsize'] = 10, 8
    rcParams['xtick.labelsize'] = 20

    color = line_color_iter(len(data))

    for i in xrange(len(data)):
        a_line = [map(lambda_func[j], data[i][j]) for j in range(len(data[i]))] # Implement lambda funcs on a line
        # print a_line
        if legend_titles is None:
            legend_title=""
        else:
            legend_title=legend_titles[i]

        if len(a_line) == 4:
            x, y, x_err, y_err = a_line
            plt.errorbar(x, y, xerr=x_err, yerr=y_err,marker='o',label = legend_title,c=next(color))
        elif len(a_line) == 3:
            x, y, y_err = a_line
            plt.errorbar(x, y, yerr=y_err,marker='o',label = legend_title,c=next(color))
        elif len(a_line) == 2:
            x, y = a_line
            # print x
            plt.errorbar(x, y, marker='o',label = legend_title,c=next(color))
        else:
            print "Incorrect number found in data for plotting"
            print a_line
            return

    plt.tick_params(labelsize=15)
    plt.xlabel(titles[1], fontsize=18)
    plt.ylabel(titles[2], fontsize=18)
    plt.title(titles[0], fontsize=26)
    plt.grid(True)
    if legend_titles is not None:
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0.)


def make_root_plot_from_results_file(rid, is_parallel, draw_string, cut_string = "", option_string=""):
    # gStyle.SetOptStat("iMRKS")

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

    c1 = rootnotes.canvas("Canvas", (1200, 800))
    hit_tree.Draw(draw_string,cut_string,option_string)
    return c1



