"""
Dynamic content library for Seasonal Horizon.
Multilingual support: English (en) and German (de).
"""

# ===== FORECAST NARRATIVES =====
WEEKDAYS = {
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
           "Saturday", "Sunday"],
    "de": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag",
           "Samstag", "Sonntag"],
}


FORECAST_NARRATIVES = {
    "rain_clearing_soon": {
        "en": [
            "Grey skies today, but the forecast shows {clear_day} breaking through—just {days_until} more days to wait.",
            "The rain is temporary. By {clear_day}, the clouds lift and you'll have your moment in the sun.",
            "Hold steady through the grey. {clear_day} brings the clearing you're waiting for.",
            "This wet stretch has an end date: {clear_day}. Mark your calendar.",
            "Today's drizzle is just weather passing through. {clear_day}'s sunshine is coming.",
            "The clouds are visitors, not residents. They leave by {clear_day}.",
            "Patience pays: {days_until} {days} of grey, then {clear_day} delivers clear skies.",
            "Rain now, but I can see {clear_day} on the forecast—good conditions are coming.",
            "Every rainy streak has its last day. This one ends before {clear_day}.",
            "Wet windows today, but {clear_day} is circled on the weather chart.",
        ],
        "de": [
            "Heute noch grau, aber die Aussichten bessern sich: Am {clear_day} kommt die Sonne durch – nur noch {days_until} {days}.",
            "Regen ist kein Dauerzustand. Bis {clear_day} verziehen sich die Wolken und machen Platz für Sonne.",
            "Halt durch bei dem Grau. Der {clear_day} bringt die Aufhellung, auf die du wartest.",
            "Diese Regenphase hat ein Ablaufdatum: {clear_day}. Den Tag kannst du dir schon mal markieren.",
            "Wolken sind nur Besucher, keine Dauergäste. Spätestens am {clear_day} sind sie weg.",
            "Geduld lohnt sich: noch {days_until} {days} Grau, dann liefert der {clear_day} blauen Himmel.",
            "Aktuell noch nass, aber der {clear_day} sieht auf der Karte schon richtig gut aus.",
            "Lass den Kopf nicht hängen – das Wetter dreht sich. Am {clear_day} ist Besserung in Sicht.",
            "Nur noch ein kurzes Durchhalten: In {days_until} {days_dat}, am {clear_day}, übernimmt wieder die Sonne.",
            "Der Blick auf die Vorhersage tröstet: Am {clear_day} ist Schluss mit dem Grau.",
            "Zieh die Schultern hoch und geh da durch – am {clear_day} wartet die Belohnung.",
            "Streich die Tage ab: Noch {days_until} mal schlafen, dann wird es am {clear_day} schön.",
            "Kein Regen hält ewig. Der {clear_day} bringt das Licht zurück.",
        ],
    },
    
    "carpe_diem": {
        "en": [
            "This is your window. {rain_day} brings rain, so today's sunshine is prime time for getting outside.",
            "The sun is here now, but it's packing for {rain_day}. Don't waste this opportunity.",
            "Clear skies have an expiration date: {rain_day}. Make today count.",
            "Sunshine on borrowed time—{rain_day} takes it back. Get your outdoor tasks done.",
            "The forecast gives you until {rain_day}. That's your deadline for outdoor plans.",
            "Today is the good day. {rain_day} is the wet one. Act accordingly.",
            "This sun won't wait. By {rain_day}, you'll wish you'd used today.",
            "The weather window closes {rain_day}. Today is wide open.",
            "Don't save the sunshine for later—{rain_day} has other plans.",
            "Blue sky today, grey by {rain_day}. If you have outdoor errands, now is the time.",
        ],
        "de": [
            "Das ist dein Zeitfenster. Am {rain_day} kommt der Regen – nutz die Sonne heute unbedingt.",
            "Die Sonne ist da, aber nur auf der Durchreise. Am {rain_day} ist sie weg – verpass die Chance nicht.",
            "Dieser blaue Himmel läuft ab: Stichtag ist der {rain_day}. Mach was draus.",
            "Sonne auf Abruf – am {rain_day} übernimmt wieder das Grau. Erledige heute alles Wichtige draußen.",
            "Die Vorhersage gibt dir eine Frist bis {rain_day}. Bis dahin: Ab nach draußen.",
            "Heute ist der Genießertag, der {rain_day} wird der Regentag. Plan entsprechend.",
            "Das Wetterfenster schließt sich am {rain_day} wieder. Heute steht es noch sperrangelweit offen.",
            "Heb dir die Sonne nicht für später auf – der {rain_day} hat andere Pläne.",
            "Carpe Diem: Schnapp dir das Licht, bevor am {rain_day} die Wolken zurückkehren.",
            "Alles, was du heute an Sonne tankst, hilft dir über den {rain_day} hinweg.",
            "Dringende Empfehlung: Geh raus. Am {rain_day} ist es damit erst mal vorbei.",
            "Ein klassischer Fall von 'Jetzt oder nie'. Warte nicht auf den {rain_day}.",
            "Sammle heute Sonnenstrahlen, du wirst sie am {rain_day} brauchen.",
            "Der Countdown für gutes Wetter läuft und endet am {rain_day}.",
        ],
    },
    
    "warming_trend": {
        "en": [
            "The thermometer is climbing all week—{temp_change}°C warmer by the end. The season is definitely shifting.",
            "Each day this week runs warmer than the last. You can feel the change happening.",
            "The temperature trend is clear: warmer conditions arriving, degree by degree.",
            "Watch the degrees tick up day by day. The cold is losing ground this week.",
            "This week's forecast reads like a warming staircase. {temp_change}°C of progress ahead.",
            "The air is softening. By week's end, you'll notice the difference.",
            "Temperatures are stacking up consistently warmer through the week.",
            "The warming trend is obvious in the forecast. The season is turning.",
        ],
        "de": [
            "Das Thermometer klettert die ganze Woche – am Ende sind es {temp_change}°C mehr. Der Umschwung ist da.",
            "Jeder Tag legt eine Schippe drauf. Man spürt förmlich, wie es wärmer wird.",
            "Der Trend ist eindeutig: Es geht bergauf mit den Temperaturen, Grad für Grad.",
            "Behalt die Temperaturen im Auge – die Kälte verliert diese Woche an Boden.",
            "Die Vorhersage gleicht einer Treppe nach oben: {temp_change}°C Gewinn liegen vor dir.",
            "Die Luft wird milder. Bis zum Wochenende fühlt sich das Wetter ganz anders an.",
            "Konsequent wärmer: Die Temperaturen stapeln sich diese Woche nach oben.",
            "Endlich gute Nachrichten vom Thermometer: Es wird stetig milder.",
            "Die Kälte zieht sich zurück – freu dich auf {temp_change}°C mehr bis Ende der Woche.",
            "Schritt für Schritt wird die Luft angenehmer.",
            "Ein Hauch von Wärme kündigt sich an. Jeden Tag ein bisschen mehr.",
            "Das Wetter schaltet auf 'milder'. Genieße den Anstieg.",
            "Ein schöner Trend: Die Temperaturen klettern aus dem Keller.",
        ],
    },
    
    "cooling_trend": {
        "en": [
            "The week ahead cools down by {temp_change}°C. Time to adjust expectations.",
            "Each day dips a little lower. The season is shifting gears.",
            "The thermometer tells the story: cooler conditions moving in.",
            "Cooler days stack up ahead—{temp_change}°C lower by week's end.",
            "The air is getting crisper. By week's end, layers will be useful.",
            "This week's trend points toward cooler temperatures. Dress accordingly.",
            "The cooling is gradual but consistent through the forecast.",
            "Temperatures drop steadily over the coming days.",
        ],
        "de": [
            "Die Woche bringt Abkühlung: {temp_change}°C gehen runter. Stell dich drauf ein.",
            "Jeden Tag sinkt die Temperatur etwas tiefer. Das Wetter schaltet einen Gang zurück.",
            "Das Thermometer lügt nicht: Frische Luft ist im Anmarsch.",
            "Es wird frischer – bis zum Wochenende fehlen {temp_change}°C im Vergleich zu heute.",
            "Die Luft wird klarer und kälter. Leg dir schon mal den wärmeren Pulli bereit.",
            "Langsam aber sicher kühlt es ab – die Vorhersage lässt da keinen Zweifel.",
            "Mach dich auf frischeres Wetter gefasst.",
            "Es wird Zeit für den Zwiebel-Look – es kühlt merklich ab.",
            "Die Wärme verabschiedet sich vorerst, es wird knackiger.",
            "Bereite dich auf kühlere Tage vor, der Trend ist eindeutig.",
            "Ein Temperatursturz in Raten kommt auf uns zu.",
            "Die milden Tage machen erst mal Pause.",
            "Kühle Luft übernimmt die Regie für den Rest der Woche.",
        ],
    },
    
    "light_fighter": {
        "en": [
            "The clouds are grey, but behind them the sun just got {delta_min} {minutes} stronger. The light is gaining even when you can't see it.",
            "Grey skies, but here's the reality: you have {delta_min} more minutes of daylight than yesterday. Progress continues regardless of clouds.",
            "Don't let the overcast fool you. The light gained {delta_min} {minutes} since yesterday—the trend doesn't stop for weather.",
            "The clouds block the view but not the progress: +{delta_min} {minutes} of daylight today compared to yesterday.",
            "It looks grey out there, but the data shows {delta_min} more minutes of light. The days are lengthening regardless.",
            "Grey today, but the light doesn't stop for clouds. It added {delta_min} {minutes} anyway.",
            "Behind all that grey, the daylight increased by {delta_min} {minutes}. The clock keeps moving in your favor.",
            "Overcast skies can't change the astronomy: the day stretched {delta_min} {minutes} longer than yesterday.",
            "Clouds are temporary. The {delta_min} {minutes} you gained today are permanent progress.",
            "The sky forgot to be sunny, but it didn't forget to be longer. +{delta_min} {minutes}.",
        ],
        "de": [
            "Graue Wolken, aber dahinter hat die Sonne {delta_min} {minutes} Kraft gewonnen. Das Licht arbeitet für dich, auch unsichtbar.",
            "Der Himmel ist grau, aber Fakt ist: Du hast {delta_min} {minutes} mehr Licht als gestern. Der Fortschritt lässt sich nicht aufhalten.",
            "Lass dich vom Grau nicht täuschen. Das Tageslicht hat {delta_min} {minutes} zugelegt – der Trend wartet nicht auf schönes Wetter.",
            "Die Wolken versperren die Sicht, aber nicht den Weg: +{delta_min} {minutes} Helligkeit im Vergleich zu gestern.",
            "Draußen sieht's trüb aus, aber die Daten lügen nicht: {delta_min} {minutes} mehr Licht. Die Tage werden länger, egal was das Wetter macht.",
            "Heute grau, aber das Licht macht keine Pause. Es sind trotzdem {delta_min} {minutes} dazugekommen.",
            "Hinter der grauen Fassade ist der Tag um {delta_min} {minutes} gewachsen. Die Zeit spielt dir in die Karten.",
            "Wolken können die Astronomie nicht bremsen: Der Tag ist heute {delta_min} {minutes} länger.",
            "Wolken sind vergänglich, aber die {delta_min} {minutes} Gewinn von heute bleiben dir erhalten.",
            "Der Himmel hat vergessen sonnig zu sein, aber nicht, länger hell zu bleiben. +{delta_min} {minutes} für dich.",
            "Das Wetter ist mies, aber die Astronomie ist gut: {delta_min} {minutes} mehr Licht als gestern.",
            "Auch wenn man die Sonne nicht sieht – sie arbeitet im Hintergrund und schenkt dir {delta_min} extra Minuten.",
            "Konzentrier dich auf das Positive: Es bleibt abends {delta_min} {minutes} länger hell als gestern.",
            "Die Dunkelheit verliert heute wieder {delta_min} {minutes} an Boden, Wolken hin oder her.",
            "Vergiss das Grau, feiere das Plus: {delta_min} {minutes} mehr Tageslicht.",
            "Lass es regnen, das Licht gewinnt trotzdem: +{delta_min} {minutes} heute.",
        ],
    },
    
    "peak_light": {
        "en": [
            "You're at the top of the light curve. These are the longest days the year offers—{day_length} from sunrise to sunset.",
            "Peak daylight is here. Evenings stretch as late as they possibly can.",
            "Maximum daylight: {day_length}. This is the year's peak generosity with light.",
            "These are the apex days—{day_length} of light. It doesn't get more than this.",
            "You're at the year's maximum brightness. {day_length} of daylight today.",
            "Maximum daylight achieved: {day_length}. This is what we waited for through winter.",
            "The sun has topped out at {day_length}. This is as much light as the year gives.",
            "Peak hours: {day_length}. The calendar's maximum light offering.",
        ],
        "de": [
            "Du bist am Gipfel der Lichtkurve angekommen. Das sind die längsten Tage des Jahres – {day_length} Helligkeit pur.",
            "Maximale Helligkeit erreicht. Die Abende dehnen sich jetzt so weit aus, wie es physikalisch möglich ist.",
            "Licht-Rekord: {day_length}. Großzügiger wird das Jahr nicht mehr.",
            "Das sind die Spitzentage – {day_length} Licht am Stück. Mehr geht einfach nicht.",
            "Das Jahresmaximum ist da: {day_length} Tageslicht heute.",
            "Die Sonne gibt alles: {day_length}. Mehr Licht hat das Jahr nicht im Angebot.",
            "Hochsaison fürs Licht: {day_length}. Das absolute Maximum im Kalender.",
            "Genieß es: Länger als heute ({day_length}) scheint die Sonne nicht.",
            "Wir schwimmen im Licht. Mit {day_length} sind wir am absoluten Höhepunkt.",
            "Besser wird's nicht: {day_length} Tageslicht stehen dir heute zur Verfügung.",
            "Das ist der Zenit. {day_length} zwischen Aufgang und Untergang.",
            "Saug das Licht auf – wir haben heute {day_length} davon.",
            "Ein Tag der Superlative: {day_length} Helligkeit.",
            "Es sind die goldenen Tage des Jahres mit {day_length} Lichtdauer.",
        ],
    },
    
    "post_solstice_grind": {
        "en": [
            "The cold is real, but so is this: you've already gained {hours_gained} since the solstice. The turnaround is underway.",
            "Winter's grip feels solid, but the numbers show {hours_gained} more daylight than December's minimum.",
            "It's cold and dark, but you're {hours_gained} ahead of the solstice already. The climb has definitely begun.",
            "January asks for patience and delivers progress: {hours_gained} more light than the darkest day.",
            "The weather says winter. The daylight says recovery: +{hours_gained} since the turning point.",
            "The solstice was the bottom. You've climbed {hours_gained} since then, even if it doesn't feel dramatic yet.",
            "Winter is obvious. The returning light is subtle. But you're already {hours_gained} ahead.",
            "The grind continues, but so does the gain: {hours_gained} of progress since December.",
        ],
        "de": [
            "Die Kälte ist echt, aber der Fortschritt auch: Seit der Sonnenwende hast du schon {hours_gained} Licht gewonnen.",
            "Der Winter hat uns noch fest im Griff, aber wir haben schon {hours_gained} mehr Tageslicht als im tiefsten Dezember.",
            "Es ist kalt, ja. Aber du bist schon {hours_gained} über dem Tiefpunkt. Es geht bergauf.",
            "Der Januar fordert Geduld, gibt aber auch zurück: {hours_gained} mehr Licht als am dunkelsten Tag.",
            "Das Wetter schreit 'Winter', aber das Licht flüstert 'Frühling': +{hours_gained} seit der Wende.",
            "Die Sonnenwende war die Talsohle. Seitdem ging es {hours_gained} nach oben, auch wenn man es kaum merkt.",
            "Der Winter ist offensichtlich, das Licht subtil. Aber der Vorsprung beträgt schon {hours_gained}.",
            "Lass dich nicht unterkriegen: Wir haben schon {hours_gained} Licht zurückerobert.",
            "Ein stiller Erfolg: Das Tageslicht ist um {hours_gained} gewachsen.",
            "Der Weg aus dem Dunkeln ist {hours_gained} lang.",
            "Schritt für Schritt raus aus dem Winter: +{hours_gained} sind geschafft.",
            "Das Schlimmste liegt hinter uns – genau genommen {hours_gained} Lichtstunden.",
            "Sieh es positiv: Wir sind {hours_gained} vom dunkelsten Punkt entfernt.",
            "Die Richtung stimmt wieder: +{hours_gained} auf dem Lichtkonto.",
        ],
    },
    
    "good_streak": {
        "en": [
            "Clear skies today, tomorrow, and beyond—{streak_days} {days} of good weather ahead. The forecast is cooperating.",
            "This is a genuine stretch of good weather. {streak_days} {days} of decent conditions ahead.",
            "The forecast shows {streak_days} consecutive good days. That's worth planning around.",
            "A proper run of good weather: {streak_days} {days}. Streaks like this deserve action.",
            "Day after day of good conditions ahead. {streak_days} {days} of cooperative weather.",
            "The forecast is consistent: good, good, good. {streak_days} {days} to work with.",
        ],
        "de": [
            "Klarer Himmel heute, morgen und darüber hinaus – {streak_days} {days} Schönwetter am Stück.",
            "Das ist eine echte Glückssträhne. {streak_days} {days} gute Bedingungen warten auf dich.",
            "Die Vorhersage zeigt {streak_days} gute Tage in Folge. Da kann man was planen.",
            "Eine stabile Schönwetterphase: {streak_days} {days}. So eine Serie muss man nutzen.",
            "Ein Tag schöner als der andere. Das Wetter kooperiert für ganze {streak_days} {days}.",
            "Endlich mal Beständigkeit: Freu dich auf {streak_days} {days} Sonne.",
            "Das Wetter meint es ernst – im positiven Sinne. {streak_days} {days} lang.",
            "Rausgehen ist jetzt Pflicht: Eine Serie von {streak_days} schönen Tagen startet.",
            "Keine Ausreden mehr: {streak_days} {days} Top-Wetter liegen vor dir.",
            "Genieß die Serie: {streak_days} {days} ohne Sorgen beim Blick in den Himmel.",
        ],
    },
    
    "grey_stretch": {
        "en": [
            "The week looks grey throughout—{streak_days} {days} of clouds ahead. Time to embrace indoor activities.",
            "A stretch of overcast: {streak_days} {days}. The weather wants you to slow down.",
            "{streak_days} {days} of grey ahead. Good time for indoor projects.",
            "The forecast is consistent: clouds, clouds, clouds for {streak_days} {days}.",
            "An extended grey period. Books, projects, and indoor activities.",
            "The sky is taking a break from blue. {streak_days} {days} of grey ahead.",
        ],
        "de": [
            "Die Woche zeigt sich grau in grau – {streak_days} {days} Wolken. Mach's dir drinnen gemütlich.",
            "Eine echte Grauphase: {streak_days} {days} am Stück. Das Wetter lädt zum Entschleunigen ein.",
            "{streak_days} {days} Grau voraus. Die perfekte Zeit für Projekte in den eigenen vier Wänden.",
            "Die Vorhersage ist leider konstant: Wolken für {streak_days} {days}.",
            "Das Grau bleibt uns erhalten. Zeit für Bücher, Tee und Sofa.",
            "Nimm's gelassen: Es folgen {streak_days} {days} Couch-Wetter.",
            "Die Sonne macht Urlaub, und zwar für {streak_days} {days}.",
            "Stell dich auf {streak_days} {days} Einheitsgrau ein.",
            "Perfektes Wetter, um Dinge zu erledigen: {streak_days} {days} Wolken.",
            "Kuscheldecke raus: Es bleiben {streak_days} {days} grau.",
        ],
    },
    
    "breakthrough_day": {
        "en": [
            "The grey has broken. Today is the clear one - the forecast has nothing better lined up.",
            "Today is the good day this week gets. Worth arranging something around.",
            "The clouds stepped aside. Nothing else in the forecast looks like this.",
            "This is the opening. The rest of the week goes back to grey.",
            "Clear today, and the forecast does not repeat itself. Take it while it is here.",
            "The sky finally cooperated. It is a one-day offer, going by the forecast.",
            "Today stands alone in this forecast. Bright, and not repeated.",
            "After the grey, a clear one. The forecast suggests making the most of it.",
            "The weather remembered how to be clear. Just for today, by the look of it.",
            "One clear day in an otherwise unremarkable week. This is it.",
        ],
        "de": [
            "Das Grau ist aufgebrochen. Heute ist der klare Tag - die Vorhersage hat nichts Besseres im Angebot.",
            "Heute ist der gute Tag dieser Woche. Lohnt sich, etwas darum herum zu legen.",
            "Die Wolken sind zur Seite getreten. Nichts sonst in der Vorhersage sieht so aus.",
            "Das ist das Fenster. Danach geht es zurück ins Grau.",
            "Heute klar, und die Vorhersage wiederholt sich nicht. Nimm es mit, solange es da ist.",
            "Der Himmel hat endlich mitgespielt. Ein Ein-Tages-Angebot, den Daten nach.",
            "Heute steht allein in dieser Vorhersage. Hell, und ohne Wiederholung.",
            "Nach dem Grau ein klarer Tag. Die Vorhersage legt nahe, ihn auszunutzen.",
            "Das Wetter hat sich erinnert, wie klar geht. Offenbar nur für heute.",
            "Ein klarer Tag in einer sonst unauffälligen Woche. Das ist er.",
        ],
    },
    
    "weekend_good": {
        "en": [
            "The weekend forecast looks solid. Saturday and Sunday both show good conditions for outdoor plans.",
            "Good news for the weekend: clear skies on both days. Plan something outside.",
            "The forecast saved the good weather for the weekend. Saturday and Sunday both look decent.",
            "Your weekend looks workable. Outdoor plans are reasonable to make.",
            "Saturday and Sunday both look favorable. Good timing for outdoor activities.",
        ],
        "de": [
            "Die Wochenend-Prognose sieht stabil aus. Samstag und Sonntag bieten gute Bedingungen.",
            "Gute Nachrichten fürs Wochenende: Klarer Himmel an beiden Tagen. Nichts wie raus!",
            "Die Vorhersage hat sich das gute Wetter fürs Wochenende aufgehoben. Sieht gut aus.",
            "Dein Wochenende wird brauchbar. Pläne für draußen kannst du definitiv machen.",
            "Samstag und Sonntag zeigen sich von ihrer besten Seite. Perfektes Timing.",
            "Freu dich aufs Wochenende: Das Wetter spielt an beiden Tagen mit.",
            "Endlich mal ein Wochenende, an dem man was unternehmen kann.",
            "Das Wochenende wird schön – nutz die freien Tage.",
        ],
    },
    
    "weekend_bad": {
        "en": [
            "The weekend looks wet. Indoor plans might be the smarter choice.",
            "Rain on Saturday, more on Sunday. The weekend is an indoor one.",
            "The forecast suggests a cozy weekend—clouds and rain throughout.",
            "The weekend weather isn't cooperating. Time for indoor alternatives.",
            "Grey skies for Saturday and Sunday. The week ends quietly indoors.",
        ],
        "de": [
            "Das Wochenende wird nass. Such dir lieber was für drinnen.",
            "Regen am Samstag, noch mehr am Sonntag. Ein klassisches Couch-Wochenende.",
            "Die Vorhersage deutet auf Gemütlichkeit hin – Wolken und Regen durchgehend.",
            "Das Wetter am Wochenende streikt. Zeit für Plan B in der Wohnung.",
            "Grauer Himmel am Samstag und Sonntag. Die Woche endet ruhig.",
            "Mach's dir zuhause schön, draußen wird es ungemütlich.",
            "Ein Wochenende zum Ausschlafen und Lesen – draußen verpasst du nichts.",
            "Das Wochenende wird leider verregnet.",
        ],
    },
    
    "stable_focus_light": {
        "en": [
            "The weather is steady and unremarkable—which puts the focus on the light: {day_length} of daylight today.",
            "Nothing dramatic in the forecast. Just the quiet progress of {delta_min} more minutes per day.",
            "Stable conditions mean the real story is the daylight: {day_length} and changing.",
            "The weather is background. The light—{day_length}—is the actual news.",
            "Uneventful skies. That leaves room to notice you have {day_length} of daylight today.",
        ],
        "de": [
            "Das Wetter ist unspektakulär – umso mehr rückt das Licht in den Fokus: {day_length} heute.",
            "Nichts Dramatisches in der Vorhersage. Nur der stille Fortschritt von {delta_min} {minutes} täglich.",
            "Stabiles Wetter heißt: Die eigentliche Story ist das Tageslicht ({day_length}).",
            "Das Wetter ist Nebensache. Das Licht – satte {day_length} – ist die eigentliche News.",
            "Ruhiger Himmel. Das gibt Raum zu bemerken: Du hast heute {day_length} Licht.",
            "Keine Wetterkapriolen, dafür verlässliches Licht: {day_length} lang.",
            "Wenn das Wetter langweilig ist, zählt die Tageslänge: {day_length}.",
            "Ein ruhiger Tag, an dem das Licht die Hauptrolle spielt.",
        ],
    },
    
    "spring_acceleration": {
        "en": [
            "This is the fast phase. The light is gaining {delta_min} {minutes} daily—the steepest climb of the year.",
            "The daylight is increasing quickly now: +{delta_min} {minutes} per day. You can see the evenings stretching.",
            "The acceleration is measurable. {delta_min} {minutes} daily means visible change week to week.",
            "This is when waiting turns to momentum. +{delta_min} {minutes} each day adds up fast.",
            "The daylight gains are at their maximum now: {delta_min} {minutes} daily.",
        ],
        "de": [
            "Das ist die Überholspur. Das Licht gewinnt täglich {delta_min} {minutes} – steiler geht's nicht.",
            "Es geht rasant aufwärts: +{delta_min} {minutes} pro Tag. Die Abende werden förmlich länger gezogen.",
            "Die Beschleunigung ist enorm. {delta_min} {minutes} täglich bedeuten sichtbare Veränderung jede Woche.",
            "Jetzt kommt Schwung in die Sache. +{delta_min} {minutes} jeden Tag summieren sich schnell.",
            "Vollgas Richtung Sommer: Wir gewinnen {delta_min} {minutes} jeden einzelnen Tag.",
            "Spürst du das Tempo? Jeden Tag {delta_min} {minutes} mehr Licht.",
            "Das ist der Turbo-Gang des Jahres: +{delta_min} {minutes}.",
            "Schneller werden die Tage nicht mehr länger: {delta_min} {minutes} Zuwachs.",
        ],
    },
    
    "solstice_approaching": {
        "en": [
            "The solstice is {days_to_solstice} days away. You're in the final approach to the year's turning point.",
            "Only {days_to_solstice} days until the solstice. The light is almost at its {peak_or_min}.",
            "The solstice approaches: {days_to_solstice} days. The year is about to pivot.",
            "We're in solstice territory—just {days_to_solstice} days from the astronomical milestone.",
            "The countdown is on: {days_to_solstice} days until the year turns.",
        ],
        "de": [
            "Die Sonnenwende ist nur noch {days_to_solstice} Tage entfernt. Endanflug auf den Wendepunkt.",
            "Nur noch {days_to_solstice} Tage bis zur Wende. Das Licht ist fast am {peak_or_min}.",
            "Der Countdown läuft: {days_to_solstice} Tage bis sich das Jahr dreht.",
            "Bald ist es soweit: In {days_to_solstice} Tagen ist Sonnenwende.",
            "Das große Ereignis steht bevor: noch {days_to_solstice} Tage.",
            "Wir zählen die Tage: Nur noch {days_to_solstice} bis zur Wende.",
            "Fast geschafft: {days_to_solstice} Tage trennen uns vom Wendepunkt.",
            "Merk dir das Datum, in {days_to_solstice} Tagen ändert sich die Richtung.",
        ],
    },

    "fog_day": {
        "en": [
            "Fog today. The light is still there, just filtered through a few hundred metres of cloud sitting on the ground.",
            "Everything is soft-edged today. Fog does that, and it usually burns off by midday.",
            "Grey right down to street level. Worth checking whether the hills above you are in sunshine - often they are.",
            "Fog flattens the world for a day. It also tends to mean calm air and no wind.",
            "Visibility is short today. If you are near higher ground, the top of this often sits in clear sun.",
            "A fog day. Quiet, close, and usually thinner by the afternoon.",
        ],
        "de": [
            "Heute Nebel. Das Licht ist trotzdem da, nur gefiltert durch ein paar hundert Meter Wolke am Boden.",
            "Alles hat heute weiche Kanten. Das macht der Nebel, und meist löst er sich bis Mittag auf.",
            "Grau bis auf Strassenhöhe. Lohnt sich zu schauen, ob die Höhen über dir in der Sonne liegen - oft ist es so.",
            "Nebel macht die Welt für einen Tag flach. Dafür ist die Luft ruhig und es geht kein Wind.",
            "Die Sicht ist heute kurz. Wenn Erhöhungen in der Nähe sind: obendrüber steht oft die Sonne.",
            "Ein Nebeltag. Still, nah, und am Nachmittag meistens dünner.",
        ],
    },
    "first_frost": {
        "en": [
            "It is dropping to {temp_low} tonight. First real frost changes how the morning smells.",
            "Frost tonight - down to {temp_low}. Scrape the windscreen, and expect the grass to crunch.",
            "{temp_low} overnight. Cold enough to finish the tender plants and start the proper season.",
            "Clear and freezing tonight, around {temp_low}. Those two usually arrive together.",
            "Down to {temp_low} tonight. Frost mornings are cold, but they are also the bright ones.",
        ],
        "de": [
            "Heute Nacht geht es auf {temp_low} runter. Der erste richtige Frost verändert, wie der Morgen riecht.",
            "Frost heute Nacht - bis {temp_low}. Scheibe kratzen, und das Gras wird knirschen.",
            "{temp_low} über Nacht. Kalt genug, um die empfindlichen Pflanzen zu beenden und die Saison zu eröffnen.",
            "Klar und frostig heute Nacht, um {temp_low}. Die beiden kommen meistens zusammen.",
            "Bis {temp_low} heute Nacht. Frostmorgen sind kalt, aber es sind auch die hellen.",
        ],
    },
    "heat_day": {
        "en": [
            "{temp_high} today. The early morning and the late evening are the usable parts.",
            "It reaches {temp_high} today. Shade and water, and save anything strenuous for after seven.",
            "Heat of {temp_high} coming. The long evenings are the compensation - use them.",
            "{temp_high} at the peak. Worth being somewhere near water if you can manage it.",
            "A proper hot one, up to {temp_high}. The light lasts late, so there is no rush.",
        ],
        "de": [
            "Heute {temp_high}. Der frühe Morgen und der späte Abend sind die brauchbaren Teile.",
            "Es wird {temp_high} heute. Schatten und Wasser, und alles Anstrengende auf nach sieben legen.",
            "Hitze bis {temp_high}. Die langen Abende sind die Entschädigung - nutz sie.",
            "{temp_high} in der Spitze. Lohnt sich, in der Nähe von Wasser zu sein, wenn es geht.",
            "Ein richtig heisser Tag, bis {temp_high}. Das Licht bleibt lange, es eilt also nicht.",
        ],
    },

}


