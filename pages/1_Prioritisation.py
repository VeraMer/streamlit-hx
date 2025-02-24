import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

import streamlit as st
import pandas as pd
import numpy as np
from datetime import datetime, timedelta

# handling plotly in cases where it's not intalled
try:
    import plotly.express as px
    import plotly.graph_objs as go
    plotly_available = True
except ImportError:
    st.warning("Plotly is not installed. Some visualizations may not display correctly.")
    plotly_available = False

def filter_dataframe(df, time_period, line_of_business, broker, sort_by):
    """
    Filter and sort the dataframe based on user selections
    """
    # Createcopy of the dataframe to avoid modifying original
    filtered_df = df.copy()
    
    # Time period filter
    current_date = datetime.now()
    if time_period == "Next 30 days":
        filtered_df = filtered_df[
            pd.to_datetime(filtered_df['Expiry_Date']) <= current_date + timedelta(days=30)
        ]
    elif time_period == "30-60 days":
        filtered_df = filtered_df[
            (pd.to_datetime(filtered_df['Expiry_Date']) > current_date + timedelta(days=30)) &
            (pd.to_datetime(filtered_df['Expiry_Date']) <= current_date + timedelta(days=60))
        ]
    elif time_period == "60-90 days":
        filtered_df = filtered_df[
            (pd.to_datetime(filtered_df['Expiry_Date']) > current_date + timedelta(days=60)) &
            (pd.to_datetime(filtered_df['Expiry_Date']) <= current_date + timedelta(days=90))
        ]
    
    # Line of Business Filter
    if line_of_business != "All":
        filtered_df = filtered_df[filtered_df['Line_of_Business'] == line_of_business]
    
    # Broker Filter
    if broker != "All":
        filtered_df = filtered_df[filtered_df['Broker'] == broker]
    
    # Sorting
    if sort_by == "Risk Score":
        filtered_df = filtered_df.sort_values('Risk_Score', ascending=False)
    elif sort_by == "Premium Size":
        filtered_df = filtered_df.sort_values('Premium', ascending=False)
    elif sort_by == "Expiry Date":
        filtered_df = filtered_df.sort_values('Expiry_Date')
    
    return filtered_df

def create_renewals_insights_charts(filtered_df):
    """
    Create visualizations for renewals insights
    """
    # Create two columns for charts
    chart_col1, chart_col2 = st.columns(2)

    if plotly_available:
        # Chart 1: Risk Score vs Premium Scatter Plot
        with chart_col1:
            st.subheader("Risk Score vs Premium")
            fig1 = px.scatter(
                filtered_df, 
                x='Risk_Score', 
                y='Premium', 
                color='Priority',
                hover_data=['Policy_Ref', 'Insured'],
                title='Risk Score vs Premium by Priority',
                labels={'Risk_Score': 'Risk Score', 'Premium': 'Premium (£)'}
            )
            fig1.update_layout(height=400)
            st.plotly_chart(fig1, use_container_width=True)

        # Chart 2: Rate Change Distribution by Line of Business
        with chart_col2:
            st.subheader("Rate Changes by Line of Business")
            fig2 = px.box(
                filtered_df, 
                x='Line_of_Business', 
                y='Rate_Change', 
                color='Priority',
                title='Rate Change Distribution',
                labels={'Rate_Change': 'Rate Change', 'Line_of_Business': 'Line of Business'}
            )
            fig2.update_layout(height=400)
            st.plotly_chart(fig2, use_container_width=True)
    else:
        # Fallback visualizations using Streamlit's native charts
        with chart_col1:
            st.subheader("Risk Score vs Premium")
            st.scatter_chart(
                filtered_df, 
                x='Risk_Score', 
                y='Premium',
                color='Priority'
            )
        
        with chart_col2:
            st.subheader("Rate Changes by Line of Business")
            # Group by Line of Business and calculate mean rate change
            lob_summary = filtered_df.groupby('Line_of_Business')['Rate_Change'].mean().reset_index()
            st.bar_chart(lob_summary, x='Line_of_Business', y='Rate_Change')

