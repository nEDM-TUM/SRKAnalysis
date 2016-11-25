from srkanalysis import get_dipole_pos_from_dist
import srkdata
import srkmisc
import srkmultiprocessing
import srkanalysis
import sqlite3
import numpy as np
from datetime import date
import srkglobal

import time
start_time = time.time()

today = date.today()
s = srkdata.default_srk_settings()
r = srkdata.default_run_settings()
srkglobal.set_computer("work_laptop")
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Date'] = today.strftime('%m/%d/%y')
# r['SRKVersion'] = 'ebf724686bcbc17c2aa0d7348295f633d770aa2c'
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 50000
#
# s['B0FieldStrength'] = 1.e-6
# s['E0FieldStrength'] = 1.e6
# r['Title'] = 'Quick check runs'
# s['DipolePosition'] = '0. 0. -0.061' #1 mm below chamber
#
# dipole_field_strengths = srkmisc.even_sample_over_log(1e-18, 1e-11, 16)
#
# for i in dipole_field_strengths:
#     s['DipoleFieldStrength'] = i
#     srkdata.run_on_optima(s, r)

#srkdata.get_settings_from_database()

# rid_numbers = range(217, 231)
# new_rid_numbers = []
# for i in rid_numbers:
#     s, r = srkdata.get_settings_from_database(i)
#     r['SRKVersion'] = 'ebf724686bcbc17c2aa0d7348295f633d770aa2c'
#     r['Date'] = today.strftime('%m/%d/%y')
#     r['Title'] = 'Vary Dipole E=0, 6 mm below'
#     r['RunType'] = 'parOnly'
#     s['DipolePosition'] = '0. 0. -0.12'
#     s['ParallelFields'] = 1
#     r['NumTracksPer'] = 5000
#     new_rid_numbers += [srkdata.make_macro_and_add_to_database(s, r)]
#
# # new_rid_numbers = range(349, 363)
# for i in new_rid_numbers[0:6]:
# # # for i in new_rid_numbers:
#     s, r = srkdata.get_settings_from_database(i)
# # #     srkdata.make_macro(i,s,r)
#     srkdata.run_macro_laptop(i)
#     # srkdata.run_macro_optima([i])
# # # srkdata.run_macro_optima(new_rid_numbers)


# for i in range(363, 369):
#     srkdata.calc_orientation_stats_to_database(i, True)




# db_connection = sqlite3.connect(srkdata.database_path)
# db_cursor = db_connection.cursor()
#
# for i in xrange(1, 320):
#
#     print "Run"+str(i)
#     select_str = 'SELECT DipolePosition,DipolePositionBelowChamber,ChamberHeight,DipolePositionX FROM '+ srkdata.database_runlog_table_name + ' WHERE Run='+str(i)
#     db_cursor.execute(select_str)
#     values = db_cursor.fetchone()
#     dipole_pos = values[0]
#     dipole_pos_x = values[3]
#     if dipole_pos_x is not None or dipole_pos_x > 0:
#         dipole_pos_below = values[1]
#         chamber_height = values[2]
#         dipole_pos = str(dipole_pos_x)+" 0. "+str(-0.5*chamber_height-dipole_pos_below)
#         update_str = "UPDATE RunLog SET DipolePosition='"+dipole_pos+"' WHERE Run="+str(i)
#         db_cursor.execute(update_str)
#         db_connection.commit()



# Close up DB connection
#db_connection.close()

###################################################################
#
# dist_range = np.concatenate([[.001], np.arange(.01, .11, .01)])
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 1000
# r['Title'] = 'Fixed Chamber Height, Vary dipole, E=5e5'
# s['E0FieldStrength'] = 5e5
#
# rid_list = []
# for dip_str in srkmisc.even_sample_over_log(1e-18, 1e-13, 6):
#     s['DipoleFieldStrength'] = dip_str
#     for dist in dist_range:
#         s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - dist)
#         rid_list += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
# #
# # #
# #
# # rid_list = range(377, 443)
# rid_chunks = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# for i in rid_chunks:
#     srkdata.make_macro_mult_from_database(i)
#     srkdata.run_macro_mult_laptop(i)
###################################################################

# rid_list = range(377, 443)
# rids = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# # print zip(*rids)
# rids=sum(rids,[])
#
# rid_list = range(443, 509)
# for i in rid_list:
#     srkdata.calc_orientation_stats_to_database(i, True)

# for i in range(1, 443):
#     s, r = srkdata.get_settings_from_database(i)
#     predictions = srkanalysis.calc_dipole_predictions_pignol_and_rocia(s)
#     srkdata.update_database(predictions, 'Run='+str(i))
###################################################################

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 500000
# r['Title'] = 'Fixed Chamber Height, Dipole Shifts'
# s['E0FieldStrength'] = 5e6
#
# rid_list=[]
# dist_range = np.arange(.01, .11, .01)
# for dist in dist_range:
#     s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - dist)
#     rid_list += [srkdata.make_macro_and_add_to_database(s, r)]
#
# for i in rid_list:
#     srkdata.run_macro_optima([i])
# rid_list = range(509, 575)
# for i in rid_list:
#     srkdata.calc_orientation_stats_to_database(i, True)

#####################################################################
# dist_range = np.concatenate([[.001], np.arange(.01, .11, .01)])
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 1000
# r['Title'] = 'Fixed Chamber Height, Vary E Field'
# s['E0FieldStrength'] = 5e5
#
# rid_list = []
# for dip_str in srkmisc.even_sample_over_log(1e-18, 1e-13, 6):
#     s['DipoleFieldStrength'] = dip_str
#     for dist in dist_range:
#         s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - dist)
#         rid_list += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
# #
# # #
# #
# # rid_list = range(377, 443)
# rid_chunks = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# for i in rid_chunks:
#     srkdata.make_macro_mult_from_database(i)
#     srkdata.run_macro_mult_laptop(i)

###################################################
## Variable electric field

# dist_range = np.concatenate([[.001], np.arange(.01, .11, .01)])
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 1000
# r['Title'] = 'Fixed Chamber Height, Vary E Field'
#
# s['DipoleFieldStrength'] = 1e-16
#
# rid_list = []
# for e_field in srkmisc.even_sample_over_log(1e5, 1e8, 6):
#     s['E0FieldStrength'] = e_field
#     for dist in dist_range:
#         s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - dist)
#         # rid_list += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#

# rid_list = range(585, 651)
# rid_chunks = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# for i in rid_chunks[4:6]:
#     # srkdata.make_macro_mult_from_database(i)
#     print i
#     srkdata.run_mult_macro_local(i)


#srkdata.run_macro_local([596,597,598,599,600,601,602,603,604,605,606])
# srkdata.run_mult_macro_local(range(618,629))

###################################################
## Normalize max magnetic field

# dist_range = np.concatenate([[.001], np.arange(.01, .11, .01)])

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 1000
# r['Title'] = 'Vary Max B Field and Distance'
# s['E0FieldStrength'] = 1.e6
#
#
# rid_list = []
# for max_b_field in srkmisc.even_sample_over_log(1e-9, 1e-7, 6):
#     s['DipoleFieldStrength'] = max_b_field
#     for dist in dist_range:
#         s['DipolePosition'] = srkanalysis.get_dipole_pos_from_dist(dist, s['ChamberHeight'])
#         # rid_list += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]


# rid_list = range(585, 651)
# rid_chunks = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# for i in rid_chunks:
#     srkdata.make_macro_mult_from_database(i)
#     # srkdata.run_mult_macro_local(i)


###################################################
## 2D simulation of linear gradient
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = '2D Diffuse'
# s['Use2D'] = 1
# s['TimeLimit'] = 1.
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 1.e6
#
# run_ids = []
# for gradient in [1.e-10, 1.e-9, 1.e-8]:
#     s['BGradFieldStrength'] = gradient
#     run_ids += [srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 100)]
#
# for x in run_ids:
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)

# for i in xrange(585, 1017):
#     srkdata.calc_run_stats_to_database(i)

###############
## Specular
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = '2D Specular'
# s['Use2D'] = 1
# s['TimeLimit'] = 1.
# s['DiffuseReflectionProb'] = 0
# s['E0FieldStrength'] = 1.e6
#
# run_ids = []
# for gradient in [1.e-10, 1.e-9, 1.e-8]:
#     s['BGradFieldStrength'] = gradient
#     run_ids += [srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 100)]
#
# for x in run_ids:
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)

# for i in xrange(1317, 1916):
#     srkdata.calc_run_stats_to_database(i)


###################################################
## Normalize max magnetic field - edge

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()

# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Vary Max B Field at edge'
# s['E0FieldStrength'] = 1.e6
# s['DipolePosition'] = '.235 0 .061'

# for max_b_field in srkmisc.even_sample_over_log(1e-9, 1e-7, 3):
#     s['DipoleFieldStrength'] = max_b_field
#     rid = srkdata.add_to_database(srkdata.merge_dicts(s, r))
    # srkdata.run_macro_local(rid)

# for rid in range(1919, 1920):
#     srkdata.make_macro(rid,s,r)
#     srkdata.run_macro_local(rid)

# for i in xrange(1917, 1920):
#     srkdata.calc_run_stats_to_database(i)


###################################################
## Normalize max magnetic field
#
# dist_range = np.concatenate([[.001], np.arange(.01, .11, .01)])
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Vary Max B Field and Distance'
# s['E0FieldStrength'] = 5.e5
#
#
# rid_list = []
# for max_b_field in srkmisc.even_sample_over_log(1e-9, 1e-7, 6):
#     s['DipoleFieldStrength'] = max_b_field
#     for dist in dist_range:
#         s['DipolePosition'] = srkanalysis.get_dipole_pos_from_dist(dist, s['ChamberHeight'])
#         rid_list += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
#
# rid_chunks = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# for i in rid_chunks:
#     srkdata.make_macro_mult_from_database(i)
#     srkdata.run_mult_macro_local(i)


###################################################
## Diffuse Omega Vary Dipole
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = '3D Diffuse, Vary Omega Dipole 1mm'
# s['Use2D'] = 0
# s['TimeLimit'] = 1.
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 1.e6
# s['DipolePosition'] = '0. 0. 0.061'
#
# run_ids = []
# for dipoleStr in [1.e-18, 1.e-16, 1.e-14]:
#     s['DipoleFieldStrength'] = dipoleStr
#     run_ids += [srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 100)]
#
# for x in run_ids:
#     srkdata.make_macro_mult_from_database(x)
#     # srkdata.run_mult_macro_local(x)
#
# # for i in xrange(585, 1017):
# #     srkdata.calc_run_stats_to_database(i)

