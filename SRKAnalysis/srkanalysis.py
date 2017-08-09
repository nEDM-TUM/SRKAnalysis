import csv
from ROOT import TFile, gDirectory, gROOT, gRandom, TH1D, TF1, TGeoTube, TVector3
import ROOT
import srkdata
import srkmisc
import srkglobal
import math
import array
from scipy.stats import kurtosis, skew
from uncertainties import ufloat
import numpy as np
import matplotlib.pyplot as plt

__author__ = "Matthew Bales"
__credits__ = ["Matthew Bales"]
__license__ = "GPL"
__maintainer__ = "Matthew Bales"
__email__ = "matthew.bales@gmail.com"


def calc_stats_for_results_file(file_path, runtype="nedm", use_wrapping=False):
    """Calculates summary stats for a SRK results ROOT file."""
    stats = srkdata.default_file_stats(runtype)

    # Check if file exists and is valid
    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return {}

    root_file = TFile(file_path, "READ")

    hit_tree = gDirectory.Get('hitTree')
    gROOT.cd()
    stats['NumEventsRun'] = hit_tree.GetEntries()

    # Get arrays for phi and theta from file
    phi_array = np.empty(hit_tree.GetEntries())
    theta_array = np.empty(hit_tree.GetEntries())
    for i in xrange(stats['NumEventsRun']):
        hit_tree.GetEntry(i)
        phi_array[i] = hit_tree.phi
        theta_array[i] = hit_tree.theta
    root_file.Close()

    # Calculate the mean phi's and thetas.  Depending on purpose, wrap around at two pi depending on mean location.
    if use_wrapping:
        stats['PhiMean'] = srkmisc.reduce_periodics(phi_array)
        stats['ThetaMean'] = srkmisc.reduce_periodics(theta_array)
    else:
        stats['PhiMean'] = srkmisc.careful_mean(phi_array)
        stats['ThetaMean'] = srkmisc.careful_mean(theta_array)

    if runtype != "g2":
		# Calculate probability of detecting the spin in the opposite direction
		stats['SZDetProb'] = 0.
		for phi, theta in zip(phi_array, theta_array):
			stats['SZDetProb'] += calc_opposite_spin_prob(phi - stats['PhiMean'], theta)
		stats['SZDetProb'] /= stats['NumEventsRun']

    # Calculate other summary info
    stats['PhiStDev'] = srkmisc.careful_std(phi_array)
    stats['ThetaStDev'] = srkmisc.careful_std(theta_array)
    stats['PhiError'] = stats['PhiStDev'] / math.sqrt(len(phi_array))
    stats['ThetaError'] = stats['ThetaStDev'] / math.sqrt(len(theta_array))
    if runtype != "g2":
		stats['PhiKurtosis'] = kurtosis(phi_array)
		stats['ThetaKurtosis'] = kurtosis(theta_array)
		stats['PhiSkewness'] = skew(phi_array)
		stats['ThetaSkewness'] = skew(theta_array)
		print "Phi Kurtosis: %f" % stats['PhiKurtosis']

		percentile_lower, percentile_upper = np.percentile(phi_array, (16.5, 83.50))
		percentile_width = percentile_upper - percentile_lower
		stats['PhiPercentileWidth'] = percentile_width

		percentile_lower, percentile_upper = np.percentile(theta_array, (16.5, 83.5))
		percentile_width = percentile_upper - percentile_lower
		stats['ThetaPercentileWidth'] = percentile_width

		# Fit phi to Tsallis q-Gaussian function (old form)
		power, error = make_tsallis_fit(phi_array, stats['PhiMean'], stats['PhiStDev'])
		stats['PhiTsallisPower'] = power
		stats['PhiTsallisPowerError'] = error

		# Fit theta to Tsallis q-Gaussian function (old form)
		power, error = make_tsallis_fit(theta_array, stats['ThetaMean'], stats['ThetaStDev'])
		stats['ThetaTsallisPower'] = power
		stats['ThetaTsallisPowerError'] = error

		# Fit phi to Tsallis q-Gaussian function (new form)
		power, error = make_qgaussian_fit(phi_array, stats['PhiMean'], stats['PhiStDev'])
		stats['PhiQGaussianQ'] = power
		stats['PhiQGaussianQError'] = error

		# Fit theta to Tsallis q-Gaussian function (new form)
		power, error = make_qgaussian_fit(theta_array, stats['ThetaMean'], stats['ThetaStDev'])
		stats['ThetaQGaussianQ'] = power
		stats['ThetaQGaussianQError'] = error

    return stats


