from runqmc import H2Runner
import pandas as pd
import os
import pickle
runners=[]

for r in [1.0,1.5,2.0,2.5,3.0,3.5,4.0]:
  for wf in ['singlet','triplet']:
    #os.system("rm qw.*")
    basename="qw%s%g"%(wf,r)
    print("=====Running",wf,"for r =",r,"Bohr")
    runner=H2Runner()
    runner.r=r
    runner.wavefunction=wf
    runner.run_all(basename)
    
    with open(basename+".pickle",'wb') as f:
      pickle.dump(runner,f)