# ===== SEASONAL PHASE DESCRIPTIONS =====
SEASONAL_PHASE = {
    "deep_winter": {
        "en": [
            "This is January's deal: cold outside, but the light account is already growing.",
            "Deep winter has settled in, but the solstice already happened—the days are getting longer.",
            "The coldest weeks coincide with the start of light recovery. The pattern has already reversed.",
            "January's weather doesn't match its astronomy: the harshest cold comes after the light starts returning.",
            "Winter at its coldest, but astronomically we're already past the lowest point.",
        ],
        "de": [
            "Der Winter sitzt tief, aber die Sonnenwende ist durch – die Tage strecken sich wieder.",
            "Die kältesten Wochen treffen auf die Rückkehr des Lichts. Die Wende ist längst passiert.",
            "Das Wetter hinkt der Astronomie hinterher: Die Kälte kommt, wenn das Licht schon zurückkehrt.",
            "Tiefster Winter gefühlt, aber astronomisch ist das Schlimmste vorbei.",
            "Lass dich von der Kälte nicht täuschen, das Licht kommt zurück.",
            "Der Winter zeigt Zähne, aber die Sonne holt auf.",
            "Wir stecken mitten im Winter, aber der Weg führt Richtung Licht.",
            "Kalt, aber hoffnungsvoll: Die Tage werden wieder länger.",
        ],
    },
    "late_winter": {
        "en": [
            "Late winter shows real momentum now—daylight gains are accelerating noticeably.",
            "February's energy comes from knowing change is close and visible.",
            "This is the sprint phase: daylight gains accelerate toward the equinox.",
            "Late winter delivers evidence. The light proves change is coming.",
            "The push toward spring is obvious now. The light is moving fast.",
        ],
        "de": [
            "Die Energie des Februars: Man spürt, dass der Wandel nah ist.",
            "Sprintphase: Wir rasen auf die Tagundnachtgleiche zu.",
            "Der Schub Richtung Frühling ist unübersehbar. Das Licht macht Tempo.",
            "Es geht voran, und zwar schnell. Der Winter muss weichen.",
            "Jeden Tag ein bisschen mehr Frühling in der Luft.",
            "Das Licht drückt aufs Gaspedal.",
            "Es ist nicht mehr zu übersehen: Die dunkle Zeit endet.",
            "Der Februar macht ernst mit dem Frühling.",
        ],
    },
    "early_spring": {
        "en": [
            "The equinox is behind you. Days now outlast nights—the balance has shifted.",
            "Early spring is the exhale after winter. Light wins from here.",
            "You're in the bright half of the year now. That's the astronomy.",
            "Spring's arrival is official. The light proves what the weather sometimes denies.",
            "The equinox marked the turn. You're on the generous side of the calendar now.",
        ],
        "de": [
            "Die Tagundnachtgleiche liegt hinter uns. Die Tage sind jetzt länger als die Nächte.",
            "Frühling heißt Aufatmen nach dem Winter. Ab jetzt gewinnt das Licht.",
            "Willkommen in der hellen Jahreshälfte.",
            "Der Frühling ist offiziell. Das Licht beweist, was das Wetter vielleicht noch leugnet.",
            "Die Wende ist geschafft. Wir sind auf der Sonnenseite des Kalenders.",
            "Die Dunkelheit hat verloren, die Tage dominieren.",
            "Endlich mehr Licht als Schatten.",
            "Das große Aufwachen hat begonnen.",
            "Genieß das Plus an Helligkeit, es gehört jetzt uns.",
        ],
    },
    "late_spring": {
        "en": [
            "Late spring is the approach to peak light. The longest days are near.",
            "You're climbing toward the summit. Maximum light is weeks away.",
            "Late spring offers some of the best light conditions of the year.",
            "The climb toward summer solstice continues. Each day adds more.",
            "This is the phase where light is abundant. The peak is close.",
        ],
        "de": [
            "Später Frühling: Der Anflug auf das Licht-Maximum. Die längsten Tage sind greifbar.",
            "Wir klettern Richtung Gipfel. Das maximale Licht ist nur noch Wochen entfernt.",
            "Der Aufstieg zur Sommersonnenwende läuft. Jeden Tag ein Stückchen mehr.",
            "Es wird kaum noch dunkel.",
            "Wir baden förmlich in Tageslicht.",
            "Die Vorfreude auf den längsten Tag steigt.",
            "Helligkeit satt – das ist der späte Frühling.",
            "Jeden Abend bleibt es länger hell.",
        ],
    },
    "peak_summer": {
        "en": [
            "You're at the top. The year offers no longer day than these.",
            "Peak summer is the summit. From here, the only way is gently down.",
            "The longest days of the year are now. This is what the climb was for.",
            "Summer solstice territory: maximum light, maximum evening.",
            "You're standing at the peak of the light cycle.",
        ],
        "de": [
            "Ganz oben angekommen. Länger werden die Tage nicht mehr.",
            "Das sind die längsten Tage. Dafür haben wir den Winter durchgestanden.",
            "Sonnenwende-Territorium: maximales Licht, endlose Abende.",
            "Du stehst auf der Spitze des Lichtzyklus.",
            "Mehr Sommer geht nicht.",
            "Die Nächte sind nur noch kurze Pausen.",
            "Genieß den Höchststand der Sonne.",
            "Das Licht feiert seinen Triumph.",
            "Es sind die Tage, die nie enden wollen.",
            "Nutze die langen Abende, sie gehören dir.",
        ],
    },
    "late_summer": {
        "en": [
            "Late summer is the slow decline. Still bright, but the peak is behind you.",
            "The days are noticeably shorter than at the solstice, but still generous.",
            "Late summer is abundance with awareness. The light is receding.",
            "You're past the peak, but the descent is gentle. Summer lingers.",
            "The retreat from maximum light is underway, but slow.",
        ],
        "de": [
            "Spätsommer heißt Fülle mit Bewusstsein.",
            "Der Höhepunkt ist vorbei, aber der Sommer bleibt noch.",
            "Der Rückzug vom Maximum läuft, aber ganz gemächlich.",
            "Goldenes Licht und lange Abende.",
            "Der Sommer reift, das Licht wird wärmer.",
            "Genieß die Reste des langen Lichts.",
            "Es wird früher dunkel, aber es ist noch schön.",
            "Ein sanftes Ausklingen der hellen Jahreszeit.",
            "Die Abende sind immer noch ein Geschenk.",
        ],
    },
    "early_autumn": {
        "en": [
            "The equinox signals the shift. Nights now outlast days.",
            "Early autumn is the mirror of early spring—steep change, opposite direction.",
            "You've crossed into the dark half of the year. The nights are winning now.",
            "The descent accelerates through autumn. Each week is noticeably shorter.",
            "Early autumn is when the loss becomes obvious. Sunset comes earlier fast.",
        ],
        "de": [
            "Die Tagundnachtgleiche signalisiert den Wechsel. Die Nächte sind jetzt länger.",
            "Willkommen in der dunklen Jahreshälfte. Die Nächte übernehmen die Führung.",
            "Der Abstieg beschleunigt sich. Jede Woche wird spürbar kürzer.",
            "Es wird gemütlicher, aber auch dunkler.",
            "Die Balance kippt zur Dunkelheit.",
            "Der Herbst macht ernst: Kurze Tage voraus.",
            "Abschied vom langen Licht.",
            "Der Wandel ist jetzt nicht mehr zu leugnen.",
        ],
    },
    "late_autumn": {
        "en": [
            "Late autumn is the final approach to the year's minimum. The solstice is near.",
            "You're descending toward the bottom, but the turning point is in sight.",
            "Late autumn is the last stretch of darkness before the turnaround.",
            "The shortest days approach. Late autumn is the valley before the climb.",
            "November brings you close to the minimum. The solstice waits ahead.",
        ],
        "de": [
            "Spätherbst ist der Endanflug aufs Jahresminimum. Die Sonnenwende ist nah.",
            "Wir steigen zum Tiefpunkt ab, aber der Wendepunkt ist schon in Sicht.",
            "Die kürzesten Tage kommen. Das ist das Tal vor dem nächsten Aufstieg.",
            "Der November bringt uns nah ans Minimum. Bald geht's wieder aufwärts.",
            "Durchhalten, die Wende ist nicht mehr weit.",
            "Es wird dunkel, aber bald kehrt das Licht zurück.",
            "Die Zielgerade zum kürzesten Tag.",
            "Nur noch ein bisschen tiefer, dann kommt die Wende.",
        ],
    },
}


