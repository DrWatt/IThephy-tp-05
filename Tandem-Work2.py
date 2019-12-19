import ROOT
from ROOT import TGenPhaseSpace, TLorentzVector, TVector3,TGraph
from ROOT import TMath, TCanvas, TH1F, TH2F, TComplex,TStyle,TColor,TChain,TTree,TLegend,TList,TLatex,THStack
import uproot
import uproot_methods
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from array import array


events = uproot.open("/home/camsdiaz/Documents/Tandem/Lb_Tuple_presel.root")["tree"]
num_entries = uproot.numentries("/home/camsdiaz/Documents/Tandem/Lb_Tuple_presel.root", "tree")
L=80559
D=191256
#reconstructed momenta
px_proton_reco, py_proton_reco, pz_proton_reco = events.arrays(["hplus_PX", "hplus_PY", "hplus_PZ"], outputtype=tuple)
px_pion_reco, py_pion_reco, pz_pion_reco       = events.arrays(["hminus_PX", "hminus_PY", "hminus_PZ"], outputtype=tuple)

#true momenta
px_proton_true, py_proton_true, pz_proton_true = events.arrays(["hplus_TRUEP_X", "hplus_TRUEP_Y", "hplus_TRUEP_Z"], outputtype=tuple)
px_pion_true, py_pion_true, pz_pion_true = events.arrays(["hminus_TRUEP_X", "hminus_TRUEP_Y", "hminus_TRUEP_Z"], outputtype=tuple)

#Track type
tracktype_proton, tracktype_pion = events.arrays(["hplus_TRACK_Type", "hminus_TRACK_Type"], outputtype=tuple)

#Cut variables
V0_ENDVERTEX_Z, proton_ip, pion_ip, proton_ipchi2, pion_ipchi2 = events.arrays(["V0_ENDVERTEX_Z", "hplus_IP_OWNPV", "hminus_IP_OWNPV", "hplus_IPCHI2_OWNPV", "hminus_IPCHI2_OWNPV"], outputtype=tuple)


#Mass
m_proton = 938.272
m_pion   = 139.570

#Energy
E_proton_reco = np.sqrt(px_proton_reco**2 + py_proton_reco**2 + pz_proton_reco**2 + m_proton**2)
E_pion_reco   = np.sqrt(px_pion_reco**2 + py_pion_reco**2 + pz_pion_reco**2 + m_pion**2)
E_proton_true = np.sqrt(px_proton_true**2 + py_proton_true**2 + pz_proton_true**2 + m_proton**2)
E_pion_true   = np.sqrt(px_pion_true**2 + py_pion_true**2 + pz_pion_true**2 + m_pion**2)

#LorentzVectors
proton_reco = uproot_methods.TLorentzVectorArray.from_cartesian(px_proton_reco, py_proton_reco, pz_proton_reco, E_proton_reco)
pion_reco   = uproot_methods.TLorentzVectorArray.from_cartesian(px_pion_reco, py_pion_reco, pz_pion_reco, E_pion_reco)
proton_true = uproot_methods.TLorentzVectorArray.from_cartesian(px_proton_true, py_proton_true, pz_proton_true, E_proton_true)
pion_true   = uproot_methods.TLorentzVectorArray.from_cartesian(px_pion_true, py_pion_true, pz_pion_true, E_pion_true)


#Variables(need to add more?)
lambda_reco = proton_reco + pion_reco
lambda_true = proton_true + pion_true

proton_pseudo_reco = np.array(proton_reco.rapidity)
pion_pseudo_reco = np.array(pion_reco.rapidity)
lambda_pseudo_reco = np.array(lambda_reco.rapidity)

proton_transverse_reco = np.array(proton_reco.perp)
pion_transverse_reco = np.array(pion_reco.perp)
lambda_transverse_reco = np.array(lambda_reco.perp)

proton_moment_reco = np.array(proton_reco.p)
pion_moment_reco = np.array(pion_reco.p)
lambda_moment_reco = np.array(lambda_reco.p)

angle_reco = np.arccos((pion_reco.p3.dot(proton_reco.p3))/(proton_reco.p*pion_reco.p))
resolution = np.array(lambda_true.mass-lambda_reco.mass)

variables=[proton_pseudo_reco,pion_pseudo_reco,lambda_pseudo_reco,proton_transverse_reco,pion_transverse_reco,lambda_transverse_reco,proton_moment_reco,pion_moment_reco,lambda_moment_reco,angle_reco,V0_ENDVERTEX_Z, proton_ip, pion_ip, proton_ipchi2, pion_ipchi2]
variables_names=['proton_pseudo_reco','pion_pseudo_reco','lambda_pseudo_reco','proton_transverse_reco','pion_transverse_reco','lambda_transverse_reco','proton_moment_reco','pion_moment_reco','lambda_moment_reco','angle_reco','V0_ENDVERTEX_Z', 'proton_ip', 'pion_ip', 'proton_ipchi2', 'pion_ipchi2']
track_types=[5,3]
track_num=[D,L]

