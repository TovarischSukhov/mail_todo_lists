#encoding "utf-8"

TimeHour -> AnyWord<wff=/([0-1]?[0-9])|(2[0-4])/>;
TimeMinute -> AnyWord<wff=/([0-6]?[0-9])/>;

Time -> TimeHour interp (TimeFact.Hour) TimeMinute interp (TimeFact.Minutes);
Time -> TimeHour interp (TimeFact.Minutes);