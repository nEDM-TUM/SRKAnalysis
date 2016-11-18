__author__ = "Matthew Bales"
__credits__ = ["Matthew Bales"]
__license__ = "GPL"
__maintainer__ = "Matthew Bales"
__email__ = "matthew.bales@gmail.com"

# Global settings
database_runlog_table_name = "RunLog"

# Computer specific paths and settings
computer = None  # Computer alias
macro_dir = None  # Where SRK macros are stored
graphs_dir = None  # Where graphs are stored
hists_dir = None  # Where histograms or txt data are stored
results_dir = None  # Where SRK root files are stored
logs_dir = None  # Where SRK log files are stored
tracks_dir = None  # Where tracks are stored
srk_path = None  # Where SRK executable binary is stored
database_path = None  # Where sqlite database is stored
os = None  # What OS the computer uses
optima_address="optimal.universe-cluster.de" # Optima address


def set_computer(inp_computer):
    """Sets universal settings and paths based on which computer is selected."""
    global macro_dir
    global results_dir
    global logs_dir
    global graphs_dir
    global hists_dir
    global srk_path
    global tracks_dir
    global database_path
    global os
    global computer
    computer = inp_computer
    if computer == 'work_laptop':
        macro_dir = '/home/mjbales/work/nedm/macros/'
        results_dir = '/media/mjbales/data/nedm/results/'
        logs_dir = '/home/mjbales/work/nedm/logs/'
        graphs_dir = '/home/mjbales/work/nedm/graphs/'
        hists_dir = '/home/mjbales/work/nedm/hists/'
        srk_path = '/home/mjbales/work/code/SRK/Release/bin/SRK'
        tracks_dir = '/media/mjbales/data/nedm/tracks/'
        database_path = '/home/mjbales/work/code/SRKAnalysis/nedmAnalysis.sqlite'
        os = 'Linux'
    elif computer == 'home_desktop':
        macro_dir = 'D:\\work\\nedm\\macros\\'
        results_dir = 'D:\\work\\nedm\\results\\'
        graphs_dir = 'D:\\work\\nedm\\graphs\\'
        hists_dir = 'D:\\work\\nedm\\hists\\'
        logs_dir = 'D:\\work\\nedm\\logs\\'
        srk_path = 'D:\\work\\code\\SRK\\Release\\SRK.exe'
        tracks_dir = 'D:\\work\\nedm\\tracks\\'
        database_path = 'D:\\work\\code\\SRKAnalysis\\nedmAnalysis.sqlite'
        os = 'Windows'
    elif computer == 'optima':
        macro_dir = '/home/mjbales/work/nedm/macros/'
        results_dir = '/home/mjbales/work/nedm/results/'
        logs_dir = '/home/mjbales/work/nedm/logs/'
        graphs_dir = '/home/mjbales/work/nedm/graphs/'
        hists_dir = '/home/mjbales/work/nedm/hists/'
        srk_path = '/home/mjbales/SRK/build/SRK'
        tracks_dir = '/media/mjbales/data/nedm/tracks/'
        database_path = '/home/mjbales/work/code/SRKAnalysis/nedmAnalysis.sqlite'
        os = 'Linux'