def run_triage_view():
    st.title("Renewals Triage")

    # Generate sample data with more comprehensive information
    data = {
        'Policy_Ref': ['POL001', 'POL002', 'POL003', 'POL004', 'POL005', 'POL006', 'POL007', 'POL008', 'POL009'],
        'Insured': ['ABC Corp', 'XYZ Ltd', 'Tech Inc', 'Global Enterprises', 'Innovative Solutions', 
                    'Energy Partners', 'Financial Services', 'Manufacturing Co', 'Retail Giant'],
        'Expiry_Date': [
            (datetime.now() + timedelta(days=x)).strftime('%Y-%m-%d') 
            for x in [30, 45, 60, 20, 75, 90, 40, 55, 85]
        ],
        'Premium': [1000000, 2500000, 500000, 3000000, 1500000, 4000000, 2000000, 1800000, 3500000],
        'Claims_Ratio': [0.65, 0.40, 0.85, 0.55, 0.75, 0.30, 0.60, 0.45, 0.50],
        'Rate_Change': [0.05, 0.08, -0.02, 0.06, 0.03, 0.10, 0.04, 0.07, 0.05],
        'Risk_Score': [85, 72, 45, 90, 60, 95, 80, 70, 88],
        'Priority': ['High', 'Medium', 'Low', 'High', 'Medium', 'High', 'Medium', 'Low', 'High'],
        'Line_of_Business': ['Property', 'Casualty', 'Marine', 'Energy', 'Property', 'Energy', 
                             'Casualty', 'Marine', 'Property'],
        'Broker': ['Aon', 'WTW', 'Marsh', 'Other', 'Aon', 'WTW', 'Marsh', 'Other', 'Aon']
    }
    df = pd.DataFrame(data)

    # Filters row
    col1, col2, col3, col4 = st.columns(4)
    with col1:
        time_period = st.selectbox("Time Period", ["Next 30 days", "30-60 days", "60-90 days", "All"])
    with col2:
        line_of_business = st.selectbox("Line of Business", ["All", "Property", "Casualty", "Marine", "Energy"])
    with col3:
        broker = st.selectbox("Broker", ["All", "Aon", "WTW", "Marsh", "Other"])
    with col4:
        sort_by = st.selectbox("Sort by", ["Risk Score", "Premium Size", "Expiry Date"])

    # Apply filters and sorting
    filtered_df = filter_dataframe(df, time_period, line_of_business, broker, sort_by)

    # Calculate dynamic metrics
    total_renewals = len(filtered_df)
    total_premium = filtered_df['Premium'].sum()
    avg_rate_change = filtered_df['Rate_Change'].mean()
    high_priority = filtered_df[filtered_df['Priority'] == 'High'].shape[0]

    # Key metrics row
    metrics_cols = st.columns(4)
    with metrics_cols[0]:
        st.metric("Total Renewals", f"{total_renewals}")
    with metrics_cols[1]:
        st.metric("Total Premium", f"£{total_premium:,.0f}")
    with metrics_cols[2]:
        st.metric("Avg Rate Change", f"{avg_rate_change:+.1%}")
    with metrics_cols[3]:
        st.metric("High Priority", f"{high_priority}")

    # Create insights charts
    create_renewals_insights_charts(filtered_df)

    # Main renewals grid
    st.dataframe(
        filtered_df.style.format({
            'Premium': '£{:,.0f}',
            'Claims_Ratio': '{:.1%}',
            'Rate_Change': '{:+.1%}',
            'Risk_Score': '{:.0f}'
        }).applymap(
            lambda x: 'background-color: #ffcccc' if x == 'High' 
            else ('background-color: #ffffcc' if x == 'Medium' 
            else 'background-color: #ccffcc'),
            subset=['Priority']
        ),
        use_container_width=True
    )

    # Action buttons
    col1, col2, col3 = st.columns(3)
    with col1:
        st.button("Export to Excel")
    with col2:
        st.button("Generate Reports")
    with col3:
        st.button("Send as Email")

if __name__ == "__main__":
    run_triage_view()
