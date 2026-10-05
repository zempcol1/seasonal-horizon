// ===== I18N LABELS =====
const i18n = {
    en: {
        locale: "en-GB",
        sunrise: "Sunrise",
        sunset: "Sunset",
        daylight: "Daylight",
        sinceYesterday: "Since yesterday",
        sinceLastWeek: "Since last week",
        sinceSolstice: "Since solstice",
        another: "Another thought",
        settings: "Settings",
        close: "Close",
        language: "Language",
        location: "Location",
        searchCity: "Search for a city",
        cityPlaceholder: "e.g. Zurich, Munich, Vienna...",
        loading: "Reading the sky...",
        // One line under the card for each phase of the year.
        footer: {
            darkening: "The year is resting, and the turn is coming.",
            returning_light: "Your daily reminder that light always returns.",
            spring: "Everything that waited is growing again.",
            summer: "The long days are here. Enjoy them.",
            autumn: "The season of colour and harvest."
        },
        current: "Current",
        searching: "Searching...",
        noResults: "No cities found",
        searchFailed: "Search failed. Try again.",
        connectionError: "Connection issue. Please refresh.",
        sunHours: h => `${h} h of sun`,
        sky: { grey: "Cloudy", rain: "Rain", snow: "Snow", fog: "Fog" },
        changelog: [
            { version: "v0.6", text: "Rebuilt around what is good about today, tuned for Central Europe: light calculated, weather read from sunshine hours, nature by region and weather, Zurich customs, and one message a day with a button for another" },
            { version: "v0.5", text: "Winter now leads with the returning light: spring signs, sun tips, and only facts we actually measured" },
            { version: "v0.4.1", text: "Weather-aware nature observations, better mobile layout" },
            { version: "v0.4", text: "Multi-language support (English/German)" },
            { version: "v0.3", text: "Smart forecast narratives with 7-day weather analysis" },
            { version: "v0.2", text: "Location selection and improved text generation" },
            { version: "v0.1", text: "Initial release" }
        ]
    },
    de: {
        locale: "de-CH",
        sunrise: "Aufgang",
        sunset: "Untergang",
        daylight: "Tageslicht",
        sinceYesterday: "Seit gestern",
        sinceLastWeek: "Seit Vorwoche",
        sinceSolstice: "Seit Sonnenwende",
        another: "Ein anderer Gedanke",
        settings: "Einstellungen",
        close: "Schliessen",
        language: "Sprache",
        location: "Standort",
        searchCity: "Stadt suchen",
        cityPlaceholder: "z.B. Zürich, München, Wien...",
        loading: "Blick in den Himmel...",
        footer: {
            darkening: "Das Jahr ruht, und die Wende kommt.",
            returning_light: "Deine tägliche Erinnerung daran, dass das Licht immer wiederkehrt.",
            spring: "Alles, was gewartet hat, wächst wieder.",
            summer: "Die langen Tage sind da. Geniess sie.",
            autumn: "Die Zeit der Farben und der Ernte."
        },
        current: "Aktuell",
        searching: "Suche...",
        noResults: "Keine Städte gefunden",
        searchFailed: "Suche fehlgeschlagen. Nochmal versuchen.",
        connectionError: "Verbindungsproblem. Bitte neu laden.",
        sunHours: h => `${h} Std. Sonne`,
        sky: { grey: "Bewölkt", rain: "Regen", snow: "Schnee", fog: "Nebel" },
        changelog: [
            { version: "v0.6", text: "Neu aufgebaut um das, was heute gut ist, abgestimmt auf Mitteleuropa: Licht berechnet, Wetter nach Sonnenstunden, Natur nach Region und Wetter, Zürcher Bräuche, und eine Botschaft pro Tag mit Knopf für eine andere" },
            { version: "v0.5", text: "Im Winter steht das zurückkehrende Licht im Vordergrund: Frühlingsboten, Sonnentipps, und nur noch belegte Angaben" },
            { version: "v0.4.1", text: "Wetterabhängige Naturbeobachtungen, optimiertes Layout" },
            { version: "v0.4", text: "Mehrsprachigkeit (Englisch/Deutsch)" },
            { version: "v0.3", text: "Intelligente Wetternarrative mit 7-Tage-Analyse" },
            { version: "v0.2", text: "Standortauswahl und verbesserte Textgenerierung" },
            { version: "v0.1", text: "Erste Version" }
        ]
    }
};