# ===== NATURE SIGNS BY MONTH =====
NATURE_SIGNS = {
    1: {
        "en": [
            "Robins are singing from bare branches—they hold territory even now. Listen for them.",
            "Check south-facing walls: daisies often bloom right through winter there.",
            "Hazel catkins turn yellow when temperatures rise. A sign spring is loading.",
            "Without leaves, raptors are easy to spot perched on fence posts. Look up.",
            "Great tits start their territory song on sunny January days. Spring practice.",
            "Squirrels are out searching for their hidden nuts. Watch for their acrobatics.",
        ],
        "de": [
            "Rotkehlchen singen auch jetzt von kahlen Ästen. Hör mal raus.",
            "Schau an Südmauern: Gänseblümchen blühen dort oft den ganzen Winter durch.",
            "Haselkätzchen werden gelb, sobald es etwas wärmer wird. Ein Zeichen.",
            "Ohne Laub sind Greifvögel auf Zaunpfählen gut zu entdecken. Schau hoch.",
            "Kohlmeisen üben an sonnigen Tagen schon ihren Reviergesang.",
            "Eichhörnchen suchen tagsüber nach ihren versteckten Nüssen.",
            "Die tiefe Sonne wirft lange Schatten – Konturen werden sichtbar.",
            "Moos im Wald leuchtet jetzt besonders grün ohne Konkurrenz.",
        ],
    },
    2: {
        "en": [
            "Snowdrops are pushing through. Check old gardens and churchyards.",
            "Bumblebee queens wake on warm days, searching for nest sites.",
            "Birdsong is getting louder. The dawn chorus is building.",
            "Tree buds are swelling visibly. Life is preparing.",
            "Woodpeckers drum louder now—bare trunks make perfect resonators.",
        ],
        "de": [
            "Schneeglöckchen schieben sich durch. Schau in alten Gärten.",
            "Hummelköniginnen wachen an warmen Tagen auf und suchen Nistplätze.",
            "Der Vogelgesang wird lauter. Die Vögel bereiten sich vor.",
            "Knospen schwellen sichtbar an den Zweigen. Das Leben rüstet sich.",
            "Spechte trommeln lauter – kahle Stämme sind perfekte Verstärker.",
            "An windstillen Stellen tanzen kleine Mückenschwärme im Licht.",
            "Kastanienknospen glänzen schon dick und klebrig.",
        ],
    },
    3: {
        "en": [
            "Daffodils are out. Wild ones in woods, cultivated ones in gardens.",
            "Blackbirds sing before sunrise now. Worth waking up for.",
            "Wild garlic appears in woodlands. Follow your nose.",
            "Frogs are active in ponds. Listen for their calls at dusk.",
            "The equinox means days now beat nights. The bright half begins.",
        ],
        "de": [
            "Narzissen blühen. Wilde im Wald, zahme in Gärten.",
            "Amseln singen jetzt schon vor Sonnenaufgang. Lohnt das frühe Aufstehen.",
            "Bärlauch taucht im Wald auf. Folge deiner Nase.",
            "Frösche sind in Teichen aktiv. Hör abends mal hin.",
            "Nach der Tagundnachtgleiche sind die Tage länger. Die helle Hälfte beginnt.",
        ],
    },
    4: {
        "en": [
            "Cherry blossom in April sun—one of the year's best sights.",
            "The dawn chorus is intense. Get up early, it starts before 5 AM.",
            "Butterflies are out: orange tips, peacocks, small whites.",
            "Apple blossom scent fills the air. Notice it on your walks.",
            "Swallows are arriving. Watch for them swooping low.",
        ],
        "de": [
            "Kirschblüten in der Aprilsonne – einer der schönsten Anblicke.",
            "Das Morgenkonzert ist jetzt laut. Früh aufstehen lohnt sich.",
            "Schmetterlinge sind unterwegs: Aurorafalter, Tagpfauenaugen.",
            "Apfelblüten duften. Achte drauf beim Spazieren.",
            "Die Schwalben kommen zurück. Beobachte ihre Flugkünste.",
        ],
    },
    5: {
        "en": [
            "Swifts are back, screaming through evening skies. Summer is here.",
            "Butterflies everywhere now. Watch for painted ladies and commas.",
            "May evenings stay light past 9 PM. Use them.",
            "Everything is growing, flowering, or nesting. Peak activity.",
            "Lilac and elderflower scent the evening air.",
        ],
        "de": [
            "Mauersegler sind zurück und jagen schreiend durch den Himmel.",
            "Schmetterlinge überall. Distelfalter und C-Falter beobachten.",
            "Maiabende bleiben bis nach 21 Uhr hell. Nutz sie.",
            "Alles wächst, blüht oder brütet. Hochbetrieb in der Natur.",
            "Flieder und Holunder parfümieren die Abendluft.",
        ],
    },
    6: {
        "en": [
            "These are nearly the longest days. Sunset after 9:30 PM.",
            "Swifts are everywhere, feeding hard. Watch their aerial shows.",
            "Roses are at their peak. Stop and smell them.",
            "Twilight lasts until almost 11 PM. The nights barely get dark.",
            "Bees work late into the evening on long June days.",
        ],
        "de": [
            "Fast die längsten Tage. Sonne bis nach halb zehn.",
            "Mauersegler jagen überall. Schau ihren Flugshows zu.",
            "Rosen sind auf dem Höhepunkt. Stehenbleiben und riechen.",
            "Die Dämmerung dauert fast bis 23 Uhr. Kaum Dunkelheit.",
            "Bienen arbeiten an langen Junitagen bis spät abends.",
        ],
    },
    7: {
        "en": [
            "Lavender and buddleia attract clouds of butterflies. Watch for peacocks.",
            "July evenings are warm enough to sit out until 10 PM.",
            "Crickets chirp on warm nights. Summer soundtrack.",
            "Wild strawberries are ripe in forest clearings.",
            "Swifts will leave soon. Appreciate them while they're here.",
        ],
        "de": [
            "Lavendel und Sommerflieder ziehen Schmetterlinge an. Beobachte sie.",
            "Juliabende sind warm genug zum Draußensitzen bis 22 Uhr.",
            "Grillen zirpen in warmen Nächten. Sommermusik.",
            "Walderdbeeren sind reif an Lichtungen.",
            "Die Mauersegler gehen bald. Genieß sie noch.",
        ],
    },
    8: {
        "en": [
            "Blackberries are ripe. Free snacks on every walk.",
            "August light has a golden quality. Autumn is approaching.",
            "Swifts are leaving. The first sign summer is waning.",
            "Apples are ripening. Check old orchards.",
            "Spiders build impressive webs. Morning dew makes them visible.",
        ],
        "de": [
            "Brombeeren sind reif. Gratis-Snacks bei jedem Spaziergang.",
            "Augustlicht hat diese goldene Qualität. Der Herbst naht.",
            "Die Mauersegler gehen. Erstes Zeichen, dass der Sommer endet.",
            "Äpfel reifen. Schau in alten Obstgärten vorbei.",
            "Spinnen bauen imposante Netze. Morgentau macht sie sichtbar.",
        ],
    },
    9: {
        "en": [
            "September sun on turning leaves—the color show begins.",
            "Apples, pears, plums are ready. Harvest time.",
            "Migrating birds gather. Watch for swallow flocks.",
            "Mushrooms appear after rain. Check forest edges.",
            "Days shorten fast now. Notice the earlier sunsets.",
        ],
        "de": [
            "Septembersonne auf bunten Blättern – die Farbshow beginnt.",
            "Äpfel, Birnen, Pflaumen sind reif. Erntezeit.",
            "Zugvögel sammeln sich. Schau nach Schwalbenschwärmen.",
            "Pilze erscheinen nach Regen. Schau an Waldrändern.",
            "Die Tage werden jetzt schnell kürzer. Achte auf frühere Sonnenuntergänge.",
        ],
    },
    10: {
        "en": [
            "Peak autumn color now. One of the year's best sights.",
            "Clear October days are cold but beautiful. Treasure them.",
            "Squirrels are busy burying nuts. Winter prep.",
            "Geese fly south in V-formation. Listen for their calls.",
            "First frosts reveal spider webs in morning grass.",
        ],
        "de": [
            "Herbstfarben auf dem Höhepunkt. Einer der schönsten Anblicke.",
            "Klare Oktobertage sind kalt, aber wunderschön. Schätz sie.",
            "Eichhörnchen vergraben emsig Nüsse. Wintervorrat.",
            "Gänse ziehen in V-Formation nach Süden. Hör auf ihre Rufe.",
            "Erster Frost macht Spinnennetze im Morgengras sichtbar.",
        ],
    },
    11: {
        "en": [
            "November sun is precious. Bare trees let it through.",
            "Fieldfare and redwing arrive from the north. Winter visitors.",
            "Mistle thrushes sing even in rain. The storm-cock.",
            "Fallen leaves reveal hidden paths and structures.",
            "Fungi season continues in mild spells.",
        ],
        "de": [
            "Novembersonne ist kostbar. Kahle Bäume lassen sie durch.",
            "Wacholderdrosseln kommen aus dem Norden. Wintergäste.",
            "Misteldrosseln singen sogar im Regen. Unerschütterlich.",
            "Gefallene Blätter geben Blick auf versteckte Pfade frei.",
            "Pilzsaison geht bei mildem Wetter weiter.",
        ],
    },
    12: {
        "en": [
            "Every minute of December sun counts. Go outside when it's there.",
            "Robins sing all winter. They're staking territory for spring.",
            "Evergreen ivy and mistletoe are the only green in bare trees.",
            "After the solstice, days lengthen. The turn has happened.",
            "Winter ducks from the north gather on lakes and rivers.",
        ],
        "de": [
            "Jede Minute Dezembersonne zählt. Geh raus, wenn sie scheint.",
            "Rotkehlchen singen den ganzen Winter. Sie sichern ihr Revier.",
            "Efeu und Misteln sind das einzige Grün in kahlen Kronen.",
            "Nach der Sonnenwende werden die Tage länger. Die Wende ist da.",
            "Winterenten aus dem Norden sammeln sich auf Seen und Flüssen.",
        ],
    },
}


