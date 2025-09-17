import pandas as pd
import numpy as np
from cleaning_functions import clean_data



df = pd.read_csv('Travel details dataset.csv')


df_clean = clean_data(df)
df_clean.to_csv('Cleaned travel data.csv') 
df_clean.info()
