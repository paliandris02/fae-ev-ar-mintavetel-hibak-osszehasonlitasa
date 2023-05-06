import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import scipy.stats as stats

# 1) eredeti adatábázisból kiszedem a nem kellő adatokat 
airbnb = pd.read_csv("AB_NYC_2019_Páli András_VBII48_II_témakör.csv")
airbnb = airbnb.drop(columns=['id','name','host_name', 'host_id','latitude','longitude','minimum_nights',
                              'number_of_reviews','last_review','reviews_per_month',
                              'calculated_host_listings_count','availability_365'])
airbnb.price.hist()
airbnb.describe()

##### 
# neighbourhoodGroup = régió
# neighbourhood = körzet
######

# 2)
# alap paraméterek
n = 100
mintaDb = 200


# oszlopnevek gyártása
oszlopnevek = np.array(range(n))+1
oszlopnevek = oszlopnevek.astype(str)
oszlopnevek = np.core.defchararray.add("Elem ",oszlopnevek)

    # FAE mintavétel

randomStateFAE = 2002
# oszlopnevek a minta dataframe-ben
airbnb_price_FAE_minta = pd.DataFrame(columns=oszlopnevek)

# FAE minta dataframe feltöltés
for i in range(mintaDb):
    # mintavétel, replace = True --> FAE
    temp_Minta = airbnb['price'].sample(n=n,replace=True,random_state=randomStateFAE+i)
    temp_Minta.index = oszlopnevek
    # hozzáfűzöm az egy darab mintavétel a df-hez
    airbnb_price_FAE_minta=airbnb_price_FAE_minta.append(temp_Minta, ignore_index=True)


    # EV mintavétel

randomStateEV = 1900
# oszlopnevek a minta dataframe-ben
airbnb_price_EV_minta = pd.DataFrame(columns=oszlopnevek)

# EV minta dataframe feltöltés
for i in range(mintaDb):
    # mintavétel, replace = False --> EV
    temp_Minta = airbnb['price'].sample(n=n,replace=False,random_state=randomStateEV+i)
    temp_Minta.index = oszlopnevek
    # hozzáfűzöm az egy darab mintavétel a df-hez
    airbnb_price_EV_minta=airbnb_price_EV_minta.append(temp_Minta, ignore_index=True)

# 3) AR mintavétel

# arányok kiszámolása
    # régiók
uniqueNeighbourhoodGroups = airbnb.neighbourhood_group.unique()

# arányokhoz df oszlopnevekkel
neighbourhoodGroupsRate = pd.DataFrame(columns=['neighbourhoodGroup','rate'])


for i in range(len(uniqueNeighbourhoodGroups)):
    # new_row --> a régió neve, aránya
    new_row = {'neighbourhoodGroup': uniqueNeighbourhoodGroups[i], 'rate': np.sum(airbnb['neighbourhood_group'] == uniqueNeighbourhoodGroups[i]) / len(airbnb)}
    neighbourhoodGroupsRate.loc[len(neighbourhoodGroupsRate)] = new_row
    
    # körzetek
uniqueNeighbourhoods = airbnb.neighbourhood.unique() 

# arányokhoz df oszlopnevekkel
neighbourhoodsRate = pd.DataFrame(columns=['neighbourhood','rate'])

for i in range(len(uniqueNeighbourhoods)):
    # new_row --> a körzet neve, aránya
    new_row = {'neighbourhood': uniqueNeighbourhoods[i], 'rate': np.sum(airbnb['neighbourhood'] == uniqueNeighbourhoods[i]) / len(airbnb)}
    neighbourhoodsRate.loc[len(neighbourhoodsRate)] = new_row
   
    # szoba típusok
uniqueRoomTypes = airbnb.room_type.unique() 

# arányokhoz df oszlopnevekkel
roomTypesRate = pd.DataFrame(columns=['room_type','rate'])

for i in range(len(uniqueRoomTypes)):
    # new_row --> a szoba típusa, aránya
    new_row = {'room_type': uniqueRoomTypes[i], 'rate': np.sum(airbnb['room_type'] == uniqueRoomTypes[i]) / len(airbnb)}
    roomTypesRate.loc[len(roomTypesRate)] = new_row

# arányok
neighbourhoodGroupsRate
neighbourhoodsRate
roomTypesRate

# AR mintavétel a körzetek alapján
uniqueNeighbourhoodGroups # 5 db

# arányok formázása
aranyok_lista =[x * 100 for x in neighbourhoodGroupsRate['rate'].tolist() ]
aranyok_lista = [ round(x) for x in aranyok_lista] # elemek összege: 100
aranyok_lista    

# oszlopnevek a minta dataframe-ben
airbnb_price_AR_minta = pd.DataFrame(columns=oszlopnevek)
    
randomStateAR = 40

for index in range(mintaDb):
    # egy darab mintavétel df definiálása
    egy_darab_AR_minta = pd.DataFrame()
    # egy darab mintavétel során, annyiszor fut le ez a ciklus, ahány réteg van, jelen esetben 5-ször fog
    for j in range(len(uniqueNeighbourhoodGroups)):
        # a sokaságból az összes olyan kiszedése ami az adott régiójú
        temp_reteg = airbnb.loc[airbnb['neighbourhood_group'] ==f'{uniqueNeighbourhoodGroups[j]}'] 
        # a rétegből EV mintavétel, hozzá tartozó aránnyal
        temp_minta = temp_reteg.sample(n=aranyok_lista[j], random_state = randomStateAR+index, replace=False)
        # hozzáfűzi az új mintát az előzőhöz (itt még minden adat megvan az egyedekről)
        egy_darab_AR_minta = pd.concat([egy_darab_AR_minta,temp_minta], axis=0)
    egy_darab_AR_minta.index = oszlopnevek
    # hozzáfűzi a mintákat tartalmazó df-hez, itt már csak a price marad meg
    airbnb_price_AR_minta = airbnb_price_AR_minta.append(egy_darab_AR_minta['price'], ignore_index=True)
        
