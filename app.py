import streamlit as st
import subprocess
import json
from urllib.parse import quote

# =========================================================
# GOVERNMENT API
# =========================================================

API_KEY = st.secrets["API_KEY"]

BASE_URL = "https://api.data.gov.in/resource/9ef84268-d588-465a-a308-a864a43d0070"


# =========================================================
# GET DATA FROM GOVERNMENT API
# =========================================================

def get_data(commodity=None):

    all_records = []
    offset = 0
    limit = 1000

    while True:

        url = (
            BASE_URL
            + "?api-key=" + API_KEY
            + "&format=json"
            + "&limit=" + str(limit)
            + "&offset=" + str(offset)
            + "&filters%5Bstate%5D=Telangana"
        )

        if commodity:
            url += "&filters%5Bcommodity%5D=" + quote(commodity)

        result = subprocess.run(
            ["curl", "--max-time", "20", "-s", url],
            capture_output=True,
            text=True
        )

        if result.returncode != 0:
            break

        try:
            data = json.loads(result.stdout)
        except:
            break

        records = data.get("records", [])

        if not records:
            break

        all_records.extend(records)

        total = int(data.get("total", 0))

        offset += limit

        if offset >= total:
            break

    return all_records


# =========================================================
# AUTOMATIC CATEGORY CLASSIFICATION
# =========================================================

def get_category(commodity):

    name = commodity.lower().strip()

    # -------------------------
    # VEGETABLES
    # -------------------------

    vegetables = [
        "tomato",
        "onion",
        "potato",
        "brinjal",
        "eggplant",
        "cabbage",
        "cauliflower",
        "carrot",
        "beetroot",
        "radish",
        "turnip",
        "beans",
        "green beans",
        "french beans",
        "lady finger",
        "okra",
        "bhindi",
        "green chilli",
        "chilli",
        "capsicum",
        "cucumber",
        "pumpkin",
        "bottle gourd",
        "ridge gourd",
        "bitter gourd",
        "snake gourd",
        "drumstick",
        "peas",
        "sweet potato",
        "spinach",
        "amaranth",
        "colocasia",
        "yam",
        "garlic",
        "ginger"
    ]

    for item in vegetables:
        if item in name:
            return "🥕 Vegetables"


    # -------------------------
    # FRUITS
    # -------------------------

    fruits = [
        "apple",
        "banana",
        "mango",
        "orange",
        "grapes",
        "papaya",
        "pomegranate",
        "guava",
        "water melon",
        "watermelon",
        "muskmelon",
        "pineapple",
        "lemon",
        "lime",
        "coconut",
        "sapota",
        "chikoo",
        "jack fruit",
        "jackfruit",
        "pear",
        "peach",
        "plum",
        "kiwi"
    ]

    for item in fruits:
        if item in name:
            return "🍎 Fruits"


    # -------------------------
    # SEEDS
    # -------------------------

    seeds = [
        "seed",
        "seeds",
        "cotton seed",
        "groundnut seed",
        "sesamum seed",
        "sesame seed",
        "sunflower seed",
        "mustard seed",
        "castor seed",
        "niger seed",
        "linseed",
        "melon seed"
    ]

    for item in seeds:
        if item in name:
            return "🌻 Seeds"


    # -------------------------
    # CEREALS
    # -------------------------

    cereals = [
        "maize",
        "paddy",
        "rice",
        "wheat",
        "jowar",
        "sorghum",
        "bajra",
        "millet",
        "ragi",
        "barley",
        "oats"
    ]

    for item in cereals:
        if item in name:
            return "🌾 Cereals"


    # -------------------------
    # PULSES
    # -------------------------

    pulses = [
        "gram",
        "bengal gram",
        "chickpea",
        "chana",
        "black gram",
        "urad",
        "green gram",
        "moong",
        "mung",
        "red gram",
        "arhar",
        "tur",
        "lentil",
        "masoor",
        "peas"
    ]

    for item in pulses:
        if item in name:
            return "🌱 Pulses"


    # -------------------------
    # SPICES
    # -------------------------

    spices = [
        "turmeric",
        "coriander",
        "cumin",
        "pepper",
        "cardamom",
        "clove",
        "fenugreek",
        "chilli",
        "dry chilli",
        "dry red chilli"
    ]

    for item in spices:
        if item in name:
            return "🌶️ Spices"


    # -------------------------
    # OILSEEDS
    # -------------------------

    oilseeds = [
        "groundnut",
        "soyabean",
        "soybean",
        "sunflower",
        "mustard",
        "sesamum",
        "sesame",
        "castor",
        "niger",
        "linseed"
    ]

    for item in oilseeds:
        if item in name:
            return "🛢️ Oilseeds"


    # -------------------------
    # OTHER
    # -------------------------

    return "🌿 Other"