def calc_orientation_stats(run_id, is_parallel):
    """Calc stats related to an orientation of the E0 and B0 fields (parallel and anti-parallel)"""

    if is_parallel:
        letter = 'P'
        run_type = 'Par'
    else:
        letter = 'A'
        run_type = 'Anti'
    file_path = srkdata.srkglobal.results_dir + "Results_RID" + str(run_id) + "_" + letter + ".root"

    stats = calc_stats_for_results_file(file_path)

    if len(stats) == 0:
        return {}

    stats = srkdata.prefix_dict_keys(stats, run_type + '_')

    srk_settings, run_settings = srkdata.get_settings_from_database(run_id)
    pr_stats = calc_dipole_predictions_pignol_and_rocia(srk_settings)

    return srkdata.merge_dicts(stats, pr_stats)


def calc_delta_stats_same_tracks(run_id, use_wrapping=True):
    """Calculates differences in orientation of fields when tracks are the same"""
    hit_trees = []
    root_files = []
    for is_parallel in [True, False]:
        if is_parallel:
            letter = 'P'
        else:
            letter = 'A'
        file_path = srkglobal.results_dir + "Results_RID" + str(run_id) + "_" + letter + ".root"

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
        delta_phi = hit_trees[0].phi - hit_trees[1].phi
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
    """Calculates all the run statistics for a nedm-type run for the database."""
    srk_settings, run_settings = srkdata.get_settings_from_database(run_id)

    # Calculate all the statistics related to each orientation
    p_stats = calc_orientation_stats(run_id, True)
    a_stats = calc_orientation_stats(run_id, False)

    # Check if data for both orientations exists
    both_orientations = False
    if len(p_stats) > 0 or len(a_stats) > 0:
        both_orientations = True

    p_stats['DipolePositionBelowChamber'] = get_dist_bottom_from_pos(srk_settings['DipolePosition'],
                                                                     srk_settings['ChamberHeight'])
    pos = [float(x) for x in srk_settings['DipolePosition'].split(' ')]  # Splits up space separates position list
    p_stats['DipolePositionX'] = pos[0]

    # Return here if both orientations
    if not both_orientations:
        return srkdata.merge_dicts(p_stats, a_stats)

    # Calculate stats related to frequency difference between orientaitons
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

    pr_stats = calc_dipole_predictions_pignol_and_rocia(srk_settings)

    return srkdata.merge_dicts(run_stats, p_stats, a_stats, pr_stats)


def check_user_info_tree(run_id, post_fix):
    """Prints use info tree (contains used macro commands)."""
    file_path = srkdata.srkglobal.results_dir + "Results_RID" + str(run_id) + "_" + post_fix + ".root"
    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return
    root_file = TFile(file_path, "READ")
    hit_tree = gDirectory.Get('hitTree')
    u = hit_tree.GetUserInfo()
    u.Print()
    root_file.Close()
    return


def calc_centered_rho_b_sub_rho(dip_str, radius, height, dist):
    """See dipole paper from Pignol and Rocia."""
    return ((2. * dip_str) / (radius * radius * height)) * (
        2. * height + ((radius * radius + 2. * dist * dist) / math.sqrt(radius * radius + dist * dist)) - (
            (radius * radius + 2. * pow(dist + height, 2)) / math.sqrt(radius * radius + pow(dist + height, 2))))