###################################################
## Diffuse Omega Vary Gradient 3D

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = '3D Specular, Linear Gradients'
# s['Use2D'] = 0
# s['TimeLimit'] = 1.
# s['DiffuseReflectionProb'] = 0.
# s['E0FieldStrength'] = 1.e6
#
# run_ids = []
# for gradient in [1.e-10, 1.e-9, 1.e-8]:
#     s['BGradFieldStrength'] = gradient
#     run_ids += [srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 100)]
#
# for x in run_ids:
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)

# for i in xrange(2486, 2886):
#     srkdata.calc_run_stats_to_database(i)

# for i in range(1986,2487,100):
#     srkdata.run_mult_macro_local(range(i,i+100))

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()



######
##Long term desktop
#######################
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 500000
# r['Title'] = 'Fixed Chamber Height, Dipole Shifts'
# s['E0FieldStrength'] = 5e6
# #
# # dist_range = np.arange(.01, .03, .01)
# # for dist in dist_range:
# #     s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - dist)
# #     rid = srkdata.make_macro_and_add_to_database(s, r)
# #     srkdata.run_macro_local(rid)
#
# distances =[0.01,.02]
# rids=[2886,2887]
# for i in [0, 1]:
#     s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - distances[i])
#     srkdata.make_macro(rids[i],s,r)
#     srkdata.run_macro_local(rids[i])


###################################################
## Specular Omega Vary Dipole
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = '3D Specular, Vary Omega Dipole 1mm'
# s['Use2D'] = 0
# s['TimeLimit'] = 1.
# s['DiffuseReflectionProb'] = 0
# s['E0FieldStrength'] = 1.e6
# s['DipolePosition'] = '0. 0. 0.061'
#
# run_ids = []
# for dipoleStr in [1.e-18, 1.e-16, 1.e-14]:
#     s['DipoleFieldStrength'] = dipoleStr
#     run_ids += [srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 100)]
#
# for x in run_ids:
#     # srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)
#
# # for i in xrange(585, 1017):
# #     srkdata.calc_run_stats_to_database(i)

###################################################
## Variable time

# dist_range = np.concatenate([[.001], np.arange(.01, .11, .01)])
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Vary Time'
#
# s['DipoleFieldStrength'] = 1e-16
#
# rid_list = []
# for timeLimit in srkmisc.even_sample_over_log(.1, 100, 6):
#     s['TimeLimit'] = timeLimit
#     for dist in dist_range:
#         s['DipolePosition'] = srkanalysis.get_dipole_pos_from_dist(dist, s['ChamberHeight'])
#         rid_list += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
#
# # rid_list = range()
# rid_chunks = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# for i in rid_chunks:
#     srkdata.make_macro_mult_from_database(i)
#     srkdata.run_mult_macro_local(i)

###############
## Specular 2.5D 2D fixed momentum + random Z components
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '1d58463f3b1c1163ed87da40c9fc8842c10f1288'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 1000
# r['Title'] = 'Specular Linear Gradient 2.5D 2D fixed momentum + random Z components'
# s['Use2D'] = 1
# s['BGradFieldStrength'] = 1e-10
# s['TimeLimit'] = 100.
# s['DiffuseReflectionProb'] = 0
# s['E0FieldStrength'] = 1.e6
#
# run_ids = []
# for extraVelZ in [0.1, 10, 100]:
#     s['AdditionalRandomVelZ'] = extraVelZ
#     run_ids += [srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 100)]
#
# for x in run_ids:
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)

###############
## Diffuse 2.5D 2D fixed momentum + random Z components
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '1d58463f3b1c1163ed87da40c9fc8842c10f1288'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 1000
# r['Title'] = 'Diffuse Linear Gradient 2.5D 2D fixed momentum + random Z components'
# s['Use2D'] = 1
# s['BGradFieldStrength'] = 1e-10
# s['TimeLimit'] = 100.
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 1.e6
#
# run_ids = []
# for extraVelZ in [0.1, 10, 100]:
#     s['AdditionalRandomVelZ'] = extraVelZ
#     run_ids += [srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 100)]
#
# for x in run_ids:
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)

# for i in xrange(3254, 3854):
#     srkdata.calc_run_stats_to_database(i)


#####
# let's make some track files
######
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'a9824ece0a76b9cae2b9987401297b1c0c892834'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 1000
# r['Title'] = 'Diffuse Linear Gradient with PA same trackfile'
# s['Use2D'] = 1
# s['TimeLimit'] = 1.
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 1.e6
# s['TrackFilePath'] = '!static'
# #srkdata.make_tracks_for_steyerl(100000, s, .1, 10, 100)
#
# run_ids = []
# for gradient in [1.e-10, 1.e-9, 1.e-8]:
#     s['BGradFieldStrength'] = gradient
#     run_ids += [srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 100)]
#
# for x in run_ids:
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)
#
# for i in xrange(4454, 4754):
#     srkdata.calc_run_stats_to_database(i)

####
# Longish dipole run
##
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'a9824ece0a76b9cae2b9987401297b1c0c892834'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Dipole with PA same trackfile'
# s['E0FieldStrength'] = 5e6
# s['TrackFilePath'] = "/data/nedm/tracks/Tracks_3D_Diffuse_100s_193ms.root"
#
# srkdata.make_track_file(10000, s)
#
# rid_list = []
# dist_range = np.concatenate([[.001], np.arange(.01, .11, .01)])
# for dip_str in srkmisc.even_sample_over_log(1e-18, 1e-13, 6):
#     s['DipoleFieldStrength'] = dip_str
#     for dist in dist_range:
#         s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - dist)
#         rid_list += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# rid_chunks = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# for i in rid_chunks:
#     srkdata.make_macro_mult_from_database(i)
#     srkdata.run_mult_macro_local(i)

# for i in range(4454,4820):
#     srkdata.calc_run_stats_to_database(i)

####
# Longish dipole run - now with random seeds
##
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '378328e9d8f2f40557029f7b59b8d20d8ef1d19a'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmegaSame'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Dipole with PA same tracks via same seed for each deltaOmega'
# s['E0FieldStrength'] = 5e5
# s['TrackFilePath'] = "!dynamic"
#
# rid_list = []
# dist_range = np.concatenate([[.001], np.arange(.01, .11, .01)])
# for dip_str in srkmisc.even_sample_over_log(1e-18, 1e-13, 6):
#     s['DipoleFieldStrength'] = dip_str
#     for dist in dist_range:
#         s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - dist)
#         rid_list += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# rid_chunks = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# for i in rid_chunks:
#     srkdata.make_macro_mult_from_database(i)
#     srkdata.run_mult_macro_local(i)

# for i in range(4454,4820):
#     srkdata.calc_run_stats_to_database(i)

###
#Analyze time variance

# dist_range = np.concatenate([[.001], np.arange(.01, .11, .01)])
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Vary Time'
#
# s['DipoleFieldStrength'] = 1e-16
#
# rid_list = []
# for timeLimit in srkmisc.even_sample_over_log(.1, 100, 6):
#     s['TimeLimit'] = timeLimit
#     for dist in dist_range:
#         s['DipolePosition'] = srkanalysis.get_dipole_pos_from_dist(dist, s['ChamberHeight'])
#         rid_list += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
#
# # rid_list = range()
# rid_chunks = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# for i in rid_chunks:
#     srkdata.make_macro_mult_from_database(i)
#     srkdata.run_mult_macro_local(i)

# ridlist=[range(4820,4828),range(4831,4839),range(4842,4850),range(4842,4850),range(4853,4861),range(4864,4872),range(4875,4883)]
# for i in srkmisc.flatten_list(ridlist):
#     srkdata.calc_run_stats_to_database(i)

####
# Longish dipole run - now with random seeds part deux - close range
##
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '378328e9d8f2f40557029f7b59b8d20d8ef1d19a'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmegaSame'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Dipole with PA same tracks via same seed for each deltaOmega'
# s['E0FieldStrength'] = 5e5
# s['TrackFilePath'] = "!dynamic"
#
# rid_list = []
# dist_range = np.concatenate([[.0001], np.arange(.001, .011, .001)])
# for dip_str in srkmisc.even_sample_over_log(1e-18, 1e-13, 6):
#     s['DipoleFieldStrength'] = dip_str
#     for dist in dist_range:
#         s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - dist)
#         rid_list += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# rid_chunks = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# for i in rid_chunks:
#     srkdata.make_macro_mult_from_database(i)
#     srkdata.run_mult_macro_local(i)

# for i in range(1,183):
#     srkdata.calc_run_stats_to_database(i)

##################################################
# Diffuse Omega Vary Dipole
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '378328e9d8f2f40557029f7b59b8d20d8ef1d19a'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = '3D Diffuse, No E Field, Vary Omega Dipole 1mm'
# s['Use2D'] = 0
# s['TimeLimit'] = 1.
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 0
# s['DipolePosition'] = '0. 0. 0.061'
#
# run_ids = []
# for dipoleStr in [1.e-18, 1.e-16, 1.e-14]:
#     s['DipoleFieldStrength'] = dipoleStr
#     run_ids += [srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 100)]
#
# for x in run_ids:
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)

# for i in xrange(4952, 5252):
#     srkdata.calc_run_stats_to_database(i)

##################################################
# Diffuse Omega Only B0 and E0, Vary E

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '85828d9d4a81f6693112cf7c6b67ce83071e2a66'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = '3D Diffuse, Only B0 and E0 Field'
# s['Use2D'] = 0
# s['TimeLimit'] = 1
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 0
#
#
#
# run_ids = []
# for e_field_str in srkmisc.even_sample_over_log(1e5, 1e7, 100):
#     s['E0FieldStrength'] = e_field_str
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
# #
# # run_ids = range(5252, 5352)
# for macro_ids in srkmisc.chunk_list(run_ids, 25):
#     srkdata.make_macro_mult_from_database(macro_ids)
#     srkdata.run_mult_macro_local(macro_ids)

# for i in xrange(5252, 5352):
#     srkdata.calc_run_stats_to_database(i)

##################################################
# Diffuse Omega Only B0 and E0 for only 100 s

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '85828d9d4a81f6693112cf7c6b67ce83071e2a66'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 1000
# r['Title'] = '3D Diffuse, Only B0 and E0 Field'
# s['Use2D'] = 0
# s['TimeLimit'] = 100
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 5e6
#
#
# for i in xrange(6):
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro(run_id, s, r)
#     srkdata.run_macro_local(run_id)

