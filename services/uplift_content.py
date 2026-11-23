"""
Text library for Seasonal Horizon, in English and German.

A message is a lead plus a companion line. The lead comes from SIGNALS (one
pool per signal in uplift_engine, some with variants like "snow.alpine") or,
when nothing stands out, from PHASES - after dusk in the cold phases from
EVENINGS. The companion comes from NATURE or, on a sunny winter day,
SUN_ENJOYMENT.

How these are written:

- Calm and concrete. Something you could notice, not something to feel.
- At most two sentences. No exclamation marks, no "you've got this".
- True for the region, in an ordinary year. Where timing varies, hedge
  ("around now", "often") rather than claim a date.
- Never dwell on the dark or the shrinking days. Shrinking daylight has no
  pool on purpose.
- German uses Swiss spelling: ss, never the sharp s. A Helvetism where it
  fits (innert, Velo, Beiz), but readable in Germany and Austria too.
- Each signal pool may only use the placeholders its signal provides; the
  tests check this.
"""

WEEKDAYS = {
    "en": ["Monday", "Tuesday", "Wednesday", "Thursday", "Friday",
           "Saturday", "Sunday"],
    "de": ["Montag", "Dienstag", "Mittwoch", "Donnerstag", "Freitag",
           "Samstag", "Sonntag"],
}

MONTHS = {
    "en": ["January", "February", "March", "April", "May", "June", "July",
           "August", "September", "October", "November", "December"],
    "de": ["Januar", "Februar", "März", "April", "Mai", "Juni", "Juli",
           "August", "September", "Oktober", "November", "Dezember"],
}


# ===== Phases of the year =====
#
# The fallback lead, used when no signal is stronger. No figures, so they
# hold on any day of their phase.

PHASES = {
    "darkening": {
        "en": [
            "This is the quiet end of the year. Candles, warm kitchens, early evenings - it has its own kind of comfort.",
            "The light at this time of year is low and golden. It makes even ordinary streets look painted.",
            "The year is slowing down, and it is fine to slow down with it.",
            "Dark evenings are made for the things summer never leaves room for: long dinners, books, a proper conversation.",
            "Bare trees let the low sun through. Rooms and paths that lay in shade all summer get light now.",
            "The shortest days are not far off, and the turn comes with them.",
            "Lit windows on a dark street are one of the best things about this time of year.",
            "Soup season, blanket season, early-to-bed season. Not every season has to be about doing more.",
            "The low sun throws long shadows even at noon. Everything looks sculpted in it.",
            "The sun stands low enough now to shine right to the back of a room. In summer it never gets that far.",
            "This is the time of year for the oven: baked apples, roast chestnuts, anything that warms the kitchen.",
            "Early dusk makes a short walk feel like an outing. The air is cold, and the lights are on by the time you turn back.",
            "Tea tastes better at this time of year. So does anything eaten by lamplight.",
            "The trees have put everything away for the winter. Resting is part of how they grow.",
            "There is nothing to catch up on outside right now. The season is asking for less.",
            "A candle on the table at five in the afternoon makes sense again. In June it never did.",
            "Wool, wood smoke, roasted chestnuts: the season has its own smells, and they are good ones.",
        ],
        "de": [
            "Das ist das stille Ende des Jahres. Kerzen, warme Küchen, frühe Abende - das hat seinen eigenen Trost.",
            "Das Licht steht um diese Jahreszeit tief und golden. Selbst gewöhnliche Strassen sehen darin aus wie gemalt.",
            "Das Jahr wird langsamer, und es ist in Ordnung, mit ihm langsamer zu werden.",
            "Dunkle Abende sind gemacht für das, wofür der Sommer nie Platz lässt: lange Essen, Bücher, ein richtiges Gespräch.",
            "Kahle Bäume lassen die tiefe Sonne durch. Zimmer und Wege, die den ganzen Sommer im Schatten lagen, bekommen jetzt Licht.",
            "Die kürzesten Tage sind nicht mehr weit, und mit ihnen kommt die Wende.",
            "Erleuchtete Fenster in einer dunklen Strasse gehören zum Schönsten an dieser Jahreszeit.",
            "Suppenzeit, Deckenzeit, Früh-ins-Bett-Zeit. Nicht jede Jahreszeit muss mehr von dir wollen.",
            "Die tiefe Sonne wirft selbst mittags lange Schatten. Alles wirkt darin wie gemeisselt.",
            "Die Sonne steht jetzt tief genug, um bis hinten ins Zimmer zu scheinen. Im Sommer kommt sie nie so weit.",
            "Jetzt ist die Zeit für den Ofen: Bratäpfel, heisse Marroni, alles, was die Küche wärmt.",
            "Die frühe Dämmerung macht aus einem kurzen Spaziergang einen Ausflug. Die Luft ist kalt, und wenn du umkehrst, brennen schon die Lichter.",
            "Tee schmeckt um diese Jahreszeit besser. Alles, was man bei Lampenlicht isst, auch.",
            "Die Bäume haben für den Winter alles weggeräumt. Auch das Ruhen gehört zu ihrem Wachsen.",
            "Draussen gibt es gerade nichts nachzuholen. Die Jahreszeit verlangt weniger.",
            "Eine Kerze auf dem Tisch um fünf Uhr nachmittags passt wieder. Im Juni hätte sie das nie getan.",
            "Wolle, Holzrauch, heisse Marroni: Die Jahreszeit hat ihre eigenen Gerüche, und es sind gute.",
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
            "Every day from here is a little lighter than the one before. That is a rare kind of guarantee.",
            "Winter still has the weather, but it has lost the light. It just has not admitted it yet.",
            "The year has its back to the darkness now. Every week faces a little more towards summer.",
            "Seed packets in the shops, the first garden catalogues in the post: the year is already planning its spring.",
        ],
        "de": [
            "Die Kälte hält sich noch, aber das Licht hat es sich schon anders überlegt.",
            "Der Winter macht gerade viel Lärm, das Licht arbeitet leise. Gewinnen wird das Licht.",
            "Nichts am heutigen Tag muss sich nach Frühling anfühlen, damit der Frühling unterwegs ist.",
            "Das ist der Teil des Jahres, der Geduld verlangt. Zurückgezahlt hat er sie noch immer.",
            "Der härteste Abschnitt des Jahres ist zugleich der, der sich schon bessert.",
            "Irgendwo unter alldem zählt der Boden die Tage mit. Er weiss, was als Nächstes kommt.",
            "Das Jahr hat gewendet. Alles ab hier ist ein langsames Argument für das Licht.",
            "Es wird noch früh dunkel, und es ist schon weniger dunkel, als es war.",
            "Graue Tage lassen sich leichter aushalten, wenn das Licht dahinter länger wird.",
            "Du bist jetzt auf der Seite des Jahres, auf der das Licht zurückkommt. Das ist an so einem Morgen etwas wert.",
            "Jeder Tag ab hier ist ein bisschen heller als der davor. Das ist eine seltene Garantie.",
            "Der Winter hat noch das Wetter, aber das Licht hat er verloren. Er gibt es nur noch nicht zu.",
            "Das Jahr kehrt der Dunkelheit jetzt den Rücken. Jede Woche schaut ein wenig mehr Richtung Sommer.",
            "Saatgut in den Läden, die ersten Gartenkataloge im Briefkasten: Das Jahr plant schon seinen Frühling.",
        ],
    },
    "spring": {
        "en": [
            "The bright half of the year has begun. Days now outlast nights.",
            "Spring is the exhale after winter. Everything that waited is moving again.",
            "The evenings are long enough again to do something with them.",
            "This is the season of first times: the first meal outside, the first short sleeves, the first swifts.",
            "Green arrives fast now. Look closely at a hedge and it is different from last week.",
            "The light is generous now, and it is still growing.",
            "Windows open again. The air smells of cut grass and wet earth.",
            "The evenings are getting warm enough to stay out in. That is a whole second day, every day.",
            "Birdsong starts before you are awake now, and keeps going after you are home.",
            "Everything is in a hurry this time of year. It is worth slowing down to watch it.",
            "Cafés put their chairs back out. A whole season of sitting outside starts now.",
        ],
        "de": [
            "Die helle Jahreshälfte hat begonnen. Die Tage sind jetzt länger als die Nächte.",
            "Der Frühling ist das Ausatmen nach dem Winter. Alles, was gewartet hat, bewegt sich wieder.",
            "Die Abende sind wieder lang genug, um etwas mit ihnen anzufangen.",
            "Das ist die Zeit der ersten Male: das erste Essen draussen, die ersten kurzen Ärmel, die ersten Mauersegler.",
            "Das Grün kommt jetzt schnell. Schau eine Hecke genau an - sie ist anders als letzte Woche.",
            "Das Licht ist jetzt grosszügig, und es wächst noch.",
            "Die Fenster gehen wieder auf. Die Luft riecht nach geschnittenem Gras und feuchter Erde.",
            "Die Abende werden warm genug, um draussen zu bleiben. Das ist jeden Tag ein zweiter Tag.",
            "Der Vogelgesang beginnt jetzt, bevor du wach bist, und ist noch nicht vorbei, wenn du heimkommst.",
            "Alles hat es eilig um diese Jahreszeit. Es lohnt sich, langsamer zu werden und zuzuschauen.",
            "Die Cafés stellen ihre Stühle wieder hinaus. Eine ganze Saison des Draussensitzens beginnt.",
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
            "Long light means no rush. A walk after dinner is still a walk in daylight.",
            "The lakes and rivers are warm enough now. Summer is best taken with a swim.",
            "Cherries, apricots, berries - summer arrives on the market stalls in waves.",
            "Warm nights, open windows, late voices in the street. Summer sounds different.",
            "Summer nights barely get dark. Around midsummer the sky in the north-west still glows well after ten.",
        ],
        "de": [
            "Das sind die langen Tage. Abende, die lang genug dauern, um die Zeit zu vergessen.",
            "Der Sommer ist die Jahreszeit, in der man draussen ist, ohne es zu planen.",
            "Warme Abende, spätes Licht, nirgendwo hinmüssen. Darauf hat der Winter gewartet.",
            "Das Licht ist jetzt am grosszügigsten. Es ist genug da, um etwas davon zu verschwenden.",
            "Sommerabende werden in ihrer letzten Stunde golden. Es ist die schönste Stunde des Tages.",
            "Das Obst reift, das Wasser ist warm, und die Abende gehören dir.",
            "Langes Licht heisst: keine Eile. Ein Spaziergang nach dem Abendessen ist immer noch einer bei Tageslicht.",
            "Seen und Flüsse sind jetzt warm genug. Am besten nimmt man den Sommer mit einem Sprung ins Wasser.",
            "Kirschen, Aprikosen, Beeren - der Sommer kommt in Wellen auf die Marktstände.",
            "Warme Nächte, offene Fenster, späte Stimmen auf der Strasse. Der Sommer klingt anders.",
            "Sommernächte werden kaum richtig dunkel. Um Mittsommer leuchtet der Himmel im Nordwesten noch weit nach zehn.",
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
            "Autumn mornings often start in mist and end in clear sun.",
            "The air has that clean, cool smell now. Good walking weather.",
            "The grapes are being picked on the slopes, and the new wine is in the village inns.",
            "Soon the chestnut stands will be back on the street corners. Autumn has a smell.",
            "Pumpkins on doorsteps, fresh cider in the cellars, the first fire in the stove. Autumn is generous.",
        ],
        "de": [
            "Das Herbstlicht steht tief und warm. Alles sieht darin aus wie ein Foto.",
            "Es ist Erntezeit - Äpfel, Birnen, Trauben, die ersten Marroni.",
            "Die Farben wechseln. Für ein paar Wochen sind die Wälder das Leuchtendste weit und breit.",
            "Frische Morgen und milde Nachmittage. Der Herbst kann beides am selben Tag.",
            "Klare Herbsttage haben eine Schärfe, die der Sommer nie schafft. Ferne Hügel wirken zum Greifen nah.",
            "Es ist die Zeit für lange Spaziergänge und eine warme Küche zum Heimkommen.",
            "Herbstmorgen beginnen oft im Nebel und enden in klarer Sonne.",
            "Die Luft hat jetzt diesen klaren, kühlen Geruch. Gutes Wanderwetter.",
            "An den Hängen ist Weinlese, und in den Beizen gibt es Sauser.",
            "Bald stehen wieder Marronistände an den Ecken. Der Herbst hat einen Geruch.",
            "Kürbisse vor den Türen, Süssmost in den Kellern, das erste Feuer im Ofen. Der Herbst ist grosszügig.",
        ],
    },
}


# ===== Signals =====
#
# One pool per signal, keyed like the signal, plus variants after a dot.
# The placeholders each pool may use are listed above it.

