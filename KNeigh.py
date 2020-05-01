#!/usr/bin/env python3
# -*- coding: utf-8 -*-
from keras.models import Sequential
# from keras.layers.normalization import BatchNormalization
# from keras.layers.convolutional import Conv2D
# from keras.layers.convolutional import MaxPooling2D
# from keras.layers.core import Activation
from keras.layers.core import Dropout
from keras.layers.core import Dense
# from keras.layers import Flatten
# from keras.layers import Input
# from keras.models import Model
from keras.wrappers.scikit_learn import KerasRegressor
from keras.optimizers import Adam
import numpy as np
import pandas as pd
from sklearn.neighbors import KNeighborsRegressor
from sklearn.tree import DecisionTreeRegressor, ExtraTreeRegressor
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor, AdaBoostRegressor
from sklearn.model_selection import train_test_split, KFold, cross_val_score,GridSearchCV
from sklearn.linear_model import LinearRegression
from sklearn.metrics import mean_squared_error,mean_absolute_error
from sklearn.preprocessing import MinMaxScaler,MaxAbsScaler
from sklearn.svm import SVR
import xgboost as xgb
from xgboost import XGBRegressor
import matplotlib.pyplot as plt
import requests
import time
import argparse


seed = 586
np.random.seed(seed)


down = 0

def data_upload(datapath):
    if("http" in datapath):
        print("Downloading Dataset")
        try:
            # Download
            dataset = requests.get(datapath)
            dataset.raise_for_status()
        except requests.exceptions.RequestException:
            print("Error: Could not download file")
            raise Exception
            return 404
        
        # Writing dataset on disk.    
        with open("datatot.csv","wb") as o:
            o.write(dataset.content)
        datapath = "datatot.csv"
    print("Loading Dataset from Disk")
    try:
        # Reading dataset and creating pandas.DataFrame.
        dataset = pd.read_csv(datapath,index_col=False)
        print("Entries ", len(dataset))        
        
    except Exception:
        raise Exception
        print("Error: File not found or empty")
        return 404
    return dataset
#filename = args.save.replace('.pdf', '') + '_Data.json'
#file = open(filename, 'wb')
#np.savetxt(file, ["Calculated Parameters\n"], "%s")


#### https://drive.google.com/open?id=1pZoeB-J7xMqlkRBNXYEnkug1PZKUmc62  LINK FOR THE DATASET
try:
    data = data_upload("datatree_v3.csv")
except Exception:
    data = data_upload("https://www.dropbox.com/s/vr4ppf3q4h19l14/datatree_v3.csv?dl=1")

if down == 1:
    #Dropping all tracks with Type 3 (long)
    data = data.drop(data[data['hminus_TRACK_Type'] == 3 ].index)
    variables = ["V0_ENDVERTEX_CHI2","V0_ENDVERTEX_Z","V0_ENDVERTEX_Y","hplus_P","hplus_PT","hminus_P","Angle","nDownstreamTracks","V0_ORIVX_X","V0_ORIVX_Z","V0_ORIVX_CHI2","hplus_IP_OWNPV","hplus_TRACK_GhostProb","hminus_TRACK_CHI2NDOF"]
else:
    data = data.drop(data[data['hminus_TRACK_Type'] == 5 ].index)
    variables =  ["V0_ENDVERTEX_Z","hplus_P","hplus_PT","hminus_PT","hminus_PZ","Angle","nLongTracks","V0_ENDVERTEX_CHI2","hplus_TRACK_GhostProb","hminus_TRACK_CHI2NDOF"]

#"V0_ENDVERTEX_Y""nTracks","V0_ORIVX_Y","V0_ORIVX_CHI2"
#  down==1 variables: "V0_ENDVERTEX_CHI2","V0_ENDVERTEX_Z","V0_ENDVERTEX_Y","hplus_P","hplus_PY","hminus_P","Angle","nTracks","V0_ORIVX_X","V0_ORIVX_Z","V0_ORIVX_CHI2","hplus_IP_OWNPV"
#Declaring real masses from pdg
# data= data.drop(["Track_type"],axis=1)
pionm = 139.57061
protonm = 938.272081
lambdam = 1115.683



cs = MaxAbsScaler()

# norm = data.max() - data.min()
# data = data - [data.min()[0],data.min()[1],data.min()[2],data.min()[3],data.min()[4],data.min()[5],0]
# data = data.div([norm[0],norm[1],norm[2],norm[3],norm[4],norm[5],1])

