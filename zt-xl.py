import pandas as pd

file_path = 'data/ATP Donor Report BONE.xlsx'

df = pd.read_excel(file_path, header=6)#, usecols='D:')
df = df.drop(df.columns[[0, 1, 6,7]], axis=1)
df.to_csv('data/out.csv')
print(df)
quit()