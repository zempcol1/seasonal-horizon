"""
Text library for Seasonal Horizon, in English and German.

A message is a lead plus a companion line. The lead comes from SIGNALS (one
pool per signal in uplift_engine) or, when nothing stands out, from PHASES.
The companion comes from SPRING_SIGNS, NATURE_SIGNS or SUN_ENJOYMENT.

Each signal pool may only use the placeholders its signal provides; the
tests check this. Shrinking daylight has no pool on purpose.
"""

WEEKDAYS = {
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
           "Saturday", "Sunday"],
    "de": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag",
           "Samstag", "Sonntag"],
}


# ===== Phases of the year =====
#
# The fallback lead, used when no signal is stronger. No figures, so they
# hold on any day of their phase.

PHASES = {
    "darkening": {
        "en": [
            "This is the quiet end of the year. Candles, warm kitchens, early evenings - it has its own kind of comfort.",
            "November light is low and golden when it comes. It makes even ordinary streets look painted.",
            "The year is slowing down, and it is fine to slow down with it.",
            "Dark evenings are made for the things summer never leaves room for: long dinners, books, a proper conversation.",
            "Bare trees let more of the low sun through than you would expect. The light is scarce now, so it shows.",
            "The shortest days are not far off, and the turn comes with them.",
        ],
        "de": [
            "Das ist das stille Ende des Jahres. Kerzen, warme Küchen, frühe Abende - das hat seinen eigenen Trost.",
            "Das Novemberlicht steht tief und golden, wenn es kommt. Selbst gewöhnliche Straßen sehen dann aus wie gemalt.",
            "Das Jahr wird langsamer, und es ist in Ordnung, mit ihm langsamer zu werden.",
            "Dunkle Abende sind gemacht für das, wofür der Sommer nie Platz lässt: lange Essen, Bücher, ein richtiges Gespräch.",
            "Kahle Bäume lassen mehr von der tiefen Sonne durch, als man denkt. Das Licht ist knapp, darum fällt es auf.",
            "Die kürzesten Tage sind nicht mehr weit, und mit ihnen kommt die Wende.",
        ],
    },
    "returning_light": {
        "en": [
            "The cold is still doing its thing, but the light has already changed its mind.",
            "Winter is loud right now and the light is quiet about it. The light is the one that wins.",
            "Nothing about today needs to feel like spring for spring to be on its way.",
            "This is the part of the year that asks for patience. It has never failed to pay it back.",
            "The hardest stretch of the year is also the one that is already improving.",
            "Somewhere under all this, the ground is keeping time. It knows what comes next.",
            "The year has turned. Everything from here is a slow argument in favour of the light.",
            "It is still dark early, and it is already less dark than it was.",
            "Grey days are easier to sit with when the light behind them is lengthening.",
            "You are on the returning side of the year now. That is worth knowing on a morning like this.",
        ],
        "de": [
            "Die Kälte macht noch ihr Ding, aber das Licht hat es sich bereits anders überlegt.",
            "Der Winter ist gerade laut und das Licht ist still dabei. Gewinnen wird das Licht.",
            "Nichts an heute muss sich nach Frühling anfühlen, damit der Frühling unterwegs ist.",
            "Das ist der Teil des Jahres, der Geduld verlangt. Zurückgezahlt hat er sie noch immer.",
            "Der härteste Abschnitt des Jahres ist zugleich der, der sich schon bessert.",
            "Irgendwo unter alldem hält der Boden die Zeit. Er weiß, was als Nächstes kommt.",
            "Das Jahr hat gewendet. Alles ab hier ist ein langsames Argument für das Licht.",
            "Es wird noch früh dunkel, und es ist schon weniger dunkel als es war.",
            "Graue Tage lassen sich leichter aushalten, wenn das Licht dahinter länger wird.",
            "Du bist jetzt auf der zurückkehrenden Seite des Jahres. Das ist an so einem Morgen etwas wert.",
        ],
    },
    "spring": {
        "en": [
            "The bright half of the year has begun. Days now outlast nights.",
            "Spring is the exhale after winter. Everything that waited is moving again.",
            "The evenings are long enough again to do something with them.",
            "This is the season of first times: the first meal outside, the first bare arms, the first swifts.",
            "Green arrives fast now. Look closely at a hedge and it is different from last week.",
            "The light is generous now, and it is still growing.",
        ],
        "de": [
            "Die helle Jahreshälfte hat begonnen. Die Tage sind jetzt länger als die Nächte.",
            "Der Frühling ist das Ausatmen nach dem Winter. Alles, was gewartet hat, bewegt sich wieder.",
            "Die Abende sind wieder lang genug, um etwas mit ihnen anzufangen.",
            "Das ist die Zeit der ersten Male: das erste Essen draußen, die ersten nackten Arme, die ersten Mauersegler.",
            "Das Grün kommt jetzt schnell. Schau eine Hecke genau an - sie ist anders als letzte Woche.",
            "Das Licht ist jetzt großzügig, und es wächst noch.",
        ],
    },
    "summer": {
        "en": [
            "These are the long days. Evenings that go on long enough to forget the time.",
            "Summer is the season of being outside without planning it.",
            "Warm evenings, late light, nowhere to be. This is what the winter was waiting for.",
            "The light is at its most generous now. There is enough of it to waste some.",
            "Summer evenings turn golden in their last hour. It is the best hour of the day.",
            "Fruit is ripening, the water is warm, and the evenings belong to you.",
        ],
        "de": [
            "Das sind die langen Tage. Abende, die lang genug dauern, um die Zeit zu vergessen.",
            "Der Sommer ist die Jahreszeit, in der man draußen ist, ohne es zu planen.",
            "Warme Abende, spätes Licht, nirgendwo hinmüssen. Darauf hat der Winter gewartet.",
            "Das Licht ist jetzt am großzügigsten. Es ist genug da, um etwas davon zu verschwenden.",
            "Sommerabende werden in ihrer letzten Stunde golden. Es ist die schönste Stunde des Tages.",
            "Das Obst reift, das Wasser ist warm, und die Abende gehören dir.",
        ],
    },
    "autumn": {
        "en": [
            "Autumn light is low and warm. It makes everything look like a photograph.",
            "This is harvest time - apples, pears, grapes, the first chestnuts.",
            "The colours are turning. For a few weeks the woods are the brightest thing around.",
            "Crisp mornings and soft afternoons. Autumn does both on the same day.",
            "Clear autumn days have a sharpness summer never manages. Far hills look close enough to touch.",
            "It is the season for long walks and a warm kitchen to come back to.",
        ],
        "de": [
            "Das Herbstlicht steht tief und warm. Alles sieht darin aus wie ein Foto.",
            "Es ist Erntezeit - Äpfel, Birnen, Trauben, die ersten Marroni.",
            "Die Farben kippen. Für ein paar Wochen sind die Wälder das Hellste weit und breit.",
            "Frische Morgen und milde Nachmittage. Der Herbst kann beides am selben Tag.",
            "Klare Herbsttage haben eine Schärfe, die der Sommer nie schafft. Ferne Hügel wirken zum Greifen nah.",
            "Es ist die Zeit für lange Spaziergänge und eine warme Küche zum Heimkommen.",
        ],
    },
}


