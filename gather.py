import glob,pickle
import pandas as pd
from runqmc import H2Runner,generate_dataframe


runners=[]
for filename in glob.glob("*.pickle"):
  with open(filename,'rb') as f:
    runner=pickle.load(f)
    runners.append(runner)

df=pd.DataFrame(generate_dataframe(runners))
print(df)
df.to_csv("data.csv")


