"""
Dynamic content library for Seasonal Horizon.
Extensive variety with nature observations, weather context, and seasonal awareness.
"""

# ===== SEASONAL PHASE DESCRIPTIONS =====
# Based on where we are relative to solstices/equinoxes
SEASONAL_PHASE = {
    "deep_winter": [  # Dec 21 - Jan 31
        "We're in the heart of winter, but the days are already lengthening since the solstice.",
        "The darkest days are behind us—each day now brings a bit more light.",
        "Winter has settled in, but astronomically we're already climbing back toward spring.",
        "January's cold belies the fact that we've turned the corner on darkness.",
        "The solstice was the bottom; we're now on the upward path, even if winter feels dominant.",
        "Deep winter outside, but the light is quietly, steadily returning.",
        "The year's darkest point is behind us—the arc bends toward brightness now.",
        "Winter's grip is firm, but the daylight trend has definitively reversed.",
    ],
    "late_winter": [  # Feb 1 - Mar 19
        "Late winter shows real momentum now—daylight gains are accelerating noticeably.",
        "We're in the fastest phase of light increase before the equinox.",
        "The push toward spring is unmistakable; light levels improve rapidly this time of year.",
        "February and March bring the steepest climb in daylight hours.",
        "The rate of change peaks now—each week feels noticeably different.",
        "Late winter's light gains are dramatic if you're paying attention.",
        "This is when the cumulative effect becomes impossible to ignore.",
        "The momentum toward spring builds daily; we're in the acceleration phase.",
    ],
    "early_spring": [  # Mar 20 - Apr 30
        "Spring is officially here, with days now longer than nights.",
        "We're in the light half of the year now—outdoor time is practical again.",
        "The equinox is behind us; each day brings generous gains in usable daylight.",
        "Spring has arrived astronomically; the balance has shifted toward light.",
        "Days exceed nights now—the season's energy reflects this shift.",
        "Early spring delivers on winter's promise: real, abundant light.",
        "The equinox marked the turning point; we're solidly in the bright half now.",
        "Spring's arrival means evening activities outdoors become routine.",
    ],
    "late_spring": [  # May 1 - Jun 20
        "We're approaching peak daylight—the longest days of the year are near.",
        "Late spring offers some of the best light conditions of the entire year.",
        "The climb toward summer solstice continues; evening light extends late.",
        "These weeks offer exceptional daylight for outdoor activities.",
        "The approach to maximum light is tangible; evenings stretch generously.",
        "Late spring's long days preview the summer solstice ahead.",
        "We're nearing the year's peak; daylight hours are close to maximum.",
        "The final push toward peak light—enjoy these generous days.",
    ],
    "peak_summer": [  # Jun 21 - Jul 31
        "We're at or near peak daylight—the longest days of the year.",
        "Summer solstice marks the peak; enjoy maximum daylight while it lasts.",
        "These are the longest days; the slow decrease begins after the solstice.",
        "Peak light is here—the year's most generous portion of daylight.",
        "The solstice marks both a peak and a turning point.",
        "Maximum daylight achieved; the slow descent begins from here.",
        "We're at the summit of the year's light curve.",
        "Enjoy peak daylight—from here, we begin the gradual return toward winter.",
    ],
    "late_summer": [  # Aug 1 - Sep 21
        "Summer remains strong, but the days are noticeably shorter than at the solstice.",
        "Late summer light is still generous, though sunset creeps earlier each week.",
        "We're past the peak, but there's still plenty of good light for outdoor activities.",
        "The decrease is gentle for now; summer's abundance continues.",
        "Late summer offers a good balance—still long days, but cooler evenings.",
        "We're descending from the peak, though the change is gradual.",
        "Summer lingers in the light levels, even as we move past the solstice.",
        "The slow retreat from maximum daylight is underway.",
    ],
    "early_autumn": [  # Sep 22 - Oct 31
        "Autumn has arrived; the rapid decrease in daylight is the mirror of spring's gains.",
        "We're now in the dark half of the year, with days shorter than nights.",
        "Fall's light decrease is fastest now—each week brings noticeably earlier sunsets.",
        "The equinox signals the shift; darkness now exceeds light each day.",
        "Autumn's rapid changes mirror spring's—just in the opposite direction.",
        "Early fall brings the steepest decline in usable evening light.",
        "We've crossed into the dark half; outdoor time requires more planning.",
        "The descent toward winter accelerates through autumn.",
    ],
    "late_autumn": [  # Nov 1 - Dec 20
        "We're approaching the year's shortest days; the solstice will mark the turning point.",
        "Late autumn means minimal daylight, but the turnaround is now weeks away.",
        "The descent toward winter solstice continues, but the bottom is in sight.",
        "November brings us close to minimum light—the solstice approaches.",
        "The final descent into winter's darkness; the turning point is near.",
        "Late autumn's short days test patience, but the reversal is imminent.",
        "We're in the final stretch before the solstice marks a new beginning.",
        "The year's darkest days approach, but so does the return of light.",
    ],
}