# for i in xrange(5352, 5358):
#     srkdata.calc_run_stats_to_database(i)

##################################################
# Diffuse Omega Only B0 and E0 for only 100 s
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '85828d9d4a81f6693112cf7c6b67ce83071e2a66'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# r['Title'] = '2D Diffuse, Only B0 and E0 Field'
# s['Use2D'] = 1
# s['TimeLimit'] = 100
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 5e6
#
#
# for i in xrange(1):
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro(run_id, s, r)
#     srkdata.run_macro_local(run_id)


#################################################
#Specular Omega Only B0 and E0 for only 100 s
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '85828d9d4a81f6693112cf7c6b67ce83071e2a66'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# r['Title'] = '2D Specular, Only B0 and E0 Field'
# s['Use2D'] = 1
# s['TimeLimit'] = 100
# s['DiffuseReflectionProb'] = 0
# s['E0FieldStrength'] = 5e6
#
#
# for i in xrange(1):
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro(run_id, s, r)
#     srkdata.run_macro_local(run_id)

# for i in xrange(917, 1017):
#     srkdata.calc_run_stats_to_database(i)

###################################################
## 3D simulation of linear gradient

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '85828d9d4a81f6693112cf7c6b67ce83071e2a66'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 1000
# r['Title'] = 'No Grav ideal of Grav Depolarizaiton paper'
# s['Use2D'] = 0
# s['TimeLimit'] = 180
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 0
#
# s['MeanVel'] = 5
#
# run_ids = []
# for gradient in srkmisc.even_sample_over_log(1e-8,1e-6,6):
#     s['BGradFieldStrength']=gradient
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro(run_id, s, r)
#     srkdata.run_macro_local(run_id)

# for i in xrange(5374, 5380):
#     srkdata.calc_run_stats_to_database(i)

##################################################
# Diffuse Omega Only B0 and E0 for only Vary Time

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# r['Title'] = '3D Diffuse, Only B0 and E0 Field Vary Time'
# s['Use2D'] = 0
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 5e6
#
#
# for i in srkmisc.even_sample_over_log(0.1,1000,6):
#     s['TimeLimit'] = i
#     r['NumTracksPer'] = int(1000000/i) #To get same integrated particle time
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro(run_id, s, r)
#     srkdata.run_macro_local(run_id)
#
# for i in range(5400,5406):
#     srkdata.run_macro_local(i)
#
# for i in xrange(5380, 5386):
#     srkdata.calc_run_stats_to_database(i)

# for i in xrange(5398, 5400):
#     srkdata.calc_run_stats_to_database(i)

# for i in range(5392,5400):
#     srkdata.calc_run_stats_to_database(i)

#Current ver d495d9829c4312265761c89436681c78e49b0fcf


#################################################
# Specular Omega Only B0 and E0 for only long time
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 1000
# r['Title'] = '3D Specular, Only B0 and E0 Field Vary EPS'
# s['Use2D'] = 0
# s['DiffuseReflectionProb'] = 0
# s['E0FieldStrength'] = 5e6
# s['TimeLimit'] = 100
#
# for i in srkmisc.even_sample_over_log(1e-9,1e-6,6):
#     s['EPSAbs'] = i
#     s['EPSRel'] = i
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro(run_id, s, r)
#     srkdata.run_macro_local(run_id)

# for i in range(5412,5418):
#     srkdata.calc_run_stats_to_database(i)

################################################
# Diffuse Omega Only B0 and E0 for only long time
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 1000
# r['Title'] = '3D Diffuse, Only B0 and E0 Field Vary EPS Alt Stepping'
# s['Use2D'] = 0
# s['DiffuseReflectionProb'] = 1
# s['E0FieldStrength'] = 5e6
# s['TimeLimit'] = 100
# s['UseAltStepping'] = 1
#
# for i in srkmisc.even_sample_over_log(1e-9,1e-6,6):
#     s['EPSAbs'] = i
#     s['EPSRel'] = i
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro(run_id, s, r)
#     srkdata.run_macro_local(run_id)

# for i in range(5418,5424):
#     srkdata.calc_run_stats_to_database(i)

##################################################
# Specular Omega Only B0 and E0 for only Vary Time

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['Title'] = '3D Specular, Only B0 and E0 Field Vary Time'
# s['Use2D'] = 0
# s['DiffuseReflectionProb'] = 0
# s['E0FieldStrength'] = 7e7
#
#
# for i in srkmisc.even_sample_over_log(0.1,1000,6):
#     s['TimeLimit'] = i
#     r['NumTracksPer'] = int(1000000/i) #To get same integrated particle time
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro(run_id, s, r)
#     srkdata.run_macro_local(run_id)

# for i in range(5441,5442):
#         srkdata.calc_run_stats_to_database(i)

###################################################
## 3D simulation of linear gradient

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'No Grav ideal of Grav Depolarizaiton paper, With E'
# s['Use2D'] = 0
# s['TimeLimit'] = 180
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 1e6
#
# s['MeanVel'] = 5
#
# run_ids = []
# for gradient in srkmisc.even_sample_over_log(5e-8,5e-7,6):
#     s['BGradFieldStrength']=gradient
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro(run_id, s, r)
#     srkdata.run_macro_local(run_id)
#
# for i in xrange(4820, 4952):
#     srkdata.calc_run_stats_to_database(i)

####
# Longish dipole run - now with random seeds
##
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmegaSame'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Dipole with PA same tracks via same seed for each deltaOmega'
# s['E0FieldStrength'] = 5e5
# s['TrackFilePath'] = "!dynamic"
#
# rid_list = []
# dist_range = np.arange(.1, .5, .1)
# for dip_str in srkmisc.even_sample_over_log(1e-18, 1e-13, 6):
#     s['DipoleFieldStrength'] = dip_str
#     for dist in dist_range:
#         s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - dist)
#         rid_list += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# rid_chunks = [rid_list[x:x+len(dist_range)] for x in xrange(0, len(rid_list), len(dist_range))]
# for i in rid_chunks:
#     srkdata.make_macro_mult_from_database(i)
#     srkdata.run_mult_macro_local(i)
#
# for i in range(5460,5484):
#     srkdata.calc_run_stats_to_database(i)

###################################################
## 3D simulation of linear gradient

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'No grav ideal of Grav Depolarization paper'
# s['Use2D'] = 0
# s['TimeLimit'] = 180
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 1e6
#
# s['GyromagneticRatio'] = "1.83247172e8"
# s['MeanVel'] = 5

# run_ids = []
# for gradient in np.linspace(0, 800*1e-12*100, num=6):
#     s['BGradFieldStrength'] = gradient
#     # run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     # srkdata.make_macro(run_id, s, r)
#     # srkdata.run_macro_local(run_id)
#     srkdata.run_on_optima(s,r)

# for i in xrange(5490,5496):
#     srkdata.run_macro_optima(i)
# for i in xrange(5374, 5380):
#     srkdata.calc_run_stats_to_database(i)

###################################################
## 2D simulation of linear gradient - UCN

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'No grav ideal of Grav Depolarization paper 2D'
# s['Use2D'] = 1
# s['TimeLimit'] = 180
# s['DiffuseReflectionProb'] = 1.
# s['E0FieldStrength'] = 1e6
#
# s['GyromagneticRatio'] = "1.83247172e8"
# s['MeanVel'] = 5
#
# run_ids = []
# for gradient in np.linspace(0, 800*1e-12*100, num=6):
#     s['BGradFieldStrength'] = gradient
#     srkdata.run_on_optima(s,r)


# for i in xrange(5484, 5502):
#     srkdata.calc_run_stats_to_database(i)

###################################################
## 3D simulation of linear gradient

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Intrinsic T2, Vary Vel'
# s['Use2D'] = 0
# s['TimeLimit'] = 180
# s['DiffuseReflectionProb'] = 0
# s['E0FieldStrength'] = 0
#
# s['GyromagneticRatio'] = "1.83247172e8"
# s['MeanVel'] = 0.5
# s['BGradFieldStrength']=10/(0.01*1e12)
#
# run_ids = []
# for velocity in np.linspace(.5, 2, num=6):
#     s['BGradFieldStrength'] = gradient
#     # run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     # srkdata.make_macro(run_id, s, r)
#     # srkdata.run_macro_local(run_id)
#     srkdata.run_on_optima(s,r)



###################################################
## Let's make some mass runs

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Radius'
#
# run_ids = []
# for x in np.linspace(0.1, 1., num = 10):
#     s['ChamberRadius'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Height'
#
# run_ids = []
# for x in np.linspace(0.1, 1., num = 10):
#     s['ChamberHeight'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Height'
#
# run_ids = []
# for x in np.linspace(0., 1., num = 11):
#     s['DiffuseReflectionProb'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary BField'
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(1.e-7, 1.e-5, 10):
#     s['B0FieldStrength'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Efield'
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(1.e5, 1.e7, 10):
#     s['E0FieldStrength'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Time'
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(1, 1000, 10):
#     s['TimeLimit'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary EPS'
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(1e-5, 1e-9, 5):
#     s['EPSAbs'] = x
#     s['EPSRel'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)


# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Vel'
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(0.5, 200, 90):
#     s['MeanVel'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# for i in srkmisc.chunk_list(run_ids, 9):
#     srkdata.make_macro_mult_from_database(i)
#     srkdata.run_mult_macro_optima(i)

# for i in xrange(5520, 5675):
#     srkdata.calc_run_stats_to_database(i)

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Efield, No B'
# s['B0FieldStrength']=0
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(1.e5, 1.e7, 10):
#     s['E0FieldStrength'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# for i in run_ids:
#     srkdata.make_macro_from_database(i)
#     srkdata.run_macro_local(i)

###################################################
## Let's make some mass runs
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Radius'
# s['GyromagneticRatio']=1.83247172e8
#
# run_ids = []
# for x in np.linspace(0.1, 1., num = 10):
#     s['ChamberRadius'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Height'
# s['GyromagneticRatio']=1.83247172e8
#
# run_ids = []
# for x in np.linspace(0.1, 1., num = 10):
#     s['ChamberHeight'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Height'
# s['GyromagneticRatio']=1.83247172e8
#
# run_ids = []
# for x in np.linspace(0., 1., num = 11):
#     s['DiffuseReflectionProb'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary BField'
# s['GyromagneticRatio']=1.83247172e8
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(1.e-7, 1.e-5, 10):
#     s['B0FieldStrength'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Efield'
# s['GyromagneticRatio']=1.83247172e8
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(1.e5, 1.e7, 10):
#     s['E0FieldStrength'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Time'
# s['GyromagneticRatio']=1.83247172e8
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(1, 1000, 10):
#     s['TimeLimit'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary EPS'
# s['GyromagneticRatio']=1.83247172e8
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(1e-5, 1e-9, 5):
#     s['EPSAbs'] = x
#     s['EPSRel'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# srkdata.make_macro_mult_from_database(run_ids)
# srkdata.run_mult_macro_optima(run_ids)
#
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'd495d9829c4312265761c89436681c78e49b0fcf'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Vel'
# s['GyromagneticRatio']=1.83247172e8
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(0.5, 200, 90):
#     s['MeanVel'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# for i in srkmisc.chunk_list(run_ids, 9):
#     srkdata.make_macro_mult_from_database(i)
#     srkdata.run_mult_macro_optima(i)

