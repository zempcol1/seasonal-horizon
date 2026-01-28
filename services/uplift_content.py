"""
Dynamic content library for Seasonal Horizon.
Multilingual support: English (en) and German (de).
"""

# ===== FORECAST NARRATIVES =====
FORECAST_NARRATIVES = {
    "rain_clearing_soon": {
        "en": [
            "Grey skies today, but the forecast shows {clear_day} breaking through—just {days_until} more days to wait.",
            "The rain is temporary. By {clear_day}, the clouds lift and you'll have your moment in the sun.",
            "Hold steady through the grey. {clear_day} brings the clearing you're waiting for.",
            "This wet stretch has an end date: {clear_day}. Mark your calendar.",
            "Today's drizzle is just weather passing through. {clear_day}'s sunshine is coming.",
            "The clouds are visitors, not residents. They leave by {clear_day}.",
            "Patience pays: {days_until} days of grey, then {clear_day} delivers clear skies.",
            "Rain now, but I can see {clear_day} on the forecast—good conditions are coming.",
            "Every rainy streak has its last day. This one ends before {clear_day}.",
            "Wet windows today, but {clear_day} is circled on the weather chart.",
        ],
        "de": [
            "Heute bleibt der Himmel grau, doch laut Vorhersage bricht am {clear_day} die Sonne durch – nur noch {days_until} Tage durchhalten.",
            "Der Regen ist nur vorübergehend. Bis {clear_day} lichten sich die Wolken, dann gehört die Sonne dir.",
            "Einfach durchhalten bei diesem Grau. Am {clear_day} klart es endlich auf.",
            "Diese Regenphase hat ein Enddatum: {clear_day}. Schon mal im Kalender markieren.",
            "Der Nieselregen heute zieht nur durch. Am {clear_day} wartet Sonnenschein.",
            "Die Wolken sind nur zu Besuch – bis {clear_day} ziehen sie weiter.",
            "Geduld zahlt sich aus: noch {days_until} graue Tage, dann liefert der {clear_day} blauen Himmel.",
            "Gerade regnet es, aber der {clear_day} sieht vielversprechend aus.",
            "Jede Regenphase hat ihren letzten Tag. Diese endet spätestens am {clear_day}.",
            "Heute trommelt der Regen ans Fenster, aber der {clear_day} ist schon vorgemerkt.",
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
            "Jetzt ist deine Chance. Am {rain_day} kommt Regen – der heutige Sonnenschein ist Gold wert.",
            "Die Sonne ist da, aber sie packt schon für den {rain_day}. Nutze die Gelegenheit.",
            "Der blaue Himmel hat ein Verfallsdatum: {rain_day}. Mach das Beste aus heute.",
            "Sonnenschein auf Zeit – am {rain_day} ist Schluss damit. Erledige alles, was draußen ansteht.",
            "Die Vorhersage gibt dir Zeit bis {rain_day}. Das ist deine Frist für Outdoor-Pläne.",
            "Heute ist der gute Tag, am {rain_day} wird es nass. Handle entsprechend.",
            "Diese Sonne wartet nicht. Am {rain_day} wirst du dir wünschen, du hättest heute etwas unternommen.",
            "Das Wetterfenster schließt sich am {rain_day}. Heute steht dir noch alles offen.",
            "Spar dir den Sonnenschein nicht auf – am {rain_day} ist er ohnehin weg.",
            "Blauer Himmel heute, grau am {rain_day}. Wenn du draußen was erledigen willst: jetzt oder nie.",
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
            "Das Thermometer klettert die ganze Woche nach oben – bis zum Ende wird es {temp_change}°C wärmer. Die Jahreszeit dreht sich spürbar.",
            "Jeder Tag diese Woche ist wärmer als der davor. Der Wandel ist förmlich zu spüren.",
            "Der Temperaturtrend ist eindeutig: Es wird wärmer, Grad für Grad.",
            "Tag für Tag klettern die Temperaturen. Die Kälte verliert langsam an Boden.",
            "Die Wochenvorhersage liest sich wie eine Wärmetreppe: {temp_change}°C Anstieg bis zum Ende.",
            "Die Luft wird milder. Bis zum Wochenende wirst du den Unterschied merken.",
            "Die Temperaturen steigen diese Woche stetig an – ein klarer Trend.",
            "Der Erwärmungstrend ist in der Vorhersage deutlich erkennbar. Die Jahreszeit wendet sich.",
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
            "Die kommende Woche bringt eine Abkühlung um {temp_change}°C. Zeit, sich darauf einzustellen.",
            "Jeden Tag sinken die Temperaturen ein Stück weiter. Die Jahreszeit schaltet einen Gang runter.",
            "Das Thermometer spricht eine klare Sprache: Kühlere Verhältnisse ziehen auf.",
            "Kühlere Tage stehen bevor – bis zum Wochenende wird es {temp_change}°C frischer.",
            "Die Luft wird merklich frischer. Bis zum Wochenende lohnt sich eine zusätzliche Schicht.",
            "Der Wochentrend zeigt nach unten. Zieh dich entsprechend an.",
            "Die Abkühlung kommt langsam, aber stetig – das zeigt die Vorhersage deutlich.",
            "Die Temperaturen sinken kontinuierlich über die nächsten Tage.",
        ],
    },
    
    "light_fighter": {
        "en": [
            "The clouds are grey, but behind them the sun just got {delta_min} minutes stronger. The light is gaining even when you can't see it.",
            "Grey skies, but here's the reality: you have {delta_min} more minutes of daylight than yesterday. Progress continues regardless of clouds.",
            "Don't let the overcast fool you. The light gained {delta_min} minutes since yesterday—the trend doesn't stop for weather.",
            "The clouds block the view but not the progress: +{delta_min} minutes of daylight today compared to yesterday.",
            "It looks grey out there, but the data shows {delta_min} more minutes of light. The days are lengthening regardless.",
            "Grey today, but the light doesn't stop for clouds. It added {delta_min} minutes anyway.",
            "Behind all that grey, the daylight increased by {delta_min} minutes. The clock keeps moving in your favor.",
            "Overcast skies can't change the astronomy: the day stretched {delta_min} minutes longer than yesterday.",
            "Clouds are temporary. The {delta_min} minutes you gained today are permanent progress.",
            "The sky forgot to be sunny, but it didn't forget to be longer. +{delta_min} minutes.",
        ],
        "de": [
            "Die Wolken sind grau, aber dahinter hat die Sonne gerade {delta_min} Minuten dazugewonnen. Das Licht wächst, auch wenn du es nicht siehst.",
            "Grauer Himmel, aber Fakt ist: Du hast bereits {delta_min} Minuten mehr Tageslicht als gestern. Dieser Trend geht weiter, trotz der Wolken.",
            "Lass dich vom Grau nicht täuschen. Das Tageslicht hat seit gestern {delta_min} Minuten zugelegt – der Trend pausiert nicht fürs Wetter.",
            "Die Wolken versperren die Sicht, aber nicht den Fortschritt: +{delta_min} Minuten Tageslicht im Vergleich zu gestern.",
            "Draußen sieht es grau aus, aber die Zahlen sprechen eine andere Sprache: {delta_min} Minuten mehr Licht. Die Tage werden trotzdem länger.",
            "Heute grau, aber das Licht macht keine Pause für Wolken. Es sind trotzdem {delta_min} Minuten dazugekommen.",
            "Hinter all dem Grau ist das Tageslicht um {delta_min} Minuten gewachsen. Die Uhr tickt zu deinen Gunsten.",
            "Wolken können die Astronomie nicht ändern: Der Tag war {delta_min} Minuten länger als gestern.",
            "Wolken sind vergänglich. Die {delta_min} Minuten, die du heute gewonnen hast, bleiben dauerhaft.",
            "Der Himmel hat vergessen sonnig zu sein, aber nicht länger hell zu bleiben. +{delta_min} Minuten.",
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
            "Du bist am Zenit des Lichtzyklus. Dies sind die längsten Tage des Jahres – {day_length} von Sonnenaufgang bis Sonnenuntergang.",
            "Das Maximum an Tageslicht ist erreicht. Die Abende dehnen sich so weit wie nur möglich.",
            "Maximales Tageslicht: {day_length}. Großzügiger mit Licht wird das Jahr nicht mehr.",
            "Das sind die Gipfeltage – {day_length} Licht am Stück. Mehr geht nicht.",
            "Du hast das Jahresmaximum an Helligkeit erreicht. {day_length} Tageslicht heute.",
            "Tageslicht-Maximum erreicht: {day_length}. Darauf haben wir den ganzen Winter gewartet.",
            "Die Sonne hat ihren Höchststand erreicht: {day_length}. Mehr Licht gibt das Jahr nicht her.",
            "Spitzenzeiten: {day_length}. Das absolute Maximum im Kalender.",
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
            "Die Kälte ist real, aber auch das: Seit der Sonnenwende hast du bereits {hours_gained} gewonnen. Die Wende läuft.",
            "Der Winter hat uns fest im Griff, aber die Zahlen zeigen: {hours_gained} mehr Tageslicht als im Dezember-Tief.",
            "Kalt und dunkel, aber du bist schon {hours_gained} weiter als zur Sonnenwende. Der Aufstieg hat definitiv begonnen.",
            "Der Januar verlangt Geduld und liefert Fortschritt: {hours_gained} mehr Licht als am dunkelsten Tag des Jahres.",
            "Das Wetter sagt Winter, aber das Tageslicht sagt Erholung: +{hours_gained} seit dem Wendepunkt.",
            "Die Sonnenwende war der Tiefpunkt. Seitdem bist du {hours_gained} geklettert, auch wenn es sich noch nicht spektakulär anfühlt.",
            "Der Winter ist offensichtlich, das zurückkehrende Licht noch subtil. Aber du bist bereits {hours_gained} voraus.",
            "Die harte Phase geht weiter, aber auch der Gewinn: {hours_gained} Fortschritt seit Dezember.",
        ],
    },
    
    "good_streak": {
        "en": [
            "Clear skies today, tomorrow, and beyond—{streak_days} days of good weather ahead. The forecast is cooperating.",
            "This is a genuine stretch of good weather. {streak_days} days of decent conditions ahead.",
            "The forecast shows {streak_days} consecutive good days. That's worth planning around.",
            "A proper run of good weather: {streak_days} days. Streaks like this deserve action.",
            "Day after day of good conditions ahead. {streak_days} days of cooperative weather.",
            "The forecast is consistent: good, good, good. {streak_days} days to work with.",
        ],
        "de": [
            "Klarer Himmel heute, morgen und übermorgen – {streak_days} Tage Schönwetter am Stück. Die Vorhersage spielt mit.",
            "Das ist eine echte Schönwetterphase. {streak_days} Tage gute Bedingungen liegen vor dir.",
            "Die Vorhersage zeigt {streak_days} gute Tage hintereinander. Das lohnt sich einzuplanen.",
            "Eine richtige Schönwetterperiode: {streak_days} Tage. So eine Serie will genutzt werden.",
            "Tag für Tag gute Bedingungen voraus. {streak_days} Tage kooperiert das Wetter.",
            "Die Vorhersage ist eindeutig: gut, gut, gut. {streak_days} Tage zum Ausnutzen.",
        ],
    },
    
    "grey_stretch": {
        "en": [
            "The week looks grey throughout—{streak_days} days of clouds ahead. Time to embrace indoor activities.",
            "A stretch of overcast: {streak_days} days. The weather wants you to slow down.",
            "{streak_days} days of grey ahead. Good time for indoor projects.",
            "The forecast is consistent: clouds, clouds, clouds for {streak_days} days.",
            "An extended grey period. Books, projects, and indoor activities.",
            "The sky is taking a break from blue. {streak_days} days of grey ahead.",
        ],
        "de": [
            "Die ganze Woche sieht grau aus – {streak_days} Tage Wolken voraus. Zeit für Aktivitäten drinnen.",
            "Eine Grauphase: {streak_days} Tage am Stück. Das Wetter lädt zum Entschleunigen ein.",
            "{streak_days} Tage Grau voraus. Gute Zeit für Projekte in den eigenen vier Wänden.",
            "Die Vorhersage ist einheitlich: Wolken, Wolken, Wolken für {streak_days} Tage.",
            "Eine ausgedehnte Grauphase. Zeit für Bücher, Projekte und Gemütlichkeit drinnen.",
            "Der Himmel macht Pause vom Blausein. {streak_days} Tage Grau liegen vor dir.",
        ],
    },
    
    "breakthrough_day": {
        "en": [
            "Today breaks the streak. After {bad_days} days of grey, the sun finally shows up.",
            "The waiting paid off. Today is the day the weather remembered to cooperate.",
            "After {bad_days} days of grey, today delivers. The sun is out.",
            "The clouds finally moved on. Today is the breakthrough after {bad_days} grey days.",
            "This is the day the pattern broke. Sun after {bad_days} days of overcast.",
            "The grey streak ends today. After {bad_days} days, the sun returns.",
        ],
        "de": [
            "Heute bricht die Serie. Nach {bad_days} grauen Tagen zeigt sich endlich wieder die Sonne.",
            "Das Warten hat sich gelohnt. Heute erinnert sich das Wetter endlich ans Mitspielen.",
            "Nach {bad_days} Tagen Grau liefert der heutige Tag. Die Sonne ist zurück.",
            "Die Wolken sind endlich weitergezogen. Heute ist der Durchbruch nach {bad_days} grauen Tagen.",
            "Heute bricht das Muster. Sonne nach {bad_days} Tagen Bewölkung – endlich.",
            "Die Grauphase endet heute. Nach {bad_days} Tagen kehrt die Sonne zurück.",
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
            "Die Wochenendvorhersage sieht vielversprechend aus. Samstag und Sonntag bieten beide gute Bedingungen für Pläne draußen.",
            "Gute Nachrichten fürs Wochenende: Klarer Himmel an beiden Tagen. Zeit, etwas draußen zu unternehmen.",
            "Die Vorhersage hat das gute Wetter fürs Wochenende aufgespart. Samstag und Sonntag sehen beide gut aus.",
            "Dein Wochenende sieht brauchbar aus. Outdoor-Pläne sind definitiv eine gute Idee.",
            "Samstag und Sonntag zeigen sich beide von ihrer guten Seite. Perfektes Timing für Aktivitäten draußen.",
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
            "Das Wochenende wird nass. Pläne für drinnen sind vermutlich die klügere Wahl.",
            "Regen am Samstag, noch mehr am Sonntag. Ein klassisches Indoor-Wochenende.",
            "Die Vorhersage deutet auf ein gemütliches Wochenende hin – Wolken und Regen durchgehend.",
            "Das Wochenendwetter spielt nicht mit. Zeit für Alternativen drinnen.",
            "Grauer Himmel am Samstag und Sonntag. Die Woche endet ruhig daheim.",
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
            "Das Wetter ist ruhig und unauffällig – umso mehr rückt das Licht in den Fokus: {day_length} Tageslicht heute.",
            "Nichts Dramatisches in der Vorhersage. Nur der stille Fortschritt von {delta_min} Minuten mehr pro Tag.",
            "Stabile Verhältnisse bedeuten: Die eigentliche Story ist das Tageslicht – {day_length} und im stetigen Wandel.",
            "Das Wetter ist Nebensache. Das Licht – {day_length} – ist die eigentliche Nachricht.",
            "Unauffälliger Himmel, aber das gibt Raum zu bemerken: Du hast heute {day_length} Tageslicht.",
        ],
    },
    
    "spring_acceleration": {
        "en": [
            "This is the fast phase. The light is gaining {delta_min} minutes daily—the steepest climb of the year.",
            "The daylight is increasing quickly now: +{delta_min} minutes per day. You can see the evenings stretching.",
            "The acceleration is measurable. {delta_min} minutes daily means visible change week to week.",
            "This is when waiting turns to momentum. +{delta_min} minutes each day adds up fast.",
            "The daylight gains are at their maximum now: {delta_min} minutes daily.",
        ],
        "de": [
            "Das ist die schnelle Phase. Das Licht gewinnt täglich {delta_min} Minuten dazu – der steilste Anstieg des Jahres.",
            "Das Tageslicht nimmt jetzt rasant zu: +{delta_min} Minuten pro Tag. Man sieht förmlich, wie sich die Abende dehnen.",
            "Die Beschleunigung ist messbar. {delta_min} Minuten täglich bedeuten sichtbare Veränderung von Woche zu Woche.",
            "Jetzt wird aus Warten echter Schwung. +{delta_min} Minuten jeden Tag summieren sich rasant.",
            "Die Tageslichtgewinne sind jetzt am Maximum: {delta_min} Minuten täglich.",
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
            "Die Sonnenwende ist nur noch {days_to_solstice} Tage entfernt. Du bist im Endanflug auf den Wendepunkt des Jahres.",
            "Nur noch {days_to_solstice} Tage bis zur Sonnenwende. Das Licht nähert sich seinem {peak_or_min}.",
            "Die Sonnenwende naht: noch {days_to_solstice} Tage. Das Jahr steht kurz vor der Wende.",
            "Wir sind im Sonnenwende-Territorium – nur noch {days_to_solstice} Tage bis zum astronomischen Meilenstein.",
            "Der Countdown läuft: {days_to_solstice} Tage bis zur Jahreswende des Lichts.",
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
            "So funktioniert der Januar: Draußen kalt, aber das Lichtkonto wächst bereits.",
            "Der tiefe Winter hat sich eingenistet, aber die Sonnenwende liegt hinter uns – die Tage werden wieder länger.",
            "Die kältesten Wochen fallen mit dem Beginn der Lichterholung zusammen. Die Wende ist längst passiert.",
            "Januars Wetter passt nicht zu seiner Astronomie: Die härteste Kälte kommt, obwohl das Licht schon auf dem Rückweg ist.",
            "Winter auf dem Kältegipfel, aber astronomisch liegt der Tiefpunkt bereits hinter uns.",
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
            "Der Spätwinter zeigt jetzt echtes Momentum – die Tageslichtgewinne beschleunigen merklich.",
            "Die Energie des Februars kommt davon, dass der Wandel so nah und sichtbar ist.",
            "Das ist die Sprintphase: Tageslichtgewinne beschleunigen sich Richtung Tagundnachtgleiche.",
            "Der Spätwinter liefert Beweise. Das Licht zeigt unmissverständlich: Die Veränderung kommt.",
            "Der Schub Richtung Frühling ist jetzt unübersehbar. Das Licht legt ordentlich zu.",
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
            "Die Tagundnachtgleiche liegt hinter dir. Die Tage sind jetzt länger als die Nächte – das Gleichgewicht hat sich verschoben.",
            "Früher Frühling ist das Ausatmen nach dem Winter. Von hier an gewinnt das Licht.",
            "Du bist jetzt in der hellen Jahreshälfte angekommen. So will es die Astronomie.",
            "Der Frühling ist offiziell da. Das Licht beweist, was das Wetter manchmal noch leugnet.",
            "Die Tagundnachtgleiche markierte die Wende. Du bist jetzt auf der großzügigen Seite des Kalenders.",
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
            "Der späte Frühling ist der Anflug auf das Lichtmaximum. Die längsten Tage sind nah.",
            "Du kletterst Richtung Gipfel. Das maximale Licht ist nur noch Wochen entfernt.",
            "Der späte Frühling bietet einige der besten Lichtverhältnisse des ganzen Jahres.",
            "Der Aufstieg zur Sommersonnenwende geht weiter. Jeder Tag bringt ein Stück mehr.",
            "Das ist die Phase, in der Licht im Überfluss vorhanden ist. Der Gipfel ist nah.",
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
            "Du bist ganz oben angekommen. Längere Tage bietet das Jahr nicht.",
            "Hochsommer ist der Gipfel. Von hier an geht es nur noch sanft bergab.",
            "Die längsten Tage des Jahres sind jetzt. Dafür war der ganze Aufstieg.",
            "Sonnenwende-Territorium: maximales Licht, maximaler Abend.",
            "Du stehst auf dem Gipfel des Lichtzyklus.",
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
            "Der Spätsommer ist der langsame Abstieg. Noch hell, aber der Gipfel liegt hinter dir.",
            "Die Tage sind merklich kürzer als zur Sonnenwende, aber immer noch großzügig bemessen.",
            "Spätsommer ist Fülle mit Bewusstsein. Das Licht geht langsam zurück.",
            "Der Gipfel liegt hinter dir, aber der Abstieg ist sanft. Der Sommer verweilt noch.",
            "Der Rückzug vom Lichtmaximum ist im Gange, aber gemächlich.",
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
            "Die Tagundnachtgleiche signalisiert den Wechsel. Die Nächte sind jetzt länger als die Tage.",
            "Früher Herbst ist das Spiegelbild des frühen Frühlings – steiler Wandel, entgegengesetzte Richtung.",
            "Du hast die dunkle Jahreshälfte betreten. Die Nächte gewinnen jetzt.",
            "Der Abstieg beschleunigt sich im Herbst. Jede Woche ist spürbar kürzer.",
            "Im frühen Herbst wird der Verlust offensichtlich. Der Sonnenuntergang kommt jeden Tag früher.",
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
            "Spätherbst ist der Endanflug auf das Jahresminimum. Die Sonnenwende ist nah.",
            "Du steigst zum Tiefpunkt ab, aber der Wendepunkt ist bereits in Sichtweite.",
            "Spätherbst ist die letzte Etappe der Dunkelheit vor der Wende.",
            "Die kürzesten Tage nähern sich. Spätherbst ist das Tal vor dem nächsten Aufstieg.",
            "Der November bringt dich nah ans Minimum. Die Sonnenwende wartet schon.",
        ],
    },
}


