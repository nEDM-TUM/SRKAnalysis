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
s = srkdata.default_srk_settings()
r = srkdata.default_run_settings()
r['SRKVersion'] = 'ea49998fff39515da5439bb86ec80c743e3d5d5e'
r['Date'] = today.strftime('%m/%d/%y')
r['RunType'] = 'deltaOmega'
r['NumTracksPer'] = 500000
r['Title'] = 'Fixed Chamber Height, Dipole Shifts'
s['E0FieldStrength'] = 5e6
#
# dist_range = np.arange(.01, .03, .01)
# for dist in dist_range:
#     s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - dist)
#     rid = srkdata.make_macro_and_add_to_database(s, r)
#     srkdata.run_macro_local(rid)

distances =[0.01,.02]
rids=[2886,2887]
for i in [0, 1]:
    s['DipolePosition'] = '0. 0. '+str(-0.5 * s['ChamberHeight'] - distances[i])
    srkdata.make_macro(rids[i],s,r)
    srkdata.run_macro_local(rids[i])
