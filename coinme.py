import streamlit as st
import pandas as pd
import plotly.express as px
import plotly.graph_objects as go
from datetime import datetime, timedelta
import numpy as np

# Set page config
st.set_page_config(
    page_title="Coinme Competitive Intelligence Dashboard",
    page_icon="🏦",
    layout="wide",
    initial_sidebar_state="expanded"
)

# Custom CSS for better styling
st.markdown("""
<style>
    .main-header {
        font-size: 2rem;
        font-weight: bold;
        color: #003366;
        text-align: center;
        margin-bottom: 1.5rem;
    }
    .coinme-brand {
        background: #1f2937;
        color: white;
        padding: 1rem;
        border-radius: 6px;
        margin-bottom: 1.5rem;
    }
    .high-relevance {
        background-color: #2e3b4e;
        border-left: 4px solid #e74c3c;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #f8f9fa;
    }
    .medium-relevance {
        background-color: #37465c;
        border-left: 4px solid #f39c12;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #f8f9fa;
    }
    .low-relevance {
        background-color: #2c3e50;
        border-left: 4px solid #3498db;
        padding: 1rem;
        margin: 0.5rem 0;
        color: #f8f9fa;
    }
    .action-item {
        background-color: #1e293b;
        border: 1px solid #6b7280;
        padding: 1rem;
        border-radius: 6px;
        margin: 0.5rem 0;
        color: #f8f9fa;
    }
</style>
""", unsafe_allow_html=True)

@st.cache_data
def load_real_data():
    """Load the actual Coinme competitive intelligence data"""
    
    # Real data from the provided dataset
    real_data = [
        {
            "Company": "Avalon Labs",
            "Date": "2024-12-01",
            "Funding_Stage": "Series A",
            "Amount_USD_M": 10.0,
            "Use_of_Funds": "Bitcoin-backed DeFi ecosystem expansion, lending, stablecoins",
            "Source_Link": "https://cointelegraph.com/news/vc-roundup-crypto-funding-climbs-13-6-billion-2024",
            "Relevance_to_Coinme": "Direct competitor in Bitcoin financial services with 20,000+ BTC serviced",
            "Sales_Action": "Partner opportunity for enterprise custody solutions; competitive pricing strategy needed",
            "Segment": "Bitcoin Financial Services",
            "Relevance_Level": "High",
            "Competitive_Threat": "High"
        },
        {
            "Company": "Usual",
            "Date": "2024-12-01",
            "Funding_Stage": "Series A",
            "Amount_USD_M": 10.0,
            "Use_of_Funds": "Stablecoin expansion, traditional finance integration",
            "Source_Link": "https://cointelegraph.com/news/vc-roundup-crypto-funding-climbs-13-6-billion-2024",
            "Relevance_to_Coinme": "Adjacent player in crypto payments with $1.7B TVL",
            "Sales_Action": "Explore stablecoin payment integration for enterprise clients",
            "Segment": "Payments",
            "Relevance_Level": "Medium",
            "Competitive_Threat": "Medium"
        },
        {
            "Company": "Accountable",
            "Date": "2024-12-01",
            "Funding_Stage": "Seed",
            "Amount_USD_M": 2.3,
            "Use_of_Funds": "Bitcoin lending platform, privacy-focused data solutions",
            "Source_Link": "https://cointelegraph.com/news/vc-roundup-crypto-funding-climbs-13-6-billion-2024",
            "Relevance_to_Coinme": "Competitor in Bitcoin lending space with $2M+ loans facilitated",
            "Sales_Action": "Position Coinme's institutional lending capabilities against new entrants",
            "Segment": "Bitcoin Lending",
            "Relevance_Level": "High",
            "Competitive_Threat": "Medium"
        },
        {
            "Company": "Monad Labs",
            "Date": "2024-06-01",
            "Funding_Stage": "Series A",
            "Amount_USD_M": 225.0,
            "Use_of_Funds": "Layer-1 smart contract network development",
            "Source_Link": "https://cointelegraph.com/news/paradigm-leads-225m-funding-solana-killer",
            "Relevance_to_Coinme": "Infrastructure layer relevant to payment processing",
            "Sales_Action": "Monitor for potential integration opportunities in smart contract payments",
            "Segment": "Infrastructure",
            "Relevance_Level": "Low",
            "Competitive_Threat": "Low"
        },
        {
            "Company": "Berachain",
            "Date": "2024-04-01",
            "Funding_Stage": "Series A",
            "Amount_USD_M": 100.0,
            "Use_of_Funds": "Modular blockchain development platform",
            "Source_Link": "https://cointelegraph.com/news/crypto-venture-capital-funding-hits-one-billion-april",
            "Relevance_to_Coinme": "Blockchain infrastructure for payment systems",
            "Sales_Action": "Assess partnership potential for enhanced payment rails",
            "Segment": "Infrastructure",
            "Relevance_Level": "Low",
            "Competitive_Threat": "Low"
        },
        {
            "Company": "Babylon",
            "Date": "2024-05-01",
            "Funding_Stage": "Series A",
            "Amount_USD_M": 70.0,
            "Use_of_Funds": "Bitcoin staking protocol development",
            "Source_Link": "https://cointelegraph.com/news/crypto-vc-l2-interoperability-ai",
            "Relevance_to_Coinme": "Bitcoin ecosystem expansion, potential custody competitor",
            "Sales_Action": "Develop Bitcoin yield products for enterprise clients",
            "Segment": "Bitcoin Services",
            "Relevance_Level": "Medium",
            "Competitive_Threat": "Medium"
        },
        {
            "Company": "Securitize",
            "Date": "2024-03-01",
            "Funding_Stage": "Series A",
            "Amount_USD_M": 47.0,
            "Use_of_Funds": "Tokenization platform expansion, BlackRock partnership",
            "Source_Link": "https://cointelegraph.com/news/securitize-blackrock-47m-funding-round",
            "Relevance_to_Coinme": "Enterprise tokenization services, institutional adoption",
            "Sales_Action": "Target similar institutional clients with Bitcoin payment solutions",
            "Segment": "Institutional Services",
            "Relevance_Level": "High",
            "Competitive_Threat": "Medium"
        },
        {
            "Company": "Thena",
            "Date": "2024-12-01",
            "Funding_Stage": "Strategic",
            "Amount_USD_M": 5.0,  # Estimated for undisclosed
            "Use_of_Funds": "DEX expansion, cross-chain operations",
            "Source_Link": "https://cointelegraph.com/news/vc-roundup-crypto-funding-climbs-13-6-billion-2024",
            "Relevance_to_Coinme": "DeFi payment infrastructure with $63M TVL",
            "Sales_Action": "Consider DeFi integration for enterprise payment flows",
            "Segment": "DeFi/Trading",
            "Relevance_Level": "Medium",
            "Competitive_Threat": "Low"
        }
    ]
    
    # Convert to DataFrame and add additional computed fields
    df = pd.DataFrame(real_data)
    df['Date'] = pd.to_datetime(df['Date'])
    df['Year'] = df['Date'].dt.year
    df['Month'] = df['Date'].dt.month
    df['Quarter'] = df['Date'].dt.quarter
    df['Quarter_Year'] = df['Date'].dt.to_period('Q').astype(str)
    
    return df

