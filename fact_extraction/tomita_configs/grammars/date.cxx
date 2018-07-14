#encoding "utf-8"

DayOfWeek -> Noun<kwtype="день_недели">;
Day -> AnyWord<wff=/([1-2]?[0-9])|(3[0-1])/>;
Month -> Noun<kwtype="month"> | AnyWord<wff=/(0?[1-9])|(1[0-2])/>;
YearDescr -> "год" | "г. ";
Year -> AnyWord<wff=/[1-2]?[0-9]{3}г?\.?/>;
Year -> Year YearDescr;
DateSep -> Punct | Comma | Hyphen | '/';

        // день недели, запятая, число, месяц и год:
        // "понедельник, 3 сентября 2012г."
Date -> DayOfWeek interp (DateFact.DayOfWeek) (DateSep)
        Day interp (DateFact.Day) (DateSep)
        Month interp (DateFact.Month) (DateSep)
        (Year interp (DateFact.Year));

        // число, месяц и год: "10 января 2011"
Date -> Day interp (DateFact.Day)
        Month interp (DateFact.Month)
        (Year interp (DateFact.Year));

Date -> Day interp (DateFact.Day) (DateSep)
        Month interp (DateFact.Month);

        // месяц и год: "июнь 2009"
Date -> Month interp (DateFact.Month) (DateSep)
        Year interp (DateFact.Year);

Date -> AnyWord<wff=/(([1-2]?[0-9])|(3[0-1]))-((0?[1-9])|(1[0-2]))-([1-2]?[0-9]{1,3})/> interp (DateFact.Full);