# for i in xrange(5675, 5842):
#     srkdata.calc_run_stats_to_database(i)


##################################
## 'Maxwell profiles: Temperature'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Temperature'
# r['SRKVersion'] = 'e7418ae18139be18a21f468ee29f838ba9c1f733'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
#
#
# for x in np.linspace(77, 300, num = 6):
#     s['VelProfHistPath'] = '!'+str(x)
#     # rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

# run_ids = range(5842, 5848)
# for rid in run_ids:
#     srkdata.run_macro_local(rid)

# for i in xrange(5845, 5848):
#     srkdata.calc_run_stats_to_database(i)

##################################
## 'Maxwell profiles: Vary Temperature with Linear Gradient'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary Temperature with linear gradient'
# r['SRKVersion'] = '81de8031a61f34f84d5616d0e0fbfcc2beff137d'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# #
# s['BGradFieldStrength']=1.e-12*100.
#
#
# for x in np.linspace(77, 300, num = 6):
#     s['VelProfHistPath'] = '!'+str(x)
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

##################################
## 'Maxwell profiles: Vary linear gradient with 300 K'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary linear gradient with 300 K'
# r['SRKVersion'] = '81de8031a61f34f84d5616d0e0fbfcc2beff137d'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# #
# s['VelProfHistPath'] = '!300.'
#
# for x in srkmisc.even_sample_over_log(1e-8, 1e-3, 6):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)


##################################
## 'Maxwell profiles: Vary B Field with 300 K'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary B Field with 300 K'
# r['SRKVersion'] = '81de8031a61f34f84d5616d0e0fbfcc2beff137d'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# #
# s['VelProfHistPath'] = '!300.'
#
# for x in srkmisc.even_sample_over_log(1e-8, 1e-3, 6):
#     s['B0FieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)

##################################
## 'Maxwell profiles: Vary E Field with 300 K'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary E Field with 300 K'
# r['SRKVersion'] = '81de8031a61f34f84d5616d0e0fbfcc2beff137d'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# #
# s['VelProfHistPath'] = '!300.'
#
# for x in srkmisc.even_sample_over_log(1e4, 1e9, 6):
#     s['E0FieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_local(rid)

# for i in xrange(5866, 5878):
#     srkdata.calc_run_stats_to_database(i)


##################################
## 'Maxwell profiles: Vary linear gradient with 3.5 K'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary linear gradient with UCN at 3.5 mK'
# r['SRKVersion'] = 'ef94d849373d78367e3e17a4a087b7ca8de168e4'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# #
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
#
# for x in srkmisc.even_sample_over_log(1e-14, 1e-3, 6):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_local(rid)

##################################
## 'Maxwell profiles: Vary linear gradient with 3.5 mK'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary linear gradient with UCN at 3.5 mK'
# r['SRKVersion'] = 'ef94d849373d78367e3e17a4a087b7ca8de168e4'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# #
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
#
# for x in srkmisc.even_sample_over_log(1e-14, 1e-3, 6):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_local(rid)


###################################################
## 2D simulation of no gradients
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ef94d849373d78367e3e17a4a087b7ca8de168e4'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = '2D Specular, 100s'
# s['Use2D'] = 1
# s['TimeLimit'] = 100.
# s['DiffuseReflectionProb'] = 0.
#
# # run_ids = []
# # run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 60)
#
# run_ids=range(5944,6004)
# for x in srkmisc.chunk_list(run_ids,5):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_optima(x)

# for i in xrange(5884, 6004):
#     srkdata.calc_run_stats_to_database(i)



##################################################
# 2D simulation of no gradients
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ef94d849373d78367e3e17a4a087b7ca8de168e4'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = '2D Diffuse, 1s'
# s['Use2D'] = 1
# s['TimeLimit'] = 1.
# s['DiffuseReflectionProb'] = 1.
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 60)
#
# # run_ids=range(5944,6004)
# for x in srkmisc.chunk_list(run_ids,3):
#     # srkdata.make_macro_mult_from_database(x)
#     srkdata.run_macro_local(x)
#
# r['Title'] = '2D Specular, 1s'
# s['DiffuseReflectionProb'] = 0.
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 60)

# run_ids=range(6004,6124)
# for x in srkmisc.chunk_list(run_ids,6):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)

# for rid in run_ids:
#     srkdata.calc_run_stats_to_database(rid)

##################################################
# 2D simulation of no gradients
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
# r['SRKVersion'] = 'ef94d849373d78367e3e17a4a087b7ca8de168e4'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = '2D Diffuse, Vary B'
# s['Use2D'] = 1
#
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(1.e-7, 1.e-5, 10):
#     s['B0FieldStrength'] = x
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]

# run_ids=range(6124, 6134)[0:6]
# for i in run_ids:
#     srkdata.make_macro_from_database(i)
#     srkdata.run_macro_local(i)

# run_ids=range(6124, 6134)
# for rid in run_ids:
#     srkdata.calc_run_stats_to_database(rid)

###################
## Double check with constant stepper
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = 'ef94d849373d78367e3e17a4a087b7ca8de168e4'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Const Step Size'
# s['ConstStepper']=1
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(1e-4, 1, 5):
#     s['InitialStepSize'] = x
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)

# run_ids=range(6134, 6139)
# for i in run_ids:
#     # srkdata.run_macro_local(i)
#     srkdata.calc_run_stats_to_database(i)

#####
##Testttttt
####
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# # r['SRKVersion'] = 'TEST No Theta 2'
# # r['Title'] = 'TEST No Theta 2'
# # r['Date'] = today.strftime('%m/%d/%y')
# # r['RunType'] = 'parOnly'
# # r['NumTracksPer'] = 10000
#
# # run_id= srkdata.add_to_database(srkdata.merge_dicts(s, r))
# # srkdata.make_macro_from_database(run_id)
# # srkdata.run_macro_local(run_id)
# thedict=srkanalysis.calc_run_stats(6140)
# print "Phi:", thedict['Par_PhiMean']
# print "Kurtosis:", thedict['Par_PhiKurtosis']
# print "Tsallis Power:", thedict['Par_PhiTsallisPower']


#######
## Rerun UCN at various gradients
# run_ids=range(5878, 5884)
# for i in run_ids:
#     # srkdata.run_macro_local(i)
#     srkdata.calc_run_stats_to_database(i)


###################
## Vary Initial Theta

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '5bea8d2ccce715a627b4c75fcba0255ed9efffe3'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary initial theta'
#
#
# for x in srkmisc.even_sample_over_log(1e-9, 1e-2, 8):
#     s['ThetaStart'] = x
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)

# run_ids = range(6141, 6149)
# for run_id in run_ids:
#     # srkdata.make_macro_from_database(run_id)
#     # srkdata.run_macro_optima(run_id)
#     srkdata.calc_run_stats_to_database(run_id)


##################################
## 'Maxwell profiles: Vary linear gradient with 3.5 mK'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary linear gradient with UCN at 3.5 mK'
# r['SRKVersion'] = '5bea8d2ccce715a627b4c75fcba0255ed9efffe3'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 100000
# #
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
#
# for x in srkmisc.even_sample_over_log(1e-14, 1e-3, 5):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)


##################################
## 'Maxwell profiles: Vary diffusivity  with 3.5 mK'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary diffusivity with UCN at 3.5 mK'
# r['SRKVersion'] = '5bea8d2ccce715a627b4c75fcba0255ed9efffe3'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 100000
# #
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
#
# for x in np.linspace(0., 1., num = 11):
#     s['DiffuseReflectionProb'] = x
#     rid = srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)


##################################
## 'Maxwell profiles: Vary Theta Start with 3.5 mK'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary Theta Start with UCN at 3.5 mK'
# r['SRKVersion'] = '5bea8d2ccce715a627b4c75fcba0255ed9efffe3'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 100000
# #
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
#
# for x in srkmisc.even_sample_over_log(1e-4, 1e-1, 8):
#     s['ThetaStart'] = x
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_local(run_id)

# run_ids = range(6165, 6173)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)


# ###################
# ## Vary E0 angle
# #
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '406df5d43344aa1209665f7a3a861489d4686065'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary E0 angle'
#
#
# for x in srkmisc.even_sample_over_log(1e-4, 1e-1, 6):
#     s['E0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(x),np.cos(x))
#     # print s['E0FieldDirection']
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_local(run_id)

# run_ids = range(6141, 6149)
# for run_id in run_ids:
#     # srkdata.make_macro_from_database(run_id)
#     # srkdata.run_macro_optima(run_id)
#     srkdata.calc_run_stats_to_database(run_id)

###################
## Vary B0 angle
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '406df5d43344aa1209665f7a3a861489d4686065'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary B0 angle'
#
#
# for x in srkmisc.even_sample_over_log(1e-4, 1e-1, 6):
#     s['B0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(x),np.cos(x))
#     # print s['E0FieldDirection']
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_local(run_id)

# run_ids = range(6173, 6185)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

#

##################################
## 'Maxwell profiles: Vary linear E gradient with 3.5 mK'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary linear electric gradient with UCN at 3.5 mK'
# r['SRKVersion'] = '5bea8d2ccce715a627b4c75fcba0255ed9efffe3'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 100000
# #
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
#
# for x in srkmisc.even_sample_over_log(1e-14*(1.e6/1.e-6), 1e-3*(1.e6/1.e-6), 12):
#     s['EGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)

# run_ids = range(6185, 6197)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################
## 'Maxwell profiles: Vary linear E gradient with 3.5 mK'
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary linear electric gradient with UCN at 3.5 mK'
# r['SRKVersion'] = '5bea8d2ccce715a627b4c75fcba0255ed9efffe3'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 100000
# #
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
#
# for x in srkmisc.even_sample_over_log(1e-14, 1e-2, 12):
#     s['EGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)

