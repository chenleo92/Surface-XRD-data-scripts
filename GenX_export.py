#! /usr/bin/python2

#==============================================================================
# Modify parameters in this section according to your needs

# choose what we want to export
do_fom_log = 1         # FOM as a function of iteration
do_final_tab = 1       # Export table (like in GenX File menu)
do_error_bars = 0      # Calculate errors in the gx file (like GenX menu item)
do_last_foms = 0       # FOMs for all individuals in the last generation
do_last_pars = 0       # Parameter values of all individuals in last generation
do_all_foms = 0        # All FOMs for all individuals in the buffer
do_par_limits = 0      # Parameter limit values
do_atom_tab = 0        # atomic coordinate file for best FOM solution

# path to the GenX distribution (i.e. where the genx_gui.py is located)
genxpath = '/home/tongjie/Softwares/genx'

#==============================================================================
import sys
import numpy as np
import os


# Add the genx directory to the python path
sys.path.append(genxpath)


if len(sys.argv) <2:
    print sys.argv
    print 'Wrong number of arguments to %s'%sys.argv[0]
    print 'Usage: %s infile.gx'%sys.argv[0]
    sys.exit(1)


print "number of files to process: %d" % (len(sys.argv)-1)

for filename in sys.argv[1:]:
    print "\n\n--------------------"
    print "Now exporting: %s" %filename

    name = os.path.basename(filename)    # filename without path
    name =  os.path.splitext(name)[0]    # remove the filename extension
    mainpath = os.path.dirname(filename) # path of file withouth filename
    
    import model, diffev, filehandling, time
    mod = model.Model()
    opt = diffev.DiffEv()
    config = filehandling.Config()
    
    # Load the model ...
    print 'Loading model %s...'%filename
    filehandling.load_gx(filename, mod, opt, config)
    
    # Simulate, this will also compile the model script
    print 'Simulating model...'
    mod.simulate()
    
    # Setting up the solver
    #opt.pickle_load(mod.load_addition('optimizer'))
    
    # export the fom as function of generation
    if do_fom_log:
        print 'saving fom log to file...'
        exportfile = os.path.join(mainpath,name + '_fom_log.dat')
        np.savetxt(exportfile, opt.fom_log)
    
    # export the fom array of all individuals
    if do_all_foms:
        print 'saving individual foms to file...'
        exportfile = os.path.join(mainpath,name + '_fom_evals.dat')
        my_fom_evals = diffev.CircBuffer.array(opt.fom_evals)
        np.savetxt(exportfile,my_fom_evals)
    
    ## export the parameters for all individuals
    #print 'saving individual parameters to file...'
    #exportfile = os.path.join(mainpath, name + '_par_evals.dat')
    #my_par_evals = de.CircBuffer.array(opt.par_evals)
    #np.savetxt(exportfile,my_par_evals)
    
    # export the trial foms of last generation
    if do_last_foms:
        print 'saving the trial foms of last the generation to file...'
        exportfile = os.path.join(mainpath, name + '_last_fom.dat')
        np.savetxt(exportfile,opt.fom_vec)
    
    # export the trial parameters of last generation
    if do_last_pars:
        print 'saving the trial parameters of last the generation to file...'
        exportfile = os.path.join(mainpath,name + '_last_pars.dat')
        np.savetxt(exportfile,opt.trial_vec)
    
    
    # export the limits to file
    if do_par_limits:
        print 'saving parameter limits to file...'
        exportfile = os.path.join(mainpath,name + '_par_limits.dat')
        griddata = mod.parameters.get_data()
        lolim=[]
        hilim=[]
        for line in griddata:
            if (not line[0] == '') and line[2] == True:
                lolim.append(line[3])
                hilim.append(line[4])
        outdata = [lolim, hilim]
        np.savetxt(exportfile,outdata)
            
    
    # calculate error bars
    if do_error_bars:
        print 'calculating error bars...'
        error_bar_level = 1.05
        n_elements = len(opt.start_guess)
        print 'Number of elemets to calc errobars for: %d' % n_elements
        error_values = []
        for index in range(n_elements):
            (error_low, error_high) = opt.calc_error_bar(\
                    index, error_bar_level)
            error_str = '(%.3e, %.3e,)'%(error_low, error_high)
            error_values.append(error_str)
        mod.parameters.set_error_pars(error_values)
    
    #export table
    if do_final_tab:
        print 'saving parameter table to file...'
        mod.export_table(os.path.join(mainpath,name + '_final.tab'))
    
    #save updated .gx file
    print 'saving updated .gx file (this may take a while)...'
    filehandling.save_gx(filename, mod, opt, config)
    
    # export atom table (label, element, x, y, z, occ, u)
    if do_atom_tab:
        print 'saving atom table to file...'
        exportfile = os.path.join(mainpath,name + '_atom_tab.dat')
    
        f = open(exportfile,'w')
        atomdata = mod.script_module.sample.create_uc_output()
        
        id = atomdata[6]
        el = atomdata[5]
        x = atomdata[0]
        y = atomdata[1]
        z = atomdata[2]
        oc = atomdata[3]
        u = atomdata[4]
        
        f.write('#%-5s %-4s %10s %10s %10s %10s %10s\n' % \
                ('ID', 'El', 'x', 'y', 'z', 'occ', 'u'))
        for ii in range(np.shape(atomdata)[1]):
            f.write('%-6s %-4s %10.4f %10.4f %10.4f %10.4f %10.4f\n' % \
                (id[ii].replace('.',''),el[ii],x[ii],y[ii],z[ii],oc[ii],u[ii]))
        f.close()

    # we are done with the file
    print 'finished exporting '+ name + '.'

# end of loop over all files
print 'done!'
print ''
