from subprocess import call
import paramiko
import sqlite3
import srkanalysis
import srkmisc
from ROOT import gRandom

__author__ = 'mjbales'


class SRKSystems:
    macro_dir = '/home/mjbales/work/nedm/macros/'
    graphs_dir = '/home/mjbales/work/nedm/graphs/'
    hists_dir = '/home/mjbales/work/nedm/hists/'
    results_dir = '/home/mjbales/work/nedm/results/'
    logs_dir = '/home/mjbales/work/nedm/logs/'
    tracks_dir = '/data/nedm/tracks/'
    srk_path = '/home/mjbales/work/code/SRK/Release/bin/SRK'
    database_path = '/home/mjbales/work/code/SRKAnalysis/nedmAnalysis.sqlite'
    database_runlog_table_name = 'RunLog'
    optima_results_dir = results_dir
    optima_address="optimal.universe-cluster.de"
    settings_file_read= False
    computer = 'work_laptop'
    os = 'Linux'
    def __init__(self):
        self.read_settings_file()
        return

    def read_settings_file(self):
        if SRKSystems.settings_file_read:
            return
        f=open('settings.txt','r')
        for line in f:
            if line[0] != '#':
                command, value = line.split(' ')

                if command == 'setComputer':
                    SRKSystems.set_computer(self, value)
        f.close()
        SRKSystems.settings_file_read = True
        return

    def set_computer(self, value):

        SRKSystems.computer=value
        if SRKSystems.computer == 'work_laptop':
            SRKSystems.macro_dir = '/home/mjbales/work/nedm/macros/'
            SRKSystems.results_dir = '/home/mjbales/work/nedm/results/'
            SRKSystems.logs_dir = '/home/mjbales/work/nedm/logs/'
            SRKSystems.graphs_dir = '/home/mjbales/work/nedm/graphs/'
            SRKSystems.hists_dir = '/home/mjbales/work/nedm/hists/'
            SRKSystems.srk_path = '/home/mjbales/work/code/SRK/Release/bin/SRK'
            SRKSystems.tracks_dir = '/data/nedm/tracks/'
            SRKSystems.database_path = '/home/mjbales/work/code/SRKAnalysis/nedmAnalysis.sqlite'
            SRKSystems.os = 'Linux'
        elif SRKSystems.computer == 'home_desktop':
            SRKSystems.macro_dir = 'D:\\work\\nedm\\macros\\'
            SRKSystems.results_dir = 'D:\\work\\nedm\\results\\'
            SRKSystems.graphs_dir = 'D:\\work\\nedm\\graphs\\'
            SRKSystems.hists_dir = 'D:\\work\\nedm\\hists\\'
            SRKSystems.logs_dir = 'D:\\work\\nedm\\logs\\'
            SRKSystems.srk_path = 'D:\\work\\code\\SRK\\Release\\SRK.exe'
            SRKSystems.tracks_dir = 'D:\\work\\nedm\\tracks\\'
            SRKSystems.database_path = 'D:\\work\\code\\SRKAnalysis\\nedmAnalysis.sqlite'
            SRKSystems.os = 'Windows'


# Default settings for macro files for SRK
def default_srk_settings():
    return {
        'RecordAllSteps': 0,
        'UseAltStepping': 0,
        'ConstStepper': 0,
        'Use2D': 0,
        'AdditionalRandomVelZ': 0.,
        'ManualTracking': 0,
        'B0FieldStrength': 0.000001,
        'E0FieldStrength': 1000000,
        'BGradFieldStrength': 0,
        'DipoleFieldStrength': 0,
        'ChamberRadius': 0.235,
        'ChamberHeight': 0.12,
        'MeanVel': 193,
        'GyromagneticRatio': -48457883.9927,
        'TimeLimit': 100,
        'DiffuseReflectionProb': 1.0,
        'ReflectionLimit': 9999999,
        'TrackFilePath': '!dynamic',
        'Pos': '0 0 0',
        'Vel': '193 0 0',
        'DipolePosition': '0 0 0',
        'DipoleDirection': '0 0 1',
        'EPSAbs': 1e-7,
        'EPSRel': 1e-7
    }


