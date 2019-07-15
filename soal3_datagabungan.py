import pandas as pd

dfpoke=pd.read_csv('pokemon.csv',index_col=0)
dfpoke=dfpoke[['Name','HP','Attack','Defense','Sp. Atk','Sp. Def','Speed']]
dfcombats=pd.read_csv('combats.csv')

#df train gabungan 
id1=[]
id2=[]
hp1=[]
hp2=[]
attack1=[]
attack2=[]
defense1=[]
defense2=[]
spatk1=[]
spatk2=[]
spdef1=[]
spdef2=[]
speed1=[]
speed2=[]
winner=[]
for i in range(len(dfcombats)):
    idpoke1=dfcombats.iloc[i]['First_pokemon']
    idpoke2=dfcombats.iloc[i]['Second_pokemon']
    winners=dfcombats.iloc[i]['Winner']
    id1.append(idpoke1)
    id2.append(idpoke2)
    hp1.append(dfpoke.loc[idpoke1]['HP'])
    hp2.append(dfpoke.loc[idpoke2]['HP'])
    attack1.append(dfpoke.loc[idpoke1]['Attack'])
    attack2.append(dfpoke.loc[idpoke2]['Attack'])
    defense1.append(dfpoke.loc[idpoke1]['Defense'])
    defense2.append(dfpoke.loc[idpoke2]['Defense'])
    spatk1.append(dfpoke.loc[idpoke1]['Sp. Atk'])
    spatk2.append(dfpoke.loc[idpoke2]['Sp. Atk'])
    spdef1.append(dfpoke.loc[idpoke1]['Sp. Def'])
    spdef2.append(dfpoke.loc[idpoke2]['Sp. Def'])
    speed1.append(dfpoke.loc[idpoke1]['Speed'])
    speed2.append(dfpoke.loc[idpoke2]['Speed'])
    if winners==idpoke1:
        win=0
        winner.append(win)        #yang menang poke 1
    else:
        win=1
        winner.append(win)        #yang menang poke 2

df=pd.DataFrame(dict(idpoke1=id1,idpoke2=id2,hp1=hp1,hp2=hp2,attack1=attack1,attack2=attack2,defense1=defense1,defense2=defense2,spatk1=spatk1,spatk2=spatk2,spdef1=spdef1,spdef2=spdef2,speed1=speed1,speed2=speed2,winner=winner))
df.to_csv('datatrain.csv')
