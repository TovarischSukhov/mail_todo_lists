NP_ -> Noun;                              // правило 1: именная группа может состоять
                                         //            из одного существительного
NP_ -> Adj<gnc-agr[1]> Noun<gnc-agr[1]>;  // правило 2: именная группа может включать
                                         //            согласованные прилагательное и существительное
NP_ -> Noun Noun;              // правило 3: именная группа может состоять из двух

NP -> (Noun) NP_;