SIGNALS = {
    # -- light ----------------------------------------------------------------

    # (none)
    "turning_day": {
        "en": [
            "Today is the shortest day of the year. From tomorrow, every day is a little longer than the one before.",
            "The solstice is today. This is the bottom of the curve - from here it only goes one way.",
            "Shortest day today. The darkness has reached as far as it goes, and tonight it turns.",
            "The darkest day of the year is today. It is also the last day the darkness grows.",
            "Solstice. The sun stops sinking and starts its long climb back.",
            "Solstice. Today the noon sun stands lower than on any other day, and from tomorrow it climbs again.",
        ],
        "de": [
            "Heute ist der kürzeste Tag des Jahres. Ab morgen ist jeder Tag ein wenig länger als der davor.",
            "Heute ist Sonnenwende. Das ist der Tiefpunkt der Kurve - ab hier geht es nur noch in eine Richtung.",
            "Kürzester Tag heute. Weiter reicht die Dunkelheit nicht, und ab heute Nacht weicht sie zurück.",
            "Heute ist der dunkelste Tag des Jahres. Und der letzte, an dem die Dunkelheit wächst.",
            "Sonnenwende. Die Sonne hört auf zu sinken und beginnt ihren langen Aufstieg.",
            "Sonnenwende. Heute steht die Mittagssonne so tief wie an keinem anderen Tag, und ab morgen steigt sie wieder.",
        ],
    },

    # (none)
    "equinox_day": {
        "en": [
            "Equinox: the sun crosses the equator today, and the bright half of the year begins.",
            "Equinox. The light has caught up with the dark, and from here it pulls ahead.",
            "Spring's astronomical start. From here the days stay longer than the nights until September.",
            "Halfway from the darkest day to the brightest. The rest of the climb is the easy part.",
            "Equinox: day and night are about equal today - and from here the day stays ahead until September.",
        ],
        "de": [
            "Tagundnachtgleiche: Die Sonne überquert heute den Äquator, und die helle Jahreshälfte beginnt.",
            "Tagundnachtgleiche. Das Licht hat die Dunkelheit eingeholt, und ab hier zieht es davon.",
            "Astronomischer Frühlingsbeginn. Ab jetzt sind die Tage bis im September länger als die Nächte.",
            "Halbzeit zwischen dem dunkelsten und dem hellsten Tag. Der Rest des Aufstiegs ist der leichte Teil.",
            "Tagundnachtgleiche: Tag und Nacht sind heute etwa gleich lang - und ab hier bleibt der Tag bis im September vorn.",
        ],
    },

    # {hours_gained}
    "lichtmess": {
        "en": [
            "Candlemas. The old saying goes that by today the day is an hour longer - and it holds: {hours_gained} since the solstice.",
            "2 February, Lichtmess. The farmers' rule says an hour of light has come back. The numbers agree: {hours_gained}.",
            "Today is Candlemas, the old halfway mark of winter. Since the solstice the day has grown by {hours_gained}.",
        ],
        "de": [
            "Lichtmess. «An Lichtmess ist der Tag eine Stunde länger», heisst es - und es stimmt: {hours_gained} seit der Sonnenwende.",
            "2. Februar, Lichtmess. Die Bauernregel sagt, eine Stunde Licht sei zurück. Die Zahlen geben ihr recht: {hours_gained}.",
            "Heute ist Lichtmess, die alte Wintermitte. Seit der Sonnenwende ist der Tag um {hours_gained} gewachsen.",
        ],
    },

    # {days_to_solstice} {days} {days_dat}
    "solstice_countdown": {
        "en": [
            "{days_to_solstice} {days} to the solstice. After that, the light starts coming back.",
            "The turn is close: in {days_to_solstice} {days_dat} the days stop getting shorter.",
            "Only {days_to_solstice} {days} until the shortest day. Everything after it is a gain.",
            "The countdown is short now: {days_to_solstice} {days} to the turn of the light.",
            "The bottom of the year is {days_to_solstice} {days} away. After that, every day is a little longer.",
            "{days_to_solstice} more {days}, and then the light turns.",
        ],
        "de": [
            "Noch {days_to_solstice} {days} bis zur Sonnenwende. Danach kommt das Licht zurück.",
            "Die Wende ist nah: In {days_to_solstice} {days_dat} hören die Tage auf, kürzer zu werden.",
            "Nur noch {days_to_solstice} {days} bis zum kürzesten Tag. Alles danach ist Gewinn.",
            "Der Countdown ist kurz: noch {days_to_solstice} {days} bis zur Wende des Lichts.",
            "Der Tiefpunkt des Jahres ist {days_to_solstice} {days} entfernt. Danach wird jeder Tag ein wenig länger.",
            "Noch {days_to_solstice} {days}, dann dreht das Licht.",
        ],
    },

    # {days_to_equinox} {days} {days_dat}
    "equinox_countdown": {
        "en": [
            "{days_to_equinox} {days} to the equinox. Then the bright half of the year begins.",
            "In {days_to_equinox} {days_dat} the sun crosses the equator, and spring starts by the calendar too.",
            "The equinox is {days_to_equinox} {days} off. The days are gaining about as fast as they ever do.",
            "{days_to_equinox} more {days} until day and night are equal. After that, the light has the bigger share.",
        ],
        "de": [
            "Noch {days_to_equinox} {days} bis zur Tagundnachtgleiche. Dann beginnt die helle Jahreshälfte.",
            "In {days_to_equinox} {days_dat} überquert die Sonne den Äquator, und der Frühling beginnt auch im Kalender.",
            "Die Tagundnachtgleiche ist {days_to_equinox} {days} entfernt. Die Tage wachsen jetzt so schnell wie sonst kaum im Jahr.",
            "Noch {days_to_equinox} {days}, bis Tag und Nacht gleich lang sind. Danach hat das Licht den grösseren Anteil.",
        ],
    },

    # {days_since} {days} {sunset_later} {minutes}
    "turned": {
        "en": [
            "The year has turned. For now the day gains seconds; by the end of January it is two or three minutes a day.",
            "{days_since} {days} past the shortest day. The light comes back slowly at first, then faster every week.",
            "The turn is behind you. The sun already sets {sunset_later} {minutes} later than at its earliest, in mid-December.",
            "The evenings are leading the way: sunset is {sunset_later} {minutes} later than at its earliest. The mornings follow in early January.",
            "The shortest day is behind you. Every day from here is longer than the one before, all the way to June.",
            "The shortest day is behind you, and from here the numbers only point one way.",
            "The turn has happened, quietly, with no one watching. The light is on its way back.",
        ],
        "de": [
            "Das Jahr hat gewendet. Noch gewinnt der Tag Sekunden; Ende Januar sind es zwei bis drei Minuten am Tag.",
            "{days_since} {days} nach dem kürzesten Tag. Das Licht kommt zurück, zuerst langsam, dann jede Woche schneller.",
            "Die Wende liegt hinter dir. Die Sonne geht schon {sunset_later} {minutes} später unter als an ihrem frühesten Tag Mitte Dezember.",
            "Die Abende gehen voran: Die Sonne geht {sunset_later} {minutes} später unter als an ihrem frühesten Tag. Die Morgen folgen Anfang Januar.",
            "Der kürzeste Tag liegt hinter dir. Ab jetzt ist jeder Tag länger als der davor, bis im Juni.",
            "Der kürzeste Tag liegt hinter dir, und ab hier zeigen die Zahlen nur noch in eine Richtung.",
            "Die Wende ist passiert, leise und ohne Zuschauer. Das Licht ist auf dem Rückweg.",
        ],
    },

    # {minutes_left} {minutes} {days_to_solstice} {days}
    "near_shortest": {
        "en": [
            "The days are now within {minutes_left} {minutes} of their shortest. From here the year stands almost still, and then it turns.",
            "Almost at the turning point: today is only {minutes_left} {minutes} longer than the shortest day will be.",
            "The light has nearly stopped changing: today's daylight and the shortest day's differ by just {minutes_left} {minutes}.",
            "The year is slowing to a standstill before it turns. All that separates today from the turning point is {minutes_left} {minutes} of daylight.",
            "The days have only {minutes_left} {minutes} left to shorten, and the turn is {days_to_solstice} {days} away. Nearly all of it is done.",
            "{days_to_solstice} {days} until the turn, and only {minutes_left} {minutes} between today and the shortest day. Almost there.",
        ],
        "de": [
            "Die Tage sind jetzt nur noch {minutes_left} {minutes} von ihrem kürzesten Stand entfernt. Ab hier steht das Jahr fast still, und dann wendet es.",
            "Fast am Wendepunkt: Der heutige Tag ist nur noch {minutes_left} {minutes} länger als der kürzeste.",
            "Das Licht verändert sich kaum noch: Das Tageslicht von heute und das des kürzesten Tages unterscheiden sich nur um {minutes_left} {minutes}.",
            "Das Jahr kommt vor der Wende fast zum Stillstand. Vom Wendepunkt trennen heute nur noch {minutes_left} {minutes} Tageslicht.",
            "Den Tagen bleiben nur noch {minutes_left} {minutes} bis zum Tiefpunkt, und die Wende ist {days_to_solstice} {days} entfernt. Fast alles ist geschafft.",
            "Noch {days_to_solstice} {days} bis zur Wende, und nur noch {minutes_left} {minutes} Unterschied zum kürzesten Tag. Fast geschafft.",
        ],
    },

    # {sunset}
    "evenings_turned": {
        "en": [
            "The sun set a few seconds later today than yesterday. The evenings have turned before the solstice even arrives.",
            "A quiet one: sunsets are already getting later again. {sunset} today, and later from here on.",
            "The earliest sunset of the year is behind you. The evenings start growing now, ahead of the solstice.",
            "Something the calendar does not tell you: the evenings start growing before the solstice. Sunset today {sunset}, a touch later than yesterday.",
            "The darkest afternoons are already behind you. Sunsets have turned and are creeping later.",
            "Sunset at {sunset} - a few seconds later than yesterday. The evenings are the first part of the day to turn.",
        ],
        "de": [
            "Die Sonne ist heute ein paar Sekunden später untergegangen als gestern. Die Abende haben gedreht, noch bevor die Sonnenwende da ist.",
            "Ein leises Zeichen: Die Sonnenuntergänge werden schon wieder später. Heute um {sunset}, und ab jetzt jeden Tag etwas später.",
            "Der früheste Sonnenuntergang des Jahres liegt hinter dir. Die Abende wachsen schon, der Sonnenwende voraus.",
            "Etwas, das der Kalender nicht verrät: Die Abende wachsen schon vor der Sonnenwende. Sonnenuntergang heute {sunset}, eine Spur später als gestern.",
            "Die dunkelsten Nachmittage liegen schon hinter dir. Die Sonnenuntergänge haben gedreht und werden wieder später.",
            "Sonnenuntergang um {sunset} - ein paar Sekunden später als gestern. Die Abende drehen als Erstes.",
        ],
    },

    # {sunrise}
    "mornings_turned": {
        "en": [
            "The mornings have turned too: sunrise at {sunrise}, a little earlier each day now.",
            "Sunrise is creeping earlier again - {sunrise} today. The dark mornings are on their way out.",
            "Both ends of the day are growing now. The sun was up at {sunrise}, and tomorrow it is earlier still.",
            "The darkest mornings are over. Sunrise at {sunrise}, and earlier each day from here.",
            "Light at breakfast is coming back. The sun rose at {sunrise} today, a little sooner than yesterday.",
        ],
        "de": [
            "Auch die Morgen haben gedreht: Sonnenaufgang um {sunrise}, jetzt jeden Tag etwas früher.",
            "Der Sonnenaufgang rückt wieder nach vorn - heute {sunrise}. Die dunklen Morgen sind auf dem Rückzug.",
            "Jetzt wächst der Tag an beiden Enden. Die Sonne ging um {sunrise} auf, und morgen noch etwas früher.",
            "Die dunkelsten Morgen sind vorbei. Sonnenaufgang um {sunrise}, und ab hier jeden Tag etwas früher.",
            "Das Licht beim Frühstück kommt zurück. Die Sonne ging heute um {sunrise} auf, ein wenig früher als gestern.",
        ],
    },

    # {hours_mark} {days_until} {when} {days} {days_dat}
    "hour_mark": {
        "en": [
            "The day passes {hours_mark} hours {when}. Another mark on the way back to summer.",
            "{hours_mark} hours of daylight is close: {days_until} more {days}.",
            "Watch for it {when}: the first day with more than {hours_mark} hours of light.",
            "The {hours_mark}-hour day is coming {when}. Each of these marks is a little further from winter.",
            "More than {hours_mark} hours of daylight, {when}. The light is counting in whole hours now.",
        ],
        "de": [
            "Der Tag knackt {when} die {hours_mark}-Stunden-Marke. Wieder eine Etappe auf dem Weg zum Sommer.",
            "{hours_mark} Stunden Tageslicht sind nah: noch {days_until} {days}.",
            "Achte {when} darauf: der erste Tag mit mehr als {hours_mark} Stunden Licht.",
            "Der {hours_mark}-Stunden-Tag kommt {when}. Jede dieser Marken liegt ein Stück weiter weg vom Winter.",
            "Mehr als {hours_mark} Stunden Tageslicht, {when}. Das Licht zählt jetzt in ganzen Stunden.",
        ],
    },
    "hour_mark.today": {
        "en": [
            "Today is the first day with more than {hours_mark} hours of daylight.",
            "{hours_mark} hours of light, passed today - for the first time this year.",
            "A small milestone: the day is over {hours_mark} hours long again.",
            "The day has crossed {hours_mark} hours. It was last this long in autumn, heading the other way.",
            "From today there are more than {hours_mark} hours between sunrise and sunset. One more whole hour won back.",
        ],
        "de": [
            "Heute ist der erste Tag mit mehr als {hours_mark} Stunden Tageslicht.",
            "{hours_mark} Stunden Licht, heute geknackt - zum ersten Mal in diesem Jahr.",
            "Ein kleiner Meilenstein: Der Tag ist wieder über {hours_mark} Stunden lang.",
            "Der Tag hat die {hours_mark} Stunden überschritten. So lang war er zuletzt im Herbst, in der anderen Richtung.",
            "Ab heute liegen mehr als {hours_mark} Stunden zwischen Sonnenaufgang und Sonnenuntergang. Wieder eine ganze Stunde zurückgewonnen.",
        ],
    },

    # {hours_gained}
    "since_solstice": {
        "en": [
            "The light has already turned. Since the solstice the day has grown by {hours_gained}, whether or not it feels like it yet.",
            "The year has added {hours_gained} since the shortest day. That is not nothing, even if the mornings still argue otherwise.",
            "Quietly, without ceremony, the year has handed back {hours_gained} of daylight since the solstice.",
            "There are already {hours_gained} of light between you and the darkest day. The direction is settled now.",
            "Since the solstice: {hours_gained} more light. It accumulates whether you notice it or not.",
            "{hours_gained} more daylight than at the solstice. It adds up quietly, a few minutes at a time.",
            "Since the shortest day the light has grown by {hours_gained}. The trend has one direction now.",
        ],
        "de": [
            "Das Licht hat schon gedreht. Seit der Sonnenwende ist der Tag um {hours_gained} gewachsen, auch wenn es sich noch nicht so anfühlt.",
            "Seit dem kürzesten Tag hat das Jahr {hours_gained} zugelegt. Das ist nicht nichts, auch wenn die Morgen noch dagegenhalten.",
            "Ganz ohne Aufhebens hat das Jahr seit der Sonnenwende {hours_gained} Tageslicht zurückgegeben.",
            "Zwischen dir und dem dunkelsten Tag liegen schon {hours_gained} Licht. Die Richtung steht inzwischen fest.",
            "Seit der Sonnenwende: {hours_gained} mehr Licht. Das sammelt sich an, ob man es bemerkt oder nicht.",
            "{hours_gained} mehr Tageslicht als zur Sonnenwende. Es summiert sich leise, ein paar Minuten aufs Mal.",
            "Seit dem kürzesten Tag ist das Licht um {hours_gained} gewachsen. Der Trend kennt jetzt nur eine Richtung.",
        ],
    },

    # {twin_date}
    "autumn_twin": {
        "en": [
            "The day is as long again as it was on {twin_date}. The light is winding back through autumn.",
            "Today has the same length of daylight as {twin_date}. Remember how light that still felt?",
            "Back to the light of {twin_date}. Every day from here goes a little further back towards summer.",
            "By length of daylight, today matches {twin_date}. The dark part of the winter is unwinding.",
            "Today is as long as {twin_date} was. The days are retracing autumn's steps, in the right direction this time.",
        ],
        "de": [
            "Der Tag ist wieder so lang wie am {twin_date}. Das Licht spult zurück durch den Herbst.",
            "Heute gibt es gleich viel Tageslicht wie am {twin_date}. Weisst du noch, wie hell sich das damals anfühlte?",
            "Zurück beim Licht vom {twin_date}. Ab hier geht es jeden Tag ein Stück weiter Richtung Sommer.",
            "Von der Tageslänge her entspricht der heutige Tag dem {twin_date}. Der dunkle Teil des Winters wickelt sich ab.",
            "Heute ist so lang wie der {twin_date}. Die Tage gehen den Weg des Herbstes zurück, diesmal in die richtige Richtung.",
        ],
    },

    # {delta} {minutes} {day_length} {sunrise} {sunset}
    "daily_gain": {
        "en": [
            "Today is {delta} {minutes} longer than yesterday. Small, but it happens again tomorrow.",
            "Another {delta} {minutes} of light today. Small enough to miss, steady enough to count on.",
            "Sunrise {sunrise}, sunset {sunset} - {day_length} of daylight, and more of it tomorrow.",
            "{day_length} of light today, {delta} {minutes} more than yesterday.",
            "The day grew by {delta} {minutes} overnight. Nobody announced it, but it happened.",
            "{delta} {minutes} more light than yesterday, and the gain goes on tomorrow.",
        ],
        "de": [
            "Heute ist {delta} {minutes} länger als gestern. Wenig, aber morgen passiert es wieder.",
            "Wieder {delta} {minutes} mehr Licht heute. Klein genug, um es zu übersehen, stetig genug, um darauf zu zählen.",
            "Aufgang {sunrise}, Untergang {sunset} - {day_length} Tageslicht, und morgen etwas mehr.",
            "{day_length} Licht heute, {delta} {minutes} mehr als gestern.",
            "Der Tag ist über Nacht um {delta} {minutes} gewachsen. Niemand hat es angekündigt, aber es ist passiert.",
            "{delta} {minutes} mehr Licht als gestern, und morgen geht es weiter.",
        ],
    },
    "daily_gain.fast": {
        "en": [
            "{delta} {minutes} more light than yesterday. The days grow about as fast now as they ever do.",
            "The days are racing now: +{delta} {minutes} since yesterday. You can see the difference within a week.",
            "Another {delta} {minutes} today. At this pace the evenings change from one week to the next.",
            "{day_length} of light, {delta} {minutes} more than yesterday. This is the steep part of the climb.",
            "+{delta} {minutes} on yesterday. At this time of year the light arrives by the week, not by the day.",
        ],
        "de": [
            "{delta} {minutes} mehr Licht als gestern. Schneller wachsen die Tage im ganzen Jahr kaum.",
            "Die Tage legen jetzt richtig zu: +{delta} {minutes} seit gestern. Den Unterschied sieht man innert einer Woche.",
            "Wieder {delta} {minutes} mehr heute. In diesem Tempo verändern sich die Abende von Woche zu Woche.",
            "{day_length} Licht, {delta} {minutes} mehr als gestern. Das ist der steile Teil des Aufstiegs.",
            "+{delta} {minutes} gegenüber gestern. Um diese Jahreszeit kommt das Licht wochenweise, nicht tageweise.",
        ],
    },

    # {milestone_time} {milestone_days} {when} {days} {days_dat} {sunset}
    # ({milestone_days} is absent at one day, leaving the {when} lines)
    "sunset_milestone": {
        "en": [
            "In {milestone_days} {days} the sun sets after {milestone_time} again. Something to look forward to on the way home.",
            "Mark it: {milestone_days} {days} from now the sunset moves past {milestone_time}. Evenings start feeling different around then.",
            "The sun currently sets at {sunset}. In {milestone_days} {days_dat} that becomes {milestone_time}, and the afternoon stretches out a little.",
            "{milestone_days} {days_dat} until sunset passes {milestone_time}. The evenings are being handed back to you.",
            "Sunset at {sunset} today. {milestone_time} is {milestone_days} {days} away.",
            "Count {milestone_days} {days}: then the sun stays up past {milestone_time}.",
            "The sunset moves past {milestone_time} {when}. The evenings keep opening up.",
            "Sunset today at {sunset}; {when} it is after {milestone_time}.",
        ],
        "de": [
            "In {milestone_days} {days_dat} geht die Sonne wieder nach {milestone_time} unter. Etwas, worauf man sich auf dem Heimweg freuen kann.",
            "Merk dir das: In {milestone_days} {days_dat} wandert der Sonnenuntergang hinter {milestone_time}. Ab dann fühlen sich die Abende anders an.",
            "Die Sonne geht gerade um {sunset} unter. In {milestone_days} {days_dat} ist es {milestone_time}, und der Nachmittag wird spürbar länger.",
            "Noch {milestone_days} {days}, bis der Sonnenuntergang {milestone_time} überschreitet. Die Abende kommen zurück.",
            "Sonnenuntergang heute um {sunset}. Bis {milestone_time} sind es noch {milestone_days} {days}.",
            "Zähl {milestone_days} {days}: Dann bleibt die Sonne bis nach {milestone_time}.",
            "Der Sonnenuntergang rückt {when} über {milestone_time} hinaus. Die Abende öffnen sich weiter.",
            "Sonnenuntergang heute um {sunset}; {when} ist es nach {milestone_time}.",
        ],
    },

    # {milestone_time} {milestone_days} {when} {days} {days_dat} {sunrise}
    "sunrise_milestone": {
        "en": [
            "In {milestone_days} {days} the sun rises before {milestone_time} again. The mornings are coming back.",
            "Sunrise is at {sunrise} today. In {milestone_days} {days} it moves ahead of {milestone_time}.",
            "{milestone_days} {days} until the sun is up before {milestone_time}. Light on the way to work is not far off.",
            "The sun rises before {milestone_time} {when}. The mornings are filling with light.",
            "Sunrise at {sunrise} today; {when} it is before {milestone_time}.",
            "The mornings are brightening: in {milestone_days} {days_dat} the sun is up before {milestone_time}.",
        ],
        "de": [
            "In {milestone_days} {days_dat} geht die Sonne wieder vor {milestone_time} auf. Die Morgen kommen zurück.",
            "Sonnenaufgang heute um {sunrise}. In {milestone_days} {days_dat} rückt er vor {milestone_time}.",
            "Noch {milestone_days} {days}, bis die Sonne vor {milestone_time} aufgeht. Licht auf dem Arbeitsweg ist nicht mehr weit.",
            "Die Sonne geht {when} vor {milestone_time} auf. Die Morgen füllen sich mit Licht.",
            "Sonnenaufgang heute um {sunrise}; {when} ist es vor {milestone_time}.",
            "Die Morgen werden heller: In {milestone_days} {days_dat} ist die Sonne vor {milestone_time} oben.",
        ],
    },

    # {noon_gain}
    "noon_sun": {
        "en": [
            "At midday the sun now stands {noon_gain} degrees higher than at the solstice. You can feel it on your face when it comes out.",
            "The sun climbs higher every noon - {noon_gain} degrees above its December low already. On a south-facing wall, that is real warmth.",
            "{noon_gain} degrees higher at noon than at the turn of the year. The sun is not just staying longer, it is getting stronger.",
            "Midday shadows are noticeably shorter than in December: the sun stands {noon_gain} degrees higher.",
            "{noon_gain} degrees more height at midday since the solstice. On a sheltered bench in the sun, you feel the difference.",
        ],
        "de": [
            "Mittags steht die Sonne jetzt {noon_gain} Grad höher als zur Sonnenwende. Wenn sie rauskommt, spürst du das im Gesicht.",
            "Die Sonne steigt jeden Mittag höher - schon {noon_gain} Grad über ihrem Tiefstand im Dezember. An einer Südwand ist das echte Wärme.",
            "Mittags {noon_gain} Grad höher als zur Jahreswende. Die Sonne bleibt nicht nur länger, sie wird auch kräftiger.",
            "Die Mittagsschatten sind spürbar kürzer als im Dezember: Die Sonne steht {noon_gain} Grad höher.",
            "{noon_gain} Grad mehr Höhe am Mittag seit der Sonnenwende. Auf einer windgeschützten Bank an der Sonne spürst du den Unterschied.",
        ],
    },

    # {dusk} {sunset}
    "dusk_light": {
        "en": [
            "The sun sets at {sunset}, but it stays light enough to be outside until about {dusk}.",
            "Sunset is not the end of the day: there is usable light until around {dusk}.",
            "After sunset at {sunset}, the blue hour lasts until about {dusk}. Worth a walk.",
            "Daylight officially ends at {sunset}. In practice you can walk without a lamp until about {dusk}.",
            "Sunset at {sunset}, light without a lamp until about {dusk}. The evening starts gently.",
            "The time between {sunset} and {dusk} is the blue hour. Lit windows look their best in it.",
            "There is light enough for the way home until about {dusk}, well after the sun has set at {sunset}.",
            "Dusk lingers until around {dusk} today. The sky often keeps its colour longest once the sun is gone.",
        ],
        "de": [
            "Die Sonne geht um {sunset} unter, aber hell genug für draussen bleibt es bis etwa {dusk}.",
            "Mit dem Sonnenuntergang ist der Tag nicht vorbei: Brauchbares Licht gibt es bis gegen {dusk}.",
            "Nach dem Sonnenuntergang um {sunset} dauert die blaue Stunde bis etwa {dusk}. Ein Spaziergang lohnt sich.",
            "Offiziell endet das Tageslicht um {sunset}. Tatsächlich kommst du bis etwa {dusk} ohne Lampe aus.",
            "Sonnenuntergang um {sunset}, Licht ohne Lampe bis etwa {dusk}. Der Abend fängt sanft an.",
            "Die Zeit zwischen {sunset} und {dusk} ist die blaue Stunde. Erleuchtete Fenster sehen darin am schönsten aus.",
            "Für den Heimweg reicht das Licht bis etwa {dusk}, lange nachdem die Sonne um {sunset} untergegangen ist.",
            "Die Dämmerung hält heute bis gegen {dusk}. Der Himmel behält seine Farbe oft am längsten, wenn die Sonne schon weg ist.",
        ],
    },

    # {day_length} {sunset}
    "peak_light": {
        "en": [
            "{day_length} of daylight today, the sun setting at {sunset}. These are the long days the winter was saving up for.",
            "The light is near its peak: {day_length} from sunrise to sunset. Plenty to spend on a long evening.",
            "Sunset at {sunset}. There is no need to hurry anything today.",
            "Light from early morning to well past {sunset}. Days like this have room for everything.",
            "{day_length} between sunrise and sunset. There is time today for the thing you keep postponing.",
            "{day_length} of daylight. On days like this, even a swim after work happens in the sun.",
        ],
        "de": [
            "{day_length} Tageslicht heute, Sonnenuntergang um {sunset}. Für diese langen Tage hat der Winter gespart.",
            "Das Licht ist nahe am Höhepunkt: {day_length} von Aufgang bis Untergang. Genug für einen langen Abend.",
            "Sonnenuntergang um {sunset}. Heute muss nichts eilen.",
            "Licht vom frühen Morgen bis weit nach {sunset}. Solche Tage haben Platz für alles.",
            "{day_length} zwischen Aufgang und Untergang. Heute ist Zeit für das, was du immer aufschiebst.",
            "{day_length} Tageslicht. An solchen Tagen ist auch das Bad nach Feierabend noch eines an der Sonne.",
        ],
    },

    # -- weather --------------------------------------------------------------

    # {grey_days} {days} {days_dat} {sun_hours} {hours}
    "first_sun": {
        "en": [
            "After {grey_days} grey {days}, a sunny one: about {sun_hours} {hours} of sun today.",
            "The sun is back. The first proper sunshine in {grey_days} {days} - around {sun_hours} {hours} of it.",
            "{grey_days} {days} without much sun, and now this: roughly {sun_hours} {hours} today.",
            "Finally. After {grey_days} {days} of grey, today brings about {sun_hours} {hours} of sunshine.",
            "The grey has broken: about {sun_hours} {hours} of sun today, after {grey_days} {days} without.",
            "Today the sun shows it was there all along: around {sun_hours} {hours}, the first real sunshine in {grey_days} {days}.",
        ],
        "de": [
            "Nach {grey_days} grauen {days_dat} ein sonniger: rund {sun_hours} {hours} Sonne heute.",
            "Die Sonne ist zurück. Der erste richtige Sonnentag seit {grey_days} {days_dat} - etwa {sun_hours} {hours}.",
            "{grey_days} {days} ohne viel Sonne, und jetzt das: heute ungefähr {sun_hours} {hours}.",
            "Endlich. Nach {grey_days} {days_dat} Grau bringt heute rund {sun_hours} {hours} Sonnenschein.",
            "Das Grau ist aufgerissen: etwa {sun_hours} {hours} Sonne heute, nach {grey_days} {days_dat} ohne.",
            "Heute zeigt die Sonne, dass sie die ganze Zeit da war: rund {sun_hours} {hours}, der erste richtige Sonnenschein seit {grey_days} {days_dat}.",
        ],
    },

    # {sunny_day} {when} {sun_hours} {hours}
    "sun_ahead": {
        "en": [
            "Something to look forward to: {sunny_day} brings about {sun_hours} {hours} of sunshine.",
            "The sun is coming back {when}. {sunny_day} looks bright - around {sun_hours} {hours} of it.",
            "{sunny_day} has sun in the forecast, about {sun_hours} {hours}. Worth keeping a little of it free.",
            "Hold on until {sunny_day}: the forecast promises around {sun_hours} {hours} of sun.",
            "{sunny_day} looks like the bright day of this stretch: around {sun_hours} {hours} of sun.",
            "Keep {sunny_day} in mind - the forecast has about {sun_hours} {hours} of sunshine for it.",
        ],
        "de": [
            "Etwas, worauf du dich freuen kannst: Der {sunny_day} bringt rund {sun_hours} {hours} Sonne.",
            "Die Sonne kommt {when} zurück. Der {sunny_day} sieht hell aus - etwa {sun_hours} {hours} lang.",
            "Für {sunny_day} steht Sonne in der Vorhersage, ungefähr {sun_hours} {hours}. Es lohnt sich, dir etwas davon freizuhalten.",
            "Bis {sunny_day} durchhalten: Die Vorhersage verspricht rund {sun_hours} {hours} Sonne.",
            "Der {sunny_day} sieht nach dem hellen Tag dieser Woche aus: rund {sun_hours} {hours} Sonne.",
            "Merk dir den {sunny_day} - die Vorhersage hat etwa {sun_hours} {hours} Sonnenschein dafür.",
        ],
    },

    # the evening of a sunny day, with another one to follow
    "sun_ahead.again": {
        "en": [
            "Tomorrow brings sun again: about {sun_hours} {hours} of it.",
            "More of the same tomorrow - around {sun_hours} {hours} of sunshine on {sunny_day}.",
            "{sunny_day} looks bright again, with about {sun_hours} {hours} of sun. Worth planning something outside.",
            "Another sunny day tomorrow: about {sun_hours} {hours}. Good news to go to sleep on.",
        ],
        "de": [
            "Morgen gibt es wieder Sonne: etwa {sun_hours} {hours}.",
            "Morgen geht es so weiter - rund {sun_hours} {hours} Sonnenschein am {sunny_day}.",
            "Der {sunny_day} sieht wieder hell aus, mit etwa {sun_hours} {hours} Sonne. Es lohnt sich, etwas draussen zu planen.",
            "Morgen wieder ein Sonnentag: etwa {sun_hours} {hours}. Eine gute Nachricht zum Einschlafen.",
        ],
    },

    # (none)
    "hochnebel": {
        "en": [
            "A lid of low cloud today, with clear sky above it. A few hundred metres up, the sun is out.",
            "Hochnebel: grey down here, blue above. Any hill that pokes through the lid is in sunshine.",
            "The grey today is a layer, not a heavy sky. Above it the sun is shining - worth a trip up if you can.",
            "A fog-lid day. From a viewpoint above it, the land below looks like a sea of cloud.",
            "The cloud today sits low and flat, and the sky above it is clear. The sun has not gone anywhere.",
            "Grey below, sun above: today's cloud is a flat lid. The nearest hill or mountain railway may be enough to get over it.",
            "Hochnebel today. It keeps the nights milder underneath, and the sun is waiting just above.",
        ],
        "de": [
            "Heute liegt ein Deckel aus tiefen Wolken über dem Land, darüber klarer Himmel. Ein paar hundert Meter höher scheint die Sonne.",
            "Hochnebel: unten grau, oben blau. Jeder Hügel, der durch den Deckel ragt, liegt an der Sonne.",
            "Das Grau heute ist eine Schicht, kein schwerer Himmel. Darüber scheint die Sonne - wer kann, fährt hinauf.",
            "Ein Hochnebeltag. Von einem Aussichtspunkt darüber sieht das Land darunter aus wie ein Nebelmeer.",
            "Die Wolken liegen heute tief und flach, der Himmel darüber ist klar. Die Sonne ist nirgends hingegangen.",
            "Unten grau, oben Sonne: Die Wolke ist heute ein flacher Deckel. Der nächste Hügel oder die nächste Bergbahn reicht vielleicht, um darüber zu kommen.",
            "Hochnebel heute. Darunter bleiben die Nächte milder, und gleich darüber wartet die Sonne.",
        ],
    },

    # {snow_cm}
    "snow": {
        "en": [
            "Snow today. It turns the grey into light - everything reflects, and the world goes quiet.",
            "Fresh snow: the brightest thing winter does. Even a dull sky looks lighter over it.",
            "Snow is falling. Tracks to read, a quieter town, and a reason for a hot drink after.",
            "A snow day. The light bounces off everything, and for a while the year looks new.",
            "Snow today. Even the dullest light goes further when the ground reflects it.",
            "Snow today. Every branch and fence gets a white outline, and the town looks freshly drawn.",
        ],
        "de": [
            "Heute Schnee. Er macht aus Grau Licht - alles reflektiert, und die Welt wird still.",
            "Frischer Schnee: das Hellste, was der Winter kann. Selbst ein trüber Himmel wirkt darüber heller.",
            "Es schneit. Spuren zum Lesen, eine leisere Stadt, und ein Grund für ein heisses Getränk danach.",
            "Ein Schneetag. Das Licht prallt von allem ab, und für eine Weile sieht das Jahr neu aus.",
            "Heute Schnee. Selbst das trübste Licht reicht weiter, wenn der Boden es zurückwirft.",
            "Heute Schnee. Jeder Ast und jeder Zaun bekommt eine weisse Kontur, und die Stadt sieht aus wie frisch gezeichnet.",
        ],
    },
    "snow.fresh": {
        "en": [
            "{snow_cm} cm of fresh snow today. The world goes quiet and bright at the same time.",
            "Around {snow_cm} cm of new snow. Tracks to read, a muffled town, and light coming from the ground.",
            "Fresh snow, about {snow_cm} cm. The grey has a white floor today, and everything is lighter for it.",
            "About {snow_cm} cm of new snow. Enough to change the sound of the whole neighbourhood.",
            "{snow_cm} cm of snow today. Tonight the streets will be brighter than on any evening without it.",
        ],
        "de": [
            "{snow_cm} cm Neuschnee heute. Die Welt wird gleichzeitig still und hell.",
            "Rund {snow_cm} cm Neuschnee. Spuren zum Lesen, eine gedämpfte Stadt, und Licht, das vom Boden kommt.",
            "Neuschnee, etwa {snow_cm} cm. Das Grau hat heute einen weissen Boden, und alles ist heller dadurch.",
            "Etwa {snow_cm} cm Neuschnee. Genug, um den Klang des ganzen Quartiers zu verändern.",
            "{snow_cm} cm Schnee heute. Am Abend sind die Strassen heller als an jedem Abend ohne.",
        ],
    },
    # (none) - the first snow in over a month, in autumn or the darkening
    "snow.first": {
        "en": [
            "The first snow of the season. However often it has happened before, people still stop at the window for it.",
            "Snow for the first time this season. Everything outside gets quieter with it.",
            "First snow. The year has a few days everyone notices, and this is one of them.",
            "The first snow of the season. Even a thin layer makes the town look new.",
        ],
        "de": [
            "Der erste Schnee der Saison. Wie oft es ihn schon gab: Die Leute bleiben dafür noch immer am Fenster stehen.",
            "Schnee, zum ersten Mal in dieser Saison. Draussen wird damit alles leiser.",
            "Erster Schnee. Das Jahr hat ein paar Tage, die allen auffallen, und das ist einer davon.",
            "Der erste Schnee der Saison. Schon eine dünne Schicht lässt die Stadt neu aussehen.",
        ],
    },
    "snow.alpine": {
        "en": [
            "Snow up here today. Good for the slopes, good for the sledge run, good for the quiet.",
            "It is snowing. Tomorrow the first tracks in the fresh snow could be yours.",
            "Fresh snow on the mountain. When the sun comes back, it will be dazzling.",
            "Snowfall today. The winter up here is doing exactly what it should.",
            "Snow is falling on the mountain. In the huts the stoves are lit and the windows steam up.",
        ],
        "de": [
            "Hier oben schneit es heute. Gut für die Pisten, gut für den Schlittelweg, gut für die Ruhe.",
            "Es schneit. Morgen könnten die ersten Spuren im Neuschnee deine sein.",
            "Neuschnee am Berg. Wenn die Sonne zurückkommt, wird es blendend hell.",
            "Schneefall heute. Der Winter hier oben macht genau, was er soll.",
            "Am Berg schneit es. In den Hütten brennen die Öfen, und die Fenster beschlagen.",
        ],
    },

    # {sun_hours} {hours}
    "sunny_today": {
        "en": [
            "About {sun_hours} {hours} of sunshine today. The light has the day to itself.",
            "A bright one: around {sun_hours} {hours} of sun in the forecast.",
            "The sun has the day - roughly {sun_hours} {hours} of it.",
            "Sunshine for most of the day - about {sun_hours} {hours}.",
            "A day with the sun in charge: around {sun_hours} {hours} of it.",
        ],
        "de": [
            "Rund {sun_hours} {hours} Sonne heute. Das Licht hat den Tag für sich.",
            "Ein heller Tag: etwa {sun_hours} {hours} Sonne in der Vorhersage.",
            "Die Sonne hat heute das Sagen - ungefähr {sun_hours} {hours}.",
            "Sonnenschein fast den ganzen Tag - rund {sun_hours} {hours}.",
            "Ein Tag, an dem die Sonne regiert: etwa {sun_hours} {hours}.",
        ],
    },
    "sunny_today.winter": {
        "en": [
            "Winter sun today, about {sun_hours} {hours} of it. Low, warm on the face, and golden all day long.",
            "A clear winter day: around {sun_hours} {hours} of sunshine. These are the days that carry you through.",
            "Sun in the cold season - roughly {sun_hours} {hours}. The light is low and long, and everything glows in it.",
            "About {sun_hours} {hours} of sun today. In this part of the year, that is a gift.",
            "Around {sun_hours} {hours} of sun today. The low sun lights up rooms right to the back wall.",
            "A bright day: about {sun_hours} {hours} of sunshine. Long shadows, clear air, and colour back in everything.",
            "Sunshine for about {sun_hours} {hours} today. The sunny side of the street is the warm one.",
        ],
        "de": [
            "Wintersonne heute, rund {sun_hours} {hours}. Tief, warm im Gesicht, und den ganzen Tag golden.",
            "Ein klarer Wintertag: etwa {sun_hours} {hours} Sonnenschein. Solche Tage tragen einen durch.",
            "Sonne in der kalten Jahreszeit - ungefähr {sun_hours} {hours}. Das Licht ist tief und lang, und alles leuchtet darin.",
            "Rund {sun_hours} {hours} Sonne heute. In diesem Teil des Jahres ist das ein Geschenk.",
            "Rund {sun_hours} {hours} Sonne heute. Die tiefe Sonne leuchtet die Zimmer bis zur Rückwand aus.",
            "Ein heller Tag: etwa {sun_hours} {hours} Sonnenschein. Lange Schatten, klare Luft, und alles hat wieder Farbe.",
            "Etwa {sun_hours} {hours} Sonnenschein heute. Die Sonnenseite der Strasse ist die warme.",
        ],
    },

    # {temp_high} {since_date}
    "warmest_since": {
        "en": [
            "Up to {temp_high} today - the warmest day since {since_date}.",
            "{temp_high} at its warmest: no day has been this mild since {since_date}.",
            "The mildest day since {since_date}, reaching about {temp_high}. The air feels different.",
            "You have to go back to {since_date} for a day as warm as today's {temp_high}.",
            "{temp_high} today. The last time the thermometer got this far was {since_date}.",
        ],
        "de": [
            "Bis {temp_high} heute - der wärmste Tag seit dem {since_date}.",
            "{temp_high} in der Spitze: So mild war es seit dem {since_date} nicht mehr.",
            "Der mildeste Tag seit dem {since_date}, mit rund {temp_high}. Die Luft fühlt sich anders an.",
            "Um einen so warmen Tag wie heute mit {temp_high} zu finden, musst du bis zum {since_date} zurückgehen.",
            "{temp_high} heute. So weit kam das Thermometer zuletzt am {since_date}.",
        ],
    },
    "warmest_since.month": {
        "en": [
            "Up to {temp_high} today - the warmest day in more than a month.",
            "No day in the past month has been this warm: {temp_high} at the peak.",
            "{temp_high} today. You would have to go back more than a month for a milder day.",
            "{temp_high} today - nothing in the past month came close.",
        ],
        "de": [
            "Bis {temp_high} heute - der wärmste Tag seit über einem Monat.",
            "Kein Tag im letzten Monat war so warm: {temp_high} in der Spitze.",
            "{temp_high} heute. Für einen milderen Tag müsstest du über einen Monat zurückgehen.",
            "{temp_high} heute - nichts im letzten Monat kam da heran.",
        ],
    },

    # {uv}
    "uv_strength": {
        "en": [
            "UV index {uv} at midday. The sun has real strength again - you can feel it on your skin.",
            "The midday sun reaches UV {uv} today. Winter sun does not usually manage that; this one does.",
            "UV {uv}: the sun is strong enough again to warm a wall, and your face.",
            "UV index {uv} today. A sun that strong is no longer a winter sun.",
            "At midday the UV index reaches {uv}. On a sheltered bench the sun warms properly again.",
        ],
        "de": [
            "UV-Index {uv} am Mittag. Die Sonne hat wieder echte Kraft - man spürt sie auf der Haut.",
            "Die Mittagssonne erreicht heute UV {uv}. Das schafft Wintersonne normalerweise nicht; diese schon.",
            "UV {uv}: Die Sonne ist wieder stark genug, um eine Mauer zu wärmen, und dein Gesicht.",
            "UV-Index {uv} heute. Eine so kräftige Sonne ist keine Wintersonne mehr.",
            "Am Mittag erreicht der UV-Index {uv}. Auf einer geschützten Bank wärmt die Sonne wieder richtig.",
        ],
    },

    # {week_hours} {past_week_hours}
    "sunny_week": {
        "en": [
            "The week ahead has about {week_hours} hours of sun in the forecast, against {past_week_hours} in the week behind.",
            "A brighter week is coming: around {week_hours} hours of sunshine, where the last one had {past_week_hours}.",
            "{week_hours} hours of sun forecast for the next seven days. The last seven managed {past_week_hours}.",
            "Around {week_hours} hours of sun in the next seven days, up from {past_week_hours} in the last seven. A week to look forward to.",
            "The forecast has turned brighter: about {week_hours} hours of sunshine this coming week, compared with {past_week_hours} last week.",
        ],
        "de": [
            "Die kommende Woche hat rund {week_hours} Sonnenstunden in der Vorhersage, gegenüber {past_week_hours} in der letzten.",
            "Eine hellere Woche kommt: etwa {week_hours} Stunden Sonne, die letzte hatte {past_week_hours}.",
            "{week_hours} Sonnenstunden sind für die nächsten sieben Tage angesagt. Die letzten sieben schafften {past_week_hours}.",
            "Rund {week_hours} Sonnenstunden in den nächsten sieben Tagen, nach {past_week_hours} in den letzten sieben. Eine Woche zum Vorfreuen.",
            "Die Vorhersage ist heller geworden: etwa {week_hours} Stunden Sonnenschein in der kommenden Woche, gegenüber {past_week_hours} in der letzten.",
        ],
    },

    # (none)
    "fog": {
        "en": [
            "Fog today. Above it - often only a few hundred metres up - the sun is usually out.",
            "Everything is soft-edged today. Fog like this often lifts by midday, or sits below clear sky on the hills.",
            "A fog day: quiet, close and calm. If you can get a little higher, there is a fair chance of sun above it.",
            "Fog today: the world shrinks to a few streets, and the light turns soft and silver.",
            "Fog today. Trees and houses come out of it one at a time, like a drawing being finished.",
            "A foggy day. Spider webs and bare twigs carry rows of drops - fog shows what is usually invisible.",
        ],
        "de": [
            "Heute Nebel. Darüber - oft nur ein paar hundert Meter höher - scheint meistens die Sonne.",
            "Alles hat heute weiche Kanten. Solcher Nebel löst sich oft bis Mittag auf oder liegt unter klarem Himmel auf den Hügeln.",
            "Ein Nebeltag: gedämpft, nah und ruhig. Wer etwas höher kommt, hat gute Chancen auf Sonne darüber.",
            "Nebel heute: Die Welt schrumpft auf ein paar Strassen, und das Licht wird weich und silbern.",
            "Nebel heute. Bäume und Häuser treten einzeln daraus hervor, wie eine Zeichnung, die gerade fertig wird.",
            "Ein Nebeltag. Spinnweben und kahle Zweige tragen Tropfenreihen - der Nebel zeigt, was sonst unsichtbar ist.",
        ],
    },
    "fog.alpine": {
        "en": [
            "Fog today. Up here that is often cloud passing through - it can clear as fast as it came.",
            "Fog on the mountain. When it tears open, the view is all the sharper for it.",
            "In the fog today. Somewhere above or below there is sun; the layers shift quickly at this height.",
        ],
        "de": [
            "Heute Nebel. Hier oben sind das oft durchziehende Wolken - sie können so schnell verschwinden, wie sie kamen.",
            "Nebel am Berg. Wenn er aufreisst, ist die Sicht umso klarer.",
            "Im Nebel heute. Irgendwo darüber oder darunter scheint die Sonne; die Schichten wechseln in dieser Höhe schnell.",
        ],
    },

    # {temp_low}
    "frost_clear": {
        "en": [
            "Frost overnight, down to {temp_low}, then sun. Cold and bright is the best kind of winter day.",
            "{temp_low} this morning, and clear. The frost will sparkle while the sun is low.",
            "A frosty start at {temp_low}, with sun to follow. Crunching grass, clear air, long shadows.",
            "Frost and sunshine: {temp_low} overnight, blue sky by day. The cold looks its best like this.",
            "Down to {temp_low} last night, and now the sun. Breath clouds, bright air, white roofs.",
        ],
        "de": [
            "Frost in der Nacht, bis {temp_low}, dann Sonne. Kalt und hell ist die beste Sorte Wintertag.",
            "{temp_low} am Morgen, und klar. Der Reif glitzert, solange die Sonne tief steht.",
            "Ein frostiger Start mit {temp_low}, danach Sonne. Knirschendes Gras, klare Luft, lange Schatten.",
            "Frost und Sonnenschein: {temp_low} in der Nacht, tagsüber blauer Himmel. So sieht die Kälte am schönsten aus.",
            "Bis {temp_low} letzte Nacht, und jetzt die Sonne. Atemwolken, helle Luft, weisse Dächer.",
        ],
    },

    # {temp_low}
    "frost": {
        "en": [
            "Frost this morning, down to {temp_low}. Roofs, cars and grass stay white until the day warms up.",
            "{temp_low} overnight. The puddles have a skin of ice, and the air smells clean.",
            "A frosty night at {temp_low}. It is the kind of cold that makes coming back inside a pleasure.",
            "Down to {temp_low} last night. Hoarfrost outlines every blade of grass and every fence wire.",
            "A frost night, down to {temp_low}. On mornings like this the air is the clearest of the week.",
        ],
        "de": [
            "Frost am Morgen, bis {temp_low}. Dächer, Autos und Gras bleiben weiss, bis der Tag wärmer wird.",
            "{temp_low} in der Nacht. Die Pfützen tragen eine Eishaut, und die Luft riecht sauber.",
            "Eine Frostnacht mit {temp_low}. Die Sorte Kälte, die das Heimkommen zum Vergnügen macht.",
            "Bis {temp_low} letzte Nacht. Der Reif zeichnet jeden Grashalm und jeden Zaundraht nach.",
            "Eine Frostnacht, bis {temp_low}. An solchen Morgen ist die Luft so klar wie sonst die ganze Woche nicht.",
        ],
    },
    "frost.first": {
        "en": [
            "The first frost of the season: {temp_low} overnight. White grass and white roofs make the morning brighter.",
            "{temp_low} last night - the first frost of the season. It is what sweetens the sloes and the Brussels sprouts.",
            "First frost, {temp_low} at the coldest. Time for the good gloves.",
            "The season's first frost: {temp_low} last night. The gardens get their first silver edges.",
        ],
        "de": [
            "Der erste Frost der Saison: {temp_low} in der Nacht. Weisses Gras und weisse Dächer machen den Morgen heller.",
            "{temp_low} letzte Nacht - der erste Frost der Saison. Er macht die Schlehen und den Rosenkohl süss.",
            "Erster Frost, {temp_low} in der kältesten Stunde. Zeit für die guten Handschuhe.",
            "Der erste Frost der Saison: {temp_low} letzte Nacht. Die Gärten bekommen ihre ersten silbernen Ränder.",
        ],
    },

    # {temp_high}
    "mild_day": {
        "en": [
            "Up to {temp_high} today. A day to leave the jacket open and stay out a little longer.",
            "{temp_high} at this time of year: mild enough for a coffee outside, with a coat on.",
            "A mild day, up to {temp_high}. Good for a long walk with no hurry to get back.",
            "{temp_high} today. A day like this, so late in the year, is a small bonus.",
            "{temp_high} today: a day to open the windows and air the house through.",
        ],
        "de": [
            "Bis {temp_high} heute. Ein Tag für die offene Jacke und ein bisschen länger draussen.",
            "{temp_high} um diese Jahreszeit: mild genug für einen Kaffee draussen, mit Mantel.",
            "Ein milder Tag, bis {temp_high}. Gut für einen langen Spaziergang, ohne Eile heimzukommen.",
            "{temp_high} heute. So ein Tag, so spät im Jahr, ist eine kleine Zugabe.",
            "{temp_high} heute: ein Tag, um die Fenster aufzumachen und das Haus durchzulüften.",
        ],
    },

    # (none)
    "rainy_day": {
        "en": [
            "Rain today. A good day for the things that happen indoors: soup on the stove, a book, a long phone call.",
            "A rainy day, and nothing outside needs you. Days like this are what warm rooms are for.",
            "A wet day. Rain on the window is one of the better sounds to read by.",
            "Plenty of rain today. The cinema, the sauna and the sofa were all made for this.",
            "A rainy day. Good weather for the slow jobs: sorting photos, baking, finishing that puzzle.",
        ],
        "de": [
            "Heute regnet es. Ein guter Tag für alles, was drinnen passiert: Suppe auf dem Herd, ein Buch, ein langes Telefonat.",
            "Ein Regentag, und draussen braucht dich nichts. Für solche Tage gibt es warme Zimmer.",
            "Ein nasser Tag. Regen am Fenster gehört zu den besseren Geräuschen zum Lesen.",
            "Viel Regen heute. Kino, Sauna und Sofa sind dafür gemacht.",
            "Ein Regentag. Gutes Wetter für die langsamen Dinge: Fotos sortieren, backen, das Puzzle fertig machen.",
        ],
    },

    # {temp_change}
    "warming": {
        "en": [
            "The thermometer is climbing this week - about {temp_change}°C warmer by the end. The air is softening.",
            "Milder days are on the way: around {temp_change}°C more by the end of the week.",
            "This week's forecast reads like a staircase going up: {temp_change}°C of warmth ahead.",
            "Warmer air is moving in: the second half of the week runs about {temp_change}°C milder than the first.",
            "The forecast is softening. In a few days it is around {temp_change}°C warmer.",
        ],
        "de": [
            "Das Thermometer klettert diese Woche - am Ende rund {temp_change}°C wärmer. Die Luft wird milder.",
            "Mildere Tage sind unterwegs: etwa {temp_change}°C mehr bis Ende der Woche.",
            "Die Vorhersage gleicht einer Treppe nach oben: {temp_change}°C mehr Wärme liegen vor dir.",
            "Wärmere Luft zieht heran: Die zweite Wochenhälfte ist rund {temp_change}°C milder als die erste.",
            "Die Vorhersage wird milder. In ein paar Tagen sind es etwa {temp_change}°C mehr.",
        ],
    },

    # {streak_days} {days}
    "sunny_streak": {
        "en": [
            "{streak_days} sunny {days} in a row, starting today. A proper stretch of light.",
            "The forecast is generous: {streak_days} {days} of sunshine ahead. Something to plan around.",
            "Sun today, tomorrow and beyond - {streak_days} {days} of it. Streaks like this deserve to be used.",
            "{streak_days} {days} of sunshine in a row, starting today. Good weather to get used to.",
            "{streak_days} {days} of sun in a row from today. Plans for outside can be made with confidence.",
        ],
        "de": [
            "{streak_days} sonnige {days} am Stück, ab heute. Eine richtige Schönwetterphase.",
            "Die Vorhersage ist grosszügig: {streak_days} {days} Sonne liegen vor dir. Da lässt sich etwas planen.",
            "Sonne heute, morgen und darüber hinaus - {streak_days} {days} lang. So eine Serie will genutzt werden.",
            "{streak_days} {days} Sonnenschein am Stück, ab heute. Daran kann man sich gewöhnen.",
            "{streak_days} {days} Sonne am Stück ab heute. Pläne für draussen kann man jetzt getrost machen.",
        ],
    },

    # {sun_hours} {hours}
    "some_sun": {
        "en": [
            "Even today the sun gets through for about {sun_hours} {hours}. It is still there.",
            "Not a bright day, but around {sun_hours} {hours} of sun are in it. Keep an eye out for the gaps.",
            "The sun is not gone, just busy: about {sun_hours} {hours} of it today, between the clouds.",
            "A grey day with gaps in it: about {sun_hours} {hours} of sun will get through.",
            "Even on a day like this, the sun finds about {sun_hours} {hours}. Look up now and then.",
        ],
        "de": [
            "Selbst heute kommt die Sonne rund {sun_hours} {hours} durch. Sie ist noch da.",
            "Kein heller Tag, aber etwa {sun_hours} {hours} Sonne stecken darin. Achte auf die Lücken.",
            "Die Sonne ist nicht weg, nur beschäftigt: heute ungefähr {sun_hours} {hours}, zwischen den Wolken.",
            "Ein grauer Tag mit Lücken: Etwa {sun_hours} {hours} Sonne kommen durch.",
            "Selbst an so einem Tag findet die Sonne rund {sun_hours} {hours}. Schau ab und zu hinauf.",
        ],
    },

    # (none)
    "weekend_sunny": {
        "en": [
            "The weekend looks sunny, both days. Worth keeping some of it free for being outside.",
            "Saturday and Sunday both have sun in the forecast. Good timing.",
            "Something for the weekend: sunshine on both days.",
            "The forecast has kept the sun for the weekend. Both days look bright.",
            "Both weekend days look sunny. Good for a longer walk, or a train ride somewhere with a view.",
        ],
        "de": [
            "Das Wochenende sieht sonnig aus, an beiden Tagen. Es lohnt sich, etwas davon fürs Draussensein freizuhalten.",
            "Samstag und Sonntag haben beide Sonne in der Vorhersage. Gut getroffen.",
            "Etwas fürs Wochenende: Sonnenschein an beiden Tagen.",
            "Die Vorhersage hat sich die Sonne fürs Wochenende aufgespart. Beide Tage sehen hell aus.",
            "Beide Wochenendtage sehen sonnig aus. Gut für einen längeren Spaziergang oder eine Zugfahrt an einen Ort mit Aussicht.",
        ],
    },

    # -- nature, tied to measurements -----------------------------------------

    # {temp_high}
    "bees": {
        "en": [
            "Up to {temp_high} and sunny: warm enough for the first bees. Watch the crocuses and willow catkins.",
            "{temp_high} in the sun today - the bumblebee queens are out looking for nest sites.",
            "Bee weather: {temp_high} and sunshine. The first ones are working the early flowers.",
            "{temp_high} and sun: honeybees leave the hive from about ten degrees. Today they are flying.",
            "Warm enough for wings: at {temp_high} in the sun, the first bees and hoverflies are on the hazel and the snowdrops.",
        ],
        "de": [
            "Bis {temp_high} und sonnig: warm genug für die ersten Bienen. Schau bei den Krokussen und Weidenkätzchen.",
            "{temp_high} an der Sonne heute - die Hummelköniginnen sind auf Nistplatzsuche.",
            "Bienenwetter: {temp_high} und Sonnenschein. Die ersten fliegen schon die frühen Blüten an.",
            "{temp_high} und Sonne: Ab etwa zehn Grad verlassen die Honigbienen den Stock. Heute fliegen sie.",
            "Warm genug zum Fliegen: Bei {temp_high} in der Sonne sitzen die ersten Bienen und Schwebfliegen auf Hasel und Schneeglöckchen.",
        ],
    },

    # (none)
    "toads": {
        "en": [
            "Mild and wet: on evenings like this the toads set off for their ponds. Watch the roads near water.",
            "Above five degrees and raining - toad migration weather. In many places volunteers carry them across the roads.",
            "A mild, damp evening. This is when frogs and toads move to the water where they were born.",
            "A mild, wet night ahead. The first toads and frogs use nights like this to cross to their spawning ponds.",
            "Rain and mild air after dark: amphibian weather. Drive slowly near ponds and woods tonight.",
        ],
        "de": [
            "Mild und nass: An solchen Abenden machen sich die Kröten auf den Weg zu ihren Teichen. Vorsicht auf Strassen in Wassernähe.",
            "Über fünf Grad und Regen - Krötenwanderwetter. Vielerorts tragen Freiwillige sie über die Strassen.",
            "Ein milder, feuchter Abend. Jetzt wandern Frösche und Kröten zu dem Gewässer, in dem sie geboren wurden.",
            "Eine milde, nasse Nacht steht bevor. Die ersten Kröten und Frösche nutzen solche Nächte für den Weg zu ihren Laichgewässern.",
            "Regen und milde Luft nach Einbruch der Dunkelheit: Amphibienwetter. Fahr heute Abend langsam in der Nähe von Weihern und Wäldern.",
        ],
    },

    # (none) - rare on purpose, see POLLEN_EVERY_DAYS in uplift_engine
    "pollen.alder": {
        "en": [
            "Alder pollen is in the air. Hard on hay fever, but a sure sign: the trees have started their spring.",
            "The alders are flowering - their pollen is measurable in the air today. Spring is literally in the air.",
        ],
        "de": [
            "Erlenpollen sind in der Luft. Hart für Allergiker, aber ein sicheres Zeichen: Die Bäume haben ihren Frühling begonnen.",
            "Die Erlen blühen - ihre Pollen sind heute messbar in der Luft. Der Frühling liegt buchstäblich in der Luft.",
        ],
    },
    "pollen.birch": {
        "en": [
            "Birch pollen is flying. Sorry, hay fever sufferers - but the birches are in full spring.",
            "The birches are in flower; their pollen is in the air today. Spring is well and truly here.",
        ],
        "de": [
            "Birkenpollen fliegen. Pech für Allergiker - aber die Birken sind mitten im Frühling.",
            "Die Birken blühen, ihre Pollen sind heute in der Luft. Der Frühling ist endgültig da.",
        ],
    },
    "pollen.grass": {
        "en": [
            "Grass pollen in the air: the meadows are in full flower. Early summer has arrived.",
            "The grasses are flowering - you can measure it in the air. The meadows are at their tallest.",
        ],
        "de": [
            "Gräserpollen in der Luft: Die Wiesen stehen in voller Blüte. Der Frühsommer ist da.",
            "Die Gräser blühen - messbar in der Luft. Die Wiesen sind jetzt am höchsten.",
        ],
    },

    # -- customs, Zurich and Aargau only --------------------------------------

    # {days_until} {when} {days} {days_dat}
    "custom.sechselaeuten_soon": {
        "en": [
            "Sechseläuten is {when}. The Böögg is waiting on his pyre - and with him, winter's end.",
            "{days_until} more {days} until Sechseläuten. Zurich gets ready to burn winter in effigy.",
            "Sechseläuten {when}: the guilds are polishing their costumes, and the snowman's days are numbered.",
        ],
        "de": [
            "Sechseläuten ist {when}. Der Böögg wartet auf seinem Scheiterhaufen - und mit ihm das Ende des Winters.",
            "Noch {days_until} {days} bis zum Sechseläuten. Zürich macht sich bereit, den Winter zu verbrennen.",
            "Sechseläuten {when}: Die Zünfte putzen ihre Kostüme, und die Tage des Schneemanns sind gezählt.",
        ],
    },
    "custom.sechselaeuten": {
        "en": [
            "Today is Sechseläuten. At six the Böögg burns - and the faster his head explodes, the better the summer, so they say.",
            "Sechseläuten in Zurich: the guilds parade, and at six o'clock winter goes up in smoke on the Sechseläutenplatz.",
            "Böögg day. Whatever the timing says about the summer, winter is officially over in Zurich tonight.",
        ],
        "de": [
            "Heute ist Sechseläuten. Um sechs brennt der Böögg - und je schneller sein Kopf explodiert, desto schöner der Sommer, sagt man.",
            "Sechseläuten in Zürich: Die Zünfte ziehen durch die Stadt, und um sechs Uhr geht der Winter auf dem Sechseläutenplatz in Rauch auf.",
            "Böögg-Tag. Was auch immer die Zeit über den Sommer sagt: Heute Abend ist der Winter in Zürich offiziell vorbei.",
        ],
    },
    "custom.knabenschiessen": {
        "en": [
            "Knabenschiessen weekend in Zurich: young sharpshooters at the Albisgütli, and the big fair around them.",
            "It is Knabenschiessen. The Albisgütli fair is on - one of Zurich's best late-summer traditions.",
        ],
        "de": [
            "Knabenschiessen-Wochenende in Zürich: die jungen Schützinnen und Schützen im Albisgütli, und rundherum die grosse Chilbi.",
            "Es ist Knabenschiessen. Die Chilbi im Albisgütli läuft - eine der schönsten Zürcher Spätsommertraditionen.",
        ],
    },
    "custom.samichlaus": {
        "en": [
            "6 December, Samichlaus. Mandarins, nuts and gingerbread - and a reminder that the darkest weeks have their own warmth.",
            "Samichlaus day. Somewhere tonight a child is reciting a verse in exchange for peanuts and a Grittibänz.",
            "It is Samichlaus. The evening is dark early, and that is exactly when the lanterns and bells come out.",
        ],
        "de": [
            "6. Dezember, Samichlaus. Mandarinen, Nüsse und Lebkuchen - und eine Erinnerung daran, dass die dunkelsten Wochen ihre eigene Wärme haben.",
            "Samichlaus-Tag. Irgendwo sagt heute Abend ein Kind ein Versli auf, für Erdnüsse und einen Grittibänz.",
            "Es ist Samichlaus. Der Abend wird früh dunkel, und genau dann kommen die Laternen und Glocken.",
        ],
    },
    "custom.christmas_markets": {
        "en": [
            "The Christmas markets are open: mulled wine, roasted almonds and a lot of light against a lot of dark.",
            "Christmas market season. The darkest weeks of the year, lit up on purpose.",
            "Lights strung over the streets, stalls on the squares. This is how a town answers the long nights.",
            "The Christmas markets are on. In cold air the smell of roasted chestnuts and mulled wine carries a long way.",
        ],
        "de": [
            "Die Weihnachtsmärkte sind offen: Glühwein, gebrannte Mandeln und viel Licht gegen viel Dunkel.",
            "Weihnachtsmarkt-Zeit. Die dunkelsten Wochen des Jahres, mit Absicht erleuchtet.",
            "Lichterketten über den Gassen, Stände auf den Plätzen. So antwortet eine Stadt auf die langen Nächte.",
            "Die Weihnachtsmärkte laufen. In der kalten Luft trägt der Duft von Marroni und Glühwein weit.",
        ],
    },
}


