#encoding "utf-8"

//In -> 'в';

TimeHour -> AnyWord<wff=/([0-1]?[0-9])|(2[0-4])/>;
TimeMinute -> AnyWord<wff=/([0-6]?[0-9])/>;
TimeSep -> ':';

Time -> TimeHour interp (TimeFact.Hour) (TimeSep) TimeMinute interp (TimeFact.Minutes);
//Time -> TimeHour interp (TimeFact.Hour);