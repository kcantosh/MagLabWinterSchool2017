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
args={'mew':1,'linestyle':'-'}
palette=sns.color_palette()
colors={'slat':palette[0],
        'multislat':palette[1],
        'sj':palette[2],
        'dmc':palette[3]
        }
labels={'slat':"Slater",
        'multislat':"Multiple Slater",
        'sj':"Multiple Slater-Jastrow",
        'dmc':"DMC"
        }

markers={'singlet':'o',
         'triplet':'s' 
         }

for a,b in groups:
  for ansatz in ['slat','multislat','sj','dmc']:
    plt.errorbar(b['r'].values,b[ansatz+'_double'].values,b[ansatz+'_double_err'].values,
            label=labels[ansatz]+","+a,color=colors[ansatz],marker=markers[a],
            **args)
  
plt.xlabel("r (Bohr)")
plt.xlim(1.0,4.1)
plt.ylabel("Double occupancy of a single site")
plt.legend(loc=(1.0,0.5))

sns.despine()
plt.savefig("double.pdf",bbox_inches='tight')