# ===== NATURE OBSERVATIONS BY MONTH =====
NATURE_OBSERVATIONS = {
    1: [
        "Look for winter flocks of birds—they're more visible against bare branches.",
        "Notice how the low sun creates long shadows and golden light on clear days.",
        "Evergreens stand out now as the only green in many landscapes.",
        "This is a good time to observe tree structure—no leaves to obscure the shapes.",
        "Winter birds at feeders are a reminder of life's persistence.",
        "The quiet of winter forests has its own appeal for those who venture out.",
        "Frost patterns on windows and plants reveal nature's geometry.",
        "Look for animal tracks in snow—they tell stories of nighttime activity.",
        "Indoor plants appreciate any natural light you can give them now.",
        "The smell of cold air and woodsmoke marks the season.",
    ],
    2: [
        "Snowdrops and early crocuses may be pushing through—the first flowers of spring.",
        "Listen for increased birdsong, especially on milder mornings.",
        "Willow and hazel catkins release pollen—early signs of the growing season.",
        "The angle of light is noticeably higher than in January.",
        "Early bees may appear on warmer afternoons, testing the conditions.",
        "Tree buds are swelling, though you might need to look closely.",
        "Days feel different now—there's a quality of returning life.",
        "The smell of thawing earth after winter is unmistakable.",
        "Notice how the late afternoon light lingers longer each week.",
        "Squirrels are more active as longer days trigger behavioral changes.",
    ],
    3: [
        "Daffodils and early tulips announce spring's arrival.",
        "Migrating birds return—listen for new songs each morning.",
        "Trees begin to flower before leafing out—look for blossoms.",
        "Frogs and toads emerge to breed in ponds and wetlands.",
        "The dawn chorus intensifies as breeding season approaches.",
        "Bumblebee queens appear, searching for nest sites.",
        "Lambs in fields are a classic sign of the season in rural areas.",
        "Wildflowers begin to carpet woodland floors before trees leaf out.",
        "The smell of spring—damp earth, new growth—is in the air.",
        "Notice how quickly the landscape greens up week to week.",
    ],
    4: [
        "Bluebells and other spring flowers reach their peak in woodlands.",
        "Trees are leafing out—the canopy closes in week by week.",
        "Butterflies emerge in greater numbers on warm days.",
        "Nesting season is underway—birds are busy gathering materials.",
        "Cherry and apple blossoms create spectacular displays.",
        "The dawn chorus is at its peak—early mornings are worth getting up for.",
        "Swallows and martins return from Africa, a classic spring marker.",
        "Gardens explode with growth as warmth and light combine.",
        "The evenings are mild enough for outdoor dining and activities.",
        "Spring energy is palpable—everything is growing, moving, alive.",
    ],
    5: [
        "Cow parsley and hawthorn blossom line country roads.",
        "The canopy is fully closed now—woodland walks are shaded and green.",
        "May blossom (hawthorn) and elderflower scent the hedgerows.",
        "Baby birds are fledging—look for clumsy juveniles in gardens.",
        "Butterflies are numerous on sunny days.",
        "Late evening light extends outdoor time significantly.",
        "Wildflower meadows reach their peak color.",
        "The dawn chorus continues strong; evenings are full of birdsong too.",
        "Gardens require constant attention as growth accelerates.",
        "Outdoor events and activities are in full swing with the generous light.",
    ],
    6: [
        "Elderflowers are ready for cordial-making and fragrant drinks.",
        "The summer solstice brings near-endless twilight at higher latitudes.",
        "Dog roses bloom pink and white in hedgerows.",
        "Early strawberries and soft fruits ripen in gardens.",
        "Haymaking begins in traditional farming areas.",
        "Midsummer celebrations mark the peak of light.",
        "Gardens are lush and full; growth is at its maximum.",
        "Long evenings invite outdoor dining and late walks.",
        "The year's longest days deserve to be noticed and enjoyed.",
        "Wildlife is fully active—birds, insects, mammals all busy.",
    ],
    7: [
        "Lavender and buddleia attract clouds of butterflies.",
        "Wild berries begin to ripen—blackberries in hedgerows.",
        "Swifts scream through evening skies before their August departure.",
        "Summer wildflowers are at their peak in meadows.",
        "Harvest of early crops begins—beans, courgettes, tomatoes.",
        "Warm evenings support outdoor activities well into the night.",
        "Crickets and grasshoppers provide the soundtrack of summer.",
        "Holiday season brings people outdoors in large numbers.",
        "Gardens need watering; the summer maintenance is ongoing.",
        "The slight shortening of days is barely noticeable amid summer warmth.",
    ],
    8: [
        "Blackberries ripen in abundance—free fruit in every hedgerow.",
        "Swallows gather on wires, preparing for autumn migration.",
        "Late summer wildflowers—knapweed, scabious—feed pollinators.",
        "Harvest is in full swing in agricultural areas.",
        "The slant of light shifts noticeably—evenings have a golden quality.",
        "Apples and pears ripen in orchards and gardens.",
        "Corn and grain fields turn golden before harvest.",
        "A hint of autumn appears in morning mists and cooler nights.",
        "Summer holidays wind down; there's a transitional feel.",
        "Enjoy the remaining long evenings—they're shrinking noticeably.",
    ],
    9: [
        "Autumn colors begin to appear in sensitive trees like rowans and cherries.",
        "Mushrooms and fungi emerge in woods and fields after rain.",
        "Migration intensifies—waders and geese move through in large numbers.",
        "Harvest festivals mark the season's abundance.",
        "Berries abound—elderberries, rosehips, sloes for making.",
        "Spider webs catch morning dew, revealing their intricate structures.",
        "The equinox marks a turning point—nights now exceed days.",
        "Squirrels are actively caching nuts for winter.",
        "Apple harvest and cider-making season in many regions.",
        "The quality of light changes—lower, warmer, more golden.",
    ],
    10: [
        "Autumn colors peak—maples, oaks, beeches put on their show.",
        "Leaf fall accelerates through the month.",
        "Geese and swans arrive from the north for winter.",
        "Clocks change in many regions, shifting light to mornings.",
        "The smell of fallen leaves and wood smoke marks the season.",
        "Fungi continue to fruit—keep eyes open on woodland walks.",
        "Halloween and harvest traditions celebrate the season.",
        "Prepare gardens for winter; the growing season is ending.",
        "Wildlife prepares for winter—activity is purposeful.",
        "The rapid shortening of days is undeniable now.",
    ],
    11: [
        "Trees are mostly bare now—the landscape opens up.",
        "Starling murmurations create spectacular evening displays.",
        "Winter thrushes—fieldfares and redwings—arrive from Scandinavia.",
        "Frost becomes regular; the year's chill settles in.",
        "The last leaves fall; winter's structure is revealed.",
        "Bonfire smoke and the smell of burning leaves mark the season.",
        "Gardens go dormant; it's time for planning next year.",
        "Bird feeders become essential as natural food runs low.",
        "The approach to solstice is tangible; darkness dominates evenings.",
        "Indoor time increases as outdoor light shrinks.",
    ],
    12: [
        "The winter solstice marks the year's turning point—light returns from here.",
        "Evergreens symbolize life through the darkest days.",
        "Winter birds—robins, wrens—are easiest to spot now.",
        "Holly berries and mistletoe add color to bare branches.",
        "Frost and perhaps snow transform the landscape.",
        "The shortest days deserve acknowledgment—the climb begins.",
        "Festival lights compensate for nature's minimal offering.",
        "Animal activity continues—foxes, deer are often visible.",
        "The quietness of winter has its own peaceful appeal.",
        "Despite the cold and dark, the solstice brings hope of returning light.",
    ],
}