# ===== Signals =====
#
# One pool per signal, keyed like the signal. The placeholders each pool may
# use are listed above it.

SIGNALS = {
    # -- light ----------------------------------------------------------------

    # (none)
    "turning_day": {
        "en": [
            "Today is the shortest day of the year. From tomorrow, every day is a little longer than the one before.",
            "The solstice is today. This is the bottom of the curve - from here it only goes one way.",
            "Shortest day today. The darkness has reached as far as it goes, and tonight it turns.",
        ],
        "de": [
            "Heute ist der kürzeste Tag des Jahres. Ab morgen ist jeder Tag ein wenig länger als der davor.",
            "Heute ist Sonnenwende. Das ist der Tiefpunkt der Kurve - ab hier geht es nur noch in eine Richtung.",
            "Kürzester Tag heute. Weiter reicht die Dunkelheit nicht, und heute Nacht dreht sie.",
        ],
    },

    # {days_to_solstice} {days} {days_dat}
    "solstice_countdown": {
        "en": [
            "{days_to_solstice} {days} to the solstice. After that, the light starts coming back.",
            "The turn is close: in {days_to_solstice} {days_dat} the days stop getting shorter.",
            "Only {days_to_solstice} {days} until the shortest day. Everything after it is a gain.",
            "The countdown is short now: {days_to_solstice} {days} to the turn of the light.",
        ],
        "de": [
            "Noch {days_to_solstice} {days} bis zur Sonnenwende. Danach kommt das Licht zurück.",
            "Die Wende ist nah: In {days_to_solstice} {days_dat} hören die Tage auf, kürzer zu werden.",
            "Nur noch {days_to_solstice} {days} bis zum kürzesten Tag. Alles danach ist Gewinn.",
            "Der Countdown ist kurz: noch {days_to_solstice} {days} bis zur Wende des Lichts.",
        ],
    },

    # {sunset}
    "evenings_turned": {
        "en": [
            "The sun set a few seconds later today than yesterday. The evenings have turned before the solstice even arrives.",
            "A quiet one: sunsets are already getting later again. {sunset} today, and later from here on.",
            "The earliest sunset of the year is behind you. The evenings start growing now, ahead of the solstice.",
        ],
        "de": [
            "Die Sonne ist heute ein paar Sekunden später untergegangen als gestern. Die Abende haben gedreht, noch bevor die Sonnenwende da ist.",
            "Ein leises Zeichen: Die Sonnenuntergänge werden schon wieder später. Heute um {sunset}, und ab jetzt jeden Tag etwas später.",
            "Der früheste Sonnenuntergang des Jahres liegt hinter dir. Die Abende wachsen schon, der Sonnenwende voraus.",
        ],
    },

    # {sunrise}
    "mornings_turned": {
        "en": [
            "The mornings have turned too: sunrise at {sunrise}, a little earlier each day now.",
            "Sunrise is creeping earlier again - {sunrise} today. The dark mornings are on their way out.",
            "Both ends of the day are growing now. The sun was up at {sunrise}, and tomorrow it is earlier still.",
        ],
        "de": [
            "Auch die Morgen haben gedreht: Sonnenaufgang um {sunrise}, jetzt jeden Tag etwas früher.",
            "Der Sonnenaufgang rückt wieder nach vorn - heute {sunrise}. Die dunklen Morgen sind auf dem Rückzug.",
            "Jetzt wächst der Tag an beiden Enden. Die Sonne ging um {sunrise} auf, und morgen noch etwas früher.",
        ],
    },

    # {hours_gained}
    "since_solstice": {
        "en": [
            "The light has already turned. Since the solstice the day has grown by {hours_gained}, whether or not it feels like it yet.",
            "You are {hours_gained} past the shortest day. That is not nothing, even if the mornings still argue otherwise.",
            "Quietly, without ceremony, the year has handed back {hours_gained} of daylight since the solstice.",
            "The darkest day is behind you by {hours_gained} of light. The direction of travel is settled now.",
            "Since the solstice: {hours_gained} more light. It accumulates whether you notice it or not.",
        ],
        "de": [
            "Das Licht hat schon gedreht. Seit der Sonnenwende ist der Tag um {hours_gained} gewachsen, auch wenn es sich noch nicht so anfühlt.",
            "Du bist {hours_gained} über den kürzesten Tag hinaus. Das ist nicht nichts, selbst wenn die Morgen noch dagegenhalten.",
            "Ganz ohne Aufhebens hat das Jahr seit der Sonnenwende {hours_gained} Tageslicht zurückgegeben.",
            "Der dunkelste Tag liegt {hours_gained} Licht hinter dir. Die Richtung steht inzwischen fest.",
            "Seit der Sonnenwende: {hours_gained} mehr Licht. Das sammelt sich an, ob man es bemerkt oder nicht.",
        ],
    },

    # {delta} {minutes} {day_length} {sunrise} {sunset}
    "daily_gain": {
        "en": [
            "Today is {delta} {minutes} longer than yesterday. Small, but it happens again tomorrow.",
            "Another {delta} {minutes} of light today. Small enough to miss, steady enough to count on.",
            "Sunrise {sunrise}, sunset {sunset} - {day_length} of daylight, and more of it tomorrow.",
            "{day_length} of light today, {delta} {minutes} more than yesterday.",
        ],
        "de": [
            "Heute ist {delta} {minutes} länger als gestern. Wenig, aber morgen passiert es wieder.",
            "Wieder {delta} {minutes} mehr Licht heute. Klein genug, um es zu übersehen, und stetig genug, sich darauf zu verlassen.",
            "Aufgang {sunrise}, Untergang {sunset} - {day_length} Tageslicht, und morgen etwas mehr.",
            "{day_length} Licht heute, {delta} {minutes} mehr als gestern.",
        ],
    },

    # {milestone_time} {milestone_days} {days} {days_dat} {sunset}
    "sunset_milestone": {
        "en": [
            "In {milestone_days} {days} the sun sets after {milestone_time} again. Something to look forward to on the way home.",
            "Mark it: {milestone_days} {days} from now the sunset moves past {milestone_time}. Evenings start feeling different around then.",
            "The sun currently sets at {sunset}. In {milestone_days} {days_dat} that becomes {milestone_time}, and the afternoon stretches out a little.",
            "{milestone_days} {days_dat} until sunset passes {milestone_time}. The evenings are being handed back to you.",
        ],
        "de": [
            "In {milestone_days} {days_dat} geht die Sonne wieder nach {milestone_time} unter. Etwas, worauf man sich auf dem Heimweg freuen kann.",
            "Merk dir das: In {milestone_days} {days_dat} wandert der Sonnenuntergang hinter {milestone_time}. Ab dann fühlen sich die Abende anders an.",
            "Die Sonne geht gerade um {sunset} unter. In {milestone_days} {days_dat} ist es {milestone_time}, und der Nachmittag wird spürbar länger.",
            "Noch {milestone_days} {days}, bis der Sonnenuntergang {milestone_time} überschreitet. Die Abende kommen zurück.",
        ],
    },

    # {noon_gain}
    "noon_sun": {
        "en": [
            "At midday the sun now stands {noon_gain} degrees higher than at the solstice. You can feel it on your face when it comes out.",
            "The sun climbs higher every noon - {noon_gain} degrees above its December low already. On a south-facing wall, that is real warmth.",
            "{noon_gain} degrees higher at noon than at the turn of the year. The sun is not just staying longer, it is getting stronger.",
        ],
        "de": [
            "Mittags steht die Sonne jetzt {noon_gain} Grad höher als zur Sonnenwende. Wenn sie rauskommt, spürst du das im Gesicht.",
            "Die Sonne steigt jeden Mittag höher - schon {noon_gain} Grad über ihrem Tiefstand im Dezember. An einer Südwand ist das echte Wärme.",
            "Mittags {noon_gain} Grad höher als zur Jahreswende. Die Sonne bleibt nicht nur länger, sie wird auch kräftiger.",
        ],
    },

    # {day_length} {sunset}
    "peak_light": {
        "en": [
            "{day_length} of daylight today, the sun setting at {sunset}. These are the long days the winter was saving up for.",
            "The light is near its peak: {day_length} from sunrise to sunset. Plenty to spend on a long evening.",
            "Sunset at {sunset}. There is no need to hurry anything today.",
        ],
        "de": [
            "{day_length} Tageslicht heute, Sonnenuntergang um {sunset}. Auf diese langen Tage hat der Winter hingespart.",
            "Das Licht ist nahe am Höhepunkt: {day_length} von Aufgang bis Untergang. Genug für einen langen Abend.",
            "Sonnenuntergang um {sunset}. Heute muss nichts eilen.",
        ],
    },

    # -- weather --------------------------------------------------------------

    # {sunny_day} {when} {sun_hours} {hours}
    "sun_ahead": {
        "en": [
            "Something to look forward to: {sunny_day} brings about {sun_hours} {hours} of sunshine.",
            "The sun is coming back {when}. {sunny_day} looks bright - around {sun_hours} {hours} of it.",
            "{sunny_day} has sun in the forecast, about {sun_hours} {hours}. Worth keeping a little of it free.",
            "Hold on until {sunny_day}: the forecast promises around {sun_hours} {hours} of sun.",
        ],
        "de": [
            "Etwas zum Freuen: Der {sunny_day} bringt rund {sun_hours} {hours} Sonne.",
            "Die Sonne kommt {when} zurück. Der {sunny_day} sieht hell aus - etwa {sun_hours} {hours} lang.",
            "Für {sunny_day} steht Sonne in der Vorhersage, ungefähr {sun_hours} {hours}. Lohnt sich, etwas davon freizuhalten.",
            "Bis {sunny_day} durchhalten: Die Vorhersage verspricht rund {sun_hours} {hours} Sonne.",
        ],
    },

    # {sun_hours} {hours}
    "sunny_today": {
        "en": [
            "About {sun_hours} {hours} of sunshine today. The light has the day to itself.",
            "A bright one: around {sun_hours} {hours} of sun in the forecast.",
            "The sun has the day - roughly {sun_hours} {hours} of it.",
        ],
        "de": [
            "Rund {sun_hours} {hours} Sonne heute. Das Licht hat den Tag für sich.",
            "Ein heller Tag: etwa {sun_hours} {hours} Sonne in der Vorhersage.",
            "Die Sonne hat heute das Sagen - ungefähr {sun_hours} {hours}.",
        ],
    },

    # {sun_hours} {hours}
    "some_sun": {
        "en": [
            "Even today the sun gets through for about {sun_hours} {hours}. It is still there.",
            "Not a bright day, but around {sun_hours} {hours} of sun are in it. Keep an eye out for the gaps.",
            "The sun is not gone, just busy: about {sun_hours} {hours} of it today, between the clouds.",
        ],
        "de": [
            "Selbst heute kommt die Sonne rund {sun_hours} {hours} durch. Sie ist noch da.",
            "Kein heller Tag, aber etwa {sun_hours} {hours} Sonne stecken darin. Achte auf die Lücken.",
            "Die Sonne ist nicht weg, nur beschäftigt: heute ungefähr {sun_hours} {hours}, zwischen den Wolken.",
        ],
    },

    # (none)
    "snow": {
        "en": [
            "Snow today. It turns the grey into light - everything reflects, and the world goes quiet.",
            "Fresh snow: the brightest thing winter does. Even a dull sky looks lighter over it.",
            "Snow is falling. Tracks to read, a quieter town, and a reason for a hot drink after.",
            "A snow day. The light bounces off everything, and for a while the year looks new.",
        ],
        "de": [
            "Heute Schnee. Er macht aus Grau Licht - alles reflektiert, und die Welt wird still.",
            "Frischer Schnee: das Hellste, was der Winter kann. Selbst ein trüber Himmel wirkt darüber heller.",
            "Es schneit. Spuren zum Lesen, eine leisere Stadt, und ein Grund für ein heißes Getränk danach.",
            "Ein Schneetag. Das Licht prallt von allem ab, und für eine Weile sieht das Jahr neu aus.",
        ],
    },

    # (none)
    "fog": {
        "en": [
            "Fog today. Above it - often only a few hundred metres up - the sun is usually out.",
            "Everything is soft-edged today. Fog like this often lifts by midday, or sits below clear sky on the hills.",
            "A fog day: quiet, close and calm. If you can get a little higher, there is a fair chance of sun above it.",
        ],
        "de": [
            "Heute Nebel. Darüber - oft nur ein paar hundert Meter höher - scheint meistens die Sonne.",
            "Alles hat heute weiche Kanten. Solcher Nebel löst sich oft bis Mittag auf oder liegt unter klarem Himmel auf den Hügeln.",
            "Ein Nebeltag: still, nah und windstill. Wer etwas höher kommt, hat gute Chancen auf Sonne darüber.",
        ],
    },

    # {temp_low}
    "frost_clear": {
        "en": [
            "Frost overnight, down to {temp_low}, then sun. Cold and bright is the best kind of winter day.",
            "{temp_low} this morning, and clear. The frost will sparkle while the sun is low.",
            "A frosty start at {temp_low}, with sun to follow. Crunching grass, clear air, long shadows.",
        ],
        "de": [
            "Frost in der Nacht, bis {temp_low}, dann Sonne. Kalt und hell ist die beste Sorte Wintertag.",
            "{temp_low} am Morgen, und klar. Der Reif glitzert, solange die Sonne tief steht.",
            "Ein frostiger Start mit {temp_low}, danach Sonne. Knirschendes Gras, klare Luft, lange Schatten.",
        ],
    },

    # {temp_change}
    "warming": {
        "en": [
            "The thermometer is climbing this week - about {temp_change}°C warmer by the end. The air is softening.",
            "Milder days are on the way: around {temp_change}°C more by the end of the week.",
            "This week's forecast reads like a staircase going up: {temp_change}°C of warmth ahead.",
        ],
        "de": [
            "Das Thermometer klettert diese Woche - am Ende rund {temp_change}°C wärmer. Die Luft wird milder.",
            "Mildere Tage sind unterwegs: etwa {temp_change}°C mehr bis Ende der Woche.",
            "Die Vorhersage gleicht einer Treppe nach oben: {temp_change}°C mehr Wärme liegen vor dir.",
        ],
    },

    # {streak_days} {days}
    "sunny_streak": {
        "en": [
            "{streak_days} sunny {days} in a row, starting today. A proper stretch of light.",
            "The forecast is generous: {streak_days} {days} of sunshine ahead. Something to plan around.",
            "Sun today, tomorrow and beyond - {streak_days} {days} of it. Streaks like this deserve to be used.",
        ],
        "de": [
            "{streak_days} sonnige {days} am Stück, ab heute. Eine richtige Lichtstrecke.",
            "Die Vorhersage ist großzügig: {streak_days} {days} Sonne liegen vor dir. Da lässt sich etwas planen.",
            "Sonne heute, morgen und darüber hinaus - {streak_days} {days} lang. So eine Serie will genutzt werden.",
        ],
    },

    # (none)
    "weekend_sunny": {
        "en": [
            "The weekend looks sunny, both days. Worth keeping some of it free for being outside.",
            "Saturday and Sunday both have sun in the forecast. Good timing.",
            "Something for the weekend: sunshine on both days.",
        ],
        "de": [
            "Das Wochenende sieht sonnig aus, an beiden Tagen. Lohnt sich, etwas davon fürs Draußensein freizuhalten.",
            "Samstag und Sonntag haben beide Sonne in der Vorhersage. Gutes Timing.",
            "Etwas fürs Wochenende: Sonnenschein an beiden Tagen.",
        ],
    },
}