# ===== Nature =====
#
# The companion line: region -> month -> weather tag -> language. "any" holds
# on every day of the month; the other tags only when that weather is
# measured today (see _conditions in uplift_engine):
#   sunny, grey, wet, frost, snow, warm (15°C and up), cold (3°C or less)
#
# "alpine" is from about 800 m up. Spring comes weeks later there, snow
# stays, and the valley is something you look down on.

NATURE = {
    "lowland": {
        1: {
            "any": {
                "en": [
                    "Snowdrops are up in the sheltered corners of gardens and parks.",
                    "Hazel catkins are lengthening - the first pollen of the year is on its way.",
                    "Great tits have started their two-note call on the milder mornings.",
                    "Robins sing from bare branches, holding their ground through the winter.",
                    "Without leaves, the buzzards on the fence posts are easy to spot.",
                    "Moss and lichen glow green on walls and tree trunks - winter is their season.",
                    "Witch hazel is flowering in gardens - yellow threads on bare twigs, in the middle of winter.",
                    "Wrens sing all winter from the hedges - a huge voice for a tiny bird.",
                    "Foxes are calling at night around now. January is their mating season.",
                    "Goosanders, tufted ducks and coots winter on the lakes in their thousands.",
                ],
                "de": [
                    "In geschützten Ecken von Gärten und Parks stehen die Schneeglöckchen.",
                    "Die Haselkätzchen strecken sich - der erste Pollen des Jahres ist unterwegs.",
                    "An milderen Morgen ruft die Kohlmeise wieder zweisilbig.",
                    "Rotkehlchen singen von kahlen Ästen und halten ihr Revier durch den Winter.",
                    "Ohne Laub sind die Mäusebussarde auf den Zaunpfählen gut zu sehen.",
                    "Moos und Flechten leuchten grün an Mauern und Stämmen - der Winter ist ihre Saison.",
                    "In den Gärten blüht die Zaubernuss - gelbe Fäden an kahlen Zweigen, mitten im Winter.",
                    "Zaunkönige singen den ganzen Winter aus den Hecken - eine riesige Stimme für einen winzigen Vogel.",
                    "Füchse rufen jetzt in der Nacht. Im Januar ist ihre Paarungszeit.",
                    "Gänsesäger, Reiherenten und Blässhühner überwintern zu Tausenden auf den Seen.",
                ],
            },
            "frost": {
                "en": ["Hoarfrost turns every twig and spider web white. Look closely before the sun takes it.",
                       "Frozen puddles, crunching grass: frost makes the ordinary walk worth doing."],
                "de": ["Raureif macht jeden Zweig und jedes Spinnennetz weiss. Schau genau hin, bevor die Sonne ihn holt.",
                       "Gefrorene Pfützen, knirschendes Gras: Frost macht den gewöhnlichen Spaziergang lohnend."],
            },
            "sunny": {
                "en": ["On sun-warmed walls the odd fly or ladybird comes out to bask."],
                "de": ["An sonnenwarmen Mauern sonnt sich die eine oder andere Fliege, manchmal auch ein Marienkäfer."],
            },
            "snow": {
                "en": ["Fresh snow shows who was out last night: fox, hare, deer and birds all leave their tracks."],
                "de": ["Frischer Schnee zeigt, wer letzte Nacht unterwegs war: Fuchs, Hase, Reh und Vögel hinterlassen ihre Spuren."],
            },
        },
        2: {
            "any": {
                "en": [
                    "Hazel and alder are flowering; the first pollen is already in the air.",
                    "Blackbirds are singing from the rooftops again around now.",
                    "Winter aconite and snowdrops are out wherever the ground has thawed.",
                    "Rooks and jackdaws are pairing up and inspecting last year's nests.",
                    "Woodpeckers are drumming - on bare trunks the sound carries a long way.",
                    "Buds are visibly swelling; the horse chestnut buds are already fat and sticky.",
                    "Song thrushes are back in voice - each phrase sung two or three times over.",
                    "The first skylarks return to the fields and sing high over the bare ground.",
                    "Crocus tips and the first leaves of the daffodils are pushing through.",
                    "Willow buds are splitting, showing the silver fur underneath.",
                ],
                "de": [
                    "Hasel und Erle blühen, der erste Pollen liegt schon in der Luft.",
                    "Die Amseln singen um diese Zeit wieder von den Dächern.",
                    "Winterlinge und Schneeglöckchen stehen überall dort, wo der Boden aufgetaut ist.",
                    "Saatkrähen und Dohlen finden sich paarweise und begutachten die alten Nester.",
                    "Die Spechte trommeln - an kahlen Stämmen trägt der Klang weit.",
                    "Die Knospen schwellen sichtbar; die der Rosskastanie sind schon dick und klebrig.",
                    "Die Singdrosseln singen wieder - jede Strophe zwei- oder dreimal wiederholt.",
                    "Die ersten Feldlerchen kehren auf die Felder zurück und singen hoch über dem kahlen Boden.",
                    "Krokusspitzen und die ersten Blätter der Osterglocken stossen durch.",
                    "Die Knospen der Salweide platzen auf und zeigen das silberne Fell darunter.",
                ],
            },
            "sunny": {
                "en": ["On sunny afternoons the first brimstone butterflies can be out - they overwinter as adults."],
                "de": ["An sonnigen Nachmittagen kann schon der Zitronenfalter fliegen - er überwintert als Falter."],
            },
            "wet": {
                "en": ["Rain on thawing ground: the soil smells again, for the first time in weeks."],
                "de": ["Regen auf auftauendem Boden: Die Erde riecht wieder, zum ersten Mal seit Wochen."],
            },
            "frost": {
                "en": ["Frost on the snowdrops - they droop in the cold and stand up again by midday."],
                "de": ["Frost auf den Schneeglöckchen - sie lassen in der Kälte die Köpfe hängen und stehen bis Mittag wieder auf."],
            },
            "snow": {
                "en": ["Snow on the first flowers: the snowdrops have seen this before and will be fine."],
                "de": ["Schnee auf den ersten Blüten: Die Schneeglöckchen kennen das und überstehen es."],
            },
        },
        3: {
            "any": {
                "en": [
                    "Crocuses are open across the parks and the first bees are on them.",
                    "Blackthorn is coming into flower along the field edges.",
                    "The first bumblebee queens are out hunting for nest sites.",
                    "Migrating birds are moving back through - cranes on the high routes.",
                    "Wild garlic is coming up in the damp woods. You smell it before you see it.",
                    "Blackbirds sing before sunrise now - the dawn chorus is filling out.",
                    "Chiffchaffs are back, calling their own name from the treetops.",
                    "Coltsfoot flowers on bare banks and verges - yellow before a single leaf.",
                    "Wood anemones are starting to open on the forest floor, before the trees take the light.",
                    "The willows are in full catkin, and loud with bees on a mild day.",
                    "White storks are returning to their nests.",
                ],
                "de": [
                    "In den Parks sind die Krokusse offen, und die ersten Bienen sitzen darauf.",
                    "An den Feldrändern fängt die Schlehe an zu blühen.",
                    "Die ersten Hummelköniginnen suchen nach Nistplätzen.",
                    "Der Vogelzug geht wieder nach Norden - Kraniche auf den hohen Routen.",
                    "In feuchten Wäldern kommt der Bärlauch. Man riecht ihn, bevor man ihn sieht.",
                    "Die Amseln singen jetzt vor Sonnenaufgang - das Morgenkonzert wird voller.",
                    "Die Zilpzalpe sind zurück und rufen ihren eigenen Namen aus den Baumkronen.",
                    "Huflattich blüht an kahlen Böschungen und Wegrändern - gelb, bevor ein einziges Blatt da ist.",
                    "Die Buschwindröschen beginnen am Waldboden zu blühen, bevor die Bäume das Licht nehmen.",
                    "Die Weiden stehen voll in Kätzchen und summen an milden Tagen vor Bienen.",
                    "Die Weissstörche kehren zu ihren Horsten zurück.",
                ],
            },
            "sunny": {
                "en": ["In the sun the first lizards come out onto warm stones."],
                "de": ["An der Sonne kommen die ersten Eidechsen auf warme Steine."],
            },
            "wet": {
                "en": ["Mild rain brings the frogs to the ponds - listen for them in the evening."],
                "de": ["Milder Regen bringt die Frösche an die Teiche - hör abends hin."],
            },
            "frost": {
                "en": ["A frosty morning in March: the cold does not last long now, the sun clears it by mid-morning."],
                "de": ["Ein frostiger Märzmorgen: Die Kälte hält nicht mehr lange, die Sonne vertreibt sie bis zum Vormittag."],
            },
            "warm": {
                "en": ["Fifteen degrees and more: the first T-shirt of the year is a possibility."],
                "de": ["Fünfzehn Grad und mehr: Das erste T-Shirt des Jahres liegt drin."],
            },
        },
        4: {
            "any": {
                "en": [
                    "The orchards are in blossom, which is a short and worthwhile window.",
                    "Dandelions are taking over the verges and the meadows are thickening.",
                    "Beech and birch are unfolding that brief, particular green.",
                    "Swallows are arriving back at last year's nesting sites.",
                    "The cuckoo is calling again in the woods - one of spring's most recognisable sounds.",
                    "Cowslips and wood anemones carpet the edges of the woods.",
                    "Blackcaps are back - a rich, fluting song from every thicket.",
                    "Wild cherries flower white along the forest edges before the woods turn green.",
                ],
                "de": [
                    "Die Obstgärten blühen. Ein kurzes Fenster, das sich lohnt.",
                    "Der Löwenzahn erobert die Wegränder, und die Wiesen werden dichter.",
                    "Buche und Birke entfalten dieses kurze, besondere Grün.",
                    "Die Schwalben kommen an den Nistplätzen vom Vorjahr wieder an.",
                    "Im Wald ruft wieder der Kuckuck - einer der bekanntesten Frühlingsklänge.",
                    "Schlüsselblumen und Buschwindröschen bedecken die Waldränder.",
                    "Die Mönchsgrasmücken sind zurück - ein voller, flötender Gesang aus jedem Gebüsch.",
                    "Die Vogelkirschen blühen weiss an den Waldrändern, bevor der Wald grün wird.",
                ],
            },
            "sunny": {
                "en": ["Sunny April afternoons bring out the first orange-tip butterflies along the hedges."],
                "de": ["Sonnige Aprilnachmittage locken die ersten Aurorafalter an die Hecken."],
            },
            "wet": {
                "en": ["April rain: everything green grows a little faster for it, almost fast enough to watch."],
                "de": ["Aprilregen: Alles Grüne wächst dadurch ein wenig schneller, fast zum Zuschauen."],
            },
            "warm": {
                "en": ["Warm enough to eat outside. The first evening on a terrace is one of the year's small events."],
                "de": ["Warm genug, um draussen zu essen. Der erste Abend auf einer Terrasse ist eines der kleinen Ereignisse des Jahres."],
            },
        },
        5: {
            "any": {
                "en": [
                    "Swifts are back, screaming through the evening skies.",
                    "Butterflies everywhere now - watch for painted ladies and commas.",
                    "May evenings stay light past nine. Use them.",
                    "Everything is growing, flowering or nesting. Peak activity.",
                    "Lilac and elderflower scent the evening air.",
                    "The meadows are in flower before the first hay cut - buttercups, sage, ox-eye daisies.",
                    "Hawthorn first, then dog rose and elder: the hedges flower one after another.",
                    "Young blackbirds and sparrows are out of the nest, begging loudly in the bushes.",
                ],
                "de": [
                    "Die Mauersegler sind zurück und jagen schreiend durch den Abendhimmel.",
                    "Schmetterlinge überall - achte auf Distelfalter und C-Falter.",
                    "Maiabende bleiben bis nach neun hell. Nutz sie.",
                    "Alles wächst, blüht oder brütet. Hochbetrieb in der Natur.",
                    "Flieder und Holunder parfümieren die Abendluft.",
                    "Die Wiesen blühen vor dem ersten Heuschnitt - Hahnenfuss, Salbei, Margeriten.",
                    "Zuerst der Weissdorn, dann Hundsrose und Holunder: Die Hecken blühen eine nach der anderen.",
                    "Junge Amseln und Spatzen sind ausgeflogen und betteln laut in den Büschen.",
                ],
            },
            "sunny": {
                "en": ["On warm May evenings you can sometimes hear cockchafers buzzing around the treetops."],
                "de": ["An warmen Maiabenden hört man manchmal Maikäfer um die Baumkronen brummen."],
            },
            "wet": {
                "en": ["After a May shower the whole garden smells green."],
                "de": ["Nach einem Mairegen riecht der ganze Garten grün."],
            },
            "warm": {
                "en": ["Warm evenings, and the first swims in the lake for the brave."],
                "de": ["Warme Abende, und für die Mutigen die ersten Bäder im See."],
            },
        },
        6: {
            "any": {
                "en": [
                    "Swifts are everywhere, feeding hard. Watch their aerial shows.",
                    "Roses are at their peak. Stop and smell them.",
                    "Bees work late into the evening on long June days.",
                    "Elderflower is out along the hedges - the smell of early summer.",
                    "Fireflies glow in the warm nights near woods and meadows.",
                    "The hay is being cut; the smell drifts over whole villages.",
                    "The lime trees are in flower; on warm evenings whole avenues smell of honey.",
                ],
                "de": [
                    "Mauersegler jagen überall. Schau ihren Flugkünsten zu.",
                    "Die Rosen sind auf dem Höhepunkt. Stehenbleiben und riechen.",
                    "Bienen arbeiten an langen Junitagen bis spät abends.",
                    "Der Holunder blüht an den Hecken - der Duft des Frühsommers.",
                    "In warmen Nächten leuchten an Waldrändern und Wiesen die Glühwürmchen.",
                    "Das Heu wird geschnitten; der Duft zieht über ganze Dörfer.",
                    "Die Linden blühen; an warmen Abenden duften ganze Alleen nach Honig.",
                ],
            },
            "warm": {
                "en": ["Warm nights: the windows stay open and the crickets keep singing."],
                "de": ["Warme Nächte: Die Fenster bleiben offen und die Grillen zirpen weiter."],
            },
            "wet": {
                "en": ["A summer shower, then steam rising off the warm streets."],
                "de": ["Ein Sommerschauer, dann dampft es von den warmen Strassen."],
            },
        },
        7: {
            "any": {
                "en": [
                    "Lavender and buddleia draw clouds of butterflies. Watch for peacocks.",
                    "July evenings are warm enough to sit out until ten.",
                    "Crickets chirp on warm nights - the summer soundtrack.",
                    "Wild strawberries are ripe in the forest clearings.",
                    "The swifts will leave soon. Appreciate them while they are here.",
                    "Apricots and berries are in season - summer you can eat.",
                    "Dragonflies and damselflies patrol every pond and stream.",
                ],
                "de": [
                    "Lavendel und Sommerflieder ziehen Schmetterlinge an. Achte auf das Tagpfauenauge.",
                    "Juliabende sind warm genug zum Draussensitzen bis um zehn.",
                    "Grillen zirpen in warmen Nächten - die Musik des Sommers.",
                    "An den Waldlichtungen sind die Walderdbeeren reif.",
                    "Die Mauersegler ziehen bald weg. Geniess sie, solange sie da sind.",
                    "Aprikosen und Beeren haben Saison - Sommer zum Essen.",
                    "Libellen patrouillieren an jedem Teich und Bach.",
                ],
            },
            "warm": {
                "en": ["On hot evenings the swifts scream low over the rooftops."],
                "de": ["An heissen Abenden jagen die Mauersegler kreischend über die Dächer."],
            },
            "wet": {
                "en": ["A thunderstorm clears the air - the evening after is often the best of the week."],
                "de": ["Ein Gewitter reinigt die Luft - der Abend danach ist oft der schönste der Woche."],
            },
        },
        8: {
            "any": {
                "en": [
                    "Blackberries are ripening along the paths. Free snacks on every walk.",
                    "August light has a golden quality, especially in the evening.",
                    "Apples are ripening in the old orchards.",
                    "Spiders build impressive webs now; morning dew makes them visible.",
                    "Late-summer meadows hum with grasshoppers and crickets.",
                    "Swallows are feeding their second brood, flying low over the meadows.",
                ],
                "de": [
                    "Entlang der Wege reifen die Brombeeren. Gratis-Znüni bei jedem Spaziergang.",
                    "Das Augustlicht ist golden, besonders am Abend.",
                    "In den alten Obstgärten reifen die Äpfel.",
                    "Spinnen bauen jetzt imposante Netze; der Morgentau macht sie sichtbar.",
                    "Spätsommerwiesen summen vor Heuschrecken und Grillen.",
                    "Die Schwalben füttern ihre zweite Brut und fliegen tief über die Wiesen.",
                ],
            },
            "warm": {
                "en": ["Warm lake water: August is the best month for a swim."],
                "de": ["Warmes Seewasser: Der August ist der beste Monat zum Schwimmen."],
            },
            "wet": {
                "en": ["After a warm rain, mushrooms appear almost overnight at the edges of the woods."],
                "de": ["Nach einem warmen Regen schiessen am Waldrand fast über Nacht Pilze hervor."],
            },
        },
        9: {
            "any": {
                "en": [
                    "September sun on the first turning leaves - the colour show begins.",
                    "Apples, pears and plums are ready. Harvest time.",
                    "Swallows gather on the wires before they leave. Watch for the flocks.",
                    "Mushrooms appear after rain. Check the forest edges.",
                    "The first grapes are being picked on the sunny slopes.",
                    "Morning dew on the spider webs turns every hedge into lace.",
                    "Ivy is flowering - one of the last big feasts of the year for bees and hoverflies.",
                    "Robins are singing again: a quieter autumn version of their spring song.",
                ],
                "de": [
                    "Septembersonne auf den ersten bunten Blättern - das Farbenspiel beginnt.",
                    "Äpfel, Birnen, Zwetschgen sind reif. Erntezeit.",
                    "Die Schwalben sammeln sich auf den Drähten, bevor sie ziehen. Achte auf die Schwärme.",
                    "Nach dem Regen kommen die Pilze. Schau an den Waldrändern.",
                    "An den sonnigen Hängen werden die ersten Trauben gelesen.",
                    "Morgentau auf den Spinnennetzen macht aus jeder Hecke Spitze.",
                    "Der Efeu blüht - eines der letzten grossen Festessen des Jahres für Bienen und Schwebfliegen.",
                    "Die Rotkehlchen singen wieder: eine leisere Herbstversion ihres Frühlingslieds.",
                ],
            },
            "warm": {
                "en": ["Warm September afternoons: summer is taking its time to leave."],
                "de": ["Warme Septembernachmittage: Der Sommer lässt sich Zeit mit dem Gehen."],
            },
        },
        10: {
            "any": {
                "en": [
                    "The autumn colours are building, week by week, towards their peak.",
                    "Squirrels are busy burying nuts for the winter.",
                    "On clear days you may hear migrating cranes or geese overhead.",
                    "Chestnuts are falling - the shiny ones in the parks, the edible ones in the woods.",
                    "Wherever there are vines, the leaves turn yellow and red after the harvest.",
                    "Walnuts are falling; the first ones taste the best.",
                ],
                "de": [
                    "Die Herbstfarben bauen sich auf, Woche für Woche bis zum Höhepunkt.",
                    "Eichhörnchen vergraben emsig Nüsse für den Winter.",
                    "An klaren Tagen hört man vielleicht ziehende Kraniche oder Gänse über sich.",
                    "Die Kastanien fallen - die glänzenden in den Parks, die essbaren im Wald.",
                    "Wo Reben stehen, färbt sich das Laub nach der Lese gelb und rot.",
                    "Die Baumnüsse fallen; die ersten schmecken am besten.",
                ],
            },
            "sunny": {
                "en": ["Low October sun through yellow leaves - the woods glow from inside."],
                "de": ["Tiefe Oktobersonne durch gelbes Laub - der Wald leuchtet von innen."],
            },
            "frost": {
                "en": ["The first frosts reveal the spider webs in the morning grass."],
                "de": ["Erster Frost macht Spinnennetze im Morgengras sichtbar."],
            },
            "warm": {
                "en": ["A warm October day - the butterflies on the last flowers are making the most of it too."],
                "de": ["Ein warmer Oktobertag - die Schmetterlinge auf den letzten Blüten nutzen ihn auch."],
            },
            "wet": {
                "en": ["Wet woods smell of mushrooms and leaves. Autumn's own perfume."],
                "de": ["Nasse Wälder riechen nach Pilzen und Laub. Das Parfum des Herbstes."],
            },
            "grey": {
                "en": ["On grey days the autumn colours glow even brighter - no harsh light to wash them out."],
                "de": ["An grauen Tagen leuchten die Herbstfarben noch stärker - kein hartes Licht wäscht sie aus."],
            },
        },
        11: {
            "any": {
                "en": [
                    "Rosehips and spindle berries hang bright in the bare hedges.",
                    "Starlings gather in large flocks before dusk and wheel over the fields.",
                    "Hazel catkins are already on the bushes, closed and waiting for February.",
                    "Next year's buds already sit on the beeches and chestnuts. The trees were ready before the leaves fell.",
                    "Hedgehogs have gone into their nests of leaves. A pile left in the garden is a winter home.",
                    "Fieldfares and redwings arrive from the north - winter visitors.",
                    "Fallen leaves reveal hidden paths and the shapes of the land.",
                    "Ducks from the north arrive on the lakes - tufted ducks, pochards, goldeneyes.",
                ],
                "de": [
                    "Hagebutten und Pfaffenhütchen leuchten in den kahlen Hecken.",
                    "Stare sammeln sich vor der Dämmerung in grossen Schwärmen und kreisen über den Feldern.",
                    "Die Haselkätzchen hängen schon an den Sträuchern, geschlossen, und warten auf den Februar.",
                    "Die Knospen fürs nächste Jahr sitzen schon an Buchen und Kastanien. Die Bäume waren bereit, bevor das Laub fiel.",
                    "Die Igel haben sich in ihre Laubnester zurückgezogen. Ein Laubhaufen im Garten ist ein Winterquartier.",
                    "Wacholderdrosseln und Rotdrosseln kommen aus dem Norden - Wintergäste.",
                    "Das gefallene Laub gibt versteckte Pfade und die Formen der Landschaft frei.",
                    "Auf den Seen kommen die Wintergäste aus dem Norden an - Reiher-, Tafel- und Schellenten.",
                ],
            },
            "grey": {
                "en": ["In the November grey, the last yellow leaves on the larches and birches shine like lamps."],
                "de": ["Im Novembergrau leuchten die letzten gelben Blätter an Lärchen und Birken wie Lampen."],
            },
            "frost": {
                "en": ["Frosty mornings: when the sun reaches them, the last leaves come down all at once."],
                "de": ["Frostige Morgen: Wenn die Sonne sie erreicht, fallen die letzten Blätter auf einmal."],
            },
            "sunny": {
                "en": ["A sunny November day is worth more than three in May. Bare branches let all of it through."],
                "de": ["Ein sonniger Novembertag ist mehr wert als drei im Mai. Kahle Äste lassen alles davon durch."],
            },
            "wet": {
                "en": ["Rain on the fallen leaves: the woods smell rich and earthy.",
                       "Mistle thrushes sing even in the rain.",
                       "After rain, the fungi season carries on at the forest edges."],
                "de": ["Regen auf dem Laub: Der Wald riecht satt und erdig.",
                       "Misteldrosseln singen sogar im Regen.",
                       "Nach dem Regen geht die Pilzsaison an den Waldrändern weiter."],
            },
        },
        12: {
            "any": {
                "en": [
                    "Robins sing all winter. They are staking out territory for spring.",
                    "Evergreen ivy and mistletoe are the only green in the bare trees.",
                    "Winter ducks from the north gather on the lakes and rivers.",
                    "Holly and ivy berries feed the blackbirds and thrushes through the cold.",
                    "Under the leaf litter, next spring's bulbs are already rooted and waiting.",
                    "The bare trees show their shapes now - every species has its own silhouette.",
                    "Hazel catkins hang ready on the bare bushes. In a mild winter the first open in January.",
                    "Tits, nuthatches and finches travel together in mixed flocks now. A feeder brings them close.",
                    "Tawny owls call on December nights. They are pairing up for the year ahead.",
                    "The buds on the trees are next spring already, packed small and sealed against the cold.",
                ],
                "de": [
                    "Rotkehlchen singen den ganzen Winter. Sie sichern ihr Revier für den Frühling.",
                    "Efeu und Misteln sind das einzige Grün in den kahlen Kronen.",
                    "Winterenten aus dem Norden sammeln sich auf Seen und Flüssen.",
                    "Stechpalmen- und Efeubeeren ernähren Amseln und Drosseln durch die Kälte.",
                    "Unter dem Laub warten die Zwiebeln des nächsten Frühlings schon bewurzelt.",
                    "Die kahlen Bäume zeigen jetzt ihre Formen - jede Art hat ihre eigene Silhouette.",
                    "Die Haselkätzchen hängen bereit an den kahlen Sträuchern. In einem milden Winter öffnen sich die ersten im Januar.",
                    "Meisen, Kleiber und Finken ziehen jetzt in gemischten Trupps umher. Ein Futterhaus holt sie nah heran.",
                    "Waldkäuze rufen in den Dezembernächten. Sie finden sich jetzt zu Paaren fürs nächste Jahr.",
                    "Die Knospen an den Bäumen sind schon der nächste Frühling, klein verpackt und gegen die Kälte versiegelt.",
                ],
            },
            "sunny": {
                "en": ["Every minute of December sun counts. It is worth being out in it."],
                "de": ["Jede Minute Dezembersonne zählt. Es lohnt sich, sie draussen zu geniessen."],
            },
            "frost": {
                "en": ["Hoarfrost on the hedges: a whole landscape drawn in white."],
                "de": ["Raureif an den Hecken: eine ganze Landschaft in Weiss gezeichnet."],
            },
            "snow": {
                "en": ["Snow on the evergreens - the robins look twice as red against it."],
                "de": ["Schnee auf den Nadelbäumen - die Rotkehlchen wirken davor doppelt so rot."],
            },
        },
    },

    "alpine": {
        1: {
            "any": {
                "en": [
                    "Snow cover holds the light - on clear days the brightness up here is hard to beat.",
                    "Chamois and ibex come lower in deep winter; look along the sunny slopes.",
                    "On mild days snow fleas - tiny springtails - dot the snow near the trees.",
                    "Ravens and alpine choughs work the ski areas for scraps.",
                    "Bearded vultures are already sitting on eggs - they breed in the middle of winter.",
                    "Ptarmigan dig into the powder snow to sleep. It is warmer in there than outside.",
                    "Crossbills breed even now, as long as the spruces carry cones.",
                ],
                "de": [
                    "Der Schnee hält das Licht - an klaren Tagen ist die Helligkeit hier oben kaum zu schlagen.",
                    "Gämsen und Steinböcke kommen im tiefen Winter weiter herunter; schau an den Sonnenhängen.",
                    "An milden Tagen sprenkeln Schneeflöhe - winzige Springschwänze - den Schnee bei den Bäumen.",
                    "Kolkraben und Alpendohlen suchen die Skigebiete nach Resten ab.",
                    "Die Bartgeier sitzen schon auf ihren Eiern - sie brüten mitten im Winter.",
                    "Schneehühner graben sich zum Schlafen in den Pulverschnee. Darin ist es wärmer als draussen.",
                    "Fichtenkreuzschnäbel brüten sogar jetzt, solange die Fichten Zapfen tragen.",
                ],
            },
            "sunny": {
                "en": ["On sunny days the south-facing slopes are already warm enough to sit out at lunchtime."],
                "de": ["An sonnigen Tagen sind die Südhänge mittags schon warm genug zum Draussensitzen."],
            },
            "snow": {
                "en": ["Fresh snow shows who passed in the night: mountain hare, fox, black grouse."],
                "de": ["Frischer Schnee zeigt, wer in der Nacht vorbeikam: Schneehase, Fuchs, Birkhuhn."],
            },
            "frost": {
                "en": ["Sparkling frost on the snow crust - the clearest air of the year."],
                "de": ["Glitzernder Reif auf dem Harsch - die klarste Luft des Jahres."],
            },
        },
        2: {
            "any": {
                "en": [
                    "On south-facing slopes the snow is starting to pull back around the rocks.",
                    "Hazel and alder are flowering down in the valleys; on warm days the pollen drifts up.",
                    "Great tits and nuthatches start calling again on bright mornings.",
                    "The sun clears the ridges a little earlier every week.",
                    "The sun is reaching valley villages again that lay in shadow for weeks.",
                    "Golden eagles are displaying over their territories - long dives and climbs on clear days.",
                    "Icicles grow on the south side of the roofs: thawing by day, freezing by night.",
                ],
                "de": [
                    "An Südhängen zieht sich der Schnee rund um die Felsen langsam zurück.",
                    "Unten in den Tälern blühen Hasel und Erle; an warmen Tagen treibt der Pollen herauf.",
                    "Kohlmeisen und Kleiber rufen an hellen Morgen wieder.",
                    "Die Sonne kommt jede Woche ein wenig früher über die Grate.",
                    "Die Sonne erreicht wieder Taldörfer, die wochenlang im Schatten lagen.",
                    "Steinadler zeigen ihre Balzflüge über dem Revier - lange Sturzflüge und Aufstiege an klaren Tagen.",
                    "An der Südseite der Dächer wachsen Eiszapfen: tagsüber taut es, nachts friert es.",
                ],
            },
            "sunny": {
                "en": ["Sunny days soften the snow by noon - a first taste of the spring snow to come."],
                "de": ["Sonnige Tage machen den Schnee bis Mittag weich - ein erster Vorgeschmack auf den Sulzschnee."],
            },
            "snow": {
                "en": ["Another layer of snow: the mountains are filling up their reserves for the spring rivers."],
                "de": ["Noch eine Schicht Schnee: Die Berge füllen ihre Vorräte für die Frühlingsflüsse auf."],
            },
        },
        3: {
            "any": {
                "en": [
                    "The snowpack is settling; below about a thousand metres it is losing ground fast.",
                    "Black grouse start displaying at dawn in the clearings near the treeline.",
                    "The first crocuses push up at the edge of the melting snow.",
                    "Meltwater is starting to run - the streams get louder week by week.",
                    "Marmots are still asleep, but not for long - the first come out through the snow in April.",
                    "Alpine choughs follow the skiers up; down in the valley the first coltsfoot is out.",
                    "Larch buds are swelling; in a few weeks the bare trees turn the lightest green on the mountain.",
                ],
                "de": [
                    "Die Schneedecke setzt sich; unterhalb von etwa tausend Metern verliert sie schnell an Boden.",
                    "Die Birkhähne beginnen in der Morgendämmerung zu balzen, auf Lichtungen nahe der Waldgrenze.",
                    "Am Rand des schmelzenden Schnees stossen die ersten Krokusse durch.",
                    "Das Schmelzwasser beginnt zu fliessen - die Bäche werden Woche für Woche lauter.",
                    "Die Murmeltiere schlafen noch, aber nicht mehr lange - die ersten kommen im April durch den Schnee.",
                    "Die Alpendohlen folgen den Skifahrern nach oben; unten im Tal blüht der erste Huflattich.",
                    "Die Lärchenknospen schwellen; in wenigen Wochen tragen die kahlen Bäume das hellste Grün am Berg.",
                ],
            },
            "sunny": {
                "en": ["Spring snow: frozen in the morning, soft by noon. The best time of the ski year."],
                "de": ["Sulzschnee: am Morgen gefroren, am Mittag weich. Die schönste Zeit des Skijahres."],
            },
            "snow": {
                "en": ["March snow does not stay long. It is a last coat of white before the melt."],
                "de": ["Märzschnee bleibt nicht lange. Er ist ein letzter weisser Anstrich vor der Schmelze."],
            },
        },
        4: {
            "any": {
                "en": [
                    "Marmots are coming out of hibernation on the alpine pastures.",
                    "The valley orchards are in blossom below, while the slopes above are still white.",
                    "Soldanella pushes its fringed bells right through the last snow.",
                    "The snow is retreating up the slopes, a little higher every week.",
                    "Ptarmigan and mountain hares are turning brown again as the snow retreats.",
                ],
                "de": [
                    "Auf den Alpweiden kommen die Murmeltiere aus dem Winterschlaf.",
                    "Unten im Tal blühen die Obstgärten, während die Hänge darüber noch weiss sind.",
                    "Das Alpenglöckchen schiebt seine gefransten Glocken direkt durch den letzten Schnee.",
                    "Der Schnee zieht sich die Hänge hinauf zurück, jede Woche ein Stück höher.",
                    "Schneehühner und Schneehasen werden wieder braun, während der Schnee zurückweicht.",
                ],
            },
            "sunny": {
                "en": ["On sunny days the meltwater roars - the mountains are emptying their winter."],
                "de": ["An sonnigen Tagen rauscht das Schmelzwasser - die Berge leeren ihren Winter."],
            },
            "wet": {
                "en": ["Rain up here washes the last snow off the meadows; the green follows within days."],
                "de": ["Regen hier oben wäscht den letzten Schnee von den Wiesen; das Grün folgt innert Tagen."],
            },
        },
        5: {
            "any": {
                "en": [
                    "Gentians and crocuses colour the pastures as the snow line climbs.",
                    "The larches turn a soft new green - the brightest green in the mountains.",
                    "The cuckoo and the first redstarts are back in the mountain villages.",
                    "The waterfalls are at their fullest with the snowmelt.",
                    "Pasqueflowers open their furry purple bells on the sunny slopes.",
                ],
                "de": [
                    "Enziane und Krokusse färben die Weiden, während die Schneegrenze steigt.",
                    "Die Lärchen werden zart neugrün - das hellste Grün in den Bergen.",
                    "Kuckuck und die ersten Rotschwänze sind zurück in den Bergdörfern.",
                    "Die Wasserfälle führen mit der Schneeschmelze am meisten Wasser.",
                    "Die Kuhschellen öffnen ihre pelzigen, violetten Glocken an den Sonnenhängen.",
                ],
            },
            "sunny": {
                "en": ["Warm sun on the high meadows - the marmots are out sunbathing too."],
                "de": ["Warme Sonne auf den hohen Wiesen - auch die Murmeltiere liegen an der Sonne."],
            },
        },
        6: {
            "any": {
                "en": [
                    "The alpine meadows are in full flower: gentian, globeflower, and soon the alpine roses.",
                    "The cows are going up to the alps - the season of cowbells begins.",
                    "Long evenings in the mountains: the peaks glow pink when the valley is already in shadow.",
                    "Snowfields linger in the gullies, bright against the new green.",
                    "Young marmots show themselves at the burrow entrances for the first time.",
                ],
                "de": [
                    "Die Alpwiesen stehen in voller Blüte: Enzian, Trollblume, bald die Alpenrosen.",
                    "Die Kühe ziehen auf die Alp - die Zeit der Kuhglocken beginnt.",
                    "Lange Abende in den Bergen: Die Gipfel glühen rosa, wenn das Tal schon im Schatten liegt.",
                    "In den Rinnen halten sich Schneefelder, hell vor dem neuen Grün.",
                    "Junge Murmeltiere zeigen sich zum ersten Mal am Eingang ihres Baus.",
                ],
            },
            "warm": {
                "en": ["Warm days up here are the best of both: summer heat in the valley, fresh air at this height."],
                "de": ["Warme Tage hier oben sind das Beste aus beidem: unten Sommerhitze, hier frische Luft."],
            },
            "wet": {
                "en": ["After the rain the meadows smell of herbs, and the clouds hang in the valleys below."],
                "de": ["Nach dem Regen duften die Wiesen nach Kräutern, und die Wolken hängen unten in den Tälern."],
            },
        },
        7: {
            "any": {
                "en": [
                    "The alpine roses colour the slopes red.",
                    "Edelweiss and alpine asters are flowering on the rocky ground higher up.",
                    "Cowbells, hay and wild thyme - the sound and smell of an alpine summer.",
                    "Bilberries are ripening on the slopes.",
                    "Glacier streams run milky and loud in the afternoon warmth.",
                ],
                "de": [
                    "Die Alpenrosen färben die Hänge rot.",
                    "Weiter oben blühen auf steinigem Boden Edelweiss und Alpenastern.",
                    "Kuhglocken, Heu und wilder Thymian - der Klang und Duft eines Alpsommers.",
                    "An den Hängen reifen die Heidelbeeren.",
                    "Die Gletscherbäche fliessen am Nachmittag milchig und laut.",
                ],
            },
            "sunny": {
                "en": ["Clear mornings up here start cool and blue - the best hours for a hike."],
                "de": ["Klare Morgen hier oben beginnen kühl und blau - die besten Stunden für eine Wanderung."],
            },
            "wet": {
                "en": ["A summer storm in the mountains passes quickly; the air afterwards is like glass."],
                "de": ["Ein Sommergewitter in den Bergen zieht schnell vorbei; die Luft danach ist wie Glas."],
            },
        },
        8: {
            "any": {
                "en": [
                    "Bilberries and wild raspberries are ripe along the trails.",
                    "The hay is in; the meadows are cut short and smell sweet.",
                    "Marmots are fattening up for winter, whistling from the rocks.",
                    "Late-summer light on the peaks is warm and golden in the evening.",
                    "The stone pine cones are ripening, and the nutcrackers are already harvesting.",
                ],
                "de": [
                    "Entlang der Wege sind Heidelbeeren und Waldhimbeeren reif.",
                    "Das Heu ist eingebracht; die Wiesen sind kurz geschnitten und duften süss.",
                    "Die Murmeltiere fressen sich Winterspeck an und pfeifen von den Felsen.",
                    "Das Spätsommerlicht auf den Gipfeln ist am Abend warm und golden.",
                    "Die Arvenzapfen reifen, und die Tannenhäher ernten schon.",
                ],
            },
            "sunny": {
                "en": ["Long clear days for the high trails - the snow is gone from all but the highest paths."],
                "de": ["Lange klare Tage für die hohen Wege - der Schnee ist bis auf die höchsten Pfade verschwunden."],
            },
        },
        9: {
            "any": {
                "en": [
                    "The cows come down from the alps, decorated with flowers - the season of the Alpabzug.",
                    "The red deer rut begins: on still evenings the stags roar in the forests.",
                    "Bilberry leaves turn red, colouring whole slopes.",
                    "Autumn crocuses dot the pastures after the cows have gone.",
                    "Rowan berries glow red along the paths.",
                ],
                "de": [
                    "Die Kühe kommen geschmückt von der Alp herunter - die Zeit der Alpabzüge.",
                    "Die Hirschbrunft beginnt: An stillen Abenden röhren die Hirsche in den Wäldern.",
                    "Das Heidelbeerlaub wird rot und färbt ganze Hänge.",
                    "Nach dem Alpabzug sprenkeln Herbstzeitlosen die Weiden.",
                    "Die Vogelbeeren leuchten rot entlang der Wege.",
                ],
            },
            "frost": {
                "en": ["Frost at night, sun by day - the best hiking weather of the year."],
                "de": ["Nachts Frost, tagsüber Sonne - das beste Wanderwetter des Jahres."],
            },
        },
        10: {
            "any": {
                "en": [
                    "The larches are turning gold - the mountains' last and best colour.",
                    "Clear autumn days give the longest views of the year.",
                    "Above the valley fog, the mountains are often in full sun.",
                    "The chamois are growing their dark winter coats.",
                    "The marmots have gone underground for the winter.",
                ],
                "de": [
                    "Die Lärchen werden golden - die letzte und schönste Farbe der Berge.",
                    "Klare Herbsttage bringen die beste Fernsicht des Jahres.",
                    "Über dem Nebel im Tal liegen die Berge oft in voller Sonne.",
                    "Die Gämsen bekommen ihr dunkles Winterfell.",
                    "Die Murmeltiere haben sich für den Winter unter die Erde zurückgezogen.",
                ],
            },
            "snow": {
                "en": ["The first snow dusts the peaks - autumn colours below, winter white above."],
                "de": ["Der erste Schnee pudert die Gipfel - unten Herbstfarben, oben Winterweiss."],
            },
            "sunny": {
                "en": ["Warm sun on the larches: the slopes look lit from inside."],
                "de": ["Warme Sonne auf den Lärchen: Die Hänge sehen aus wie von innen beleuchtet."],
            },
        },
        11: {
            "any": {
                "en": [
                    "The November fog often stays down in the valleys; up here the sun is easier to find.",
                    "The larches drop their needles, carpeting the paths in gold.",
                    "Mountain villages go quiet between the seasons - the in-between has its own peace.",
                    "Ptarmigan and mountain hares are turning white for the winter.",
                    "Chamois are in their rut now; the bucks chase each other across the steep slopes.",
                    "The first snow on the peaks sharpens every ridge line.",
                    "Nutcrackers are living off the stone pine seeds they hid in autumn.",
                ],
                "de": [
                    "Der Novembernebel bleibt oft unten in den Tälern; hier oben ist die Sonne leichter zu finden.",
                    "Die Lärchen werfen ihre Nadeln ab und legen einen goldenen Teppich auf die Wege.",
                    "Die Bergdörfer werden still zwischen den Saisons - das Dazwischen hat seine eigene Ruhe.",
                    "Schneehühner und Schneehasen werden weiss für den Winter.",
                    "Die Gämsen sind in der Brunft; die Böcke jagen einander über die steilen Hänge.",
                    "Der erste Schnee auf den Gipfeln zeichnet jede Gratlinie scharf.",
                    "Die Tannenhäher leben von den Arvennüssen, die sie im Herbst versteckt haben.",
                ],
            },
            "snow": {
                "en": ["Snow is settling in for the season. The quiet that comes with it is worth listening to."],
                "de": ["Der Schnee richtet sich für die Saison ein. Die Stille, die mit ihm kommt, lohnt das Hinhören."],
            },
            "sunny": {
                "en": ["Sunny November days up here can be warmer than in the fog below."],
                "de": ["Sonnige Novembertage können hier oben wärmer sein als unten im Nebel."],
            },
        },
        12: {
            "any": {
                "en": [
                    "Winter is settling in up here: clear nights, short bright days, and snow coming or already there.",
                    "Golden eagles are easier to spot over the snowy slopes now.",
                    "Ibex gather on the sunny cliffs, where the snow slides off first.",
                    "Long nights, bright snow - the light up here is thrown back twice.",
                    "Ibex are in their rut - December is when the big males join the herds.",
                    "Above the valley fog the days are often clear, and the view reaches further than at other times of year.",
                    "Marmots are deep asleep under the snow, a whole family in one burrow.",
                ],
                "de": [
                    "Der Winter richtet sich hier oben ein: klare Nächte, kurze helle Tage, und Schnee, der kommt oder schon liegt.",
                    "Steinadler sind über den verschneiten Hängen jetzt leichter zu entdecken.",
                    "Steinböcke sammeln sich an den sonnigen Felsen, wo der Schnee zuerst abrutscht.",
                    "Lange Nächte, heller Schnee - das Licht wird hier oben doppelt zurückgeworfen.",
                    "Die Steinböcke sind in der Brunft - im Dezember stossen die grossen Böcke zu den Herden.",
                    "Über dem Talnebel sind die Tage oft klar, und die Sicht reicht weiter als sonst im Jahr.",
                    "Die Murmeltiere schlafen tief unter dem Schnee, die ganze Familie in einem Bau.",
                ],
            },
            "snow": {
                "en": ["Fresh snow before Christmas - the first proper winter days on the slopes."],
                "de": ["Neuschnee vor Weihnachten - die ersten richtigen Wintertage an den Hängen."],
            },
            "sunny": {
                "en": ["Sun on fresh snow is the brightest light of the year. Sunglasses, even in December."],
                "de": ["Sonne auf frischem Schnee ist das hellste Licht des Jahres. Sonnenbrille, sogar im Dezember."],
            },
        },
    },
}