# ===== NATURE SIGNS BY MONTH =====
# Simplified structure with language support
NATURE_SIGNS = {
    1: {
        "en": [
            "On clear winter days, watch for robins—they're more visible now and singing from exposed perches.",
            "If you have a bird feeder, clear cold days bring the most visitors.",
            "Hazel catkins are worth watching. When they lengthen and turn yellow, spring is loading.",
            "Days are now gaining light at an accelerating rate.",
            "Winter rain brings earthworms to the surface. That's why blackbirds patrol lawns.",
        ],
        "de": [
            "An klaren Wintertagen lohnt es sich, nach Rotkehlchen Ausschau zu halten – sie sind jetzt gut sichtbar und singen von exponierten Plätzen.",
            "Falls du ein Vogelhäuschen hast: Klare, kalte Tage bringen die meisten Besucher.",
            "Haselkätzchen sind jetzt interessant zu beobachten. Wenn sie länger und gelb werden, lädt der Frühling.",
            "Die Tage gewinnen jetzt Licht mit zunehmender Geschwindigkeit.",
            "Winterregen bringt Regenwürmer an die Oberfläche – deshalb patrouillieren Amseln über den Rasen.",
        ],
    },
    2: {
        "en": [
            "Snowdrops are fully out now. They're the reliable first flower—check churchyards and old gardens.",
            "On sunny February days, watch for bumblebee queens searching for nest sites.",
            "Birdsong intensifies in February. Great tits and robins are getting louder.",
            "Trees are visibly preparing. Buds are swelling on everything.",
            "February feels like waiting, but the activity underneath is intense. Life is loading.",
        ],
        "de": [
            "Schneeglöckchen blühen jetzt in voller Pracht. Sie sind die verlässlichen Erstlinge – schau auf Friedhöfen und in alten Gärten.",
            "An sonnigen Februartagen kannst du Hummelköniginnen beobachten, die Nistplätze suchen.",
            "Der Vogelgesang wird im Februar lauter. Kohlmeisen und Rotkehlchen drehen auf.",
            "Die Bäume bereiten sich sichtbar vor. Überall schwellen die Knospen.",
            "Februar fühlt sich an wie Warten, aber unter der Oberfläche herrscht intensive Aktivität. Das Leben lädt.",
        ],
    },
    3: {
        "en": [
            "Daffodils are out now—wild ones in woods, cultivated ones everywhere else.",
            "The dawn chorus is significant now. Blackbirds and song thrushes sing before sunrise.",
            "Wild garlic starts to appear in woodlands. You smell it before you see it.",
            "March is the month of visible acceleration. Everything happens at once.",
            "The equinox means days longer than nights from here. The dark half is over.",
        ],
        "de": [
            "Narzissen blühen jetzt – wilde in Wäldern, kultivierte überall sonst.",
            "Das morgendliche Vogelkonzert ist jetzt richtig laut. Amseln und Singdrosseln singen vor Sonnenaufgang.",
            "Bärlauch taucht in Wäldern auf. Man riecht ihn, bevor man ihn sieht.",
            "März ist der Monat der sichtbaren Beschleunigung. Alles passiert gleichzeitig.",
            "Die Tagundnachtgleiche bedeutet: Ab jetzt sind die Tage länger als die Nächte. Die dunkle Hälfte ist vorbei.",
        ],
    },
    4: {
        "en": [
            "April sun on cherry blossom is one of the best sights of the year.",
            "The dawn chorus is intense now. Get up early—the singing starts before 5 AM.",
            "Butterflies are everywhere now: orange tips, peacocks, small whites.",
            "The smell of blossom is pervasive. Apple, cherry, hawthorn.",
            "The warmth is becoming reliable now. April evenings are mild.",
        ],
        "de": [
            "Aprilsonne auf Kirschblüten – einer der schönsten Anblicke des Jahres.",
            "Das Morgenkonzert ist jetzt auf dem Höhepunkt. Früh aufstehen lohnt sich – der Gesang beginnt vor 5 Uhr.",
            "Schmetterlinge sind jetzt überall unterwegs: Aurorafalter, Tagpfauenaugen, Kleine Kohlweißlinge.",
            "Blütenduft liegt überall in der Luft. Apfel, Kirsche, Weißdorn.",
            "Die Wärme wird jetzt verlässlich. Aprilabende sind mild.",
        ],
    },
    5: {
        "en": [
            "May warmth brings butterflies in clouds. Painted ladies, commas, and whites.",
            "Swifts are fully present now, screaming through evening skies.",
            "Clear May evenings are long and warm. Sunset comes after 9 PM now.",
            "May is the month of abundance. Everything is growing, flowering, or nesting.",
            "May brings the sense that summer is actually here, not just coming.",
        ],
        "de": [
            "Die Maiwärme bringt Schmetterlinge in Scharen. Distelfalter, C-Falter und Weißlinge.",
            "Mauersegler sind jetzt voll präsent und kreischen durch den Abendhimmel.",
            "Klare Maiabende sind lang und warm. Sonnenuntergang ist jetzt erst nach 21 Uhr.",
            "Mai ist der Monat der Fülle. Alles wächst, blüht oder brütet.",
            "Im Mai hat man endlich das Gefühl, dass der Sommer wirklich da ist – nicht nur auf dem Weg.",
        ],
    },
    6: {
        "en": [
            "The summer solstice approaches—these are nearly the longest days of the year.",
            "June evenings are the longest. Sunset after 9:30 PM gives hours of usable light.",
            "Swifts are everywhere, feeding hard for breeding.",
            "June is the month of maximum light. Use it.",
            "The year's peak light deserves attention. Notice how late the twilight lasts.",
        ],
        "de": [
            "Die Sommersonnenwende nähert sich – das sind fast die längsten Tage des Jahres.",
            "Juniabende sind die längsten. Sonnenuntergang nach 21:30 Uhr gibt stundenlang nutzbares Licht.",
            "Mauersegler sind überall unterwegs und füttern eifrig für die Brut.",
            "Juni ist der Monat des maximalen Lichts. Nutze ihn.",
            "Das Spitzenlicht des Jahres verdient Aufmerksamkeit. Beachte, wie spät die Dämmerung dauert.",
        ],
    },
    7: {
        "en": [
            "Lavender and buddleia are butterfly magnets. Watch for peacocks and red admirals.",
            "Clear July evenings are warm enough to sit out until 10 PM.",
            "July is the month when summer feels fully arrived. The heat is real.",
            "The days are shortening, but imperceptibly. You won't notice yet.",
            "July warmth lingers into evening. Sitting outside is comfortable until dark.",
        ],
        "de": [
            "Lavendel und Sommerflieder ziehen Schmetterlinge magnetisch an. Achte auf Tagpfauenaugen und Admirale.",
            "Klare Juliabende sind warm genug, um bis 22 Uhr draußen zu sitzen.",
            "Im Juli fühlt sich der Sommer endgültig angekommen an. Die Hitze ist echt.",
            "Die Tage werden kürzer, aber unmerklich. Du wirst es noch nicht bemerken.",
            "Die Juliwärme hält bis in den Abend. Draußen sitzen ist bequem, bis es dunkel wird.",
        ],
    },
    8: {
        "en": [
            "Blackberries are fully ripe now. The picking season is at its peak.",
            "Clear August days have a golden quality. The light is aging toward autumn.",
            "August is the harvest month. The work of the year comes to fruition.",
            "Days are noticeably shorter than July. The change is measurable now.",
            "August has a melancholy edge. The abundance is real, but temporary.",
        ],
        "de": [
            "Brombeeren sind jetzt voll reif. Die Erntezeit ist auf dem Höhepunkt.",
            "Klare Augusttage haben eine goldene Qualität. Das Licht altert Richtung Herbst.",
            "August ist der Erntemonat. Die Arbeit des Jahres trägt Früchte.",
            "Die Tage sind spürbar kürzer als im Juli. Die Veränderung ist jetzt messbar.",
            "August hat einen melancholischen Beigeschmack. Die Fülle ist echt, aber vergänglich.",
        ],
    },
    9: {
        "en": [
            "September sun on turning leaves is the start of the color show.",
            "Clear September days are harvest days. Apples, pears, plums are ready.",
            "September is the transition month. Summer ends, autumn begins.",
            "The equinox means nights now exceed days. The dark half starts.",
            "Days shorten rapidly now. The rate of change matches spring in reverse.",
        ],
        "de": [
            "Septembersonne auf sich verfärbenden Blättern – der Beginn der Farbshow.",
            "Klare Septembertage sind Erntetage. Äpfel, Birnen, Pflaumen sind bereit.",
            "September ist der Übergangsmonat. Der Sommer endet, der Herbst beginnt.",
            "Ab der Tagundnachtgleiche sind die Nächte länger als die Tage. Die dunkle Hälfte beginnt.",
            "Die Tage verkürzen sich jetzt schnell. Das Tempo entspricht dem Frühling – nur umgekehrt.",
        ],
    },
    10: {
        "en": [
            "October sun on peak autumn color is one of the year's great sights.",
            "Clear October days are cold but beautiful. The light is precious.",
            "October is the main month for autumn color.",
            "Clocks change at month's end—evenings suddenly darker.",
            "Days shorten rapidly. The change is visible week to week.",
        ],
        "de": [
            "Oktobersonne auf Herbstfarben in voller Pracht – einer der großen Anblicke des Jahres.",
            "Klare Oktobertage sind kalt, aber wunderschön. Das Licht ist kostbar.",
            "Oktober ist der Hauptmonat für Herbstfarben.",
            "Zeitumstellung am Monatsende – die Abende werden schlagartig dunkler.",
            "Die Tage werden schnell kürzer. Die Veränderung ist von Woche zu Woche spürbar.",
        ],
    },
    11: {
        "en": [
            "November sun is precious. The bare trees don't block it, at least.",
            "Clear November days are cold but bright. The light is rationed.",
            "November is the month of bare trees and short days.",
            "Days are short and getting shorter. The solstice is next month.",
            "Grey November is the archetype. This is what the month often delivers.",
        ],
        "de": [
            "Novembersonne ist kostbar. Die kahlen Bäume blockieren sie wenigstens nicht.",
            "Klare Novembertage sind kalt, aber hell. Das Licht ist rationiert.",
            "November ist der Monat der kahlen Bäume und kurzen Tage.",
            "Die Tage sind kurz und werden noch kürzer. Die Sonnenwende ist nächsten Monat.",
            "Grauer November ist der Klassiker. So präsentiert sich dieser Monat oft.",
        ],
    },
    12: {
        "en": [
            "December sun is scarce but valuable. Every minute of direct light counts.",
            "The solstice approaches—the shortest day, the turning point.",
            "December sun stays low all day. A constant golden-hour quality.",
            "After the solstice, days lengthen. The psychological boost is real.",
            "December is the bottom of the light cycle. The only way is up.",
        ],
        "de": [
            "Dezembersonne ist rar, aber wertvoll. Jede Minute direktes Licht zählt.",
            "Die Sonnenwende naht – der kürzeste Tag, der Wendepunkt.",
            "Die Dezembersonne bleibt den ganzen Tag tief. Eine permanente Goldene-Stunde-Stimmung.",
            "Nach der Sonnenwende werden die Tage länger. Der psychologische Schub ist echt.",
            "Dezember ist der Tiefpunkt des Lichtzyklus. Ab hier geht es nur noch aufwärts.",
        ],
    },
}