def create_funding_by_segment_chart(df):
    """Create funding by segment chart"""
    segment_data = df.groupby('Segment').agg({
        'Amount_USD_M': 'sum',
        'Company': 'count'
    }).reset_index()
    segment_data.columns = ['Segment', 'Total_Funding', 'Deal_Count']
    segment_data = segment_data.sort_values('Total_Funding', ascending=False)
    
    fig = px.bar(
        segment_data,
        x='Segment',
        y='Total_Funding',
        text='Deal_Count',
        title='Total Funding by Market Segment',
        color='Total_Funding',
        color_continuous_scale='RdYlBu_r',
        labels={'Total_Funding': 'Funding Amount (USD Millions)'}
    )
    
    fig.update_traces(texttemplate='%{text} deals', textposition='outside')
    fig.update_layout(
        xaxis_title="Market Segment",
        yaxis_title="Funding Amount (USD Millions)",
        showlegend=False,
        xaxis_tickangle=-45
    )
    
    return fig

def create_competitive_threat_matrix(df):
    """Create competitive threat vs relevance matrix"""
    # Create threat level mapping
    threat_mapping = {'High': 3, 'Medium': 2, 'Low': 1}
    relevance_mapping = {'High': 3, 'Medium': 2, 'Low': 1}
    
    df_plot = df.copy()
    df_plot['Threat_Score'] = df_plot['Competitive_Threat'].map(threat_mapping)
    df_plot['Relevance_Score'] = df_plot['Relevance_Level'].map(relevance_mapping)
    
    fig = px.scatter(
        df_plot,
        x='Relevance_Score',
        y='Threat_Score',
        size='Amount_USD_M',
        color='Segment',
        hover_data=['Company', 'Amount_USD_M'],
        title='Competitive Threat vs Relevance Matrix',
        labels={
            'Relevance_Score': 'Relevance to Coinme',
            'Threat_Score': 'Competitive Threat Level'
        }
    )
    
    fig.update_xaxes(ticktext=['Low', 'Medium', 'High'], tickvals=[1, 2, 3])
    fig.update_yaxes(ticktext=['Low', 'Medium', 'High'], tickvals=[1, 2, 3])
    
    # Add quadrant lines
    fig.add_hline(y=2.5, line_dash="dash", line_color="gray", opacity=0.5)
    fig.add_vline(x=2.5, line_dash="dash", line_color="gray", opacity=0.5)
    
    return fig