# Suggestions for actually using the light when it is there. Kept concrete and
# small enough to act on the same day. The one invitation in a winter message.
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
        "Face the sun for a minute and close your eyes. Winter sun is warmer than it looks.",
        "Take the long way home today, the one with the view to the south.",
        "Walk on the sunny side of the street today. It is a few degrees warmer, and it costs nothing.",
    ],
    "de": [
        "Wenn mittags die Sonne da ist, nimm sie mit nach draussen. Zwanzig Minuten bringen mehr, als es klingt.",
        "Es lohnt sich, rauszugehen, solange es hell ist - das Licht wirkt über die Augen, nicht über die Haut.",
        "Ein kurzer Spaziergang bei Sonne bringt mehr als ein langer nach Einbruch der Dunkelheit.",
        "Wenn du nicht rauskommst, setz dich ans Fenster. Ein Bruchteil der Dosis, aber besser als nichts.",
        "Morgenlicht zählt im Winter doppelt. Hol dir etwas davon in der ersten Stunde nach dem Aufstehen.",
        "Der hellste Teil des Tages ist gerade kurz. Ihn draussen zu verbringen, bereut man selten.",
        "Falls irgendwo in deiner Nähe eine Bank nach Süden zeigt: Jetzt ist ihr Moment.",
        "Kaffee draussen statt am Schreibtisch - kleiner Tausch, spürbarer Unterschied.",
        "Klar und kalt ist dafür besser als grau und mild. Warm anziehen und das Licht mitnehmen.",
        "Schon zehn Minuten draussen tun etwas. Es muss kein richtiger Spaziergang sein.",
        "Halte das Gesicht eine Minute in die Sonne und schliess die Augen. Wintersonne ist wärmer, als sie aussieht.",
        "Nimm heute den längeren Heimweg, den mit Blick nach Süden.",
        "Geh heute auf der Sonnenseite der Strasse. Sie ist ein paar Grad wärmer und kostet nichts.",
    ],
}