##################################################
#2D simulation with linear gradient 100s

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = '2D Diffuse, 100s'
# s['Use2D'] = 1
# s['TimeLimit'] = 100
# s['DiffuseReflectionProb'] = 1.
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 60)
#
# for x in srkmisc.chunk_list(run_ids,6):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)

# run_ids = range(6197, 6209)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################
## 'Maxwell profiles: No Linear Gradient E gradient with 3.5 mK'
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: No Linear Gradient UCN at 3.5 mK'
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# #
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
#
#
# rid=srkdata.make_macro_and_add_to_database(s, r)
# srkdata.run_macro_local(rid)

# run_ids = range(6270, 6271)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################
## 'Maxwell profiles: No linear E gradient with 3.5 mK'
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: No Linear Gradient Hg at 300k'
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# #
# s['VelProfHistPath'] = '!300'
#
#
# rid=srkdata.make_macro_and_add_to_database(s, r)
# srkdata.run_macro_local(rid)

# run_ids = range(6209, 6267)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################################
#2D simulation with linear gradient 100s

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = '2D Diffuse, 100s with Linear Gradient'
# s['Use2D'] = 1
# s['TimeLimit'] = 100
# s['DiffuseReflectionProb'] = 1.
# s['BGradFieldStrength']=1e-10
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 60)
#
# for x in srkmisc.chunk_list(run_ids,5):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_optima(x)

# run_ids = range(6271, 6272)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################
## 'Maxwell profiles: No Gradientwith 3.5 mK'
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: No Linear Gradient Hg at 300k'
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# #
# s['VelProfHistPath'] = '!300'


# rid=srkdata.make_macro_and_add_to_database(s, r)
# srkdata.run_macro_local(6271)
#
# run_ids = range(6269, 6331)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################
## 'Maxwell profiles: Vary Temperature with Linear Gradient'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary Temperature with only E field'
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 100000
# #
#
#
# for x in np.linspace(3.5e-3, 300, num = 16):
#     s['VelProfHistPath'] = '!'+str(x)
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

##################################################
#2D simulation with linear gradient 100s

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = '2D Diffuse, 100s with Linear Gradient No E'
# s['Use2D'] = 1
# s['TimeLimit'] = 100
# s['DiffuseReflectionProb'] = 1.
# s['BGradFieldStrength']=1e-10
# s['E0FieldStrength']=0
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 60)
#
# run_ids = range(6348,6408)
# for x in srkmisc.chunk_list(run_ids,10):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)
#
# run_ids = range(6348,6408)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

# run_ids = range(6331, 6348)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################
## 'Maxwell profiles: Vary linear E gradient with 300'
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Maxwell profiles: Vary linear electric gradient with Hg at 300k'
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 100000
# #
# s['VelProfHistPath'] = '!300'
#
# for x in srkmisc.even_sample_over_log(1, 1e8, 8):
#     s['EGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)

###################
## Vary B0 angle

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# r['Title'] = 'Vary B0 angle'
#
#
# for x in srkmisc.even_sample_over_log(1e-4, 1e-1, 8):
#     s['B0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(x),np.cos(x))
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)

#########
## Vary Time
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Time 10 times less gyro'
# s['GyromagneticRatio']=-4845788.39927
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(10, 1000, 6):
#     s['TimeLimit'] = x
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_local(run_id)

# run_ids = range(6408, 6430)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

########
# Vary Time
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary Time 10 times more gyro'
# s['GyromagneticRatio']=-484578839.927
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(10, 1000, 6):
#     s['TimeLimit'] = x
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)


# ###################
# ## Vary E0 angle
# #
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# r['Title'] = 'Vary E0 angle UCN 3.5mK'
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
#
#
# for x in srkmisc.even_sample_over_log(1e-4, 1e-1, 6):
#     s['E0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(x),np.cos(x))
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)

###################
## Vary Initial Theta

# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = 'Mass Runs: Vary initial theta'
#
#
# for x in srkmisc.even_sample_over_log(1e-9, 1e-2, 8):
#     s['ThetaStart'] = x
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)


##################################
## 'Maxwell profiles: Vary linear gradient with 3.5 K'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Vary Linear Gradient with E angle 1 degree misalignment at 300K'
# r['SRKVersion'] = '83aaaefb27b5bd18b6671049797c77e5e9a5ea30'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
#
# s['VelProfHistPath'] = '!300'
# s['E0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(np.pi/180.),np.cos(np.pi/180.))
#
#
# for x in srkmisc.even_sample_over_log(1e-14, 1e-3, 8):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)


##################################
## 'Maxwell profiles: Vary linear gradient with 300 K No E'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Vary Linear Gradient 300K No E'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
#
#
# s['VelProfHistPath'] = '!300'
# s['E0FieldStrength']=0
#
#
# for x in srkmisc.even_sample_over_log(1e-12, 1e-7, 6):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_local(rid)


##################################
## 'Maxwell profiles: Vary linear gradient with 300 K No E'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = 'Vary Linear Gradient 300K No E'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
#6430
#
# s['VelProfHistPath'] = '!300'
# s['E0FieldStrength']=0
#
#
# for x in srkmisc.even_sample_over_log(1e-6, 1e-1, 6):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_local(rid)



##################################
## '2D 10xB0 Vary Omega'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = '2D 10xB0 Vary Omega'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
#
# s['B0FieldStrength']=1e-5
# s['Use2D']=1
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 60)
#
# for x in srkmisc.chunk_list(run_ids,4):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_optima(x)


# ##################################
# ## '2D Vary Linear Gradient B0=0'
# ##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = '2D Vary Linear Gradient'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
#
# s['B0FieldStrength']=0
# s['Use2D']=1
#
# for x in srkmisc.even_sample_over_log(1e-12, 1e-7, 6):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_local(rid)

##################################
## '2D Vary Linear Gradient E0=0'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = '2D Vary Linear Gradient E0=0'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
#
# s['E0FieldStrength']=0
# s['Use2D']=1
#
# for x in srkmisc.even_sample_over_log(1e-12, 1e-7, 6):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_local(rid)

#
# run_ids = range(6534, 6564)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################################
#2D simulation with linear gradient 100s
#
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# r['Title'] = '2D Diffuse, 100s with Linear Gradient No E High B'
# s['Use2D'] = 1
# s['BGradFieldStrength']=1e-10
# s['B0FieldStrength']=1e-3
# s['E0FieldStrength']=0
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .01, 1, 60)

# run_ids=range(6624,6684)
# for x in srkmisc.chunk_list(run_ids,10):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)


##################################
## '2D Vary B'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = '2D Vary B'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
# s['Use2D']=1
#
# run_ids = []
#
# for i in srkmisc.even_sample_over_log(1e-6, 1e-2, 60):
#     s['B0FieldStrength']=i
#     run_ids += [srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# for x in srkmisc.chunk_list(run_ids,4):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_optima(x)

##################################
##################################
# r['Title'] = 'Vary initial theta, larger angles'
#
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
#
#
# for x in np.linspace(0, 5, num = 10):
#     s['ThetaStart'] = x*np.pi/180.
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)

##################################
##################################
# r['Title'] = 'Vary B0 angle, larger angles'
#
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
#
#
# for x in np.linspace(0, 5, num = 10):
#     s['B0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(x*np.pi/180.),np.cos(x*np.pi/180.))
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_local(run_id)

# run_ids = range(6694, 6704)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################
##################################
# r['Title'] = 'Vary E0 angle, larger angles'
#
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
#
#
# for x in np.linspace(0, 5, num = 10):
#     s['E0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(x*np.pi/180.),np.cos(x*np.pi/180.))
#     run_id = srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_local(run_id)

# run_ids = range(6462, 6522)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################
## '2D Vary Linear Gradient E0=0'
##################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = '2D Vary Linear Gradient E0=0, UCN'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
#
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
# s['MeanVel']=5
#
# s['E0FieldStrength']=0
# s['Use2D']=1
#
# for x in srkmisc.even_sample_over_log(1e-12, 1e-7, 6):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_local(rid)



# for run_id in range(6564,6714):
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)

# run_ids = range(6564, 6714)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

#################################
# '2D Vary Linear Gradient E0=0'
#################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = '2D Vary Linear Gradient E0=0, B=10 microT'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
#
# s['E0FieldStrength']=0
# s['Use2D']=1
# s['B0FieldStrength']=1e-5
#
# for x in srkmisc.even_sample_over_log(1e-12, 1e-7, 6):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)

#################################
# '2D Vary Linear Gradient E0=0,B=100 microT'
#################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = '2D Vary Linear Gradient E0=0, B=100 microT'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
#
# s['E0FieldStrength']=0
# s['Use2D']=1
# s['B0FieldStrength']=1e-4
#
# for x in srkmisc.even_sample_over_log(1e-12, 1e-7, 6):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)



#################################
# '2D Vary Linear Gradient E0=0
#################################
# s = srkdata.default_srk_settings()
# r = srkdata.default_run_settings()
#
# r['Title'] = '2D Vary Linear Gradient E0=0'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
#
# s['E0FieldStrength']=0
# s['Use2D']=1
#
# for x in srkmisc.even_sample_over_log(1e-12, 1e-7, 12):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)
#

#


##################################################
# r['Title'] = '2D Diffuse, 100s with Linear Gradient No E'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['BGradFieldStrength']=1e-7
# s['E0FieldStrength']=0
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 60)
#
# for x in srkmisc.chunk_list(run_ids,10):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)



##################################################
# r['Title'] = '2D Diffuse, 100s with E=1e8'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['E0FieldStrength']=1e8
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 60)
#
# for x in srkmisc.chunk_list(run_ids,10):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)

##################################################
# r['Title'] = '2D Diffuse, 100s with Linear Gradient No E'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['BGradFieldStrength']=1e-8
# s['E0FieldStrength']=0
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 60)
#
# for x in srkmisc.chunk_list(run_ids,10):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)


#################################
# r['Title'] = '2D Vary Linear Gradient E0=0'
#
#
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D']=1
#
# run_ids = []
# for x in srkmisc.even_sample_over_log(.235, 40., 60):
#     s['ChamberRadius'] = x
#     run_ids +=[srkdata.add_to_database(srkdata.merge_dicts(s, r))]
#
# for x in srkmisc.chunk_list(run_ids,10):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)




################################################################
# r['Title'] = '3D Specular, 100s'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['DiffuseReflectionProb'] = 0
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, .1, 10, 60)
#
# for x in srkmisc.chunk_list(run_ids,12):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_optima(x)

