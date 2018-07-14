#encoding "utf-8"

Ipoteka -> 'ипотека' | 'кредит' ;

Possible -> 'возможно' | 'доступно' | 'доступный';

In -> 'в';

InIpoteka_ -> (Possible) In interp(IpotekaFact.needed) Ipoteka;
InIpoteka -> InIpoteka_ interp(IpotekaFact.total);