def calc_centered_db_dz(dip_str, radius, height, dist):
    """See dipole paper from Pignol and Rocia."""
    return ((2. * dip_str) / height) * (
        pow(pow(dist + height, 2) + radius * radius, -1.5) - pow(dist * dist + radius * radius, -1.5))


def calc_e_plus_one(dip_str, radius, height, dist):
    """See dipole paper from Pignol and Rocia."""
    return -(4. / (radius * radius)) * (calc_centered_rho_b_sub_rho(dip_str, radius, height, dist)
                                        / calc_centered_db_dz(dip_str, radius, height, dist))


def calc_dipole_predictions_pignol_and_rocia(srk_settings):
    """Calculates the geometric phase shift from dipole according to Pignol and Rocia paper
        PHYSICAL REVIEW A 85, 042105 (2012)"""
    out = dict()

    dip_str = srk_settings['DipoleFieldStrength']

    if dip_str == 0:
        return out

    pos = [float(x) for x in srk_settings['DipolePosition'].split(' ')]  # Splits up space separates position list
    radius = srk_settings['ChamberRadius']
    height = srk_settings['ChamberHeight']
    dist = -pos[2] - .5 * height
    gyro = srk_settings['GyromagneticRatio']
    cspeed = 299792458
    hbar = 6.582E-016

    false_edm = -(hbar * gyro * gyro / (2 * cspeed * cspeed)) * calc_centered_rho_b_sub_rho(dip_str, radius, height,
                                                                                            dist) * 100

    out['PRPrediction'] = false_edm
    if srk_settings['E0FieldStrength'] == 0.:
        out['PRPredictionDeltaOmega'] = 0.
    else:
        out['PRPredictionDeltaOmega'] = false_edm / (100. * hbar / (4. * srk_settings['E0FieldStrength']))
    out['PRPredictionDeltaPhase'] = out['PRPredictionDeltaOmega'] * srk_settings['TimeLimit']
    out['PREPlusOne'] = calc_e_plus_one(dip_str, radius, height, dist)
    return out


def calc_dipole_b_field(dipole_str, pos_vec, dipole_vec=(0., 0., 1.)):
    """Calculates the bfield do to a dipole."""
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
    """Returns the position of the dipole in simulation space based on it's distance from the bottom of the chamber."""
    return '0. 0. ' + str(-0.5 * chamber_height - dist_from_bottom)


def get_dist_bottom_from_pos(dip_pos, chamber_height):
    """Returns the distance from the bottom of the chamber based on the position in simulation space."""
    return 0.5 * chamber_height + float(dip_pos.split(' ')[2])


# Presumes centered dipole for now
def get_dipole_str_to_match_field(dist_from_bottom, normalize_val, normalize_type):
    if normalize_type == "MaxBFieldCentered":
        return 0.5 * normalize_val * dist_from_bottom * dist_from_bottom * dist_from_bottom
    else:
        print "Normalize type not recognized"
        return None


def calc_mean_vel_from_Omega(Omega, omega_0, chamber_radius):
    """Calculate a mean velocity needed for a particular Omega (See Steyerl et. al) with a given omega_0 and radius"""
    omega_r = Omega * omega_0
    return abs(omega_r * chamber_radius)


def calc_Omega(run_id):
    """Calculate the Omega (See Steyerl et. al) for a run from the database."""
    srk_settings, run_settings = srkdata.get_settings_from_database(run_id)

    omega_0 = srk_settings['B0FieldStrength'] * srk_settings['GyromagneticRatio']
    omega_r = srk_settings['MeanVel'] / srk_settings['ChamberRadius']
    return omega_r / omega_0


def calc_false_edm(delta_omega, e_field):
    """Calculate the false EDM strength based on a frequency difference and an e_field"""
    return delta_omega * (100. * 6.58211928E-016 / (4 * e_field))


def convert_std_dev_to_false_edm_measurement_error(std_dev, e_field, meas_time, num_particles):
    """Converts the standard deviation of the frequency difference to an EDM measurement error"""
    delta_omega_error = (std_dev / meas_time) / math.sqrt(num_particles)
    return math.sqrt(2) * abs(calc_false_edm(delta_omega_error, e_field))  # sqrt 2 due to both par and anti par


