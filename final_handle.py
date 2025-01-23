import pandas as pd

df = pd.read_csv("final1_test.csv")

print(df.head())
df_clean = df.dropna(subset=["mp1", "mp2", "mp3", "mp4", "mp5"])
print(df)