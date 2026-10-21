"""
Country Headline Hitters

Shows the most current news of a county in a specific country.

Usage:
    Phase 2 Wk 1 day 3.py

Requirements:
    pip install requests python-dotenv
    OPENWEATHER_API_KEY in .env file
    NEWS_API_KEY in .env file
"""

import requests
import os
from dotenv import load_dotenv
from pathlib import Path
import json

load_dotenv(Path(__file__).parent / ".env", override=True)

REST_KEY = os.getenv("REST_COUNTRIES_API_KEY")
NEWS_KEY = os.getenv("NEWS_API_KEY")

def get_country(country):
    url = f"https://restcountries.com/v3.1/name/{country}"
    headers = {}
    if REST_KEY:
        headers['Authorization'] = f'Bearer {REST_KEY}'
    response = requests.get(url, headers=headers)
    if response.status_code == 200:
        return response.json()
    print(f"Country API failed: {response.status_code} {response.text[:500]}")
    return None

def get_county_news(county):
    url = f"https://newsapi.org/v2/everything?q={county}&apiKey={NEWS_KEY}"
    response = requests.get(url)
    if response.status_code == 200:
        return response.json()
    return None

def save_to_file(data, filename):
    with open(filename, "w") as f:
        json.dump(data, f, indent=2)
    print(f"Data saved to {filename}")

def run_tool():
    print("="*16)
    print("News headline hitters")
    print("="*16)
    print()
    country = input("Enter a country name: ").strip()
    if not country:
        print("No country entered. Exiting.")
        return

    print(f"\nFetching data for {country}...")
    country_data = get_country(country)

    if not country_data:
        print(f"Could not find country data for '{country}'.")
        return

    county = input("Enter county/region to search news: ").strip()
    if not county:
        county = country
    
    # FIX 1: Create news_data BEFORE you use it
    news_data = get_county_news(county)

    # FIX 2: Save to files
    #save_to_file(country_data, "country.json")
    #save_to_file(news_data, "news.json")
  
    print(f"\n=== Results for {country} - {county} ===")

    c = {}
    try:
        c = country_data["data"]["objects"][0]
    except:
        try:
            c = country_data["data"][0]
        except:
            try:
                c = country_data[0]
            except:
                c = country_data

    population = c.get("population", 0)
    if population == 0:
        try:
            population = c.get("demographics", {}).get("population", 0)
        except:
            population = 0

    region = c.get("region", "Unknown")
    if region == "Unknown":
        try:
            region = c.get("geography", {}).get("region", "Unknown")
        except:
            pass
    if region == "Unknown":
        try:
            region = c.get("continents", ["Unknown"])[0]
        except:
            pass

    currencies = ""
    try:
        curr_obj = c.get("currencies", {})
        if isinstance(curr_obj, dict):
            currencies = ", ".join(curr_obj.keys())
        elif isinstance(curr_obj, list):
            currencies = ", ".join([x.get("code", "") for x in curr_obj])
        else:
            currencies = str(curr_obj)
        if not currencies:
            currencies = ", ".join(c.get("finance", {}).get("currencies", {}).keys())
    except:
        currencies = ""

    print()
    print("="*16)
    print("Country Info")
    print("="*16)
    print(f"Region      : {region}")
    print(f"Population  : {population:,}" if population else "Population  : Unknown")
    print(f"Currency    : {currencies}")
    print()

    if news_data:
        articles = news_data.get("articles", [])
        if not articles:
            print(f"No news found for {county}.")
            return

        first = articles[0]
        print("="*16)
        print(f"News for {county} town.")
        print("="*16)
        print(f"\nSource : {first.get('source',{}).get('name','Unknown')}")
        print(f"\nReporter: {first.get('author','Unknown')}")
        print(f"\nDescription: {first.get('description','')}.")
        print(f"\nTitle: {first.get('title','')}.")
        print(f"\nDate published: {first.get('publishedAt','')}.")
        print(f"\nContent: {first.get('content','')}.")
    
run_tool()