# ===== Nature, May to December =====
#
# The companion line outside the spring run-up. January to April come from
# SPRING_SIGNS instead, which knows lowland from alpine.
NATURE_SIGNS = {
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
            "Swifts are everywhere, feeding hard. Watch their aerial shows.",
            "Roses are at their peak. Stop and smell them.",
            "Bees work late into the evening on long June days.",
        ],
        "de": [
            "Mauersegler jagen überall. Schau ihren Flugshows zu.",
            "Rosen sind auf dem Höhepunkt. Stehenbleiben und riechen.",
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
        ],
        "de": [
            "Septembersonne auf bunten Blättern – die Farbshow beginnt.",
            "Äpfel, Birnen, Pflaumen sind reif. Erntezeit.",
            "Zugvögel sammeln sich. Schau nach Schwalbenschwärmen.",
            "Pilze erscheinen nach Regen. Schau an Waldrändern.",
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
            "Winter ducks from the north gather on lakes and rivers.",
        ],
        "de": [
            "Jede Minute Dezembersonne zählt. Geh raus, wenn sie scheint.",
            "Rotkehlchen singen den ganzen Winter. Sie sichern ihr Revier.",
            "Efeu und Misteln sind das einzige Grün in kahlen Kronen.",
            "Winterenten aus dem Norden sammeln sich auf Seen und Flüssen.",
        ],
    },
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


# Early signs of spring, by region and month. Regions come from _region() in
# uplift_engine, which splits the Central European band by elevation:
# "alpine" from about 800 m up, "lowland" below.
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
    "lowland": {
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
}