# ===== WEATHER-DEPENDENT NATURE OBSERVATIONS =====
NATURE_WEATHER = {
    "clear": {
        "en": [
            "Clear skies tonight mean good stargazing. Look up after dark.",
            "Sunny days bring lizards out on warm stones. Watch for them.",
            "Raptors ride thermals on sunny days. Easy to spot circling.",
            "Bees are extra active in sunshine. Watch them at any flower.",
            "Butterflies need this warmth to fly. Good day to spot them.",
        ],
        "de": [
            "Klarer Himmel heißt gute Sternennacht. Schau später mal hoch.",
            "Sonnige Tage locken Eidechsen auf warme Steine.",
            "Greifvögel kreisen in der Thermik. Gut zu beobachten.",
            "Bienen sind bei Sonne besonders fleißig. Schau ihnen zu.",
            "Schmetterlinge brauchen diese Wärme zum Fliegen. Guter Tag.",
        ],
    },
    "rain": {
        "en": [
            "Rain brings worms up. Blackbirds and thrushes are feasting.",
            "Snails are out after rain. Watch where you step.",
            "Frogs are more active in wet weather. Listen at dusk.",
            "The garden smells intensely green after rain.",
            "Robins keep singing even in the rain. Tough little birds.",
        ],
        "de": [
            "Regen bringt Würmer hoch. Amseln und Drosseln schlemmen.",
            "Schnecken sind nach Regen unterwegs. Pass auf beim Gehen.",
            "Frösche sind bei Nässe aktiver. Hör abends hin.",
            "Der Garten duftet nach Regen intensiv grün.",
            "Rotkehlchen singen auch im Regen weiter. Zähe Vögel.",
        ],
    },
    "grey": {
        "en": [
            "Overcast days are perfect for forest walks. Soft light, no shadows.",
            "Grey skies make autumn colors pop. Good for photos.",
            "Owls sometimes hunt earlier on dark days. Watch for them.",
            "Foxes are bolder in dim light. You might spot one.",
            "Moss glows green on grey days. Worth a closer look.",
        ],
        "de": [
            "Bedeckte Tage sind perfekt für Waldspaziergänge. Weiches Licht.",
            "Grauer Himmel lässt Herbstfarben leuchten. Gut für Fotos.",
            "Eulen jagen manchmal früher an dunklen Tagen. Augen offen.",
            "Füchse trauen sich mehr bei Dämmerlicht.",
            "Moos leuchtet an grauen Tagen besonders grün.",
        ],
    },
    "snow": {
        "en": [
            "Fresh snow reveals animal tracks. Look for fox, rabbit, bird prints.",
            "Birds need extra food in snow. Fill the feeder if you have one.",
            "Robins look beautiful against white snow.",
            "Snow muffles sound. The world is quieter.",
            "Deer come to forest edges searching for food.",
        ],
        "de": [
            "Frischer Schnee zeigt Tierspuren. Fuchs, Hase, Vögel – alles lesbar.",
            "Vögel brauchen bei Schnee extra Futter. Füll das Vogelhäuschen.",
            "Rotkehlchen leuchten vor weißem Schnee besonders schön.",
            "Schnee schluckt Geräusche. Alles ist stiller.",
            "Rehe kommen an Waldränder auf Futtersuche.",
        ],
    },
}


