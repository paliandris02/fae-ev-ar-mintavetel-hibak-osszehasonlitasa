import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# 1) eredeti adatábázisból kiszedem a nem kellő adatokat 
airbnb = pd.read_csv("AB_NYC_2019.csv")
airbnb = airbnb.iloc[0:1000]
airbnb = airbnb.drop(columns=['id','name','host_name', 'host_id','latitude','longitude','minimum_nights',
                              'number_of_reviews','last_review','reviews_per_month',
                              'calculated_host_listings_count','availability_365'])

# 2)
# alap "paraméterek"
n = 100
mintaDb = 200
randomState = 2002

    

# oszlopnevek gyártása
oszlopnevek = np.array(range(100))+1
oszlopnevek = oszlopnevek.astype(str)
oszlopnevek = np.core.defchararray.add("Elem ",oszlopnevek)

    # FAE mintavétel

# oszlopnevek a minta dataframe-ben
airbnb_price_FAE_minta = pd.DataFrame(columns=oszlopnevek)

# FAE minta dataframe feltöltés
for i in range(mintaDb):
    temp_Minta = airbnb['price'].sample(n=n,replace=True,random_state=randomState+i)
    temp_Minta.index = oszlopnevek
    airbnb_price_FAE_minta=airbnb_price_FAE_minta.append(temp_Minta, ignore_index=True)

    # EV mintavétel

# oszlopnevek a minta dataframe-ben
airbnb_price_EV_minta = pd.DataFrame(columns=oszlopnevek)

# EV minta dataframe feltöltés
for i in range(mintaDb):
    temp_Minta = airbnb['price'].sample(n=n,replace=False,random_state=randomState+i)
    temp_Minta.index = oszlopnevek
    airbnb_price_EV_minta=airbnb_price_FAE_minta.append(temp_Minta, ignore_index=True)