def create_funding_timeline(df):
    """Create funding timeline chart"""
    monthly_data = df.groupby(df['Date'].dt.to_period('M')).agg({
        'Amount_USD_M': 'sum',
        'Company': 'count'
    }).reset_index()
    monthly_data['Date'] = monthly_data['Date'].dt.to_timestamp()
    
    fig = go.Figure()
    
    fig.add_trace(go.Scatter(
        x=monthly_data['Date'],
        y=monthly_data['Amount_USD_M'],
        mode='lines+markers',
        name='Funding Amount',
        line=dict(color='#2E86AB', width=3),
        marker=dict(size=8)
    ))
    
    fig.update_layout(
        title='Funding Timeline - Competitive Landscape',
        xaxis_title='Date',
        yaxis_title='Monthly Funding (USD Millions)',
        hovermode='x unified'
    )
    
    return fig

def create_stage_distribution(df):
    """Create funding stage distribution"""
    stage_data = df.groupby('Funding_Stage').agg({
        'Amount_USD_M': 'sum',
        'Company': 'count'
    }).reset_index()
    
    fig = px.pie(
        stage_data,
        values='Amount_USD_M',
        names='Funding_Stage',
        title='Funding Distribution by Stage',
        color_discrete_sequence=px.colors.qualitative.Set3
    )
    
    return fig