def default_file_stats():
    return {
        'NumEventsRun': 0,

        'SZDetProb': 0.,

        'PhiMean': 0.,
        'PhiError': 0.,
        'PhiStDev': 0.,
        'PhiKurtosis': 0.,
        'PhiKurtosisError': 0.,
        'PhiSkewness': 0.,
        'PhiSkewnessError': 0.,
        'PhiPercentileWidth': 0.,
       # 'PhiTsallisPower': 0.,
      #  'PhiTsallisPowerError': 0.,

        'ThetaMean': 0.,
        'ThetaError': 0.,
        'ThetaStDev': 0.,
        'ThetaKurtosis': 0.,
        'ThetaKurtosisError': 0.,
        'ThetaSkewness': 0.,
        'ThetaSkewnessError': 0.,
        'ThetaPercentileWidth': 0.,
       # 'ThetaTsallisPower': 0.,
      #  'ThetaTsallisPowerError': 0.
    }


def default_delta_omega_stats():
    return {
        'DeltaPhase': 0.,
        'DeltaPhaseError': 0.,
        'DeltaOmega': 0.,
        'DeltaOmegaError': 0.,
        'FalseEDM': 0.,
        'FalseEDMError': 0.,
        'DipolePositionBelowChamber': 0,
        'DipolePositionX': 0
    }


# Default settings for macro files for SRK
def default_run_settings():
    return {
        'Title': 'DefaultTitle',
        'SRKVersion': '',
        'Date': '',
        'RunType': 'deltaOmega',
        'NumTracksPer': 10000,
    }


def merge_dicts(*dict_args):
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def make_macro_mult_from_database(run_ids):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    rid_str = str(run_ids[0])+"_thru_"+str(run_ids[-1])
    macro_file_path = SRKSystems.macro_dir + 'RID' + rid_str + '.mac'
    f = open(macro_file_path, 'w')

    f.write('setDefaultResultsDir '+SRKSystems.results_dir + '\n')

    first = True
    gRandom.SetSeed(0)

    for run_id in run_ids:
        srk_settings, run_settings = get_settings_from_database(run_id)

        if not first:
            f.write('\n')
        else:
            first = False
        f.write('#' + str(run_settings) + '\n')

        f.write('setRunID RID' + str(run_id) + '\n')

        for setting in srk_settings.keys():
            f.write('set' + setting + ' ' + str(srk_settings[setting]) + '\n')

        if run_settings['RunType'] == 'deltaOmega':
            f.write('trackSpinsDeltaOmega ' + str(run_settings['NumTracksPer']))
        elif run_settings['RunType'] == 'deltaOmegaSame':
            f.write('setRandomSeed ' + str(gRandom.Integer(1000000))+'\n')
            f.write('trackSpinsDeltaOmega ' + str(run_settings['NumTracksPer']))
        elif run_settings['RunType'] == 'parOnly':
            f.write('setParallelFields 1'+'\n')
            f.write('setResultsFilePath ' + SRKSystems.results_dir + "Results_RID" + str(run_id) + "_P.root"+'\n')
            f.write('trackSpins ' + str(run_settings['NumTracksPer']))
        elif run_settings['RunType'] == 'antiOnly':
            f.write('setParallelFields 0'+'\n')
            f.write('setResultsFilePath ' + SRKSystems.results_dir + "Results_RID" + str(run_id) + "_A.root"+'\n')
            f.write('trackSpins ' + str(run_settings['NumTracksPer']))

    f.close()
    print(macro_file_path + " created.\n")


