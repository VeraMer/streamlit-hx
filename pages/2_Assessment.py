import streamlit as st
import pandas as pd
import numpy as np

def load_policy_data():
    """
    Generate sample policy data for demonstration
    """
    policies = [
        {
            "Policy_Ref": "POL-001",
            "Client_Name": "ABC Corp",
            "Current_Premium": 1000000,
            "Claims_Ratio": 0.65,
            "Technical_Rate_Change": 0.125,
            "Market_Rate_Change": 0.082,
            "Risk_Score": 85,
            "Portfolio_Impact": "Medium",
            "Exposure_Changes": {
                "Revenue_Change": 0.15,
                "New_Territories": 2,
                "Products_Change": "No change"
            },
            "Claims_Development": {
                "New_Claims": 2,
                "Largest_Claim": 250000,
                "Claims_Frequency_Change": 0.05
            },
            "Risk_Profile": {
                "Risk_Score_Change": 10,
                "Cat_Exposure_Change": -0.05,
                "Risk_Controls": "Improved"
            },
            "Risk_Appetite": {
                "Within": ["Premium size", "Territory", "Industry sector"],
                "Outside": ["Claims ratio trending up", "Accumulation in key zone"]
            }
        },
        {
            "Policy_Ref": "POL-002",
            "Client_Name": "XYZ Manufacturing",
            "Current_Premium": 1500000,
            "Claims_Ratio": 0.55,
            "Technical_Rate_Change": 0.10,
            "Market_Rate_Change": 0.07,
            "Risk_Score": 75,
            "Portfolio_Impact": "Low",
            "Exposure_Changes": {
                "Revenue_Change": 0.10,
                "New_Territories": 1,
                "Products_Change": "+1 new product line"
            },
            "Claims_Development": {
                "New_Claims": 1,
                "Largest_Claim": 150000,
                "Claims_Frequency_Change": 0.02
            },
            "Risk_Profile": {
                "Risk_Score_Change": 5,
                "Cat_Exposure_Change": -0.03,
                "Risk_Controls": "Stable"
            },
            "Risk_Appetite": {
                "Within": ["Premium size", "Territory", "Industry sector", "Claims ratio"],
                "Outside": ["Emerging market exposure"]
            }
        },
        {
            "Policy_Ref": "POL-003",
            "Client_Name": "Global Energy Solutions",
            "Current_Premium": 2000000,
            "Claims_Ratio": 0.70,
            "Technical_Rate_Change": 0.15,
            "Market_Rate_Change": 0.10,
            "Risk_Score": 90,
            "Portfolio_Impact": "High",
            "Exposure_Changes": {
                "Revenue_Change": 0.20,
                "New_Territories": 3,
                "Products_Change": "+2 new product lines"
            },
            "Claims_Development": {
                "New_Claims": 3,
                "Largest_Claim": 500000,
                "Claims_Frequency_Change": 0.08
            },
            "Risk_Profile": {
                "Risk_Score_Change": 15,
                "Cat_Exposure_Change": 0.02,
                "Risk_Controls": "Needs improvement"
            },
            "Risk_Appetite": {
                "Within": ["Premium size"],
                "Outside": ["Claims ratio", "Risk score", "Cat exposure"]
            }
        }
    ]
    return pd.DataFrame(policies)

