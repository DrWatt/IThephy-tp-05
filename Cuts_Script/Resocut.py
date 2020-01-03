import numpy as np
import pandas as pd
import argparse
#import sys
import matplotlib.pyplot as plt
from root_pandas import read_root, to_root
from matplotlib.backends.backend_pdf import PdfPages

#import root_pandas

def main(args):
    #filename = args.save.replace('.pdf', '') + '_Data.json'
    #file = open(filename, 'wb')
    #np.savetxt(file, ["Calculated Parameters\n"], "%s")

    data = read_root(args.file)
    pp = PdfPages(args.save)

    if args.down == 1:
        data = data.drop(data[data['hplus_TRACK_Type'] == 3 ].index)
        #Dropping all tracks with Type 3 (long)
    else:
        data = data.drop(data[data['hplus_TRACK_Type'] == 5 ].index)

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

    data["Lambda_M_TRUE"] = np.sqrt(data.Lambda_E_TRUE**2-(data.Lambda_PX_TRUE**2+data.Lambda_PY_TRUE**2+data.Lambda_PZ_TRUE**2))
    data["Lambda_M"] = np.sqrt(data.Lambda_E**2-(data.Lambda_PX**2+data.Lambda_PY**2+data.Lambda_PZ**2))

    data["Resolution"] = data.Lambda_M_TRUE - data.Lambda_M

    variables = ["nTracks"]
    V0Vars = ["V0_ENDVERTEX_Z", "V0_ENDVERTEX_X", "V0_ENDVERTEX_Y", "V0_ENDVERTEX_CHI2"]
    hIPVars = ["hplus_IP_OWNPV", "hminus_IP_OWNPV", "hplus_IPCHI2_OWNPV", "hminus_IPCHI2_OWNPV"]
    hplusP = ["hplus_PX", "hplus_PY", "hplus_PZ", "hplus_P"]
    variables.extend(V0Vars)
    variables.extend(hIPVars)
    variables.extend(hplusP)

    units = [""]
    V0Units = ["", "", "", ""]
    hIPUnits = ["", "", "", ""]
    hplusPUnits = ["MeV / c", "MeV / c", "MeV / c", "MeV / c"]
    units.extend(V0Units)
    units.extend(hIPUnits)
    units.extend(hplusPUnits)

    Limits = [[0, 167, 333, 500]]#nTracks
    if args.down == 1: #There are other Limits for different Track types
        #Down == 5
        V0Limits = [[-200, 800, 1800, 2800], [-500, -167, 167,500], [-500, -167, 167,500], [0, 5, 10, 15]]
        hIPLimits = [[0,7,14,21], [0,33,67,100], [0,133,267,400], [0,320,640,960]]
        HpPLimits = [[-12000,-4000,4000,12000], [-12000,-4000,4000,12000], [0,58000,106000,175000], [0,58000,106000,175000]]
        rng = 40 #range
    else:
        #Long == 3
        V0Limits = [[-200, 100, 400, 700], [-35, -12, 12, 35], [-35, -12, 12, 35], [0 , 7, 14, 21]]
        hIPLimits = [[0,2,4,6], [0,8,16,24], [0,2000,4000,6000], [0,1000,2000,3000]]
        HpPLimits = [[-9000,-3000,3000,9000], [-8000,-2667,2667,8000], [0,60000,120000,180000], [0,60000,120000,180000]]
        rng = 20
    Limits.extend(V0Limits)
    Limits.extend(hIPLimits)
    Limits.extend(HpPLimits)

    for i in range(len(variables)):
        temp = data.drop(data[data["{}".format(variables[i])] >= Limits[i][1]].index)
        temp2 = data.drop(data[(data["{}".format(variables[i])] >= Limits[i][2]) | (data["{}".format(variables[i])] < Limits[i][1])].index)
        temp3 = data.drop(data[(data["{}".format(variables[i])] >= Limits[i][3]) | (data["{}".format(variables[i])] < Limits[i][2])].index)

        plt.hist(temp["{}".format(variables[i])], bins=83, range=(Limits[i][0], Limits[i][3]), color = 'orange', label='low {}'.format(variables[i]))
        plt.hist(temp2["{}".format(variables[i])], bins=83, range=(Limits[i][0], Limits[i][3]), color = 'green', label='intermediate {}'.format(variables[i]))
        plt.hist(temp3["{}".format(variables[i])], bins=83, range=(Limits[i][0], Limits[i][3]), color = 'steelblue', label='high {}'.format(variables[i]))
        plt.title("Used Intervalls of {}".format(variables[i]))
        if units[i]:
            plt.xlabel("{} / {}".format(variables[i], units[i]))
        else:
            plt.xlabel("{}".format(variables[i]))
        plt.ylabel("Events")
        plt.legend()
        pp.savefig()
        plt.clf()

        plt.hist(temp["Resolution"], bins=100, range=(-rng,rng), color = 'orange', density=True, histtype='step', label='low'.format(variables[i]))
        #pp.savefig()
        #plt.clf()
        plt.hist(temp2["Resolution"], bins=100, range=(-rng,rng), color = 'green', density=True, histtype='step', label='intermediate'.format(variables[i]))
        #pp.savefig()
        #plt.clf()
        plt.hist(temp3["Resolution"], bins=100, range=(-rng,rng), color = 'steelblue', density=True, histtype='step', label='high'.format(variables[i]))

        plt.xlabel("Resolution")
        plt.ylabel("Normalized arbitrary units")
        plt.title("Resolution of used Intervalls of {}".format(variables[i]))
        plt.legend()
        plt.grid()
        pp.savefig()
        plt.clf()
        #np.savetxt(file, [temp["Resolution"].mean()])
        print('-----------------------')
        print("low {} mean:".format(variables[i]), temp["Resolution"].mean())
        print("low {} std:".format(variables[i]), temp["Resolution"].std())
        print("intermediate {} mean:".format(variables[i]), temp2["Resolution"].mean())
        print("intermediate {} std:".format(variables[i]), temp2["Resolution"].std())
        print("high {} mean:".format(variables[i]), temp3["Resolution"].mean())
        print("high {} std:".format(variables[i]), temp3["Resolution"].std())





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