# ===== DAYLIGHT TREND OBSERVATIONS =====
# Based on actual daily gain/loss in minutes
TREND_STRONG_GAIN = [  # 2+ min/day
    "Days are lengthening rapidly now—you're gaining {delta} minutes daily.",
    "The light increase is strong: +{delta} minutes compared to yesterday.",
    "At {delta} minutes per day, the change is dramatic week to week.",
    "Significant daily gains of {delta} minutes add up fast.",
    "You're adding {delta} minutes each day—the momentum is real.",
    "The upward trend is steep right now: +{delta} minutes daily.",
    "+{delta} minutes today alone; this is the fast phase of the cycle.",
    "Rapid gains of {delta} minutes per day make this an exciting time.",
]

TREND_MODERATE_GAIN = [  # 1-2 min/day
    "Steady gains of {delta} minutes daily add up quickly.",
    "You're adding {delta} minutes of light each day—noticeable over a week.",
    "The upward trend continues: +{delta} minutes from yesterday.",
    "Consistent gains of {delta} minutes build toward brighter days.",
    "+{delta} minutes daily; the steady climb continues.",
    "Each day adds {delta} minutes—the pattern is reliably positive.",
    "Moderate gains of {delta} minutes per day compound nicely.",
    "The light increases by {delta} minutes daily; progress is steady.",
]

