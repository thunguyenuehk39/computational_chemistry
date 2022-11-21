import os
import numpy as np
import pandas as pd
import numpy as np
import glob

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

def distance(PATH,bond):
    #Read data
    nn=[]
    os.chdir(PATH)
    num_file = len(glob.glob("*.out"))
    print(num_file)
    mylist = []
    for i in range(0,num_file):
        out_file = os.path.join("umbrella_"+ str(i)+".out")
        natom, atoms = atom_data(out_file)
        print(out_file)
        with open(out_file) as f:
            text = [line.rstrip('\n') for line in f]
            mylist.append(text)
    distance = []
    data = []
    pos ='ATOMIC_POSITIONS (angstrom)'
    #Finding position
    mylist = np.array([item for sublist in mylist for item in sublist])
    nn = np.where(np.array(mylist) == pos)[0]
    for nb in nn:
        first = mylist[nb+1].split()
        second = mylist[nb+2].split()
        third = mylist[nb+3].split()
        fouth = mylist[nb+4].split()
        fifth = mylist[nb+5].split()
        sixth = mylist[nb+6].split()
        seventh = mylist[nb+7].split()
        data.append([first,second,third,fouth,fifth,sixth,seventh])
    #pd.DataFrame(data)
        if bond == "c-o":
            c_o = np.sqrt((float(first[1])-float(fifth[1]))**2+(float(first[2])-float(fifth[2]))**2+(float(first[3])-float(fifth[3]))**2)
            distance.append(c_o)
        elif bond =='o-o':
            o_o = np.sqrt((float(sixth[1])-float(fifth[1]))**2+(float(sixth[2])-float(fifth[2]))**2+(float(sixth[3])-float(fifth[3]))**2)
            distance.append(o_o)
        else:
            o_h = np.sqrt((float(sixth[1])-float(seventh[1]))**2+(float(sixth[2])-float(seventh[2]))**2+(float(sixth[3])-float(seventh[3]))**2)
            distance.append(o_h)
    distance = pd.DataFrame(distance, columns = ['distance'])
    return  distance, nn, mylist, natom, atoms

#def energy(PATH,number,solven):
def energy(nn,natom,mylist):
    Energy_all = []
    for nb in nn:
      kinetic_energy = mylist[nb+natom + 3].split()
      Ekin_Etot = mylist[nb+natom + 5].split()
      Energy = float(Ekin_Etot[5]) - float(kinetic_energy[4])
      Energy_all.append(Energy)
    Energy_all =pd.DataFrame(Energy_all, columns = ["energy"])
    return Energy_all

def minimum_energy(PATH,bond,solven,inital_step,range_):
    # PATH is path to data
    # solven are "methanol" or "water"
    # Bond are h-ooh or ho-oh
    # initial_step is beginnig distance 
    # range_ is range of error
    distance_ , nn,mylist, natom, atoms = distance(PATH,bond)
    #energy_ = energy(PATH,number,solven)
    energy_ = energy(nn,natom,mylist)
    frames = [distance_, energy_]
    result = pd.concat(frames, axis=1, sort=False)
    inital_step = inital_step*1000
    step = (inital_step+(0.01*150))*1000
    for i, j in zip(range(0,150), range(int(inital_step),int(step),10)):
        step = j/1000
        data = []
        for ii in range(0,len(result)):
          if result['distance'][ii] >= [step - range_]:
              if result['distance'][ii] <= [step + range_]:
                  data.append(result.iloc[ii])
              else:
                  pass
          else:
              pass
        data = pd.DataFrame(data)
        data = data.sort_values(by=['energy'],ascending=True)
        location = nn[data.index.values[0]]
        file_name = os.path.join(PATH,solven +"_"+ bond+ "_"+str(i)+".in")
        file_xyz = open(file_name,'w')
        for ii in range(natom):
          file_xyz.write("%s\n" % mylist[location+ii])
        file_xyz.close()
        print(data)
        print("done",file_name)
    return data , location

ethanol_c_o_PATH = "/content/drive/MyDrive/Computational Chemistry/thayhung/project_2/data/umbrella/c-o/CH3OOH-C2H5OH"
methanol_c_o_PATH = "/content/drive/MyDrive/Computational Chemistry/thayhung/project_2/data/umbrella/c-o/CH3OOH-CH3OH"
water_c_o_PATH = "/content/drive/MyDrive/Computational Chemistry/thayhung/project_2/data/umbrella/c-o/CH3OOH-H2O"
minimum_energy(water_c_o_PATH,"c-o","h2o",1.4,0.0025)
minimum_energy(methanol_c_o_PATH,"c-o","methanol",1.43,0.0025)
minimum_energy(ethanol_c_o_PATH,"c-o","ethanol",1.43,0.0025)