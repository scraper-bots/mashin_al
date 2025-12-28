#!/usr/bin/env python3
"""
Business Analytics Chart Generator for Mashin.al Car Marketplace
Generates comprehensive business insights visualizations
"""

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
from pathlib import Path

# Set professional style
plt.style.use('seaborn-v0_8-darkgrid')
sns.set_palette("husl")
plt.rcParams['figure.figsize'] = (12, 7)
plt.rcParams['font.size'] = 10
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 11

# Create output directory
OUTPUT_DIR = Path('charts')
OUTPUT_DIR.mkdir(exist_ok=True)

print("Loading data...")
df = pd.read_csv('optimized_mashin_cars.csv')

# Data cleaning
print("Cleaning data...")
df['price_clean'] = df['price'].astype(str).str.replace(' AZN', '').str.replace(' USD', '').str.replace(' ', '').str.replace(',', '')
df['price_clean'] = pd.to_numeric(df['price_clean'], errors='coerce')
df['year'] = pd.to_numeric(df['year'], errors='coerce')
df['mileage_clean'] = df['mileage'].astype(str).str.replace(' ', '').str.replace(',', '')
df['mileage_clean'] = pd.to_numeric(df['mileage_clean'], errors='coerce')
df['age'] = 2025 - df['year']

# Filter valid data
df_valid = df[(df['price_clean'] > 0) & (df['price_clean'] < 500000) &
              (df['year'] >= 1990) & (df['year'] <= 2025)].copy()

print(f"Total listings: {len(df):,}")
print(f"Valid listings for analysis: {len(df_valid):,}")
print("\nGenerating charts...\n")

# ============================================================================
# CHART 1: Market Share - Top Brands by Volume
# ============================================================================
print("1. Generating market share chart...")
fig, ax = plt.subplots(figsize=(14, 8))
top_brands = df['brand'].value_counts().head(12)
colors = sns.color_palette("Spectral", len(top_brands))
bars = ax.barh(range(len(top_brands)), top_brands.values, color=colors)
ax.set_yticks(range(len(top_brands)))
ax.set_yticklabels(top_brands.index)
ax.set_xlabel('Number of Listings', fontweight='bold')
ax.set_title('Market Share: Top 12 Brands by Listing Volume', fontweight='bold', fontsize=16, pad=20)
ax.invert_yaxis()

