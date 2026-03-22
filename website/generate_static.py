"""
Pre-generate JSON data for the static Vercel dashboard.
Run this locally to produce data.json, then deploy the static site.
"""
import pandas as pd
import numpy as np
import os
import re
import json

DATA_DIR = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))

def load_data():
    files = [
        os.path.join(DATA_DIR, f"annual_aqi_by_county_{y}.csv") for y in range(2021, 2025)
    ]
    dfs = []
    for f in files:
        if os.path.exists(f):
            d = pd.read_csv(f)
            m = re.search(r'(\d{4})\.csv', f)
            if m: d['Year'] = int(m.group(1))
            dfs.append(d)
    return pd.concat(dfs, ignore_index=True)

df = load_data()

# County stats (4-year averages)
county_stats = df.groupby(['State', 'County']).agg({
    'Median AQI': 'mean', 'Max AQI': 'mean'
}).reset_index()
county_stats.columns = ['State', 'County', 'mean_median_aqi', 'mean_max_aqi']

# Thresholds
median_thresh = float(county_stats['mean_median_aqi'].quantile(0.90))
max_thresh = float(county_stats['mean_max_aqi'].quantile(0.90))

# Risk categories
cs = county_stats.copy()
cs['risk'] = 'Low Risk'
cs.loc[cs['mean_median_aqi'] >= median_thresh, 'risk'] = 'High Chronic'
cs.loc[cs['mean_max_aqi'] >= max_thresh, 'risk'] = 'High Acute'
cs.loc[(cs['mean_median_aqi'] >= median_thresh) & (cs['mean_max_aqi'] >= max_thresh), 'risk'] = 'Double Jeopardy'

# Normalized scores
min_med, max_med = cs['mean_median_aqi'].min(), cs['mean_median_aqi'].max()
min_mx, max_mx = cs['mean_max_aqi'].min(), cs['mean_max_aqi'].max()
cs['vuln_score'] = ((cs['mean_median_aqi'] - min_med) / (max_med - min_med)).round(4) if max_med != min_med else 0.5
cs['hazard_score'] = ((cs['mean_max_aqi'] - min_mx) / (max_mx - min_mx)).round(4) if max_mx != min_mx else 0.5
cs['severity_score'] = ((cs['vuln_score'] + cs['hazard_score']) / 2).round(4)

# Build JSON payload
data = {
    'total_counties': len(cs),
    'dj_count': int((cs['risk'] == 'Double Jeopardy').sum()),
    'median_thresh': round(median_thresh, 1),
    'max_thresh': round(max_thresh, 1),
    'risk_counts': cs['risk'].value_counts().to_dict(),
    # All counties for scatter
    'counties': cs[['State', 'County', 'mean_median_aqi', 'mean_max_aqi', 'risk',
                     'vuln_score', 'hazard_score', 'severity_score']].round(2).to_dict(orient='records'),
    # Top 15 chronic
    'chronic_top15': cs.sort_values('mean_median_aqi', ascending=False).head(15)[
        ['State', 'County', 'mean_median_aqi', 'mean_max_aqi']].round(1).to_dict(orient='records'),
    # Top 15 acute
    'acute_top15': cs.sort_values('mean_max_aqi', ascending=False).head(15)[
        ['State', 'County', 'mean_median_aqi', 'mean_max_aqi']].round(1).to_dict(orient='records'),
    # Top 15 severity
    'severity_top15': cs.sort_values('severity_score', ascending=False).head(15)[
        ['State', 'County', 'vuln_score', 'hazard_score', 'severity_score', 'risk']].round(3).to_dict(orient='records'),
    # Double Jeopardy counties
    'dj_counties': cs[cs['risk'] == 'Double Jeopardy'].sort_values('severity_score', ascending=False)[
        ['State', 'County', 'mean_median_aqi', 'mean_max_aqi', 'vuln_score', 'hazard_score', 'severity_score']
    ].round(3).to_dict(orient='records'),
}

out_path = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static', 'data.json')
os.makedirs(os.path.dirname(out_path), exist_ok=True)
with open(out_path, 'w') as f:
    json.dump(data, f)

print(f"Generated {out_path}")
print(f"  {data['total_counties']} counties, {data['dj_count']} Double Jeopardy")
print(f"  File size: {os.path.getsize(out_path) / 1024:.1f} KB")
