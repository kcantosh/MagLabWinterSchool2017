import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import glob,pickle
from runqmc import generate_dataframe

def normalize(a):
  x=np.array(a)
  n=np.sum(x**2)
  return x/n

sns.set_style('white')
args={'marker':'o','mew':1,'linestyle':'','lw':1}

runners=[]
for filename in glob.glob("*.pickle"):
  with open(filename,'rb') as f:
    runner=pickle.load(f)
    runners.append(runner)

df=pd.DataFrame(generate_dataframe(runners))
#df=df[df['wavefunction']=='triplet']
nax=len(df)
#nax=3
fig,axes=plt.subplots(nax,1,figsize=(3,8),sharex=True,sharey=False)

for i in range(nax):
  axes[i].set_title(df['wavefunction'][i]+str(df['r'][i]))
  fac=1./np.array(df['gr_r'][i])**2
  axes[i].plot(df['gr_r'][i],normalize(df['slatgr'][i])*fac,label='Slater')
  axes[i].plot(df['gr_r'][i],normalize(df['sjgr'][i])*fac,label='Slater-Jastrow')
  axes[i].plot(df['gr_r'][i],normalize(df['dmcgr'][i])*fac,label='DMC')
  axes[i].set_xlim(0.1,4)
#axes[i].legend()

plt.savefig("gr.pdf",bbox_inches='tight')
