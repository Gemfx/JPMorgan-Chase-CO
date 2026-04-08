import pandas as pd

def price_contract(injection_dates, withdrawal_dates, 
                   injection_prices, withdrawal_prices,
                   rate, max_volume, storage_cost_per_day):
    
    total_profit = 0
    current_volume = 0

    for i in range(len(injection_dates)):
        
        # Convert dates
        inj_date = pd.to_datetime(injection_dates[i])
        wd_date = pd.to_datetime(withdrawal_dates[i])
        
        # Days in storage
        days_stored = (wd_date - inj_date).days
        
        # Volume we can inject (respect max storage)
        volume = min(rate, max_volume - current_volume)
        
        # Update stored volume
        current_volume += volume
        
        # Cost to buy gas
        purchase_cost = volume * injection_prices[i]
        
        # Revenue from selling gas
        selling_revenue = volume * withdrawal_prices[i]
        
        # Storage cost
        storage_cost = volume * storage_cost_per_day * days_stored
        
        # Profit for this cycle
        profit = selling_revenue - purchase_cost - storage_cost
        
        total_profit += profit
        
        # After withdrawal, storage reduces
        current_volume -= volume

    return total_profit

injection_dates = ["2023-01-01", "2023-02-01"]
withdrawal_dates = ["2023-03-01", "2023-04-01"]

injection_prices = [2.5, 2.7]
withdrawal_prices = [3.0, 3.2]

rate = 1000
max_volume = 2000
storage_cost_per_day = 0.01

value = price_contract(
    injection_dates,
    withdrawal_dates,
    injection_prices,
    withdrawal_prices,
    rate,
    max_volume,
    storage_cost_per_day
)

print("Contract Value:", value)