def calc_t2(phi, theta, time):
    """Calculates T_2 time (spin relaxtion) based on the phi angle, theta, and time.
        This presumes a spin flip will take place."""
    opp_spin_prob = calc_opposite_spin_prob(phi, theta)
    return -time / math.log(1. - opp_spin_prob)


def calc_t2_from_prob(opp_spin_prob, time):
    """Calculates T_2 time (spin relaxtion) based on the detection probability of spin being in the opposite direction
        compared to where it started."""
    return -time / math.log(1. - opp_spin_prob)


def make_phi_hist_with_noise(rid, is_parallel, hist_dim, noise_stdev, normalize):
    """Makes a histogram of the phi angle with added noise."""
    hist = TH1D("blurredHist" + str(rid), "blurredHist" + str(rid), hist_dim[0], hist_dim[1], hist_dim[2])

    if is_parallel:
        letter = 'P'
    else:
        letter = 'A'
    file_path = srkdata.srkglobal.results_dir + "Results_RID" + str(rid) + "_" + letter + ".root"

    f = ROOT.TFile.Open(file_path)
    phi_list = []
    for event in f.hitTree:
        phi_list.append(gRandom.Gaus(event.phi, noise_stdev))

    mean = srkmisc.reduce_periodics(phi_list)
    stdev = srkmisc.careful_std(phi_list)
    for x in phi_list:
        if normalize:
            hist.Fill((x - mean) / stdev)
        else:
            hist.Fill(x)

    f.Close()
    ROOT.SetOwnership(hist, True)
    return hist


def make_tsallis_fit(data, mean, stdev):
    """Fits a Tsallis q-Gaussian function (old version) to an array of numbers"""
    if stdev == 0:
        return [0, 0]
    histogram = TH1D("hist", "hist", 100, -5, 5)
    for phi in data:
        histogram.Fill((phi - mean) / stdev)
    tsallis_func = TF1("phiTsallisFunc", "[0]/pow(1+((x)/[1])*((x)/[1]),[2])", -5, 5)
    max_bin = histogram.GetMaximum()
    tsallis_func.SetParNames("Amplitude", "Sigma", "Power")
    tsallis_func.SetParLimits(1, .1, 20)
    tsallis_func.SetParLimits(0, 0.5 * max_bin, 1.5 * max_bin)
    tsallis_func.SetParLimits(2, 2, 100)
    tsallis_func.SetParameters(max_bin, stdev, 7)
    if histogram.Integral() == 0:
        return [0, 0]

    histogram.Fit("phiTsallisFunc", "NM")

    if ROOT.gMinuit.fCstatu == "OK        " and tsallis_func.GetNDF() > 0:  # If no error
        chisquare_per_ndf = tsallis_func.GetChisquare() / tsallis_func.GetNDF()
        if chisquare_per_ndf < 2:
            print "Tsallis fitted!"
            return [tsallis_func.GetParameter(2), tsallis_func.GetParError(2)]
    print "Failed to fit Tsallis"
    return [0, 0]


