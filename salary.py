import streamlit as st

st.set_page_config(page_title="Smart Salary Calculator", layout="wide")

st.title("📊 Smart Salary Calculator")

# Define year range from 2025 to 2027 only
years = st.multiselect("Select Year(s) for Calculation", options=[2025, 2026, 2027], default=[2025])

for year in years:
    st.markdown(f"---\n## Year: {year}")

    with st.form(key=f"form_{year}"):
        col1, col2 = st.columns(2)

        with col1:
            basic_salary = st.number_input(f"Basic Salary (PKR) for {year}", min_value=0.0, step=1000.0, format="%.2f")
            cola_percentage = st.number_input(f"COLA %", min_value=0.0, max_value=100.0, step=1.0, format="%.2f")
            extra_percentage = st.number_input("Additional Allowance (%) of Basic", min_value=0.0, max_value=100.0, step=1.0, format="%.2f")
            cpi = st.number_input("Consumer Price Index (CPI)", min_value=0.0, step=0.1, format="%.2f")

        with col2:
            if year == 2025:
                current_salary = st.number_input("Current Gross Salary (2025)", min_value=0.0, step=1000.0, format="%.2f")

            st.subheader("Additional Income")
            add_income = []
            income_count = st.number_input(f"Number of Additional Income Fields", 0, 10, key=f"inc_count_{year}")
            for i in range(int(income_count)):
                inc_col1, inc_col2 = st.columns([3, 2])
                with inc_col1:
                    title = st.text_input(f"Income Title {i+1}", key=f"inc_title_{year}_{i}")
                with inc_col2:
                    amount = st.number_input(f"Amount", key=f"inc_amt_{year}_{i}", min_value=0.0, step=100.0)
                add_income.append(amount)

            st.subheader("Deductions")
            deductions = []
            deduct_count = st.number_input(f"Number of Deduction Fields", 0, 10, key=f"deduct_count_{year}")
            for i in range(int(deduct_count)):
                dec_col1, dec_col2 = st.columns([3, 2])
                with dec_col1:
                    title = st.text_input(f"Deduction Title {i+1}", key=f"deduct_title_{year}_{i}")
                with dec_col2:
                    amount = st.number_input(f"Amount", key=f"deduct_amt_{year}_{i}", min_value=0.0, step=100.0)
                deductions.append(amount)

        submitted = st.form_submit_button("🧮 Calculate Salary")

        if submitted:
            housing_rent = 0.45 * basic_salary
            utility = 0.10 * basic_salary
            cola = (cola_percentage / 100) * basic_salary
            additional_percent = (extra_percentage / 100) * basic_salary
            total_income = basic_salary + housing_rent + utility + cola + additional_percent + sum(add_income)
            total_deductions = sum(deductions)
            net_salary = total_income - total_deductions

            st.success(f"💼 Gross Salary for {year}: PKR {total_income:,.2f}")
            st.warning(f"📉 Total Deductions: PKR {total_deductions:,.2f}")
            st.success(f"🧾 Net Salary for {year}: PKR {net_salary:,.2f}")

            if year == 2025 and current_salary > 0:
                diff = net_salary - current_salary
                pct_change = (diff / current_salary) * 100 if current_salary != 0 else 0
                st.info(f"📈 Change from Current Salary: {'+' if diff >= 0 else ''}{diff:,.2f} PKR ({pct_change:.2f}%)")
