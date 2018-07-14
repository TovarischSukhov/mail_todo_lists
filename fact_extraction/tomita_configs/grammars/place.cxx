#encoding "utf-8"

Near -> 'рядом' 'с' | 'около' | 'в' 'районе' | 'рядом' 'со' | 'недалеко' 'от' | 'у';
In -> 'в' | 'на' ;

NearIn -> Near | In;

PlaceWord_ -> 'район' | 'метро' | 'улица' | 'площадь' | 'проспект' | 'переулок' | 'проезд' | 'тупик';
PlaceShort -> 'р-н' | 'рн' | 'м' | 'г' | 'пл' | 'ул' | 'пр' | 'пер' | 'просп' | 'пр-д';

PlaceWord -> PlaceWord_ | PlaceShort;

// PossiblePlace -> Near Word<kwtype='NP', kwtype=~'stopwords'> interp(PlaceFact.possible_places::norm="nom,sg");

DictGeo -> Word<kwtype='geo_1'> interp(PlaceFact.place::norm="nom,sg");

PossiblePlace -> Near Word<kwtype='NP'> interp(PlaceFact.possible_places::norm="nom,sg");

Area ->  Word<kwtype='prefix_words'> (Hyphen) DictGeo | DictGeo (Hyphen) Word<kwtype='prefix_words'>;

PlaceGeoWord_1 -> (NearIn) (PlaceWord) Area interp(PlaceFact.place::norm="nom,sg");
PlaceGeoWord_2 -> (NearIn) Area interp(PlaceFact.place::norm="nom,sg") (PlaceWord) ;

PlaceGeoWord_3 -> (NearIn) (PlaceWord) DictGeo interp(PlaceFact.place::norm="nom,sg");
PlaceGeoWord_4 -> (NearIn) DictGeo interp(PlaceFact.place::norm="nom,sg") (PlaceWord) ;

Place_ -> PlaceGeoWord_1 | PlaceGeoWord_2 | PlaceGeoWord_3 | PlaceGeoWord_4 | DictGeo | PossiblePlace;

Place -> Place_ interp(PlaceFact.total);