import pandas as pd
import numpy as np
from google.colab import files


data = files.upload()
df =pd.read_csv('finalData.csv',ignore_index=True)

def filtering_data(df)
    dataframe=np.array(df.groupby(['frame','ID']))

    df.loc[(df['Color'] == 'blue') & (df['ID'] == 69), 'ID'] = '3'
    df.loc[(df['Color'] == 'blue') & (df['ID'] == 102), 'ID'] = '3'
    df.loc[(df['Color'] == 'red') & (df['ID'] == 3), 'ID'] = '12'
    df.loc[(df['frame'] >= 16*7) & (df['frame'] <=19*7) & (df['ID'] == 90), 'ID'] = '1'
    df.loc[(df['Color'] == 'red') & (df['ID'] == 1), 'ID'] = '9'
    df.loc[(df['Color'] == 'white') & (df['ID'] == 72), 'ID'] = '6'
    df.loc[(df['Position'] == 'Ball') & ((df['ID'] == 44) | (df['ID'] == 50) | (df['ID'] == 57) | (df['ID'] == 59) | (df['ID'] == 81)), 'ID'] = '0'

    df = df[(df.ID == 3) | (df.ID == 1) | (df.ID == 27) | (df.ID == 8) | (df.ID == 10) | (df.ID == 12) | (df.ID == 9) | (df.ID == 7) | (df.ID == 4) | (df.ID == 5) | (df.ID == 2) | (df.ID == 13) | (df.ID == 14) | (df.ID == 11) | (df.ID == 6) | (df.ID == 0)]

    df.to_csv('filtered_data.csv')

    return df