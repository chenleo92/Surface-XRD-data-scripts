#! /usr/bin/python2
###############################################################################
# Parameter section - modify values according to your needs
###############################################################################
#
# To leave any of the control parameters unchanged with respect to the ones in
# the loaded .gx file, you need to comment out the corresponding variables
# below

# List of repetition numbers.
# For each number in the list, one run will be performed for each distinct com-
# bination of km, kr, and fom  parameters (see below). The run files will be
# named according to these numbers
# e.g. range(5)    --> [0,1,2,3,4] (total of 5 repetitions named 0-4)
#      range(5,10) --> [5,6,7,8,9] (total of 5 repetitions starting with 5)
#      [1]         --> [1] (one iteration with index 1)
#iter_list = range(5)
iter_list = [1,2]

# figure of merit (FOM) to use
# needs to be a list of strings, valid names are:
#   'R1'
#   'R2'
#   'log'
#   'diff'
#   'sqrt'
#   'chi2bars'
#   'chibars'
#   'logbars'
#   'sintth4'
# e.g.: fom_list = ['log','R1']  # performs all repetitions for 'log' and 'R1'
fom_list = ['log']

# diffev control parameters
# needs to be a list of parameters combinations to use. 
# example:
#   krkm_list = [[0.7,0.8], [0.9,0.95]]
#   will run fits with these parameter combinations:
#   1. km = 0.7, kr = 0.8
#   2. km = 0.9, kr = 0.95
krkm_list = [[0.5,0.8], [0.9,0.95]]


# NOT YET WORKING!!!
# create_trial = 'best_1_bin'    #'best_1_bin','rand_1_bin',
                                 #'best_either_or','rand_either_or'
# Population size
use_pop_mult = False             # absolute (F) or relative (T) population size
pop_mult = 8                     # if use_pop_mult = True, populatio multiplier
pop_size = 200                   # if use_pop_mult = False, population size

# Generations
use_max_generations = True       # absolute (T) or relative (F) maximum gen.
max_generations = 10000           # if use_max_generations = True
max_generation_mult = 6          # if use_max_generations = False

# Parallel processing
use_parallel_processing = False
chunksize = 2
processes = 2

# Fitting
use_start_guess = False
use_boundaries = True
use_autosave = True
autosave_interval = 200
max_log = 600000

# Sleep time between generations
sleep_time = 0.000001

# Genx directory to add to the system path:
#genxpath = '/afs/umich.edu/user/c/s/cschlep/software/python/genx'
genxpath = '/home/tongjie/Softwares/genx'

###############################################################################
# End of parameter section
#-------------------------
# DO NOT MODIFY CODE BELOW
###############################################################################

import sys
import time
sys.path.insert(0,genxpath)

import model, diffev, io,  time, fom_funcs, filehandling


mod = model.Model()
config = filehandling.Config()
opt = diffev.DiffEv()

# Okay lets make it possible to batch script this file ...
if len(sys.argv) != 2:
    print sys.argv
    print 'Wrong number of arguments to %s'%sys.argv[0]
    print 'Usage: %s infile.gx'%sys.argv[0]
    sys.exit(1)
   
infile = sys.argv[1]

logfile = '%s_%s_runlog.txt' % \
          (infile.replace('.gx',''), time.strftime('%Y%m%d_%H%m%S'))
# Changed file name from original to this.
fid = open(logfile,'w')
fid.write('# GenX logfile for %s\n' % infile)
fid.write('# %s\n' % time.asctime())
fid.write('# \n')
fid.write('# %12s %4s %4s %4s %12s\n' % ('FOM-Function', 'km', 'kr', 'iter', 'FOM'))
fid.close


def autosave():
    #print 'Updating the parameters'
    mod.parameters.set_value_pars(opt.best_vec)
    filehandling.save_gx(outfile, mod, opt, config)
    
opt.set_autosave_func(autosave)