# ===== DAYLIGHT FACTS TEMPLATES =====
DAYLIGHT_FACTS = {
    "en": [
        "Today you have {day_length} of daylight, running from {sunrise} to {sunset}.",
        "The day runs {day_length}, with sunrise at {sunrise} and sunset at {sunset}.",
        "Daylight today: {day_length}. The sun is up from {sunrise} to {sunset}.",
        "You're working with {day_length} of light today, {sunrise} to {sunset}.",
    ],
    "de": [
        "Heute hast du {day_length} Tageslicht, von {sunrise} bis {sunset}.",
        "Der Tag bringt dir {day_length} Licht – Aufgang {sunrise}, Untergang {sunset}.",
        "Lichtbilanz heute: {day_length}. Sonne von {sunrise} bis {sunset}.",
        "{day_length} Helligkeit stehen dir heute zur Verfügung ({sunrise} bis {sunset}).",
        "Zwischen {sunrise} und {sunset} ist es hell – insgesamt {day_length}.",
        "Lichtdauer heute: {day_length}.",
        "Von {sunrise} bis {sunset} regiert die Sonne ({day_length}).",
    ],
}


# ===== DELTA PHRASES =====
DELTA_PHRASES = {
    "gaining": {
        "en": [
            "That's {delta} {minutes} more than yesterday.",
            "You gained {delta} {minutes} compared to yesterday.",
            "+{delta} {minutes} versus yesterday.",
        ],
        "de": [
            "Das sind {delta} {minutes} mehr als gestern.",
            "Du hast {delta} {minutes} im Vergleich zu gestern gewonnen.",
            "+{delta} {minutes} gegenüber gestern.",
            "Der Tag ist um {delta} {minutes} gewachsen.",
        ],
    },
    "losing": {
        "en": [
            "That's {delta} {minutes} less than yesterday.",
            "You lost {delta} {minutes} compared to yesterday.",
            "{delta} {minutes} shorter than yesterday.",
        ],
        "de": [
            "Das sind {delta} {minutes} weniger als gestern.",
            "Du hast {delta} {minutes} im Vergleich zu gestern verloren.",
            "{delta} {minutes} kürzer als gestern.",
            "Der Tag ist um {delta} {minutes} geschrumpft.",
        ],
    },
}


