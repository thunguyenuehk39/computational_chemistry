import numpy as np
import os.path
from os import lchown, mkdir, path
import re
from os import listdir
from os.path import isfile, join

def charge_input(PATH,PATH_OUT):
    files = os.listdir(PATH)
    for file,lowdin_file in zip(range(0,len(files)+1),files):
        mkdir_folder = os.path.join(PATH_OUT,str(file))
        os.mkdir(mkdir_folder)
        # file dos.in
        dos_form = open(os.path.join(PATH,'form','0_dos.in'),'r')
        dos_line = dos_form.readlines()
        file_in = str(file)+'_dos.in'
        PATH_outdir = '/lustre/lwork/dchieu/thu/potential/'
        file_name = os.path.join(mkdir_folder,file_in)
        file_in = open(file_name,'w')
        for i in dos_line:
            file_in.write(i)
        file_in.close()

        scf_form = open(os.path.join(PATH,'form','0_scf.in'),'r')
        scf_line = scf_form.readlines()
        f =  open(os.path.join(PATH,lowdin_file),'r')
        buf = f.readlines()
        natom = len(buf)
        dat = open(os.path.join(mkdir_folder,str(file)+'_scf.in'),'w')
        for i in scf_line[0:43]:
            dat.write(i)
        for line in buf:
            dat.write(line)
        dat.write("K_POINTS gamma")
        dat.close()
        f.close()
        print("done", file)




#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-H2O-2/lowenergy','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-H2O-2')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-CH3OH/lowenergy','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-CH3OH')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-C2H5OH/lowenergy','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-C2H5OH')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-H2O/lowenergy','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-H2O')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-CH3OH/lowenergy','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-CH3OH')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-C2H5OH/lowenergy','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-C2H5OH')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-H2O/lowding','/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-H2O')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-CH3OH/lowding','/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-CH3OH')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-C2H5OH/lowdin','/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-C2H5OH')
