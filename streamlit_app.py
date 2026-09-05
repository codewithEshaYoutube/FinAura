import streamlit as st
import streamlit.components.v1 as components
import json

# =============================================================================
# 1. SETUP STREAMLIT PAGE
# =============================================================================
st.set_page_config(
    page_title="FinAura HTML Dashboard",
    page_icon="💸",
    layout="wide"
)

# =============================================================================
# 2. DEFINE YOUR DATA (Simulating Session State)
# =============================================================================
# In a real app, this would come from st.session_state or a database
financial_data = {
    "income": 4500.00,
    "transactions": [
        { "desc": "Iced Coffee", "amount": 5.50, "category": "Joy", "date": "Today" },
        { "desc": "Rent Payment", "amount": 1500.00, "category": "Essential", "date": "Yesterday" },
        { "desc": "Spotify Premium", "amount": 12.99, "category": "Essential", "date": "Yesterday" },
        { "desc": "Concert Tickets", "amount": 120.00, "category": "Joy", "date": "2 days ago" },
        { "desc": "Late Night Taco Bell", "amount": 25.00, "category": "Oops", "date": "2 days ago" }
    ],
    "isSetup": True # Set to False to see the landing page
}

# =============================================================================
# 3. READ THE HTML FILE
# =============================================================================
try:
    with open('dashboard.html', 'r', encoding='utf-8') as f:
        html_code = f.read()
except FileNotFoundError:
    st.error("dashboard.html not found! Please save the HTML file in the same directory.")
    st.stop()

# =============================================================================
# 4. INJECT DATA INTO HTML (The Magic Part)
# =============================================================================
# We need to convert Python data to a JSON string that JavaScript can understand.
data_json_string = json.dumps(financial_data)

# We look for the line "let state = {" in the HTML and replace the default data
# with our actual data from Python.
html_code = html_code.replace("let state = {", f"let state = {data_json_string}")

# =============================================================================
# 5. RENDER THE HTML
# =============================================================================
# We render the HTML in an iframe.
# height=1000 ensures the dashboard has enough room to scroll.
components.html(
    html_code,
    height=1000,
    scrolling=True
)

# =============================================================================
# 6. (OPTIONAL) ADD STREAMLIT CONTROLS
# =============================================================================
# You can still use native Streamlit elements below the HTML dashboard
st.markdown("---")
st.subheader("Native Streamlit Controls Below")

new_income = st.number_input("Update Income (Updates Dashboard on Refresh)", value=financial_data['income'])
if st.button("Save Changes"):
    # Note: In a real app, you would save this to a database or session state
    # and rerun the app to update the HTML.
    st.success("Income updated! (Note: The HTML above is static for this demo)")
