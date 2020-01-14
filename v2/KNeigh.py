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
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import MinMaxScaler
import xgboost as xgb
from xgboost import XGBRegressor


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

data = pd.read_csv("data.csv",index_col=False)

if down == 1:
    data = data.drop(data[data['Track_type'] == 3 ].index)
    #Dropping all tracks with Type 3 (long)
else:
    data = data.drop(data[data['Track_type'] == 5 ].index)

#Declaring real masses from pdg
data= data.drop(["Track_type"],axis=1)
pionm = 139.57061
protonm = 938.272081
lambdam = 1115.683


variables = ["V0_Endvertex_Z","V0_Endvertex_Y","V0_FDCHI2_ORIVX","V0_M","V0_FD_ORIVX","Lambda_E","hplus_IP_OWNPV","hplus_IPCHI2_OWNPV","hplus_P","hminus_P","Angle","Resolution"]


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

Limits=[]
for var in variables:
   tmp = data.sort_values(by=var)
   tmp = tmp.reset_index(drop=True)
   if down == 1:
       lms=[[tmp.loc[0, var],tmp.loc[63751, var],tmp.loc[127503, var],tmp.loc[191255, var]]]
       rng = 40 #range
   else:
       lms=[[tmp.loc[0, var],tmp.loc[26852, var],tmp.loc[53706, var],tmp.loc[80558, var]]]
       rng = 20
   Limits.extend(lms)

LowData = pd.DataFrame()
InterData = pd.DataFrame()
HighData = pd.DataFrame()

cs = MinMaxScaler()

# norm = data.max() - data.min()
# data = data - [data.min()[0],data.min()[1],data.min()[2],data.min()[3],data.min()[4],data.min()[5],0]
# data = data.div([norm[0],norm[1],norm[2],norm[3],norm[4],norm[5],1])


for i in range(len(variables)):
    LowData = data.drop(data[data["{}".format(variables[i])] >= Limits[i][1]].index)
    InterData = data.drop(data[(data["{}".format(variables[i])] >= Limits[i][2]) | (data["{}".format(variables[i])] < Limits[i][1])].index)
    HighData = data.drop(data[(data["{}".format(variables[i])] >= Limits[i][3]) | (data["{}".format(variables[i])] < Limits[i][2])].index)

bst = XGBRegressor(learning_rate=0.1,max_depth=3)



data = data.dropna()

Xtrain,Xvalid,Ytrain,Yvalid=train_test_split(data[["V0_Endvertex_Z","V0_Endvertex_Y","V0_FDCHI2_ORIVX","V0_M","V0_FD_ORIVX","Lambda_E","hplus_IP_OWNPV","hplus_IPCHI2_OWNPV","hplus_P","hminus_P","Angle"]],data["Resolution"],test_size=0.3)

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

#print(bst.get_params())
trainbst = bst.fit(Xtrain,Ytrain,eval_set=[(Xtrain, Ytrain), (Xvalid, Yvalid)])
#print(trainbst.evals_result())

neigh = KNeighborsRegressor(n_neighbors=5,weights='distance',n_jobs=-1)
neigh.fit(Xtrain,Ytrain)
print(neigh.get_params())
print(neigh.score(Xvalid,Yvalid))

