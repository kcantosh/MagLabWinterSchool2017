from runqmc import H2Runner
import pandas as pd
import os
import pickle
runners=[]

for r in [0.9]: #[1.0,1.2,1.5,2.0,3.0,4.0,5.0]:
  for wf in ['singlet','triplet']:
    #os.system("rm qw.*")
    basename="qw%s%g"%(wf,r)
    print(wf,r)
    runner=H2Runner()
    runner.r=r
    runner.wavefunction=wf
    runner.run_all(basename)
    
    with open(basename+".pickle",'wb') as f:
      pickle.dump(runner,f)

