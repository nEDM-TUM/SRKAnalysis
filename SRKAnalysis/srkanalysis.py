import csv
from ROOT import TFile, TTree, gDirectory, gROOT, gRandom, TH1D, TF1,TGeoTube,TVector3
import ROOT
import srkdata
import srkmisc
import math
import array
from scipy import constants as const
from scipy.stats import kurtosis, skew
from uncertainties import ufloat
import numpy as np
import matplotlib.pyplot as plt

__author__ = 'mjbales'


def calc_stats_for_results_file(file_path, use_wrapping = False):
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
    print "Phi Kurtosis: %f" % stats['PhiKurtosis']
    stats['ThetaKurtosis'] = kurtosis(theta_list)

    stats['PhiSkewness'] = skew(phi_list)
    stats['ThetaSkewness'] = skew(theta_list)

    percentile_lower, percentile_upper = np.percentile(phi_list, [16.5, 83.5])
    percentile_width = percentile_upper - percentile_lower
    stats['PhiPercentileWidth'] = percentile_width

    percentile_lower, percentile_upper = np.percentile(theta_list, [16.5, 83.5])
    percentile_width = percentile_upper - percentile_lower
    stats['ThetaPercentileWidth'] = percentile_width


    power,error=make_tsallis_fit(phi_list,stats['PhiMean'],stats['PhiStDev'])

    stats['PhiTsallisPower']=power
    stats['PhiTsallisPowerError']=error

    power,error=make_tsallis_fit(theta_list,stats['ThetaMean'],stats['ThetaStDev'])

    stats['ThetaTsallisPower']=power
    stats['ThetaTsallisPowerError']=error

    power,error=make_qgaussian_fit(phi_list,stats['PhiMean'],stats['PhiStDev'])

    stats['PhiQGaussianQ']=power
    stats['PhiQGaussianQError']=error

    power,error=make_qgaussian_fit(theta_list,stats['ThetaMean'],stats['ThetaStDev'])

    stats['ThetaQGaussianQ']=power
    stats['ThetaQGaussianQError']=error

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

    if len(p_stats) == 0 or len(a_stats) == 0:
        return srkdata.merge_dicts(p_stats, a_stats)

    run_stats = srkdata.default_delta_omega_stats()

    if len(p_stats) > 0 or len(a_stats) > 0:
        p_stats['DipolePositionBelowChamber'] = get_dist_bottom_from_pos(srk_settings['DipolePosition'], srk_settings['ChamberHeight'])
        pos = [float(x) for x in srk_settings['DipolePosition'].split(' ')]  # Splits up space separates position list
        p_stats['DipolePositionX'] = pos[0]

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
    out['PREPlusOne'] = calc_e_plus_one(dip_str, radius, height, dist)
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
    return 0.5 * chamber_height + float(dip_pos.split(' ')[2])


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





def calc_t2(phi, theta, time):
    opp_spin_prob=calc_opposite_spin_prob(phi,theta)
    return -time/math.log(1.-opp_spin_prob)


def calc_t2_from_prob(opp_spin_prob, time):
    return -time/math.log(1.-opp_spin_prob)


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


def make_tsallis_fit(phi_list,mean,stdev):
    if stdev == 0:
        return [0, 0]
    histogram = TH1D("phi_hist", "phi_hist", 100, -5, 5)
    for phi in phi_list:
        histogram.Fill((phi - mean) / stdev)
    phi_tsallis_func = TF1("phiTsallisFunc", "[0]/pow(1+((x)/[1])*((x)/[1]),[2])", -5,5)
    max_bin = histogram.GetMaximum()
    phi_tsallis_func.SetParNames("Amplitude", "Sigma", "Power")
    phi_tsallis_func.SetParLimits(1, .1, 20)
    phi_tsallis_func.SetParLimits(0, 0.5 * max_bin, 1.5 * max_bin)
    phi_tsallis_func.SetParLimits(2, 2, 100)
    phi_tsallis_func.SetParameters(max_bin, stdev, 7)
    if histogram.Integral() == 0:
        return [0, 0]

    histogram.Fit("phiTsallisFunc", "NM")

    if ROOT.gMinuit.fCstatu == "OK        " and phi_tsallis_func.GetNDF() > 0:  # If no error
        chisquare_per_ndf = phi_tsallis_func.GetChisquare() / phi_tsallis_func.GetNDF()
        if chisquare_per_ndf < 2:
            print "Tsallis fitted!"
            return [phi_tsallis_func.GetParameter(2), phi_tsallis_func.GetParError(2)]
    print "Failed to fit Tsallis"
    return [0, 0]


def make_qgaussian_fit(phi_list,mean,stdev):
    if stdev == 0:
        return [0, 0]
    histogram = TH1D("phi_hist", "phi_hist", 100, -5, 5)
    for phi in phi_list:
        histogram.Fill((phi - mean) / stdev)
    qGaussianFunc = TF1("qGaussianFunc", "[0]*pow(1+([2]-1)*[1]*x*x,-1/([2]-1))")
    max_bin = histogram.GetMaximum()
    qGaussianFunc.SetParNames("Amplitude", "Beta", "q");
    qGaussianFunc.SetParLimits(1,0.1,20)
    qGaussianFunc.SetParLimits(0,0.5*max_bin,1.5*max_bin)
    qGaussianFunc.SetParLimits(2,1.0001,3)
    qGaussianFunc.SetParameters(max_bin, 3,2)
    print "Hist Kurtosis: %f" % histogram.GetKurtosis()
    if histogram.Integral() == 0:
        return [0, 0]

    histogram.Fit("qGaussianFunc", "NMV")
    print "Status: %s" % ROOT.gMinuit.fCstatu
    if (ROOT.gMinuit.fCstatu == "OK        " or ROOT.gMinuit.fCstatu == "CONVERGED ") and qGaussianFunc.GetNDF() > 0:  # If no error

        chisquare_per_ndf = qGaussianFunc.GetChisquare() / qGaussianFunc.GetNDF()
        print "Chisquared/NDF: %d / %d" % (qGaussianFunc.GetChisquare(),qGaussianFunc.GetNDF())
        # if chisquare_per_ndf < 2:
        #     print "qGaussian fitted!"
        return [qGaussianFunc.GetParameter(2), qGaussianFunc.GetParError(2)]
    print "Failed to fit qGaussian"
    return [0, 0]


