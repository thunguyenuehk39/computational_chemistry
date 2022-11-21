import numpy as np
import os.path
from os import path
import re
from os import listdir
from os.path import isfile, join

# check if file is QE output
def check_QE(s):
  isQE = False
  fr = open(s,'r')
  for i in range(0, 10):
    buf = fr.readline()
    if not buf:
      break
    if 'Quantum ESPRESSO' in buf:
      isQE = True
  return isQE

# read number of atoms
def read_num_atoms(s):
  fr = open(s,'r')
  latvec = np.zeros((3, 3))
  while True:
    buf = fr.readline()
    if not buf:
      break
    
    if 'lattice parameter (alat)' in buf:
      line = buf.split()
      alat = float(line[4])
    
    if 'number of atoms/cell' in buf:
      line = buf.split()
      n = int(line[-1])
    
    if 'cart. coord. in units of alat' in buf:
      for i in range(0, 3):
        buf = fr.readline().split()
        latvec[i, 0] = float(buf[3])
        latvec[i, 1] = float(buf[4])
        latvec[i, 2] = float(buf[5])
      break
  
  fr.close()
  return n, alat*latvec*0.529177

def atom_data(output_file):
  natom, alat = read_num_atoms(output_file)
  fr = open(output_file,'r')
  while True:
    buf = fr.readline()
    if not buf:
      break
    if 'ATOMIC_POSITIONS' in buf:
      atoms = []
      for i in range(0, natom):
        line = fr.readline()
        atoms = np.append(atoms, line)
  fr.close()
  return natom, atoms

def check_files_in_progress():
  allfiles = [f for f in listdir('./') if isfile(join('./', f))]
  max_cnt = -1
  file_input_read = ''
  file_output_read = ''
  file_input_new = ''
  for fs in allfiles:
    if ('umbrella' in fs) and (check_QE(fs)):
      s = re.split('_|\\.', fs)
      if max_cnt < int(s[1]):
        max_cnt = int(s[1])
        file_input_read = './umbrella_' + str(max_cnt) + '.in'
        file_output_read = './' + fs
        file_input_new = './umbrella_' + str(max_cnt + 1) + '.in'
  return file_input_read, file_output_read, file_input_new

def get_print_new_bias(f_out):
  f = open(f_out, 'r')
  while True:
    buf = f.readline()
    if not buf:
      break
    if 'Atom' in buf:
      s = buf.split()
      r = float(s[10]) + 0.05
      newbias = s[1] + ' ' + s[4] + ' ' + s[7]
      fo = open('bias_harmonic', 'w')
      fo.write('%s %7.2f' %(newbias, r))
      fo.close()
      break
  f.close()
  return 0

def print_new_input():
  umbrella_files = check_files_in_progress()
  print(umbrella_files)
  f_input_r = open(umbrella_files[0], 'r')
  f_input_w = open(umbrella_files[2], 'w')
  natom, atoms = atom_data(umbrella_files[1])
  get_print_new_bias(umbrella_files[1])
  while True:
    buf = f_input_r.readline()
    if not buf:
      break
    if 'ATOMIC_POSITIONS' in buf:
      f_input_w.write(buf)
      for i in range(0, natom):
        line = f_input_r.readline()
        f_input_w.write(atoms[i])
    else:
      f_input_w.write(buf)
  f_input_r.close()
  f_input_w.close()
  return umbrella_files[2]

def print_new_script(fi_name):
  s = fi_name[2:]
  fo = open('super_sub.sh', 'w')
  fo.write('#!/bin/sh\n')
  fo.write('#PBS -l select=1\n')
  fo.write('#PBS -q P_016\n')
  fo.write('#PBS -N hooh\n')
  fo.write('#PBS -l walltime=24:00:00\n')
  fo.write('cd ${PBS_O_WORKDIR}\n')
  fo.write('aprun -n 36 -N 36 -j 1 /home/hungmle/ESPRESSO/testqe/bin/pw.x < ' + s + ' > ' + s[:-2] + 'out')
  fo.close()

umbrella_file = print_new_input()
print_new_script(umbrella_file)
