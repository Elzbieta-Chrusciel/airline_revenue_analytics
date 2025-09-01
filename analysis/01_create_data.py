# Airline Data Generation

import pandas as pd
import numpy as np
from datetime import datetime, timedelta
import os

print("Creating airline dataset...")

# Set seed for reproducible results
np.random.seed(42)

# Create data folder if it doesn't exist
os.makedirs('../data', exist_ok=True)

# =============================================================================
# CREATE FLIGHTS DATA
# =============================================================================

print("1. Creating flights...")

# Simple route list
routes = ['NYC-LAX', 'NYC-CHI', 'LAX-SF', 'CHI-MIA', 'NYC-BOS']
aircraft = ['A320', 'B737', 'A321']
capacities = [150, 180, 220]

# Generate 50,000 flights (smaller, more manageable)
n_flights = 50000
flight_data = []

for i in range(n_flights):
    # Pick random route and aircraft
    route = np.random.choice(routes)
    plane = np.random.choice(aircraft)
    capacity = np.random.choice(capacities)
    
    # Random date in 2023
    days_from_start = np.random.randint(0, 365)
    flight_date = datetime(2023, 1, 1) + timedelta(days=days_from_start)
    
    # Simple pricing - more expensive routes cost more
    if route == 'NYC-LAX':
        base_price = np.random.normal(400, 50)
    elif route == 'NYC-CHI':
        base_price = np.random.normal(300, 40)
    else:
        base_price = np.random.normal(250, 30)
    
    # Make sure price is reasonable
    base_price = max(base_price, 100)
    
    flight_data.append({
        'flight_id': f'FL{i+1:05d}',
        'route': route,
        'date': flight_date,
        'aircraft': plane,
        'capacity': capacity,
        'base_price': round(base_price, 2)
    })

# Convert to DataFrame and save
flights_df = pd.DataFrame(flight_data)
flights_df.to_csv('../data/flights.csv', index=False)
print(f"   Created {len(flights_df):,} flights")

# =============================================================================
# CREATE CUSTOMERS DATA
# =============================================================================

print("2. Creating customers...")

# Generate 15,000 customers (manageable size)
n_customers = 15000
customer_data = []

for i in range(n_customers):
    # Simple customer characteristics
    age = np.random.randint(18, 70)
    income = np.random.normal(60000, 20000)
    income = max(income, 25000)  # Minimum income
    
    # Business traveler or not (simple rule)
    if income > 80000 and age > 30:
        is_business = np.random.choice([0, 1], p=[0.4, 0.6])  # More likely business
    else:
        is_business = np.random.choice([0, 1], p=[0.8, 0.2])  # Less likely business
    
    customer_data.append({
        'customer_id': f'CU{i+1:05d}',
        'age': age,
        'income': round(income, 0),
        'is_business': is_business,
        'home_city': np.random.choice(['NYC', 'LAX', 'CHI', 'MIA', 'BOS'])
    })

customers_df = pd.DataFrame(customer_data)
customers_df.to_csv('../data/customers.csv', index=False)
print(f"   Created {len(customers_df):,} customers")

# =============================================================================
# CREATE BOOKINGS DATA  
# =============================================================================

print("3. Creating bookings...")

# Generate 150,000 bookings
n_bookings = 150000
booking_data = []

for i in range(n_bookings):
    # Pick a random flight and customer
    flight = flights_df.sample(1).iloc[0]
    customer = customers_df.sample(1).iloc[0]
    
    # Booking date (before flight date)
    days_before = np.random.randint(1, 90)  # Book 1-90 days in advance
    booking_date = flight['date'] - timedelta(days=days_before)
    
    # Price varies based on advance booking and customer type
    price = flight['base_price']
    
    # Last minute bookings cost more
    if days_before < 7:
        price *= 1.3
    # Early bookings get discount
    elif days_before > 60:
        price *= 0.85
    
    # Business travelers might pay more for premium
    if customer['is_business'] == 1:
        price *= np.random.uniform(1.0, 1.4)
    
    # Random variation
    price *= np.random.normal(1.0, 0.1)
    price = max(price, 100)  # Minimum price
    
    booking_data.append({
        'booking_id': f'BK{i+1:06d}',
        'flight_id': flight['flight_id'],
        'customer_id': customer['customer_id'],
        'booking_date': booking_date,
        'price_paid': round(price, 2),
        'advance_days': days_before,
        'passengers': np.random.choice([1, 2, 3], p=[0.7, 0.2, 0.1])
    })

bookings_df = pd.DataFrame(booking_data)
bookings_df.to_csv('../data/bookings.csv', index=False)
print(f"   Created {len(bookings_df):,} bookings")

# =============================================================================
# SHOW SUMMARY
# =============================================================================

print("\n✅ DATASET COMPLETE!")
print("=" * 30)
print(f"Flights:  {len(flights_df):,}")
print(f"Customers: {len(customers_df):,}")
print(f"Bookings: {len(bookings_df):,}")

print(f"\nTotal Revenue: ${bookings_df['price_paid'].sum():,.0f}")
print(f"Average Ticket: ${bookings_df['price_paid'].mean():.0f}")
print(f"Date Range: {flights_df['date'].min().date()} to {flights_df['date'].max().date()}")

print(f"\nRoutes: {', '.join(routes)}")
print(f"Files saved in ../data/ folder")

# Quick preview
print(f"\n📊 SAMPLE DATA:")
print("Flights sample:")
print(flights_df.head(3))
print(f"\nBookings sample:")  
print(bookings_df.head(3))