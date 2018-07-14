#encoding "utf-8" 

Or -> 'или';

RoomsWord -> Word<wff=/((ух)|(ех)|(х))?комн.*/>;

Number_ -> AnyWord<wff=/[1-9]/> | AnyWord<wff=/[1-9](-[1-9])+/>;
WordNumber -> Word<kwtype='number_word'>;
Number -> Number_ | WordNumber;

Ending -> UnknownPOS | Word<kwtype='окончание'>;

RoomsCountWord -> Word<kwtype=rooms_w_number>;

RoomsOr -> Number (Hyphen) (Ending) Or;

RoomsHyphen -> Number (Hyphen);

RoomsEnd ->  RoomsWord | RoomsCountWord;

Rooms_1 -> RoomsOr+ Number (Hyphen) (Ending) (Hyphen) RoomsEnd;
Rooms_2 -> RoomsHyphen+ Number (Hyphen) (Ending) (Hyphen) RoomsEnd;
Rooms_3 -> Number (Hyphen) (Ending) (Hyphen) RoomsEnd;
Rooms_4 -> Number (Hyphen) Ending;

Rooms_ -> Rooms_1 | Rooms_2 | Rooms_3 | RoomsCountWord | Rooms_4;
Rooms -> Rooms_ interp(RoomsFact.num_rooms);