def make_macro(run_id, srk_settings, run_settings):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    macro_file_path = SRKSystems.macro_dir + 'RID' + str(run_id) + '.mac'
    f = open(macro_file_path, 'w')

    f.write('#' + str(run_settings) + '\n')
    f.write('setRunID RID' + str(run_id) + '\n')
    f.write('setDefaultResultsDir '+SRKSystems.results_dir + '\n')

    for setting in srk_settings.keys():
        f.write('set' + setting + ' ' + str(srk_settings[setting]) + '\n')

    if run_settings['RunType'] == 'deltaOmega':
        f.write('trackSpinsDeltaOmega ' + str(run_settings['NumTracksPer']))
    elif run_settings['RunType'] == 'makeTracks':
        f.write('makeTracks '+str(run_settings['NumTracksPer']))
    elif run_settings['RunType'] == 'parOnly':
        f.write('setParallelFields 1'+'\n')
        f.write('setResultsFilePath ' + SRKSystems.results_dir + "Results_RID" + str(run_id) + "_P.root"+'\n')
        f.write('trackSpins ' + str(run_settings['NumTracksPer']))
    elif run_settings['RunType'] == 'antiOnly':
        f.write('setParallelFields 0'+'\n')
        f.write('setResultsFilePath ' + SRKSystems.results_dir + "Results_RID" + str(run_id) + "_A.root"+'\n')
        f.write('trackSpins ' + str(run_settings['NumTracksPer']))

    f.close()
    print(macro_file_path + " created.\n")


def make_macro_from_database(run_id):
    srk_settings, run_settings = get_settings_from_database(run_id)
    make_macro(run_id, srk_settings, run_settings)


def add_to_database(values_dict):
    """

    :rtype : int
    """
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()

    # Connect to DB
    db_connection = sqlite3.connect(SRKSystems.database_path)
    db_cursor = db_connection.cursor()

    # Must gather column names and their values
    column_string = ''
    value_tuple = ()
    question_mark_string = ''
    for i in values_dict.keys():
        column_string += i + ','
        question_mark_string += '?,'
        value_tuple += (values_dict[i],)
    column_string = column_string[:-1]  # remove last comma
    question_mark_string = question_mark_string[:-1]  # remove last comma

    # Insert into table
    insert_string = 'INSERT INTO ' + SRKSystems.database_runlog_table_name + '(' + column_string \
                  + ') Values (' + question_mark_string + ')'
    db_cursor.execute(insert_string, value_tuple)
    print('Insert String: '+insert_string+'\n')
    print('Values: ')
    print(value_tuple)

    # Last entry is the Run ID
    run_id=db_cursor.lastrowid

    db_connection.commit()
    db_connection.close()

    return run_id


def update_database(values_dict, where_str):
    """

    :rtype : int
    """
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    if len(values_dict) <= 0:
        print "Update database command has no values, nothing updated"
        return

    # Connect to DB
    db_connection = sqlite3.connect(SRKSystems.database_path)
    db_cursor = db_connection.cursor()

    # Must gather column names and their values
    value_tuple = ()
    update_string = 'UPDATE '+SRKSystems.database_runlog_table_name + " SET "
    for x in values_dict.keys():
        update_string += x + "=?, "
        value_tuple += (values_dict[x],)
    update_string = update_string[:-2]  # remove last comma
    update_string += "WHERE " + where_str
    print('Update String: '+update_string+'\n')
    print('Values: ')
    print(value_tuple)
    # Update table
    db_cursor.execute(update_string, value_tuple)

    db_connection.commit()
    db_connection.close()


def get_data_for_rids_from_database(run_ids, columns_str, db_connection=None):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    database_was_open = True
    if db_connection is None:
        # Open DB connection
        database_was_open = False
        db_connection = sqlite3.connect(SRKSystems.database_path)

    db_cursor = db_connection.cursor()

    # where_str =' WHERE'
    # for x in run_ids[:-1]:
    #     where_str += ' Run =' + str(x) + ' OR '
    # where_str += ' Run =' + str(run_ids[-1])
    #
    # select_str = 'SELECT ' + columns_str + ' FROM ' + SRKSystems.database_runlog_table_name+where_str
    # db_cursor.execute(select_str)
    # values_from_select = db_cursor.fetchall()
    values_from_select=[]
    where_str =' WHERE'
    for x in run_ids:
        where_str = ' WHERE Run =' + str(x) + ' '
        select_str = 'SELECT ' + columns_str + ' FROM ' + SRKSystems.database_runlog_table_name+where_str
        db_cursor.execute(select_str)
        values_from_select.append(db_cursor.fetchall()[0])

    if not database_was_open:
        db_connection.commit()
        db_connection.close()

    return values_from_select


