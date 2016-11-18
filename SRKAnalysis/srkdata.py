from subprocess import call
import paramiko
import sqlite3
import srkanalysis
import srkmisc
import srkglobal
from ROOT import gRandom, gDirectory, TList, TFile, TNamed, TTree

__author__ = "Matthew Bales"
__credits__ = ["Matthew Bales"]
__license__ = "GPL"
__maintainer__ = "Matthew Bales"
__email__ = "matthew.bales@gmail.com"

gRandom.SetSeed(0)


def default_srk_settings():
    """Returns default dictionary for SRK settings.

            These correspond to SRK macro commands in the form: set<key> <value>"""
    return {
        'RecordAllSteps': 0,
        'UseAltStepping': 0,
        'ConstStepper': 0,
        'InitialStepSize': 0.01,
        'Use2D': 0,
        'AdditionalRandomVelZ': 0.,
        'ManualTracking': 0,
        'B0FieldStrength': 0.000001,
        'E0FieldStrength': 1000000,
        'E0FieldDirection': '0 0 1',
        'B0FieldDirection': '0 0 1',
        'BGradFieldStrength': 0,
        'EGradFieldStrength': 0,
        'DipoleFieldStrength': 0,
        'ChamberRadius': 0.235,
        'ChamberHeight': 0.12,
        'MeanVel': 193,
        'GyromagneticRatio': -48457883.9927,
        'TimeLimit': 100,
        'DiffuseReflectionProb': 1.0,
        'PhiStart': 0.,
        'ThetaStart': 0.,
        'ReflectionLimit': 9999999,
        'TrackFilePath': '!dynamic',
        'Pos': '0 0 0',
        'Vel': '193 0 0',
        'DipolePosition': '0 0 0',
        'DipoleDirection': '0 0 1',
        'EPSAbs': 1e-7,
        'EPSRel': 1e-7,
        'Mass': 3.30e-25,
        'MeanFreePath': -1,
        'VelProfHistPath': '',
        'RandomSeed': 0,
        'DepolAtWallProb': 0,
        'ChamberRotation': '0 0 0',
        'PeriodicStopTime': 9999999,
    }


def default_file_stats():
    """Returns default dictionary for SRK results file."""

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
    """Returns default dictionary for results of a parallel minus anti-parallel analysis from simulation."""
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


def default_run_settings():
    """Returns default dictionary for summary of applicable information attributed to one run of SRK"""
    return {
        'Title': 'DefaultTitle',
        'SRKVersion': '',
        'Date': '',
        'RunType': 'deltaOmega',
        'NumTracksPer': 10000,
    }


def merge_dicts(*dict_args):
    """Merges multiple dictionaries together."""
    result = {}
    for dictionary in dict_args:
        result.update(dictionary)
    return result


def make_macro(run_id, srk_settings, run_settings):
    """Creates macro file for run with provided settings."""

    macro_file_path = srkglobal.macro_dir + 'RID' + str(run_id) + '.mac'
    macro_file = open(macro_file_path, 'w')
    macro_file.write('setDefaultResultsDir ' + srkglobal.results_dir + '\n')
    write_macro_commands_to_file(macro_file, run_id, srk_settings, run_settings)

    macro_file.close()
    print(macro_file_path + " created.\n")


def write_macro_commands_to_file(macro_file, run_id, srk_settings, run_settings):
    """Writes macro commands for run with provided settings to already opened text macrofile."""

    macro_file.write('#' + str(run_settings) + '\n')
    macro_file.write('setRunID RID' + str(run_id) + '\n')

    for setting in srk_settings.keys():
        macro_file.write('set' + setting + ' ' + str(srk_settings[setting]) + '\n')

    if run_settings['RunType'] == 'deltaOmega':
        macro_file.write('trackSpinsDeltaOmega ' + str(run_settings['NumTracksPer']))
    elif run_settings['RunType'] == 'deltaOmegaSame':
        macro_file.write('setRandomSeed ' + str(gRandom.Integer(1000000)) + '\n')
        macro_file.write('trackSpinsDeltaOmega ' + str(run_settings['NumTracksPer']))
    elif run_settings['RunType'] == 'parOnly':
        macro_file.write('setParallelFields 1' + '\n')
        macro_file.write('setResultsFilePath ' + srkglobal.results_dir + "Results_RID" + str(run_id) + "_P.root" + '\n')
        macro_file.write('trackSpins ' + str(run_settings['NumTracksPer']))
    elif run_settings['RunType'] == 'antiOnly':
        macro_file.write('setParallelFields 0' + '\n')
        macro_file.write('setResultsFilePath ' + srkglobal.results_dir + "Results_RID" + str(run_id) + "_A.root" + '\n')
        macro_file.write('trackSpins ' + str(run_settings['NumTracksPer']))


