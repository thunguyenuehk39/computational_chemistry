import numpy as np
import subprocess
import periodictable
import os
#subprocess.run('/home/hung/Soft/packmol/packmol < mixture.inp', shell = True)
out_files = os.listdir('C:/Users/binhm/OneDrive/Com_Chem/project_2/density/')
file_path = 'C:/Users/binhm/OneDrive/Com_Chem/project_2/density/'
for file_density in out_files:
  f = open(os.path.join(file_path,file_density), 'r')
  l = 10.0
  line = f.readline()
  line = f.readline()
  total_mass = 0
  while True:
    line = f.readline()
    if not(line): break
    s = line.split()
    for atom in periodictable.elements:
      if s[0] == str(atom):
        total_mass += atom.mass
  f.close()
  density = total_mass/(l**3)
  print(file_density,":", density*10/6.022)