def get_settings_from_database(run_id, db_connection=None):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    # Open DB connection
    db_connection = sqlite3.connect(SRKSystems.database_path)
    db_cursor = db_connection.cursor()

    # Must gather column names and their values
    all_settings = merge_dicts(default_run_settings(), default_srk_settings())
    columns_str = ''
    for i in all_settings.keys():
        columns_str += i + ','
    columns_str = columns_str[:-1]  # remove last comma

    values_from_select = get_data_for_rids_from_database([run_id, ], columns_str, db_connection)
    values_from_select = values_from_select[0]

    # Put into dictionary in the same order we got them
    all_settings = dict(zip(all_settings.keys(), values_from_select))

    # Transfer dicts to individual ones
    srk_settings_out = default_srk_settings()
    run_settings_out = default_run_settings()

    for i in srk_settings_out:
        srk_settings_out[i]=all_settings[i]

    for i in run_settings_out:
        run_settings_out[i]=all_settings[i]

    return srk_settings_out, run_settings_out


def make_macro_and_add_to_database(srk_settings, run_settings):
    """

    :rtype : int
    """
    run_id = add_to_database(merge_dicts(srk_settings, run_settings))
    make_macro(run_id, srk_settings, run_settings)
    return run_id


def sync_macros_to_optima():
    call(['bash', '/home/mjbales/work/nedm/scripts/syncMacrosToOptima.sh'])


def sync_results_to_optima():
    call(['bash', '/home/mjbales/work/nedm/scripts/syncResultsFromOptima.sh'])


def run_command_optima(command):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(SRKSystems.optima_address, username="mjbales")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    print('$OPTIMA stdout: ' + str(ssh_stdout.readlines()))
    print('$OPTIMA stderr: ' + str(ssh_stderr.readlines()))
    ssh.close()


def run_macro_optima(rid_numbers):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    sync_macros_to_optima()
    command = '. "/opt/software/root/root_v5.34.21/bin/thisroot.sh"; '

    for i in rid_numbers:
        command += 'nohup /home/mjbales/SRK/build/bin/SRK ' +SRKSystems.macro_dir + 'RID' + str(
            i) + '.mac &> ' + SRKSystems.logs_dir + 'logRID' + str(i) + '.txt&'
        command += '; '
    command = command[:-2]  # remove last semicolon and space

    run_command_optima(command)


def run_mult_macro_local(run_ids):
    rid_str = str(run_ids[0])+"_thru_"+str(run_ids[-1])
    run_macro_local(rid_str)


def run_macro_local(rid_number, wait=False):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()

    command = ''
    if srk_sys.os == 'Linux':
        if not wait:
            command += 'nohup '
        command += SRKSystems.srk_path + ' ' + SRKSystems.macro_dir + 'RID' + str(rid_number) + '.mac'
        command += ' > ' + SRKSystems.logs_dir + 'logRID' + str(rid_number) + '.txt'
        if not wait:
            command += '&'
    elif srk_sys.os == 'Windows':
        if not wait:
            command += 'start cmd /c '
        command += SRKSystems.srk_path + ' ' + SRKSystems.macro_dir + 'RID' + str(rid_number) + '.mac'
        command += ' ^> ' + SRKSystems.logs_dir + 'logRID' + str(rid_number) + '.txt'
    else:
        print "Operating system not recognized."
        return

    print command

    call(command, shell=True)


def run_on_optima(srk_settings, run_settings):
    """

    :rtype : int
    """

    run_id = make_macro_and_add_to_database(srk_settings, run_settings)
    run_macro_optima([run_id])
    return run_id

def execute_runlog_command(command, value_tuple):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    db_connection = sqlite3.connect(SRKSystems.database_path)
    db_cursor = db_connection.cursor()

    db_cursor.execute(command, value_tuple)

    db_connection.commit()
    db_connection.close()


def prefix_dict_keys(inp, prefix):
    out = {}
    for x in inp.keys():
        out[prefix + x] = inp[x]
    return out


def calc_run_stats_to_database(run_id):
    all_stats = srkanalysis.calc_run_stats(run_id)
    where_str = "Run=" + str(run_id)
    update_database(all_stats, where_str)


