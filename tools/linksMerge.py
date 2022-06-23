import pandas as pd

df_new=pd.read_csv("input_new.csv")
df_old=pd.read_csv("resources/input.csv")

for idx , row in df_new.iterrows():
    symbol = row["Symbol"]
    link = row["website_ir"]
    if pd.isna(link):
        dt_temp = df_old[ df_old["Symbol"]==symbol ]
        if len(dt_temp.index)>0:
            link = dt_temp.iloc[0]
            df_new.at[idx, 'website_ir'] = link['website_ir']
            print(df_new.at[idx, 'website_ir'])


df_new.to_csv("input_new.csv")


print("done")