import uproot
import uproot_methods
import numpy as np
import matplotlib
from matplotlib import pyplot as plt
from matplotlib.ticker import AutoMinorLocator, MultipleLocator
from uncertainties import ufloat
from uncertainties.unumpy import nominal_values as noms
from uncertainties.unumpy import std_devs as stds

events = uproot.open("/home/michael/Module/Tandem/Lb_Tuple_presel.root")["tree"]

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

#Invariant Mass
lambda_reco      = proton_reco + pion_reco
lambda_true      = proton_true + pion_true
lambda_true_mass_all = np.array(lambda_true.mass)
lambda_reco_mass_all = np.array(lambda_reco.mass)
