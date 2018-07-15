OR -> 'или';

NP_ -> Noun;

NP_ -> Adj<gnc-agr[1]> Noun<gnc-agr[1]>;
NP_ -> Noun UnknownPOS;
NP_ -> Prep Noun;

NP_ -> NP_ OR NP_;

NP -> (Noun) NP_;