def main():
    """Main dashboard function"""
    
    # Header with Coinme branding
    st.markdown("""
    <div class="coinme-brand">
        <h1> Coinme Competitive Intelligence Dashboard</h1>
        <p>Real-time funding analysis and competitive positioning insights</p>
    </div>
    """, unsafe_allow_html=True)
    
    # Load real data
    df = load_real_data()
    
    # Sidebar filters
    st.sidebar.markdown("###  Analysis Filters")
    
    # Relevance filter
    relevance_filter = st.sidebar.multiselect(
        "Relevance to Coinme",
        options=df['Relevance_Level'].unique(),
        default=df['Relevance_Level'].unique()
    )
    
    # Segment filter
    segment_filter = st.sidebar.multiselect(
        "Market Segments",
        options=df['Segment'].unique(),
        default=df['Segment'].unique()
    )
    
    # Competitive threat filter
    threat_filter = st.sidebar.multiselect(
        "Competitive Threat Level",
        options=df['Competitive_Threat'].unique(),
        default=df['Competitive_Threat'].unique()
    )
    
    # Apply filters
    df_filtered = df[
        (df['Relevance_Level'].isin(relevance_filter)) &
        (df['Segment'].isin(segment_filter)) &
        (df['Competitive_Threat'].isin(threat_filter))
    ]
    
    # Key metrics
    col1, col2, col3, col4 = st.columns(4)
    
    with col1:
        total_funding = df_filtered['Amount_USD_M'].sum()
        st.metric(
            "Total Competitive Funding",
            f"${total_funding:.1f}M",
            f"{len(df_filtered)} companies"
        )
    
    with col2:
        high_threat = df_filtered[df_filtered['Competitive_Threat'] == 'High']
        st.metric(
            "High Threat Competitors",
            len(high_threat),
            f"${high_threat['Amount_USD_M'].sum():.1f}M raised"
        )
    
    with col3:
        bitcoin_focused = df_filtered[df_filtered['Segment'].str.contains('Bitcoin', case=False)]
        st.metric(
            "Bitcoin-Focused Companies",
            len(bitcoin_focused),
            f"${bitcoin_focused['Amount_USD_M'].sum():.1f}M"
        )
    
    with col4:
        recent_funding = df_filtered[df_filtered['Date'] >= '2024-11-01']
        st.metric(
            "Recent Funding (Nov+)",
            len(recent_funding),
            f"${recent_funding['Amount_USD_M'].sum():.1f}M"
        )
    
    # Charts section
    st.markdown("---")
    st.markdown("###  Competitive Analysis")
    
    # Row 1: Segment funding and competitive matrix
    col1, col2 = st.columns(2)
    
    with col1:
        fig1 = create_funding_by_segment_chart(df_filtered)
        st.plotly_chart(fig1, use_container_width=True)
    
    with col2:
        fig2 = create_competitive_threat_matrix(df_filtered)
        st.plotly_chart(fig2, use_container_width=True)
    
    # Row 2: Timeline and stage distribution
    col1, col2 = st.columns(2)
    
    with col1:
        fig3 = create_funding_timeline(df_filtered)
        st.plotly_chart(fig3, use_container_width=True)
    
    with col2:
        fig4 = create_stage_distribution(df_filtered)
        st.plotly_chart(fig4, use_container_width=True)
    
    # Strategic insights section
    st.markdown("---")
    st.markdown("###  Strategic Insights & Action Items")
    
    # High priority competitors
    high_relevance = df_filtered[df_filtered['Relevance_Level'] == 'High']
    if not high_relevance.empty:
        st.markdown("####  High Priority Competitors")
        for _, row in high_relevance.iterrows():
            st.markdown(f"""
            <div class="high-relevance">
                <strong>{row['Company']}</strong> - ${row['Amount_USD_M']:.1f}M ({row['Funding_Stage']})
                <br><strong>Relevance:</strong> {row['Relevance_to_Coinme']}
                <br><strong>Action Required:</strong> {row['Sales_Action']}
            </div>
            """, unsafe_allow_html=True)
    
    # Action items by segment
    st.markdown("####  Action Items by Business Segment")
    
    for segment in df_filtered['Segment'].unique():
        segment_data = df_filtered[df_filtered['Segment'] == segment]
        if not segment_data.empty:
            st.markdown(f"**{segment}** ({len(segment_data)} companies, ${segment_data['Amount_USD_M'].sum():.1f}M total)")
            
            for _, row in segment_data.iterrows():
                st.markdown(f"""
                <div class="action-item">
                    <strong>{row['Company']}</strong>: {row['Sales_Action']}
                </div>
                """, unsafe_allow_html=True)
    
    # Detailed competitor analysis
    st.markdown("---")
    st.markdown("###  Detailed Competitor Analysis")
    
    # Search and filter
    search_term = st.text_input(" Search companies, use cases, or actions:")
    
    if search_term:
        df_search = df_filtered[
            df_filtered['Company'].str.contains(search_term, case=False, na=False) |
            df_filtered['Use_of_Funds'].str.contains(search_term, case=False, na=False) |
            df_filtered['Sales_Action'].str.contains(search_term, case=False, na=False)
        ]
    else:
        df_search = df_filtered
    
    # Format display data
    df_display = df_search.copy()
    df_display['Amount_USD_M'] = df_display['Amount_USD_M'].apply(lambda x: f"${x:.1f}M")
    df_display['Date'] = df_display['Date'].dt.strftime('%Y-%m-%d')
    df_display = df_display.sort_values('Date', ascending=False)
    
    # Display with enhanced formatting
    st.dataframe(
        df_display[['Company', 'Date', 'Funding_Stage', 'Amount_USD_M', 'Segment', 
                   'Relevance_Level', 'Competitive_Threat', 'Use_of_Funds', 
                   'Sales_Action', 'Source_Link']],
        use_container_width=True,
        hide_index=True,
        column_config={
            "Date": st.column_config.TextColumn("Date"),
            "Amount_USD_M": st.column_config.TextColumn("Amount"),
            "Source_Link": st.column_config.LinkColumn("Source"),
            "Relevance_Level": st.column_config.TextColumn("Relevance"),
            "Competitive_Threat": st.column_config.TextColumn("Threat Level"),
            "Use_of_Funds": st.column_config.TextColumn("Use of Funds", width="medium"),
            "Sales_Action": st.column_config.TextColumn("Required Action", width="medium")
        }
    )
    
    # Download functionality
    st.markdown("---")
    csv = df_filtered.to_csv(index=False)
    st.download_button(
        label=" Download Intelligence Report (CSV)",
        data=csv,
        file_name="coinme_competitive_intelligence.csv",
        mime="text/csv"
    )
    
    # Summary insights
    st.markdown("---")
    st.markdown("###  Key Takeaways")
    
    col1, col2 = st.columns(2)
    
    with col1:
        st.markdown("""
        **Market Threats:**
        - Avalon Labs: Direct Bitcoin services competitor with significant traction
        - Accountable: Emerging Bitcoin lending threat
        - Securitize: Institutional tokenization with BlackRock backing
        """)
    
    with col2:
        st.markdown("""
        **Opportunities:**
        - Partner with infrastructure players (Monad, Berachain)
        - Develop Bitcoin yield products to compete with Babylon
        - Target enterprise clients similar to Securitize's approach
        """)
    
    st.markdown("""
    ---
    **Data Source:** Real competitive intelligence data from Coinme market analysis.
    **Last Updated:** December 2024
    """)

if __name__ == "__main__":
    main()