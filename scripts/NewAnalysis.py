import sys
import new_modules as nm
import new_modules2 as nm2
import new_modules3 as nm3
import os
import users_settings as us
from datetime import date
import yaml
import numpy as  np
import fnmatch
sys.path.append('extra_and_old_modules/')
import manage_files as mf
import matplotlib.pyplot as plt

from matplotlib.backends.backend_pdf import PdfPages

gammaD=41.695*10**6; #r*s^(-1)*T^(-1)
gammaH=267.513*10**6;
gammaC=67.262*10**6;
gammaN=-27.166*10**6;


if us.magnetic_field_units=='MHz':
    us.magnetic_field=us.magnetic_field*2*np.pi/gammaH*10**6


def exp_sum(xvalues,timescales):
    results=[]
    for res in range(1,len(timescales)):
        corr=np.zeros(len(xvalues))
        for i,timescale in enumerate(timescales[0]):
            corr+=timescales[res][i]*np.exp(-xvalues/(timescale*10**12))
        results.append(corr)
    return results

if us.perform_analysis == 1:
    timescale_report=[]
    for file in os.listdir(us.parent_folder_path):
        folder_path = us.parent_folder_path+os.fsdecode(file)+"/"
        for system in us.systems:
            if fnmatch.fnmatch(os.fsdecode(file), "*"+system+"*"):
                print(f' \n \n ########################### \n')
                print(f' 1) Creating and updating README.yaml for \n    {folder_path} \n')
                mf.go_through_simulation(folder_path)
                mf.remove_water(folder_path,us.selection,us.compress_xtc)
                with open(f'{folder_path}/README.yaml') as yaml_file:
                    readme = yaml.load(yaml_file, Loader=yaml.FullLoader)
                xtcfile=f"{folder_path}/{readme['FILES_FOR_RELAXATION']['xtc']['NAME']}"
                tprfile=f"{folder_path}/{readme['FILES_FOR_RELAXATION']['tpr']['NAME']}"
                title=readme['FILES']['tpr']['NAME'][:-4]
                output_name=title  

                print(f'\n 2) Calculating Correlation functions for \n    {folder_path} \n')
                
                nm.calculate_correlation_functions(xtcfile,tprfile,us.output_path_correlation,output_name,us.end,us.begin,us.atom1_atom2_bonds, us.split_groups,title)
                correlations_path=f'{us.output_path_correlation}/{output_name}/'
                
                print(f'\n 3) Calculating Timescales for \n    {folder_path} \n')               
                timescale_return = nm2.get_timescales_for_system(correlations_path,us.OP,us.smallest_corr_time,us.biggest_corr_time, us.N_exp_to_fit,us.analyze,us.output_path_timescales,output_name,save_yaml=True,save_txt=True)
                if len(timescale_return)>1:
                    timescale_report.append(timescale_return)
                print(f'\n 4) Calculating Spin relaxation times for \n    {folder_path} \n')
                timescales_file=f'{us.output_path_timescales}/{output_name}_timescales.yaml'
                 
                T1s, T2s, NOEs,  residues = nm3.get_spin_relaxation_times(us.magnetic_field,us.OP,us.smallest_corr_time, us.biggest_corr_time, us.N_exp_to_fit,us.analyze,timescales_file,us.nuclei,us.output_path_relaxations,output_name,save_yaml=True,save_txt=True)
                
    with PdfPages('try.pdf') as pdf:    
        rows=3
        cols=2
        per_page=rows*cols

        plt.rcParams["figure.figsize"] = [8.25, 11.75]
        plt.rcParams["figure.autolayout"] = True
        fig, axs = plt.subplots(rows, cols)
        i=0
        for i,system in enumerate(timescale_report):
            xvalues=np.array(system[4][0])
            fits=exp_sum(xvalues,system[0])

            for j in range(1,len(system[4])):
                axs[(i//cols)%per_page,(i%cols)].plot(xvalues/1000,system[4][j],"-",c=f"C{j-1}")
                
                axs[(i//cols)%per_page,(i%cols)].plot(xvalues/1000,fits[j-1],"--",c=f"C{j-1}")
            axs[(i//cols)%per_page,(i%cols)].set_xlabel('Time [ns]')
            axs[(i//cols)%per_page,(i%cols)].set_ylabel('Correlation function')
            axs[(i//cols)%per_page,(i%cols)].set_title(system[5],size=8)
            if (i%per_page==0 and i!=0):
                pdf.savefig()  # saves the current figure into a pdf page
                plt.rcParams["figure.figsize"] = [8.25, 11.75]
                plt.rcParams["figure.autolayout"] = True
                fig, axs = plt.subplots(rows, cols)
    
        for j in range(i+1,((i//per_page)+1)*per_page):
            axs[(j//cols)%per_page,(j%cols)].axis('off')
    
        pdf.savefig()          
        plt.close()                 
                
if us.perform_analysis == 2:
    pass

#correlation_file='/home/ricky/Documents/from_work/git/CorysPeptides/correlation_functions/2024_02_22_try_now_new_stuff/NHrotaCF_0.xvg'
#output_name='2024_02_22_try_now_new_stuff.yaml'
#print(nm2.get_timescales(correlation_file,OP,smallest_corr_time, biggest_corr_time, N_exp_to_fit,analyze,magnetic_field,nuclei))

#folder_path='/home/ricky/Documents/from_work/git/CorysPeptides/correlation_functions/2024_02_22_try_now_new_stuff/'
#nm2.get_timescales_for_system(folder_path,OP,smallest_corr_time, biggest_corr_time, N_exp_to_fit,analyze,output_name)

#timescales_file=output_name
#nm3.get_spin_relaxation_times(magnetic_field,OP,smallest_corr_time, biggest_corr_time, N_exp_to_fit,analyze,timescales_file,nuclei)