#Histograms(done with root because i found it easier)
for tt,tn in zip(track_types,track_num):
    for var, name in zip(variables, variables_names):
        n=np.argsort(var)
        i=0
        if tn==L:
            hist_double= TH2F("Resolution L vs "+name,"Resolution L vs "+name, 100,var[n[11]],var[n[271700]],100,-45,45)
        else:
            hist_double= TH2F("Resolution D vs "+name,"Resolution D vs "+name, 100,var[n[11]],var[n[271700]],100,-45,45)
        hist1=TH1F("Resolution  vs."+name,"Resolution  vs."+name,100,-40,40)
        hist2=TH1F("2","2",100,-40,40)
        hist3=TH1F("3","3",100,-40,40)
        hist4=TH1F("4","4",100,-40,40)
        hist5=TH1F("5","5",100,-40,40)
        hist6=TH1F("6","6",100,-40,40)
        
        for j in range(0, num_entries):
            if tracktype_proton[n[j]]==tt:
                if i==0:
                    num0=var[n[j]]
                hist_double.Fill(var[n[j]],resolution[n[j]])
                if i<(tn*1)/6:
                    hist1.Fill(resolution[n[j]]) 
                    hist1.SetLineColor(1)
                    num1=var[n[j]]
                elif i>=(tn*1)/6 and i<(tn*2)/6:
                    hist2.Fill(resolution[n[j]])
                    hist2.SetLineColor(2)
                    num2=var[n[j]]
                elif i>=(tn*2)/6 and i<(tn*3)/6:
                    hist3.Fill(resolution[n[j]])
                    hist3.SetLineColor(3)
                    num3=var[n[j]]
                elif i>=(tn*3)/6 and i<(tn*4)/6:
                    hist4.Fill(resolution[n[j]])
                    hist4.SetLineColor(4)
                    num4=var[n[j]]
                elif i>=(tn*4)/6 and i<(tn*5)/6:
                    hist5.Fill(resolution[n[j]])
                    hist5.SetLineColor(6)
                    num5=var[n[j]]
                elif i>=(tn*5)/6 and i<(tn*6)/6:
                    hist6.Fill(resolution[n[j]])
                    hist6.SetLineColor(7)
                    num6=var[n[j]]
                i+=1
        num=[num0,num1,num2,num3,num4,num5,num6]
        print(num)
        hist=[hist1,hist2,hist3,hist4,hist5,hist6]
        zonas=["%.3f" % round(num0,3)+"-"+"%.3f" % round(num1,3),"%.3f" % round(num1,3)+"-"+"%.3f" % round(num2,3),"%.3f" % round(num2,3)+"-"+"%.3f" % round(num3,3),"%.3f" % round(num3,3)+"-"+"%.3f" % round(num4,3),"%.3f" % round(num4,3)+"-"+"%.3f" % round(num5,3),"%.3f" % round(num5,3)+"-"+"%.3f" % round(num6,3)]
        x=array('f')
        std=array('f')
        for i in range(0,6):
            x.append((num[i]+num[i+1])/2)
            std.append(hist[i].GetStdDev())
        plot=TGraph(6, x,std)
        plot.SetTitle( '#sigma zones' )
        plot.SetMarkerStyle(21)
        c=TCanvas ( "c", "c", 1200, 400)
        c.Divide(3,1)
        c.cd(1)
        hist_double.Draw("COL")
        c.cd(2)
        hist1.Draw()
        hist1.SetStats(0)
        hist2.Draw("SAME")
        hist3.Draw("SAME")
        hist4.Draw("SAME")
        hist5.Draw("SAME")
        hist6.Draw("SAME")
        legend1=TLegend(0.65, 0.55, 0.95, 0.85)
        legend1.AddEntry(hist1,zonas[0],"l")
        legend1.AddEntry(hist2,zonas[1],"l")
        legend1.AddEntry(hist3,zonas[2],"l")
        legend1.AddEntry(hist4,zonas[3],"l")
        legend1.AddEntry(hist5,zonas[4],"l")
        legend1.AddEntry(hist6,zonas[5],"l")
        legend1.SetTextSize(0.023)
        legend1.Draw()
        c.cd(3)
        plot.Draw("")
        c.Draw()
        if tn==L:
            c.SaveAs("/home/camsdiaz/Documents/Tandem/work2-findingvariables/plots/"+name+" L.png")
        else:
            c.SaveAs("/home/camsdiaz/Documents/Tandem/work2-findingvariables/plots/"+name+" D.png")
