import numpy as np
import os.path
from os import lchown, mkdir, path
import re
from os import listdir
from os.path import isfile, join
import codecs
import glob

def charge_input(PATH,PATH_OUT):
    files = os.listdir(PATH)
    for file in range(0,len(files)+1):
        mkdir_folder = os.path.join(PATH_OUT,str(file))
        #os.mkdir(mkdir_folder)
        # file dos.in
        file_in = str(file)+'_dos.in'
        PATH_outdir = '/lustre/lwork/dchieu/thu/potential/'
        file_name = os.path.join(PATH_OUT,file_in)
        file_in = open(file_name,'w')
        file_in.write("&projwfc\n")
        file_in.write(" outdir ='/lustre/lwork/dchieu/scratch/'\n")
        file_in.write(" prefix ='126',\n")
        file_in.write(" filpdos ='%s.pdos',\n" %file)
        file_in.write(" Emin = -20.0,\n")
        file_in.write(" Emax = 6.0,\n DeltaE = 0.01,\n ngauss = 1,\n degauss = 0.02,\n/")
        file_in.close()

        f =  open(os.path.join(PATH,str(file)+'.in'),'r')
        buf = f.readlines()
        natom = len(buf)
        dat = open(os.path.join(PATH_OUT,str(file)+'_scf.in'),'w')
        dat.write("&control\n")
        dat.write("  calculation      = 'scf',\n")
        dat.write("  prefix           = '126',\n")
        dat.write("  restart_mode     = 'from_scratch',\n")
        dat.write("  pseudo_dir       = '/lustre/lwork/dchieu/thu/potential/',\n")
        dat.write("  outdir           = '/lustre/lwork/dchieu/scratch/',\n")
        dat.write("  nstep            = 500,\n")
        dat.write("  verbosity        = 'medium',\n")
        dat.write("/\n")
        dat.write("&system\n")
        dat.write("  ibrav            = 1,\n")
        dat.write("  celldm(1)        = 18.8973,\n")
        dat.write("  nat              = %s,\n" % (natom-1))
        dat.write("  ntyp             = 3,\n")
        dat.write("  ntyp             = 3,\n")
        dat.write("  occupations      = 'smearing',\n")
        dat.write("  smearing         = 'gauss',\n")
        dat.write("  degauss          = 0.01,\n")
        dat.write("  ecutwfc          = 40.0,\n")
        dat.write("  london           = .true.,\n")
        dat.write("  dftd3_version    = 3,\n")
        dat.write("  nosym            = .true.,\n")
        dat.write("/\n")
        dat.write("&electrons\n")
        dat.write("  diagonalization  = 'david',\n")
        dat.write("  mixing_beta      = 0.7,\n")
        dat.write("  electron_maxstep = 100,\n")
        dat.write("  conv_thr         = 1.0d-07,\n")
        dat.write("/\n")
        dat.write("&ions\n")
        dat.write("  ion_dynamics     = 'verlet',\n")
        dat.write("  ion_temperature  = 'rescaling',\n")
        dat.write("  tempw            = 300,\n")
        dat.write("  tolp             = 20, \n")
        dat.write("/\n")
        dat.write("&cell\n")
        dat.write("  cell_dynamics    = 'bfgs',\n")
        dat.write("/\n")
        dat.write("ATOMIC_SPECIES\n")
        dat.write("  C  12.0000000  C.pbe-n-rrkjus_psl.1.0.0.UPF\n")
        dat.write("  H  1.00782503  H.pbe-rrkjus_psl.1.0.0.UPF\n")
        dat.write("  O  15.9949146  O.pbe-n-rrkjus_psl.1.0.0.UPF\n")
        for line in buf:
            dat.write(line)
        dat.write("K_POINTS gamma")
        dat.close()
        f.close()
        print("done", file)
        




#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-H2O-2/lowenergy/','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-H2O-2')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-CH3OH/lowenergy/','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-CH3OH')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-C2H5OH/lowenergy/','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-h/CH3OOH-C2H5OH')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-H2O/lowenergy/','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-H2O')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-CH3OH/lowenergy/','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-CH3OH')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-C2H5OH/lowenergy/','/Users/apple/OneDrive/Com_Chem/project_2/scf/o-o/CH3OOH-C2H5OH')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-H2O/lowding/','/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-H2O')
#charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-CH3OH/lowdin/','/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-CH3OH')
charge_input('/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-C2H5OH/lowdin/','/Users/apple/OneDrive/Com_Chem/project_2/scf/c-o/CH3OOH-C2H5OH')
