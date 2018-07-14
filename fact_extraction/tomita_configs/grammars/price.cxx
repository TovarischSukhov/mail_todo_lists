#encoding "utf-8" 

OrderW -> AnyWord<kwtype=sum_order> | 'руб' | 'р' | 'рубль';

Not -> 'не';
More -> 'более' | 'больше' | 'дороже';
Less -> 'менее' | 'меньше';

NotLess -> 'от' | 'минимум' | Not Less;
NotMuch -> 'до' | 'максимум' | 'лимит' | Not More;
SomeWhat -> 'около' | 'в' 'районе' | 'за';

PlainNumber -> AnyWord<wff=/[1-9][0-9]*/>;
DecNumber -> AnyWord<wff=/[1-9][0-9]*(,|.)[0-9]*/>;
WordNumber -> Word<kwtype='number_word'>;

JustANumber -> PlainNumber | DecNumber | WordNumber;

PriceHyphen -> JustANumber (Hyphen) (JustANumber);

PriceSep -> PriceHyphen OrderW<rt>;

BigNumber_1 -> AnyWord<wff=/[1-9]([0-9]){6,12}/>+;
BigNumber_2 -> AnyWord<wff=/[1-9]([0-9]){0,12}/> AnyWord<wff=/([0-9]){3,12}/>+;

BigNumber -> BigNumber_1 | BigNumber_2;

// Price_nPrep_ -> PriceSep;
Price_nPrep -> PriceSep | BigNumber;

MinNumber -> NotLess JustANumber interp(PriceFact.price_min::norm="nom,sg");

PriceMin -> NotLess Price_nPrep<rt> interp(PriceFact.price_min::norm="nom,sg");
PriceMax -> NotMuch Price_nPrep<rt> interp(PriceFact.price_max::norm="nom,sg");
PriceAbout -> SomeWhat Price_nPrep<rt> interp(PriceFact.price_about::norm="nom,sg");

MinPart -> PriceMin | MinNumber;
PriceFromTo -> MinPart  PriceMax<rt> ;

Price_ -> PriceFromTo | PriceAbout | PriceMax | PriceMin | Price_nPrep interp(PriceFact.price_about::norm="nom,sg");
Price -> Price_ interp(PriceFact.price::norm="nom,sg");