# 5

sokasagi_szoras = np.std(airbnb.price)
sokasagi_atlag = np.mean(airbnb.price)
sokasagi_var = sokasagi_szoras ** 2 

airbnb_price_EV_minta['Atlagok'] = np.mean(airbnb_price_EV_minta.iloc[:,0:100], axis=1)
airbnb_price_FAE_minta['Atlagok'] = np.mean(airbnb_price_FAE_minta.iloc[:,0:100], axis=1)
airbnb_price_AR_minta['Atlagok'] = np.mean(airbnb_price_AR_minta.iloc[:,0:100], axis=1)


elvi_mse_atlag_EV = np.sum((airbnb_price_EV_minta.Atlagok - sokasagi_atlag)**2)/mintaDb
elvi_mse_atlag_FAE = np.sum((airbnb_price_FAE_minta.Atlagok - sokasagi_atlag)**2)/mintaDb
elvi_mse_atlag_AR = np.sum((airbnb_price_AR_minta.Atlagok - sokasagi_atlag)**2)/mintaDb

# ellenőrzés a másik képlettel
np.mean((airbnb_price_EV_minta.Atlagok)-sokasagi_atlag)**2 + np.std(airbnb_price_EV_minta.Atlagok)**2
np.mean((airbnb_price_FAE_minta.Atlagok)-sokasagi_atlag)**2 + np.std(airbnb_price_FAE_minta.Atlagok)**2
np.mean((airbnb_price_AR_minta.Atlagok)-sokasagi_atlag)**2 + np.std(airbnb_price_AR_minta.Atlagok)**2


round(np.mean(airbnb_price_EV_minta['Atlagok'])-sokasagi_atlag, 1)
round(np.mean(airbnb_price_FAE_minta['Atlagok'])-sokasagi_atlag, 1)
round(np.mean(airbnb_price_AR_minta['Atlagok'])-sokasagi_atlag, 1)

# 6
mintaatlag_atlag_EV = np.mean(airbnb_price_EV_minta.Atlagok)
mintaatlag_atlag_FAE = np.mean(airbnb_price_FAE_minta.Atlagok)
mintaatlag_atlag_AR = np.mean(airbnb_price_AR_minta.Atlagok)

tapasztalati_mse_atlag_EV = np.sum((airbnb_price_EV_minta.Atlagok - mintaatlag_atlag_EV)**2)/mintaDb
tapasztalati_mse_atlag_FAE = np.sum((airbnb_price_FAE_minta.Atlagok - mintaatlag_atlag_FAE)**2)/mintaDb
tapasztalati_mse_atlag_AR = np.sum((airbnb_price_AR_minta.Atlagok - mintaatlag_atlag_AR)**2)/mintaDb

# 7

mse_eltérések = {
    "EV(elvi-tapasztalati)" : elvi_mse_atlag_EV - tapasztalati_mse_atlag_EV,
    "FAE(elvi-tapasztalati)" : elvi_mse_atlag_FAE - tapasztalati_mse_atlag_FAE,
    "AR(elvi-tapasztalati)" : elvi_mse_atlag_AR - tapasztalati_mse_atlag_AR
}
mse_eltérések

     
# RÉGI KÓDÓK    
###################################################################
    
#reteg1 = airbnb.loc[airbnb['neighbourhood_group'] ==f'{uniqueNeighbourhoodGroups[0]}']
#reteg2 = airbnb.loc[airbnb['neighbourhood_group'] ==f'{uniqueNeighbourhoodGroups[1]}']
#reteg3 = airbnb.loc[airbnb['neighbourhood_group'] ==f'{uniqueNeighbourhoodGroups[2]}']
#reteg4 = airbnb.loc[airbnb['neighbourhood_group'] ==f'{uniqueNeighbourhoodGroups[3]}']
#reteg5 = airbnb.loc[airbnb['neighbourhood_group'] ==f'{uniqueNeighbourhoodGroups[4]}']

#for index in range(mintaDb):
 #   minta1 = reteg1.sample(n=aranyok_lista[0], random_state = randomStateAR+index, replace=False)
    
  #  minta2 = reteg2.sample(n=aranyok_lista[1], random_state = randomStateAR+index, replace=False)
    
 #   minta3 = reteg3.sample(n=aranyok_lista[2], random_state = randomStateAR+index, replace=False)
    
 #   minta4 = reteg4.sample(n=aranyok_lista[3], random_state = randomStateAR+index, replace=False)
    
 #   minta5 = reteg5.sample(n=aranyok_lista[4], random_state = randomStateAR+index, replace=False)
    
 #   egy_darab_AR_minta = pd.concat([minta1, minta2, minta3, minta4, minta5], axis=0)
 #   egy_darab_AR_minta.index = oszlopnevek
    
 #   airbnb_price_AR_minta = airbnb_price_AR_minta.append(egy_darab_AR_minta['price'], ignore_index=True)
    
#airbnb_price_EV_minta['Korrigalatlan_Varianciak'] = np.std(airbnb_price_EV_minta.iloc[:,0:100], axis=1)**2
#airbnb_price_FAE_minta['Korrigalatlan_Varianciak'] = np.std(airbnb_price_FAE_minta.iloc[:,0:100], axis=1)**2
#airbnb_price_AR_minta['Korrigalatlan_Varianciak'] = np.std(airbnb_price_AR_minta.iloc[:,0:100], axis=1)**2