# ===== Winter =====
#
# From November to March the message is about the light coming back rather
# than about the weather. These entries are written as complete thoughts,
# usually two sentences, so the text reads as one piece instead of a handful
# of unrelated observations stitched together.
#
# Placeholders resolve only when the fact behind them was actually measured:
#   {day_length} {sunrise} {sunset}   - today's figures
#   {delta} {minutes}                 - gain against yesterday, only if positive
#   {hours_gained}                    - gain since the solstice, only if positive
#   {milestone_time} {milestone_days} {days_dat}
#                                     - the next half-hour mark the sunset
#                                       crosses, straight from the forecast
# Anything unavailable simply removes the templates that mentioned it.

WINTER_ANTICIPATION = {
    "en": [
        # -- measurable gain since the solstice
        "The light has already turned. Since the solstice the day has grown by {hours_gained}, whether or not it feels like it yet.",
        "You are {hours_gained} past the shortest day. That is not nothing, even if the mornings still argue otherwise.",
        "Quietly, without ceremony, the year has handed back {hours_gained} of daylight since the solstice.",
        "The darkest day is behind you by {hours_gained} of light. The direction of travel is settled now.",
        "Since the solstice: {hours_gained} more light. It accumulates whether you notice it or not.",
        "{hours_gained} of daylight have come back since the turn of the year. The rest arrives on its own schedule.",

        # -- daily gain
        "Today is {delta} {minutes} longer than yesterday. Small, but it happens again tomorrow.",
        "Another {delta} {minutes} of light today. The gain is small enough to miss and steady enough to count on.",
        "The day gained {delta} {minutes} overnight. That is roughly a whole extra hour every month at this rate.",
        "{delta} more {minutes} than yesterday. Winter is being dismantled one of these at a time.",
        "Yesterday's day was {delta} {minutes} shorter than this one. The trend only goes one way from here.",

        # -- the sunset milestone, straight from the forecast
        "In {milestone_days} {days} the sun sets after {milestone_time} again. Something to look forward to on the way home.",
        "Mark it: {milestone_days} {days} from now the sunset moves past {milestone_time}. Evenings start feeling different around then.",
        "The sun currently sets at {sunset}. In {milestone_days} {days_dat} that becomes {milestone_time}, and the afternoon stretches out a little.",
        "{milestone_days} {days_dat} until sunset passes {milestone_time}. The evenings are being handed back to you.",

        # -- today's figures, framed forward
        "Sunrise {sunrise}, sunset {sunset} - {day_length} of daylight, and more of it tomorrow.",
        "{day_length} of light today. Every one of the coming weeks adds to that.",
        "The day runs {day_length} at the moment. By spring you will barely recognise that number.",
        "Light from {sunrise} to {sunset} today. Both ends of that are still moving in your favour.",

        # -- pure anticipation, no figures required
        "The cold is still doing its thing, but the light has already changed its mind.",
        "Winter is loud right now and the light is quiet about it. The light is the one that wins.",
        "Nothing about today needs to feel like spring for spring to be on its way.",
        "This is the part of the year that asks for patience. It has never failed to pay it back.",
        "The hardest stretch of the year is also the one that is already improving.",
        "Somewhere under all this, the ground is keeping time. It knows what comes next.",
        "The year has turned. Everything from here is a slow argument in favour of the light.",
        "It is still dark early, and it is already less dark than it was.",
        "The season is not over, but it has stopped growing. That counts for something.",
        "Grey days are easier to sit with when the light behind them is lengthening.",
        "You are on the returning side of the year now. That is worth knowing on a morning like this.",
        "Cold and bright is a fair trade in February. Cold and lengthening is a better one.",
    ],
    "de": [
        # -- messbarer Zuwachs seit der Sonnenwende
        "Das Licht hat schon gedreht. Seit der Sonnenwende ist der Tag um {hours_gained} gewachsen, auch wenn es sich noch nicht so anfühlt.",
        "Du bist {hours_gained} über den kürzesten Tag hinaus. Das ist nicht nichts, selbst wenn die Morgen noch dagegenhalten.",
        "Ganz ohne Aufhebens hat das Jahr seit der Sonnenwende {hours_gained} Tageslicht zurückgegeben.",
        "Der dunkelste Tag liegt {hours_gained} Licht hinter dir. Die Richtung steht inzwischen fest.",
        "Seit der Sonnenwende: {hours_gained} mehr Licht. Das sammelt sich an, ob man es bemerkt oder nicht.",
        "{hours_gained} Tageslicht sind seit der Jahreswende zurückgekommen. Der Rest kommt in seinem eigenen Tempo.",

        # -- täglicher Zuwachs
        "Heute ist {delta} {minutes} länger als gestern. Wenig, aber morgen passiert es wieder.",
        "Wieder {delta} {minutes} mehr Licht heute. Klein genug, um es zu übersehen, und stetig genug, sich darauf zu verlassen.",
        "Der Tag hat über Nacht {delta} {minutes} gewonnen. In dem Tempo ist das ungefähr eine ganze Stunde pro Monat.",
        "{delta} {minutes} mehr als gestern. So wird der Winter abgebaut, Stück für Stück.",
        "Gestern war der Tag {delta} {minutes} kürzer als heute. Von hier aus geht es nur noch in eine Richtung.",

        # -- der Sonnenuntergangs-Meilenstein, direkt aus der Vorhersage
        "In {milestone_days} {days_dat} geht die Sonne wieder nach {milestone_time} unter. Etwas, worauf man sich auf dem Heimweg freuen kann.",
        "Merk dir das: in {milestone_days} {days_dat} wandert der Sonnenuntergang hinter {milestone_time}. Ab dann fühlen sich die Abende anders an.",
        "Die Sonne geht gerade um {sunset} unter. In {milestone_days} {days_dat} ist es {milestone_time}, und der Nachmittag wird spürbar länger.",
        "Noch {milestone_days} {days_dat}, bis der Sonnenuntergang {milestone_time} überschreitet. Die Abende kommen zurück.",

        # -- heutige Zahlen, nach vorn gedacht
        "Aufgang {sunrise}, Untergang {sunset} - {day_length} Tageslicht, und morgen etwas mehr.",
        "{day_length} Licht heute. Jede der kommenden Wochen legt darauf noch etwas drauf.",
        "Der Tag dauert im Moment {day_length}. Im Frühling wirst du diese Zahl kaum wiedererkennen.",
        "Licht von {sunrise} bis {sunset} heute. Beide Enden verschieben sich weiter zu deinen Gunsten.",

        # -- reine Vorfreude, ohne Zahlen
        "Die Kälte macht noch ihr Ding, aber das Licht hat es sich bereits anders überlegt.",
        "Der Winter ist gerade laut und das Licht ist still dabei. Gewinnen wird das Licht.",
        "Nichts an heute muss sich nach Frühling anfühlen, damit der Frühling unterwegs ist.",
        "Das ist der Teil des Jahres, der Geduld verlangt. Zurückgezahlt hat er sie noch immer.",
        "Der härteste Abschnitt des Jahres ist zugleich der, der sich schon bessert.",
        "Irgendwo unter alldem hält der Boden die Zeit. Er weiß, was als Nächstes kommt.",
        "Das Jahr hat gewendet. Alles ab hier ist ein langsames Argument für das Licht.",
        "Es wird noch früh dunkel, und es ist schon weniger dunkel als es war.",
        "Die Jahreszeit ist nicht vorbei, aber sie wächst nicht mehr. Das zählt.",
        "Graue Tage lassen sich leichter aushalten, wenn das Licht dahinter länger wird.",
        "Du bist jetzt auf der zurückkehrenden Seite des Jahres. Das ist an so einem Morgen etwas wert.",
        "Kalt und hell ist im Februar ein fairer Tausch. Kalt und länger werdend ist ein besserer.",
    ],
}


