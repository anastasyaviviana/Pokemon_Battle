import pandas as pd

# load model with joblib
import joblib
model=joblib.load('modeljoblib')

df=pd.read_csv('datatesting.csv')
var_x=df.drop(['idpoke1','idpoke2'],axis=1)

df['predict']=model.predict(var_x)
proba=model.predict_proba(var_x)
# print(proba[0,1])
dataproba=[]
for i in range(len(df)):
    if proba[i,0] < proba[i,1]:
        dataproba.append(proba[i,1])
    else:
        dataproba.append(proba[i,0])
df['proba']=dataproba

df.to_csv('hasiltesting.csv')