# Add value labels
for i, (bar, value) in enumerate(zip(bars, top_brands.values)):
    pct = (value / len(df)) * 100
    ax.text(value + 100, i, f'{value:,} ({pct:.1f}%)', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '01_market_share_by_brand.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 2: Average Price by Top Brands
# ============================================================================
print("2. Generating price positioning chart...")
fig, ax = plt.subplots(figsize=(14, 8))
top_brands_list = df_valid['brand'].value_counts().head(12).index
brand_avg_price = df_valid[df_valid['brand'].isin(top_brands_list)].groupby('brand')['price_clean'].mean().sort_values(ascending=True)
colors = sns.color_palette("RdYlGn_r", len(brand_avg_price))
bars = ax.barh(range(len(brand_avg_price)), brand_avg_price.values, color=colors)
ax.set_yticks(range(len(brand_avg_price)))
ax.set_yticklabels(brand_avg_price.index)
ax.set_xlabel('Average Price (AZN)', fontweight='bold')
ax.set_title('Price Positioning: Average Price by Top Brands', fontweight='bold', fontsize=16, pad=20)
ax.invert_yaxis()

# Add value labels
for i, (bar, value) in enumerate(zip(bars, brand_avg_price.values)):
    ax.text(value + 500, i, f'{value:,.0f} AZN', va='center', fontweight='bold')

# Add market average line
market_avg = df_valid['price_clean'].mean()
ax.axvline(market_avg, color='red', linestyle='--', linewidth=2, label=f'Market Avg: {market_avg:,.0f} AZN')
ax.legend()

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '02_average_price_by_brand.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 3: Inventory Age Distribution
# ============================================================================
print("3. Generating inventory age distribution...")
fig, ax = plt.subplots(figsize=(12, 7))
age_bins = [0, 3, 7, 15, 100]
age_labels = ['0-3 years\n(Nearly New)', '3-7 years\n(Recent)', '7-15 years\n(Used)', '15+ years\n(Old)']
df_valid['age_category'] = pd.cut(df_valid['age'], bins=age_bins, labels=age_labels, right=False)
age_dist = df_valid['age_category'].value_counts().reindex(age_labels)

colors = ['#2ecc71', '#3498db', '#f39c12', '#e74c3c']
bars = ax.bar(range(len(age_dist)), age_dist.values, color=colors, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(age_dist)))
ax.set_xticklabels(age_labels, fontweight='bold')
ax.set_ylabel('Number of Listings', fontweight='bold')
ax.set_title('Inventory Distribution by Vehicle Age', fontweight='bold', fontsize=16, pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, age_dist.values)):
    pct = (value / len(df_valid)) * 100
    ax.text(i, value + 200, f'{value:,}\n({pct:.1f}%)', ha='center', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '03_inventory_age_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 4: Regional Market Distribution
# ============================================================================
print("4. Generating regional distribution...")
fig, ax = plt.subplots(figsize=(14, 8))
top_regions = df['region'].value_counts().head(10)
colors = sns.color_palette("viridis", len(top_regions))
bars = ax.barh(range(len(top_regions)), top_regions.values, color=colors)
ax.set_yticks(range(len(top_regions)))
ax.set_yticklabels(top_regions.index)
ax.set_xlabel('Number of Listings', fontweight='bold')
ax.set_title('Geographic Distribution: Top 10 Regions by Listing Volume', fontweight='bold', fontsize=16, pad=20)
ax.invert_yaxis()

# Add value labels
for i, (bar, value) in enumerate(zip(bars, top_regions.values)):
    pct = (value / len(df)) * 100
    ax.text(value + 200, i, f'{value:,} ({pct:.1f}%)', va='center', fontweight='bold')

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '04_regional_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 5: Price Depreciation by Age
# ============================================================================
print("5. Generating price depreciation analysis...")
fig, ax = plt.subplots(figsize=(12, 7))
age_categories = ['0-3 years\n(Nearly New)', '3-7 years\n(Recent)', '7-15 years\n(Used)', '15+ years\n(Old)']
df_valid['age_category'] = pd.cut(df_valid['age'], bins=[0, 3, 7, 15, 100], labels=age_categories, right=False)
price_by_age = df_valid.groupby('age_category', observed=True)['price_clean'].mean().reindex(age_categories)

colors = ['#27ae60', '#3498db', '#f39c12', '#e74c3c']
bars = ax.bar(range(len(price_by_age)), price_by_age.values, color=colors, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(price_by_age)))
ax.set_xticklabels(age_categories, fontweight='bold')
ax.set_ylabel('Average Price (AZN)', fontweight='bold')
ax.set_title('Price Depreciation: Average Price by Vehicle Age', fontweight='bold', fontsize=16, pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, price_by_age.values)):
    ax.text(i, value + 800, f'{value:,.0f} AZN', ha='center', fontweight='bold', fontsize=11)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '05_price_depreciation_by_age.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 6: Feature Adoption Rates
# ============================================================================
print("6. Generating feature adoption analysis...")
fig, ax = plt.subplots(figsize=(12, 7))

features = {
    'Credit\nAvailable': df['credit'].sum(),
    'Trade-In\nAccepted': df['tradeable'].sum(),
    'VIN\nShown': df['show_vin'].sum(),
    'Phone\nNumber': df['phone_number'].notna().sum()
}

percentages = [(v / len(df)) * 100 for v in features.values()]
colors = ['#3498db', '#2ecc71', '#9b59b6', '#e67e22']

bars = ax.bar(range(len(features)), percentages, color=colors, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(features)))
ax.set_xticklabels(features.keys(), fontweight='bold', fontsize=12)
ax.set_ylabel('Adoption Rate (%)', fontweight='bold')
ax.set_title('Feature Adoption Rates Across All Listings', fontweight='bold', fontsize=16, pad=20)
ax.set_ylim(0, max(percentages) * 1.2)

# Add value labels
for i, (bar, pct, count) in enumerate(zip(bars, percentages, features.values())):
    ax.text(i, pct + 1, f'{pct:.1f}%\n({count:,} listings)', ha='center', fontweight='bold', fontsize=10)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '06_feature_adoption_rates.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 7: Top Models by Brand (Top 3 Brands)
# ============================================================================
print("7. Generating top models analysis...")
fig, axes = plt.subplots(1, 3, figsize=(16, 6))
top_3_brands = df['brand'].value_counts().head(3).index

