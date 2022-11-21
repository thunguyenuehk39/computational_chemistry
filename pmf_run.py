import numpy as np
import os.path
from os import path
import re
from os import listdir
from os.path import isfile, join
import subprocess
import matplotlib.pyplot as mp
mp.rcParams.update({'font.size': 14})

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

def check_files_in_progress(dir_name):
  allfiles = [f for f in listdir(dir_name) if isfile(join(dir_name, f))]
  tmp = np.copy(allfiles)
  for fs in tmp:
    if not check_QE(dir_name + fs):
      allfiles.remove(fs)
  print('************')
  return sorted(np.sort(allfiles), key = len)

def get_print_pmf_data(path, pmf_path, f_out):
  global timestep, t
  print(path + f_out)
  f = open(path + f_out, 'r')
  f_meta = open(pmf_path + 'metadata.pmf', 'a')
  f_series = open(pmf_path + f_out + '.pmf', 'w')
  energy = 0
  spring = 0
  eq = 0
  while True:
    buf = f.readline()
    if not buf: break
    if '!    total energy' in buf:
      buf = buf.split()
      energy = float(buf[4])
    if 'Distance' in buf:
      t += timestep
      buf = buf.replace('=', ' ')
      buf = buf.split()
      current_position = float(buf[4])
      buf = f.readline()
      buf = f.readline().split()
      eq = float(buf[10])
      spring = float(buf[7])
      f_series.write('%12.6f %12.6f\n' %(t, current_position))
  f.close()
  f_meta.write('%s %12.6f %12.6f\n' %(f_out + '.pmf', eq, spring))
  f_meta.close()
  f_series.close()
  return eq, spring

def plot_pmf(series, color1, color2):
  f = open('result.dat', 'r')
  line = f.readline()
  r = []
  energy = []
  error = []
  while True:
    line = f.readline().split()
    if '#Window' in line: break
    r = np.append(r, float(line[0]))
    energy = np.append(energy, float(line[1]))
    error = np.append(error, float(line[2]))
  mp.plot(r, energy, 'k-', linewidth = 1, label = series, color = color1)
  mp.fill_between(r, energy - error, energy + error, color = color2)
  f.close()

def run_pmf(path, tol, temp, scf, series, color1, color2):
  min_data = 100000
  max_data = -100000
  eq_old = 0
  try:
    os.mkdir(path + 'pmf')
  except OSError:
    print ("Creation of directory")
  else:
    print ("Creation of directory")
  pmf_path = path + 'pmf/'
  fo = open(pmf_path + 'metadata.pmf', 'w')
  fo.close()
#  out_files = np.flip(check_files_in_progress(path))
  out_files = check_files_in_progress(path)
  for f in out_files:
    eq, spring = get_print_pmf_data(path, pmf_path, f)
    step = eq - eq_old
    eq_old = eq
    if min_data > eq: min_data = eq
    if max_data < eq: max_data = eq
  num_step = round((max_data - min_data)/step) + 1
  min_data = min_data - step/2
  max_data = max_data + step/2
  wham = '/home/hung/Soft/wham/wham/wham ' + str(round(min_data, 2)) + ' ' + str(round(max_data, 2)) + ' ' + str(num_step) + ' '
  wham = wham + str(tol) + ' ' + str(temp) + ' 0 metadata.pmf result.dat ' + str(scf) + ' ' + str(np.random.randint(100000))
  owd = os.getcwd()
  os.chdir(path + 'pmf')
  subprocess.run(wham, shell = True)
  plot_pmf(series, color1, color2)
  os.chdir(owd)
  return 0

global timestep, t

mp.figure(1, figsize = (9, 4.5))
t = 0.0
timestep = 20.0 * 4.8378 * pow(10, -5) #ps
run_pmf('C:/Users/binhm/OneDrive/Com_Chem/project_2/umbrella/CH3OOH-H2O', 0.001, 300.0, 50, 'H2O', 'red', 'lightcoral')

t = 0.0
timestep = 20.0 * 4.8378 * pow(10, -5) #ps
run_pmf('C:/Users/binhm/OneDrive/Com_Chem/project_2/umbrella/CH3OOH-CH3OH', 0.001, 300.0, 50, 'H-OOH', 'blue', 'lightsteelblue')

mp.xlabel('Reaction coordinate (' + chr(197) + ')')
mp.ylabel('PMF (kcal/mol)')
mp.grid()
mp.tight_layout()
mp.legend()

mp.show()