par_list = [(f,rm,i) for f in fom_list for rm in krkm_list \
            for i in iter_list]
#par_list = [(f,m,r,i) for f in fom_list for (m,r) in zip(km_list, kr_list) \
#            for i in iter_list]


for pars in par_list:

    fom = pars[0]
    km = pars[1][1]  # km    
    kr = pars[1][0]  # kr
    iter = pars[2]
    
    # Load the model ...
    print 'Loading model %s...'%infile
    filehandling.load_hgx(infile, mod, opt, config)
    
    # Simulate, this will also compile the model script
    print 'Simulating model...'
    mod.simulate()
    
    # Setting up the solver
    
    eval('mod.set_fom_func(fom_funcs.%s)' % fom)
    
    
    # Lets set the solver parameters:
    try:
        opt.set_create_trial('best_1_bin')
    except:
        print 'Warning: create_trial is not defined in script.'   
    try:
        opt.set_kr(kr)
    except:
        print 'Warning: kr is not defined in script.'   
    try:
        opt.set_km(km)
    except :
        print 'Warning: km is not defined in script.'
    try:
        opt.set_use_pop_mult(use_pop_mult)
    except:
        print 'Warning: use_pop_mult is not defined in script.'   
    try:
        opt.set_pop_mult(pop_mult)
    except:
        print 'Warning: pop_mult is not defined in script.'   
    try:
        opt.set_pop_size(pop_size)
    except:
        print 'Warning: pop_size is not defined in script.'   
    try:
        opt.set_use_max_generations(use_max_generations)
    except:
        print 'Warning: use_max_generations is not defined in script.'   
    try:
        opt.set_max_generations(max_generations)
    except:
        print 'Warning: max_generations is not defined in script.'   
    try:
        opt.set_max_generation_mult(max_generation_mult)
    except:
        print 'Warning: max_generation_mult is not defined in script.'   
    try:
        opt.set_use_parallel_processing(use_parallel_processing)
    except:
        print 'Warning: use_parallel_processing is not defined in script.'   
    try:
        opt.set_chunksize(chunksize)
    except:
        print 'Warning: chunksize is not defined in script.'   
    try:
        opt.set_processes(processes)
    except:
        print 'Warning: processes is not defined in script.'   
    try:
        opt.set_use_start_guess(use_start_guess)
    except:
        print 'Warning: use_start_guess is not defined in script.'   
    try:
        opt.set_use_boundaries(use_boundaries)
    except:
        print 'Warning: use_boundaries is not defined in script.'   
    try:
        opt.set_use_autosave(use_autosave)
    except:
        print 'Warning: use_autosave is not defined in script.'   
    try:
        opt.set_autosave_interval(autosave_interval)
    except:
        print 'Warning: autosave_interval is not defined in script.'   
    try:
        opt.set_max_log(max_log)
    except:
        print 'Warning: max_log is not defined in script.'   
    try:
        opt.set_sleep_time(sleep_time)
    except:
        print 'Warning: sleep_time is not defined in script.'     
    
    # Sets up the fitting ...
    print 'Setting up the optimizer...'
    opt.reset() # <--- Add this line
    opt.init_fitting(mod)
    opt.init_fom_eval()
    #opt.max_gen=500 #needs to be called after opt.init functions
    
    ### block: save config
    # make sure the modified solver parameters get saved to file
    # need to be updated in config
    
    options_float = ['km', 'kr', 'pop mult', 'pop size',\
                     'max generations', 'max generation mult',\
                     'sleep time', 'max log elements',\
                     'autosave interval',\
                     'parallel processes', 'parallel chunksize', 
                     'allowed fom discrepancy']
    set_float = [opt.km, opt.kr,
                 opt.pop_mult,\
                 opt.pop_size,\
                 opt.max_generations,\
                 opt.max_generation_mult,\
                 opt.sleep_time,\
                 opt.max_log, \
                 opt.autosave_interval,\
                 opt.processes,\
                 opt.chunksize,\
                 opt.fom_allowed_dis
                 ]
    
    options_bool = ['use pop mult', 'use max generations',
                    'use start guess', 'use boundaries', 
                    'use parallel processing', 'use autosave',
                    ]
    set_bool = [ opt.use_pop_mult,
                 opt.use_max_generations,
                 opt.use_start_guess,
                 opt.use_boundaries,
                 opt.use_parallel_processing,
                 opt.use_autosave,
                 ]
    
    # Make sure that the config is set
    if config:
        # Start witht the float values
        for index in range(len(options_float)):
            try:
                val = config.set('solver', options_float[index],\
                                      set_float[index])
            except io.OptionError, e:
                print 'Could not locate save solver.' +\
                      options_float[index]
                
            # Then the bool flags
            for index in range(len(options_bool)):
                try:
                    val = config.set('solver',\
                                         options_bool[index], set_bool[index])
                except io.OptionError, e:
                    print 'Could not write option solver.' +\
                          options_bool[index]
                    
            try:
                config.set('solver', 'create trial',\
                               opt.get_create_trial())
            except io.OptionError, e:
                print 'Could not write option solver.create trial'
    else:
        print 'Could not write config to file'
    ### end of block: save config
    
    # build outfile name
    outfile = infile
    outfile = outfile.replace('.gx','')
    outfile = '%s_%s_kr%.2f_km%.2f_run%d.gx' % (outfile, fom, kr, km, iter)
                
    print 'Saving the initial model to %s'%outfile
    filehandling.save_gx(outfile, mod, opt, config)
    
    print ''
    print 'Settings:'
    print '---------'
    
    print 'Number of fit parameters    = %s' % len(opt.best_vec)
    print 'FOM function                = %s' % mod.fom_func.func_name
    print ''
    print 'opt.km                      = %s' % opt.km
    print 'opt.kr                      = %s' % opt.kr
    print 'opt.create_trial            = %s' % opt.create_trial.im_func
    print ''
    print 'opt.use_parallel_processing = %s' % opt.use_parallel_processing
    print 'opt.chunksize               = %s' % opt.chunksize
    print 'opt.processes               = %s' % opt.processes
    print ''
    print 'opt.use_max_generations     = %s' % opt.use_max_generations
    print 'opt.max_generation_mult     = %s' % opt.max_generation_mult
    print 'opt.max_generations         = %s' % opt.max_generations
    print 'opt.max_gen                 = %s' % opt.max_gen
    print 'opt.max_log                 = %s' % opt.max_log
    print ''                          
    print 'opt.use_start_guess         = %s' % opt.use_start_guess
    print 'opt.use_boundaries          = %s' % opt.use_boundaries 
    print 'opt.use_autosave            = %s' % opt.use_autosave
    print 'opt.autosave_interval       = %s' % opt.autosave_interval
    print ''
    print 'opt.pop_size                = %s' % opt.pop_size       
    print 'opt.use_pop_mult            = %s' % opt.use_pop_mult   
    print 'opt.pop_mult                = %s' % opt.pop_mult       
    print 'opt.n_pop                   = %s' % opt.n_pop          
    print ''
    print '--------'
    print ''
    
    
    # To start the fitting
    print 'Fitting starting...'
    t1 = time.time()
    opt.optimize()
    t2 = time.time()
    print 'Fitting finsihed!'
    print 'Time to fit: ', (t2-t1)/60., ' min'
    
    print 'Updating the parameters'
    mod.parameters.set_value_pars(opt.best_vec)
    
    print 'Saving the fit to %s'%outfile
    filehandling.save_gx(outfile, mod, opt, config)
    
    print 'finished current fit'
    fid = open(logfile,'a')
    fid.write('%-14s %4.2f %4.2f %4d %12.6g\n' % \
                (fom, km, kr, iter, opt.fom_log[-1][1]))
    fid.close
    
print 'Fitting sucessfully finished'