# ===== Evenings =====
#
# The fallback lead after dusk in the cold phases, in place of PHASES: the
# day is over, so these are about the evening itself. No figures.

EVENINGS = {
    "darkening": {
        "en": [
            "The day is done, and the evening is long. That is the part of this season worth having.",
            "Dark early means a long evening. Room for a film, a game, a slow dinner.",
            "Lamps on, curtains drawn, something warm in a cup. This season is good at evenings.",
            "This is the time of year when staying in needs no excuse.",
            "A long evening is a good place for the book that has been waiting since summer.",
            "Evenings like this are for cooking something that takes its time. The oven warms the kitchen along the way.",
            "The nights are long enough now to sleep properly. It is the one season that hands out extra rest.",
            "Lit windows up and down the street: for once everyone is home at the same time.",
            "An evening walk at this time of year has the streets almost to itself, and every window is a small stage.",
            "Candles look right again. So do blankets, thick socks and second helpings.",
            "Nothing more is expected of today. The evening is yours.",
            "Long evenings are when people get round to each other: a call, a visit, a table that stays full a while.",
            "The best seat of the season is the one nearest the lamp.",
            "Warm light indoors, cold air on the other side of the glass. The contrast is half the comfort.",
            "The kettle, the radio, a pot on low heat. The evening sounds are the comfortable ones now.",
        ],
        "de": [
            "Der Tag ist vorbei, und der Abend ist lang. Das ist der Teil dieser Jahreszeit, der sich lohnt.",
            "Früh dunkel heisst langer Abend. Platz für einen Film, ein Spiel, ein langsames Abendessen.",
            "Lampen an, Vorhänge zu, etwas Warmes in der Tasse. Abende kann diese Jahreszeit gut.",
            "Das ist die Jahreszeit, in der Daheimbleiben keine Ausrede braucht.",
            "Ein langer Abend ist ein guter Ort für das Buch, das seit dem Sommer wartet.",
            "Solche Abende sind für Gerichte, die Zeit brauchen. Der Ofen wärmt nebenbei die Küche.",
            "Die Nächte sind jetzt lang genug, um richtig zu schlafen. Keine andere Jahreszeit schenkt so viel Ruhe.",
            "Erleuchtete Fenster die ganze Strasse entlang: Für einmal sind alle gleichzeitig zu Hause.",
            "Wer jetzt abends spazieren geht, hat die Strassen fast für sich, und jedes Fenster ist eine kleine Bühne.",
            "Kerzen passen wieder. Decken, dicke Socken und ein Nachschlag auch.",
            "Von heute wird nichts mehr erwartet. Der Abend gehört dir.",
            "An langen Abenden kommt man endlich zueinander: ein Anruf, ein Besuch, ein Tisch, der eine Weile voll bleibt.",
            "Der beste Platz der Saison ist der gleich neben der Lampe.",
            "Warmes Licht drinnen, kalte Luft auf der anderen Seite der Scheibe. Der Gegensatz ist die halbe Gemütlichkeit.",
            "Wasserkocher, Radio, ein Topf auf kleiner Flamme. Die Abendgeräusche sind jetzt die gemütlichen.",
        ],
    },
    "returning_light": {
        "en": [
            "Another day on the returning side of the year is done. Tomorrow has a little more light in it.",
            "It is dark now, and tomorrow it will be dark a little later. That is how this part of the year works.",
            "The long evenings are still here, and still worth using. They will not last: the light is already taking them back.",
            "Winter evenings are for slow food and early nights. Spring will ask more of you soon enough.",
            "While you sleep tonight, the year moves another small step towards the light.",
            "Lamps on, something warm in a cup. The evenings are still long, and each one a little shorter than the last.",
            "Nothing more is expected of today. The light did its part, and will do a little more tomorrow.",
            "A winter evening is a good place for making plans. The days to carry them out are on their way.",
            "Seed catalogues, hiking maps, summer plans: winter evenings are when the bright half of the year gets planned.",
            "The evening is long enough for the book, the film and an early night. Use it while it lasts.",
            "Cold outside, warm inside, and the year heading the right way. A good evening to be home.",
            "Tonight is a little shorter than last night. It has been that way since the solstice, and it adds up.",
            "Soup, a blanket, an early night. Winter still knows how to do evenings.",
            "Rest is part of the season. The light is doing the work for now.",
        ],
        "de": [
            "Wieder ein Tag auf dem Weg ins Helle geschafft. Morgen steckt ein bisschen mehr Licht drin.",
            "Jetzt ist es dunkel, und morgen wird es ein wenig später dunkel. So geht dieser Teil des Jahres.",
            "Die langen Abende sind noch da und immer noch gut zu gebrauchen. Sie bleiben nicht: Das Licht holt sie sich schon zurück.",
            "Winterabende sind für langsames Essen und frühes Schlafen. Der Frühling will noch früh genug mehr von dir.",
            "Während du heute Nacht schläfst, rückt das Jahr wieder einen kleinen Schritt aufs Licht zu.",
            "Lampen an, etwas Warmes in der Tasse. Die Abende sind noch lang, und jeder ein wenig kürzer als der davor.",
            "Von heute wird nichts mehr erwartet. Das Licht hat seinen Teil getan und tut morgen etwas mehr.",
            "Ein Winterabend ist ein guter Ort, um Pläne zu machen. Die Tage dafür sind unterwegs.",
            "Samenkataloge, Wanderkarten, Sommerpläne: An Winterabenden wird die helle Jahreshälfte geplant.",
            "Der Abend reicht für das Buch, den Film und frühes Schlafen. Nutz ihn, solange er dauert.",
            "Draussen kalt, drinnen warm, und das Jahr in der richtigen Richtung unterwegs. Ein guter Abend, um zu Hause zu sein.",
            "Die heutige Nacht ist ein wenig kürzer als die letzte. So geht das seit der Sonnenwende, und es summiert sich.",
            "Suppe, Decke, früh ins Bett. Abende kann der Winter immer noch.",
            "Ausruhen gehört zur Jahreszeit. Die Arbeit macht vorerst das Licht.",
        ],
    },
}