TREND_SLOW_GAIN = [  # 0-1 min/day
    "The rate of increase is slowing as we approach peak daylight.",
    "Days are still lengthening, though the pace has slowed near the solstice.",
    "Small daily gains—we're near the year's longest days.",
    "The climb flattens as we approach maximum daylight.",
    "Gains are tapering off; we're near the top of the curve.",
    "The rate of change slows near the peak; that's normal.",
    "Minimal but still positive gains as we near the solstice.",
    "We're approaching the plateau; daily changes are small now.",
]

TREND_STABLE = [  # ~0 min/day
    "Day length is essentially stable right now, near a solstice turning point.",
    "We're at a plateau—the rate of change pauses briefly before reversing.",
    "Minimal change in day length as we're near a solstice.",
    "The curve flattens at the solstice before reversing direction.",
    "Stable daylight hours for now—the peak or trough of the cycle.",
    "Little change day to day; we're at a turning point.",
]

TREND_SLOW_LOSS = [  # 0-1 min/day
    "Days are just beginning to shorten—barely noticeable.",
    "The decrease is gradual for now.",
    "We're losing daylight slowly; the pace will accelerate toward the equinox.",
    "Small losses for now; the steeper descent comes later.",
    "The early phase of decline is gentle.",
    "Minimal decreases as we leave the solstice behind.",
]

