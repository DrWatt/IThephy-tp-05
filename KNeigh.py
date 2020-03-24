#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from keras.models import Sequential
# from keras.layers.normalization import BatchNormalization
# from keras.layers.convolutional import Conv2D
# from keras.layers.convolutional import MaxPooling2D
# from keras.layers.core import Activation
# from keras.layers.core import Dropout
from keras.layers.core import Dense
# from keras.layers import Flatten
# from keras.layers import Input
# from keras.models import Model
from keras.optimizers import Adam
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
import xgboost as xgb
from xgboost import XGBRegressor
import matplotlib.pyplot as plt


seed = 12345
np.random.seed(seed)

def create_mlp(dim, regress=False):
        model = Sequential()
        model.add(Dense(7,input_dim=dim,kernel_initializer='normal',activation="relu"))
        #model.add(Dense(16, activation="relu"))
        
	# check to see if the regression node should be added
        if regress:
                model.add(Dense(1, activation="linear"))
        # return our model
        return model
 


down = 0
#filename = args.save.replace('.pdf', '') + '_Data.json'
#file = open(filename, 'wb')
#np.savetxt(file, ["Calculated Parameters\n"], "%s")


#### https://drive.google.com/open?id=1pZoeB-J7xMqlkRBNXYEnkug1PZKUmc62  LINK FOR THE DATASET
data = pd.read_csv("datatot.csv",index_col=False)

if down == 1:
    data = data.drop(data[data['hminus_TRACK_Type'] == 3 ].index)
    #Dropping all tracks with Type 3 (long)
else:
    data = data.drop(data[data['hminus_TRACK_Type'] == 5 ].index)

#Declaring real masses from pdg
# data= data.drop(["Track_type"],axis=1)
pionm = 139.57061
protonm = 938.272081
lambdam = 1115.683


variables = ["V0_ENDVERTEX_Z","V0_ENDVERTEX_Y","hplus_P","Angle","nTracks","V0_ORIVX_Z","V0_ORIVX_CHI2","Resolution"]

# units.extend(V0Units)
# units.extend(V0AdvUnits)
# units.extend(LambdaUnits)
# units.extend(hIPUnits)
# units.extend(hplusPUnits)
# units.extend(hminusPUnits)
# units.extend(pseudorapUnits)
# units.extend(transverseUnits)
# units.extend(angleUnits)

# Limits=[]
# for var in variables:
#    tmp = data.sort_values(by=var)
#    tmp = tmp.reset_index(drop=True)
#    if down == 1:
#        lms=[[tmp.loc[0, var],tmp.loc[63751, var],tmp.loc[127503, var],tmp.loc[191255, var]]]
#        rng = 40 #range
#    else:
#        lms=[[tmp.loc[0, var],tmp.loc[26852, var],tmp.loc[53706, var],tmp.loc[80558, var]]]
#        rng = 20
#    Limits.extend(lms)

# LowData = pd.DataFrame()
# InterData = pd.DataFrame()
# HighData = pd.DataFrame()

cs = MinMaxScaler()

# norm = data.max() - data.min()
# data = data - [data.min()[0],data.min()[1],data.min()[2],data.min()[3],data.min()[4],data.min()[5],0]
# data = data.div([norm[0],norm[1],norm[2],norm[3],norm[4],norm[5],1])


# for i in range(len(variables)):
#     LowData = data.drop(data[data["{}".format(variables[i])] >= Limits[i][1]].index)
#     InterData = data.drop(data[(data["{}".format(variables[i])] >= Limits[i][2]) | (data["{}".format(variables[i])] < Limits[i][1])].index)
#     HighData = data.drop(data[(data["{}".format(variables[i])] >= Limits[i][3]) | (data["{}".format(variables[i])] < Limits[i][2])].index)




data = data.dropna()
Xtrain,Xvalid,Ytrain,Yvalid=train_test_split(data[["V0_ENDVERTEX_Z","V0_ENDVERTEX_Y","hplus_P","Angle","nTracks","V0_ORIVX_Z","V0_ORIVX_CHI2","V0_ORIVX_Y"]],data["Resolution"],test_size=0.3)
Xtrain = cs.fit_transform(Xtrain)
Xvalid = cs.transform(Xvalid)

kf = KFold(n_splits=10,shuffle=True,random_state=seed)
#print(bst.get_params())


print("------------------MLP----------------------------")
model = create_mlp(Xtrain.shape[1], regress=True)
opt = Adam(lr=1e-3, decay=1e-3 / 200)
model.compile(loss="mean_squared_error", optimizer=opt, metrics=['mae','accuracy'])
 # # train the model
print("[INFO] training model...")
model.fit(Xtrain, Ytrain, validation_data=(Xvalid, Yvalid),epochs=20, batch_size=20,verbose=True)
test_score =model.evaluate(Xvalid, Yvalid, batch_size=20)
print('Score:', test_score)
#dtrain=xgb.DMatrix(Xtrain,label=Ytrain)
#dvalid=xgb.DMatrix(Xvalid,label=Yvalid)
print(model.metrics_names)