# ===== Also =====
#
# In the returning light the lead takes one more sign of it along, in one
# short sentence: more evidence, inside the message. Only signals listed here
# can come along; they use the same data as their own pools.

ALSO = {
    "turned": {
        "en": ["And the sun already sets {sunset_later} {minutes} later than at its earliest."],
        "de": ["Und die Sonne geht schon {sunset_later} {minutes} später unter als an ihrem frühesten Tag."],
    },
    "since_solstice": {
        "en": ["Since the solstice the day has grown by {hours_gained}.",
               "The day is already {hours_gained} longer than at the solstice."],
        "de": ["Seit der Sonnenwende ist der Tag um {hours_gained} gewachsen.",
               "Der Tag ist schon {hours_gained} länger als zur Sonnenwende."],
    },
    "daily_gain": {
        "en": ["Today alone adds {delta} {minutes} of light."],
        "de": ["Allein heute kommen {delta} {minutes} Licht dazu."],
    },
    "mornings_turned": {
        "en": ["The mornings are turning too: sunrise at {sunrise}, a little earlier each day."],
        "de": ["Auch die Morgen drehen: Sonnenaufgang um {sunrise}, jeden Tag etwas früher."],
    },
    "sunset_milestone": {
        "en": ["And {when} the sun sets after {milestone_time}.",
               "The sun sets after {milestone_time} {when}."],
        "de": ["Und {when} geht die Sonne nach {milestone_time} unter.",
               "Die Sonne geht {when} nach {milestone_time} unter."],
    },
    "sunrise_milestone": {
        "en": ["Sunrise moves before {milestone_time} {when}."],
        "de": ["Der Sonnenaufgang rückt {when} vor {milestone_time}."],
    },
    "hour_mark": {
        "en": ["The day passes {hours_mark} hours {when}."],
        "de": ["Der Tag überschreitet {when} die {hours_mark} Stunden."],
    },
    "noon_sun": {
        "en": ["At noon the sun already stands {noon_gain}° higher than at the solstice."],
        "de": ["Am Mittag steht die Sonne schon {noon_gain}° höher als zur Sonnenwende."],
    },
    "autumn_twin": {
        "en": ["The day is as long again as on {twin_date}."],
        "de": ["Der Tag ist wieder so lang wie am {twin_date}."],
    },
    "equinox_countdown": {
        "en": ["Day and night are equal in {days_to_equinox} {days}."],
        "de": ["In {days_to_equinox} {days_dat} sind Tag und Nacht gleich lang."],
    },
    "sun_ahead": {
        "en": ["And {sunny_day} brings about {sun_hours} {hours} of sun.",
               "{sunny_day} looks sunny, with about {sun_hours} {hours}."],
        "de": ["Und der {sunny_day} bringt etwa {sun_hours} {hours} Sonne.",
               "Der {sunny_day} sieht sonnig aus, mit etwa {sun_hours} {hours}."],
    },
    "sunny_week": {
        "en": ["The week ahead has about {week_hours} hours of sun, after {past_week_hours} in the last."],
        "de": ["Die kommende Woche hat etwa {week_hours} Sonnenstunden, nach {past_week_hours} in der letzten."],
    },
    "warming": {
        "en": ["By the end of the week it is about {temp_change}°C milder."],
        "de": ["Bis Ende Woche wird es etwa {temp_change}°C milder."],
    },
    "uv_strength": {
        "en": ["At midday the UV index reaches {uv}."],
        "de": ["Am Mittag erreicht der UV-Index {uv}."],
    },
}
