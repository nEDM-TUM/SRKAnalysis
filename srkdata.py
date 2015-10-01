from subprocess import call
import paramiko
import sqlite3
import srkanalysis

__author__ = 'mjbales'

macro_dir = '/home/mjbales/work/nedm/macros/'
results_dir = '/home/mjbales/work/nedm/results/'
logs_dir = '/home/mjbales/work/nedm/logs/'
srk_path = '/home/mjbales/work/code/SRK/Release/bin/SRK'
database_path = '/home/mjbales/work/nedm/analysis/nedmAnalysis.sqlite'
database_runlog_table_name = 'RunLog'
optima_results_dir = results_dir
optima_address="optimal.universe-cluster.de"


# Default settings for macro files for SRK
def default_srk_settings():
    return {
        'RecordAllSteps': 0,
        'UseAltStepping': 0,
        'ConstStepper': 0,
        'Use2D': 0,
        'ManualTracking': 0,
        'B0FieldStrength': 0.000001,
        'E0FieldStrength': 10000000,
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
        'DipoleDirection': '0 0 1'
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
    rid_str = "".join([str(x)+'_' for x in run_ids])[:-1]
    macro_file_path = macro_dir + 'RID' + rid_str + '.mac'
    f = open(macro_file_path, 'w')

    first = True
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
        elif run_settings['RunType'] == 'parOnly':
            f.write('setParallelFields 1'+'\n')
            f.write('setResultsFilePath ' + results_dir + "Results_RID" + str(run_id) + "_P.root"+'\n')
            f.write('trackSpins ' + str(run_settings['NumTracksPer']))
        elif run_settings['RunType'] == 'antiOnly':
            f.write('setParallelFields 0'+'\n')
            f.write('setResultsFilePath ' + results_dir + "Results_RID" + str(run_id) + "_A.root"+'\n')
            f.write('trackSpins ' + str(run_settings['NumTracksPer']))

    f.close()
    print(macro_file_path + " created.\n")


def make_macro(run_id, srk_settings, run_settings):
    macro_file_path = macro_dir + 'RID' + str(run_id) + '.mac'
    f = open(macro_file_path, 'w')

    f.write('#' + str(run_settings) + '\n')
    f.write('setRunID RID' + str(run_id) + '\n')

    for setting in srk_settings.keys():
        f.write('set' + setting + ' ' + str(srk_settings[setting]) + '\n')

    if run_settings['RunType'] == 'deltaOmega':
        f.write('trackSpinsDeltaOmega ' + str(run_settings['NumTracksPer']))
    elif run_settings['RunType'] == 'parOnly':
        f.write('setParallelFields 1'+'\n')
        f.write('setResultsFilePath ' + results_dir + "Results_RID" + str(run_id) + "_P.root"+'\n')
        f.write('trackSpins ' + str(run_settings['NumTracksPer']))
    elif run_settings['RunType'] == 'antiOnly':
        f.write('setParallelFields 0'+'\n')
        f.write('setResultsFilePath ' + results_dir + "Results_RID" + str(run_id) + "_A.root"+'\n')
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

    # Connect to DB
    db_connection = sqlite3.connect(database_path)
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
    insert_string = 'INSERT INTO ' + database_runlog_table_name + '(' + column_string \
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

    if len(values_dict) <= 0:
        print "Update database command has no values, nothing updated"
        return

    # Connect to DB
    db_connection = sqlite3.connect(database_path)
    db_cursor = db_connection.cursor()

    # Must gather column names and their values
    value_tuple = ()
    update_string = 'UPDATE '+database_runlog_table_name + " SET "
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

    database_was_open = True
    if db_connection is None:
        # Open DB connection
        database_was_open = False
        db_connection = sqlite3.connect(database_path)

    db_cursor = db_connection.cursor()

    where_str =' WHERE'
    for x in run_ids[:-1]:
        where_str += ' Run =' + str(x) + ' OR '
    where_str += ' Run =' + str(run_ids[-1])

    select_str = 'SELECT ' + columns_str + ' FROM ' + database_runlog_table_name+where_str
    db_cursor.execute(select_str)
    values_from_select = db_cursor.fetchall()

    if not database_was_open:
        db_connection.commit()
        db_connection.close()

    return values_from_select


def get_settings_from_database(run_id, db_connection=None):

    # Open DB connection
    db_connection = sqlite3.connect(database_path)
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
    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(optima_address, username="mjbales")
    ssh_stdin, ssh_stdout, ssh_stderr = ssh.exec_command(command)
    print('$OPTIMA stdout: ' + str(ssh_stdout.readlines()))
    print('$OPTIMA stderr: ' + str(ssh_stderr.readlines()))
    ssh.close()


def run_macro_optima(rid_numbers):
    sync_macros_to_optima()
    command = '. "/opt/software/root/root_v5.34.21/bin/thisroot.sh"; '

    for i in rid_numbers:
        command += 'nohup /home/mjbales/SRK/build/bin/SRK ' + macro_dir + 'RID' + str(
            i) + '.mac &> ' + logs_dir + 'logRID' + str(i) + '.txt&'
        command += '; '
    command = command[:-2]  # remove last semicolon and space

    run_command_optima(command)

def run_macro_mult_laptop(rid_numbers):
    rid_str = "".join([str(x)+'_' for x in rid_numbers])[:-1]
    run_macro_laptop(rid_str)

def run_macro_laptop(rid_number):
    command = 'nohup ' + srk_path + ' ' + macro_dir + 'RID' + str(rid_number) + '.mac'
    command += ' > ' + logs_dir + 'logRID' + str(rid_number) + '.txt&'
    print command

    call(command, shell=True)


def run_on_optima(srk_settings, run_settings):
    """

    :rtype : int
    """

    run_id = make_macro_and_add_to_database(srk_settings, run_settings)
    run_macro_optima([run_id])
    return run_id


def fix_dipole_positions_in_table(first, last):

    db_connection = sqlite3.connect(database_path)
    db_cursor = db_connection.cursor()
    where_str = ' WHERE Run >= ' + str(first) + ' AND Run <= ' + str(last)
    select_command = 'SELECT DipolePositionBelowChamber FROM ' + database_runlog_table_name + where_str
    db_cursor.execute(select_command, ())
    position_below = db_cursor.fetchall()

    dipole_positions = []
    for i in position_below:
        dipole_positions += [('0. 0. '+str(i[0]),)]

    update_command = 'UPDATE ' + database_runlog_table_name + ' SET DipolePosition=?' + where_str+';'
    db_cursor.executemany(update_command,dipole_positions)

    db_connection.commit()
    db_connection.close()


def execute_runlog_command(command, value_tuple):

    db_connection = sqlite3.connect(database_path)
    db_cursor = db_connection.cursor()

    db_cursor.execute(command, value_tuple)

    db_connection.commit()
    db_connection.close()


def prefix_dict_keys(inp, prefix):
    out={}
    for x in inp.keys():
        out[prefix + x]=inp[x]
    return out


def calc_run_stats_to_database(run_id):
    all_stats = srkanalysis.calc_run_stats(run_id)
    where_str = "Run="+str(run_id)
    update_database(all_stats, where_str)


def calc_orientation_stats_to_database(run_id, is_parallel):
    stats = srkanalysis.calc_orientation_stats(run_id, is_parallel)
    where_str = "Run="+str(run_id)
    update_database(stats, where_str)


# presumes 2D array incoming for multiple lines
def get_plot_data_from_database(rids_for_many_graphs, column_x, column_y):

    db_connection = sqlite3.connect(database_path)

    x_out = []
    y_out = []
    for rids_one_graph in rids_for_many_graphs:
        single_line_data = get_data_for_rids_from_database(rids_one_graph, column_x+', '+column_y, db_connection)
        x, y = zip(*single_line_data)
        x_out.append(x)
        y_out.append(y)

    db_connection.close()

    return x_out, y_out