# Suggestions for actually using the light when it is there. Kept concrete and
# small enough to act on the same day.
SUN_ENJOYMENT = {
    "en": [
        "If the sun is out at lunch, take it outside. Twenty minutes does more than it sounds like.",
        "Worth stepping out while it is bright - the light does its work through your eyes, not your skin.",
        "A short walk while the sun is up beats a long one after dark. Take it if you can.",
        "Sit by the window if you cannot get out. It is a fraction of the dose, but it is not nothing.",
        "Morning light counts double in winter. Get some in the first hour you are awake if you can.",
        "The brightest part of the day is short right now. Spending some of it outside is rarely regretted.",
        "If there is a south-facing bench anywhere near you, this is its moment.",
        "Coffee outside instead of at the desk - small trade, noticeable difference.",
        "Clear and cold beats grey and mild for this. Wrap up and take the light while it is offered.",
        "Even ten minutes out there resets something. It does not need to be a proper walk.",
    ],
    "de": [
        "Wenn mittags die Sonne da ist, nimm sie mit nach draußen. Zwanzig Minuten bringen mehr, als es klingt.",
        "Lohnt sich, rauszugehen solange es hell ist - das Licht wirkt über die Augen, nicht über die Haut.",
        "Ein kurzer Spaziergang bei Sonne schlägt einen langen nach Einbruch der Dunkelheit.",
        "Wenn du nicht rauskommst, setz dich ans Fenster. Ein Bruchteil der Dosis, aber besser als nichts.",
        "Morgenlicht zählt im Winter doppelt. Hol dir etwas davon in der ersten Stunde nach dem Aufstehen.",
        "Der hellste Teil des Tages ist gerade kurz. Ihn draußen zu verbringen bereut man selten.",
        "Falls irgendwo in deiner Nähe eine Bank nach Süden zeigt: jetzt ist ihr Moment.",
        "Kaffee draußen statt am Schreibtisch - kleiner Tausch, spürbarer Unterschied.",
        "Klar und kalt ist dafür besser als grau und mild. Warm anziehen und das Licht mitnehmen.",
        "Auch zehn Minuten draußen setzen etwas zurück. Es muss kein richtiger Spaziergang sein.",
    ],
}


