import pandas as pd
import numpy as np

# Read the original CSV file
df = pd.read_csv('phone_active_use_scores_full.csv')

# Dictionary of known prices for released phones (in USD)
known_prices = {
    'Apple iPhone 15': 799,
    'Apple iPhone 15 Plus': 899,
    'Apple iPhone 15 Pro': 999,
    'Apple iPhone 15 Pro Max': 1199,
    'Samsung Galaxy S24': 799,
    'Samsung Galaxy S24+': 999,
    'Samsung Galaxy S24 Ultra': 1199,
    'Google Pixel 8': 699,
    'Google Pixel 8 Pro': 999,
    'OnePlus 12': 799,
    'Xiaomi 14': 899,
    'Xiaomi 14 Ultra': 999,
    'Nothing Phone (2)': 499,
    'Motorola Edge 50 Ultra': 899,
    'Sony Xperia 1 V': 1399,
    'Sony Xperia 5 V': 999,
    'Sony Xperia 10 V': 399,
    'Huawei Mate 50 Pro': 1199,
    'Samsung Galaxy Z Fold5': 1799,
    'Samsung Galaxy Z Flip5': 999,
    'OnePlus Open': 1699,
    'Google Pixel 8a': 499,
    'Samsung Galaxy A54': 449,
    'Xiaomi 13 Pro': 999,
    'Xiaomi 13 Ultra': 899,
    'Honor Magic V2': 1199,
    'Samsung Galaxy S23': 799,
    'Samsung Galaxy S23+': 999,
    'Samsung Galaxy S23 Ultra': 1199,
    'Samsung Galaxy S23 FE': 599,
    'Huawei MatePad Pro 13.2': 899,
    'Huawei Mate XT Ultimate': 1999,
}

# Function to estimate price based on phone characteristics
def estimate_price(row):
    # If we have a known price, use it
    if row['phone'] in known_prices:
        return known_prices[row['phone']]
    
    # Base price estimation on company and model characteristics
    base_price = 0
    
    # Company base prices
    company_base = {
        'Apple': 999,
        'Samsung': 899,
        'Google': 799,
        'OnePlus': 699,
        'Xiaomi': 599,
        'Nothing': 499,
        'Motorola': 599,
        'Sony': 999,
        'Huawei': 899,
        'Honor': 799,
        'Oppo': 699,
        'vivo': 699,
        'Realme': 599,
        'ZTE': 599,
        'Asus': 699,
        'Tecno': 399,
        'Infinix': 299,
        'HMD': 299
    }
    
    base_price = company_base.get(row['company'], 699)
    
    # Adjust based on model characteristics
    if 'Ultra' in row['phone'] or 'Pro Max' in row['phone']:
        base_price += 300
    elif 'Pro' in row['phone'] or 'Plus' in row['phone']:
        base_price += 200
    elif 'Lite' in row['phone'] or 'SE' in row['phone']:
        base_price -= 200
    
    # Adjust for year (newer models tend to be more expensive)
    year_diff = 2025 - row['year_of_release']
    base_price -= year_diff * 50
    
    # Ensure price is within reasonable bounds
    return max(299, min(1999, base_price))

# Add price column
df['price_in_usd'] = df.apply(estimate_price, axis=1)

# Save the updated dataset
df.to_csv('phone_active_use_scores_with_prices.csv', index=False)
print("Updated dataset saved with price information.") 