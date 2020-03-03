//////////////////////////////////////////////////////////
// This class has been automatically generated on
// Thu Dec 19 11:49:38 2019 by ROOT version 6.18/04
// from TTree tree/tree
// found on file: Lb_Tuple_presel_v2.root
//////////////////////////////////////////////////////////

#ifndef tree_h
#define tree_h

#include <TROOT.h>
#include <TChain.h>
#include <TFile.h>

// Header file for the classes stored in the TTree if any.

class tree {
public :
   TTree          *fChain;   //!pointer to the analyzed TTree or TChain
   Int_t           fCurrent; //!current Tree number in a TChain

// Fixed size dimensions of array or collections stored in the TTree if any.

   // Declaration of leaf types
   Double_t        hplus_PX;
   Double_t        hplus_PY;
   Double_t        hplus_PZ;
   Double_t        hminus_PX;
   Double_t        hminus_PY;
   Double_t        hminus_PZ;
   Double_t        hplus_TRUEP_X;
   Double_t        hplus_TRUEP_Y;
   Double_t        hplus_TRUEP_Z;
   Double_t        hminus_TRUEP_X;
   Double_t        hminus_TRUEP_Y;
   Double_t        hminus_TRUEP_Z;
   Int_t           nTracks;
   Double_t        hplus_IP_OWNPV;
   Double_t        hminus_IP_OWNPV;
   Double_t        hplus_IPCHI2_OWNPV;
   Double_t        hminus_IPCHI2_OWNPV;
   Int_t           hplus_TRACK_Type;
   Int_t           hminus_TRACK_Type;
   Double_t        V0_ENDVERTEX_X;
   Double_t        V0_ENDVERTEX_Y;
   Double_t        V0_ENDVERTEX_Z;
   Double_t        V0_ENDVERTEX_CHI2;
   Double_t        V0_M;
   Double_t        V0_ORIVX_X;
   Double_t        V0_ORIVX_Y;
   Double_t        V0_ORIVX_Z;
   Double_t        V0_ORIVX_CHI2;
   Double_t        V0_FD_ORIVX;
   Double_t        V0_FDCHI2_ORIVX;

   // List of branches
   TBranch        *b_hplus_PX;   //!
   TBranch        *b_hplus_PY;   //!
   TBranch        *b_hplus_PZ;   //!
   TBranch        *b_hminus_PX;   //!
   TBranch        *b_hminus_PY;   //!
   TBranch        *b_hminus_PZ;   //!
   TBranch        *b_hplus_TRUEP_X;   //!
   TBranch        *b_hplus_TRUEP_Y;   //!
   TBranch        *b_hplus_TRUEP_Z;   //!
   TBranch        *b_hminus_TRUEP_X;   //!
   TBranch        *b_hminus_TRUEP_Y;   //!
   TBranch        *b_hminus_TRUEP_Z;   //!
   TBranch        *b_nTracks;   //!
   TBranch        *b_hplus_IP_OWNPV;   //!
   TBranch        *b_hminus_IP_OWNPV;   //!
   TBranch        *b_hplus_IPCHI2_OWNPV;   //!
   TBranch        *b_hminus_IPCHI2_OWNPV;   //!
   TBranch        *b_hplus_TRACK_Type;   //!
   TBranch        *b_hminus_TRACK_Type;   //!
   TBranch        *b_V0_ENDVERTEX_X;   //!
   TBranch        *b_V0_ENDVERTEX_Y;   //!
   TBranch        *b_V0_ENDVERTEX_Z;   //!
   TBranch        *b_V0_ENDVERTEX_CHI2;   //!
   TBranch        *b_V0_M;   //!
   TBranch        *b_V0_ORIVX_X;   //!
   TBranch        *b_V0_ORIVX_Y;   //!
   TBranch        *b_V0_ORIVX_Z;   //!
   TBranch        *b_V0_ORIVX_CHI2;   //!
   TBranch        *b_V0_FD_ORIVX;   //!
   TBranch        *b_V0_FDCHI2_ORIVX;   //!

   tree(TTree *tree=0);
   virtual ~tree();
   virtual Int_t    Cut(Long64_t entry);
   virtual Int_t    GetEntry(Long64_t entry);
   virtual Long64_t LoadTree(Long64_t entry);
   virtual void     Init(TTree *tree);
   virtual void     Loop();
   //virtual void     Graphs();
   virtual void	    tocsv();
   virtual Bool_t   Notify();
   virtual void     Show(Long64_t entry = -1);
};

#endif

#ifdef tree_cxx
tree::tree(TTree *tree) : fChain(0) 
{
// if parameter tree is not specified (or zero), connect the file
// used to generate this class and read the Tree.
   if (tree == 0) {
      TFile *f = (TFile*)gROOT->GetListOfFiles()->FindObject("Lb_Tuple_presel_v2.root");
      if (!f || !f->IsOpen()) {
         f = new TFile("Lb_Tuple_presel_v2.root");
      }
      f->GetObject("tree",tree);

   }
   Init(tree);
}

tree::~tree()
{
   if (!fChain) return;
   delete fChain->GetCurrentFile();
}

Int_t tree::GetEntry(Long64_t entry)
{
// Read contents of entry.
   if (!fChain) return 0;
   return fChain->GetEntry(entry);
}
Long64_t tree::LoadTree(Long64_t entry)
{
// Set the environment to read one entry
   if (!fChain) return -5;
   Long64_t centry = fChain->LoadTree(entry);
   if (centry < 0) return centry;
   if (fChain->GetTreeNumber() != fCurrent) {
      fCurrent = fChain->GetTreeNumber();
      Notify();
   }
   return centry;
}

