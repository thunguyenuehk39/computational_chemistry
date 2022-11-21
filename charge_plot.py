import os
import numpy as np
import pandas as pd

def distance(PATH,bond):
    #Read data
    nn=[]
    try:
        mylist = []
        for i in range(0,20):
            out_file = os.path.join(PATH,"umbrella_"+ str(i)+".out")
            print(out_file)
            with open(out_file) as f:
                text = [line.rstrip('\n') for line in f]
                mylist.append(text)
    except Exception:
        pass
    distance = []
    data = []
    pos ='ATOMIC_POSITIONS (angstrom)'
    #out_file = os.path.join(PATH,"umbrella_"+str(number)+".out")
    #with open(out_file) as f:
    #    mylist = [line.rstrip('\n') for line in f]
    #nn = np.where(np.array(mylist) == pos)[0]
    #Finding position
    mylist = np.array([item for sublist in mylist for item in sublist])
    nn = np.where(np.array(mylist) == pos)[0]
    for nb in nn:
        first = mylist[nb+1].split()
        second = mylist[nb+2].split()
        third = mylist[nb+3].split()
        fouth = mylist[nb+4].split()
        data.append([first,second,third,fouth])
    #pd.DataFrame(data)
        if bond == "h_ooh":
            h_o = np.sqrt((float(first[1])-float(second[1]))**2+(float(first[2])-float(second[2]))**2+(float(first[3])-float(second[3]))**2)
            distance.append(h_o)
        else:
            o_o = np.sqrt((float(second[1])-float(third[1]))**2+(float(second[2])-float(third[2]))**2+(float(second[3])-float(third[3]))**2)
            distance.append(o_o)
    distance = pd.DataFrame(distance, columns = ['distance'])
    return  distance, nn, mylist

def energy()