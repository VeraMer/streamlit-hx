import streamlit as st
import pandas as pd
import numpy as np

def load_terms_data():
    """
    Generate sample terms data for demonstration
    """
    return {
        'policies': [
            {
                'Policy_Ref': 'POL-001',
                'Client_Name': 'ABC Corp',
                'Technical_Premium': 1125000,
                'Market_Premium': 1080000,
                'Recommended_Premium': 1100000,
                'Premium_Change': 0.10,
                'Terms': {
                    'Premium': {
                        'Expiring': 1000000,
                        'Model': 1125000,
                        'Market': 1080000,
                        'Proposed': 1100000
                    },
                    'Deductible': {
                        'Expiring': 50000,
                        'Model': 75000,
                        'Market': 50000,
                        'Proposed': 60000
                    },
                    'Limit': {
                        'Expiring': 10000000,
                        'Model': 10000000,
                        'Market': 10000000,
                        'Proposed': 10000000
                    }
                },
                'Capacity': {
                    'Line_Size': 0.65,
                    'Aggregate_Exposure': 0.45
                },
                'Risk_Factors': {
                    'Claims_Trend': {'Value': 'Deteriorating', 'Delta': 0.15},
                    'Exposure_Change': {'Value': 'Increasing', 'Delta': 0.10},
                    'Rate_Adequacy': {'Value': 'Below Target', 'Delta': -0.05}
                }
            },
            {
                'Policy_Ref': 'POL-002',
                'Client_Name': 'XYZ Manufacturing',
                'Technical_Premium': 1250000,
                'Market_Premium': 1200000,
                'Recommended_Premium': 1225000,
                'Premium_Change': 0.15,
                'Terms': {
                    'Premium': {
                        'Expiring': 1100000,
                        'Model': 1250000,
                        'Market': 1200000,
                        'Proposed': 1225000
                    },
                    'Deductible': {
                        'Expiring': 75000,
                        'Model': 100000,
                        'Market': 75000,
                        'Proposed': 90000
                    },
                    'Limit': {
                        'Expiring': 12000000,
                        'Model': 12000000,
                        'Market': 12000000,
                        'Proposed': 12000000
                    }
                },
                'Capacity': {
                    'Line_Size': 0.70,
                    'Aggregate_Exposure': 0.50
                },
                'Risk_Factors': {
                    'Claims_Trend': {'Value': 'Stable', 'Delta': 0.05},
                    'Exposure_Change': {'Value': 'Moderate', 'Delta': 0.05},
                    'Rate_Adequacy': {'Value': 'On Target', 'Delta': 0.02}
                }
            }
        ]
    }

