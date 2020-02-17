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
#include <TLegend.h>
#include <TGraphErrors.h>
#include <TH2F.h>
#include <fstream>
#include <TObjArray.h>
#include <TObject.h>

void tree::tocsv()
{
	float pionmsq = 139.57061*139.57061;
	float protonmsq = 938.272081*938.272081;
	float lambdam = 1115.683;

	vector<float> hplus_P;
	vector<float> hplus_E;
	vector<float> hminus_P;
	vector<float> hminus_E;
	vector<float> Lambda_E;
	vector<float> hplus_P_TRUE;
	vector<float> hminus_P_TRUE;
	vector<float> hplus_E_TRUE;
	vector<float> hminus_E_TRUE;
	vector<float> Lambda_E_TRUE;
	vector<float> Lambda_PX_TRUE;
	vector<float> Lambda_PY_TRUE;
	vector<float> Lambda_PZ_TRUE;
	vector<float> Lambda_PX;
	vector<float> Lambda_PY;
	vector<float> Lambda_PZ;
	vector<float> Lambda_M;
	vector<float> Lambda_M_TRUE;
	vector<float> Angle;
	vector<float> Resolution;
	ofstream o;
	o.open("datatree2.csv");
	//o << "V0_Endvertex_Z,V0_Endvertex_Y,V0_FDCHI2_ORIVX,V0_M,V0_FD_ORIVX,Lambda_E,hplus_IP_OWNPV,hplus_IPCHI2_OWNPV,hplus_P,hminus_P,Angle,Resolution,Track_type\n";
	if (fChain == 0) return;

	Long64_t nentries = fChain->GetEntriesFast();

	Long64_t nbytes = 0, nb = 0;

	TObjArray* a = fChain->GetListOfLeaves();
	for (int i = 0; i < a->GetEntries(); ++i)
	{
		clog <<a->At(i)->GetName()<< endl;
		o << a->At(i)->GetName() << ',';
	}
	o << "Lambda_E,hplus_P,hminus_P,Angle,Resolution\n";



   	for (Long64_t jentry=0; jentry<nentries;jentry++) {
   		Long64_t ientry = LoadTree(jentry);
   		if (ientry < 0) break;
   		nb = fChain->GetEntry(jentry);   nbytes += nb;
   		// if (Cut(ientry) < 0) continue;

      float t = jentry/1000.;
      if (t == (int)t) clog <<'\r' << "Entry " << jentry;


      hplus_P.push_back(sqrt(hplus_PX*hplus_PX+hplus_PY*hplus_PY+hplus_PZ*hplus_PZ));
	  hplus_E.push_back(sqrt(hplus_P.at(jentry)*hplus_P.at(jentry)+protonmsq));
	  hminus_P.push_back(sqrt(hminus_PX*hminus_PX+hminus_PY*hminus_PY+hminus_PZ*hminus_PZ));
	  hminus_E.push_back(sqrt(hminus_P.at(jentry)*hminus_P.at(jentry)+pionmsq));

	  hplus_P_TRUE.push_back(sqrt(hplus_TRUEP_X*hplus_TRUEP_X+hplus_TRUEP_Y*hplus_TRUEP_Y+hplus_TRUEP_Z*hplus_TRUEP_Z));
	  hminus_P_TRUE.push_back(sqrt(hminus_TRUEP_X*hminus_TRUEP_X+hminus_TRUEP_Y*hminus_TRUEP_Y+hminus_TRUEP_Z*hminus_TRUEP_Z));
	  hplus_E_TRUE.push_back(sqrt(hplus_P_TRUE.at(jentry)*hplus_P_TRUE.at(jentry)+protonmsq));
	  hminus_E_TRUE.push_back(sqrt(hminus_P_TRUE.at(jentry)*hminus_P_TRUE.at(jentry)+pionmsq));

	  Lambda_PX.push_back(hplus_PX+hminus_PX);
	  Lambda_PY.push_back(hplus_PY+hminus_PY);
	  Lambda_PZ.push_back(hplus_PZ+hminus_PZ);

	  Lambda_PX_TRUE.push_back(hplus_TRUEP_X+hminus_TRUEP_X);
	  Lambda_PY_TRUE.push_back(hplus_TRUEP_Y+hminus_TRUEP_Y);
	  Lambda_PZ_TRUE.push_back(hplus_TRUEP_Z+hminus_TRUEP_Z);

	  Lambda_E.push_back(hplus_E.at(jentry)+hminus_E.at(jentry));
	  Lambda_E_TRUE.push_back(hplus_E_TRUE.at(jentry)+hminus_E_TRUE.at(jentry));

	  Angle.push_back(acos((hplus_TRUEP_X*hminus_TRUEP_X+hplus_TRUEP_Y*hminus_TRUEP_Y+hplus_TRUEP_Z*hminus_TRUEP_Z)/(hplus_P_TRUE.at(jentry)*hminus_P_TRUE.at(jentry))));

	  Lambda_M.push_back(sqrt(Lambda_E.at(jentry)*Lambda_E.at(jentry)-(Lambda_PX.at(jentry)*Lambda_PX.at(jentry)+Lambda_PY.at(jentry)*Lambda_PY.at(jentry)+Lambda_PZ.at(jentry)*Lambda_PZ.at(jentry))));
	  Lambda_M_TRUE.push_back(sqrt(Lambda_E_TRUE.at(jentry)*Lambda_E_TRUE.at(jentry)-(Lambda_PX_TRUE.at(jentry)*Lambda_PX_TRUE.at(jentry)+Lambda_PY_TRUE.at(jentry)*Lambda_PY_TRUE.at(jentry)+Lambda_PZ_TRUE.at(jentry)*Lambda_PZ_TRUE.at(jentry))));

	  Resolution.push_back(Lambda_M_TRUE.at(jentry)-Lambda_M.at(jentry));

	
	for (int i = 0; i < a->GetEntries(); ++i)
	{
		o << fChain->GetLeaf(a->At(i)->GetName())->GetValue() << ',';
	}
	  o << Lambda_E.at(jentry) << ',';
	  o << hplus_P.at(jentry) << ',';
	  o << hminus_P.at(jentry) << ',';
	  o << Angle.at(jentry) << ',';
	  o << Resolution.at(jentry) << ',';
	  o << '\n';
	}
	o.close();
}


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
vector<float> EndVertX;
vector<float> EndVertY;
vector<float> EndVertZ;
vector<float> Angle;
vector<int> NTracks;