def get_last_primary_key_in_database(db_connection=None):
    """Return the last primary key in the database."""
    database_was_open = True
    if db_connection is None:
        # Open DB connection
        database_was_open = False
        db_connection = sqlite3.connect(srkglobal.database_path)

    sql_string = "SELECT rowid FROM runlog ORDER BY rowid DESC LIMIT 1;"

    db_cursor = db_connection.cursor()
    db_cursor.execute(sql_string)
    last_rid = db_cursor.fetchall()[0][0]

    if not database_was_open:
        db_connection.commit()
        db_connection.close()

    return last_rid


def make_macro_from_database(run_id):
    """Makes a macro file from settings from the database"""
    srk_settings, run_settings = get_settings_from_database(run_id)
    make_macro(run_id, srk_settings, run_settings)


def make_macro_mult_from_database(run_ids):
    """Creates single macro file for multiple runs with settings from database."""
    rid_str = str(run_ids[0]) + "_thru_" + str(run_ids[-1])
    macro_file_path = srkglobal.macro_dir + 'RID' + rid_str + '.mac'
    macro_file = open(macro_file_path, 'w')

    macro_file.write('setDefaultResultsDir ' + srkglobal.results_dir + '\n')

    first = True

    for run_id in run_ids:
        srk_settings, run_settings = get_settings_from_database(run_id)

        if not first:
            macro_file.write('\n')
        else:
            first = False
            write_macro_commands_to_file(macro_file, run_id, srk_settings, run_settings)

    macro_file.close()
    print(macro_file_path + " created.\n")


def delete_from_database(run_id):
    """"Deletes an entry from the database"""

    # Connect to DB
    db_connection = sqlite3.connect(srkglobal.database_path)
    db_cursor = db_connection.cursor()

    # Insert into table
    command_string = 'DELETE FROM ' + srkglobal.database_runlog_table_name + ' WHERE Run=' + run_id
    db_cursor.execute(command_string)
    print('Delete Command String: ' + command_string + '\n')

    db_connection.commit()
    db_connection.close()


def add_to_database(values_dict):
    """Adds new entry to database based on dictionary"""

    # Connect to DB
    db_connection = sqlite3.connect(srkglobal.database_path)
    db_cursor = db_connection.cursor()

    # Last entry + 1 is new runid
    run_id = get_last_primary_key_in_database(db_connection) + 1
    values_dict["Run"] = run_id

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
    insert_string = 'INSERT INTO ' + srkglobal.database_runlog_table_name + '(' + column_string \
                    + ') Values (' + question_mark_string + ')'
    db_cursor.execute(insert_string, value_tuple)
    print('Insert String: ' + insert_string + '\n')
    print('Values: ')
    print(value_tuple)

    db_connection.commit()
    db_connection.close()

    return run_id


def update_database(values_dict, where_str):
    """Updates dictionary based on dictionary and SQL WHERE string."""

    if len(values_dict) <= 0:
        print "Update database command has no values, nothing updated"
        return

    # Connect to DB
    db_connection = sqlite3.connect(srkglobal.database_path)
    db_cursor = db_connection.cursor()

    # Must gather column names and their values
    value_tuple = ()
    update_string = 'UPDATE ' + srkglobal.database_runlog_table_name + " SET "
    for x in values_dict.keys():
        update_string += x + "=?, "
        value_tuple += (values_dict[x],)
    update_string = update_string[:-2]  # remove last comma
    update_string += "WHERE " + where_str
    print('Update String: ' + update_string + '\n')
    print('Values: ')
    print(value_tuple)
    # Update table
    db_cursor.execute(update_string, value_tuple)

    db_connection.commit()
    db_connection.close()