data = data.dropna()
data = data.drop(data[data.Resolution.abs() > 10].index)
datamlp= data[variables]
labelmlp = data["Resolution"].abs()

Xtrain,Xvalid,Ytrain,Yvalid=train_test_split(data[variables],data["Resolution"].abs(),test_size=0.3)
datamlp = cs.fit_transform(datamlp)
Xtrain = cs.transform(Xtrain)
Xvalid = cs.transform(Xvalid)

kf = KFold(n_splits=10,shuffle=True,random_state=seed)
#print(bst.get_params())
def create_mlp(dim=9, regress=True):
        model = Sequential()
        model.add(Dense(20,input_dim=dim,kernel_initializer='random_normal',activation="relu"))
        model.add(Dropout(rate=0.1))
        model.add(Dense(5,activation="relu"))
        #model.add(Dropout(rate=0.1))

        #model.add(Dense(16, activation="relu"))
        opt = Adam(lr=0.001)
    
        
      # # train the model
 	# check to see if the regression node should be added
        if regress:
                model.add(Dense(1, activation="linear"))
                
                
        model.compile(loss="mean_squared_error", optimizer=opt, metrics=['mae'])
        # return our model
        return model
 



def mlp():
    print("------------------MLP----------------------------")
    #model = create_mlp(Xtrain.shape[1], regress=True)
    estimator = KerasRegressor(build_fn=create_mlp, epochs=200, batch_size=10, verbose=2)
    print("[INFO] training model...")
    #estimator.fit(dataset, encoded_labels, epochs=par[0], batch_size=par[1],verbose=2,validation_split=par[2])

    history = estimator.fit(datamlp,labelmlp,epochs=300, batch_size=100,validation_split=0.2,verbose=2)
    #test_score = model.evaluate(Xvalid, Yvalid, batch_size=20)
    #print('Score:', test_score)
    #dtrain=xgb.DMatrix(Xtrain,label=Ytrain)
    #dvalid=xgb.DMatrix(Xvalid,label=Yvalid)
    #print(model.metrics_names)
    
    #'mae','accuracy'
    plt.plot(history.history['mae'])
    plt.plot(history.history['val_mae'])
    plt.title('Model MAE')
    plt.ylabel('MAE')      
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig("Keras_MAE.png")
    plt.clf()
    
    plt.plot(history.history['loss'])
    plt.plot(history.history['val_loss'])
    plt.title('Model loss')
    plt.ylabel('Loss')
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig("Keras_Loss_RMSE.png")
    plt.clf()

def xgbmodel():
    print("------------------------Xgboost------------------------")
    time0 = time.time()
    bst = XGBRegressor(learning_rate=0.005,max_depth=7,n_jobs=-1,n_estimators=2000,num_parallel_tree=13,objective='reg:squarederror',subsample=0.7,early_stopping_rounds=10,random_state=seed,base_score=0)
    trainbst = bst.fit(Xtrain,Ytrain,eval_set=[(Xtrain, Ytrain), (Xvalid, Yvalid)],eval_metric=['rmse','mae'],verbose=True)
    #vali = cross_val_score(trainbst,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
    evres=bst.evals_result() # See MAE metric
    
    #print(vali.mean())
    
    plt.plot(list(evres['validation_0']['rmse']))
    plt.plot(list(evres['validation_1']['rmse']))
    plt.title('Model rmse')
    plt.ylabel('rmse')       
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig("XGBoost_RMSE_v3_newvar_2.png")
    plt.clf()
    
    plt.plot(list(evres['validation_0']['mae']))
    plt.plot(list(evres['validation_1']['mae']))
    plt.title('Model mae')
    plt.ylabel('mae')       
    plt.xlabel('Epoch')
    plt.legend(['Train', 'Test'], loc='upper left')
    plt.savefig("XGBoost_MAE_v3_newvar_2.png")
    plt.clf()
    #print(trainbst.evals_result())
    Y=trainbst.predict(Xvalid)
    print("MSE:",mean_squared_error(Yvalid, Y, squared=False))
    
    print("Executed in %s s" % (time.time() - time0))
    out = pd.DataFrame(Yvalid)
    out2 = pd.DataFrame(Y)
    out.to_csv("xgb_v3_newvar_nom.csv",sep="\t")
    out2.to_csv("xgb_v3_newvar_inf.csv",sep="\t")
    return [Yvalid,Y]

