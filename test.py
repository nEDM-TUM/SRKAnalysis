from srkanalysis import get_dipole_pos_from_dist
import srkdata
import srkmisc
import srkanalysis
import sqlite3
import numpy as np
from datetime import date

today = date.today()
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
# #srkdata.make_tracks_for_omega(100000, s, .1, 10, 100)
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
## 'Maxwell profiles: Vary Temperature with Linear Gradient'
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
# for x in srkmisc.even_sample_over_log(1e-14, 1e-9, 6):
#     s['BGradFieldStrength'] = x
#     rid=srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_optima(rid)

run_ids = range(5854, 5860)
for rid in run_ids:
    srkdata.run_macro_optima(rid)