################################################################
# r['Title'] = '2D Diffuse, 100s with Linear Gradient No E'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['BGradFieldStrength']=1e-7
# s['E0FieldStrength']=0
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, 10, 100, 10)
#
# for x in run_ids:
#     srkdata.make_macro_from_database(x)
#     srkdata.run_macro_optima(x)

################################################################
# r['Title'] = '2D Diffuse, 1000s with Linear Gradient No E'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['BGradFieldStrength']=1e-10
# s['E0FieldStrength']=0
# s['TimeLimit']=1000
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, 0.1, 15, 6)
#
# for x in run_ids:
#     srkdata.make_macro_from_database(x)
#     srkdata.run_macro_local(x)

# #################################################################
# r['Title'] = 'Vary E0 angle, larger angles'
#
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 10):
#     s['E0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(x*np.pi/180.),np.cos(x*np.pi/180.))
#     run_ids.append(srkdata.add_to_database(srkdata.merge_dicts(s, r)))
#
# for x in srkmisc.chunk_list(run_ids,2):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_local(x)

#################################################################
# r['Title'] = 'Vary B0 angle, larger angles'
#
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 10):
#     s['B0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(x*np.pi/180.),np.cos(x*np.pi/180.))
#     run_id=srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)


# #################################################################
# r['Title'] = 'Vary E0 angle, larger angles, with Linear Gradient'
#
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=0
# s['BGradFieldStrength']=1e-7
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 10):
#     s['E0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(x*np.pi/180.),np.cos(x*np.pi/180.))
#     run_ids.append(srkdata.add_to_database(srkdata.merge_dicts(s, r)))
#
# for x in srkmisc.chunk_list(run_ids,2):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_optima(x)

#################################################################
# r['Title'] = 'Vary B0 angle, larger angles, with Linear Gradient'
#
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=0
# s['BGradFieldStrength']=1e-7
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 10):
#     s['B0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(x*np.pi/180.),np.cos(x*np.pi/180.))
#     run_ids.append(srkdata.add_to_database(srkdata.merge_dicts(s, r)))
#
# for x in srkmisc.chunk_list(run_ids,2):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_optima(x)

################################################################3
# r['Title'] = 'Vary polarization angle, larger angles, with Linear Gradient'
#
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=0
# s['BGradFieldStrength']=1e-7
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 10):
#     s['ThetaStart'] = x*np.pi/180.
#     run_ids.append(srkdata.add_to_database(srkdata.merge_dicts(s, r)))
#
# for x in srkmisc.chunk_list(run_ids,2):
#     srkdata.make_macro_mult_from_database(x)
#     srkdata.run_mult_macro_optima(x)

################################################################
# r['Title'] = '2D Diffuse, with moderate Linear Gradient No E'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['BGradFieldStrength']=1e-8
# s['E0FieldStrength']=0
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, 0.1, 100, 7)
#
# for x in run_ids:
#     srkdata.make_macro_from_database(x)
#     srkdata.run_macro_local(x)

#################################################################
# r['Title'] = '2D Diffuse, with moderate E'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['E0FieldStrength']=1e7
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, 0.1, 100, 7)
#
# for x in run_ids:
#     srkdata.make_macro_from_database(x)
#     srkdata.run_macro_local(x)

# run_ids = range(7060, 7070)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

#New version: 965df7165dc68b34d9effcead0a5cf7503df1986

#################################################################
# r['Title'] = 'Vary Mean Free Path'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 10000
#
# s['Use2D']=1
# s['BGradFieldStrength'] = 1e-7
# s['MeanVel']=200
#
#
# run_ids=[]
# for x in np.linspace(0.001, 0.05, num = 6):
#     s['MeanFreePath'] = x
#     run_id=srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     # srkdata.run_macro_local(run_id)

#################################################################
# r['Title'] = 'Vary Time Limit - 3D Vel Prof'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=0
# s['BGradFieldStrength']=1e-7
#
# for x in [1.,10.,25.,50.,100.,150.]:
#     s['TimeLimit'] = x
#     run_id=srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_local(run_id)


#################################################################
# r['Title'] = '2D Diffuse, with moderate E'
# r['SRKVersion'] = '6e812fba7a61c9037c8eb6e2983348ac85748d32'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['E0FieldStrength']=1e8
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, 0.1, 100, 7)
#
# for x in run_ids:
#     srkdata.make_macro_from_database(x)
#     srkdata.run_macro_local(x)

#################################################################
# r['Title'] = 'Vary Time Limit with linear gradient - 3D UCN'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'deltaOmega'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!3.5e-3'
# s['E0FieldStrength']=0
# s['BGradFieldStrength']=1e-7
#
# for x in [1.,10.,25.,50.,100.,150.]:
#     s['TimeLimit'] = x
#     run_id=srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_local(run_id)

###########################################################
# r['Title'] = '2D Diffuse, 100s with Linear Gradient No E'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['BGradFieldStrength']=1e-10
# s['E0FieldStrength']=0
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, 10, 100, 10)

# run_ids=range(7149,7159)
# for x in run_ids:
#     srkdata.make_macro_from_database(x)
#     srkdata.run_macro_local(x)

###########################################################
# r['Title'] = '2D Diffuse, 100s with  E'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['E0FieldStrength']=1e6
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, 10, 100, 10)

# run_ids=range(1,7169)
# for x in run_ids:
#     srkdata.make_macro_from_database(x)
#     srkdata.run_macro_optima(x)

###########################################################
# r['Title'] = '2D Diffuse, 100s with higher E'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['E0FieldStrength']=100e6
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, 10, 100, 10)
#
# # run_ids=range(7159,7169)
# for x in run_ids:
#     srkdata.make_macro_from_database(x)
#     srkdata.run_macro_optima(x)

#


#################################################################
# r['Title'] = 'Vary Time Limit - 3D Vel Prof - Local'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=0
# s['BGradFieldStrength']=1e-7
#
# for x in [1.,10.,25.,50.,100.,150.]:
#     s['TimeLimit'] = x
#     run_id=srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)

#################################################################
# r['Title'] = 'Vary Time Limit - 3D Vel Prof - E0'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
#
#
# for x in [1.,10.,25.,50.,100.,150.]:
#     s['TimeLimit'] = x
#     run_id=srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_local(run_id)

# run_ids = range(7190, 7197)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################
# r['Title'] = 'Vary Temperature with Constant Electric'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
#
# temperatures=np.array([3.5e-3])
# temperatures= np.append(temperatures,np.linspace(77, 300, num = 6))
#
# for x in temperatures:
#     s['VelProfHistPath'] = '!'+str(x)
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

# for i in xrange(5845, 5848):
#     srkdata.calc_run_stats_to_database(i)

##################################
# r['Title'] = 'Vary Temperature with B Gradient and no E Field'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['E0FieldStrength']=0
# s['BGradFieldStrength']=1e-7
#
# temperatures=np.array([3.5e-3])
# temperatures= np.append(temperatures,np.linspace(77, 300, num = 6))
#
# for x in temperatures:
#     s['VelProfHistPath'] = '!'+str(x)
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

##########################################
# r['Title'] = 'Vary Time Limit - 3D Vel Prof - E0'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
#
#
# for x in [1.,10.,25.,50.,100.,150.]:
#     s['TimeLimit'] = x
#     run_id=srkdata.add_to_database(srkdata.merge_dicts(s, r))
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_local(run_id)

# lines = [
#          range(7070, 7078)+range(6702,6704),
#          range(7060, 7070),
#          [6684,6147]+range(6685,6694)]
#
# run_ids = [item for sublist in lines for item in sublist]
# run_ids=range(7143, 7149)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

################################################################
# r['Title'] = 'Vary polarization angle, E0'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=0
# s['BGradFieldStrength']=1e-7
#
# run_ids=[]
# for x in np.linspace(0, 1, num = 10):
#     s['ThetaStart'] = x*np.pi/180.
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

################################################################
# r['Title'] = 'Vary Temperature with Constant Electric'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
#
# temperatures=srkmisc.even_sample_over_log(1e-4, 4, 6)
#
# for x in temperatures:
#     s['VelProfHistPath'] = '!'+str(x)
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

# run_ids=range(1, 7127)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

################################################################
# r['Title'] = 'Vary Temperature with Field Gradient'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['E0FieldStrength']=0
# s['BGradFieldStrength']=1e-10
#
# temperatures=srkmisc.even_sample_over_log(1e-4, 4, 6)
#
# for x in temperatures:
#     s['VelProfHistPath'] = '!'+str(x)
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)
#
# run_ids=range(7238, 7250)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

################################################################
# r['Title'] = 'Vary E Field with Linear Gradient UCN'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['B0FieldStrength']=1e-6
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
# s['BGradFieldStrength'] = 1e-7
#
# y=srkmisc.even_sample_over_log(1, 1e9, 4)
# for x in y:
#     s['E0FieldStrength']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

# run_ids=range(7245, 7265)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

###############################################################
# r['Title'] = 'Vary Time Limit with Weak Gradient UCN'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['B0FieldStrength']=1e-6
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
# s['BGradFieldStrength'] = 1e-10
#
# y=[1.,10.,25.,50.,100.,150.]
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

# run_ids=range(7265, 7271)
# for run_id in run_ids:
#     srkdata.run_macro_optima(run_id)

# ###############################################################
# r['Title'] = 'Vary Time Limit with Strong Gradient Hg'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['B0FieldStrength']=1e-6
# s['VelProfHistPath'] = '!293K'
# s['BGradFieldStrength'] = 1e-7
#
# y=[1.,10.,25.,50.,100.,150.]
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

# run_ids=range(7265, 7289)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

###############################################################
# r['Title'] = 'Vary Time Limit with E0 UCN'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
#
# y=[1.,10.,25.,50.,100.,150.]
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

###############################################################
# r['Title'] = 'Vary Time Limit with strong gradient only UCN'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
# s['BGradFieldStrength'] = 1e-7
# s['E0FieldStrength']=0
#
# y=[1.,10.,25.,50.,100.,150.]
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

###############################################################
# r['Title'] = 'Vary Time Limit with weak gradient only UCN'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
# s['BGradFieldStrength'] = 1e-10
# s['E0FieldStrength']=0
#
# y=[1.,10.,25.,50.,100.,150.]
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

# run_ids=range(7289, 7295)
# for run_id in run_ids:
#     srkdata.run_macro_optima(run_id)

###############################################################
# r['Title'] = 'Vary Time Limit with E0 UCN'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!3.5e-3'
# s['GyromagneticRatio']=1.83247172e8
# s['Mass']=1.674927471e-27
#
# y=[1.,10.,25.,50.,100.,150.]
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