print("------------------------Xgboost------------------------")
bst = XGBRegressor(learning_rate=0.1,max_depth=4,n_jobs=-1,n_estimators=150,num_parallel_tree=10,objective='reg:squarederror',subsample=0.8)
trainbst = bst.fit(Xtrain,Ytrain,eval_set=[(Xtrain, Ytrain), (Xvalid, Yvalid)],eval_metric=['rmse','mae'],verbose=True)
vali = cross_val_score(trainbst,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
evres=bst.evals_result() # See MAE metric

#print(vali.mean())

plt.plot(list(evres['validation_0']['rmse']))
plt.plot(list(evres['validation_1']['rmse']))
plt.title('Model rmse')
plt.ylabel('rmse')       
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show() 
plt.clf()

plt.plot(list(evres['validation_0']['mae']))
plt.plot(list(evres['validation_1']['mae']))
plt.title('Model mae')
plt.ylabel('mae')       
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
plt.show()
plt.clf()
#print(trainbst.evals_result())
Y=trainbst.predict(Xvalid)
print("MSE:",mean_squared_error(Yvalid, Y, squared=False))


print("--------------------KNeighbors-------------------------")
neigh = KNeighborsRegressor(n_neighbors=10,weights='distance',n_jobs=-1)
valiN = cross_val_score(neigh,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
print(valiN.mean())
neigh.fit(Xtrain,Ytrain)
print(neigh.get_params())
print('Score:',neigh.score(Xvalid,Yvalid))
Y=neigh.predict(Xvalid)
print("MSE:",mean_squared_error(Yvalid, Y, squared=False))
# plt.plot(list(evres['validation_0']['rmse']))
# plt.plot(list(evres['validation_1']['rmse']))
# plt.title('Model rmse')
# plt.ylabel('rmse')       
# plt.xlabel('Epoch')
# plt.legend(['Train', 'Test'], loc='upper left')
# #plt.savefig("Keras_NN_Accuracy.png")
# plt.show() 
# plt.clf()

#SVM too slow, not accurate
#print("-----------------SVM------------------")
#s=SVR(kernel='poly',verbose=True)
#s.fit(Xtrain,Ytrain)
#print('Score:',s.score(Xvalid,Yvalid))


print("-----------------DecisionTree-----------------")
trees = []
for md in [2, 5, 7, 8]:
    tree = DecisionTreeRegressor(max_depth=md,criterion='mse').fit(Xtrain, Ytrain)
    valiTree=cross_val_score(tree,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
    test_score = tree.score(Xvalid, Yvalid)
    trees.append([md, valiTree.mean(), test_score])
    Y=tree.predict(Xvalid)
    print(test_score)
    print("MSE:",mean_squared_error(Yvalid, Y, squared=False))
    
trees = pd.DataFrame(trees, columns = ['max_depth', 'cross_val_score', 'test_score'])

plt.scatter(trees['max_depth'], trees['cross_val_score'])
plt.scatter(trees['max_depth'], trees['test_score'])
plt.title('DecisionTreeRegressor')
plt.ylabel('Score')       
plt.xlabel('Max_depth')
plt.legend(['Cross_val', 'Test'], loc='upper left')
plt.show()
plt.clf()


print("----------------------GBR----------------------------")
gbr=GradientBoostingRegressor(learning_rate=0.1,n_estimators=150,criterion='mse',verbose=0,validation_fraction=0.2)
gbr.fit(Xtrain,Ytrain)
valigbr=cross_val_score(gbr,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
test_score = gbr.score(Xvalid, Yvalid)
Y=gbr.predict(Xvalid)
print(test_score)
print("MSE:",mean_squared_error(Yvalid, Y, squared=False))

print("----------------------Ada----------------------------")
t= DecisionTreeRegressor(max_depth=7,criterion='mse')
ada=AdaBoostRegressor(base_estimator=t,n_estimators=150,random_state=seed)
ada.fit(Xtrain,Ytrain)
valiada=cross_val_score(ada,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
test_score = ada.score(Xvalid, Yvalid)
Y=ada.predict(Xvalid)
print(test_score)
print("MSE:",mean_squared_error(Yvalid, Y, squared=False))



print("---------------------RandomForest---------------------")
forests = []
for md in [2, 5, 7, 8]:
    forest = RandomForestRegressor(max_depth=md,criterion='mse').fit(Xtrain, Ytrain)
    valiForest=cross_val_score(forest,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
    test_score = tree.score(Xvalid, Yvalid)
    forests.append([md, valiForest.mean(), test_score])
    Y=forest.predict(Xvalid)
    print(test_score)
    print("MSE:",mean_squared_error(Yvalid, Y, squared=False))


forests = pd.DataFrame(trees, columns = ['max_depth', 'cross_val_score', 'test_score'])
plt.scatter(forests['max_depth'], forests['cross_val_score'])
plt.scatter(forests['max_depth'], forests['test_score'])
plt.title('RandomForestRegressor')
plt.ylabel('max_depth')       
plt.xlabel('Score')
plt.legend(['Cross_val', 'Test'], loc='upper left')
plt.show()
plt.clf()


    
