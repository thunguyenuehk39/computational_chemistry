import numpy as np
import os.path
from os import path
import re
from os import listdir
from os.path import isfile, join
import subprocess

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

def get_r_distance(path, f_out):
  f =  open(path + f_out, 'r')
  r_eq = 0
  while True:
    buf = f.readline()
    if not buf: break
    if 'Atom' in buf:
      buf = buf.split()
      r_eq = float(buf[10])
      break
  return r_eq

def get_pmf_data(path, f_out):
  cnt = 0
  r_eq = get_r_distance(path, f_out)
  f = open(path + f_out, 'r')
  backward = False
  forward = False
  while True:
    buf = f.readline()
    if not buf: break
    if '!    total energy' in buf:
      buf = buf.split()
      energy = float(buf[4])
    if 'Distance' in buf:
      cnt += 1
      buf = buf.replace('=', ' ')
      buf = buf.split()
      current_position = float(buf[4])
      if current_position < r_eq:
        backward = True
      else:
        forward = True
  f.close()
  if forward and backward:
    print(path + f_out + ': ok ' + str(cnt) + ' ' + str(r_eq))
  else:
    print(path + f_out + ': not ok ' + str(cnt) + ' ' + str(r_eq))
  return 0

def check_pmf_data(path):
  out_files = check_files_in_progress(path)
  for f in out_files:
    get_pmf_data(path, f)
  return 0

check_pmf_data('ho_oh/')
check_pmf_data('h_ooh/')
