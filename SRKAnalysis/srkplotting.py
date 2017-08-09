import srkdata
import numpy as np
import ROOT as r
import matplotlib.pyplot as plt
plt.style.use('mastercolor')
import srkglobal
import srkmisc

default_params = ["posX", "posZ", "velX", "velZ", "phi", "theta"]#, "Bx", "By", "Bz"]

def make_tree_to_array(run_id, query_list=default_params):
	"""Makes the step_tree of result files into a numpy array"""
	#Currently only for one particle!
	
#	print query_list
	results_path = srkglobal.results_dir + "Results_RID" + str(run_id) + ".root"
	if not srkmisc.file_exits_and_not_zombie(results_path):
		print "No results file found for RunID " + str(run_id) + ". Aborting."
		return
	else:
		root_file = r.TFile(results_path, "READ")
		step_tree = r.gDirectory.Get('stepTree')
#		r.gROOT.cd()
		
		return_arr = np.empty((len(query_list), step_tree.GetEntries()+2))
#		tree_dict = {
#			"posX":step_tree.pos.x(),
#			"posZ":step_tree.pos.z(),
#			"velX":step_tree.vel.x(),
#			"velZ":step_tree.vel.z(),
#			"phi":step_tree.phi,
#			"theta":step_tree.theta()
#		}
		for i in range(step_tree.GetEntries()):
			step_tree.GetEntry(i)
			return_arr[0,i+1] = step_tree.pos.x()
			return_arr[1,i+1] = step_tree.pos.z()
			return_arr[2,i+1] = step_tree.vel.x()
			return_arr[3,i+1] = step_tree.vel.z()
			return_arr[4,i+1] = step_tree.phi
			return_arr[5,i+1] = step_tree.theta
			#return_arr[6,i+1] = step_tree.BFieldStrenth.x()
			#return_arr[7,i+1] = step_tree.BFieldStrenth.y()
			#return_arr[8,i+1] = step_tree.BFieldStrenth.z()
#			for j in range(len(query_list)):
#				return_arr[j,i]=tree_dict[query_list[j]]
		
		hit_tree = r.gDirectory.Get('hitTree')
		hit_tree.GetEntry(0)
		
		return_arr[0,0] = hit_tree.pos0.x()
		return_arr[1,0] = hit_tree.pos0.z()
		return_arr[2,0] = hit_tree.vel0.x()
		return_arr[3,0] = hit_tree.vel0.z()
		return_arr[4,0] = hit_tree.phi0
		return_arr[5,0] = hit_tree.theta0
		#return_arr[6,0] = np.NaN
		#return_arr[7,0] = np.NaN
		#return_arr[8,0] = np.NaN
		
		return_arr[0,-1] = hit_tree.pos.x()
		return_arr[1,-1] = hit_tree.pos.z()
		return_arr[2,-1] = hit_tree.vel.x()
		return_arr[3,-1] = hit_tree.vel.z()
		return_arr[4,-1] = hit_tree.phi
		return_arr[5,-1] = hit_tree.theta
		#return_arr[6,-1] = np.NaN
		#return_arr[7,-1] = np.NaN
		#return_arr[8,-1] = np.NaN
		
		root_file.Close()
		return return_arr
		
def make_timeline(run_id):
	srk_settings, run_settings = srkdata.get_settings_from_database(run_id, "g2")
	no = srk_settings['TimeLimit']/srk_settings['PeriodicStopTime'] + 1
	time_arr = np.linspace(0, no*srk_settings['PeriodicStopTime'], no, False)
	return time_arr
	
def delta_phi(arr, baseline, absolute=False):
	if len(arr) != len(baseline):
		print "Arrays not of same length, aborting!" #later maybe length of shortest? 
		return
	new_arr = np.empty(len(arr))
	if absolute: 
		new_arr = arr-baseline
	else:
		new_arr[0] = np.nan
		new_arr[1:] = (arr[1:]-baseline[1:])/(baseline[1:]-baseline[0])
	return new_arr
	
def plot_single(title, arr, timeline, savemode = 'both', titleY = False, legend = False, style=False, rangeX=False, rangeY=False):
	if not legend: legend = ''
	if not style: style='-'
	plt.plot(timeline, arr, style, label=legend)
	plt.legend(loc='best')
	plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
	plt.xlabel('t [s]')
	plt.title(title)
	plt.tick_params(right=True)
	if titleY: plt.ylabel(titleY)
	if rangeX: plt.xlim((rangeX[0], rangeX[1]))
	if rangeY: plt.ylim((rangeY[0], rangeY[1]))
	if not savemode in ['plot', 'show']: 
		nameparts = title.split()
		savetitle = ''
		for n in nameparts:
			savetitle += n + '_'
		savetitle = savetitle[:-1]
		plt.savefig(srkglobal.graphs_dir+savetitle+'.png') #save to srkglobal graphs directory?
	if savemode != 'save': plt.show()
	
def plot_comparative(title, arr_list, timelines, savemode = 'both', titleY = False, legend_list = False, style=False, rangeX=False, rangeY=False):
	if not legend_list: legend_list = [i for i in range(len(arr_list))]
	if not style: style = '-' #later also list of styles? careful, string = list of chars
	if np.linalg.matrix_rank(timelines) == 1:
		timelines = [timelines for i in range(len(arr_list))]
	for i in range(len(arr_list)):
		plt.plot(timelines[i], arr_list[i], style, label=legend_list[i])
	plt.ticklabel_format(style='sci', axis='x', scilimits=(0,0))
	plt.legend(loc='best')
	plt.xlabel('t [s]')
	plt.title(title)
	plt.tick_params(right=True)
	if titleY: plt.ylabel(titleY)
	if rangeX: plt.xlim((rangeX[0], rangeX[1]))
	if rangeY: plt.ylim((rangeY[0], rangeY[1]))
	if not savemode in ['plot', 'show']:
		nameparts = title.split()
		savetitle = ''
		for n in nameparts:
			savetitle += n + '_'
		savetitle = savetitle[:-1]
		plt.savefig(srkglobal.graphs_dir+savetitle+'.png')
	if savemode != 'save': plt.show()