for idx, brand in enumerate(top_3_brands):
    brand_df = df[df['brand'] == brand]
    top_models = brand_df['model'].value_counts().head(8)

    colors_gradient = sns.color_palette("Blues_r", len(top_models)) if idx == 0 else \
                      sns.color_palette("Reds_r", len(top_models)) if idx == 1 else \
                      sns.color_palette("Greens_r", len(top_models))

    axes[idx].barh(range(len(top_models)), top_models.values, color=colors_gradient)
    axes[idx].set_yticks(range(len(top_models)))
    axes[idx].set_yticklabels(top_models.index, fontsize=9)
    axes[idx].set_xlabel('Listings', fontweight='bold')
    axes[idx].set_title(f'{brand}\nTop Models', fontweight='bold', fontsize=12)
    axes[idx].invert_yaxis()

    # Add value labels
    for i, value in enumerate(top_models.values):
        axes[idx].text(value + 20, i, f'{value:,}', va='center', fontsize=9)

plt.suptitle('Most Popular Models by Top 3 Brands', fontweight='bold', fontsize=16, y=1.02)
plt.tight_layout()
plt.savefig(OUTPUT_DIR / '07_top_models_by_brand.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 8: Price Distribution Analysis
# ============================================================================
print("8. Generating price distribution chart...")
fig, ax = plt.subplots(figsize=(14, 7))

price_bins = [0, 5000, 10000, 15000, 20000, 30000, 50000, 100000, 500000]
price_labels = ['Under 5K', '5-10K', '10-15K', '15-20K', '20-30K', '30-50K', '50-100K', '100K+']
df_valid['price_range'] = pd.cut(df_valid['price_clean'], bins=price_bins, labels=price_labels)
price_dist = df_valid['price_range'].value_counts().reindex(price_labels)

colors = sns.color_palette("coolwarm", len(price_dist))
bars = ax.bar(range(len(price_dist)), price_dist.values, color=colors, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(price_dist)))
ax.set_xticklabels(price_labels, rotation=45, ha='right', fontweight='bold')
ax.set_ylabel('Number of Listings', fontweight='bold')
ax.set_title('Price Distribution: Number of Listings by Price Range (AZN)', fontweight='bold', fontsize=16, pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, price_dist.values)):
    if pd.notna(value):
        pct = (value / len(df_valid)) * 100
        ax.text(i, value + 100, f'{value:,.0f}\n({pct:.1f}%)', ha='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '08_price_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 9: Listings Over Time (Creation Date Trends)
# ============================================================================
print("9. Generating temporal trends chart...")
fig, ax = plt.subplots(figsize=(14, 7))

# Parse creation date
df['created_month'] = df['created_at'].astype(str).str.split().str[1]
month_order = ['yanvar', 'fevral', 'mart', 'aprel', 'may', 'iyun', 'iyul', 'avqust', 'sentyabr', 'oktyabr', 'noyabr', 'dekabr']
month_mapping = {m: i for i, m in enumerate(month_order, 1)}
month_labels = ['Jan', 'Feb', 'Mar', 'Apr', 'May', 'Jun', 'Jul', 'Aug', 'Sep', 'Oct', 'Nov', 'Dec']

listings_by_month = df['created_month'].value_counts()
# Map to proper order
month_counts = []
for month in month_order:
    count = listings_by_month.get(month, 0)
    month_counts.append(count)

x = range(len(month_labels))
ax.plot(x, month_counts, marker='o', linewidth=3, markersize=10, color='#3498db')
ax.fill_between(x, month_counts, alpha=0.3, color='#3498db')
ax.set_xticks(x)
ax.set_xticklabels(month_labels, fontweight='bold')
ax.set_xlabel('Month', fontweight='bold')
ax.set_ylabel('Number of Listings Created', fontweight='bold')
ax.set_title('Listing Activity: New Listings Created by Month', fontweight='bold', fontsize=16, pad=20)
ax.grid(True, alpha=0.3)

# Add value labels
for i, value in enumerate(month_counts):
    if value > 0:
        ax.text(i, value + 50, f'{value:,}', ha='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '09_listings_over_time.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 10: Regional Price Comparison
# ============================================================================
print("10. Generating regional price comparison...")
fig, ax = plt.subplots(figsize=(14, 8))

top_regions_list = df_valid['region'].value_counts().head(10).index
regional_prices = df_valid[df_valid['region'].isin(top_regions_list)].groupby('region')['price_clean'].mean().sort_values(ascending=True)

colors = sns.color_palette("plasma", len(regional_prices))
bars = ax.barh(range(len(regional_prices)), regional_prices.values, color=colors)
ax.set_yticks(range(len(regional_prices)))
ax.set_yticklabels(regional_prices.index)
ax.set_xlabel('Average Price (AZN)', fontweight='bold')
ax.set_title('Regional Price Comparison: Average Price by Top 10 Regions', fontweight='bold', fontsize=16, pad=20)
ax.invert_yaxis()

# Add value labels
for i, (bar, value) in enumerate(zip(bars, regional_prices.values)):
    ax.text(value + 200, i, f'{value:,.0f} AZN', va='center', fontweight='bold')

# Add market average line
market_avg = df_valid['price_clean'].mean()
ax.axvline(market_avg, color='red', linestyle='--', linewidth=2, label=f'Market Avg: {market_avg:,.0f} AZN')
ax.legend()

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '10_regional_price_comparison.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 11: Credit Impact Analysis
# ============================================================================
print("11. Generating credit impact analysis...")
fig, ax = plt.subplots(figsize=(10, 7))

credit_data = {
    'With Credit\nAvailable': df_valid[df_valid['credit'] == True]['price_clean'].mean(),
    'Without Credit': df_valid[df_valid['credit'] == False]['price_clean'].mean()
}

colors = ['#2ecc71', '#e74c3c']
bars = ax.bar(range(len(credit_data)), credit_data.values(), color=colors, edgecolor='black', linewidth=2)
ax.set_xticks(range(len(credit_data)))
ax.set_xticklabels(credit_data.keys(), fontweight='bold', fontsize=12)
ax.set_ylabel('Average Price (AZN)', fontweight='bold')
ax.set_title('Credit Availability Impact on Vehicle Pricing', fontweight='bold', fontsize=16, pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, credit_data.values())):
    ax.text(i, value + 500, f'{value:,.0f} AZN', ha='center', fontweight='bold', fontsize=12)

# Calculate and show premium
premium = ((credit_data['With Credit\nAvailable'] / credit_data['Without Credit']) - 1) * 100
ax.text(0.5, max(credit_data.values()) * 0.5, f'Premium: +{premium:.1f}%',
        ha='center', fontsize=14, fontweight='bold',
        bbox=dict(boxstyle='round', facecolor='yellow', alpha=0.7))

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '11_credit_impact_analysis.png', dpi=300, bbox_inches='tight')
plt.close()

