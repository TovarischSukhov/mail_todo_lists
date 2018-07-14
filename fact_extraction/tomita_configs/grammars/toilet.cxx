#encoding "utf-8"

ToiletWord -> 'туалет' | 'санузел' | 'сортир' | 'уборная' | 'сан' 'узел';

ObligatoryWord -> 'обязательно' | 'важно' | 'нужен' | 'важен';
PreferableWord -> 'желательно' | 'хотелось' 'бы' ;

DividedWord -> 'раздельный' | 'отдельный';
CombinedWord -> 'объединенный' | 'слитный' | 'совмещенный' | 'общий';

NeedPower -> ObligatoryWord | PreferableWord ;

ToiletCombined_1 -> (NeedPower) (Prep) ToiletWord<rt> (Word) (Word) CombinedWord interp(ToiletFact.combined);
ToiletCombined_2 -> (NeedPower) (Prep) CombinedWord interp(ToiletFact.combined) (Word) (Word) ToiletWord<rt> ;

ToiletDivided_1 -> (NeedPower) (Prep) ToiletWord<rt> (Word) (Word) DividedWord interp(ToiletFact.divided);
ToiletDivided_2 -> (NeedPower) (Prep) DividedWord interp(ToiletFact.divided) (Word) (Word) ToiletWord<rt> ;

Toilet_ -> ToiletCombined_1 | ToiletCombined_2 | ToiletDivided_1 | ToiletDivided_2 ;
Toilet -> Toilet_ interp(ToiletFact.total) ;