def get_data_for_rids_from_database(run_ids, columns_str, db_connection=None):
    """Get dictionary data for list of run_ids for particular columns."""

    database_was_open = True
    if db_connection is None:
        # Open DB connection
        database_was_open = False
        db_connection = sqlite3.connect(srkglobal.database_path)

    db_cursor = db_connection.cursor()

    values_from_select = []
    for x in run_ids:
        where_str = ' WHERE Run =' + str(x) + ' '
        select_str = 'SELECT ' + columns_str + ' FROM ' + srkglobal.database_runlog_table_name + where_str
        db_cursor.execute(select_str)
        values_from_select.append(db_cursor.fetchall()[0])

    if not database_was_open:
        db_connection.commit()
        db_connection.close()

    return values_from_select


def get_settings_from_database(run_id, db_connection=None):
    """Returns srk_settings and run_settings from database."""

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
        srk_settings_out[i] = all_settings[i]

    for i in run_settings_out:
        run_settings_out[i] = all_settings[i]

    return srk_settings_out, run_settings_out


def make_macro_and_add_to_database(srk_settings, run_settings):
    """Makes macro and adds it to database."""
    run_id = add_to_database(merge_dicts(srk_settings, run_settings))
    make_macro(run_id, srk_settings, run_settings)
    return run_id


def sync_macros_to_optima():
    """Syncs macros from local to optima using a shell script."""
    call(['bash', '/home/mjbales/work/nedm/scripts/syncMacrosToOptima.sh'])


def sync_results_from_optima():
    """Syncs result files from optima."""
    call(['bash', '/home/mjbales/work/nedm/scripts/syncResultsFromOptima.sh'])


def run_command_optima(command):
    """Runs a remote command on optima."""

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(srkglobal.optima_address, username="mjbales")
    ssh_std_in, ssh_std_out, ssh_std_err = ssh.exec_command(command)
    print('$OPTIMA stdout: ' + str(ssh_std_out.readlines()))
    print('$OPTIMA stderr: ' + str(ssh_std_err.readlines()))
    ssh.close()


def run_mult_macro_optima(run_ids):
    """Runs multiple rid mode macros on optima."""
    rid_str = str(run_ids[0]) + "_thru_" + str(run_ids[-1])
    run_macro_optima(rid_str)


def run_macro_optima(rid_number):
    """Runs a single rid on optima"""

    sync_macros_to_optima()
    command = '. "/opt/software/root/root_v5.34.21/bin/thisroot.sh"; '

    command += 'nohup ' + srkglobal.srk_path + ' ' + srkglobal.macro_dir + 'RID' + str(
        rid_number) + '.mac &> ' + srkglobal.logs_dir + 'logRID' + str(rid_number) + '.txt&'

    run_command_optima(command)


def run_mult_macro_local(run_ids):
    """Runs multiple rid mode macros on the local machine."""
    rid_str = str(run_ids[0]) + "_thru_" + str(run_ids[-1])
    run_macro_local(rid_str)


def run_macro_local(rid_number, wait=False):
    """Runs a single rid on the local machine"""

    command = ''
    if srkglobal.os == 'Linux':
        if not wait:
            command += 'nohup nice -10 '
        command += srkglobal.srk_path + ' ' + srkglobal.macro_dir + 'RID' + str(rid_number) + '.mac'
        command += ' > ' + srkglobal.logs_dir + 'logRID' + str(rid_number) + '.txt'
        if not wait:
            command += '&'
    elif srkglobal.os == 'Windows':
        if not wait:
            command += 'start cmd /c '
        command += srkglobal.srk_path + ' ' + srkglobal.macro_dir + 'RID' + str(rid_number) + '.mac'
        command += ' ^> ' + srkglobal.logs_dir + 'logRID' + str(rid_number) + '.txt'
    else:
        print "Operating system not recognized."
        return

    print command

    call(command, shell=True)