# ============================================================================
# CHART 12: Mileage Distribution
# ============================================================================
print("12. Generating mileage distribution...")
fig, ax = plt.subplots(figsize=(14, 7))

mileage_bins = [0, 50000, 100000, 150000, 200000, 300000, 500000, 1000000]
mileage_labels = ['0-50K', '50-100K', '100-150K', '150-200K', '200-300K', '300-500K', '500K+']
df_valid['mileage_range'] = pd.cut(df_valid['mileage_clean'], bins=mileage_bins, labels=mileage_labels)
mileage_dist = df_valid['mileage_range'].value_counts().reindex(mileage_labels)

colors = sns.color_palette("YlOrRd", len(mileage_dist))
bars = ax.bar(range(len(mileage_dist)), mileage_dist.values, color=colors, edgecolor='black', linewidth=1.5)
ax.set_xticks(range(len(mileage_dist)))
ax.set_xticklabels(mileage_labels, rotation=45, ha='right', fontweight='bold')
ax.set_ylabel('Number of Listings', fontweight='bold')
ax.set_title('Mileage Distribution: Number of Listings by Mileage Range (km)', fontweight='bold', fontsize=16, pad=20)

# Add value labels
for i, (bar, value) in enumerate(zip(bars, mileage_dist.values)):
    if pd.notna(value) and value > 0:
        pct = (value / df_valid['mileage_range'].notna().sum()) * 100
        ax.text(i, value + 100, f'{value:,.0f}\n({pct:.1f}%)', ha='center', fontweight='bold', fontsize=9)

plt.tight_layout()
plt.savefig(OUTPUT_DIR / '12_mileage_distribution.png', dpi=300, bbox_inches='tight')
plt.close()

print("\n" + "="*60)
print("✓ All charts generated successfully!")
print(f"✓ Charts saved to: {OUTPUT_DIR.absolute()}")
print("="*60)
print("\nGenerated charts:")
for i, chart_file in enumerate(sorted(OUTPUT_DIR.glob('*.png')), 1):
    print(f"  {i:2d}. {chart_file.name}")
