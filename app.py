import streamlit as st
from dataclasses import dataclass
from typing import List
import pandas as pd

@dataclass
class EMIRecord:
    month: int
    principal: float
    interest: float
    balance: float

class SmartLoanPlanner:
    def __init__(self, amount: float, annual_rate: float, monthly_emi: float):
        self.amount = amount
        self.annual_rate = annual_rate
        self.monthly_emi = monthly_emi
        self.monthly_rate = annual_rate / 1200
        self.records: List[EMIRecord] = []

    def simulate_repayment(self):
        balance = self.amount
        month = 0
        total_interest = 0.0
        total_principal = 0.0

        while balance > 0:
            month += 1
            interest = balance * self.monthly_rate
            principal_part = min(self.monthly_emi - interest, balance)
            if principal_part <= 0:
                st.error("⚠️ EMI too low. Loan can't be repaid.")
                break
            balance -= principal_part
            total_interest += interest
            total_principal += principal_part
            self.records.append(EMIRecord(month, round(principal_part, 2), round(interest, 2), round(balance, 2)))
        return month, round(total_interest, 2), round(total_principal, 2)

    def get_df(self):
        return pd.DataFrame([r.__dict__ for r in self.records])

# === Streamlit UI ===
st.set_page_config(page_title="Loan Repayment Tracker", layout="centered")
st.title("💰 Loan Repayment Tracker")

amount = st.number_input("Loan Amount (₹)", min_value=1000.0, step=100.0)
rate = st.number_input("Annual Interest Rate (%)", min_value=1.0, step=0.1)
emi = st.number_input("Monthly EMI (₹)", min_value=500.0, step=100.0)

if st.button("Generate Schedule"):
    planner = SmartLoanPlanner(amount, rate, emi)
    months, interest, principal = planner.simulate_repayment()
    df = planner.get_df()
    st.subheader(f"📊 Repayment Schedule ({months} months)")
    st.dataframe(df)

    st.subheader("💡 Summary")
    st.write(f"**Total Principal Paid:** ₹{principal}")
    st.write(f"**Total Interest Paid:** ₹{interest}")
    st.write(f"**Total Amount Paid:** ₹{interest + principal}")

    csv = df.to_csv(index=False).encode('utf-8')
    st.download_button("📥 Download CSV", data=csv, file_name='loan_schedule.csv', mime='text/csv')
