import streamlit as st
import requests

# ============================================================
# PAGE CONFIG
# ============================================================

st.set_page_config(
    page_title="Telangana Agricultural Markets",
    page_icon="🌿",
    layout="wide"
)

# ============================================================
# API CONFIG
# ============================================================

# Correct, current resource: "Variety-wise Daily Market Prices Data of Commodity"
API_URL = "https://api.data.gov.in/resource/35985678-0d79-46b4-9ed6-6f13308a1d24"

API_KEY = st.secrets.get("API_KEY", "")


@st.cache_data(ttl=604800, show_spinner=False)  # cache for 7 days
def get_telangana_markets():
    """Fetch the real, current list of mandi/market names for
    Telangana directly from the API, so the dropdown reflects
    actual data instead of a guessed list."""

    if not API_KEY:
        return []

    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 1000,
        "filters[state]": "Telangana"
    }

    headers = {
        "User-Agent": "curl/8.9.1",
        "Accept": "*/*"
    }

    try:
        response = requests.get(API_URL, params=params, headers=headers, timeout=(8, 20))
        response.raise_for_status()
        result = response.json()
        records = result.get("records", [])

        markets = sorted({
            str(r.get("Market", "")).strip()
            for r in records
            if r.get("Market")
        })
        return markets

    except requests.exceptions.RequestException:
        return []

# ============================================================
# BACKGROUND IMAGE
# ============================================================

BACKGROUND_URL = (
    "https://images.unsplash.com/"
    "photo-1500382017468-9049fed747ef"
    "?auto=format&fit=crop&w=2200&q=90"
)

# ============================================================
# CSS
# ============================================================

st.markdown(
    f"""
    <style>

    @import url(
        'https://fonts.googleapis.com/css2?family=DM+Sans:wght@400;500;600;700&family=Playfair+Display:wght@600;700&display=swap'
    );

    .stApp {{
        background-image:
            linear-gradient(
                rgba(220, 231, 211, 0.55),
                rgba(220, 231, 211, 0.55)
            ),
            url("{BACKGROUND_URL}");
        background-size: cover;
        background-position: center;
        background-attachment: fixed;
        background-repeat: no-repeat;
    }}

    header {{
        background: #06391f !important;
    }}

    .block-container {{
        max-width: 1200px;
        padding-top: 1rem;
        padding-bottom: 4rem;
    }}

    .hero-label {{
        text-align: center;
        color: #567d25;
        font-family: 'DM Sans', sans-serif;
        font-size: 15px;
        font-weight: 700;
        letter-spacing: 5px;
        margin-top: 25px;
    }}

    .hero-title {{
        text-align: center;
        color: #063c22;
        font-family: 'Playfair Display', serif;
        font-size: 64px;
        font-weight: 700;
        line-height: 1.05;
        margin-top: 12px;
    }}

    .hero-subtitle {{
        text-align: center;
        color: #173d2b;
        font-family: 'DM Sans', sans-serif;
        font-size: 20px;
        line-height: 1.5;
        max-width: 850px;
        margin: 12px auto 35px auto;
    }}

    .search-title {{
        color: #174d2b;
        font-family: 'Playfair Display', serif;
        font-size: 32px;
        font-weight: 700;
        margin-bottom: 15px;
    }}

    div[data-baseweb="select"] > div {{
        background: white !important;
        border: 1px solid #8ca78f !important;
        border-radius: 10px !important;
        min-height: 52px !important;
    }}

    div[data-baseweb="select"] * {{
        color: #173d2b !important;
    }}

    .stButton > button {{
        width: 100%;
        height: 52px;
        background: #11662f !important;
        color: white !important;
        border: none !important;
        border-radius: 10px !important;
        font-size: 18px !important;
        font-weight: 700 !important;
    }}

    .stButton > button:hover {{
        background: #0b5125 !important;
    }}

    div[data-testid="stMetric"] {{
        background: rgba(255,255,255,0.96);
        border-radius: 18px;
        padding: 25px;
        min-height: 170px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.12);
    }}

    div[data-testid="stMetricLabel"] {{
        color: #3f7225 !important;
        font-weight: 700 !important;
    }}

    div[data-testid="stMetricValue"] {{
        color: #174d2b !important;
        font-family: 'Playfair Display', serif;
    }}

    .main-result {{
        background: #115d2c;
        color: white;
        border-radius: 18px;
        padding: 25px;
        min-height: 170px;
        box-shadow: 0 6px 20px rgba(0,0,0,0.16);
    }}

    .main-result-label {{
        color: #dce76b;
        font-size: 14px;
        font-weight: 700;
        letter-spacing: 2px;
    }}

    .main-price {{
        font-family: 'Playfair Display', serif;
        font-size: 48px;
        font-weight: 700;
        margin-top: 20px;
    }}

    .main-commodity {{
        font-family: 'Playfair Display', serif;
        font-size: 28px;
        margin-top: 5px;
    }}

    .details-box {{
        background: rgba(255,255,255,0.96);
        border-radius: 18px;
        padding: 20px;
        margin-top: 18px;
        box-shadow: 0 5px 18px rgba(0,0,0,0.10);
        color: #173d2b;
    }}

    .source-box {{
        background: rgba(255,255,255,0.96);
        border-radius: 18px;
        padding: 20px;
        margin-top: 15px;
        color: #173d2b;
    }}

    </style>
    """,
    unsafe_allow_html=True
)