def calc_orientation_stats_to_database(run_id, is_parallel):
    stats = srkanalysis.calc_orientation_stats(run_id, is_parallel)
    where_str = "Run=" + str(run_id)
    update_database(stats, where_str)


# presumes 2D array incoming for multiple lines
def get_plot_data_from_database(rids_for_many_graphs, column_x, column_y):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    db_connection = sqlite3.connect(SRKSystems.database_path)

    x_out = []
    y_out = []
    for rids_one_graph in rids_for_many_graphs:
        single_line_data = get_data_for_rids_from_database(rids_one_graph, column_x + ', ' + column_y, db_connection)
        x, y = zip(*single_line_data)
        x_out.append(x)
        y_out.append(y)

    db_connection.close()

    return x_out, y_out

def get_plot_data_from_database_mult(rids_for_many_graphs, columns):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    db_connection = sqlite3.connect(SRKSystems.database_path)

    columns_string = [j+',' for j in columns]
    columns_string = ''.join(columns_string)[:-1]

    data_out = []
    for rids_one_graph in rids_for_many_graphs:
        single_line_data = get_data_for_rids_from_database(rids_one_graph, columns_string, db_connection)
        x = zip(*single_line_data)
        data_out.append(x)

    db_connection.close()

    return data_out


def make_macros_steyerl_and_add_to_database(srk_settings, run_settings, start_Omega, end_Omega, num_Omega,
                                            approx_fixed_reflections=0.):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()

    Omega_range = srkmisc.even_sample_over_log(start_Omega, end_Omega, num_Omega)
    rid_list = []
    for i in xrange(num_Omega):
        srk_settings['MeanVel'] = srkanalysis.calc_mean_vel_from_Omega(
            Omega_range[i], srk_settings['B0FieldStrength'] * srk_settings['GyromagneticRatio'],
            srk_settings['ChamberRadius'])
        if approx_fixed_reflections > 0.:
            srk_settings['TimeLimit'] = approx_fixed_reflections * 0.75 / abs(srk_settings['MeanVel'])
        if srk_settings['TrackFilePath'] != '!dynamic':
            srk_settings['TrackFilePath'] = srk_sys.tracks_dir + get_track_file_name(i, srk_settings)
        rid_list += [add_to_database(merge_dicts(srk_settings, run_settings))]


    make_macro_mult_from_database(rid_list)

    return rid_list


def make_track_file(num_tracks, srk_settings):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    make_macro("makeTracks", srk_settings, {"NumTracksPer": num_tracks, "RunType": "makeTracks"})
    print "Making" + srk_settings['TrackFilePath']
    run_macro_local("makeTracks", True)

def make_tracks_for_omega(num_tracks, srk_settings, start_Omega, end_Omega, num_Omega, special_title=""):
    srk_sys = SRKSystems()
    srk_sys.read_settings_file()
    Omega_range = srkmisc.even_sample_over_log(start_Omega, end_Omega, num_Omega)
    for i in xrange(num_Omega):
        srk_settings['MeanVel'] = srkanalysis.calc_mean_vel_from_Omega(
            Omega_range[i], srk_settings['B0FieldStrength'] * srk_settings['GyromagneticRatio'],
            srk_settings['ChamberRadius'])
        srk_settings['TrackFilePath'] = srk_sys.tracks_dir + get_track_file_name(i, srk_settings, special_title)

        make_track_file(num_tracks, srk_settings)



def get_track_file_name(id_num, srk_settings, special_title=""):
    name = "Tracks_"

    name += special_title

    if srk_settings['Use2D']:
        name += "2D_"
    else:
        name += "3D_"

    if srk_settings['DiffuseReflectionProb'] == 1.:
        name += "Diffuse_"
    elif srk_settings['DiffuseReflectionProb'] == 0.:
        name += "Specular_"
    else:
        name += "Diffuse" + "{:.0f}".format(srk_settings['DiffuseReflectionProb']) + "_"

    name += "{:.0f}".format(srk_settings['TimeLimit']) + "s_"

    name += "ID" + str(id_num)
    name += ".root"

    return name
