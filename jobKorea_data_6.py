import pandas as pd
from jobKorea_sales_dynamic_2 import get_jobkorea_data

df = pd.read_csv("enterprise_df_10k_utf8_data.csv")
corp_name_list = df[df['담당'] == '6번']['기업명'].dropna().unique().tolist()

results_df = get_jobkorea_data(corp_name_list)

results_df.to_csv("jobkorea_data_6_0618.csv", index=False, encoding="utf-8-sig")