# ============================================================
# HERO
# ============================================================

st.markdown(
    '<div class="hero-label">TELANGANA AGRICULTURAL MARKETS</div>',
    unsafe_allow_html=True
)

st.markdown(
    '<div class="hero-title">Today\u2019s Mandi Prices</div>',
    unsafe_allow_html=True
)

st.markdown(
    """
    <div class="hero-subtitle">
        Find current commodity prices across Telangana mandis,
        sourced directly from Government of India market records.
    </div>
    """,
    unsafe_allow_html=True
)

# ============================================================
# SEARCH
# ============================================================

st.markdown(
    '<div class="search-title">🌿 Market Search</div>',
    unsafe_allow_html=True
)

col1, col2, col3 = st.columns(3)

with col1:
    st.markdown("**SELECT CATEGORY**")
    category = st.selectbox(
        "Category",
        ["Fruits", "Vegetables", "Pulses", "Spices"],
        label_visibility="collapsed"
    )

with col2:
    st.markdown("**SELECT COMMODITY**")

    commodity_list = {
        "Fruits": ["Mango", "Banana", "Papaya", "Guava", "Orange"],
        "Vegetables": ["Tomato", "Onion", "Potato", "Carrot", "Brinjal", "Cabbage"],
        "Pulses": ["Red Gram", "Black Gram", "Green Gram", "Bengal Gram"],
        "Spices": ["Chilli", "Turmeric", "Coriander", "Ginger", "Garlic"]
    }

    commodity = st.selectbox(
        "Commodity",
        commodity_list[category],
        label_visibility="collapsed"
    )

with col3:
    st.markdown("**SELECT MANDI / MARKET**")

    live_markets = get_telangana_markets()

    fallback_markets = [
        "Gaddiannaram APMC",
        "Bowenpally",
        "Nizamabad",
        "Warangal",
        "Karimnagar",
        "Sangareddy",
        "Khammam",
        "Adilabad",
        "Mahbubnagar"
    ]

    market_options = live_markets if live_markets else fallback_markets

    if not live_markets:
        st.caption("⚠️ Showing a fallback list — live market list unavailable right now.")

    market = st.selectbox(
        "Market",
        market_options,
        label_visibility="collapsed"
    )

st.write("")

# ============================================================
# BUTTON
# ============================================================

search = st.button("🔍  Check Today's Price", use_container_width=True)

# ============================================================
# API FUNCTION
#
# Notes on the underlying dataset ("Variety-wise Daily Market
# Prices Data of Commodity", resource 35985678-...-6f13308a1d24):
#   - Response fields are capitalized: Market, District, Variety,
#     Grade, Arrival_Date, Min_Price, Modal_Price, Max_Price.
#   - Prices are reported per quintal (100 kg); we convert to /kg.
#   - The API enforces a rate limit per key (visible via the
#     X-Ratelimit-* response headers) — heavy testing can
#     temporarily exhaust it.
# ============================================================

