import pandas as pd
import urllib.request
import xml.etree.ElementTree as ET
import random 
import streamlit as st

# --- 1. DATA SOURCING: TRENDS ---
def get_trending_keywords(geo='US'):
    """Fetches trending searches from the Google Trends RSS (2026 Endpoint)."""
    url = f"https://trends.google.com/trending/rss?geo={geo}"
    
    try:
        headers = {
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/124.0.0.0 Safari/537.36'
        }
        req = urllib.request.Request(url, headers=headers)
        response = urllib.request.urlopen(req)
        
        xml_data = response.read()
        root = ET.fromstring(xml_data)
        
        # Extract titles from RSS items
        keywords = [item.text for item in root.findall('.//item/title')]
        
        if not keywords:
            return ["Smart Watch", "Travel Backpack", "Portable Blender", "Yoga Mat", "Desk Lamp"]
            
        return keywords[:10] # Return top 10

    except Exception as e:
        st.sidebar.error(f"Trend Fetch Error: {e}")
        return ["Ergonomic Chair", "Wireless Earbuds", "Solar Power Bank", "Electric Kettle", "Pet Grooming Kit"]

# --- 2. DATA SOURCING: SUPPLIER (MOCK) ---
def get_supplier_data(keyword):
    """Simulates supplier API data (e.g., AliExpress/CJ Dropshipping)."""
    return {
        "supplier_cost": round(random.uniform(5.0, 25.0), 2),
        "shipping_cost": round(random.uniform(2.0, 8.0), 2)
    }

# --- 3. DATA SOURCING: RETAIL (MOCK) ---
def get_retail_data(keyword):
    """Simulates retail market data (e.g., Amazon/eBay)."""
    return {
        "retail_price": round(random.uniform(40.0, 120.0), 2),
        "monthly_sales": random.randint(500, 8000)
    }

# --- 4. THE UI & LOGIC ---
def main():
    st.set_page_config(page_title="DropShip Scout", layout="wide")
    
    # Sidebar
    st.sidebar.header("Search Settings")
    region = st.sidebar.selectbox("Region", ["US", "GB", "CA", "AU"], index=0)
    min_margin = st.sidebar.slider("Min Margin %", 10, 70, 35)
    
    st.title("🚀 DropShip Product Scout")
    st.write(f"Analyzing current trends in **{region}** to find high-margin opportunities.")

    keywords = get_trending_keywords(geo=region)
    results = []

    for kw in keywords:
        sup = get_supplier_data(kw)
        ret = get_retail_data(kw)
        
        landed_cost = sup['supplier_cost'] + sup['shipping_cost']
        profit = ret['retail_price'] - landed_cost
        margin_pct = (profit / ret['retail_price']) * 100
        
        results.append({
            "Product Trend": kw,
            "Supplier Cost": sup['supplier_cost'],
            "Shipping": sup['shipping_cost'],
            "Total Cost": landed_cost,
            "Retail Price": ret['retail_price'],
            "Margin %": round(margin_pct, 2),
            "Monthly Vol": ret['monthly_sales'],
            "Status": "✅ WINNER" if margin_pct >= min_margin else "❌ LOW MARGIN"
        })

    df = pd.DataFrame(results)

    # UI Row 1: Summary Metrics
    m1, m2, m3 = st.columns(3)
    winners_count = len(df[df['Status'] == "✅ WINNER"])
    m1.metric("Trends Analyzed", len(df))
    m2.metric("Winning Opportunities", winners_count)
    m3.metric("Avg. Margin", f"{round(df['Margin %'].mean(), 1)}%")

    # UI Row 2: Data Table
    st.subheader("Market Analysis")
    st.dataframe(
        df, 
        column_config={
            "Margin %": st.column_config.ProgressColumn("Margin %", format="%f%%", min_value=0, max_value=100),
            "Monthly Vol": st.column_config.NumberColumn("Est. Volume", format="%d units")
        },
        use_container_width=True,
        hide_index=True
    )

    # UI Row 3: Charts
    c1, c2 = st.columns(2)
    with c1:
        st.write("### Volume by Trend")
        st.bar_chart(df.set_index("Product Trend")["Monthly Vol"])
    with c2:
        st.write("### Margin Distribution")
        st.line_chart(df["Margin %"])

if __name__ == "__main__":
    main()