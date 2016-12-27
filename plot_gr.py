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
df.sort_values('r',inplace=True)
df.index = range(0,len(df))
print(df)
nax=len(df)
#nax=3
fig,axes2d=plt.subplots(int(nax/2+0.6),2,figsize=(6,8),sharex=True,sharey=False)
axes=axes2d.flatten()
for i in range(nax):
  axes[i].annotate(df['wavefunction'][i]+",r="+str(df['r'][i]),xy=(0.1,0.8),xycoords='axes fraction',fontsize=6)
  fac=1./np.array(df['gr_r'][i])**2
  axes[i].plot(df['gr_r'][i],normalize(df['slatgr'][i])*fac,label='Slater')
  axes[i].plot(df['gr_r'][i],normalize(df['sjgr'][i])*fac,label='Slater-Jastrow')
  axes[i].plot(df['gr_r'][i],normalize(df['dmcgr'][i])*fac,label='DMC')
  axes[i].set_xlim(0.1,4)
axes2d[0,1].legend(loc=(1.05,0.))
axes2d[-1,0].set_xlabel("Distance (Bohr)")
axes2d[-1,0].set_ylabel("Probability density")
plt.savefig("gr.pdf",bbox_inches='tight')