def make_qgaussian_fit(data, mean, stdev):
    """Fits a Tsallis q-Gaussian function (new version) to an array of numbers"""
    if stdev == 0:
        return [0, 0]
    histogram = TH1D("hist", "hist", 100, -5, 5)
    for phi in data:
        histogram.Fill((phi - mean) / stdev)
    q_gaussian_func = TF1("qGaussianFunc", "[0]*pow(1+([2]-1)*[1]*x*x,-1/([2]-1))")
    max_bin = histogram.GetMaximum()
    q_gaussian_func.SetParNames("Amplitude", "Beta", "q")
    q_gaussian_func.SetParLimits(1, 0.1, 20)
    q_gaussian_func.SetParLimits(0, 0.5 * max_bin, 1.5 * max_bin)
    q_gaussian_func.SetParLimits(2, 1.0001, 3)
    q_gaussian_func.SetParameters(max_bin, 3, 2)
    print "Hist Kurtosis: %f" % histogram.GetKurtosis()
    if histogram.Integral() == 0:
        return [0, 0]

    histogram.Fit("qGaussianFunc", "MV")
    print "Status: %s" % ROOT.gMinuit.fCstatu
    if (
                    ROOT.gMinuit.fCstatu == "OK        " or ROOT.gMinuit.fCstatu == "CONVERGED ") and q_gaussian_func.GetNDF() > 0:  # If no error

        # chisquare_per_ndf = q_gaussian_func.GetChisquare() / q_gaussian_func.GetNDF()
        print "Chisquared/NDF: %d / %d" % (q_gaussian_func.GetChisquare(), q_gaussian_func.GetNDF())
        # if chisquare_per_ndf < 2:
        #     print "qGaussian fitted!"
        return [q_gaussian_func.GetParameter(2), q_gaussian_func.GetParError(2)]
    print "Failed to fit qGaussian"
    return [0, 0]


def make_alpha_vs_phi_plot(run_id, is_parallel):
    if is_parallel:
        letter = 'P'
    else:
        letter = 'A'
    file_path = srkdata.srkglobal.results_dir + "Results_RID" + str(run_id) + "_" + letter + ".root"

    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return {}

    root_file = TFile(file_path, "READ")
    hit_tree = gDirectory.Get('hitTree')
    gROOT.cd()
    num_events = hit_tree.GetEntries()

    phi_list = []
    alpha_list = []
    radius = srkdata.get_data_for_rids_from_database([run_id], "ChamberRadius")[0][0]
    print radius
    for i in xrange(num_events):
        hit_tree.GetEntry(i)
        phi_list.append(hit_tree.phi)
        alpha = get_alpha_angle_2d(radius, hit_tree.pos0, hit_tree.vel0)
        alpha_list.append(alpha)
    root_file.Close()

    phi_mean = srkmisc.reduce_periodics(phi_list)

    delta_phi_list = map(lambda x: x - phi_mean, phi_list)

    plt.scatter(alpha_list, delta_phi_list)


def get_alpha_angle_2d(radius, pos0, vel0):
    shape = TGeoTube(0, radius, radius)
    point = array.array('d', [pos0.X(), pos0.Y(), 0])
    vel0.SetZ(0)

    vel0.SetMag(1)

    direction = array.array('d', [vel0.X(), vel0.Y(), 0])
    distance = shape.DistFromInside(point, direction)

    post_out = pos0 + vel0 * distance

    norm_list = array.array('d', [0, 0, 0])
    point = array.array('d', [post_out.X(), post_out.Y(), 0])

    shape.ComputeNormal(point, direction, norm_list)
    norm = TVector3(norm_list[0], norm_list[1], norm_list[2])
    dot_prod = vel0.Dot(norm)

    angle = math.acos(dot_prod)

    return angle


def q_gaussian(x, a, beta, q):
    """Calculates the value of the q_gaussian distribution (new)"""
    return a * pow(1 + (q - 1) * beta * x * x, -1 / (q - 1))


def calc_opposite_spin_prob(phi, theta):
    """Calculates the opposite spin probability given a phi and theta"""
    cos_phi = math.cos(phi)
    cos_theta = math.cos(theta)
    return 0.5 * (1. - cos_phi * cos_theta)


