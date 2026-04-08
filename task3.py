import pandas as pd
from sklearn.linear_model import LogisticRegression

df = pd.read_csv("Loan_Data.csv")

# Features (remove default and customer_id)
X = df.drop(['default', 'customer_id'], axis=1)
y = df['default']

model = LogisticRegression(max_iter=1000)
model.fit(X, y)
sample_borrower = {
    'credit_lines_outstanding': 3,
    'loan_amt_outstanding': 20000,
    'total_debt_outstanding': 15000,
    'income': 50000,
    'years_employed': 5,
    'fico_score': 650
}
def expected_loss(input_data, loan_amount):
    import pandas as pd
    
    input_df = pd.DataFrame([input_data])
    
    pd_value = model.predict_proba(input_df)[0][1]
    
    recovery_rate = 0.1
    
    expected_loss = pd_value * loan_amount * (1 - recovery_rate)
    
    return expected_loss
loan_amount = 20000

print(expected_loss(sample_borrower, loan_amount))