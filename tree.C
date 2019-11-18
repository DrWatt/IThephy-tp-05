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
vector<float> IPplus;
vector<float> IPminus;
vector<float> chiIPplus;
vector<float> chiIPminus;
vector<double> EndVert;
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
TH1F* h8 = new TH1F("IPplusL","IPplusL",100,0,20);
TH1F* h9 = new TH1F("IPminusL","IPminusL",500,0,100);
TH1F* h10 = new TH1F("chiIPplusL","chiIPplusL",2600,0,2600);
TH1F* h11 = new TH1F("chiIPminusL","chiIPminusL",2400,0,2400);

TH1F* h12 = new TH1F("ZEndVert","ZEndVert",2800,-200,2600);

TH1F* h13 = new TH1F("IPplusD","IPplusD",100,0,20);
TH1F* h14 = new TH1F("IPminusD","IPminusD",500,0,100);
TH1F* h15 = new TH1F("chiIPplusD","chiIPplusD",2600,0,2600);
TH1F* h16 = new TH1F("chiIPminusD","chiIPminusD",2400,0,2400);
TH1F* h17 = new TH1F("ZEndVertD","ZEndVertD",2800,-200,2600);





void tree::Loop()
{
	//TCanvas* c = new TCanvas("c","c");
	//TCanvas* c2 = new TCanvas("c2","c2");
	//TCanvas* c3 = new TCanvas("c3","c3");
  TCanvas* c4 = new TCanvas("c4","c4");
  TCanvas* c5 = new TCanvas("c5","c5");
  TCanvas* c6 = new TCanvas("c6","c6");


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
      float t = jentry/1000.;
      if (t == (int)t) clog <<'\r' << "Entry " << jentry;
      
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

      IPplus.push_back(this->hplus_IP_OWNPV);
      IPminus.push_back(this->hminus_IP_OWNPV);
      chiIPplus.push_back(this->hplus_IPCHI2_OWNPV);
      chiIPminus.push_back(this->hminus_IPCHI2_OWNPV);
      EndVert.push_back(this->V0_ENDVERTEX_Z);

      
	}
  clog <<'\n';
   	for (int i = 0; i < PionVect4d.size(); ++i)
   	{
   		
   		TotVect4d.push_back(PionVect4d.at(i)+ProtVect4d.at(i));
   		TotVect4dGen.push_back(PionVect4dGen.at(i)+ProtVect4dGen.at(i));
      h->Fill(TotVect4d.at(i).M());
      h6->Fill(TotVect4d.at(i).M()- LAMBDAMASS);        
      h1->Fill(TotVect4dGen.at(i).M());
      h7->Fill(TotVect4dGen.at(i).M()- LAMBDAMASS);
      if(PionTrackType.at(i) == 3)
      {
        h8->Fill(IPplus.at(i));
        h9->Fill(IPminus.at(i));
        h10->Fill(chiIPplus.at(i));
        h11->Fill(chiIPminus.at(i));
        h12->Fill(EndVert.at(i));
        h2->Fill(TotVect4d.at(i).M());

        h3->Fill(TotVect4dGen.at(i).M());
      }
      else
      {
        h13->Fill(IPplus.at(i));
        h14->Fill(IPminus.at(i));
        h15->Fill(chiIPplus.at(i));
        h16->Fill(chiIPminus.at(i));
        h17->Fill(EndVert.at(i));

        h4->Fill(TotVect4d.at(i).M());

        h5->Fill(TotVect4dGen.at(i).M());         
      }

      h12->Fill(EndVert.at(i));




   	}
   	//c->Divide(2,1);
   	//c->cd(1);
   	//h->Draw();
    //c->cd(2);
    //h1->Draw();
   	//c->Draw();
   	//h4->SetLineColor(kGreen);
   	//h5->SetLineColor(kGreen);
   	//c2->Divide(2,1);
   	//c2->cd(1);
   	//h2->Draw();
   	//h4->Draw("SAME");
   	//c2->cd(2);
   	//h3->Draw();
   	//h5->Draw("SAME");
   	//c2->Draw();
   	//c3->Divide(2,1);
   	//c3->cd(1);
   	//h6->Draw();
   	//h6->Fit("gaus");
   	//c3->cd(2);
   	//h7->Draw();
   	//h7->Fit("gaus","","",-0.03,0.04);
   	//c3->Draw();
    h13->SetLineColor(kRed);
    h14->SetLineColor(kRed);
    h15->SetLineColor(kRed);
    h16->SetLineColor(kRed);
    h17->SetLineColor(kRed);

    c4->Divide(2,1);
    c4->cd(1);
    h8->Draw();
    h13->Draw("SAME");
    c4->cd(2);
    h9->Draw();
    h14->Draw("SAME");
    c4->Draw();
    c5->Divide(2,1);
    c5->cd(1);
    h10->Draw();
    h15->Draw("SAME");
    c5->cd(2);
    h11->Draw();
    h16->Draw("SAME");
    c5->Draw();
    c6->cd();
    h12->Draw();
    h17->Draw("SAME");
    c6->Draw();
}