# Early signs of spring, by coarse region and month. Regions come from
# _region() in uplift_engine: "alpine" covers Switzerland and the pre-alpine
# foothills, which is where most users are; "central_europe" is the wider
# lowland band; "generic" avoids naming any species that might be absent.
#
# Everything here has to hold for an ordinary year in that region. Where
# timing varies, the wording hedges ("about now", "any week") rather than
# claiming a date it cannot know.

SPRING_SIGNS = {
    "alpine": {
        "en": {
            1: ["Snowdrops are already pushing up in sheltered gardens down in the valleys.",
                "Hazel catkins are lengthening on the warmer slopes - the first pollen of the year.",
                "On south-facing hillsides the snow is starting to pull back around the rocks.",
                "Great tits have begun their two-note call on mild mornings. That is a spring sound."],
            2: ["Hazel and alder are in flower in the lowlands; the first pollen is already moving.",
                "Snowdrops and winter aconite are out wherever the ground has thawed.",
                "Blackbirds start singing again from the rooftops around now.",
                "Down by the lakes the willows are showing their first silver catkins.",
                "The high snowpack is settling. Below about a thousand metres it is losing ground fast."],
            3: ["Crocuses are opening across the lawns and the bees have found them.",
                "Cherry and blackthorn buds are swelling in the orchards.",
                "The first bumblebee queens are out looking for nest sites.",
                "Alpine pastures below the treeline are turning green from the bottom up.",
                "Cranes and the first migrants are moving back north over the plateau."],
            4: ["The valley orchards are in blossom - the couple of weeks worth planning around.",
                "Meadows are filling with dandelion and the first cowslips.",
                "Marmots are coming out of hibernation up on the alps.",
                "Beech woods are going that particular green that only lasts a fortnight."],
        },
        "de": {
            1: ["In geschützten Gärten im Tal schieben die Schneeglöckchen schon.",
                "An den wärmeren Hängen strecken sich die Haselkätzchen - der erste Pollen des Jahres.",
                "An Südhängen zieht sich der Schnee rund um die Felsen langsam zurück.",
                "Die Kohlmeise ruft an milden Morgen wieder zweisilbig. Das ist ein Frühlingsgeräusch."],
            2: ["Hasel und Erle blühen im Flachland, der erste Pollen ist unterwegs.",
                "Schneeglöckchen und Winterlinge stehen überall dort, wo der Boden aufgetaut ist.",
                "Die Amseln singen um diese Zeit wieder von den Dächern.",
                "Unten an den Seen zeigen die Weiden ihre ersten silbrigen Kätzchen.",
                "Die Schneedecke setzt sich. Unterhalb von etwa tausend Metern verliert sie schnell."],
            3: ["Krokusse öffnen sich auf den Wiesen und die Bienen haben sie gefunden.",
                "In den Obstgärten schwellen die Knospen von Kirsche und Schlehe.",
                "Die ersten Hummelköniginnen suchen nach Nistplätzen.",
                "Die Alpweiden unterhalb der Waldgrenze werden von unten herauf grün.",
                "Kraniche und die ersten Zugvögel ziehen wieder über das Mittelland nach Norden."],
            4: ["Die Obstgärten im Tal blühen - die zwei Wochen, um die herum man planen sollte.",
                "Die Wiesen füllen sich mit Löwenzahn und den ersten Schlüsselblumen.",
                "Oben auf den Alpen kommen die Murmeltiere aus dem Winterschlaf.",
                "Die Buchenwälder nehmen dieses bestimmte Grün an, das nur vierzehn Tage hält."],
        },
    },
    "central_europe": {
        "en": {
            1: ["Snowdrops are up in the sheltered corners of gardens and parks.",
                "Hazel catkins are lengthening - the first pollen of the year is on its way.",
                "Great tits have started their two-note call on the milder mornings."],
            2: ["Hazel and alder are flowering; the first pollen is already in the air.",
                "Blackbirds are singing from the rooftops again around now.",
                "Winter aconite and snowdrops are out wherever the ground has thawed.",
                "Rooks and jackdaws are pairing up and inspecting last year's nests."],
            3: ["Crocuses are open across the parks and the first bees are on them.",
                "Blackthorn is coming into flower along the field edges.",
                "The first bumblebee queens are out hunting for nest sites.",
                "Migrating birds are moving back through - cranes on the high routes."],
            4: ["The orchards are in blossom, which is a short and worthwhile window.",
                "Dandelions are taking over the verges and the meadows are thickening.",
                "Beech and birch are unfolding that brief, particular green.",
                "Swallows are arriving back at last year's nesting sites."],
        },
        "de": {
            1: ["In geschützten Ecken von Gärten und Parks stehen die Schneeglöckchen.",
                "Die Haselkätzchen strecken sich - der erste Pollen des Jahres ist unterwegs.",
                "An milderen Morgen ruft die Kohlmeise wieder zweisilbig."],
            2: ["Hasel und Erle blühen, der erste Pollen liegt schon in der Luft.",
                "Die Amseln singen um diese Zeit wieder von den Dächern.",
                "Winterlinge und Schneeglöckchen stehen überall, wo der Boden aufgetaut ist.",
                "Saatkrähen und Dohlen finden sich paarweise und begutachten die alten Nester."],
            3: ["In den Parks sind die Krokusse offen und die ersten Bienen sitzen darauf.",
                "An den Feldrändern fängt die Schlehe an zu blühen.",
                "Die ersten Hummelköniginnen suchen nach Nistplätzen.",
                "Der Vogelzug geht wieder nach Norden - Kraniche auf den hohen Routen."],
            4: ["Die Obstgärten blühen. Ein kurzes Fenster, das sich lohnt.",
                "Der Löwenzahn übernimmt die Ränder und die Wiesen werden dichter.",
                "Buche und Birke entfalten dieses kurze, besondere Grün.",
                "Die Schwalben kommen an den Nistplätzen vom Vorjahr wieder an."],
        },
    },
    "generic": {
        "en": {
            1: ["The first buds are already sitting on the branches, waiting.",
                "Birdsong starts earlier in the morning than it did a month ago."],
            2: ["Buds are visibly swelling on the bare branches.",
                "The dawn chorus is filling out again, a little earlier each week."],
            3: ["Green is coming back at ground level, ahead of the trees.",
                "Insects are about again on the warmer afternoons."],
            4: ["The trees are coming into leaf and the light through them changes everything.",
                "Everything that overwintered is moving again."],
        },
        "de": {
            1: ["Die ersten Knospen sitzen schon an den Zweigen und warten.",
                "Der Vogelgesang beginnt morgens früher als noch vor einem Monat."],
            2: ["An den kahlen Zweigen schwellen die Knospen sichtbar.",
                "Der Morgenchor wird wieder voller, jede Woche etwas früher."],
            3: ["Am Boden kommt das Grün zurück, noch vor den Bäumen.",
                "An den wärmeren Nachmittagen sind wieder Insekten unterwegs."],
            4: ["Die Bäume treiben aus, und das Licht dazwischen verändert alles.",
                "Alles, was überwintert hat, ist wieder in Bewegung."],
        },
    },
}


# Near the equator the day barely changes length all year, so the returning
# light has nothing to say. This mode stays short and talks about the day
# itself instead.
TROPICS = {
    "en": [
        "The day runs close to twelve hours here, as it does most of the year. The rhythm comes from the sky, not the calendar.",
        "Sunrise and sunset barely move this close to the equator. What changes is the weather, not the light.",
        "Around twelve hours of daylight, near enough all year. The seasons here are wet and dry rather than light and dark.",
        "The sun keeps to its schedule here. {day_length} today, much the same tomorrow.",
        "Light from {sunrise} to {sunset} - and roughly the same next month, and the month after.",
        "No long evenings to wait for here, and no dark mornings to endure either. An even trade.",
        "The length of the day is settled at this latitude. Everything interesting happens in the clouds.",
        "{day_length} of daylight, steady as it goes. Worth using while the weather cooperates.",
    ],
    "de": [
        "Der Tag dauert hier nahe an zwölf Stunden, wie fast das ganze Jahr. Der Rhythmus kommt vom Himmel, nicht vom Kalender.",
        "So nah am Äquator bewegen sich Auf- und Untergang kaum. Was wechselt, ist das Wetter, nicht das Licht.",
        "Rund zwölf Stunden Tageslicht, praktisch das ganze Jahr. Die Jahreszeiten heißen hier nass und trocken statt hell und dunkel.",
        "Die Sonne hält sich hier an ihren Fahrplan. Heute {day_length}, morgen so ziemlich dasselbe.",
        "Licht von {sunrise} bis {sunset} - und nächsten Monat ungefähr genauso, und den Monat darauf auch.",
        "Keine langen Abende, auf die man warten muss, aber auch keine dunklen Morgen. Ein fairer Tausch.",
        "Auf dieser Breite ist die Tageslänge eine feste Größe. Alles Interessante passiert in den Wolken.",
        "{day_length} Tageslicht, gleichmäßig wie immer. Lohnt sich zu nutzen, solange das Wetter mitspielt.",
    ],
}