# ===== GENERAL NATURE FACTS =====
NATURE_FACTS_GENERAL = {
    "en": [
        "Bird feeders see more activity on cold days. The energy demand increases.",
        "Robins sing year-round. One of the few birds that holds winter territory.",
        "The smell of the season is as diagnostic as the temperature.",
        "Morning mist burns off when temperatures rise. Watch the process happen.",
        "Seasons are caused by Earth's tilt, not its distance from the sun.",
    ],
    "de": [
        "An kalten Tagen herrscht mehr Betrieb am Vogelhäuschen. Der Energiebedarf steigt.",
        "Rotkehlchen singen das ganze Jahr über. Sie sind einer der wenigen Vögel mit Winterrevier.",
        "Der Geruch der Jahreszeit ist genauso aufschlussreich wie die Temperatur.",
        "Morgennebel löst sich auf, wenn die Temperaturen steigen. Faszinierend zu beobachten.",
        "Jahreszeiten entstehen durch die Neigung der Erdachse, nicht durch den Abstand zur Sonne.",
    ],
}


# ===== CLOSINGS =====
CLOSINGS = {
    "practical": {
        "en": ["Plan accordingly.", "Adjust as needed.", "Good to know for planning."],
        "de": ["Entsprechend planen.", "Bei Bedarf anpassen.", "Gut zu wissen fürs Planen."],
    },
    "observational": {
        "en": ["Worth paying attention to.", "Something to notice.", "The details matter."],
        "de": ["Lohnt, darauf zu achten.", "Etwas zum Beobachten.", "Die Details machen's."],
    },
    "simple": {
        "en": ["That's the picture.", "Those are the facts.", "There it is."],
        "de": ["So sieht's aus.", "Das sind die Fakten.", "So ist es."],
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
        "Der Tag umfasst {day_length} – Sonnenaufgang um {sunrise}, Sonnenuntergang um {sunset}.",
        "Tageslicht heute: {day_length}. Die Sonne scheint von {sunrise} bis {sunset}.",
        "Dir stehen heute {day_length} Licht zur Verfügung, von {sunrise} bis {sunset}.",
    ],
}


# ===== DELTA PHRASES =====
DELTA_PHRASES = {
    "gaining": {
        "en": [
            "That's {delta} minutes more than yesterday.",
            "You gained {delta} minutes compared to yesterday.",
            "+{delta} minutes versus yesterday.",
        ],
        "de": [
            "Das sind {delta} Minuten mehr als gestern.",
            "{delta} Minuten mehr im Vergleich zu gestern.",
            "+{delta} Minuten gegenüber gestern.",
        ],
    },
    "losing": {
        "en": [
            "That's {delta} minutes less than yesterday.",
            "You lost {delta} minutes compared to yesterday.",
            "{delta} minutes shorter than yesterday.",
        ],
        "de": [
            "Das sind {delta} Minuten weniger als gestern.",
            "{delta} Minuten weniger im Vergleich zu gestern.",
            "{delta} Minuten kürzer als gestern.",
        ],
    },
}
