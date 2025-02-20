import streamlit as st
from datetime import datetime

def run_landing_page():
    st.title("Welcome to Renewals Assistant")
    # Data refresh section
    refresh_col1, refresh_col2 = st.columns([3, 1])
    with refresh_col1:
        st.markdown(f"*Last updated: {datetime.now().strftime('%d %b %Y %H:%M')}*")
    with refresh_col2:
        if st.button("🔄 Fetch Latest Data"):
            with st.spinner('Fetching latest renewals data...'):
                # Here you would typically call your data refresh function
                st.success('Data refreshed successfully!')

    # Priority actions
    st.header("⚡ Priority Actions")
    st.info("""
        **High Priority (Due Today)**
        - Review XYZ Ltd renewal - unusual claims pattern detected
        - Tech Inc rate adequacy below threshold
        
        **Medium Priority (This Week)**
        - 5 renewals entering 60-day window
        - Portfolio accumulation check needed for Property
    """)

    # Guide to app capabilities
    st.header("🎯 Making Decisions")
    st.markdown("""
        This app helps you make three key decisions:
        
        **1. Which renewals need attention first?**
        → Use the [Triage](#) view to:
        - See prioritised renewals based on risk score
        - Filter by time period, LoB, broker
        - Identify high-risk accounts
        
        **2. Should you pursue each renewal?**
        → Use the [Assessment](#) view to:
        - Compare YoY performance
        - Check risk appetite alignment
        - Review claims development
        - Make and document pursue/decline decisions
        
        **3. What terms should you offer?**
        → Use the [Terms](#) view to:
        - See model-driven recommendations
        - Check capacity availability
        - Review market conditions
        - Set final terms
    """)

    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Start Triage")
    with col2:
        st.button("Review Assessments")
    with col3:
        st.button("Set Terms")

if __name__ == "__main__":
    run_landing_page()