def display_policy_details(policy):
    """
    Display detailed information for a selected policy
    """
    # Header with key info
    col1, col2, col3 = st.columns(3)
    with col1:
        st.metric("Current Premium", f"£{policy['Current_Premium']:,}")
        st.metric("Claims Ratio", f"{policy['Claims_Ratio']:.1%}")
    with col2:
        st.metric("Technical Rate Change", f"{policy['Technical_Rate_Change']:+.1%}")
        st.metric("Market Rate Change", f"{policy['Market_Rate_Change']:+.1%}")
    with col3:
        st.metric("Risk Score", f"{policy['Risk_Score']}")
        st.metric("Portfolio Impact", policy['Portfolio_Impact'])

    # YoY Comparison
    st.subheader("Year on Year Changes")
    yoy_cols = st.columns(3)
    
    with yoy_cols[0]:
        st.markdown("**Exposure Changes**")
        st.markdown(f"- Revenue: {policy['Exposure_Changes']['Revenue_Change']:+.1%}")
        st.markdown(f"- Territories: +{policy['Exposure_Changes']['New_Territories']} new")
        st.markdown(f"- Products: {policy['Exposure_Changes']['Products_Change']}")
        
    with yoy_cols[1]:
        st.markdown("**Claims Development**")
        st.markdown(f"- {policy['Claims_Development']['New_Claims']} new claims reported")
        st.markdown(f"- Largest claim: £{policy['Claims_Development']['Largest_Claim']:,}")
        st.markdown(f"- Claims frequency: {policy['Claims_Development']['Claims_Frequency_Change']:+.1%}")
        
    with yoy_cols[2]:
        st.markdown("**Risk Profile**")
        st.markdown(f"- Risk Score: +{policy['Risk_Profile']['Risk_Score_Change']} points")
        st.markdown(f"- Cat exposure: {policy['Risk_Profile']['Cat_Exposure_Change']:+.1%}")
        st.markdown(f"- Risk controls: {policy['Risk_Profile']['Risk_Controls']}")

    # Risk Appetite Assessment
    st.subheader("Risk Appetite Assessment")
    appetite_cols = st.columns(2)
    
    with appetite_cols[0]:
        st.markdown("**Within Appetite**")
        for item in policy['Risk_Appetite']['Within']:
            st.markdown(f"✅ {item}")
        
    with appetite_cols[1]:
        st.markdown("**Outside Appetite**")
        for item in policy['Risk_Appetite']['Outside']:
            st.markdown(f"❌ {item}")

    # Decision and Comments
    st.subheader("Decision")
    col1, col2 = st.columns(2)
    
    with col1:
        decision = st.radio(
            "Renewal Decision",
            ["Pursue - Standard Terms", "Pursue - Modified Terms", "Decline"],
            key=f"decision_{policy['Policy_Ref']}"
        )
        
    with col2:
        rationale = st.text_area(
            "Decision Rationale", 
            height=100,
            key=f"rationale_{policy['Policy_Ref']}"
        )

    # Action Buttons
    action_cols = st.columns(3)
    with action_cols[0]:
        st.button("Save Decision", key=f"save_{policy['Policy_Ref']}")
    with action_cols[1]:
        st.button("Generate Referral", key=f"referral_{policy['Policy_Ref']}")
    with action_cols[2]:
        st.button("Proceed to Terms", key=f"terms_{policy['Policy_Ref']}")

def run_assessment_view():
    # Load policy data
    policies_df = load_policy_data()

    # Main page title
    st.title("Renewal Assessment")

    # Bulk Action Section
    st.subheader("Bulk Actions")
    bulk_cols = st.columns(3)
    with bulk_cols[0]:
        bulk_decision = st.selectbox(
            "Bulk Renewal Decision", 
            ["No Bulk Action", "Pursue - Standard Terms", "Pursue - Modified Terms", "Decline"]
        )
    with bulk_cols[1]:
        bulk_filter = st.multiselect(
            "Filter Policies",
            ["High Impact", "Medium Impact", "Low Impact", "Above Risk Threshold"]
        )
    with bulk_cols[2]:
        if st.button("Apply to All"):
            if bulk_decision != "No Bulk Action":
                # Apply bulk decision
                policies_df = apply_bulk_decision(policies_df, bulk_decision, bulk_filter)
                st.success(f"Bulk action '{bulk_decision}' applied to selected policies!")
            else:
                st.warning("Please select a bulk action first.")

    # Policy Selection
    st.subheader("By Policy Selection")
    
    # Multi-select policies
    selected_policies = st.multiselect(
        "Select Policies to Review",
        policies_df['Policy_Ref'] + " - " + policies_df['Client_Name']
    )

    # Display selected policies
    if selected_policies:
        for policy_display in selected_policies:
            # Extract Policy Reference
            policy_ref = policy_display.split(" - ")[0]
            
            # Find the corresponding policy
            policy = policies_df[policies_df['Policy_Ref'] == policy_ref].to_dict('records')[0]
            
            # Expandable section for each policy
            with st.expander(f"{policy_display}"):
                display_policy_details(policy)

    # Optional: Policy Summary Table
    st.subheader("Policy Overview")
    overview_df = policies_df[['Policy_Ref', 'Client_Name', 'Current_Premium', 'Risk_Score', 'Portfolio_Impact']]
    overview_df['Current_Premium'] = overview_df['Current_Premium'].apply(lambda x: f"£{x:,}")
    st.dataframe(overview_df, use_container_width=True)

if __name__ == "__main__":
    run_assessment_view()