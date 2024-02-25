perform_analysis = 1   # 1/2/3   #1 - goes through fodlers in parent folder, takes '*.xtc', '*tpr' from there, calculates correlation functions, timescales, spin relaxation times
                                 #2 - user inserts '*.xtc' and '*.tpr' files, code calculates correlation functions, timescales, spin relaxation times
                                 #3 - user inserts folder path with timescale yaml files, code calculates spin relaxation times    - will come

########################################################################
# Analysis 1 settings
########################################################################

if perform_analysis == 1:
    """Path settings, saving settings"""
    parent_folder_path="//home/ricky/Documents/from_work/git/CorysPeptides/try/" # A parent folder that contains subfolders with simulations    
    systems=[""]                            # select only systems which folder name contains some of these
    output_path_correlation="/home/ricky/Documents/from_work/git/CorysPeptides/correlation_functions/"   
    output_path_timescales="/home/ricky/Documents/from_work/git/CorysPeptides/timescales_yamls2/" 
    output_path_relaxations="/home/ricky/Documents/from_work/git/CorysPeptides/relaxations/" 
    
    save_timescales_txt=False # Generate also txt files?, Results are already saved to yaml files             
    save_relaxations_txt=False # Generate also txt files?, Results are already saved to yaml files 
    
    report_name='analysis_report.pdf'
                
    """Handeling of trajectory file"""                                                  
    compress_xtc=False # True/False/"Original" 
                       #     True - creates tpr, xtc, gro with selection "selection"
                       #     False - creates tpr, gro with the selection, 
                       #             assumes that reduced xtc already exists
                       #     "Original" - uses original trajectories for correlation function calculation
                       #                slows significantly down the calculations
                    
    selection="non-Water"  # selection for the compression
                         # at the moment only standard selections that exists in a default index file supported
                         # such as non-Water 
                 

    """Settings for correlation times calculation"""                 
    begin=-1     # trajectory to be analyzed from the time 'begin' [ps], -1 means from the start
    end=-1       # trajectory to be analyzed until the tme 'end'  [ps]


    split_groups=True   # True/False        #  True      - creates an index file with all atom1-atom2 pairs separatelly
                                            #  False     - creates an index file, where all atom1-atom2 pairs are in one group, the correlation function 
                                                         # is an average over these then

    atom1_atom2_bonds=[('N','HN')] # An example for 'Protein'

    #atom1_atom2_bonds=[("C1","H11"),("C2","H21"),("C3","H31"), 
    #("C4","H41"),("C5","H51"),("C6","H61"),
    #("C7","H71"),("C8","H81"),("C9","H91"),
    #("C10","H101"),("C11","H111"),("C12","H121")]  # En example for lipid


    """Settings for timescale analysis"""
    OP=0 # order parameter
    smallest_corr_time=0 # enter in log scale -3 fs; 0 ps; 3 ns; 6 us;
    biggest_corr_time=5 # same as above
    N_exp_to_fit=100 # number of exponential functions to be fitted between the samlles and biggest corr time
    analyze=1/12 # the proportin of correlation data to be used for fitting, ex. 1/2 uses first half of the data
                 # keep in mind that length of the corr. function is already 1/2 of the length of the simulation
    magnetic_field=851
    magnetic_field_units='MHz' # 'MHz'/'T'
    nuclei="15N" #nuclei to calculate: 2H-deutherium; 13C - carbon; 15N - nitrogen 

########################################################################
# Analysis 2 settings
########################################################################

if perform_analysis == 2:
    """Path and saving settings"""
    xtcfile="/home/ricky/Documents/from_work/git/CorysPeptides/try/eElab/no_w_eElab.xtc"
    tprfile="/home/ricky/Documents/from_work/git/CorysPeptides/try/eElab/non-Water_eElab_micelle_40SDS_CHARMM_310K_Na_Neut_OPC_replica1.tpr"
    title='eElab is good'
    output_name='eElab'  #used for correlation, timescales, spin relaxation times
    
    save_timescales_txt=False # Generate also txt files?, Results are already saved to yaml files             
    save_relaxations_txt=False # Generate also txt files?, Results are already saved to yaml files 
    
    report_name='analysis_report.pdf'
                


    output_path_correlation="/home/ricky/Documents/from_work/git/CorysPeptides/correlation_functions/"   
    output_path_timescales="/home/ricky/Documents/from_work/git/CorysPeptides/timescales_yamls2/" 
    output_path_relaxations="/home/ricky/Documents/from_work/git/CorysPeptides/relaxations/" 
    
    """Settings for correlation times calculation"""
    end=-1       # trajectory to be analyzed until the tme 'end'  [ps]
    begin=-1     # trajectory to be analyzed from the time 'begin' [ps], -1 means from the start
    atom1_atom2_bonds=[('N','HN')] # An example for 'Protein'

    split_groups=True   # True/False        #  True      - creates an index file with all atom1-atom2 pairs separatelly
                                            #  False     - creates an index file, where all atom1-atom2 pairs are in one group, the correlation function 
                                                         # is an average over these then
    
    
    """Settings for timescale analysis"""
    OP=0 # order parameter
    smallest_corr_time=0 # enter in log scale -3 fs; 0 ps; 3 ns; 6 us;
    biggest_corr_time=5 # same as above
    N_exp_to_fit=100 # number of exponential functions to be fitted between the samlles and biggest corr time
    analyze=1/12 # the proportin of correlation data to be used for fitting, ex. 1/2 uses first half of the data
                 # keep in mind that length of the corr. function is already 1/2 of the length of the simulation
    magnetic_field=851
    magnetic_field_units='MHz' # 'MHz'/'T'
    nuclei="15N" #nuclei to calculate: 2H-deutherium; 13C - carbon; 15N - nitrogen 
   