// The sky as the server reads it from the measured sun, not from weather codes.
const SKY_ICONS = { sunny: '☀️', mixed: '⛅', grey: '☁️', rain: '🌧️', snow: '🌨️', fog: '🌫️' };

// ===== STATE =====
// Server-rendered defaults, so the client keeps no copy of its own.
const defaults = document.getElementById('app-config').dataset;

// The phase of the year depends only on the date, so the server sets it on <html>.
const phase = document.documentElement.dataset.phase;

const state = {
    city: localStorage.getItem('sh_city') || defaults.city,
    lat: parseFloat(localStorage.getItem('sh_lat')) || parseFloat(defaults.lat),
    lon: parseFloat(localStorage.getItem('sh_lon')) || parseFloat(defaults.lon),
    lang: localStorage.getItem('sh_lang') || detectLanguage(),
    // 0 is today's message, the same all day; the button counts up.
    variant: 0
};

let dataController = null;
let searchController = null;
let searchTimer = null;
let searchRequestId = 0;

const $ = id => document.getElementById(id);
const labelsFor = () => i18n[state.lang] || i18n.en;

// ===== INIT =====
function detectLanguage() {
    const browserLang = navigator.language || navigator.userLanguage || 'en';
    return browserLang.startsWith('de') ? 'de' : 'en';
}

function init() {
    // The status bar on phones takes the top colour of the season's sky.
    const top = getComputedStyle(document.documentElement).getPropertyValue('--top').trim();
    if (top) document.querySelector('meta[name="theme-color"]').content = top;

    $('location-label').textContent = state.city;
    $('lang-select').value = state.lang;
    document.documentElement.lang = state.lang;
    applyLabels();
    fetchData();
}

function applyLabels() {
    const labels = labelsFor();

    document.querySelectorAll('[data-i18n]').forEach(el => {
        const text = labels[el.getAttribute('data-i18n')];
        if (typeof text === 'string') el.textContent = text;
    });
    document.querySelectorAll('[data-i18n-label]').forEach(el => {
        el.setAttribute('aria-label', labels[el.getAttribute('data-i18n-label')]);
    });

    $('date-label').textContent = new Intl.DateTimeFormat(labels.locale,
        { weekday: 'long', day: 'numeric', month: 'long' }).format(new Date());
    $('footer-text').textContent = labels.footer[phase] || labels.footer.returning_light;
    $('loader-text').textContent = labels.loading;
    $('city-input').placeholder = labels.cityPlaceholder;

    const changelogList = $('changelog-list');
    changelogList.innerHTML = '';
    labels.changelog.forEach(item => {
        const li = document.createElement('li');
        const version = document.createElement('strong');
        version.textContent = item.version;
        li.append(version, ` – ${item.text}`);
        changelogList.appendChild(li);
    });
}

function changeLanguage(lang) {
    state.lang = lang;
    localStorage.setItem('sh_lang', lang);
    document.documentElement.lang = lang;
    applyLabels();
    fetchData();
}

// ===== DATA FETCHING =====
// `gentle` keeps the card in place and only cross-fades the message - for
// "another thought", where the figures do not change.
async function fetchData({ gentle = false } = {}) {
    if (dataController) {
        dataController.abort();
    }
    dataController = new AbortController();

    const labels = labelsFor();
    const message = $('message');

    if (gentle) {
        message.classList.add('fading');
    } else {
        $('loader').classList.remove('hidden');
        $('content').classList.add('hidden');
    }
    $('another-btn').disabled = true;

    try {
        const res = await fetch(
            `/api/uplift?lat=${state.lat}&lon=${state.lon}&lang=${state.lang}&v=${state.variant}`,
            { signal: dataController.signal }
        );

        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();

        if (data.success) {
            showMessage(data.lead, data.companion);
            showFacts(data.facts, labels);
        } else {
            showMessage(data.error || labels.connectionError, '');
        }
    } catch (e) {
        if (e.name === 'AbortError') return;
        console.error('Fetch error:', e);
        showMessage(labels.connectionError, '');
    }

    $('another-btn').disabled = false;
    message.classList.remove('fading');
    $('loader').classList.add('hidden');
    $('content').classList.remove('hidden');
}

function showMessage(lead, companion) {
    $('lead').textContent = lead;
    $('companion').textContent = companion;
    $('companion').classList.toggle('hidden', !companion);
}