//vector<float> Resolution;
vector<float> GenResolution;

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
TH1F* h6 = new TH1F("Error","Error",150,-30,30);
TH1F* h7 = new TH1F("ErrorGen","ErrorGen",160,-0.4,0.4);
TH1F* h8 = new TH1F("IPplusL","IPplusL",100,0,20);
TH1F* h9 = new TH1F("IPminusL","IPminusL",125,0,100);
TH1F* h10 = new TH1F("chiIPplusL","chiIPplusL",160,0,2600);
TH1F* h11 = new TH1F("chiIPminusL","chiIPminusL",150,0,2400);

TH1F* h12 = new TH1F("ZEndVert","ZEndVert",175,-200,2600);

TH1F* h13 = new TH1F("IPplusD","IPplusD",100,0,20);
TH1F* h14 = new TH1F("IPminusD","IPminusD",125,0,100);
TH1F* h15 = new TH1F("chiIPplusD","chiIPplusD",160,0,2600);
TH1F* h16 = new TH1F("chiIPminusD","chiIPminusD",150,0,2400);
TH1F* h17 = new TH1F("ZEndVertD","ZEndVertD",175,-200,2600);

TH1F* h18 = new TH1F("AngleL","AngleL",100,0,0.1);
TH1F* h19 = new TH1F("AngleD","AngleD",100,0,0.1);


void tree::Loop()
{
TCanvas* c = new TCanvas("c","c");
	TCanvas* c2 = new TCanvas("c2","c2");
	TCanvas* c3 = new TCanvas("c3","c3");
  TCanvas* c4 = new TCanvas("c4","c4");
  TCanvas* c5 = new TCanvas("c5","c5");
  TCanvas* c6 = new TCanvas("c6","c6");
  TCanvas* c7 = new TCanvas("c7","c7");

  auto time0 = chrono::system_clock::now();


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
      EndVertX.push_back(this->V0_ENDVERTEX_X);
	  EndVertY.push_back(this->V0_ENDVERTEX_Y);
      EndVertZ.push_back(this->V0_ENDVERTEX_Z);


      Angle.push_back(acos((this->hminus_PX*this->hplus_PX+this->hminus_PY*this->hplus_PY+this->hminus_PZ*this->hplus_PZ)/(PionVect4d.at(jentry).R()*ProtVect4d.at(jentry).R())));


	}
  clog <<'\n';
