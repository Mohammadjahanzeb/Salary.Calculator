import streamlit as st
import plotly.graph_objs as go

st.set_page_config(page_title="Smart Salary Calculator", layout="wide")

st.title("📊 Smart Salary Calculator")

# Initialize session_state for each year
for year in [2025, 2026, 2027]:
    for key in [f"inc_{year}", f"ded_{year}"]:
        if key not in st.session_state:
            st.session_state[key] = []

years = st.multiselect("Select Year(s) for Calculation", options=[2025, 2026, 2027], default=[2025])

summary_data = []

for year in years:
    st.markdown(f"---\n## Year: {year}")
    with st.form(f"form_{year}"):
        col1, col2 = st.columns(2)

        with col1:
            base = st.number_input(f"Basic Salary (PKR) for {year}", min_value=0.0, step=1000.0, key=f"base_{year}")
            adj_pct = st.number_input(f"Adjustment (%)", value=0.0, step=0.5, key=f"adj_pct_{year}")
            adjusted_base = base + (adj_pct / 100) * base
            st.info(f"Adjusted Basic Salary: PKR {adjusted_base:,.2f}")

            housing = 0.45 * adjusted_base
            utility = 0.10 * adjusted_base
            cola_pct = st.number_input("COLA (%)", value=0.0, step=0.5, key=f"cola_{year}")
            cola = (cola_pct / 100) * adjusted_base
            extra_pct = st.number_input("Extra Allowance (%)", value=0.0, step=0.5, key=f"extra_pct_{year}")
            extra = (extra_pct / 100) * adjusted_base

        with col2:
            cpi = st.number_input("Consumer Price Index (CPI)", value=0.0, step=0.1, key=f"cpi_{year}")
            if year == 2025:
                current_salary = st.number_input("Current Gross Salary (2025)", min_value=0.0, step=1000.0, key="current_2025")

            # --- Additional Income
            st.subheader("Additional Income")
            inc_container = st.container()
            for i, item in enumerate(st.session_state[f"inc_{year}"]):
                cols = inc_container.columns([3, 2])
                item["title"] = cols[0].text_input("Title", value=item["title"], key=f"inc_title_{year}_{i}")
                item["amount"] = cols[1].number_input("Amount", value=item["amount"], min_value=0.0, key=f"inc_amt_{year}_{i}")

            inc_col_add, inc_col_remove = st.columns([1, 1])
            if inc_col_add.button("➕ Add Income", key=f"add_inc_{year}"):
                st.session_state[f"inc_{year}"].append({"title": "", "amount": 0.0})
            if inc_col_remove.button("➖ Remove Last Income", key=f"rm_inc_{year}"):
                if st.session_state[f"inc_{year}"]:
                    st.session_state[f"inc_{year}"].pop()

            # --- Deductions
            st.subheader("Deductions")
            ded_container = st.container()
            for i, item in enumerate(st.session_state[f"ded_{year}"]):
                cols = ded_container.columns([3, 2])
                item["title"] = cols[0].text_input("Title", value=item["title"], key=f"ded_title_{year}_{i}")
                item["amount"] = cols[1].number_input("Amount", value=item["amount"], min_value=0.0, key=f"ded_amt_{year}_{i}")

            ded_col_add, ded_col_remove = st.columns([1, 1])
            if ded_col_add.button("➕ Add Deduction", key=f"add_ded_{year}"):
                st.session_state[f"ded_{year}"].append({"title": "", "amount": 0.0})
            if ded_col_remove.button("➖ Remove Last Deduction", key=f"rm_ded_{year}"):
                if st.session_state[f"ded_{year}"]:
                    st.session_state[f"ded_{year}"].pop()

        if st.form_submit_button("🧮 Calculate"):
            total_income = adjusted_base + housing + utility + cola + extra + sum(i["amount"] for i in st.session_state[f"inc_{year}"])
            total_deductions = sum(d["amount"] for d in st.session_state[f"ded_{year}"])
            net_salary = total_income - total_deductions

            st.success(f"💼 Gross Salary: PKR {total_income:,.2f}")
            st.warning(f"📉 Deductions: PKR {total_deductions:,.2f}")
            st.success(f"🧾 Net Salary: PKR {net_salary:,.2f}")

            if year == 2025 and "current_salary" in locals() and current_salary > 0:
                diff = net_salary - current_salary
                pct = (diff / current_salary) * 100
                st.info(f"📈 Change from Current Salary: {'+' if diff >= 0 else ''}{diff:,.2f} PKR ({pct:.2f}%)")

            # Save data for summary chart
            summary_data.append({
                "year": year,
                "gross": total_income,
                "net": net_salary,
                "deductions": total_deductions,
                "cpi": cpi
            })

# --- 📊 Summary Chart
if summary_data:
    st.markdown("## 📊 Year-wise Salary Comparison")
    fig = go.Figure()
    years = [d["year"] for d in summary_data]

    fig.add_trace(go.Bar(name="Gross Salary", x=years, y=[d["gross"] for d in summary_data]))
    fig.add_trace(go.Bar(name="Net Salary", x=years, y=[d["net"] for d in summary_data]))
    fig.add_trace(go.Bar(name="Deductions", x=years, y=[d["deductions"] for d in summary_data]))

    fig.update_layout(barmode="group", title="Salary Comparison", xaxis_title="Year", yaxis_title="PKR")
    st.plotly_chart(fig, use_container_width=True)