function showFacts(facts, labels) {
    $('f-sunrise').textContent = facts.sunrise;
    $('f-sunset').textContent = facts.sunset;
    $('f-length').textContent = facts.day_length;

    showDelta('f-delta-d', facts.delta_yesterday);
    showDelta('f-delta-w', facts.delta_week);
    showDelta('f-delta-s', facts.delta_solstice);

    // Gains are only shown while they are gains - in the returning light.
    $('gains-section').classList.toggle('hidden', !facts.gains);

    const { sky, sun_hours: sun } = facts;
    $('weather-icon').textContent = SKY_ICONS[sky] || '';
    $('f-weather').textContent = sun >= 1 ? labels.sunHours(sun) : (labels.sky[sky] || '--');
    $('f-temp').textContent = facts.temp_max;
}

function anotherMessage() {
    state.variant++;
    fetchData({ gentle: true });
}

// A signed figure like "+3 min", coloured by its sign. "--" (not measured) stays plain.
function showDelta(id, value) {
    const el = $(id);
    el.textContent = value;
    el.className = 'val ' + (/^\+\d/.test(value) ? 'positive' : /^-\d/.test(value) ? 'negative' : '');
}

// ===== SETTINGS =====
function openSettings() {
    const labels = labelsFor();
    $('overlay').classList.remove('hidden');
    $('city-input').value = '';
    $('city-results').innerHTML = '';

    const current = $('current-loc');
    const name = document.createElement('strong');
    name.textContent = state.city;
    current.replaceChildren(`${labels.current}: `, name);

    $('lang-select').value = state.lang;
    $('city-input').focus();
}

function closeSettings() {
    if (searchController) {
        searchController.abort();
        searchController = null;
    }
    clearTimeout(searchTimer);
    $('overlay').classList.add('hidden');
}

function handleOverlayClick(e) {
    if (e.target.id === 'overlay') closeSettings();
}

document.addEventListener('keydown', e => {
    if (e.key === 'Escape' && !$('overlay').classList.contains('hidden')) closeSettings();
});

function toggleChangelog() {
    $('changelog').classList.toggle('hidden');
}

// ===== CITY SEARCH =====
$('city-input').addEventListener('input', function() {
    const query = this.value.trim();
    clearTimeout(searchTimer);

    if (searchController) {
        searchController.abort();
        searchController = null;
    }

    if (query.length < 2) {
        $('city-results').innerHTML = '';
        return;
    }

    searchTimer = setTimeout(() => searchCity(query), 300);
});

function listNote(list, className, text) {
    const li = document.createElement('li');
    li.className = className;
    li.textContent = text;
    list.replaceChildren(li);
}

async function searchCity(q) {
    const list = $('city-results');
    const labels = labelsFor();
    const requestId = ++searchRequestId;

    searchController = new AbortController();
    listNote(list, 'searching', labels.searching);

    try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`, {
            signal: searchController.signal
        });

        if (requestId !== searchRequestId) return;
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (requestId !== searchRequestId) return;

        if (data.length === 0) {
            listNote(list, 'no-results', labels.noResults);
            return;
        }

        list.innerHTML = '';
        data.forEach(city => {
            const li = document.createElement('li');
            li.textContent = [city.name, city.admin1, city.country].filter(Boolean).join(', ');
            // Reachable by keyboard as well: Tab to it, Enter to choose.
            li.tabIndex = 0;
            const choose = () => selectCity(city.name, city.latitude, city.longitude, city.country);
            li.addEventListener('click', choose);
            li.addEventListener('keydown', e => { if (e.key === 'Enter') choose(); });
            list.appendChild(li);
        });
    } catch (e) {
        if (e.name !== 'AbortError' && requestId === searchRequestId) {
            listNote(list, 'error', labels.searchFailed);
        }
    }
}

function selectCity(name, lat, lon, country) {
    const fullName = country ? `${name}, ${country}` : name;

    state.city = fullName;
    state.lat = lat;
    state.lon = lon;
    state.variant = 0;

    localStorage.setItem('sh_city', fullName);
    localStorage.setItem('sh_lat', String(lat));
    localStorage.setItem('sh_lon', String(lon));

    $('location-label').textContent = fullName;
    closeSettings();
    fetchData();
}

// ===== START =====
init();