################################################################
# r['Title'] = 'Vary polarization angle, E0 (for real)'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=1e6
# # s['BGradFieldStrength']=1e-7
#
# run_ids=[]
# for x in np.linspace(0, 1, num = 10):
#     s['ThetaStart'] = x*np.pi/180.
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

################################################################
# r['Title'] = 'Vary polarization angle, E0 (for real)'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=1e6
# # s['BGradFieldStrength']=1e-7
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 6):
#     s['ThetaStart'] = x*np.pi/180.
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)
#
################################################################
# r['Title'] = 'Vary E0 angle with E0'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=1e6
# # s['BGradFieldStrength']=1e-7
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 6):
#     y=x*np.pi/180.
#     s['E0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(y),np.cos(y))
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)


################################################################ Still to run
# r['Title'] = 'Vary B0 angle with E0'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=1e6
# # s['BGradFieldStrength']=1e-7
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 6):
#     y=x*np.pi/180.
#     s['B0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(y),np.cos(y))
#     rid=srkdata.add_to_database(srkdata.merge_dicts(s, r))

################################################################Still to run
# r['Title'] = 'Vary polarization angle, strong gradient'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-7
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 6):
#     s['ThetaStart'] = x*np.pi/180.
#     rid=srkdata.add_to_database(srkdata.merge_dicts(s, r))
#
################################################################Still to run
# r['Title'] = 'Vary E0 angle with strong gradient'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-7
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 6):
#     y=x*np.pi/180.
#     s['E0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(y),np.cos(y))
#     rid=srkdata.add_to_database(srkdata.merge_dicts(s, r))


################################################################ Still to run
# r['Title'] = 'Vary B0 angle with strong gradient'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-7
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 6):
#     y=x*np.pi/180.
#     s['B0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(y),np.cos(y))
#     rid=srkdata.add_to_database(srkdata.merge_dicts(s, r))

# run_ids=range(7317, 7317+16)
# for run_id in run_ids:
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)

# run_ids=range(7317+16, 7329+16+16)
# for run_id in run_ids:
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)



################################################################
# r['Title'] = 'Vary Time Limit with E0'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
#
# y=[1.,10.,25.,50.,100.,150.]
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

################################################################
# r['Title'] = 'Vary polarization angle, E0, higher stat '
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=1e6
#
# run_ids=[]
# for x in np.linspace(0.1, .9, num = 8):
#     s['ThetaStart'] = x*np.pi/180.
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

################################################################
# r['Title'] = 'Vary Time Limit with E0'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
#
# y=[1.,10.,25.,50.,100.,150.]
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)


#######################################################
# r['Title'] = 'Vary Time Limit with strong linear gradient only'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-7
# s['E0FieldStrength']=0
#
# y=[1.,10.,25.,50.,100.,150.]
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

#######################################################
# r['Title'] = 'Vary Time Limit with weak linear gradient only'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-10
# s['E0FieldStrength']=0
#
# y=[1.,10.,25.,50.,100.,150.]
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

###########################################################
# r['Title'] = '2D Diffuse, 100s with higher E'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['E0FieldStrength']=100e6
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, 0.05, 0.1, 8)
#
# # run_ids=range(7159,7169)
# for x in run_ids:
#     srkdata.make_macro_from_database(x)
#     srkdata.run_macro_optima(x)

###########################################################
# r['Title'] = '2D Diffuse, 100s with norm E'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['E0FieldStrength']=1e6
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, 0.05, 0.1, 8)
#
# # run_ids=range(7159,7169)
# for x in run_ids:
#     srkdata.make_macro_from_database(x)
#     srkdata.run_macro_optima(x)

###########################################################
# r['Title'] = '2D Diffuse, 100s with strong gradient'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
#
# s['Use2D'] = 1
# s['E0FieldStrength']=1e6
# s['BGradFieldStrength']=1e-7
#
# run_ids = []
# run_ids += srkdata.make_macros_steyerl_and_add_to_database(s, r, 0.05, 0.1, 8)
#
# # run_ids=range(7159,7169)
# for x in run_ids:
#     srkdata.make_macro_from_database(x)
#     srkdata.run_macro_optima(x)

# run_ids=range(7409, 7442)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)


###############################################################
# r['Title'] = 'Vary polarization angle, weak gradient, No E0'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-10
# s['E0FieldStrength']=0
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 6):
#     s['ThetaStart'] = x*np.pi/180.
#     rid=srkdata.add_to_database(srkdata.merge_dicts(s, r))

###############################################################
# r['Title'] = 'Vary E0 angle, weak gradient, No E0'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-10
# s['E0FieldStrength']=0
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 6):
#     y=x*np.pi/180.
#     s['E0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(y),np.cos(y))
#     rid=srkdata.add_to_database(srkdata.merge_dicts(s, r))


###############################################################
# r['Title'] = 'Vary B0 angle, weak gradient, No E0'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-10
# s['E0FieldStrength']=0
#
# run_ids=[]
# for x in np.linspace(0, 5, num = 6):
#     y=x*np.pi/180.
#     s['B0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(y),np.cos(y))
#     rid=srkdata.add_to_database(srkdata.merge_dicts(s, r))




##############################################################
# r['Title'] = 'Vary polarization angle, E0, in between angles'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=0
# s['E0FieldStrength']=1e6
#
# run_ids=[]
# for x in np.linspace(0.5, 4.5, num = 5):
#     s['ThetaStart'] = x*np.pi/180.
#     rid=srkdata.add_to_database(srkdata.merge_dicts(s, r))

# ##############################################################
# r['Title'] = 'Vary E0 angle, E0, in between angles'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=0
# s['E0FieldStrength']=1e6
#
# run_ids=[]
# for x in np.linspace(0.5, 4.5, num = 5):
#     y=x*np.pi/180.
#     s['E0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(y),np.cos(y))
#     rid=srkdata.add_to_database(srkdata.merge_dicts(s, r))

#
# ##############################################################
# r['Title'] = 'Vary B0 angle, E0, in between angles'
#
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=0
# s['E0FieldStrength']=1e6
#
# run_ids=[]
# for x in np.linspace(0.5, 4.5, num = 5):
#     y=x*np.pi/180.
#     s['B0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(y),np.cos(y))
#     rid=srkdata.add_to_database(srkdata.merge_dicts(s, r))

# run_ids=range(7433, 7442)
# for run_id in run_ids:
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_optima(run_id)

# run_ids=range(7442, 7442+6)
# for run_id in run_ids:
#     srkdata.make_macro_from_database(run_id)
#     srkdata.run_macro_local(run_id)

######################################################
# r['Title'] = 'Vary Time Limit with weak linear gradient only'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-10
# s['E0FieldStrength']=0
#
# y=srkmisc.even_sample_over_log(1e-6, 1e-1, 6)
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

######################################################
# r['Title'] = 'Vary Time Limit with strong linear gradient only'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-7
# s['E0FieldStrength']=0
#
# y=srkmisc.even_sample_over_log(1e-6, 1e-1, 6)
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

# ######################################################
# r['Title'] = 'Vary Time Limit with E0 only'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=0
# s['E0FieldStrength']=1e6
#
# y=srkmisc.even_sample_over_log(1e-6, 1e-1, 6)
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

######################################################
# r['Title'] = 'Vary Time Limit with strongE0 only'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=0
# s['E0FieldStrength']=1e8
#
# y=srkmisc.even_sample_over_log(1e-6, 1e-1, 6)
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

# run_ids=range(7466, 7473)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

######################################################
# r['Title'] = 'Vary Time Limit with strong E0 only and strong B0'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=0
# s['E0FieldStrength']=1e8
# s['B0FieldStrength']=1e8
#
# y=srkmisc.even_sample_over_log(1e-6, 1, 7)
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)

##################################
# r['Title'] = 'Vary Temperature with Constant Strong Electric'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# r['E0FieldStrength']=1e8
#
# temperatures=np.array([3.5e-3])
# temperatures= np.append(temperatures,np.linspace(77, 300, num = 6))
#
# for x in temperatures:
#     s['VelProfHistPath'] = '!'+str(x)
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

######################################################
# r['Title'] = 'Vary Time Limit with strongE0 only'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=0
# s['E0FieldStrength']=1e8
#
# y=[1.,10.,25.,50.,100.,150.]
# for x in y:
#     s['TimeLimit']=x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

##################################
# r['Title'] = 'Vary Temperature with weak field gradient'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['E0FieldStrength']=1e6
# s['BGradFieldStrength']=1e-10
#
# temperatures=np.linspace(77, 300, num = 6)
#
# for x in temperatures:
#     s['VelProfHistPath'] = '!'+str(x)
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)
#
# run_ids=range(7432, 7504)
# for run_id in run_ids:
#     srkdata.calc_run_stats_to_database(run_id)

##################################
# r['Title'] = 'Vary Temperature with Constant Strong Electric Fixed'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['E0FieldStrength']=1e8
#
# temperatures= np.linspace(77, 300, num = 6)
#
# for x in temperatures:
#     s['VelProfHistPath'] = '!'+str(x)
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

# lines = [
#          range(7393,7401)+range(5884, 5944)+range(7159,7169),
#          range(7385,7393)+range(6804, 6864)+range(7169,7179),
#          range(6534, 6564)+range(6348, 6408)+range(7149,7159),
#          range(7401,7409)+range(6744, 6804)+range(7044,7054)]
#
# for x in lines:
#     for run_id in x:
#         srkdata.calc_run_stats_to_database(run_id)

##################################
# r['Title'] = 'Vary Temperature with weak field gradient'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['E0FieldStrength']=0
# s['BGradFieldStrength']=1e-10
#
# temperatures=np.linspace(77, 300, num = 6)
#
# for x in temperatures:
#     s['VelProfHistPath'] = '!'+str(x)
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

#######################################################################
# r['Title'] = 'Standard many events strong gradient'
# r['SRKVersion'] = '965df7165dc68b34d9effcead0a5cf7503df1986'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# r['E0FieldStrength']=0
# s['VelProfHistPath'] = '!300'
# s['BGradFieldStrength']=1e-7
#
# for x in xrange(16):
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

# for run_id in range(7504,7526):
#     srkdata.calc_run_stats_to_database(run_id)

######################################################
# r['Title'] = 'Vary Time Limit with strong E0 only and strong B0'
# r['SRKVersion'] = 'Test'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 1000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=0
# s['E0FieldStrength']=1e6
# s['B0FieldStrength']=1e-6
#
# rid=srkdata.make_macro_and_add_to_database(s,r)
# srkdata.run_macro_local(rid)

