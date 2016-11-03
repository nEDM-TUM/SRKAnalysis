import multiprocessing

def run_func_helper((the_func, run_id, the_args)):
    the_func(run_id,the_args)

def run_func_rids(run_ids,the_func,*other_args):
    the_args=[]
    for run_id in run_ids:
        the_args.append([the_func]+[run_id,]+[a for a in other_args])
    p=multiprocessing.Pool(8)
    p.map(run_func_helper,the_args)