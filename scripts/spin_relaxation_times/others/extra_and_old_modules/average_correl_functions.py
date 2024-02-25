import numpy as np
import os
import yaml

class AverageCorrelFunction():
    def __init__(self,output_path, *paths):
        
        
        self.output_path=output_path
        self.paths=paths
        
        self.check_yamls()
        
        if self.all_good: 
            for file in os.listdir(paths[0]):
                if file!="README_correl.yaml":
                    self.name=file
                    self.loaded_data={}
                    self.get_average() 
                    
        if self.all_good:
            self.new_readme["FREQ_SAVE"]=float(self.saving_freq)
            with open(output_path+"README_correl.yaml","w") as f:
                yaml.dump(self.new_readme,f, sort_keys=True)
                    
    def check_yamls(self):
        yamls={}
        self.all_good=True
        self.new_readme={}
        for i,path in enumerate(self.paths):
            self.new_readme["replica"+str(i)]={}
            if os.path.isfile(path+"README_correl.yaml"):
                with open(path+"README_correl.yaml") as yaml_file:
                    yamls[i]=yaml.load(yaml_file,Loader=yaml.FullLoader)
                for key in yamls[i]:
                    if key!="BONDS":
                        self.new_readme["replica"+str(i)][key]=yamls[i][key]
            else:
                self.new_readme["replica"+str(i)]="no_readme_available"
            

        if len(yamls)>0:
            bonds=yamls[0]["BONDS"]
            for replica in yamls:
                if yamls[replica]["BONDS"]!=bonds:
                    self.all_good=False
       
        
        if self.all_good:
            self.new_readme["BONDS"]=bonds
        
            backslashes=[]
            for i,char in enumerate(self.output_path):
                if char=="/":
                    backslashes.append(i)
            self.new_readme["name"]=self.output_path[backslashes[-2]+1:-1]

        
    def get_average(self):
        
        
        
        mini=10**20 # should be larger than expected length of corr function
        
        #reads in data and finds the shortest corr. function
        for i,repeat in enumerate(self.paths):            
            self.input_data=repeat+self.name
            org_corrF, times_out=self.read_data()
            self.loaded_data[repeat]=[times_out,org_corrF]
            if len(times_out)<mini:
                minName=repeat
            mini=min(mini,len(times_out))
        
        self.average=[]
        
        #averages over corr. functions, uses only the length of the shortest corr. function
        a=len(self.loaded_data[minName][0])
        for i in range(a):
            av=[]
            for repeat in self.paths:
                av.append(self.loaded_data[repeat][1][i])
            self.average.append(np.mean(av))
        

        
        to_save=np.zeros([len(self.average),2])
        for i in range(len(self.average)):
            to_save[i,0]=self.loaded_data[minName][0][i]
            to_save[i,1]=self.average[i]
        
        saving_freq=self.loaded_data[minName][0][1]-self.loaded_data[minName][0][0]
        for repeat in self.loaded_data:
            if saving_freq!=(self.loaded_data[repeat][0][1]-self.loaded_data[repeat][0][0]):
                self.all_good=False
             
        self.all_good=True    
        if self.all_good:
            self.saving_freq=saving_freq
            try:
                os.system("mkdir "+self.output_path)
            except:
                pass

            np.savetxt(self.output_path+"/"+self.name,to_save)


    def read_data(self):
        # for reading the correlation function data
        opf = open(self.input_data, 'r')
        lines = opf.readlines()
        data_times = []
        data_F = []
        for line in lines:
            if '#' in line:
                continue
            if '&' in line:
                continue
            if '@' in line:
                continue    
            if 'label' in line:
                continue
            if line == "":
                continue
            parts = line.split()
            if np.shape(parts)[0]==2:
                data_F.append(float(parts[1]))
                data_times.append(float(parts[0]))


        data_Fout = np.array(data_F)
        times_out = np.array(data_times)
        return data_Fout, times_out
    
def set_biggest_ts_to_zero(timescales_yamls):
    for simulation in timescales_yamls:
        for analysis in timescales_yamls[simulation]:
            for residue in timescales_yamls[simulation][analysis]["results"]["Coeff"]:
                if timescales_yamls[simulation][analysis]["results"]["Coeff"][residue][-1]>0:
                    timescales_yamls[simulation][analysis]["results"]["Coeff"][residue][-1]=0
    return timescales_yamls
