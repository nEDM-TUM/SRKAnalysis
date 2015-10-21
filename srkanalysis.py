from ROOT import TFile, TTree, gDirectory, gROOT, gRandom, TH1D
import ROOT
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

    stats['SZDetProb'] = 0.
    for phi, theta in zip(phi_list, theta_list):
        stats['SZDetProb'] += calc_opposite_spin_prob(phi - stats['PhiMean'], theta)
    stats['SZDetProb'] /= stats['NumEventsRun']

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


def calc_delta_stats_same_tracks(run_id, use_wrapping=True):
    srk_sys = srkdata.SRKSystems()
    srk_sys.read_settings_file()

    hit_trees=[]
    root_files=[]
    for is_parallel in [True,False]:
        if is_parallel:
            letter = 'P'
            run_type = 'Par'
        else:
            letter = 'A'
            run_type = 'Anti'
        file_path = srk_sys.results_dir+"Results_RID"+str(run_id)+"_"+letter+".root"

        if not srkmisc.file_exits_and_not_zombie(file_path):
            print file_path + " doesn't exist or is zombie."
            return {}

        root_files.append(TFile(file_path, "READ"))
        hit_trees.append(gDirectory.Get('hitTree'))

    gROOT.cd()

    delta_phi_list = []
    for i in xrange(hit_trees[0].GetEntries()):
        hit_trees[0].GetEntry(i)
        hit_trees[1].GetEntry(i)
        delta_phi=hit_trees[0].phi-hit_trees[1].phi
        delta_phi_list.append(delta_phi)
    if use_wrapping:
        delta_phi_mean = srkmisc.reduce_periodics(delta_phi_list)
    else:
        delta_phi_mean = srkmisc.careful_mean(delta_phi_list)
    delta_phi_std = srkmisc.careful_std(delta_phi_list)
    root_files[0].Close()
    root_files[1].Close()
    return [delta_phi_mean, delta_phi_std]


def calc_run_stats(run_id):
    srk_settings, run_settings = srkdata.get_settings_from_database(run_id)
    p_stats = calc_orientation_stats(run_id, True)
    a_stats = calc_orientation_stats(run_id, False)

    if len(p_stats) > 0 or len(a_stats) > 0:
        p_stats['DipolePositionBelowChamber'] = get_dist_bottom_from_pos(srk_settings['DipolePosition'],
                                                                         srk_settings['ChamberHeight'])
    if len(p_stats) == 0 or len(a_stats) == 0:
        return srkdata.merge_dicts(p_stats, a_stats)

    run_stats = srkdata.default_delta_omega_stats()

    if run_settings['RunType'] == 'deltaOmega':
        # ufloat - floats with uncertainty
        p_phase = ufloat(p_stats['Par_PhiMean'], p_stats['Par_PhiError'])
        a_phase = ufloat(a_stats['Anti_PhiMean'], a_stats['Anti_PhiError'])

        delta_phase = p_phase - a_phase
    elif run_settings['RunType'] == 'deltaOmegaSame':
        dp = calc_delta_stats_same_tracks(run_id)
        delta_phase = ufloat(dp[0], dp[1] / run_settings['NumTracksPer'])
    else:
        return srkdata.merge_dicts(p_stats, a_stats)

    print str(run_id) + ":"
    print "Delta Phase: " + str(delta_phase)

    delta_omega = delta_phase / srk_settings['TimeLimit']
    print "Delta Omega: " + str(delta_omega)

    if srk_settings['E0FieldStrength'] == 0.:
        false_edm = ufloat(0., 0.)
    else:
        false_edm = calc_false_edm(delta_omega, srk_settings['E0FieldStrength'])
    print "False EDM: " + str(false_edm)

    run_stats['DeltaPhase'] = delta_phase.nominal_value
    run_stats['DeltaPhaseError'] = delta_phase.std_dev
    run_stats['DeltaOmega'] = delta_omega.nominal_value
    run_stats['DeltaOmegaError'] = delta_omega.std_dev
    run_stats['FalseEDM'] = false_edm.nominal_value
    run_stats['FalseEDMError'] = false_edm.std_dev

    pos = [float(x) for x in srk_settings['DipolePosition'].split(' ')]  # Splits up space separates position list
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


def calc_centered_rho_b_sub_rho(dip_str, radius, height, dist):
    return ((2. * dip_str) / (radius * radius * height)) * (
        2. * height + ((radius * radius + 2. * dist * dist) / math.sqrt(radius * radius + dist * dist)) - (
            (radius * radius + 2. * pow(dist + height, 2)) / math.sqrt(radius * radius + pow(dist + height, 2))))


def calc_centered_db_dz(dip_str, radius, height, dist):
    return ((2. * dip_str) / height) * (
        pow(pow(dist + height, 2) + radius * radius, -1.5) - pow(dist * dist + radius * radius, -1.5))


