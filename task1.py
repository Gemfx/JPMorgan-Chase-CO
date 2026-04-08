import pandas as pd
import matplotlib.pyplot as plt

# Load dataset
df = pd.read_csv("Nat_Gas.csv")

# Convert Date column
df['Dates'] = pd.to_datetime(df['Dates'])

print(df.head())

# Plot
plt.plot(df['Dates'], df['Prices'])
plt.xlabel("Dates")
plt.ylabel("Prices")
plt.title("Natural Gas Prices Over Time")
plt.show()

df['Days'] = (df['Dates'] - df['Dates'].min()).dt.days

from sklearn.linear_model import LinearRegression
import numpy as np

X = df[['Days']]
y = df['Prices']

model = LinearRegression()
model.fit(X, y)

def predict_price(date_str):
    date = pd.to_datetime(date_str)
    days = (date - df['Dates'].min()).days
    
    input_data = pd.DataFrame([[days]], columns=['Days'])
    predicted_price = model.predict(input_data)
    
    return predicted_price[0]

future_dates = pd.date_range(start=df['Dates'].max(), periods=12, freq='ME')

future_days = (future_dates - df['Dates'].min()).days

future_prices = model.predict(future_days.values.reshape(-1,1))

plt.plot(df['Dates'], df['Prices'], label="Actual")
plt.plot(future_dates, future_prices, label="Predicted", linestyle='--')
plt.legend()
plt.show()