# Save this as app.py and run with: streamlit run app.py

import streamlit as st

def calculate_balances(names, expenses):
    total = sum(expenses)
    per_person = total / len(names)
    balances = {}
    for i in range(len(names)):
        balances[names[i]] = round(expenses[i] - per_person, 2)
    return balances, total, per_person

def generate_summary(balances):
    summary = []
    debtors = {k: -v for k, v in balances.items() if v < 0}
    creditors = {k: v for k, v in balances.items() if v > 0}

    debtor_names = list(debtors.keys())
    creditor_names = list(creditors.keys())

    i, j = 0, 0
    while i < len(debtor_names) and j < len(creditor_names):
        debtor = debtor_names[i]
        creditor = creditor_names[j]
        amount = min(debtors[debtor], creditors[creditor])

        summary.append(f"{debtor} should pay ₹{amount:.2f} to {creditor}")

        debtors[debtor] -= amount
        creditors[creditor] -= amount

        if debtors[debtor] == 0:
            i += 1
        if creditors[creditor] == 0:
            j += 1

    return summary

# Streamlit UI
st.title("Smart Expense Splitter")
st.markdown("Split group expenses fairly and view who owes whom!")

with st.form("expense_form"):
    num_people = st.number_input("Enter number of people", min_value=2, max_value=20, step=1)
    names = []
    expenses = []

    for i in range(int(num_people)):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input(f"Name of person {i+1}", key=f"name_{i}")
        with col2:
            amount = st.number_input(f"Amount paid by {name or 'person'}", min_value=0.0, step=1.0, key=f"amt_{i}")
        
        names.append(name if name else f"Person {i+1}")
        expenses.append(amount)

    submitted = st.form_submit_button("Calculate")

if submitted:
    balances, total, per_person = calculate_balances(names, expenses)

    st.subheader("Summary:")
    st.write(f"*Total Expense:* ₹{total:.2f}")
    st.write(f"*Each person should pay:* ₹{per_person:.2f}")

    st.subheader("Individual Balances:")
    for person, balance in balances.items():
        if balance > 0:
            st.success(f"{person} should receive ₹{balance}")
        elif balance < 0:
            st.error(f"{person} should pay ₹{abs(balance)}")
        else:
            st.info(f"{person} is settled up.")

    st.subheader("Settlement Plan:")
    summary = generate_summary(balances)
    for line in summary:
        st.write(line)

    # Download report
    report = f"Expense Summary\nTotal: ₹{total:.2f}\nPer Person: ₹{per_person:.2f}\n\nBalances:\n"
    for person, balance in balances.items():
        status = "gets" if balance > 0 else "owes" if balance < 0 else "settled"
        report += f"{person}: {status} ₹{abs(balance):.2f}\n"
    report += "\nSettlement Plan:\n" + "\n".join(summary)

    st.download_button("Download Report", report, file_name="expense_report.txt")