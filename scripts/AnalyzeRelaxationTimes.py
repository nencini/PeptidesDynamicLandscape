import sys
import numpy as np

import os
import yaml

import fnmatch
sys.path.append('extra_and_old_modules/')
import manage_files as mf
import users_settings as us
import relaxation_times as rt

gammaD=41.695*10**6; #r*s^(-1)*T^(-1)
gammaH=267.513*10**6;
gammaC=67.262*10**6;
gammaN=-27.166*10**6;

if us.magnetic_field_units=='MHz':
    magnetic_field=magnetic_field*2*np.pi/gammaH*10**6
    
def perform_analysis_2(folder_path,output_name,RM_avail=False,grofile=None,xtcfile=None,tprfile=None):
    print(f' 2) Calculating Correlation functions for \n    {folder_path} \n')
    if us.moleculeType=="Protein": 
        rt.CalculateCorrelationFunctions(folder_path,us.begin,us.end,RM_avail,us.atom1_atom2_bonds[0][0],us.atom1_atom2_bonds[0][1],us.moleculeType,us.output_path_correlation)
    #elif us.moleculeType=="All": 
        #rt.CorrelationFunctionsLipids(folder_path,us.begin,us.end,True,us.moleculeType,us.output_path_correlation,us.systems,us.atom1_atom2_bonds)
    
    aminoAcids=rt.analyze_all_in_folder(us.OP,us.smallest_corr_time, us.biggest_corr_time, us.N_exp_to_fit,us.analyze,magnetic_field,folder_path,us.nuclei,us.output_path_timescales,output_name)


#addad 31.5.2022
#executed if not imported

if __name__ == "__main__":

    for file in os.listdir(us.parent_folder_path):
        folder_path = us.parent_folder_path+os.fsdecode(file)+"/"
        for system in us.systems:
            if fnmatch.fnmatch(os.fsdecode(file), "*"+system+"*"):
                mf.go_through_simulation(folder_path)
                mf.remove_water(folder_path,us.selection,us.compress_xtc)
                print(f' 2) Calculating Correlation functions for \n    {folder_path} \n')
                if us.moleculeType=="Protein": 
                    rt.CalculateCorrelationFunctions(folder_path,us.begin,us.end,True,us.atom1_atom2_bonds[0][0],us.atom1_atom2_bonds[0][1],us.moleculeType,us.output_path_correlation)
                elif us.moleculeType=="All": 
                    rt.CorrelationFunctionsLipids(folder_path,us.begin,us.end,True,us.moleculeType,us.output_path_correlation,us.systems,us.atom1_atom2_bonds)
    

