#encoding "utf-8"

InHelp -> 'рядом' | 'недалеко' | 'не' 'далеко';
In_ -> 'в' | 'на' | 'с' | 'от' | 'со' | 'около' ;
In -> (InHelp) In_;

PlaceWord -> 'район' | 'метро' | 'улица' | 'площадь' ;
PlaceShort -> 'р-н' | 'рн' | 'м' | 'г';

// GeoPoints -> 'школа' | 'детский' 'сад' | 'памятник' | 'детсад';

SimpleGeo -> Word<kwtype='geo_1'>;
Area ->  Word<kwtype='prefix_words'> SimpleGeo | SimpleGeo Word<kwtype='prefix_words'>;

Place_CapitalLett -> In (PlaceShort) Noun<h-reg1>;

Place_wPword_1 -> (In) PlaceWord Noun<kwtype=~'stopwords'>;
Place_wPword_2 -> (In) Noun<kwtype=~'stopwords'> PlaceWord;
Place_wPword_2 -> (In) PlaceShort Noun<kwtype=~'stopwords'>;

Place_geoWord_1 -> (In) (PlaceWord) Area ;
Place_geoWord_2 -> (In) Area (PlaceWord) ;
Place_geoWord_3 -> (In) (PlaceWord) SimpleGeo ;
Place_geoWord_4 -> (In) SimpleGeo (PlaceWord) ;

// PP -> In GeoPoints ;

// PossiblePlace -> In (GeoPoints) AnyWord<kwtype=~'stopwords', rt>+ interp(PlaceFact.possible_places::norm="nom,sg");
PossiblePlace -> In (GeoPoints) AnyWord<kwtype='NP', kwtype=~'stopwords'>+ interp(PlaceFact.possible_places::norm="nom,sg");


Place_1 -> PossiblePlace;

Place_ -> Place_wPword_1 | Place_wPword_2 | Place_CapitalLett | Place_geoWord_1 | Place_geoWord_2 | Place_geoWord_3 | Place_geoWord_4;

Place -> Place_ interp(PlaceFact.place::norm="nom,sg");

PF -> Place+ | Place_1+ ;

PlaceFinal_ -> PF+;

PlaceFinal -> PlaceFinal_ interp(PlaceFact.place_debug);