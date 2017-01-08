
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
  for ansatz in ['slat','multislat','sj','dmc']:
    plt.errorbar(b['r'],b[ansatz+'_en'],b[ansatz+'_en_err'],
            label=labels[ansatz]+","+a,color=colors[ansatz],marker=markers[a],
            **args)
#    plt.errorbar(b['r'],b['multislat_en'],b['slat_en_err'],label='Multiple Slater,'+a,**args)
#    plt.errorbar(b['r'],b['sj_en'],b['sj_en_err'],label='SJ,' + a,**args)
#    plt.errorbar(b['r'],b['dmc_en'],b['dmc_en_err'],label='DMC,' + a,**args)
  
plt.xlabel("r (Bohr)")
plt.ylabel("Energy (Hartree)")
plt.legend(loc=(1.0,0.5))
plt.xlim(0.9,4.1)
plt.ylim(-1.21,-0.39)
sns.despine(bottom=True,left=True,trim=False)
plt.savefig("energy.pdf",bbox_inches='tight')
