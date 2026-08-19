# 🌿 Telangana Mandi Price Finder

New to a city and have no clue what a fair price for tomatoes or mangoes actually is? Yeah, same. I built this so I could pull up real, official market prices from mandis across Telangana before heading out to shop — instead of just trusting whatever the vendor tells me.

**🔗 Live app:** [mandi-price-finder.streamlit.app](https://mandi-price-finder.streamlit.app)

![Streamlit](https://img.shields.io/badge/Streamlit-FF4B4B?style=flat&logo=streamlit&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.9+-blue?style=flat&logo=python&logoColor=white)
![License](https://img.shields.io/badge/License-MIT-green.svg)

---

## Why I built this

Vegetable and fruit prices swing around a lot depending on the day, the season, and which market you're at. When you move somewhere new, you have no baseline for what's reasonable — so I made something to fix that for myself: pick a commodity, pick a mandi, and see the actual minimum, maximum, and modal price being reported that day, straight from government data. No guessing.

---

## What it does

- Pulls live data from the Government of India's open data API on every search — not a cached snapshot
- Populates the market dropdown from real, current mandi names in the dataset instead of a hardcoded list
- Shows the full min/modal/max price range, not just one number
- Falls back gracefully to the closest available market record if your exact pick has no data that day, and tells you it did that
- Covers fruits, vegetables, pulses, and spices
- Shows district, variety, grade, and the date the price was reported

---

## Built with

- [Streamlit](https://streamlit.io) for the app itself, deployed on Streamlit Community Cloud
- [Requests](https://docs.python-requests.org) for the API calls
- [data.gov.in's Open Government Data API](https://www.data.gov.in) — specifically the Agmarknet dataset from the Ministry of Agriculture & Farmers Welfare

### Some of the harder parts

This ended up being less of a "call an API, done" project than I expected. A few things I had to actually debug:

- Requests were silently hanging with no error — turned out the API was stalling anything sent with Python's default `requests` User-Agent. Found this by comparing `curl` (worked instantly) against Python's `requests` (timed out every time), then fixed it by sending a browser-like header.
- The dataset's API resource ID had quietly changed after data.gov.in migrated it — had to dig through their live catalog to find the current, working endpoint.
- The field names in actual API responses (`Market`, `Min_Price`, `Modal_Price`) didn't match what I'd assumed from the docs, so records were silently coming back empty until I fixed the casing.
- Added retries and fast-failing timeouts so the app fails gracefully instead of just hanging when the government API is slow, which — working with public infrastructure — happens.

---

## Running it locally

**1. Clone it**
```bash
git clone https://github.com/priyankaponakampalli/mandi-price-finder.git
cd mandi-price-finder
```

**2. Install dependencies**
```bash
pip install -r requirements.txt
```

**3. Add your API key**

Grab a free key from [data.gov.in](https://www.data.gov.in) (register, then generate a key from any dataset's API tab), then create `.streamlit/secrets.toml`:

```toml
API_KEY = "your-api-key-here"
```

**4. Run it**
```bash
streamlit run app.py
```

---

## Deploying your own copy

1. Fork/push this repo to your GitHub
2. Go to [share.streamlit.io](https://share.streamlit.io) → New app
3. Point it at your repo, branch `main`, file `app.py`
4. Add your `API_KEY` under Advanced settings → Secrets
5. Deploy

---

## Data source

Comes from the [Variety-wise Daily Market Prices Data of Commodity](https://www.data.gov.in/resource/variety-wise-daily-market-prices-data-commodity) dataset — Directorate of Marketing and Inspection, Ministry of Agriculture and Farmers Welfare, via the AGMARKNET portal. Prices are reported per quintal (100 kg) in the raw data; I convert them to per-kg for display.

---

## Limitations, to be upfront about it

- Not every mandi reports every commodity every day, so sometimes you'll see a fallback result instead of an exact match
- The government API can be slow at times — the app retries automatically, but it's not instant every time
- This is a personal/informational project, not affiliated with the Government of India

---

## Things I might add later

- Other states, not just Telangana (the API already supports it)
- Price trend charts over time
- A clearer "how fresh is this data" indicator
- Side-by-side comparison across markets

---

## License

MIT. The underlying government data is released under the [National Data Sharing and Accessibility Policy (NDSAP)](https://www.data.gov.in/full-catalog?page=0&sortby_field=modified&sortby_direction=DESC).