# for run_id in range(7526,7527):
#     srkdata.calc_run_stats_to_database(run_id)

######################################################
# r['Title'] = "Bernd Hg Setup Test"
# r['SRKVersion'] = 'c33fb1b6c21c749f2a0560deb2328aae146d6c10'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-5
# s['E0FieldStrength']=0
# s['B0FieldStrength']=1e-6
# s['TimeLimit']=1
# 
# rid=srkdata.make_macro_and_add_to_database(s,r)
# srkdata.run_macro_local(rid)
# for run_id in range(7530,7531):
#     srkdata.calc_run_stats_to_database(run_id)

######################################################
# r['Title'] = "Bernd Hg Setup Test w Periodic"
# r['SRKVersion'] = '03191a62d5629382d26f9fd1d39e41c37291aa38'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-9
# s['E0FieldStrength']=0
# s['B0FieldStrength']=1e-6
# s['RecordAllSteps']=1
# s['PeriodicStopTime']=0.00333333
# s['TimeLimit']=100
#    
# rid=srkdata.make_macro_and_add_to_database(s,r)
# srkdata.run_macro_local(7532)
# for run_id in range(7531,7532):
#     print run_id
#     srkdata.calc_run_stats_to_database(run_id)

##############################################################
# Step tree calc
# results_file_path=srkdata.SRKSystems.results_dir+"Results_RID7532_P.root"
# txt_file_path=srkdata.SRKSystems.hists_dir+"data_steps_RID7352_P.txt"
# srkanalysis.calc_step_tree_to_txt(results_file_path, txt_file_path,0.00333333)
# print("--- %s seconds ---" % (time.time() - start_time))
######################################################
# r['Title'] = "Bernd Hg Setup Test w Periodic Fake Eq Motion"
# r['SRKVersion'] = '03191a62d5629382d26f9fd1d39e41c37291aa38'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=1e-9
# s['E0FieldStrength']=0
# s['B0FieldStrength']=1e-6
# s['RecordAllSteps']=1
# s['PeriodicStopTime']=0.00333333
# s['TimeLimit']=100
#     
# rid=srkdata.make_macro_and_add_to_database(s,r)
# srkdata.run_macro_local(7533)
# for run_id in range(7532,7534):
#     print run_id
#     srkdata.calc_run_stats_to_database(run_id)
######################################################
# r['Title'] = "Correct Bernd Hg Setup Test w Periodic"
# r['SRKVersion'] = '03191a62d5629382d26f9fd1d39e41c37291aa38'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['ChamberRadius']=0.025
# s['ChamberHeight']=0.10
# s['ChamberRotation'] = '0. 90. 0.'
# s['E0FieldStrength']=0
# s['B0FieldStrength']=1e-6
# s['RecordAllSteps']=1
# s['PeriodicStopTime']=0.00333333
# s['TimeLimit']=100
# gradients=srkmisc.even_sample_over_log(1e-5, 1e-9, 5)
# 
# for x in gradients:
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)
#     time.sleep(2)
##############################################################
# Step tree calc
# if __name__ == '__main__':
#     srkmultiprocessing.run_func_rids(range(7536,7541), srkanalysis.calc_step_tree_to_txt,0.00333333)
######################################################
# r['Title'] = "Wall Depol only-Correct Bernd Hg Setup Test w Periodic"
# r['SRKVersion'] = '3b1aada08e73b85400ffeaeb1ce43a4da0874ce6'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['ChamberRadius']=0.025
# s['ChamberHeight']=0.10
# s['ChamberRotation'] = '0. 90. 0.'
# s['E0FieldStrength']=0
# s['B0FieldStrength']=1e-6
# s['BGradFieldStrength']=0
# s['RecordAllSteps']=1
# s['PeriodicStopTime']=0.00333333
# s['TimeLimit']=100
# wall_depol=srkmisc.even_sample_over_log(0.00001, 0.001, 3)
#  
# for x in wall_depol:
#     s['DepolAtWallProb'] = x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)
#     time.sleep(2)
##############################################################
# Step tree calc
# if __name__ == '__main__':
#     srkmultiprocessing.run_func_rids(range(7541,7544), srkanalysis.calc_step_tree_to_txt,0.00333333)
################################################################
# Calc Run stats
#for run_id in range(7541,7543):
#    print run_id
#    srkdata.calc_run_stats_to_database(run_id)
################################################################
# r['Title'] = 'Vary polarization angle, E0, higher stat '
# r['SRKVersion'] = '62f26e55645b1cb7cf74994c790aa1b5127dbaa0'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=1e6
#
# run_ids=[]
# for x in np.linspace(10., 80., num = 6):
#     s['ThetaStart'] = x*np.pi/180.
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)

# for rid in xrange(7552,7558):
#     srkdata.make_macro_from_database(rid)
#     srkdata.run_macro_optima(rid)
#####################################################################
# r['Title'] = 'Vary polarization angle, E0, higher stat '
# r['SRKVersion'] = '62f26e55645b1cb7cf74994c790aa1b5127dbaa0'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 50000
# s['VelProfHistPath'] = '!293.15'
# s['E0FieldStrength']=1e6
#
# run_ids=[]
# for x in np.linspace(0, 80., num = 14):
#     s['ThetaStart'] = x*np.pi/180.
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)
###################################################################
# r['Title'] = "Correct Bernd Hg Setup Test w Periodic & EField"
# r['SRKVersion'] = '62f26e55645b1cb7cf74994c790aa1b5127dbaa0'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['ChamberRadius']=0.025
# s['ChamberHeight']=0.10
# s['ChamberRotation'] = '0. 90. 0.'
# s['BGradFieldStrength']=0
# s['B0FieldStrength']=1e-6
# s['E0FieldStrength']=1e-6
# s['RecordAllSteps']=1
# s['PeriodicStopTime']=0.00333333
# s['TimeLimit']=100
# strengths=srkmisc.even_sample_over_log(1, 1e-9, 5)
#
# for x in strengths:
#     s['E0FieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)
#     time.sleep(2)

#####################################################
# for run_id in range(7328,7329):
#     print run_id
#     srkdata.calc_run_stats_to_database(run_id)
######################################################
# r['Title'] = 'Vary E0 angles, large'
#
# r['SRKVersion'] = '62f26e55645b1cb7cf74994c790aa1b5127dbaa0'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 100000
# s['VelProfHistPath'] = '!293.15'
# s['BGradFieldStrength']=0
# s['E0FieldStrength']=1e6
#
# run_ids=[]
# for x in np.linspace(5, 50, num = 5):
#     y=x*np.pi/180.
#     s['E0FieldDirection'] = '0 {:.14f} {:.14f}'.format(np.sin(y),np.cos(y))
#     rid = srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)
###################################################
# for run_id in range(7596,7601):
#     print run_id
#     srkdata.calc_run_stats_to_database(run_id)
###################################################
# r['Title'] = "Wall Depol only-Correct Bernd Hg Setup Test w Periodic, Fixed"
# r['SRKVersion'] = 'e07f6594f4665aa10d0e1d6edb0a8f800b60890e'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['ChamberRadius']=0.025
# s['ChamberHeight']=0.10
# s['ChamberRotation'] = '0. 90. 0.'
# s['E0FieldStrength']=0
# s['B0FieldStrength']=1e-6
# s['BGradFieldStrength']=0
# s['RecordAllSteps']=1
# s['PeriodicStopTime']=0.00333333
# s['TimeLimit']=100
# wall_depol=srkmisc.even_sample_over_log(0.000001, 0.00001, 4)
#
# for x in wall_depol:
#     s['DepolAtWallProb'] = x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_local(rid)
#     time.sleep(2)

# rids=range(7606,7610)
# for rid in rids:
#     # srkdata.make_macro_from_database(rid)
#     # srkdata.run_macro_optima(rid)
#     srkdata.calc_run_stats_to_database(rid)

##############################################################
# Step tree calc
# if __name__ == '__main__':
#     srkmultiprocessing.run_func_rids(range(7606,7610), srkanalysis.calc_step_tree_to_txt,0.00333333)

###################################################
# r['Title'] = "Wall Depol only-Correct Bernd Hg Setup Test w Periodic, Fixed 2"
# r['SRKVersion'] = 'f231278675d1fa97798844ac3a47079ac6fc6a01'
# r['Date'] = today.strftime('%m/%d/%y')
# r['RunType'] = 'parOnly'
# r['NumTracksPer'] = 10000
# s['VelProfHistPath'] = '!293.15'
# s['ChamberRadius']=0.025
# s['ChamberHeight']=0.10
# s['ChamberRotation'] = '0. 90. 0.'
# s['E0FieldStrength']=0
# s['B0FieldStrength']=1e-6
# s['BGradFieldStrength']=0
# s['RecordAllSteps']=1
# s['PeriodicStopTime']=0.00333333
# s['TimeLimit']=100
# wall_depol=srkmisc.even_sample_over_log(0.000001, 0.00001, 4)
#
# for x in wall_depol:
#     s['DepolAtWallProb'] = x
#     rid=srkdata.make_macro_and_add_to_database(s,r)
#     srkdata.run_macro_optima(rid)
#     time.sleep(2)

###################################################
# rids=range(7610,7614)
# for rid in rids:
#     srkdata.calc_run_stats_to_database(rid)

##############################################################
# Step tree calc
# rids=range(7610,7614)
# if __name__ == '__main__':
#     srkmultiprocessing.run_func_rids(rids, srkanalysis.calc_step_tree_to_txt,0.00333333)

###################################################
r['Title'] = "Wall Depol only-Correct Bernd Hg Setup Test w Periodic, Fixed 3"
r['SRKVersion'] = '7dc2443902b6324aed9645abb367858138327163'
r['Date'] = today.strftime('%m/%d/%y')
r['RunType'] = 'parOnly'
r['NumTracksPer'] = 10000
s['VelProfHistPath'] = '!293.15'
s['ChamberRadius']=0.025
s['ChamberHeight']=0.10
s['ChamberRotation'] = '0. 90. 0.'
s['E0FieldStrength']=0
s['B0FieldStrength']=1e-6
s['BGradFieldStrength']=0
s['RecordAllSteps']=1
s['PeriodicStopTime']=0.00333333
s['TimeLimit']=100
wall_depol=srkmisc.even_sample_over_log(0.000001, 0.00001, 4)

for x in wall_depol:
    s['DepolAtWallProb'] = x
    srkdata.make_and_run(s,r,"optima")
    time.sleep(2)
