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
from sklearn.model_selection import train_test_split, KFold, cross_val_score
from sklearn.preprocessing import MinMaxScaler
from sklearn.svm import SVR
import xgboost as xgb
from xgboost import XGBRegressor
import matplotlib.pyplot as plt


seed = 12345
np.random.seed(seed)

def create_mlp(dim, regress=False):
	# define our MLP network
	model = Sequential()
	model.add(Dense(8, input_dim=dim, activation="relu"))
	model.add(Dense(4, activation="relu"))
 
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


# units = [""]
# V0Units = ["", "", "", ""]
# V0AdvUnits = ["MeV / c²", "", ""]
# LambdaUnits = ["MeV"]
# hIPUnits = ["", "", "", ""]
# hplusPUnits = ["MeV / c", "MeV / c", "MeV / c", "MeV / c"]
# hminusPUnits = ["MeV / c", "MeV / c", "MeV / c", "MeV / c"]
# pseudorapUnits = ["", "", "", "", "", "", ""]
# transverseUnits = ["MeV / c", "MeV / c", "MeV / c", "MeV / c","MeV / c","MeV / c"]
# angleUnits = ["rad","rad"]

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

bst = XGBRegressor(learning_rate=0.1,max_depth=4,n_jobs=-1,n_estimators=150,num_parallel_tree=10,objective='reg:squarederror',subsample=0.8)


data = data.dropna()

Xtrain,Xvalid,Ytrain,Yvalid=train_test_split(data[["V0_ENDVERTEX_Z","V0_ENDVERTEX_Y","hplus_P","Angle","nTracks","V0_ORIVX_Z","V0_ORIVX_CHI2","V0_ORIVX_Y"]],data["Resolution"],test_size=0.3)

Xtrain = cs.fit_transform(Xtrain)
Xvalid = cs.transform(Xvalid)

# model = create_mlp(Xtrain.shape[1], regress=True)
# opt = Adam(lr=1e-3, decay=1e-3 / 200)
# model.compile(loss="mean_absolute_percentage_error", optimizer=opt)
 
# # train the model
# print("[INFO] training model...")
# model.fit(Xtrain, Ytrain, validation_data=(Xvalid, Yvalid),
# 	epochs=10, batch_size=20)
#dtrain=xgb.DMatrix(Xtrain,label=Ytrain)
#dvalid=xgb.DMatrix(Xvalid,label=Yvalid)
kf = KFold(n_splits=10,shuffle=True,random_state=seed)
vali = cross_val_score(bst,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
#print(bst.get_params())
print("####################Xgboost")
trainbst = bst.fit(Xtrain,Ytrain,eval_set=[(Xtrain, Ytrain), (Xvalid, Yvalid)],eval_metric=['rmse','mae'],verbose=True)
evres=bst.evals_result() # See MAE metric
print(vali.mean())

plt.plot(list(evres['validation_0']['rmse']))
plt.plot(list(evres['validation_1']['rmse']))
plt.title('Model rmse')
plt.ylabel('rmse')       
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
#plt.savefig("Keras_NN_Accuracy.png")
plt.show() 
plt.clf()

plt.plot(list(evres['validation_0']['mae']))
plt.plot(list(evres['validation_1']['mae']))
plt.title('Model mae')
plt.ylabel('mae')       
plt.xlabel('Epoch')
plt.legend(['Train', 'Test'], loc='upper left')
#plt.savefig("Keras_NN_Accuracy.png")
plt.show()
plt.clf()
    
#print(trainbst.evals_result())
print("####################KNN")
neigh = KNeighborsRegressor(n_neighbors=10,weights='distance',n_jobs=-1)
valiN = cross_val_score(neigh,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
print(valiN.mean())
neigh.fit(Xtrain,Ytrain)
print(neigh.get_params())
print(neigh.score(Xvalid,Yvalid))
# plt.plot(list(evres['validation_0']['rmse']))
# plt.plot(list(evres['validation_1']['rmse']))
# plt.title('Model rmse')
# plt.ylabel('rmse')       
# plt.xlabel('Epoch')
# plt.legend(['Train', 'Test'], loc='upper left')
# #plt.savefig("Keras_NN_Accuracy.png")
# plt.show() 
# plt.clf()
"""
print("##################SVM")
s=SVR(verbose=True)
s.fit(Xtrain,Ytrain)
print(s.score(Xvalid,Yvalid))

"""