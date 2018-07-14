#encoding "utf-8"
#GRAMMAR_ROOT NP

NumberW_1 -> AnyWord<wff=/[1-9][0-9]*-?((ый)|(ий)|(ой)|й)?/> {outgram="муж,ед,им"};
NumberW_2 -> AnyWord<wff=/[1-9][0-9]*-?((ая)|(яя)|(ья)|я)?/> {outgram="жен,ед,им"};
NumberW_3 -> AnyWord<wff=/[1-9][0-9]*-?((ее)|(ье)|(ое)|е)?/> {outgram="сред,ед,им"};

NumberW -> NumberW_1 | NumberW_2 | NumberW_3;

NumberNoun -> Noun<rt> NumberW;

Abbreviation -> Word<wfm=/[А-Яё]+/>;

// PrepNoun -> Prep Noun;

// FigureNoun -> OrdinalNumeral Noun<rt>;
AdjNoun -> Adj<gnc-agr[1]>  Noun<gnc-agr[1], rt>;

NounNoun -> Noun Noun<gram="dat"> | Noun Noun<gram="gen"> ;

//AnyWordNoun -> AnyWord Noun<rt>;

PossibleWord -> Word<gram="~A">;

NP -> NumberNoun | Abbreviation | PossibleWord | AdjNoun | NounNoun;