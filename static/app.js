// ===== I18N LABELS =====
const i18n = {
    en: {
        sunrise: "Sunrise",
        sunset: "Sunset",
        daylight: "Daylight",
        vsYesterday: "vs Yesterday",
        vsLastWeek: "vs Last Week",
        vsSolstice: "vs Solstice",
        settings: "Settings",
        language: "Language",
        location: "Location",
        searchCity: "Search for a city",
        loading: "Reading the sky...",
        footer: "Your daily reminder that light always returns.",
        current: "Current",
        searching: "Searching...",
        noResults: "No cities found",
        searchFailed: "Search failed. Try again.",
        connectionError: "Connection issue. Please refresh.",
        weather: {
            0: "Clear", 1: "Mostly Clear", 2: "Partly Cloudy", 3: "Overcast",
            45: "Foggy", 48: "Icy Fog", 51: "Light Drizzle", 53: "Drizzle",
            55: "Heavy Drizzle", 61: "Light Rain", 63: "Rain", 65: "Heavy Rain",
            71: "Light Snow", 73: "Snow", 75: "Heavy Snow", 77: "Snow Grains",
            80: "Light Showers", 81: "Showers", 82: "Heavy Showers",
            85: "Snow Showers", 86: "Heavy Snow", 95: "Thunderstorm", 96: "Hail Storm",
            99: "Severe Storm"
        },
        changelog: [
            { version: "v0.5", text: "Winter now leads with the returning light: spring signs, sun tips, and only facts we actually measured" },
            { version: "v0.4.1", text: "Weather-aware nature observations, better mobile layout" },
            { version: "v0.4", text: "Multi-language support (English/German)" },
            { version: "v0.3", text: "Smart forecast narratives with 7-day weather analysis" },
            { version: "v0.2", text: "Location selection and improved text generation" },
            { version: "v0.1", text: "Initial release" }
        ]
    },
    de: {
        sunrise: "Aufgang",
        sunset: "Untergang",
        daylight: "Tageslicht",
        vsYesterday: "vs Gestern",
        vsLastWeek: "vs Vorwoche",
        vsSolstice: "vs Wende",
        settings: "Einstellungen",
        language: "Sprache",
        location: "Standort",
        searchCity: "Stadt suchen",
        loading: "Blick in den Himmel...",
        footer: "Deine tägliche Erinnerung daran, dass das Licht immer wiederkehrt.",
        current: "Aktuell",
        searching: "Suche...",
        noResults: "Keine Städte gefunden",
        searchFailed: "Suche fehlgeschlagen. Nochmal versuchen.",
        connectionError: "Verbindungsproblem. Bitte neu laden.",
        weather: {
            0: "Klar", 1: "Überwiegend klar", 2: "Teils bewölkt", 3: "Bedeckt",
            45: "Neblig", 48: "Eisnebel", 51: "Leichter Nieselregen",
            53: "Nieselregen", 55: "Starker Nieselregen", 61: "Leichter Regen",
            63: "Regen", 65: "Starker Regen", 71: "Leichter Schneefall",
            73: "Schneefall", 75: "Starker Schneefall", 77: "Schneegriesel",
            80: "Leichte Schauer", 81: "Schauer", 82: "Starke Schauer",
            85: "Schneeschauer", 86: "Starker Schneefall", 95: "Gewitter",
            96: "Hagelgewitter", 99: "Schweres Gewitter"
        },
        changelog: [
            { version: "v0.5", text: "Im Winter steht das zurückkehrende Licht im Vordergrund: Frühlingsboten, Sonnentipps, und nur noch belegte Angaben" },
            { version: "v0.4.1", text: "Wetterabhängige Naturbeobachtungen, optimiertes Layout" },
            { version: "v0.4", text: "Mehrsprachigkeit (Englisch/Deutsch)" },
            { version: "v0.3", text: "Intelligente Wetternarrative mit 7-Tage-Analyse" },
            { version: "v0.2", text: "Standortauswahl und verbesserte Textgenerierung" },
            { version: "v0.1", text: "Erste Version" }
        ]
    }
};