def make_sz_prob_dist(run_id, is_parallel, use_wrapping=True):
    """Make a spin direction (after flip) detection probability histogram"""
    if is_parallel:
        letter = 'P'
    else:
        letter = 'A'

    file_path = srkdata.srkglobal.results_dir + "Results_RID" + str(run_id) + "_" + letter + ".root"

    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return []

    root_file = TFile(file_path, "READ")

    hit_tree = gDirectory.Get('hitTree')
    gROOT.cd()
    num_events = hit_tree.GetEntries()

    phi_list = []
    theta_list = []
    for i in xrange(num_events):
        hit_tree.GetEntry(i)
        phi_list.append(hit_tree.phi)
        theta_list.append(hit_tree.theta)
    root_file.Close()

    if use_wrapping:
        phi_mean = srkmisc.reduce_periodics(phi_list)
    else:
        phi_mean = srkmisc.careful_mean(phi_list)

    phi_std = srkmisc.careful_std(phi_list)

    theta_std = srkmisc.careful_std(theta_list)

    comb_std = np.sqrt(phi_std * phi_std + theta_std * theta_std)

    print "Combined Standard deviation: %e" % (comb_std)

    x = np.linspace(-30, 30, num=60)

    y = []
    for num_std_dev in x:
        sz_det_prob = 0
        for phi, theta in zip(phi_list, theta_list):
            sz_det_prob += calc_opposite_spin_prob(phi - phi_mean + comb_std * num_std_dev, theta)
        sz_det_prob /= num_events
        y.append(1 - sz_det_prob)

    return x, y


def get_result_data(leaf_names, run_id, is_parallel):
    """Get result data directly from root files based on leaf names"""
    if is_parallel:
        letter = 'P'
    else:
        letter = 'A'
    file_path = srkdata.srkglobal.results_dir + "Results_RID" + str(run_id) + "_" + letter + ".root"
    print "Opening ", file_path

    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return {}

    root_file = TFile(file_path, "READ")
    hit_tree = gDirectory.Get('hitTree')
    gROOT.cd()
    num_events = hit_tree.GetEntries()

    data = []
    for leaf_name in leaf_names:
        temp_data = []
        for i in xrange(num_events):
            hit_tree.GetEntry(i)
            temp_data.append(hit_tree.GetBranch(leaf_name).GetListOfLeaves()[0].GetValue())
        data.append(temp_data)
    root_file.Close()

    return data


def calc_step_tree(file_path, inp_periodic_stop_time):
    """Calculate time and spin detection probabilities from step tree."""
    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return []
    print "Calculating step tree for {}".format(file_path)
    root_file = TFile(file_path, "READ")
    step_tree = gDirectory.Get('stepTree')
    hit_tree = gDirectory.Get('hitTree')
    gROOT.cd()
    user_info_list = hit_tree.GetUserInfo()

    periodic_stop_time = inp_periodic_stop_time
    for i in xrange(user_info_list.GetEntries()):
        par = user_info_list.At(i)
        if par.GetName() == 'PeriodicStopTime':
            periodic_stop_time = float(par.GetTitle())
            break

    num_events = hit_tree.GetEntries()
    num_steps_per_event = step_tree.GetEntries() / num_events

    time_data = np.zeros(num_steps_per_event)
    sx_prob_data = np.zeros(num_steps_per_event)

    # Set times
    for j in xrange(num_steps_per_event):
        time_data[j] = ((j + 1) * periodic_stop_time)

    # Add data
    for i in xrange(num_events):
        if i % 100 == 0:
            print "Stepping for Event {} in {}".format(i, file_path)
        for j in xrange(num_steps_per_event):
            step_tree.GetEntry(i * num_steps_per_event + j)
            sx_prob_data[j] += step_tree.sxProb

    # Normalize
    sx_prob_data /= float(num_events)

    root_file.Close()
    return zip(time_data, sx_prob_data)


def calc_step_tree_to_txt(run_id, inp_periodic_stop_time):
    """Calculate time and spin detection probabilities from step tree and save to text file."""
    results_file_path = srkdata.srkglobal.results_dir + "Results_RID" + str(run_id) + "_P.root"
    txt_file_path = srkdata.srkglobal.hists_dir + "data_steps_RID" + str(run_id) + "_P.txt"
    data = calc_step_tree(results_file_path, inp_periodic_stop_time)
    with open(txt_file_path, 'wb') as csvfile:
        the_writer = csv.writer(csvfile, delimiter='\t')
        the_writer.writerow(['#Time', 'Spin_X_Dir_Probability'])
        for x, y in data:
            the_writer.writerow([x, y])
