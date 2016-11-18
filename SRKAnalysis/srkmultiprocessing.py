import multiprocessing

__author__ = "Matthew Bales"
__credits__ = ["Matthew Bales"]
__license__ = "GPL"
__maintainer__ = "Matthew Bales"
__email__ = "matthew.bales@gmail.com"

num_procs_in_pool = 8  # Number of processors in pool


def run_func_helper((the_func, run_id, the_args)):
    """Helper function to allow for mapping by multiprocessing."""
    the_func(run_id, the_args)


def run_func_rids(run_ids, the_func, *other_args):
    """Run specified function over a range of run_ids and split work over pool of cpus"""
    the_args = []
    for run_id in run_ids:
        the_args.append([the_func] + [run_id, ] + [a for a in other_args])
    p = multiprocessing.Pool(num_procs_in_pool)
    p.map(run_func_helper, the_args)
