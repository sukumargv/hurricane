
import glob
import os
import pandas as pd

# Base Path
path = "/Users/sukumargv/Downloads/bc_ferries/"


all_files = glob.glob(os.path.join(path, "*.json")) # advisable to use os.path.join as this makes concatenation OS independent


df_from_each_file = (pd.read_json(f) for f in all_files)


concatenated_df = pd.concat(df_from_each_file, ignore_index=True)


concatenated_df['Status'] = concatenated_df['Status'].astype('category')
concatenated_df['Vessel'] = concatenated_df['Vessel'].astype('category')
concatenated_df['Time'] = pd.to_datetime(concatenated_df['Time'])
concatenated_df['route_no']  = concatenated_df['Route'].astype(str).str[-3:]
concatenated_df.drop('Route', 1, inplace=True)
concatenated_df['speed']  = concatenated_df['Speed'].astype(str).str[:-6].astype(float)
concatenated_df.drop('Speed', 1, inplace=True)
concatenated_df['route_no'] = concatenated_df['route_no'].astype('category')

Boundaries_col = concatenated_df.pop('Boundaries')


bc_ferries = pd.concat([concatenated_df, Boundaries_col.apply(pd.Series)], axis=1)

# Sort data frame by time
bc_ferries = bc_ferries.sort_values(by='Time')

# Queen of Nanaimo
# bcf_Queen_of_Nanaimo = bc_ferries[(bc_ferries['Time'] > '2016-11-17 10:40:00') & (bc_ferries['Time'] < '2016-11-18 10:38:19') & (bc_ferries['Vessel'] == 'Queen of Nanaimo')]

bc_ferries.to_pickle("bc_data.pkl")
