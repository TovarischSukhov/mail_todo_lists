#encoding "utf-8"

DayOfWeek -> Noun<kwtype="день_недели">;      // используем слова из статьи "день_недели"
Day -> AnyWord<wff=/([1-2]?[0-9])|(3[0-1])/>; // число от 1 до 31
Month -> Noun<kwtype="month">;                // используем слова из статьи "месяц"
YearDescr -> "год" | "г. ";
Year -> AnyWord<wff=/[1-2]?[0-9]{1,3}г?\.?/>; // число от 0 до 2999 с возможным "г" или "г." в конце
Year -> Year YearDescr;

        // день недели, запятая, число, месяц и год:
        // "понедельник, 3 сентября 2012г."
Date -> DayOfWeek interp (DateFact.DayOfWeek) (Comma)
        Day interp (DateFact.Day)
        Month interp (DateFact.Month)
        (Year interp (DateFact.Year));

        // число, месяц и год: "10 января 2011"
Date -> Day interp (DateFact.Day)
        Month interp (DateFact.Month)
        (Year interp (DateFact.Year));

Date -> Day interp (DateFact.Day)
        Month interp (DateFact.Month);

        // месяц и год: "июнь 2009"
Date -> Month interp (DateFact.Month)
        Year interp (DateFact.Year);