void tree::Init(TTree *tree)
{
   // The Init() function is called when the selector needs to initialize
   // a new tree or chain. Typically here the branch addresses and branch
   // pointers of the tree will be set.
   // It is normally not necessary to make changes to the generated
   // code, but the routine can be extended by the user if needed.
   // Init() will be called many times when running on PROOF
   // (once per file to be processed).

   // Set branch addresses and branch pointers
   if (!tree) return;
   fChain = tree;
   fCurrent = -1;
   fChain->SetMakeClass(1);

   fChain->SetBranchAddress("hplus_PX", &hplus_PX, &b_hplus_PX);
   fChain->SetBranchAddress("hplus_PY", &hplus_PY, &b_hplus_PY);
   fChain->SetBranchAddress("hplus_PZ", &hplus_PZ, &b_hplus_PZ);
   fChain->SetBranchAddress("hminus_PX", &hminus_PX, &b_hminus_PX);
   fChain->SetBranchAddress("hminus_PY", &hminus_PY, &b_hminus_PY);
   fChain->SetBranchAddress("hminus_PZ", &hminus_PZ, &b_hminus_PZ);
   fChain->SetBranchAddress("hplus_TRUEP_X", &hplus_TRUEP_X, &b_hplus_TRUEP_X);
   fChain->SetBranchAddress("hplus_TRUEP_Y", &hplus_TRUEP_Y, &b_hplus_TRUEP_Y);
   fChain->SetBranchAddress("hplus_TRUEP_Z", &hplus_TRUEP_Z, &b_hplus_TRUEP_Z);
   fChain->SetBranchAddress("hminus_TRUEP_X", &hminus_TRUEP_X, &b_hminus_TRUEP_X);
   fChain->SetBranchAddress("hminus_TRUEP_Y", &hminus_TRUEP_Y, &b_hminus_TRUEP_Y);
   fChain->SetBranchAddress("hminus_TRUEP_Z", &hminus_TRUEP_Z, &b_hminus_TRUEP_Z);
   fChain->SetBranchAddress("nTracks", &nTracks, &b_nTracks);
   fChain->SetBranchAddress("hplus_IP_OWNPV", &hplus_IP_OWNPV, &b_hplus_IP_OWNPV);
   fChain->SetBranchAddress("hminus_IP_OWNPV", &hminus_IP_OWNPV, &b_hminus_IP_OWNPV);
   fChain->SetBranchAddress("hplus_IPCHI2_OWNPV", &hplus_IPCHI2_OWNPV, &b_hplus_IPCHI2_OWNPV);
   fChain->SetBranchAddress("hminus_IPCHI2_OWNPV", &hminus_IPCHI2_OWNPV, &b_hminus_IPCHI2_OWNPV);
   fChain->SetBranchAddress("hplus_TRACK_Type", &hplus_TRACK_Type, &b_hplus_TRACK_Type);
   fChain->SetBranchAddress("hminus_TRACK_Type", &hminus_TRACK_Type, &b_hminus_TRACK_Type);
   fChain->SetBranchAddress("V0_ENDVERTEX_X", &V0_ENDVERTEX_X, &b_V0_ENDVERTEX_X);
   fChain->SetBranchAddress("V0_ENDVERTEX_Y", &V0_ENDVERTEX_Y, &b_V0_ENDVERTEX_Y);
   fChain->SetBranchAddress("V0_ENDVERTEX_Z", &V0_ENDVERTEX_Z, &b_V0_ENDVERTEX_Z);
   fChain->SetBranchAddress("V0_ENDVERTEX_CHI2", &V0_ENDVERTEX_CHI2, &b_V0_ENDVERTEX_CHI2);
   fChain->SetBranchAddress("V0_M", &V0_M, &b_V0_M);
   fChain->SetBranchAddress("V0_ORIVX_X", &V0_ORIVX_X, &b_V0_ORIVX_X);
   fChain->SetBranchAddress("V0_ORIVX_Y", &V0_ORIVX_Y, &b_V0_ORIVX_Y);
   fChain->SetBranchAddress("V0_ORIVX_Z", &V0_ORIVX_Z, &b_V0_ORIVX_Z);
   fChain->SetBranchAddress("V0_ORIVX_CHI2", &V0_ORIVX_CHI2, &b_V0_ORIVX_CHI2);
   fChain->SetBranchAddress("V0_FD_ORIVX", &V0_FD_ORIVX, &b_V0_FD_ORIVX);
   fChain->SetBranchAddress("V0_FDCHI2_ORIVX", &V0_FDCHI2_ORIVX, &b_V0_FDCHI2_ORIVX);
   Notify();
}

Bool_t tree::Notify()
{
   // The Notify() function is called when a new file is opened. This
   // can be either for a new TTree in a TChain or when when a new TTree
   // is started when using PROOF. It is normally not necessary to make changes
   // to the generated code, but the routine can be extended by the
   // user if needed. The return value is currently not used.

   return kTRUE;
}

void tree::Show(Long64_t entry)
{
// Print contents of entry.
// If entry is not specified, print current entry
   if (!fChain) return;
   fChain->Show(entry);
}
Int_t tree::Cut(Long64_t entry)
{
// This function may be called from Loop.
// returns  1 if entry is accepted.
// returns -1 otherwise.
   return 1;
}
#endif // #ifdef tree_cxx