TREND_MODERATE_LOSS = [  # 1-2 min/day
    "Days are shortening by {delta} minutes daily now.",
    "The light decrease is steady: -{delta} minutes from yesterday.",
    "At {delta} minutes per day, the change becomes obvious week to week.",
    "Consistent losses of {delta} minutes add up through the season.",
    "-{delta} minutes daily; the trend is clearly downward.",
    "Each day loses {delta} minutes—the pattern is reliably declining.",
]

TREND_STRONG_LOSS = [  # 2+ min/day
    "Rapid decrease now—we're losing {delta} minutes of light daily.",
    "The descent is steep: -{delta} minutes compared to yesterday.",
    "Light retreats quickly this time of year at {delta} minutes per day.",
    "-{delta} minutes today alone; this is the fast phase of decline.",
    "Significant daily losses of {delta} minutes are the norm now.",
    "The downward trend is steep: -{delta} minutes per day.",
]

# ===== WEATHER CONTEXT =====
# Based on today's conditions and forecast
WEATHER_TODAY = {
    "clear": [
        "Clear skies today make the most of available daylight.",
        "Sunny conditions—ideal for outdoor activities.",
        "Bright weather today; take advantage of the good visibility.",
        "Blue skies amplify the available light beautifully.",
        "Excellent conditions for being outside today.",
        "The sun shines unobstructed—make the most of it.",
        "Clear weather like this is worth appreciating.",
        "Sunshine boosts both light levels and mood.",
    ],
    "cloudy": [
        "Overcast today, but the daylight hours remain the same.",
        "Grey skies filter the light without changing the day length.",
        "Clouds today, though the sun still rises and sets on schedule.",
        "Overcast conditions; the light is softer but still present.",
        "Grey weather doesn't change the underlying seasonal trend.",
        "Cloud cover today, but the daylight pattern continues.",
        "The light is diffused by clouds but still useful.",
        "Overcast skies—the astronomical facts remain unchanged.",
    ],
    "rain": [
        "Rain today—the light is there, just filtered through clouds.",
        "Wet weather limits outdoor time, but the daylight trend continues.",
        "Rainy conditions; the seasonal pattern marches on regardless.",
        "Precipitation today—outdoor plans may need adjusting.",
        "Rain feeds the landscape while the light pattern persists.",
        "Wet weather; a good day for indoor activities.",
        "The rain falls, but sunrise and sunset stay on schedule.",
        "Rainy today—nature needs the water as much as the light.",
    ],
    "snow": [
        "Snow today—the white surface actually amplifies available light.",
        "Snowy conditions brighten the landscape despite short days.",
        "Winter weather, but snow reflects and extends the usable light.",
        "Fresh snow makes the most of whatever light there is.",
        "Snow brightens the world; it's nature's way of compensating.",
        "A snowy day has its own kind of brightness.",
        "Snow cover increases the effective light significantly.",
        "Winter snow creates a unique, bright landscape.",
    ],
}

WEATHER_TOMORROW = {
    "better": [
        "Tomorrow looks better weather-wise.",
        "The forecast improves for tomorrow.",
        "Better conditions expected tomorrow.",
    ],
    "worse": [
        "Tomorrow may bring less favorable weather.",
        "The forecast suggests a change for tomorrow.",
        "Weather may turn tomorrow—enjoy today.",
    ],
    "same": [
        "Similar conditions expected tomorrow.",
        "Tomorrow looks much like today weather-wise.",
        "The pattern continues tomorrow.",
    ],
}