def KNN():
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

# SVM too slow, not accurate
# print("-----------------SVM------------------")
# s=SVR(kernel='poly',verbose=True)
# s.fit(Xtrain,Ytrain)
# print('Score:',s.score(Xvalid,Yvalid))

def dt():
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
    
def gbr():    
    print("----------------------GBR----------------------------")
    gbr=GradientBoostingRegressor(learning_rate=0.1,n_estimators=150,criterion='mse',verbose=1,validation_fraction=0.3)
    gbr.fit(Xtrain,Ytrain)
    valigbr=cross_val_score(gbr,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
    test_score = gbr.score(Xvalid, Yvalid)
    Y=gbr.predict(Xvalid)
    print(test_score)
    print("MSE:",mean_squared_error(Yvalid, Y, squared=False))

def ada():    
    print("----------------------Ada----------------------------")
    t= DecisionTreeRegressor(max_depth=7,criterion='mse')
    ada=AdaBoostRegressor(base_estimator=t,n_estimators=150,random_state=seed)
    ada.fit(Xtrain,Ytrain)
    valiada=cross_val_score(ada,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
    test_score = ada.score(Xvalid, Yvalid)
    Y=ada.predict(Xvalid)
    print(test_score)
    print("MSE:",mean_squared_error(Yvalid, Y, squared=False))
    
    
def RandomForest():
    print("---------------------RandomForest---------------------")
    forests = []
    for md in [2, 5, 7, 8]:
        forest = RandomForestRegressor(max_depth=md,criterion='mse').fit(Xtrain, Ytrain)
        valiForest=cross_val_score(forest,Xvalid,Yvalid,cv=kf,verbose=1,n_jobs=-1)
        test_score = forest.score(Xvalid, Yvalid)
        forests.append([md, valiForest.mean(), test_score])
        Y=forest.predict(Xvalid)
        print(test_score)
        print("MSE:",mean_squared_error(Yvalid, Y, squared=False))
    
    
    forests = pd.DataFrame(forests, columns = ['max_depth', 'cross_val_score', 'test_score'])
    plt.scatter(forests['max_depth'], forests['cross_val_score'])
    plt.scatter(forests['max_depth'], forests['test_score'])
    plt.title('RandomForestRegressor')
    plt.ylabel('max_depth')       
    plt.xlabel('Score')
    plt.legend(['Cross_val', 'Test'], loc='upper left')
    plt.show()
    plt.clf()


def LinRegression():
    print("------------------LinearRegression----------------------------")
    lin_reg = LinearRegression()
    lin_reg.fit(Xtrain,Ytrain)
    print("Parameters: Bias = ",lin_reg.intercept_, "\nCoef. = ", lin_reg.coef_)
    predic =  lin_reg.predict(Xvalid)
    print("Prediction for validation set: ", predic)
    MSE_LinearRegression = 1/len(Yvalid) * np.sum((predic - Yvalid)**2)
    print("Mean Square Error for Linear Regression: \nMSE = ", MSE_LinearRegression)


def hyperparam_search():
    
    param_grid={'learning_rate':[0.001,0.05,0.1,0.2],'max_depth':[4,5,6],'n_estimators':[100,500,1000],'subsample':[0.7,0.8,0.9]}
    bst = XGBRegressor(n_jobs=-1,num_parallel_tree=13,objective='reg:squarederror',early_stopping_rounds=10)
    search = GridSearchCV(bst, param_grid,n_jobs=-1,verbose=51)
    search.fit(Xtrain,Ytrain)
    print(search.best_params_)
    return search.cv_results_
print(xgbmodel())
#a = hyperparam_search()
    # {'learning_rate': 0.2,
    # 'max_depth': 4,
    # 'n_estimators': 1000,
    # 'subsample': 0.7},

# for seed in range(12345,12350):
#     with open("results.txt","a+") as o:
    
#         np.random.seed(seed)
#         print("Seed: ",seed)
#         a = xgbmodel()
#         o.write(str(seed))
#         o.write('\t')
#         o.write(str(a))
#         o.write('\n')
# if __name__ == '__main__':   
#     parser=argparse.ArgumentParser()
#     parser.add_argument('--seed', type=int)
#     pars = parser.parse_args()
#     run(pars)
    
