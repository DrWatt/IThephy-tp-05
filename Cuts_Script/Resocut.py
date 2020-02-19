import numpy as np
import pandas as pd
import argparse
import sys
import math
import matplotlib.pyplot as plt
from root_pandas import read_root, to_root
from matplotlib.backends.backend_pdf import PdfPages
from scipy.optimize import curve_fit

#import root_pandas

def Normal(x, mu, sigma):
    return ((1/(math.sqrt(2*math.pi)*sigma)) * np.exp(-1.0 * (x - mu)**2 / (2 * sigma**2)))
def Linear(x, a, b):
    return a*x+b
def Quadratic(x, a, b, c):
    return a*(x**2)+b*x+c
def Logaritmic(x, a, b, c):
    return a*np.log(b*x)+c
def Exponential(x, a, b, c):
    return a*np.exp(-b*x)+c

def main(args):
    #filename = args.save.replace('.pdf', '') + '_Data.json'
    #file = open(filename, 'wb')
    #np.savetxt(file, ["Calculated Parameters\n"], "%s")

    data = read_root(args.file)
    pp = PdfPages(args.save)

    if args.down == 1:
        data = data.drop(data[data['hplus_TRACK_Type'] == 3 ].index)
        linear=["V0_ENDVERTEX_Z","V0_ENDVERTEX_CHI2","V0_FD_ORIVX","hplus_IP_OWNPV", "hminus_PZ", "hminus_P","hminus_PT_TRUE","hminus_PT","Angle_TRUE","Angle"]
        quadratic=["V0_ENDVERTEX_X", "V0_ENDVERTEX_Y","V0_M","hminus_IP_OWNPV","hplus_IPCHI2_OWNPV", "hminus_IPCHI2_OWNPV","hplus_PX","hminus_PX", "hminus_PY","hplus_eta_TRUE","hplus_eta","Lambda_eta_TRUE","Lambda_eta"]
        exponential=["V0_FDCHI2_ORIVX"]
        logaritmic=["hplus_PT_TRUE","hplus_PT","Angle_TRUE","Angle","hplus_PZ", "hplus_P","hplus_PZ", "hplus_P","Lambda_E"]

    else:
        data = data.drop(data[data['hplus_TRACK_Type'] == 5 ].index)
        linear=['nTracks',"Lambda_E","hminus_IP_OWNPV","hminus_IPCHI2_OWNPV","hminus_PZ", "hminus_P","hminus_eta_TRUE","hminus_eta","hplus_PT_TRUE","hplus_PT"]
        quadratic=["V0_ENDVERTEX_X", "V0_ENDVERTEX_Y","V0_M","hminus_PX",'hplus_PY',"Angle_TRUE","Angle","hplus_eta_TRUE","hplus_eta"]
        exponential=["hplus_IP_OWNPV","hplus_eta_TRUE","hplus_eta","hminus_eta_TRUE","hminus_eta","Lambda_eta_TRUE","Lambda_eta"]
        logaritmic=["hplus_PZ", "hplus_P"]

    #Declaring real masses from pdg
    pionm = 139.57061
    protonm = 938.272081
    lambdam = 1115.683

    #Preparing the Mass and Resolution
    data["hplus_P_TRUE"] = np.sqrt(data.hplus_TRUEP_X**2+data.hplus_TRUEP_Y**2+data.hplus_TRUEP_Z**2)
    data["hminus_P_TRUE"] = np.sqrt(data.hminus_TRUEP_X**2+data.hminus_TRUEP_Y**2+data.hminus_TRUEP_Z**2)
    data["hplus_P"] = np.sqrt(data.hplus_PX**2+data.hplus_PY**2+data.hplus_PZ**2)
    data["hminus_P"] = np.sqrt(data.hminus_PX**2+data.hminus_PY**2+data.hminus_PZ**2)

    data["hplus_E_TRUE"] = np.sqrt(data.hplus_P_TRUE**2+protonm**2)
    data["hminus_E_TRUE"] = np.sqrt(data.hminus_P_TRUE**2+pionm**2)
    data["hplus_E"] = np.sqrt(data.hplus_P**2+protonm**2)
    data["hminus_E"] = np.sqrt(data.hminus_P**2+pionm**2)

    data["Lambda_E_TRUE"] = data.hplus_E_TRUE+data.hminus_E_TRUE
    data["Lambda_E"] = data.hplus_E+data.hminus_E

    data["Lambda_PX_TRUE"] = data.hplus_TRUEP_X+data.hminus_TRUEP_X
    data["Lambda_PY_TRUE"] = data.hplus_TRUEP_Y+data.hminus_TRUEP_Y
    data["Lambda_PZ_TRUE"] = data.hplus_TRUEP_Z+data.hminus_TRUEP_Z
    data["Lambda_PX"] = data.hplus_PX+data.hminus_PX
    data["Lambda_PY"] = data.hplus_PY+data.hminus_PY
    data["Lambda_PZ"] = data.hplus_PZ+data.hminus_PZ

    data["hplus_eta_TRUE"]=0.5*np.log(data.hplus_E_TRUE+data.hplus_TRUEP_Z/data.hplus_E_TRUE-data.hplus_TRUEP_Z)
    data["hplus_eta"]=0.5*np.log(data.hplus_E+data.hplus_PZ/data.hplus_E-data.hplus_PZ)
    data["hminus_eta_TRUE"]=0.5*np.log(data.hminus_E_TRUE+data.hminus_TRUEP_Z/data.hminus_E_TRUE-data.hminus_TRUEP_Z)
    data["hminus_eta"]=0.5*np.log(data.hminus_E+data.hminus_PZ/data.hminus_E-data.hminus_PZ)
    data["Lambda_eta_TRUE"]=0.5*np.log(data.Lambda_E_TRUE+data.Lambda_PZ_TRUE/data.Lambda_E_TRUE-data.Lambda_PZ_TRUE)
    data["Lambda_eta"]=0.5*np.log(data.Lambda_E+data.Lambda_PZ/data.Lambda_E-data.Lambda_PZ)

    data["hplus_PT_TRUE"]=np.sqrt(data.hplus_TRUEP_X**2+data.hplus_TRUEP_Y**2)
    data["hplus_PT"]=np.sqrt(data.hplus_PX**2+data.hplus_PY**2)
    data["hminus_PT_TRUE"]=np.sqrt(data.hminus_TRUEP_X**2+data.hminus_TRUEP_Y**2)
    data["hminus_PT"]=np.sqrt(data.hminus_PX**2+data.hminus_PY**2)
    data["Lambda_PT_TRUE"]=np.sqrt(data.Lambda_PX_TRUE**2+data.Lambda_PY_TRUE**2)
    data["Lambda_PT"]=np.sqrt(data.Lambda_PX**2+data.Lambda_PY**2)

    data["Angle_TRUE"]=np.arccos((data.hplus_TRUEP_X*data.hminus_TRUEP_X+data.hplus_TRUEP_Y*data.hminus_TRUEP_Y+data.hplus_TRUEP_Z*data.hminus_TRUEP_Z)/(data.hplus_P_TRUE*data.hminus_P_TRUE))
    data["Angle"]=np.arccos((data.hplus_TRUEP_X*data.hminus_TRUEP_X+data.hplus_TRUEP_Y*data.hminus_TRUEP_Y+data.hplus_TRUEP_Z*data.hminus_TRUEP_Z)/(data.hplus_P_TRUE*data.hminus_P_TRUE))


    data["Lambda_M_TRUE"] = np.sqrt(data.Lambda_E_TRUE**2-(data.Lambda_PX_TRUE**2+data.Lambda_PY_TRUE**2+data.Lambda_PZ_TRUE**2))
    data["Lambda_M"] = np.sqrt(data.Lambda_E**2-(data.Lambda_PX**2+data.Lambda_PY**2+data.Lambda_PZ**2))

    data["Resolution"] = data.Lambda_M_TRUE - data.Lambda_M

    variables = ["nTracks"]
    V0Vars = ["V0_ENDVERTEX_Z", "V0_ENDVERTEX_X", "V0_ENDVERTEX_Y", "V0_ENDVERTEX_CHI2"]
    V0Advanced = ["V0_M", "V0_FD_ORIVX", "V0_FDCHI2_ORIVX"]
    Lambdavars = ["Lambda_E"]
    hIPVars = ["hplus_IP_OWNPV", "hminus_IP_OWNPV", "hplus_IPCHI2_OWNPV", "hminus_IPCHI2_OWNPV"]
    hplusP = ["hplus_PX", "hplus_PY", "hplus_PZ", "hplus_P"]
    hminusP = ["hminus_PX", "hminus_PY", "hminus_PZ", "hminus_P"]
    pseudorap = ["hplus_eta_TRUE","hplus_eta","hminus_eta_TRUE","hminus_eta","Lambda_eta_TRUE","Lambda_eta"]
    transverse = ["hplus_PT_TRUE","hplus_PT","hminus_PT_TRUE","hminus_PT","Lambda_PT_TRUE","Lambda_PT"]
    angle = ["Angle_TRUE","Angle"]

    variables.extend(V0Vars)
    variables.extend(V0Advanced)
    variables.extend(Lambdavars)
    variables.extend(hIPVars)
    variables.extend(hplusP)
    variables.extend(hminusP)
    variables.extend(pseudorap)
    variables.extend(transverse)
    variables.extend(angle)

    units = [""]
    V0Units = ["", "", "", ""]
    V0AdvUnits = ["MeV / c²", "", ""]
    LambdaUnits = ["MeV"]
    hIPUnits = ["", "", "", ""]
    hplusPUnits = ["MeV / c", "MeV / c", "MeV / c", "MeV / c"]
    hminusPUnits = ["MeV / c", "MeV / c", "MeV / c", "MeV / c"]
    pseudorapUnits = ["", "", "", "", "", "", ""]
    transverseUnits = ["MeV / c", "MeV / c", "MeV / c", "MeV / c","MeV / c","MeV / c"]
    angleUnits = ["rad","rad"]

    units.extend(V0Units)
    units.extend(V0AdvUnits)
    units.extend(LambdaUnits)
    units.extend(hIPUnits)
    units.extend(hplusPUnits)
    units.extend(hminusPUnits)
    units.extend(pseudorapUnits)
    units.extend(transverseUnits)
    units.extend(angleUnits)

    Limits=[]
    for var in variables:
       tmp = data.sort_values(by=[var])
       tmp = tmp.reset_index(drop=True)
       if args.down == 1:
           lms=[[tmp.loc[0, var],tmp.loc[31875 ,var],tmp.loc[63751, var],tmp.loc[95627, var],tmp.loc[127503, var],tmp.loc[159379, var],tmp.loc[191255, var]]]
           rng = 40 #range
       else:
           lms=[[tmp.loc[0, var],tmp.loc[13426, var],tmp.loc[26852, var],tmp.loc[40279, var],tmp.loc[53706, var],tmp.loc[67132, var],tmp.loc[80558, var]]]
           rng = 20
       Limits.extend(lms)


    """Limits = [[0, 167, 333, 500]]#nTracks
    if args.down == 1: #There are other Limits for different Track types
        #Down == 5
        V0Limits = [[-200, 800, 1800, 2800], [-500, -167, 167,500], [-500, -167, 167,500], [0, 5, 10, 15]]
        V0AdvLimits = [[1101,1111,1121,1131], [0,900,1800,2700], [-3000,8000,19000,30000]]
        LambdaLimits = [[0,67000,134000,200000]]
        hIPLimits = [[0,7,14,21], [0,33,67,100], [0,133,267,400], [0,320,640,960]]
        HpPLimits = [[-12000,-4000,4000,12000], [-12000,-4000,4000,12000], [0,58000,106000,175000], [0,58000,106000,175000]]
        HmPLimits = [[-2500,-800,800,2500], [-2500,-800,800,2500], [0,12000,24000,36000], [0,12000,24000,36000]]
        rng = 40 #range
    else:
        #Long == 3
        V0Limits = [[-200, 100, 400, 700], [-35, -12, 12, 35], [-35, -12, 12, 35], [0 , 2.3, 4.7, 7]]
        V0AdvLimits = [[1104,1112,1120,1128], [0,233,467,700], [-3000,8000,19000,30000]]
        LambdaLimits = [[0,67000,134000,200000]]
        hIPLimits = [[0,2,4,6], [0,8,16,24], [0,2000,4000,6000], [0,1000,2000,3000]]
        HpPLimits = [[-9000,-3000,3000,9000], [-8000,-2667,2667,8000], [0,60000,120000,180000], [0,60000,120000,180000]]
        HmPLimits = [[-1800,-600,600,1800], [-1800,-600,600,1800], [0,12000,24000,36000], [0,12000,24000,36000]]
        rng = 20
    Limits.extend(V0Limits)
    Limits.extend(V0AdvLimits)
    Limits.extend(LambdaLimits)
    Limits.extend(hIPLimits)
    Limits.extend(HpPLimits)
    Limits.extend(HmPLimits)"""


    for i in range(len(variables)):
        temp = data.drop(data[data["{}".format(variables[i])] >= Limits[i][1]].index)
        temp2 = data.drop(data[(data["{}".format(variables[i])] >= Limits[i][2]) | (data["{}".format(variables[i])] < Limits[i][1])].index)
        temp3 = data.drop(data[(data["{}".format(variables[i])] >= Limits[i][3]) | (data["{}".format(variables[i])] < Limits[i][2])].index)
        temp4 = data.drop(data[(data["{}".format(variables[i])] >= Limits[i][4]) | (data["{}".format(variables[i])] < Limits[i][3])].index)
        temp5 = data.drop(data[(data["{}".format(variables[i])] >= Limits[i][5]) | (data["{}".format(variables[i])] < Limits[i][4])].index)
        temp6 = data.drop(data[(data["{}".format(variables[i])] >= Limits[i][6]) | (data["{}".format(variables[i])] < Limits[i][5])].index)


        plt.hist(temp["{}".format(variables[i])], bins=50, range=(Limits[i][0], Limits[i][6]), color = 'orange', label='low {}'.format(variables[i]))
        plt.hist(temp2["{}".format(variables[i])], bins=50, range=(Limits[i][0], Limits[i][6]), color = 'green', label='low intermediate {}'.format(variables[i]))
        plt.hist(temp3["{}".format(variables[i])], bins=50, range=(Limits[i][0], Limits[i][6]), color = 'red', label='intermediate {}'.format(variables[i]))
        plt.hist(temp4["{}".format(variables[i])], bins=50, range=(Limits[i][0], Limits[i][6]), color = 'steelblue', label='high intermediate {}'.format(variables[i]))
        plt.hist(temp5["{}".format(variables[i])], bins=50, range=(Limits[i][0], Limits[i][6]), color = 'darkviolet', label='high {}'.format(variables[i]))
        plt.hist(temp5["{}".format(variables[i])], bins=50, range=(Limits[i][0], Limits[i][6]), color = 'navy', label='very high {}'.format(variables[i]))
        plt.title("Used Intervalls of {}".format(variables[i]))
        if units[i]:
            plt.xlabel("{} / {}".format(variables[i], units[i]))
        else:
            plt.xlabel("{}".format(variables[i]))
        plt.ylabel("Events")
        plt.legend()
        pp.savefig()
        plt.clf()

        (n1,bins1,patches1)=plt.hist(temp["Resolution"], bins=100, range=(-rng,rng), color='orange', density=True, histtype='step', label='low'.format(variables[i]))
        (n2,bins2,patches2)=plt.hist(temp2["Resolution"], bins=100, range=(-rng,rng), color='green', density=True, histtype='step', label='low intermediate'.format(variables[i]))
        (n3,bins3,patches3)=plt.hist(temp3["Resolution"], bins=100, range=(-rng,rng), color='red', density=True, histtype='step', label='intermediate'.format(variables[i]))
        (n4,bins4,patches4)=plt.hist(temp4["Resolution"], bins=100, range=(-rng,rng), color='steelblue', density=True, histtype='step', label='high intermediate'.format(variables[i]))
        (n5,bins5,patches5)=plt.hist(temp5["Resolution"], bins=100, range=(-rng,rng), color='darkviolet', density=True, histtype='step', label='high'.format(variables[i]))
        (n6,bins6,patches6)=plt.hist(temp6["Resolution"], bins=100, range=(-rng,rng), color='navy', density=True, histtype='step', label='very high'.format(variables[i]))

        binscenters = np.array([0.5 * (bins1[j] + bins1[j]) for j in range(len(bins1)-1)])
        xspace = np.linspace(-rng, rng, 100000)

        popt1, pcov1 = curve_fit(Normal, xdata=binscenters, ydata=n1)
        plt.plot(xspace, Normal(xspace, *popt1), color='orange', linewidth=0.5)
        popt2, pcov2 = curve_fit(Normal, xdata=binscenters, ydata=n2)
        plt.plot(xspace, Normal(xspace, *popt2), color='green', linewidth=0.5)
        popt3, pcov3 = curve_fit(Normal, xdata=binscenters, ydata=n3)
        plt.plot(xspace, Normal(xspace, *popt3), color='red', linewidth=0.5)
        popt4, pcov4 = curve_fit(Normal, xdata=binscenters, ydata=n4)
        plt.plot(xspace, Normal(xspace, *popt4), color='steelblue', linewidth=0.5)
        popt5, pcov5 = curve_fit(Normal, xdata=binscenters, ydata=n5)
        plt.plot(xspace, Normal(xspace, *popt5), color='darkviolet', linewidth=0.5)
        popt6, pcov6 = curve_fit(Normal, xdata=binscenters, ydata=n6)
        plt.plot(xspace, Normal(xspace, *popt6), color='navy', linewidth=0.5)

        perr1 = np.sqrt(np.diag(pcov1))
        perr2 = np.sqrt(np.diag(pcov2))
        perr3 = np.sqrt(np.diag(pcov3))
        perr4 = np.sqrt(np.diag(pcov4))
        perr5 = np.sqrt(np.diag(pcov5))
        perr6 = np.sqrt(np.diag(pcov6))

        plt.xlabel("Resolution")
        plt.ylabel("Normalized arbitrary units")
        plt.title("Resolution of used Intervalls of {}".format(variables[i]))
        plt.legend()
        plt.grid()
        pp.savefig()
        plt.clf()

        zone=[temp["{}".format(variables[i])],temp2["{}".format(variables[i])],temp3["{}".format(variables[i])],temp4["{}".format(variables[i])],temp5["{}".format(variables[i])],temp6["{}".format(variables[i])]]
        x=np.array([zone[j].mean() for j in range(0,6)])
        resolution=np.array([popt1[1], popt2[1], popt3[1],popt4[1],popt5[1],popt6[1]])
        error = np.array([perr1[1], perr2[1], perr3[1], perr4[1], perr5[1], perr6[1]])
        fitRange= np.linspace(x[0], x[5], 100000)

        plt.scatter(x,resolution, color=['orange', 'green', 'red', 'steelblue', 'darkviolet', 'navy'], marker = 'o')
        plt.errorbar(x, resolution, yerr=error, ecolor=['orange', 'green', 'red', 'steelblue', 'darkviolet', 'navy'], linestyle='none')
        if variables[i] in linear:
            popt, pcov = curve_fit(Linear, xdata=x, ydata=resolution)
            plt.plot(fitRange, Linear(fitRange, *popt), color='black', linewidth=0.8, label='linear fit',linestyle='-')
        if variables[i] in quadratic:
            popt, pcov = curve_fit(Quadratic, xdata=x, ydata=resolution)
            plt.plot(fitRange, Quadratic(fitRange, *popt), color='black', linewidth=0.8,label='quadratic fit',linestyle='--')
        if variables[i] in exponential:
            popt, pcov = curve_fit(Exponential, xdata=x, ydata=resolution)
            plt.plot(fitRange, Exponential(fitRange, *popt), color='black', linewidth=0.8,label='exponential fit',linestyle='-.')
        if variables[i] in logaritmic:
            popt, pcov = curve_fit(Logaritmic, xdata=x, ydata=resolution)
            plt.plot(fitRange, Logaritmic(fitRange, *popt), color='black', linewidth=0.8,label='logaritmic fit',linestyle=':')


        if units[i]:
            plt.xlabel("Mean of intervall of {} / {}".format(variables[i], units[i]))
        else:
            plt.xlabel("Mean of intervall of {}".format(variables[i]))
        plt.ylabel("Mean of Resolution in normalized arbitrary units")
        plt.title("Quantified Resolution of used Intervalls of {}".format(variables[i]))
        plt.grid()
        plt.legend()
        pp.savefig()
        plt.clf()


        #np.savetxt(file, [temp["Resolution"].mean()])
        print('-----------------------')
        print("low {} mean:".format(variables[i]), temp["Resolution"].mean())
        print("low {} std:".format(variables[i]), temp["Resolution"].std())
        print("low intermediate {} mean:".format(variables[i]), temp2["Resolution"].mean())
        print("low intermediate {} std:".format(variables[i]), temp2["Resolution"].std())
        print("intermediate {} mean:".format(variables[i]), temp3["Resolution"].mean())
        print("intermediate {} std:".format(variables[i]), temp3["Resolution"].std())
        print("high intermediate {} mean:".format(variables[i]), temp4["Resolution"].mean())
        print("high intermediate {} std:".format(variables[i]), temp4["Resolution"].std())
        print("high {} mean:".format(variables[i]), temp5["Resolution"].mean())
        print("high {} std:".format(variables[i]), temp5["Resolution"].std())
        print("very high {} mean:".format(variables[i]), temp6["Resolution"].mean())
        print("very high {} std:".format(variables[i]), temp6["Resolution"].std())





    pp.close()
    #file.close()

if __name__ == '__main__':

    parser = argparse.ArgumentParser()
    parser.add_argument('--save', help='Where to store .pdf')
    parser.add_argument('--file', nargs='+', type=str, help='Name the location of the Tuple', default='Lb_Tuple_presel_v2.root')
    parser.add_argument('--tree', help='Name of tree should it differ from tree', default='tree')
    parser.add_argument('--down', action='store_true', help='If flagged use downstream tracks')
    args = parser.parse_args()
    main(args)