WEATHER_WEEK_OUTLOOK = {
    "improving": [
        "The week ahead looks promising with improving conditions.",
        "Better weather is on the way later this week.",
        "The forecast brightens as the week progresses.",
        "Improvement expected over the coming days.",
    ],
    "stable": [
        "Expect consistent conditions through the week.",
        "The weather pattern looks stable for the coming days.",
        "No major changes expected this week.",
        "Steady conditions ahead for the next few days.",
    ],
    "worsening": [
        "The week may bring some weather challenges.",
        "Less favorable conditions possible later in the week.",
        "The forecast suggests a change coming.",
        "Weather may deteriorate as the week progresses.",
    ],
    "warming": [
        "Temperatures are trending upward this week.",
        "A warming trend is underway for the next few days.",
        "Expect warmer conditions as the week progresses.",
        "The thermometer is heading up over the coming days.",
    ],
    "cooling": [
        "Temperatures are dropping over the next few days.",
        "A cooling trend is expected this week.",
        "Cooler conditions are on the way.",
        "Expect lower temperatures as the week unfolds.",
    ],
    "mixed": [
        "Mixed conditions expected through the week.",
        "The forecast shows some variety in the days ahead.",
        "Expect a mix of conditions this week.",
    ],
}

# ===== PRACTICAL TIME OBSERVATIONS =====
PRACTICAL_SUNRISE = {
    "very_early": [  # Before 5 AM
        "Extremely early sunrise at {time}—maximum morning light.",
        "The sun rises before most people at {time}.",
    ],
    "early": [  # 5-6 AM
        "Early sunrise at {time} rewards early risers.",
        "Dawn breaks at {time}—plenty of morning light available.",
    ],
    "moderate": [  # 6-7 AM
        "Sunrise at {time} aligns well with typical morning schedules.",
        "The sun rises at {time}—a reasonable hour for most.",
    ],
    "late": [  # 7-8 AM
        "Later sunrise at {time} means darker mornings.",
        "The sun doesn't appear until {time}—mornings start in darkness.",
    ],
    "very_late": [  # After 8 AM
        "Very late sunrise at {time}—winter's signature.",
        "Dark mornings with sunrise not until {time}.",
    ],
}

PRACTICAL_SUNSET = {
    "very_early": [  # Before 4:30 PM
        "Very early sunset at {time} severely limits afternoon light.",
        "Darkness falls by {time}—winter's early evenings.",
    ],
    "early": [  # 4:30-5:30 PM
        "Early sunset at {time} limits after-work outdoor time.",
        "The sun sets at {time}—evening light is at a premium.",
    ],
    "moderate": [  # 5:30-7 PM
        "Sunset at {time} provides reasonable evening light.",
        "The sun sets at {time}—workable for after-work activities.",
    ],
    "late": [  # 7-8:30 PM
        "Late sunset at {time} extends outdoor possibilities.",
        "Evening light until {time} opens up many options.",
    ],
    "very_late": [  # After 8:30 PM
        "Very late sunset at {time}—summer's gift of long evenings.",
        "Light lingers until {time}—maximum evening potential.",
    ],
}

# ===== SOLSTICE PROGRESS COMMENTARY =====
SOLSTICE_COMMENTARY = {
    "just_past_winter": [
        "We're just days past the winter solstice—the climb has barely begun, but it has begun.",
        "Fresh off the solstice, the gains are tiny but real.",
    ],
    "early_recovery": [
        "The recovery from winter solstice is underway—{hours} regained so far.",
        "We've clawed back {hours} since December's minimum.",
    ],
    "mid_recovery": [
        "Solid progress since the solstice: {hours} of light regained.",
        "We're now {hours} ahead of the winter minimum—real progress.",
    ],
    "strong_recovery": [
        "Major recovery: {hours} more daylight than at the solstice.",
        "{hours} gained since December—spring is clearly arriving.",
    ],
    "near_peak": [
        "Approaching maximum daylight—{hours} more than winter's minimum.",
        "Near peak light with {hours} more than the solstice.",
    ],
    "at_peak": [
        "At peak daylight—the maximum the year offers.",
        "Summer solstice territory—we're at the top of the curve.",
    ],
    "past_peak": [
        "Past the summer peak, but still {hours} ahead of winter's minimum.",
        "The descent has begun, though we're still {hours} up from December.",
    ],
}
