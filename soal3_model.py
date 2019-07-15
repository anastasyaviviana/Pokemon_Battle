import pandas as pd
from sklearn.linear_model import LogisticRegression

df=pd.read_csv('datatrain.csv')

var_x=df.drop(['Unnamed: 0','idpoke1','idpoke2','winner'],axis=1)
print(var_x.columns.values)
var_y=df['winner']

#splitting to data training and data testing
from sklearn.model_selection import train_test_split
xtrain,xtest,ytrain,ytest=train_test_split(var_x,var_y,test_size=0.1)

model=LogisticRegression(solver='liblinear',multi_class='auto')
model.fit(xtrain,ytrain)
print(model.score(xtest,ytest))  #89,28%

import joblib
joblib.dump(model,'modeljoblib')