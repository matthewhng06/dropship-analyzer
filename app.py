import pandas as pd
from pytrends.request import TrendReq
import random # Used here to mock API data for the example
import streamlit as st

# 1. Fetch Trending Topics
def get_trending_keywords():
    """Fetches current trending searches from Google Trends."""
    pytrend = TrendReq(hl='en-US', tz=360)
    trending_searches_df = pytrend.trending_searches(pn='united_states')
    # Clean up the dataframe and return a list of keywords
    keywords = trending_searches_df[0].head(5).tolist() 
    return keywords

# 2. Mock API Call to Supplier (e.g., AliExpress/CJ Dropshipping)
def get_supplier_data(keyword):
    """
    In reality, you would pass the keyword to the AliExpress or CJ API.
    Here, we return mocked data for demonstration.
    """
    return {
        "product_name": f"{keyword} - Supplier version",
        "supplier_cost": round(random.uniform(2.0, 15.0), 2),
        "supplier_shipping": round(random.uniform(1.0, 5.0), 2)
    }

# 3. Mock API Call to Retailer (e.g., Amazon/Rainforest API)
def get_retail_data(keyword):
    """
    In reality, you would pass the keyword to Amazon SP-API or Keepa.
    """
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