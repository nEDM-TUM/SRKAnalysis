from ROOT import TFile, TTree, gDirectory, gROOT, gStyle
import srkdata
import srkmisc
import matplotlib.pyplot as plt
from pylab import rcParams
import numpy as np
import rootnotes
import itertools
import srkglobal

__author__ = "Matthew Bales"
__credits__ = ["Matthew Bales"]
__license__ = "GPL"
__maintainer__ = "Matthew Bales"
__email__ = "matthew.bales@gmail.com"


def idt(x):
    """Returns itself.  Used as placeholder function."""
    return x


def line_color_iter(num_lines):
    """Iterator through rainbow colors."""
    return iter(plt.cm.rainbow(np.linspace(0, 1, num_lines)))


def make_plot_from_database(rids_lines, columns, titles=None, legend_titles=None, lambda_func=(idt, idt, idt, idt)):
    """Makes a plot from database data modified by designated functions."""
    if titles is None:
        titles = [columns[1] + ' vs ' + columns[0], columns[0], columns[1]]
    data = srkdata.get_plot_data_from_database_mult(rids_lines, columns)
    make_plot_from_data(data, titles, legend_titles, lambda_func)


def make_plot_from_data(data, titles=None, legend_titles=None, lambda_func=(idt, idt, idt, idt)):
    """Makes a plot from data modified by designated functions."""

    rcParams['figure.figsize'] = 10, 7
    rcParams['xtick.labelsize'] = 20

    color = line_color_iter(len(data))
    marker = itertools.cycle(('o', '^', 's', 'v', '*'))

    for i in xrange(len(data)):
        a_line = [map(lambda_func[j], data[i][j]) for j in range(len(data[i]))]  # Implement lambda funcs on a line
        # print a_line
        if legend_titles is None:
            legend_title = ""
        else:
            legend_title = legend_titles[i]

        if len(a_line) == 4:
            x, y, x_err, y_err = a_line
            plt.errorbar(x, y, xerr=x_err, yerr=y_err, label=legend_title, c=next(color), marker=marker.next())
        elif len(a_line) == 3:
            x, y, y_err = a_line
            plt.errorbar(x, y, yerr=y_err, label=legend_title, c=next(color), marker=marker.next())
        elif len(a_line) == 2:
            x, y = a_line
            # print x
            plt.errorbar(x, y, label=legend_title, c=next(color), marker=marker.next())
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
        plt.legend(bbox_to_anchor=(1.05, 1), loc=2, borderaxespad=0., numpoints=1)


def make_root_plot_from_results_file(rid, is_parallel, draw_string, cut_string="", option_string=""):
    """Makes a ROOT plot from results file based on a draw and cut string."""

    # gStyle.SetOptStat("iMRKS")

    if is_parallel:
        letter = 'P'
    else:
        letter = 'A'
    file_path = srkglobal.results_dir + "Results_RID" + str(rid) + "_" + letter + ".root"

    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return

    root_file = TFile(file_path, "READ")
    hit_tree = gDirectory.Get('hitTree')
    gROOT.cd()

    c1 = rootnotes.canvas("Canvas", (1200, 800))
    hit_tree.Draw(draw_string, cut_string, option_string)
    root_file.Close()
    return c1


def plot_trend_line(xd, yd, order=1, c='green', alpha=1, Rval=False):
    """Make a line of best fit through x and y data."""

    # Calculate trendline
    coeffs = np.polyfit(xd, yd, order)

    intercept = coeffs[-1]
    slope = coeffs[-2]
    if order == 2:
        power = coeffs[0]
    else:
        power = 0

    minxd = np.min(xd)
    maxxd = np.max(xd)

    print "Slope: " + str(slope)
    print "Intercept: " + str(intercept)
    print minxd, maxxd

    xl = np.array([minxd, maxxd])
    yl = power * xl ** 2 + slope * xl + intercept
    print xl, yl

    # Plot trendline
    plt.plot(xl, yl, c, alpha=alpha)

    # Calculate R Squared
    p = np.poly1d(coeffs)

    ybar = np.sum(yd) / len(yd)
    ssreg = np.sum((p(xd) - ybar) ** 2)
    sstot = np.sum((yd - ybar) ** 2)
    Rsqr = ssreg / sstot

    if Rval == False:
        # Plot R^2 value
        plt.text(0.8 * maxxd + 0.2 * minxd, 0.8 * np.max(yd) + 0.2 * np.min(yd),
                 '$R^2 = %0.2f$' % Rsqr)
    else:
        # Return the R^2 value:
        return Rsqr
