from ROOT import TFile, TTree, gDirectory, gROOT
import srkdata
import srkmisc
import math
from scipy import constants as const
from scipy.stats import kurtosis, skew
from uncertainties import ufloat
import numpy

__author__ = 'mjbales'


def calc_stats_for_results_file(file_path, use_wrapping = True):
    stats = srkdata.default_file_stats()

    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return {}

    root_file = TFile(file_path, "READ")
    hit_tree = gDirectory.Get('hitTree')
    gROOT.cd()
    stats['NumEventsRun'] = hit_tree.GetEntries()

    phi_list = []
    theta_list = []
    for i in xrange(stats['NumEventsRun']):
        hit_tree.GetEntry(i)
        phi_list.append(hit_tree.phi)
        theta_list.append(hit_tree.theta)

    root_file.Close()

    if use_wrapping:
        stats['PhiMean'] = srkmisc.reduce_periodics(phi_list)
        stats['ThetaMean'] = srkmisc.reduce_periodics(theta_list)
    else:
        stats['PhiMean'] = srkmisc.careful_mean(phi_list)
        stats['ThetaMean'] = srkmisc.careful_mean(theta_list)

    stats['PhiStDev'] = srkmisc.careful_std(phi_list)
    stats['ThetaStDev'] = srkmisc.careful_std(theta_list)

    stats['PhiError'] = stats['PhiStDev'] / math.sqrt(len(phi_list))
    stats['ThetaError'] = stats['ThetaStDev'] / math.sqrt(len(theta_list))

    stats['PhiKurtosis'] = kurtosis(phi_list)
    stats['ThetaKurtosis'] = kurtosis(phi_list)

    stats['PhiSkewness'] = skew(phi_list)
    stats['ThetaSkewness'] = skew(phi_list)

    percentile_lower, percentile_upper = numpy.percentile(phi_list, [16.5, 83.5])
    percentile_width = percentile_upper - percentile_lower
    stats['PhiPercentileWidth'] = percentile_width

    percentile_lower, percentile_upper = numpy.percentile(theta_list, [16.5, 83.5])
    percentile_width = percentile_upper - percentile_lower
    stats['ThetaPercentileWidth'] = percentile_width

    return stats


def calc_orientation_stats(run_id, is_parallel):

    if is_parallel:
        letter = 'P'
        run_type = 'Par'
    else:
        letter = 'A'
        run_type = 'Anti'
    file_path = srkdata.SRKSystems.results_dir+"Results_RID"+str(run_id)+"_"+letter+".root"

    stats = calc_stats_for_results_file(file_path)

    if len(stats) == 0:
        return {}

    stats = srkdata.prefix_dict_keys(stats, run_type+'_')

    srk_settings, run_settings = srkdata.get_settings_from_database(run_id)
    pr_stats = calc_dipole_predictions_pignol_and_rocia(srk_settings)

    return srkdata.merge_dicts(stats,pr_stats)


def calc_run_stats(run_id):

    srk_settings, run_settings = srkdata.get_settings_from_database(run_id)
    p_stats = calc_orientation_stats(run_id, True)
    a_stats = calc_orientation_stats(run_id, False)

    if len(p_stats) == 0 or len(a_stats) == 0:
        return {}

    run_stats = srkdata.default_delta_omega_stats()

    # ufloat - floats with uncertainty
    p_phase = ufloat(p_stats['Par_PhiMean'], p_stats['Par_PhiError'])
    a_phase = ufloat(a_stats['Anti_PhiMean'], a_stats['Anti_PhiError'])

    delta_phase = p_phase - a_phase
    print str(run_id)+":"
    print "Delta Phase: " + str(delta_phase)

    delta_omega = delta_phase / srk_settings['TimeLimit']
    print "Delta Omega: " + str(delta_omega)

    if srk_settings['E0FieldStrength'] == 0.:
        false_edm = ufloat(0., 0.)
    else:
        false_edm = delta_omega * (100. * 6.58211928E-016 / (4 * srk_settings['E0FieldStrength']))
    print "False EDM: " + str(false_edm)

    run_stats['DeltaPhase'] = delta_phase.nominal_value
    run_stats['DeltaPhaseError'] = delta_phase.std_dev
    run_stats['DeltaOmega'] = delta_omega.nominal_value
    run_stats['DeltaOmegaError'] = delta_omega.std_dev
    run_stats['FalseEDM'] = false_edm.nominal_value
    run_stats['FalseEDMError'] = false_edm.std_dev

    pos = [float(x) for x in srk_settings['DipolePosition'] .split(' ')]  # Splits up space separates position list
    run_stats['DipolePositionBelowChamber'] = pos[2] + srk_settings['ChamberHeight']
    run_stats['DipolePositionX'] = pos[0]

    pr_stats = calc_dipole_predictions_pignol_and_rocia(srk_settings)

    return srkdata.merge_dicts(run_stats, p_stats, a_stats, pr_stats)


def check_user_info_tree(run_id,post_fix):
    file_path=srkdata.SRKSystems.results_dir+"Results_RID"+str(run_id)+"_"+post_fix+".root"
    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return
    root_file = TFile(file_path, "READ")
    hit_tree = gDirectory.Get('hitTree')
    u=hit_tree.GetUserInfo()
    u.Print()
    root_file.Close()
    return


# From PHYSICAL REVIEW A 85, 042105 (2012)
# returns stats related to this
def calc_dipole_predictions_pignol_and_rocia(srk_settings):
    out = dict()

    dip_str = srk_settings['DipoleFieldStrength']

    if dip_str == 0:
        return out

    pos = [float(x) for x in srk_settings['DipolePosition'] .split(' ')]  # Splits up space separates position list
    radius = srk_settings['ChamberRadius']
    height = srk_settings['ChamberHeight']
    dist = -pos[2] - .5*height
    gyro = srk_settings['GyromagneticRatio']
    cspeed = 299792458
    hbar = 6.582E-016

    rho_b_sub_rho = ((2. * dip_str) / (radius * radius * height)) * (
        2. * height + ((radius * radius + 2. * dist * dist) / math.sqrt(radius * radius + dist * dist)) - (
        (radius * radius + 2. * pow(dist + height, 2)) / math.sqrt(radius * radius + pow(dist + height, 2))))

    false_edm = -(hbar * gyro * gyro / (2 * cspeed * cspeed)) * rho_b_sub_rho * 100

    # db_dz = ((2. * dip_str) / height) * (
    #          pow(pow(dist + height, 2) + radius * radius, -1.5) - pow(dist * dist + radius * radius, -1.5))
    # e_plus_one = -(4. / (radius * radius)) * (rho_b_sub_rho / db_dz)
    # print e_plus_one
    out['PRPrediction'] = false_edm
    if srk_settings['E0FieldStrength'] == 0.:
        out['PRPredictionDeltaOmega'] = 0.
    else:
        out['PRPredictionDeltaOmega'] = false_edm / (100. * hbar / (4. * srk_settings['E0FieldStrength']))
    out['PRPredictionDeltaPhase'] = out['PRPredictionDeltaOmega']*srk_settings['TimeLimit']
    return out