def run_on_optima(srk_settings, run_settings):
    """Makes a macro, adds it to the database, and runs it on optima."""

    run_id = make_macro_and_add_to_database(srk_settings, run_settings)
    run_macro_optima(run_id)
    return run_id


def execute_SQL_database_command(command, value_tuple):
    """Executes a database command with no return."""
    db_connection = sqlite3.connect(srkglobal.database_path)
    db_cursor = db_connection.cursor()

    db_cursor.execute(command, value_tuple)

    db_connection.commit()
    db_connection.close()


def prefix_dict_keys(inp, prefix):
    """Returns a new dictionary with all keys prefixed with a string."""
    out = {}
    for x in inp.keys():
        out[prefix + x] = inp[x]
    return out


def calc_run_stats_to_database(run_id):
    """Calculates all the run statistics and summary data and updates the database."""
    all_stats = srkanalysis.calc_run_stats(run_id)
    where_str = "Run=" + str(run_id)
    update_database(all_stats, where_str)


def calc_orientation_stats_to_database(run_id, is_parallel):
    """Calculates all the statistics related to a particular run and updates the database."""
    stats = srkanalysis.calc_orientation_stats(run_id, is_parallel)
    where_str = "Run=" + str(run_id)
    update_database(stats, where_str)


# presumes 2D array incoming for multiple lines
def get_plot_data_from_database(rids_for_many_graphs, column_x, column_y):
    """Takes a 2D array of RIDs that represent data points x lines and outputs specified columns of data for x and y."""
    db_connection = sqlite3.connect(srkglobal.database_path)

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
    """Takes a 2D array of RIDs that represent data points x lines and outputs specified columns"""
    db_connection = sqlite3.connect(srkglobal.database_path)

    columns_string = [j + ',' for j in columns]
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
    """Makes macros for particular plot from Steyerl et. al"""

    Omega_range = srkmisc.even_sample_over_log(start_Omega, end_Omega, num_Omega)
    rid_list = []
    for i in xrange(num_Omega):
        srk_settings['MeanVel'] = srkanalysis.calc_mean_vel_from_Omega(
            Omega_range[i], srk_settings['B0FieldStrength'] * srk_settings['GyromagneticRatio'],
            srk_settings['ChamberRadius'])
        if approx_fixed_reflections > 0.:
            srk_settings['TimeLimit'] = approx_fixed_reflections * 0.75 / abs(srk_settings['MeanVel'])
        if srk_settings['TrackFilePath'] != '!dynamic':
            srk_settings['TrackFilePath'] = srkglobal.tracks_dir + get_track_file_name(i, srk_settings)
        rid_list += [add_to_database(merge_dicts(srk_settings, run_settings))]

    make_macro_mult_from_database(rid_list)

    return rid_list


def make_track_file(num_tracks, srk_settings):
    """Makes a track file locally based on settings."""
    make_macro("makeTracks", srk_settings, {"NumTracksPer": num_tracks, "RunType": "makeTracks"})
    print "Making" + srk_settings['TrackFilePath']
    run_macro_local("makeTracks", True)


def make_tracks_for_steyerl(num_tracks, srk_settings, start_Omega, end_Omega, num_Omega, special_title=""):
    """Makes a track file locally based on settings for Omega ranges i.e. Steyerl et. al"""

    Omega_range = srkmisc.even_sample_over_log(start_Omega, end_Omega, num_Omega)
    for i in xrange(num_Omega):
        srk_settings['MeanVel'] = srkanalysis.calc_mean_vel_from_Omega(
            Omega_range[i], srk_settings['B0FieldStrength'] * srk_settings['GyromagneticRatio'],
            srk_settings['ChamberRadius'])
        srk_settings['TrackFilePath'] = srkglobal.tracks_dir + get_track_file_name(i, srk_settings, special_title)

        make_track_file(num_tracks, srk_settings)


def get_track_file_name(id_num, srk_settings, special_title=""):
    """Outputs track file name in standard format based on settings."""
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