def display_policy_terms(policy):
    """
    Display detailed terms for a selected policy
    """
    # Model Recommendations
    st.subheader(f"Model Recommendations - {policy['Client_Name']}")
    col1, col2, col3 = st.columns(3)
    
    with col1:
        st.metric(
            "Technical Premium",
            f"£{policy['Technical_Premium']:,}",
            delta=f"{policy['Premium_Change']:+.1%}",
            help="Based on updated exposure and claims experience"
        )
    with col2:
        st.metric(
            "Market Premium",
            f"£{policy['Market_Premium']:,}",
            delta=f"+{policy['Premium_Change']:.1%}",
            help="Based on market conditions and peer analysis"
        )
    with col3:
        st.metric(
            "Recommended Premium",
            f"£{policy['Recommended_Premium']:,}",
            delta=f"{policy['Premium_Change']:+.1%}",
            help="Final recommendation considering all factors"
        )

    # Terms Comparison
    st.subheader("Terms Comparison")
    terms_data = pd.DataFrame([
        {'Term': 'Premium', **policy['Terms']['Premium']},
        {'Term': 'Deductible', **policy['Terms']['Deductible']},
        {'Term': 'Limit', **policy['Terms']['Limit']}
    ])
    st.dataframe(
        terms_data.style.format({
            'Expiring': '£{:,.0f}',
            'Model': '£{:,.0f}',
            'Market': '£{:,.0f}',
            'Proposed': '£{:,.0f}'
        }), 
        use_container_width=True
    )

    # Capacity Check
    st.subheader("Capacity Analysis")
    cap_col1, cap_col2 = st.columns(2)
    
    with cap_col1:
        st.markdown("**Line Size**")
        st.progress(policy['Capacity']['Line_Size'], text=f"{policy['Capacity']['Line_Size']*100:.0f}% of max line used")
        
    with cap_col2:
        st.markdown("**Aggregate Exposure**")
        st.progress(policy['Capacity']['Aggregate_Exposure'], text=f"{policy['Capacity']['Aggregate_Exposure']*100:.0f}% of budget used")

    # Risk Factors
    st.subheader("Key Risk Factors")
    risk_cols = st.columns(3)
    
    risk_factors = policy['Risk_Factors']
    with risk_cols[0]:
        st.metric(
            "Claims Trend", 
            risk_factors['Claims_Trend']['Value'], 
            delta=f"{risk_factors['Claims_Trend']['Delta']:+.1%}"
        )
    with risk_cols[1]:
        st.metric(
            "Exposure Change", 
            risk_factors['Exposure_Change']['Value'], 
            delta=f"{risk_factors['Exposure_Change']['Delta']:+.1%}"
        )
    with risk_cols[2]:
        st.metric(
            "Rate Adequacy", 
            risk_factors['Rate_Adequacy']['Value'], 
            delta=f"{risk_factors['Rate_Adequacy']['Delta']:+.1%}"
        )

    # Actions
    st.subheader("Actions")
    action_cols = st.columns(4)
    
    with action_cols[0]:
        st.button("Save Terms", key=f"save_{policy['Policy_Ref']}")
    with action_cols[1]:
        st.button("Generate Quote Sheet", key=f"quote_{policy['Policy_Ref']}")
    with action_cols[2]:
        st.button("Send for Approval", key=f"approval_{policy['Policy_Ref']}")

    # Additional Notes
    st.text_area("Underwriter Notes", height=100, key=f"notes_{policy['Policy_Ref']}")

def run_terms_view():
    # Load terms data
    terms_data = load_terms_data()

    # Main page title
    st.title("Renewal Terms")

    # Bulk Action Section
    st.subheader("Bulk Actions")
    bulk_cols = st.columns(3)
    with bulk_cols[0]:
        bulk_decision = st.selectbox(
            "Bulk Terms Action", 
            ["No Bulk Action", "Apply Recommended", "Adjust Terms", "Decline"]
        )
    with bulk_cols[1]:
        bulk_filter = st.multiselect(
            "Filter Policies",
            ["High Risk", "Capacity Constraints", "Below Rate Adequacy"]
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
        "Select Policies to Review Terms",
        [f"{p['Policy_Ref']} - {p['Client_Name']}" for p in terms_data['policies']]
    )

    # Display selected policies
    if selected_policies:
        for policy_display in selected_policies:
            # Extract Policy Reference
            policy_ref = policy_display.split(" - ")[0]
            
            # Find the corresponding policy
            policy = next(p for p in terms_data['policies'] if p['Policy_Ref'] == policy_ref)
            
            # Expandable section for each policy
            with st.expander(f"{policy_display}"):
                display_policy_terms(policy)

    # Optional: Policy Terms Summary Table
    st.subheader("Policy Terms Overview")
    overview_data = []
    for policy in terms_data['policies']:
        overview_data.append({
            'Policy_Ref': policy['Policy_Ref'],
            'Client_Name': policy['Client_Name'],
            'Recommended_Premium': f"£{policy['Recommended_Premium']:,}",
            'Premium_Change': f"{policy['Premium_Change']:+.1%}",
            'Line_Size_Used': f"{policy['Capacity']['Line_Size']*100:.0f}%",
            'Rate_Adequacy': policy['Risk_Factors']['Rate_Adequacy']['Value']
        })
    overview_df = pd.DataFrame(overview_data)
    st.dataframe(overview_df, use_container_width=True)

if __name__ == "__main__":
    run_terms_view()