const WEATHER_ICONS = {
    0: '☀️', 1: '🌤️', 2: '⛅', 3: '☁️', 45: '🌫️', 48: '🌫️',
    51: '🌦️', 53: '🌦️', 55: '🌧️', 61: '🌧️', 63: '🌧️', 65: '🌧️',
    71: '🌨️', 73: '🌨️', 75: '❄️', 77: '🌨️', 80: '🌦️', 81: '🌧️',
    82: '⛈️', 85: '🌨️', 86: '❄️', 95: '⛈️', 96: '⛈️', 99: '⛈️'
};

// ===== STATE =====
// Server-rendered defaults, so the client keeps no copy of its own.
const defaults = document.getElementById('app-config').dataset;

const state = {
    city: localStorage.getItem('sh_city') || defaults.city,
    lat: parseFloat(localStorage.getItem('sh_lat')) || parseFloat(defaults.lat),
    lon: parseFloat(localStorage.getItem('sh_lon')) || parseFloat(defaults.lon),
    lang: localStorage.getItem('sh_lang') || detectLanguage()
};

let dataController = null;
let searchController = null;
let searchTimer = null;
let searchRequestId = 0;

// ===== INIT =====
function detectLanguage() {
    const browserLang = navigator.language || navigator.userLanguage || 'en';
    return browserLang.startsWith('de') ? 'de' : 'en';
}

function init() {
    document.getElementById('location-label').textContent = state.city;
    document.getElementById('lang-select').value = state.lang;
    document.documentElement.lang = state.lang;
    applyLabels();
    fetchData();
}

