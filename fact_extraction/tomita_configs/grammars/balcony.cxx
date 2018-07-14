#encoding "utf-8"

BalconyWord -> 'балкон' | 'лоджия' ;

Or -> 'или';

BalconyOr -> BalconyWord (Or) (BalconyWord);

HaveWord -> 'наличие';

ObligatoryWord -> 'обязательно' | 'важно' | 'нужен' | 'важен';

PreferableWord -> 'желательно' | 'хотелось' 'бы' ;

ObligatoryBalcony_1 -> ObligatoryWord interp(BalconyFact.obligatory) (Word) (HaveWord) BalconyOr;
ObligatoryBalcony_2 -> (HaveWord) BalconyOr (Word) ObligatoryWord interp(BalconyFact.obligatory);
ObligatoryBalcony_3 -> Prep interp(BalconyFact.obligatory) BalconyOr;

PreferablyBalcony_1 -> PreferableWord interp(BalconyFact.preferably) (Word) (HaveWord) BalconyOr;
PreferablyBalcony_2 -> (HaveWord) BalconyOr (Word) PreferableWord interp(BalconyFact.preferably);
PreferablyBalcony_2 ->  PreferableWord interp(BalconyFact.preferably) (Prep) (Word) (HaveWord) BalconyOr;

Balcony_ -> ObligatoryBalcony_1 | ObligatoryBalcony_2 | ObligatoryBalcony_3 | PreferablyBalcony_1 | PreferablyBalcony_2;
Balcony -> Balcony_ interp(BalconyFact.total);