from runqmc import H2Runner
import pandas as pd
import os
import pickle
runners=[]

for r in [1.6,1.7,1.8,1.9,2.0,3.0,4.0,5.0]:
  for wf in ['bonding']:
    #os.system("rm qw.*")
    basename="qw%s%g"%(wf,r)
    print(wf,r)
    runner=H2Runner()
    runner.r=r
    runner.wavefunction=wf
    print("hf")
    runner.gen_hf(basename+'.hf')
    print("vmc")
    runner.gen_vmc(basename+'.vmc')
    print("dmc")
    runner.gen_dmc(basename+'.dmc',basename+'.vmc.wfout')
    with open(basename+".pickle",'wb') as f:
      pickle.dump(runner,f)

