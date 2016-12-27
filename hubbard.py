import numpy as np
import scipy
import scipy.optimize
import glob,pickle
import pandas as pd
from runqmc import generate_dataframe
import matplotlib as plt

def hubbard(t,U):
  H=np.array([[0,-2*t],[-2*t,U]])
  return np.linalg.eigh(H)

def error(p,ref):
  w,v=hubbard(p[0],p[1])
  min_i=np.argmin(w)
  gs=v[:,min_i]
  gs_en=w[min_i]
  double=0.5*gs[1]**2
 # print("double",double, "gs energy",gs_en)
  return (gs_en-ref[0],double-ref[1])

runners=[]
for filename in glob.glob("*.pickle"):
  with open(filename,'rb') as f:
    runner=pickle.load(f)
    runners.append(runner)

for U in np.linspace(0,8,10):
  print(U,error([1.0,U],[0.0,0.0]))

#quit()

df=pd.DataFrame(generate_dataframe(runners))
print(df)
groups=df.groupby('r')
for r,group in groups:
  #print(group)
  prefix='dmc'
  if len(group)==2:
    print(" ")
    for prefix in ['slat','sj','dmc']:
      triplet=np.where(group['wavefunction'].values=='triplet')[0][0]
      singlet=1-triplet
      endiff=group[prefix+'_en'].values[singlet]-group[prefix+'_en'].values[triplet]
      double=group[prefix+'_double'].values[singlet]
      x0=[1.0,0.5]
      data=[endiff,double]
      xmin,cov_x,infodict,mesg,ier=scipy.optimize.leastsq(error,x0,(data),full_output=True)
      w,v=np.linalg.eigh(cov_x)
      #print(np.linalg.eigh(cov_x))
      print(prefix,r,"t=",xmin[0],"U=",xmin[1],"U/t",xmin[1]/xmin[0],'double',double,'endiff',endiff,'condition',w)