/*

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
        h12->Fill(EndVertZ.at(i));
        h2->Fill(TotVect4d.at(i).M());

        h3->Fill(TotVect4dGen.at(i).M());

        h18->Fill(Angle.at(i));


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

        h19->Fill(Angle.at(i));
      }





   	}
    


   	c->Divide(2,1);
   	c->cd(1);
   	h->Draw();
    c->cd(2);
    h1->Draw();
   	c->Draw();
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
    h13->SetLineColor(kRed);
    h14->SetLineColor(kRed);
    h15->SetLineColor(kRed);
    h16->SetLineColor(kRed);
    h17->SetLineColor(kRed);
    h19->SetLineColor(kRed);

    c4->Divide(2,1);
    c4->cd(1);
    h8->Draw();
    h13->Draw("SAME");
    TLegend* leg = new TLegend(0.6,0.8,0.75,0.9);
    leg->AddEntry(h8);
    leg->AddEntry(h13);
    leg->Draw();
    c4->cd(2);
    h9->Draw();
    h14->Draw("SAME");
    TLegend* leg2 = new TLegend(0.6,0.8,0.75,0.9);
    leg2->AddEntry(h9);
    leg2->AddEntry(h14);
    leg2->Draw();
    c4->Draw();
    c5->Divide(2,1);
    c5->cd(1);
    h10->Draw();
    h15->Draw("SAME");
    TLegend* leg3 = new TLegend(0.6,0.8,0.75,0.9);
    leg3->AddEntry(h10);
    leg3->AddEntry(h15);
    leg3->Draw();
    c5->cd(2);
    h11->Draw();
    h16->Draw("SAME");
    TLegend* leg4 = new TLegend(0.6,0.8,0.75,0.9);
    leg4->AddEntry(h11);
    leg4->AddEntry(h16);
    leg4->Draw();
    c5->Draw();
    c6->cd();
    h12->Draw();
    h17->Draw("SAME");
    TLegend* leg5 = new TLegend(0.6,0.8,0.75,0.9);
    leg5->AddEntry(h12);
    leg5->AddEntry(h17);
    leg5->Draw();
    c6->Draw();


    c7->cd();
    h19->Draw();
    h18->Draw("SAME");
    TLegend* leg6 = new TLegend(0.6,0.8,0.75,0.9);
    leg6->AddEntry(h18);
    leg6->AddEntry(h19);
    leg6->Draw();
    c7->Draw();

    std::chrono::duration<double> elapsed_seconds = chrono::system_clock::now() - time0;
    clog << "Macro executed in " << elapsed_seconds.count() << " seconds\n";
}











void tree::Graphs()
{
/*
  auto time0 = chrono::system_clock::now();

  
  TCanvas* c1 = new TCanvas("c1","c1");
  TCanvas* c2 = new TCanvas("c2","c2");
  TCanvas* c3 = new TCanvas("c3","c3");
  TCanvas* c4 = new TCanvas("c4","c4");
  TCanvas* c5 = new TCanvas("c5","c5");
  TCanvas* c6 = new TCanvas("c6","c6");
  TCanvas* c7 = new TCanvas("c7","c7");
  TCanvas* c8 = new TCanvas("c8","c8");
  TCanvas* c9 = new TCanvas("c9","c9");

  

  TH2F* hh1 = new TH2F ("ResoVsV0","ResoVsV0",100,-200,3000,80,0,80);
  TH2F* hh2 = new TH2F ("GenResoVsV0","GenResoVsV0",100,-200,3000,80,0,80);
  TH2F* hh3 = new TH2F ("ResoVsN","ResoVsN",60,0.5,600.5,80,0,80);
  TH2F* hh4 = new TH2F ("GenResoVsN","GenResoVsN",60,0.5,600.5,80,0,80);
  TH2F* hh5 = new TH2F ("ResoVsAngle","ResoVsAngle",100,0,0.1,80,0,80);
  TH2F* hh6 = new TH2F ("GenResoVsAngle","GenResoVsAngle",100,0,0.1,80,0,80);
  TH2F* hh7 = new TH2F ("ResoVsIPPion","ResoVsIPPion",100,0,100,80,0,80);
  TH2F* hh8 = new TH2F ("GenResoVsIPPion","GenResoVsIPPion",100,0,100,80,0,80);
  TH2F* hh9 = new TH2F ("ResoVsIPProton","ResoVsIPProton",100,0,20,80,0,80);
  TH2F* hh10 = new TH2F ("GenResoVsIPProton","GenResoVsIPProton",100,0,20,80,0,80);
  TH2F* hh11 = new TH2F ("ResoVsChiIPPion","ResoVsChiIPPion",100,0,2400,80,0,80);
  TH2F* hh12 = new TH2F ("GenResoVsChiIPPion","GenResoVsChiIPPion",100,0,2400,80,0,80);
  TH2F* hh13 = new TH2F ("ResoVsChiIPProton","ResoVsChiIPProton",100,0,2600,80,0,80);
  TH2F* hh14 = new TH2F ("GenResoVsChiIPProton","GenResoVsChiIPProton",100,0,2600,80,0,80);
  TH2F* hh15 = new TH2F ("ResoVsPionMom","ResoVsPionMom",100,0,3000,80,0,80);
  TH2F* hh16 = new TH2F ("GenResoVsPionMom","GenResoVsPionMom",100,0,3000,80,0,80);
  TH2F* hh17 = new TH2F ("ResoVsProtonMom","ResoVsProtonMom",100,0,10000,80,0,80);
  TH2F* hh18 = new TH2F ("GenResoVsProtonMom","GenResoVsProtonMom",100,0,10000,80,0,80);



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
      EndVertX.push_back(this->V0_ENDVERTEX_X);
      EndVertY.push_back(this->V0_ENDVERTEX_Y);
      EndVertZ.push_back(this->V0_ENDVERTEX_Z);


      Angle.push_back(acos((this->hminus_PX*this->hplus_PX+this->hminus_PY*this->hplus_PY+this->hminus_PZ*this->hplus_PZ)/(PionVect4d.at(jentry).R()*ProtVect4d.at(jentry).R())));
      NTracks.push_back(this->nTracks);
  }
clog << '\n';
for (int i = 0; i < PionVect4d.size(); ++i)
    {
      
      TotVect4d.push_back(PionVect4d.at(i)+ProtVect4d.at(i));
      TotVect4dGen.push_back(PionVect4dGen.at(i)+ProtVect4dGen.at(i));
      h->Fill(TotVect4d.at(i).M());
      h6->Fill(TotVect4d.at(i).M()- LAMBDAMASS);        
      h1->Fill(TotVect4dGen.at(i).M());
      h7->Fill(TotVect4dGen.at(i).M()- LAMBDAMASS);

      Resolution.push_back(TotVect4d.at(i).M()- LAMBDAMASS);
      GenResolution.push_back(TotVect4dGen.at(i).M()- LAMBDAMASS);

      hh1->Fill(EndVertZ.at(i),abs(Resolution.at(i)));
      hh3->Fill(NTracks.at(i),abs(Resolution.at(i)));
      hh5->Fill(Angle.at(i),abs(Resolution.at(i)));
      hh7->Fill(IPminus.at(i),abs(Resolution.at(i)));
      hh9->Fill(IPplus.at(i),abs(Resolution.at(i)));
      hh11->Fill(chiIPminus.at(i),abs(Resolution.at(i)));
      hh13->Fill(chiIPplus.at(i),abs(Resolution.at(i)));
      hh15->Fill(PionMomentum.at(i)/1000000,abs(Resolution.at(i)));
      hh17->Fill(ProtonMomentum.at(i)/1000000,abs(Resolution.at(i)));

      hh2->Fill(EndVert.at(i),abs(GenResolution.at(i)));
      hh4->Fill(NTracks.at(i),abs(GenResolution.at(i)));
      hh6->Fill(Angle.at(i),abs(GenResolution.at(i)));
      hh8->Fill(IPminus.at(i),abs(GenResolution.at(i)));
      hh10->Fill(IPplus.at(i),abs(GenResolution.at(i)));
      hh12->Fill(chiIPminus.at(i),abs(GenResolution.at(i)));
      hh14->Fill(chiIPplus.at(i),abs(GenResolution.at(i)));
      hh16->Fill(PionMomentum.at(i)/1000000,abs(GenResolution.at(i)));
      hh18->Fill(ProtonMomentum.at(i)/1000000,abs(GenResolution.at(i)));

      if(PionTrackType.at(i) == 3)
      {
        h8->Fill(IPplus.at(i));
        h9->Fill(IPminus.at(i));
        h10->Fill(chiIPplus.at(i));
        h11->Fill(chiIPminus.at(i));
        h12->Fill(EndVertZ.at(i));
        h2->Fill(TotVect4d.at(i).M());

        h3->Fill(TotVect4dGen.at(i).M());

        h18->Fill(Angle.at(i));




      }
      else
      {

        h13->Fill(IPplus.at(i));
        h14->Fill(IPminus.at(i));
        h15->Fill(chiIPplus.at(i));
        h16->Fill(chiIPminus.at(i));
        h17->Fill(EndVertZ.at(i));

        h4->Fill(TotVect4d.at(i).M());

        h5->Fill(TotVect4dGen.at(i).M());         

        h19->Fill(Angle.at(i));



      }
    }



  //TGraphErrors* g = new TGraphErrors(TotVect4d.size(),EndVert.data(),Resolution.data());
  




  //g->GetXaxis()->SetTitle("V0");
  //g->GetYaxis()->SetTitle("Reso");
  hh1->SetXTitle("V0");
  hh1->SetYTitle("Resolution");
  hh2->SetXTitle("V0");
  hh2->SetYTitle("Resolution");

  hh3->SetXTitle("N. Tracks");
  hh3->SetYTitle("Resolution");
  hh4->SetXTitle("N. Tracks");
  hh4->SetYTitle("Resolution");

  hh5->SetXTitle("Angle");
  hh5->SetYTitle("Resolution");
  hh6->SetXTitle("Angle");
  hh6->SetYTitle("Resolution");

  hh7->SetXTitle("IP Pion");
  hh7->SetYTitle("Resolution");
  hh8->SetXTitle("IP Pion");
  hh8->SetYTitle("Resolution");

  hh9->SetXTitle("IP Proton");
  hh9->SetYTitle("Resolution");
  hh10->SetXTitle("IP Proton");
  hh10->SetYTitle("Resolution");

  hh11->SetXTitle("Chi IP Pion");
  hh11->SetYTitle("Resolution");
  hh12->SetXTitle("Chi IP Pion");
  hh12->SetYTitle("Resolution");

  hh13->SetXTitle("Chi IP Proton");
  hh13->SetYTitle("Resolution");
  hh14->SetXTitle("Chi IP Proton");
  hh14->SetYTitle("Resolution");

  hh15->SetXTitle("Pion Momentum");
  hh15->SetYTitle("Resolution");
  hh16->SetXTitle("Pion Momentum");
  hh16->SetYTitle("Resolution");

  hh17->SetXTitle("Proton Momentum");
  hh17->SetYTitle("Resolution");
  hh18->SetXTitle("Proton Momentum");
  hh18->SetYTitle("Resolution");

  gStyle->SetOptStat(0);

//hh1->Scale((1/hh1->Integral()),"width");
//hh2->Scale((1/(271815))*100);
//clog << hh1->Integral() <<endl;

  int k=0;

    for (int i = 1; i < hh1->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh1->GetNbinsY(); ++j)
    {
      k+=hh1->GetBinContent(hh1->GetBin(i,j));
    }

    for (int j = 1; j < hh1->GetNbinsY(); ++j)
    {

      if(k!=0) hh1->SetBinContent(hh1->GetBin(i,j),hh1->GetBinContent(hh1->GetBin(i,j))/k);
    }
    k=0;
    
  }

    for (int i = 1; i < hh3->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh3->GetNbinsY(); ++j)
    {
      k+=hh3->GetBinContent(hh3->GetBin(i,j));
    }

    for (int j = 1; j < hh3->GetNbinsY(); ++j)
    {

      if(k!=0) hh3->SetBinContent(hh3->GetBin(i,j),hh3->GetBinContent(hh3->GetBin(i,j))/k);
    }
    k=0;
    
  }


  for (int i = 1; i < hh5->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh5->GetNbinsY(); ++j)
    {
      k+=hh5->GetBinContent(hh5->GetBin(i,j));
    }

    for (int j = 1; j < hh5->GetNbinsY(); ++j)
    {

      if(k!=0) hh5->SetBinContent(hh5->GetBin(i,j),hh5->GetBinContent(hh5->GetBin(i,j))/k);
    }
    k=0;
    
  }

    for (int i = 1; i < hh7->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh7->GetNbinsY(); ++j)
    {
      k+=hh7->GetBinContent(hh7->GetBin(i,j));
    }

    for (int j = 1; j < hh7->GetNbinsY(); ++j)
    {

      if(k!=0) hh7->SetBinContent(hh7->GetBin(i,j),hh7->GetBinContent(hh7->GetBin(i,j))/k);
    }
    k=0;
    
  }

    for (int i = 1; i < hh9->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh9->GetNbinsY(); ++j)
    {
      k+=hh9->GetBinContent(hh9->GetBin(i,j));
    }

    for (int j = 1; j < hh9->GetNbinsY(); ++j)
    {

      if(k!=0) hh9->SetBinContent(hh9->GetBin(i,j),hh9->GetBinContent(hh9->GetBin(i,j))/k);
    }
    k=0;
    
  }

    for (int i = 1; i < hh11->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh11->GetNbinsY(); ++j)
    {
      k+=hh11->GetBinContent(hh11->GetBin(i,j));
    }

    for (int j = 1; j < hh11->GetNbinsY(); ++j)
    {

      if(k!=0) hh11->SetBinContent(hh11->GetBin(i,j),hh11->GetBinContent(hh11->GetBin(i,j))/k);
    }
    k=0;
    
  }

    for (int i = 1; i < hh13->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh13->GetNbinsY(); ++j)
    {
      k+=hh13->GetBinContent(hh13->GetBin(i,j));
    }

    for (int j = 1; j < hh13->GetNbinsY(); ++j)
    {

      if(k!=0) hh13->SetBinContent(hh13->GetBin(i,j),hh13->GetBinContent(hh13->GetBin(i,j))/k);
    }
    k=0;
    
  }

    for (int i = 1; i < hh15->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh15->GetNbinsY(); ++j)
    {
      k+=hh15->GetBinContent(hh15->GetBin(i,j));
    }

    for (int j = 1; j < hh15->GetNbinsY(); ++j)
    {

      if(k!=0) hh15->SetBinContent(hh15->GetBin(i,j),hh15->GetBinContent(hh15->GetBin(i,j))/k);
    }
    k=0;
    
  }

    for (int i = 1; i < hh17->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh17->GetNbinsY(); ++j)
    {
      k+=hh17->GetBinContent(hh17->GetBin(i,j));
    }

    for (int j = 1; j < hh17->GetNbinsY(); ++j)
    {

      if(k!=0) hh17->SetBinContent(hh17->GetBin(i,j),hh17->GetBinContent(hh17->GetBin(i,j))/k);
    }
    k=0;
    
  }

  for (int i = 1; i < hh2->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh2->GetNbinsY(); ++j)
    {
      k+=hh2->GetBinContent(hh2->GetBin(i,j));
    }

    for (int j = 1; j < hh2->GetNbinsY(); ++j)
    {

      if(k!=0) hh2->SetBinContent(hh2->GetBin(i,j),hh2->GetBinContent(hh2->GetBin(i,j))/k);
    }
    k=0;
    
  }

  for (int i = 1; i < hh4->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh4->GetNbinsY(); ++j)
    {
      k+=hh4->GetBinContent(hh4->GetBin(i,j));
    }

    for (int j = 1; j < hh4->GetNbinsY(); ++j)
    {

      if(k!=0) hh4->SetBinContent(hh4->GetBin(i,j),hh4->GetBinContent(hh4->GetBin(i,j))/k);
    }
    k=0;
    
  }

  for (int i = 1; i < hh6->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh6->GetNbinsY(); ++j)
    {
      k+=hh6->GetBinContent(hh6->GetBin(i,j));
    }

    for (int j = 1; j < hh6->GetNbinsY(); ++j)
    {

      if(k!=0) hh6->SetBinContent(hh6->GetBin(i,j),hh6->GetBinContent(hh6->GetBin(i,j))/k);
    }
    k=0;
    
  }

  for (int i = 1; i < hh8->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh8->GetNbinsY(); ++j)
    {
      k+=hh8->GetBinContent(hh8->GetBin(i,j));
    }

    for (int j = 1; j < hh8->GetNbinsY(); ++j)
    {

      if(k!=0) hh8->SetBinContent(hh8->GetBin(i,j),hh8->GetBinContent(hh8->GetBin(i,j))/k);
    }
    k=0;
    
  }

  for (int i = 1; i < hh10->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh10->GetNbinsY(); ++j)
    {
      k+=hh10->GetBinContent(hh10->GetBin(i,j));
    }

    for (int j = 1; j < hh10->GetNbinsY(); ++j)
    {

      if(k!=0) hh10->SetBinContent(hh10->GetBin(i,j),hh10->GetBinContent(hh10->GetBin(i,j))/k);
    }
    k=0;
    
  }

  for (int i = 1; i < hh12->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh12->GetNbinsY(); ++j)
    {
      k+=hh12->GetBinContent(hh12->GetBin(i,j));
    }

    for (int j = 1; j < hh12->GetNbinsY(); ++j)
    {

      if(k!=0) hh12->SetBinContent(hh12->GetBin(i,j),hh12->GetBinContent(hh12->GetBin(i,j))/k);
    }
    k=0;
    
  }

  for (int i = 1; i < hh14->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh14->GetNbinsY(); ++j)
    {
      k+=hh14->GetBinContent(hh14->GetBin(i,j));
    }

    for (int j = 1; j < hh14->GetNbinsY(); ++j)
    {

      if(k!=0) hh14->SetBinContent(hh14->GetBin(i,j),hh14->GetBinContent(hh14->GetBin(i,j))/k);
    }
    k=0;
    
  }

  for (int i = 1; i < hh16->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh16->GetNbinsY(); ++j)
    {
      k+=hh16->GetBinContent(hh16->GetBin(i,j));
    }

    for (int j = 1; j < hh16->GetNbinsY(); ++j)
    {

      if(k!=0) hh16->SetBinContent(hh16->GetBin(i,j),hh16->GetBinContent(hh16->GetBin(i,j))/k);
    }
    k=0;
    
  }

  for (int i = 1; i < hh18->GetNbinsX(); ++i)
  {
    for (int j = 1; j < hh18->GetNbinsY(); ++j)
    {
      k+=hh18->GetBinContent(hh18->GetBin(i,j));
    }

    for (int j = 1; j < hh18->GetNbinsY(); ++j)
    {

      if(k!=0) hh18->SetBinContent(hh18->GetBin(i,j),hh18->GetBinContent(hh18->GetBin(i,j))/k);
    }
    k=0;
    
  }


  
  
  c1->Divide(2,1);
  c1->cd(1);
  hh1->Draw("colz");
  c1->cd(2);
  hh2->Draw("colz");
  c1->Draw();


  c2->Divide(2,1);
  c2->cd(1);
  hh3->Draw("colz");
  c2->cd(2);
  hh4->Draw("colz");
  c2->Draw();


  c3->Divide(2,1);
  c3->cd(1);
  hh5->Draw("colz");
  c3->cd(2);
  hh6->Draw("colz");
  c3->Draw();
  

  c4->Divide(2,1);
  c4->cd(1);
  hh7->Draw("colz");
  c4->cd(2);
  hh8->Draw("colz");
  c4->Draw();
  

  c5->Divide(2,1);
  c5->cd(1);
  hh9->Draw("colz");
  c5->cd(2);
  hh10->Draw("colz");
  c5->Draw();
  

  c6->Divide(2,1);
  c6->cd(1);
  hh11->Draw("colz");
  c6->cd(2);
  hh12->Draw("colz");
  c6->Draw();
  

  c7->Divide(2,1);
  c7->cd(1);
  hh13->Draw("colz");
  c7->cd(2);
  hh14->Draw("colz");
  c7->Draw();

  c8->Divide(2,1);
  c8->cd(1);
  hh15->Draw("colz");
  c8->cd(2);
  hh16->Draw("colz");
  c8->Draw();

  c9->Divide(2,1);
  c9->cd(1);
  hh17->Draw("colz");
  c9->cd(2);
  hh18->Draw("colz");
  c9->Draw();
  

//TFile* outg = new TFile("graphs.root", "UPDATE");
//    if ( outg->IsOpen() ) printf("File opened successfully\n");
//
//  c1->Write();
//  c2->Write();
//  c3->Write();
//  c4->Write();
//  c5->Write();
//  c6->Write();
//  c7->Write();
//
//outg->Close();

  std::chrono::duration<double> elapsed_seconds = chrono::system_clock::now() - time0;
  clog << "Macro executed in " << elapsed_seconds.count() << " seconds\n";


*/
}
