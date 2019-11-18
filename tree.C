#define tree_cxx
#include "tree.h"
#include <TH2.h>
#include <TStyle.h>
#include <TCanvas.h>
#include <TH1F.h>
#include <TCanvas.h>
#include <vector>
#include <cmath>
#include <Math/PxPyPzE4D.h>
#include <Math/LorentzVector.h>
#include <Math/Vector4D.h>




#define PIONMASS 139.5706 //MeV
#define PROTMASS 938.27803 //MeV
#define CSPEED 299792458 // m/s
#define LAMBDAMASS 1115.683 //MeV


vector<float> PionMomentum;
vector<float> ProtonMomentum;
vector<float> PionMomentumGen;
vector<float> ProtonMomentumGen;
vector<float> PionEnergy;
vector<float> ProtonEnergy;
vector<float> PionEnergyGen;
vector<float> ProtonEnergyGen;
vector<int> PionTrackType;
vector<int> ProtonTrackType;
vector<ROOT::Math::PxPyPzEVector>PionVect4d;
vector<ROOT::Math::PxPyPzEVector>ProtVect4d;
vector<ROOT::Math::PxPyPzEVector>TotVect4d;
vector<ROOT::Math::PxPyPzEVector>PionVect4dGen;
vector<ROOT::Math::PxPyPzEVector>ProtVect4dGen;
vector<ROOT::Math::PxPyPzEVector>TotVect4dGen;
TH1F* h = new TH1F("Mass","Mass",320,1080,1160);
TH1F* h1 = new TH1F("Mass Gen","Mass Gen",192,1114,1117);
TH1F* h2 = new TH1F("LL Mass","LL Mass",320,1080,1160);
TH1F* h3 = new TH1F("LL Mass Gen","LL Mass Gen",192,1114,1117);
TH1F* h4 = new TH1F("DD Mass","DD Mass",320,1080,1160);
TH1F* h5 = new TH1F("DD Mass Gen","DD Mass Gen",192,1114,1117);
TH1F* h6 = new TH1F("Error","Error",600,-30,30);
TH1F* h7 = new TH1F("ErrorGen","ErrorGen",160,-0.4,0.4);