def calc_e_plus_one(dip_str, radius, height, dist):
    return -(4. / (radius * radius)) * (calc_centered_rho_b_sub_rho(dip_str, radius, height, dist)
        / calc_centered_db_dz(dip_str, radius, height, dist))


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

    false_edm = -(hbar * gyro * gyro / (2 * cspeed * cspeed)) * calc_centered_rho_b_sub_rho(dip_str, radius, height, dist) * 100

    out['PRPrediction'] = false_edm
    if srk_settings['E0FieldStrength'] == 0.:
        out['PRPredictionDeltaOmega'] = 0.
    else:
        out['PRPredictionDeltaOmega'] = false_edm / (100. * hbar / (4. * srk_settings['E0FieldStrength']))
    out['PRPredictionDeltaPhase'] = out['PRPredictionDeltaOmega']*srk_settings['TimeLimit']
    return out


def calc_dipole_b_field(dipole_str,pos_vec,dipole_vec=(0., 0., 1.)):
    r = math.sqrt(pos_vec[0] * pos_vec[0] + pos_vec[1] * pos_vec[1] + pos_vec[2] * pos_vec[2])
    r3inv = 1. / (r * r * r)
    r5inv = r3inv / (r * r)
    m_dot_r = 3. * r5inv * (dipole_vec[0] * pos_vec[0] + dipole_vec[1] * pos_vec[1] + dipole_vec[2] * pos_vec[2])
    b_field = [0., 0., 0.]
    b_field[0] += dipole_str * (pos_vec[0] * m_dot_r - dipole_vec[0] * r3inv)
    b_field[1] += dipole_str * (pos_vec[1] * m_dot_r - dipole_vec[1] * r3inv)
    b_field[2] += dipole_str * (pos_vec[2] * m_dot_r - dipole_vec[2] * r3inv)
    return b_field


def get_dipole_pos_from_dist(dist_from_bottom, chamber_height):
    return '0. 0. '+str(-0.5 * chamber_height - dist_from_bottom)

1
def get_dist_bottom_from_pos(dip_pos, chamber_height):
    return -0.5 * chamber_height + float(dip_pos.split(' ')[2])


# Presumes centered dipole for now
def get_dipole_str_to_match_field(dist_from_bottom, normalize_val, normalize_type):

    if normalize_type == "MaxBFieldCentered":
        return 0.5 * normalize_val * dist_from_bottom * dist_from_bottom * dist_from_bottom
    else:
        print "Normalize type not recognized"
        return None


def calc_mean_vel_from_Omega(Omega, omega_0, chamber_radius):
    omega_r = Omega * omega_0
    return abs(omega_r*chamber_radius)


def calc_Omega(run_id):
    srk_settings, run_settings = srkdata.get_settings_from_database(run_id)

    omega_0 = srk_settings['B0FieldStrength']*srk_settings['GyromagneticRatio']
    omega_r = srk_settings['MeanVel']/srk_settings['ChamberRadius']
    return omega_r/omega_0


# Returns value in e cm
def calc_false_edm(delta_omega, e_field):
    return delta_omega * (100. * 6.58211928E-016 / (4 * e_field))


# Presumes gaussian
def convert_std_dev_to_false_edm_measurement_error(std_dev, e_field, meas_time, num_particles):
    delta_omega_error=(std_dev/meas_time)/math.sqrt(num_particles)
    return math.sqrt(2)*abs(calc_false_edm(delta_omega_error,e_field)) # sqrt 2 due to both par and anti par


# Using phi and theta delta from central frequency
def calc_opposite_spin_prob(phi, theta):
    cos_phi = math.cos(phi)
    cos_theta = math.cos(theta)
    return 0.5 * (1. - cos_phi * cos_theta)


def test_kurtosis(num_test):
    data = []
    for i in xrange(num_test):
        data.append(gRandom.Gaus())
    return kurtosis(data)


def make_phi_hist_with_noise(rid, is_parallel, hist_dim, noise_stdev, normalize):
    hist = TH1D("blurredHist"+str(rid),"blurredHist"+str(rid), hist_dim[0],hist_dim[1],hist_dim[2])
    srk_sys = srkdata.SRKSystems()
    srk_sys.read_settings_file()

    if is_parallel:
        letter = 'P'
    else:
        letter = 'A'
    file_path = srkdata.SRKSystems.results_dir+"Results_RID"+str(rid)+"_"+letter+".root"

    f = ROOT.TFile.Open(file_path)
    phi_list=[]
    for event in f.hitTree:
        phi_list.append(gRandom.Gaus(event.phi, noise_stdev))

    mean = srkmisc.reduce_periodics(phi_list)
    stdev=srkmisc.careful_std(phi_list)
    for x in phi_list:
        if normalize:
            hist.Fill((x-mean)/stdev)
        else:
            hist.Fill(x)

    f.Close()
    ROOT.SetOwnership(hist, True)
    return hist
