
import matplotlib.pyplot as plt
import seaborn as sns
import pandas as pd
sns.set_style('whitegrid',{'grid.color':'.95'})
import glob,pickle
from runqmc import H2Runner,generate_dataframe

#--- Collect data
runners=[]
for filename in glob.glob("*.pickle"):
  with open(filename,'rb') as f:
    runner=pickle.load(f)
    runners.append(runner)
df=pd.DataFrame(generate_dataframe(runners))
df.sort_values('r',inplace=True)


#--- Plot energy
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
  for ansatz in ['slat','multislat','sj']:
    plt.plot(b['r'].values,b[ansatz+'_sigma'].values,
            label=labels[ansatz]+","+a,color=colors[ansatz],marker=markers[a],
            **args)
  
plt.xlabel("r (Bohr)")
plt.ylabel("Standard deviation of local energy (Hartree)")
plt.legend(loc=(1.0,0.5))
plt.xlim(0.9,4.1)
#plt.ylim(-1.21,-0.39)
sns.despine(bottom=True,left=True,trim=False)
plt.savefig("sigma.pdf",bbox_inches='tight')