function applyLabels() {
    const labels = i18n[state.lang] || i18n.en;
    
    document.querySelectorAll('[data-i18n]').forEach(el => {
        const key = el.getAttribute('data-i18n');
        if (labels[key]) {
            el.textContent = labels[key];
        }
    });
    
    document.getElementById('footer-text').textContent = labels.footer;
    document.getElementById('loader-text').textContent = labels.loading;
    document.getElementById('city-input').placeholder = state.lang === 'de' 
        ? 'z.B. Berlin, Zürich, Wien...' 
        : 'e.g. Berlin, Tokyo, New York...';

    // Update changelog
    const changelogList = document.getElementById('changelog-list');
    changelogList.innerHTML = '';
    labels.changelog.forEach(item => {
        const li = document.createElement('li');
        li.innerHTML = `<strong>${item.version}</strong> – ${item.text}`;
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
async function fetchData() {
    if (dataController) {
        dataController.abort();
    }
    dataController = new AbortController();
    
    const loader = document.getElementById('loader');
    const content = document.getElementById('content');
    const labels = i18n[state.lang] || i18n.en;
    
    loader.classList.remove('hidden');
    content.classList.add('hidden');
    document.getElementById('loader-text').textContent = labels.loading;

    try {
        const res = await fetch(
            `/api/uplift?lat=${state.lat}&lon=${state.lon}&city=${encodeURIComponent(state.city)}&lang=${state.lang}`,
            { signal: dataController.signal }
        );
        
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        
        if (data.success) {
            document.getElementById('uplift-text').textContent = data.text;
            
            document.getElementById('f-sunrise').textContent = data.facts.sunrise;
            document.getElementById('f-sunset').textContent = data.facts.sunset;
            document.getElementById('f-length').textContent = data.facts.day_length;
            
            const deltaD = document.getElementById('f-delta-d');
            const deltaW = document.getElementById('f-delta-w');
            const deltaS = document.getElementById('f-delta-s');
            
            deltaD.textContent = data.facts.delta_yesterday;
            deltaW.textContent = data.facts.delta_week;
            deltaS.textContent = data.facts.delta_solstice;

            deltaD.className = 'val ' + (data.facts.delta_yesterday.includes('+') ? 'positive' : (data.facts.delta_yesterday.includes('-') ? 'negative' : ''));
            deltaW.className = 'val ' + (data.facts.delta_week.includes('+') ? 'positive' : (data.facts.delta_week.includes('-') ? 'negative' : ''));
            deltaS.className = 'val ' + (data.facts.delta_solstice.includes('+') ? 'positive' : (data.facts.delta_solstice.includes('-') ? 'negative' : ''));

            const weatherCode = data.facts.weather_code || 0;
            document.getElementById('weather-icon').textContent =
                WEATHER_ICONS[weatherCode] || WEATHER_ICONS[0];
            document.getElementById('f-weather').textContent =
                labels.weather[weatherCode] || i18n.en.weather[weatherCode] || '';
            document.getElementById('f-temp').textContent = data.facts.temp_max;
        } else {
            document.getElementById('uplift-text').textContent = data.error || 'Could not load data.';
        }
    } catch (e) {
        if (e.name !== 'AbortError') {
            console.error('Fetch error:', e);
            document.getElementById('uplift-text').textContent = labels.connectionError;
        }
    }
    
    loader.classList.add('hidden');
    content.classList.remove('hidden');
}

// ===== SETTINGS =====
function openSettings() {
    const labels = i18n[state.lang] || i18n.en;
    document.getElementById('overlay').classList.remove('hidden');
    document.getElementById('city-input').value = '';
    document.getElementById('city-results').innerHTML = '';
    document.getElementById('current-loc').innerHTML = `<small>${labels.current}: <strong>${state.city}</strong></small>`;
    document.getElementById('lang-select').value = state.lang;
    document.getElementById('city-input').focus();
}

function closeSettings() {
    if (searchController) {
        searchController.abort();
        searchController = null;
    }
    clearTimeout(searchTimer);
    document.getElementById('overlay').classList.add('hidden');
}

function handleOverlayClick(e) {
    if (e.target.id === 'overlay') closeSettings();
}

function toggleChangelog() {
    document.getElementById('changelog').classList.toggle('hidden');
}

// ===== CITY SEARCH =====
document.getElementById('city-input').addEventListener('input', function() {
    const query = this.value.trim();
    clearTimeout(searchTimer);
    
    if (searchController) {
        searchController.abort();
        searchController = null;
    }
    
    if (query.length < 2) {
        document.getElementById('city-results').innerHTML = '';
        return;
    }
    
    searchTimer = setTimeout(() => searchCity(query), 300);
});

async function searchCity(q) {
    const list = document.getElementById('city-results');
    const labels = i18n[state.lang] || i18n.en;
    const requestId = ++searchRequestId;
    
    searchController = new AbortController();
    list.innerHTML = `<li class="searching">${labels.searching}</li>`;
    
    try {
        const res = await fetch(`/api/search?q=${encodeURIComponent(q)}`, {
            signal: searchController.signal
        });
        
        if (requestId !== searchRequestId) return;
        if (!res.ok) throw new Error(`HTTP ${res.status}`);
        const data = await res.json();
        if (requestId !== searchRequestId) return;
        
        if (data.length === 0) {
            list.innerHTML = `<li class="no-results">${labels.noResults}</li>`;
            return;
        }
        
        list.innerHTML = '';
        data.forEach(city => {
            const li = document.createElement('li');
            const parts = [city.name];
            if (city.admin1) parts.push(city.admin1);
            if (city.country) parts.push(city.country);
            li.textContent = parts.join(', ');
            li.addEventListener('click', () => selectCity(city.name, city.latitude, city.longitude, city.country));
            list.appendChild(li);
        });
    } catch (e) {
        if (e.name !== 'AbortError' && requestId === searchRequestId) {
            list.innerHTML = `<li class="error">${labels.searchFailed}</li>`;
        }
    }
}

function selectCity(name, lat, lon, country) {
    const fullName = country ? `${name}, ${country}` : name;
    
    state.city = fullName;
    state.lat = lat;
    state.lon = lon;
    
    localStorage.setItem('sh_city', fullName);
    localStorage.setItem('sh_lat', String(lat));
    localStorage.setItem('sh_lon', String(lon));
    
    document.getElementById('location-label').textContent = fullName;
    closeSettings();
    fetchData();
}

// ===== START =====
init();