void tree::Loop()
{
	TCanvas* c = new TCanvas("c","c");
	TCanvas* c2 = new TCanvas("c2","c2");
	TCanvas* c3 = new TCanvas("c3","c3");


//   In a ROOT session, you can do:
//      root> .L tree.C
//      root> tree t
//      root> t.GetEntry(12); // Fill t data members with entry number 12
//      root> t.Show();       // Show values of entry 12
//      root> t.Show(16);     // Read and show values of entry 16
//      root> t.Loop();       // Loop on all entries
//

//     This is the loop skeleton where:
//    jentry is the global entry number in the chain
//    ientry is the entry number in the current Tree
//  Note that the argument to GetEntry must be:
//    jentry for TChain::GetEntry
//    ientry for TTree::GetEntry and TBranch::GetEntry
//
//       To read only selected branches, Insert statements like:
// METHOD1:
//    fChain->SetBranchStatus("*",0);  // disable all branches
//    fChain->SetBranchStatus("branchname",1);  // activate branchname
// METHOD2: replace line
//    fChain->GetEntry(jentry);       //read all branches
//by  b_branchname->GetEntry(ientry); //read only this branch
	if (fChain == 0) return;

	Long64_t nentries = fChain->GetEntriesFast();

	Long64_t nbytes = 0, nb = 0;

   	for (Long64_t jentry=0; jentry<nentries;jentry++) {
   		Long64_t ientry = LoadTree(jentry);
   		if (ientry < 0) break;
   		nb = fChain->GetEntry(jentry);   nbytes += nb;
   		// if (Cut(ientry) < 0) continue;
      
    	PionMomentum.push_back(this->hminus_PX*this->hminus_PX + this->hminus_PY*this->hminus_PY + this->hminus_PZ*this->hminus_PZ);
    	ProtonMomentum.push_back(this->hplus_PX*this->hplus_PX + this->hplus_PY*this->hplus_PY + this->hplus_PZ*this->hplus_PZ);

    	PionEnergy.push_back(sqrt(PionMomentum.at(jentry) + pow(PIONMASS,2)));
    	ProtonEnergy.push_back(sqrt(ProtonMomentum.at(jentry) + pow(PROTMASS,2)));
     
    	PionVect4d.push_back(ROOT::Math::PxPyPzEVector(hminus_PX,hminus_PY,hminus_PZ,PionEnergy.at(jentry)));
    	ProtVect4d.push_back(ROOT::Math::PxPyPzEVector(hplus_PX,hplus_PY,hplus_PZ,ProtonEnergy.at(jentry)));

    	PionTrackType.push_back(this->hminus_TRACK_Type);
    	ProtonTrackType.push_back(this->hplus_TRACK_Type);

    	PionMomentumGen.push_back(this->hminus_TRUEP_X*this->hminus_TRUEP_X + this->hminus_TRUEP_Y*this->hminus_TRUEP_Y + this->hminus_TRUEP_Z*this->hminus_TRUEP_Z);
    	ProtonMomentumGen.push_back(this->hplus_TRUEP_X*this->hplus_TRUEP_X + this->hplus_TRUEP_Y*this->hplus_TRUEP_Y + this->hplus_TRUEP_Z*this->hplus_TRUEP_Z);

    	PionEnergyGen.push_back(sqrt(PionMomentumGen.at(jentry) + pow(PIONMASS,2)));
    	ProtonEnergyGen.push_back(sqrt(ProtonMomentumGen.at(jentry) + pow(PROTMASS,2)));
     
    	PionVect4dGen.push_back(ROOT::Math::PxPyPzEVector(hminus_TRUEP_X,hminus_TRUEP_Y,hminus_TRUEP_Z,PionEnergyGen.at(jentry)));
    	ProtVect4dGen.push_back(ROOT::Math::PxPyPzEVector(hplus_TRUEP_X,hplus_TRUEP_Y,hplus_TRUEP_Z,ProtonEnergyGen.at(jentry)));
	}

   	for (int i = 0; i < PionVect4d.size(); ++i)
   	{
   		
   		TotVect4d.push_back(PionVect4d.at(i)+ProtVect4d.at(i));
   		TotVect4dGen.push_back(PionVect4dGen.at(i)+ProtVect4dGen.at(i));
        h->Fill(TotVect4d.at(i).M());
       	h6->Fill(TotVect4d.at(i).M()- LAMBDAMASS);        
        h1->Fill(TotVect4dGen.at(i).M());
        h7->Fill(TotVect4dGen.at(i).M()- LAMBDAMASS);
   	}
   	c->Divide(2,1);
   	c->cd(1);
   	h->Draw();
	
	c->cd(2);
	h1->Draw();
	
   	c->Draw();

   	for (int i = 0; i < PionVect4d.size(); ++i)
   	{
   		if(PionTrackType.at(i) == 3)
   		{
        	h2->Fill(TotVect4d.at(i).M());

        	h3->Fill(TotVect4dGen.at(i).M());


   		}
   		else
   		{
        	h4->Fill(TotVect4d.at(i).M());

        	h5->Fill(TotVect4dGen.at(i).M());   			
   		}
   	}
   	h4->SetLineColor(kGreen);
   	h5->SetLineColor(kGreen);
   	c2->Divide(2,1);
   	c2->cd(1);
   	h2->Draw();
   
   	h4->Draw("SAME");
   
   	c2->cd(2);
   	h3->Draw();

   	h5->Draw("SAME");

   	c2->Draw();
   	c3->Divide(2,1);
   	c3->cd(1);
   	h6->Draw();
   	h6->Fit("gaus");
   	c3->cd(2);
   	h7->Draw();
   	h7->Fit("gaus","","",-0.03,0.04);
   	c3->Draw();
}
