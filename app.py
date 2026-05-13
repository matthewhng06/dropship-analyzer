import pandas as pd
import urllib.request
import xml.etree.ElementTree as ET
import random 
import streamlit as st

# 1. Fetch Trending Topics (Updated to use Google's official RSS feed)
def get_trending_keywords():
    """Fetches current trending searches from Google Trends RSS."""
    # We use Google's official daily RSS feed for the US
    url = "https://trends.google.com/trending/rss?geo=US"
    
    # We add a 'User-Agent' so Google thinks we are a normal web browser, not a bot
    req = urllib.request.Request(url, headers={'User-Agent': 'Mozilla/5.0'})
    response = urllib.request.urlopen(req)
    
    # Parse the XML data Google sends back
    root = ET.fromstring(response.read())
    
    # Extract the text from the <title> tags inside the feed
    keywords = [item.text for item in root.findall('.//item/title')]
    
    # Return the top 5 trending keywords
    return keywords[:5]

# 2. Mock API Call to Supplier (e.g., AliExpress/CJ Dropshipping)
def get_supplier_data(keyword):
    return {
        "product_name": f"{keyword} - Supplier version",
        "supplier_cost": round(random.uniform(2.0, 15.0), 2),
        "supplier_shipping": round(random.uniform(1.0, 5.0), 2)
    }

# 3. Mock API Call to Retailer (e.g., Amazon/Rainforest API)
def get_retail_data(keyword):
    return {
        "retail_price": round(random.uniform(20.0, 60.0), 2),
        "estimated_monthly_volume": random.randint(100, 5000)
    }

# 4. Generate the Report
def generate_report():
    st.title("Dropship Product Analyzer")
    st.write("Fetching trending keywords and analyzing market data...")
    
    keywords = get_trending_keywords()
    results = []
    
    for kw in keywords:
        supplier = get_supplier_data(kw)
        retail = get_retail_data(kw)
        
        total_cost = supplier['supplier_cost'] + supplier['supplier_shipping']
        margin_dollars = retail['retail_price'] - total_cost
        margin_percent = (margin_dollars / retail['retail_price']) * 100
        
        results.append({
            "Keyword (Trend)": kw,
            "Supplier Cost ($)": total_cost,
            "Retail Price ($)": retail['retail_price'],
            "Est. Volume": retail['estimated_monthly_volume'],
            "Margin (%)": round(margin_percent, 2),
            "Recommendation": "Investigate" if margin_percent > 40 and retail['estimated_monthly_volume'] > 1000 else "Skip"
        })
        
    df = pd.DataFrame(results)
    
    # Dashboard Visuals
    st.subheader("Top Opportunities")
    st.dataframe(df.style.highlight_max(subset=['Margin (%)', 'Est. Volume'], color='lightgreen'))
    
    st.subheader("Hottest Selling by Volume")
    st.bar_chart(df.set_index("Keyword (Trend)")["Est. Volume"])

if __name__ == "__main__":
    generate_report()