# =========================================================
# PAGE CONFIG
# =========================================================

st.set_page_config(
    page_title="Mandi Price Finder",
    page_icon="🥕",
    layout="centered"
)


# =========================================================
# HEADER
# =========================================================

st.title("🥕 Mandi Price Finder")

st.markdown(
    "### Today's commodity prices at Telangana mandis"
)

st.caption(
    "Live data from Government of India mandi price records"
)

st.divider()


# =========================================================
# LOAD DATA
# =========================================================

if "all_records" not in st.session_state:

    with st.spinner("Loading Telangana mandi data..."):

        st.session_state["all_records"] = get_data()


all_records = st.session_state["all_records"]


if not all_records:

    st.error(
        "Unable to fetch government market data."
    )

    st.stop()


# =========================================================
# CREATE COMMODITY → CATEGORY MAPPING
# =========================================================

commodity_categories = {}

for record in all_records:

    commodity = record.get("commodity", "").strip()

    if commodity:

        commodity_categories[commodity] = get_category(
            commodity
        )


# =========================================================
# CATEGORY SELECTION
# =========================================================

st.subheader("1️⃣ Select Category")

categories = sorted(
    list(set(commodity_categories.values()))
)

category = st.selectbox(
    "Choose commodity category",
    categories
)


# =========================================================
# COMMODITIES FOR CATEGORY
# =========================================================

available_commodities = sorted(
    [
        commodity
        for commodity, cat
        in commodity_categories.items()
        if cat == category
    ]
)


if not available_commodities:

    st.warning(
        "No commodities available in this category today."
    )

    st.stop()


# =========================================================
# COMMODITY SELECTION
# =========================================================

st.subheader("2️⃣ Select Commodity")

commodity = st.selectbox(
    "Choose commodity",
    available_commodities
)


# =========================================================
# GET MARKET DATA FOR COMMODITY
# =========================================================

with st.spinner(
    f"Finding Telangana mandis for {commodity}..."
):

    commodity_records = get_data(commodity)


# =========================================================
# MARKET LIST
# =========================================================

markets = sorted(
    list(
        set(
            record.get("market", "").strip()
            for record in commodity_records
            if record.get("market")
        )
    )
)


if not markets:

    st.warning(
        f"No current mandi data found for {commodity}."
    )

    st.stop()


# =========================================================
# MARKET SELECTION
# =========================================================

st.subheader("3️⃣ Select Mandi / Market")

market = st.selectbox(
    "Choose a specific mandi",
    markets
)


# =========================================================
# PRICE BUTTON
# =========================================================

if st.button(
    "💰 Check Today's Price",
    type="primary",
    use_container_width=True
):

    selected_record = None

    for record in commodity_records:

        if record.get("market", "").strip() == market:

            selected_record = record

            break


    if selected_record:

        # Government data is per quintal.
        # 1 quintal = 100 kg.

        min_price = float(
            selected_record["min_price"]
        ) / 100

        max_price = float(
            selected_record["max_price"]
        ) / 100

        modal_price = float(
            selected_record["modal_price"]
        ) / 100


        # =================================================
        # RESULT
        # =================================================

        st.divider()

        st.subheader(
            "💰 Today's Market Price"
        )


        st.metric(
            label=f"{commodity} — Price per kg",
            value=f"₹{modal_price:.2f}/kg"
        )


        # =================================================
        # MIN / MAX
        # =================================================

        col1, col2 = st.columns(2)

        with col1:

            st.metric(
                "Minimum",
                f"₹{min_price:.2f}/kg"
            )

        with col2:

            st.metric(
                "Maximum",
                f"₹{max_price:.2f}/kg"
            )


        st.divider()


        # =================================================
        # MARKET DETAILS
        # =================================================

        st.markdown(
            f"### 📍 {selected_record['market']}"
        )

        st.write(
            f"**District:** "
            f"{selected_record['district']}"
        )

        st.write(
            f"**Commodity:** "
            f"{selected_record['commodity']}"
        )

        st.write(
            f"**Variety:** "
            f"{selected_record['variety']}"
        )

        st.write(
            f"**Grade:** "
            f"{selected_record['grade']}"
        )

        st.write(
            f"**Market date:** "
            f"{selected_record['arrival_date']}"
        )


        st.success(
            f"Today's {commodity} price at "
            f"{selected_record['market']} is "
            f"**₹{modal_price:.2f} per kg**."
        )


        st.caption(
            "🏛️ Source: Ministry of Agriculture & Farmers Welfare, "
            "Government of India"
        )


# =========================================================
# REFRESH
# =========================================================

st.divider()

if st.button(
    "🔄 Refresh Government Data"
):

    st.session_state.pop(
        "all_records",
        None
    )

    st.rerun()