def make_alpha_vs_phi_plot(run_id, is_parallel):
    if is_parallel:
        letter = 'P'
        run_type = 'Par'
    else:
        letter = 'A'
        run_type = 'Anti'
    file_path = srkdata.SRKSystems.results_dir + "Results_RID" + str(run_id) + "_" + letter + ".root"

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
        alpha = get_alpha_angle_2D(radius, hit_tree.pos0, hit_tree.vel0)
        alpha_list.append(alpha)
    root_file.Close()

    phi_mean = srkmisc.reduce_periodics(phi_list)

    delta_phi_list = map(lambda x: x-phi_mean, phi_list)

    plt.scatter(alpha_list, delta_phi_list)


def get_alpha_angle_2D(radius, pos0, vel0):
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
    return a*pow(1+(q-1)*beta*x*x,-1/(q-1))


# Using phi and theta delta from central frequency
def calc_opposite_spin_prob(phi, theta):
    cos_phi = math.cos(phi)
    cos_theta = math.cos(theta)
    return 0.5 * (1. - cos_phi * cos_theta)


def make_sz_prop_dist(run_id, is_parallel, use_wrapping = True):
    if is_parallel:
        letter = 'P'
    else:
        letter = 'A'

    file_path = srkdata.SRKSystems.results_dir + "Results_RID" + str(run_id) + "_" + letter + ".root"

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


    phi_mean=0
    if use_wrapping:
        phi_mean = srkmisc.reduce_periodics(phi_list)
    else:
        phi_mean = srkmisc.careful_mean(phi_list)

    phi_std = srkmisc.careful_std(phi_list)

    theta_std = srkmisc.careful_std(theta_list)

    comb_std=np.sqrt(phi_std*phi_std+theta_std*theta_std)

    print "Combined Standard deviation: %e" % (comb_std)

    x=np.linspace(-30,30,num=60)

    y=[]
    for nstd in x:
        sz_det_prob=0
        for phi, theta in zip(phi_list, theta_list):
            sz_det_prob += calc_opposite_spin_prob(phi - phi_mean + comb_std*nstd, theta)
        sz_det_prob /= num_events
        y.append(1-sz_det_prob)

    return x,y


def get_result_data(leaf_names, run_id, is_parallel):
    if is_parallel:
        letter = 'P'
    else:
        letter = 'A'
    file_path = srkdata.SRKSystems.results_dir + "Results_RID" + str(run_id) + "_" + letter + ".root"
    print "Opening ",file_path

    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return {}

    root_file = TFile(file_path, "READ")
    hit_tree = gDirectory.Get('hitTree')
    gROOT.cd()
    num_events = hit_tree.GetEntries()

    data=[]
    for leaf_name in leaf_names:
        temp_data=[]
        for i in xrange(num_events):
            hit_tree.GetEntry(i)
            temp_data.append(hit_tree.GetBranch(leaf_name).GetListOfLeaves()[0].GetValue())
        data.append(temp_data)
    root_file.Close()

    return data


def calc_step_tree(file_path,inp_periodic_stop_time):

    if not srkmisc.file_exits_and_not_zombie(file_path):
        print file_path + " doesn't exist or is zombie."
        return []

    root_file = TFile(file_path, "READ")
    step_tree = gDirectory.Get('stepTree')
    hit_tree = gDirectory.Get('hitTree')
    gROOT.cd()
    user_info_list = hit_tree.GetUserInfo()
    
    periodic_stop_time = inp_periodic_stop_time
    for i in xrange(user_info_list.GetEntries()):
        par = user_info_list.At(i)
        if(par.GetName() == 'PeriodicStopTime'):
            periodic_stop_time = float(par.GetTitle())
            break
        
    
    num_events = hit_tree.GetEntries()
    num_steps_per_event = step_tree.GetEntries() / num_events
    
    time_data = np.zeros(num_steps_per_event)
    sx_prob_data = np.zeros(num_steps_per_event)

    #Set times
    for j in xrange(num_steps_per_event):
        time_data[j] = ((j + 1) * periodic_stop_time)
        
    #Add data
    for i in xrange(num_events):
        if(i % 10 == 0):
            print "Starting Event: {}".format(i);
        for j in xrange(num_steps_per_event):
            step_tree.GetEntry(i * num_steps_per_event + j)
            sx_prob_data[j] += step_tree.sxProb
            
    #Normalize
    sx_prob_data /= float(num_events) 
        
    root_file.Close()
    return zip(time_data,sx_prob_data)

def calc_step_tree_to_txt(results_file_path, txt_file_path,inp_periodic_stop_time):
    data=calc_step_tree(results_file_path,inp_periodic_stop_time)
    with open(txt_file_path, 'wb') as csvfile:
        the_writer = csv.writer(csvfile, delimiter='\t')
        the_writer.writerow(['#Time','Spin_X_Dir_Probability'])
        for x,y in data:
            the_writer.writerow([x,y])
