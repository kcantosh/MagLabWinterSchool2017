import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
import numpy as np
import glob,pickle
from runqmc import generate_dataframe

sns.set_style('white')
args={'marker':'o','mew':1,'linestyle':'','lw':1}

runners=[]
for filename in glob.glob("*.pickle"):
  with open(filename,'rb') as f:
    runner=pickle.load(f)
    runners.append(runner)

df=pd.DataFrame(generate_dataframe(runners))
df.sort_values('r',inplace=True)
df.index = range(0,len(df))



groups=df.groupby('wavefunction')
args={'marker':'o','mew':1,'linestyle':'-'}
for a,b in groups:
  plt.errorbar(b['r'],b['slat_double'],b['slat_double_err'],label='Slater'+a,**args)
  plt.errorbar(b['r'],b['sj_double'],b['sj_double_err'],label='SJ' + a,**args)
  plt.errorbar(b['r'],b['dmc_double'],b['dmc_double_err'],label='DMC' + a,**args)
  
plt.xlabel("r (Bohr)")
plt.ylabel("Double occupancy")
plt.legend(loc=(1.0,0.5))

sns.despine()
plt.savefig("double.pdf",bbox_inches='tight')

