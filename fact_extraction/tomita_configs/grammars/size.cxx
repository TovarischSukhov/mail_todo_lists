#encoding "utf-8" 

SizeWord -> 'площадь' | 'размер';

Not -> 'не';
More -> 'более' | 'больше';
Less -> 'менее' | 'меньше';

NotLess -> 'от' | 'минимум' | Not Less;
NotMuch -> 'до' | 'максимум' | Not More;
SomeWhat -> 'около' | 'в' 'районе';

MetricW -> Word<kwtype='метр'>;

NumberW_noLetters -> AnyWord<wff=/[1-9][0-9]*-?[1-9]?[0-9]*/> ;
NumberW_wMetric -> AnyWord<wff=/[1-9][0-9]*-?[1-9]?[0-9]*((м)|(м2)|(м.кв))/> ;

SizeSep -> NumberW_noLetters MetricW;
Size_ -> NumberW_wMetric | SizeSep ;

Size_Min -> NotLess Size_;
Size_Max -> NotMuch Size_;
Size_SomeWhat -> SomeWhat Size_;

Size_FromTo -> Size_Min Size_Max;
Size_Any -> (SizeWord) Size_SomeWhat|Size_FromTo|Size_;

Size -> Size_Any interp(SizeFact.total_size);
