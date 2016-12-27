import numpy as np
import scipy
import scipy.optimize
import glob,pickle
import pandas as pd
from runqmc import generate_dataframe
import matplotlib.pyplot as plt
import seaborn as sns

#---------------------------------
def hubbard(t,U):
  H=np.array([[0,-2*t],[-2*t,U]])
  return np.linalg.eigh(H)
#---------------------------------
def error(p,ref):
  w,v=hubbard(p[0],p[1])
  min_i=np.argmin(w)
  gs=v[:,min_i]
  gs_en=w[min_i]
  double=0.5*gs[1]**2
 # print("double",double, "gs energy",gs_en)
  return (gs_en-ref[0],double-ref[1])

#---------------------------------


#---- Collect the data from our runs
runners=[]
for filename in glob.glob("*.pickle"):
  with open(filename,'rb') as f:
    runner=pickle.load(f)
    runners.append(runner)
df=pd.DataFrame(generate_dataframe(runners))


#----  For every value of r, fit the Hubbard model.
df_hubbard={'t':[],
            'r':[],
            'U':[],
            'double_occ':[],
            'singlet-triplet':[],
            'wavefunction':[]
            }
groups=df.groupby('r')
for r,group in groups:
  #print(group)
  prefix='dmc'
  if len(group)==2:
    for prefix in ['slat','sj','dmc']:
      triplet=np.where(group['wavefunction'].values=='triplet')[0][0]
      singlet=1-triplet
      endiff=group[prefix+'_en'].values[singlet]-group[prefix+'_en'].values[triplet]
      double=group[prefix+'_double'].values[singlet]
      x0=[0.3,0.3]
      data=[endiff,double]
      xmin,cov_x,infodict,mesg,ier=scipy.optimize.leastsq(error,x0,(data),full_output=True)
      w,v=np.linalg.eigh(cov_x)
      #print(np.linalg.eigh(cov_x))
      #print(prefix,r,"t=",xmin[0],"U=",xmin[1],"U/t",xmin[1]/xmin[0],'double',double,'endiff',endiff,'condition',w)
      df_hubbard['t'].append(xmin[0])
      df_hubbard['U'].append(xmin[1])
      df_hubbard['double_occ'].append(double)
      df_hubbard['singlet-triplet'].append(endiff)
      df_hubbard['r'].append(r)
      df_hubbard['wavefunction'].append(prefix)



# --- Now we can make some plots
sns.set_style("whitegrid")
df_hubbard=pd.DataFrame(df_hubbard)
df_hubbard.sort_values('r',inplace=True)
groups=df_hubbard.groupby('wavefunction')
fig,axes=plt.subplots(3,1,figsize=(3,8),sharex=True)

args={'marker':'o','mew':1,'linestyle':'-'}

for wf,group in groups:
  axes[0].plot(group['r'],group['U'],label=wf,**args)
  axes[1].plot(group['r'],group['t'],label=wf,**args)
  axes[2].plot(group['r'],group['U']/group['t'],label=wf,**args)

axes[0].set_ylabel('U (Hartree)')
axes[1].set_ylabel('t (Hartree)')
axes[2].set_ylabel('U/t')
axes[2].set_xlabel("Bond length (Bohr)")
for i in range(3):
  axes[i].legend(loc=(1.05,0))

plt.savefig("hubbard.pdf",bbox_inches='tight')