@st.cache_data(ttl=1800, show_spinner=False)
def get_market_data(commodity, market):

    if not API_KEY:
        return None, "API_KEY is missing. Add it to .streamlit/secrets.toml."

    params = {
        "api-key": API_KEY,
        "format": "json",
        "limit": 100,
        "filters[state]": "Telangana",
        "filters[commodity]": commodity
    }

    headers = {
        "User-Agent": "curl/8.9.1",
        "Accept": "*/*"
    }

    last_error = None

    for attempt in range(3):
        try:
            response = requests.get(
                API_URL,
                params=params,
                headers=headers,
                timeout=(8, 20)   # (connect timeout, read timeout)
            )
            response.raise_for_status()
            result = response.json()
            records = result.get("records", [])

            if not records:
                return None, (
                    f"No records returned for '{commodity}' in Telangana. "
                    "This commodity may not currently be reported in this dataset."
                )

            selected_market = market.strip().lower()

            # Try exact market match
            for record in records:
                record_market = str(record.get("Market", "")).strip().lower()
                if record_market == selected_market:
                    return record, None

            # Try partial market match
            for record in records:
                record_market = str(record.get("Market", "")).strip().lower()
                if selected_market in record_market:
                    return record, None

            # Fall back to the first record for this commodity
            return records[0], None

        except requests.exceptions.ConnectTimeout:
            last_error = "Could not connect to the Government API (connection timed out). Check your internet connection."
        except requests.exceptions.ReadTimeout:
            last_error = (
                "Government API is taking too long to respond. This is "
                "often caused by an API rate limit being hit rather than "
                "a real outage."
            )
        except requests.exceptions.HTTPError as e:
            last_error = f"Government API returned an error: {e.response.status_code} {e.response.reason}"
        except requests.exceptions.RequestException as e:
            last_error = f"Government API error: {e}"
        except Exception as e:
            last_error = f"Unexpected error: {e}"

    return None, last_error


def to_float(value):
    try:
        return float(value)
    except (TypeError, ValueError):
        return 0.0


# ============================================================
# RESULT
# ============================================================

if search:

    with st.spinner("Fetching live Government market data..."):
        record, error = get_market_data(commodity, market)

    if record is None:

        st.error(error)
        st.info(
            "The interface is working, but the Government API "
            "did not return data. Check your API key and API "
            "availability."
        )

    else:

        # Government data is reported per quintal (100 kg) —
        # convert to a per-kg price for display.
        minimum = to_float(record.get("Min_Price", 0)) / 100
        modal = to_float(record.get("Modal_Price", 0)) / 100
        maximum = to_float(record.get("Max_Price", 0)) / 100

        actual_market = record.get("Market") or market
        district = record.get("District") or "—"
        variety = record.get("Variety") or "—"
        grade = record.get("Grade") or "—"
        arrival_date = record.get("Arrival_Date") or "—"

        # Warn if we fell back to a different market than requested
        if actual_market.strip().lower() != market.strip().lower():
            st.warning(
                f"No exact match for **{market}** was found. "
                f"Showing the closest available record from **{actual_market}** instead."
            )

        # ----------------------------------------------------
        # Result cards
        # ----------------------------------------------------

        st.write("")

        r1, r2, r3, r4 = st.columns([2, 1, 1, 1])

        with r1:
            st.markdown(
                f"""
                <div class="main-result">
                    <div class="main-result-label">
                        TODAY'S MODAL MARKET PRICE
                    </div>
                    <div class="main-price">
                        ₹{modal:,.2f}
                        <span style="font-size:18px;">/kg</span>
                    </div>
                    <div class="main-commodity">
                        {commodity}
                    </div>
                    <div>
                        Current mandi price per kilogram
                    </div>
                </div>
                """,
                unsafe_allow_html=True
            )

        with r2:
            st.metric("MINIMUM PRICE", f"₹{minimum:,.2f}", "per kg")

        with r3:
            st.metric("MODAL PRICE", f"₹{modal:,.2f}", "per kg")

        with r4:
            st.metric("MAXIMUM PRICE", f"₹{maximum:,.2f}", "per kg")

        # ----------------------------------------------------
        # Details
        # ----------------------------------------------------

        st.markdown(
            f"""
            <div class="details-box">

            📍 <b>DISTRICT</b>
            &nbsp;&nbsp; {district}

            &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;

            🌱 <b>VARIETY</b>
            &nbsp;&nbsp; {variety}

            &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;

            🏅 <b>GRADE</b>
            &nbsp;&nbsp; {grade}

            &nbsp;&nbsp;&nbsp; | &nbsp;&nbsp;&nbsp;

            📅 <b>MARKET DATE</b>
            &nbsp;&nbsp; {arrival_date}

            <br><br>

            🏪 <b>MARKET</b>
            &nbsp;&nbsp; {actual_market}

            </div>
            """,
            unsafe_allow_html=True
        )

        # ----------------------------------------------------
        # Source
        # ----------------------------------------------------

        st.markdown(
            """
            <div class="source-box">

            🛡️ <b>DATA SOURCE</b>

            <br><br>

            Ministry of Agriculture & Farmers Welfare,
            Government of India.

            <br><br>

            Live mandi record retrieved from the
            Government of India data platform.

            </div>
            """,
            unsafe_allow_html=True
        )

        st.success("✓ Live Government API data loaded successfully.")
