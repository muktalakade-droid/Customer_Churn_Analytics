import streamlit as st
import pandas as pd

st.set_page_config(
    page_title="European Banking Churn Analytics",
    layout="wide"
)

# Load dataset
df = pd.read_csv("data/European_Bank.csv")

st.markdown(
    "<h2 style='font-size:24px; margin-bottom:15px;'>🏦📊 European Banking — Customer Churn & Segmentation Analytics</h2>",
    unsafe_allow_html=True
)

# Global Geography Filter

col_filter1, col_filter2 = st.columns(2)

with col_filter1:

    global_geo = st.selectbox(
        "🌍 Geography",
        ["All", "France", "Germany", "Spain"],
        key="global_geo"
    )
    tenure_filter = st.selectbox(
        "📅 Tenure",
        ["All", "New", "Mid-term", "Long-term"],
        key="tenure_filter"
    )
    balance_filter = st.selectbox(
    "💰 Balance",
    ["All", "Zero-balance", "Low-balance", "High-balance"],
    key="balance_filter"
) 

with col_filter2:
    age_filter = st.selectbox(
        "👤 Age Group",
        ["All", "<30", "30–45", "46–60", "60+"],
        key="age_filter"
    )
    credit_filter = st.selectbox(
        "💳 Credit Score",
        ["All", "Low", "Medium", "High"],
        key="credit_filter"
    )  

   

st.markdown("""
<style>
div[data-baseweb="select"] > div {
    border: 2px solid #5DADE2 !important;
    border-radius: 10px !important;
    background-color: #F4FAFE !important;
}

div[data-baseweb="select"] > div:hover {
    border-color: #3498DB !important;
}
</style>
""", unsafe_allow_html=True)

# Remove unnecessary columns
df = df.drop(columns=["Year", "Surname"])

# Basic validation
# st.write("Dataset Shape:", df.shape)
# st.write("Columns:", df.columns.tolist())
# st.write("Exited Values:", df["Exited"].unique())

# Age Segmentation
df["Age_Group"] = pd.cut(
    df["Age"],
    bins=[0, 29, 45, 60, float("inf")],
    labels=["<30", "30–45", "46–60", "60+"]
)
# Credit Score Segmentation
df["Credit_Score_Group"] = pd.cut(
    df["CreditScore"],
    bins=[0, 579, 699, float("inf")],
    labels=["Low", "Medium", "High"]
)

# Tenure Segmentation
df["Tenure_Group"] = pd.cut(
    df["Tenure"],
    bins=[-1, 2, 6, 10],
    labels=["New", "Mid-term", "Long-term"]
)
# Balance Segmentation
df["Balance_Group"] = pd.cut(
    df["Balance"],
    bins=[-0.01, 0, 100000, float("inf")],
    labels=["Zero-balance", "Low-balance", "High-balance"]
)


# Apply Selected Segment Filters

filtered_df = df.copy()

# Apply Geography Filter
if global_geo != "All":
    filtered_df = filtered_df[
        filtered_df["Geography"] == global_geo
    ].copy()

# Apply Age Group Filter
if age_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Age_Group"] == age_filter
    ].copy()

# Apply Credit Score Filter
if credit_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Credit_Score_Group"] == credit_filter
    ].copy()

# Apply Tenure Filter
if tenure_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Tenure_Group"] == tenure_filter
    ].copy()


# Apply Balance Filter
if balance_filter != "All":
    filtered_df = filtered_df[
        filtered_df["Balance_Group"] == balance_filter
    ].copy()    


# =========================
# KPI CALCULATIONS
# =========================

# 1. Overall Churn Rate
churn_rate = filtered_df["Exited"].mean() * 100

# 2. Segment Churn Rate
# Geography-wise churn rate
segment_churn = df.groupby("Geography")["Exited"].mean() * 100
highest_segment_churn = segment_churn.max()
highest_segment = segment_churn.idxmax()

# 3. High-Value Churn Ratio
# Top 25% customers by Balance
high_value_threshold = df["Balance"].quantile(0.75)

high_value_customers = filtered_df[filtered_df["Balance"] >= high_value_threshold]

high_value_churn = high_value_customers["Exited"].mean() * 100

# 4. Geographic Risk Index
overall_churn_rate = filtered_df["Exited"].mean()

geographic_churn_rate = filtered_df.groupby("Geography")["Exited"].mean()

geographic_risk_index = geographic_churn_rate / overall_churn_rate

highest_geographic_risk = geographic_risk_index.max()
highest_risk_geography = geographic_risk_index.idxmax()

# 5. Engagement Drop Indicator

active_churn = (
    filtered_df[filtered_df["IsActiveMember"] == 1]["Exited"].mean() * 100
)

inactive_churn = (
    filtered_df[filtered_df["IsActiveMember"] == 0]["Exited"].mean() * 100
)

engagement_drop = inactive_churn - active_churn

# Churn Contribution by Segment Size
churn_contribution = (
    filtered_df.groupby("Geography")["Exited"]
    .sum()
    .div(filtered_df["Exited"].sum())
    .mul(100)
)

# =========================
# KPI CARD DESIGN
# =========================

st.markdown("""
<style>

.kpi-card {
    padding: 10px 8px;
    border-radius: 16px;
    text-align: center;
    height: 155px;
    box-shadow: 0 4px 12px rgba(0,0,0,0.10);
    margin-bottom: 20px;
}

.kpi-icon {
    font-size: 28px;
    margin-bottom: 5px;
}

.kpi-title {
    font-size: 14px;
    font-weight: 600;
    margin-bottom: 8px;
}

.kpi-value {
    font-size: 25px;
    font-weight: 700;
}

.kpi-note {
    font-size: 11px;
    margin-top: 5px;
}

.kpi-blue {
    background: linear-gradient(135deg, #dbeafe, #bfdbfe);
}

.kpi-purple {
    background: linear-gradient(135deg, #ede9fe, #ddd6fe);
}

.kpi-gold {
    background: linear-gradient(135deg, #fef3c7, #fde68a);
}

.kpi-teal {
    background: linear-gradient(135deg, #ccfbf1, #99f6e4);
}

.kpi-orange {
    background: linear-gradient(135deg, #ffedd5, #fed7aa);
}

</style>
""", unsafe_allow_html=True)


# =========================
# THREE KPI CARDS
# =========================

col1, col2, col3,  = st.columns(3)

with col1:
    st.markdown(f"""
    <div class="kpi-card kpi-blue">
        <div class="kpi-icon">📉</div>
        <div class="kpi-title">Overall Churn Rate</div>
        <div class="kpi-value">{churn_rate:.2f}%</div>
        <div class="kpi-note">Customers who exited</div>
    </div>
    """, unsafe_allow_html=True)

with col2:
    st.markdown(f"""
        <div class="kpi-card kpi-gold">
            <div class="kpi-icon">👑</div>
            <div class="kpi-title">High-Value Churn Ratio</div>
            <div class="kpi-value">{high_value_churn:.2f}%</div>
            <div class="kpi-note">High-balance customers</div>
        </div>
        """, unsafe_allow_html=True)

with col3:
    st.markdown(f"""
        <div class="kpi-card kpi-orange">
            <div class="kpi-icon">⚡</div>
            <div class="kpi-title">Engagement Drop Indicator</div>
            <div class="kpi-value">+{engagement_drop:.2f} pp</div>
            <div class="kpi-note">Inactive − Active churn</div>
            
    
        

        </div>
        """, unsafe_allow_html=True)
    # =========================
# CHART 1 - SEGMENT CHURN RATE
# =========================

import plotly.express as px


col1, col2 = st.columns(2)


with col1:
    st.markdown("#### 📊 Segment-wise Churn Rate")

    segment_chart = (
        filtered_df.groupby("Geography")["Exited"]
        .mean()
        .mul(100)
        .reset_index()
    )

    segment_chart.columns = ["Geography", "Churn Rate"]

    fig = px.bar(
        segment_chart,
        x="Geography",
        y="Churn Rate",
        text="Churn Rate",
        title="Churn Rate by Geography",
        color="Geography",
        color_discrete_sequence=["#5DADE2", "#F5B041", "#58D68D"]
    )

    fig.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig.update_layout(
    height=300,
    margin=dict(t=25, b=35, l=45, r=15),
    yaxis_title="Churn Rate (%)",
    xaxis_title="Geography",
    yaxis_range=[0, 40],
    showlegend=False
)

    st.plotly_chart(fig, use_container_width=True)       

with col2:
    st.markdown(
        "<h3 style='font-size:22px; margin:5px 0 8px 0;'>🌍 Geographic Risk Index</h3>",
        unsafe_allow_html=True
    )

    risk_chart = (
        geographic_risk_index
        .reset_index()
    )

    risk_chart.columns = ["Geography", "Risk Index"]

    fig2 = px.bar(
        risk_chart,
        x="Geography",
        y="Risk Index",
        text="Risk Index",
        title="Regional Churn Exposure",
        color="Geography",
        color_discrete_sequence=["#5DADE2", "#F5B041", "#58D68D"]
    )

    fig2.update_traces(
        texttemplate="%{text:.2f}x",
        textposition="outside"
    )

    fig2.update_layout(
        height=300,
        margin=dict(t=25, b=35, l=45, r=15),
        yaxis_title="Risk Index",
        xaxis_title="Geography",
        showlegend=False
    )

    st.plotly_chart(fig2, use_container_width=True)

# Churn Contribution by Segment Size Chart

col3, col4 = st.columns(2)

with col3:
    st.markdown(
        "<h3 style='font-size:18px; margin:15px 0 8px 0;'>📊 Churn Contribution by Geography</h3>",
        unsafe_allow_html=True
    )

    contribution_chart = churn_contribution.reset_index()
    contribution_chart.columns = ["Geography", "Contribution"]

    fig3 = px.bar(
        contribution_chart,
        x="Geography",
        y="Contribution",
        text="Contribution",
    
        color="Geography",
        color_discrete_sequence=["#5DADE2", "#F5B041", "#58D68D"]
    )

    fig3.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig3.update_layout(
        height=300,
        margin=dict(t=25, b=35, l=45, r=15),
        yaxis_title="Contribution to Total Churn (%)",
        xaxis_title="Geography",
        showlegend=False
    )

    st.plotly_chart(fig3, use_container_width=True)

with col4:
    # Churned vs Retained Profiles

    st.markdown(
        "<h3 style='font-size:18px; margin:15px 0 8px 0;'>👥 Churned vs Retained Profiles</h3>",
        unsafe_allow_html=True
    )

    profile_chart = (
        filtered_df["Exited"]
        .value_counts()
        .rename(index={0: "Retained", 1: "Churned"})
        .reset_index()
    )

    profile_chart.columns = ["Customer Status", "Customers"]

    fig4 = px.bar(
        profile_chart,
        x="Customer Status",
        y="Customers",
        text="Customers",
        color="Customer Status",
        color_discrete_sequence=["#58D68D", "#E67E22"]
    )

    fig4.update_traces(
        textposition="outside"
    )

    fig4.update_layout(
        height=300,
        margin=dict(t=25, b=35, l=45, r=15),
        yaxis_title="Number of Customers",
        xaxis_title="Customer Status",
        showlegend=False
    )

    st.plotly_chart(fig4, use_container_width=True)

col5, col6 = st.columns(2)

# Gender-based Churn Differences

with col5:
    st.markdown(
        "<h3 style='font-size:18px; margin:15px 0 8px 0;'>👩‍🦰 Gender-based Churn Differences</h3>",
        unsafe_allow_html=True
    )

    gender_chart = (
        filtered_df.groupby("Gender")["Exited"]
        .mean()
        .mul(100)
        .reset_index()
    )

    gender_chart.columns = ["Gender", "Churn Rate"]

    fig5 = px.bar(
        gender_chart,
        x="Gender",
        y="Churn Rate",
        text="Churn Rate",
        color="Gender",
        barmode="group"
    )

    fig5.update_traces(
        texttemplate="%{text:.2f}%",
        textposition="outside"
    )

    fig5.update_layout(
        height=210,
        margin=dict(t=5, b=15, l=45, r=15),
        yaxis_title="Churn Rate (%)",
        xaxis_title="Gender",
        yaxis_range=[0, 30],
        showlegend=False
    )

    st.plotly_chart(fig5, use_container_width=True)

# Geography-Age Interaction Analysis

with col6:

    st.markdown(
        "<h3 style='font-size:18px; margin:15px 0 8px 0;'>🔥 Geography × Age Churn Interaction</h3>",
        unsafe_allow_html=True
    )

    geo_age_chart = (
        filtered_df.groupby(["Geography", "Age_Group"], observed=False)["Exited"]
        .mean()
        .mul(100)
        .reset_index()
    )

    geo_age_chart.columns = ["Geography", "Age Group", "Churn Rate"]

    heatmap_data = geo_age_chart.pivot(
        index="Geography",
        columns="Age Group",
        values="Churn Rate"
    )

    fig6 = px.imshow(
        heatmap_data,
        text_auto=".2f",
        aspect="auto",
        labels=dict(
            x="Age Group",
            y="Geography",
            color="Churn Rate (%)"
        )
    )

    fig6.update_layout(
        height=280,
        margin=dict(t=10, b=25, l=45, r=15)
    )

    st.plotly_chart(fig6, use_container_width=True)

# Age & Tenure Churn Comparison

st.markdown(
    "<h3 style='font-size:18px; margin:15px 0 8px 0;'>📊 Age & Tenure Churn Comparison</h3>",
    unsafe_allow_html=True
)

age_tenure_chart = pd.concat([
    filtered_df.groupby("Age_Group", observed=False)["Exited"].mean().mul(100).rename("Churn Rate").reset_index().assign(Segment="Age Group"),
    filtered_df.groupby("Tenure_Group", observed=False)["Exited"].mean().mul(100).rename("Churn Rate").reset_index().assign(Segment="Tenure Group")
])

age_tenure_chart["Group"] = age_tenure_chart.apply(
    lambda row: row["Age_Group"] if row["Segment"] == "Age Group" else row["Tenure_Group"],
    axis=1
)

fig_age_tenure = px.bar(
    age_tenure_chart,
    x="Group",
    y="Churn Rate",
    color="Segment",
    text="Churn Rate",
    barmode="group",
    color_discrete_sequence=["#5DADE2", "#F5B041"]
)

fig_age_tenure.update_traces(
    texttemplate="%{text:.2f}%",
    textposition="outside",
    cliponaxis=False,
    textfont=dict(size=11)
)



fig_age_tenure.update_layout(
    height=320,
    margin=dict(t=10, b=35, l=45, r=15),
    yaxis_title="Churn Rate (%)",
    xaxis_title="Customer Segment",
    yaxis_range=[0, 60]
)

st.plotly_chart(fig_age_tenure, use_container_width=True)

# Financial Stability vs Churn

st.markdown(
    "<h3 style='font-size:18px; margin:15px 0 8px 0;'>💰 Financial Stability vs Churn</h3>",
    unsafe_allow_html=True
)
financial_chart = filtered_df.copy()

fig7 = px.scatter(
    financial_chart,
    x="EstimatedSalary",
    y="Balance",
    color="Exited",
    labels={
        "EstimatedSalary": "Estimated Salary",
        "Balance": "Balance",
        "Exited": "Churn Status"
    },
    title="Salary vs Balance by Churn Status"
)

fig7.update_layout(
    height=350,
    margin=dict(t=35, b=35, l=45, r=15)
)
fig7.update_yaxes(tickformat=",")
fig7.update_xaxes(tickformat=",")


st.plotly_chart(fig7, use_container_width=True)

col7,col8 = st.columns(2)

# High-Balance Churners

with col7:

    st.markdown(
        "<h3 style='font-size:18px; margin:15px 0 8px 0;'>👑 High-Balance Churners</h3>",
        unsafe_allow_html=True
    )

    high_balance_churners = filtered_df[
        (filtered_df["Balance"] >= high_value_threshold) &
        (filtered_df["Exited"] == 1)
    ]

    selected_geo = st.selectbox(
        "Select Geography",
        ["All", "France", "Germany", "Spain"]
    )

    if selected_geo != "All":
        high_balance_churners = high_balance_churners[
            high_balance_churners["Geography"] == selected_geo
        ]

    high_balance_geo = (
        high_balance_churners
        .groupby("Geography")
        .size()
        .reset_index(name="Churned Customers")
    )

    fig8 = px.pie(
        high_balance_geo,
        names="Geography",
        values="Churned Customers",
        hole=0.45,
        color="Geography",
        color_discrete_map={
            "France": "#5DADE2",
            "Germany": "#F5B041",
            "Spain": "#58D68D"
        }
    )

    fig8.update_traces(
        textinfo="label+percent",
        hovertemplate="<b>%{label}</b><br>High-Balance Churners: %{value}<br>Share: %{percent}"
    )

    fig8.update_layout(
        height=250,
        margin=dict(t=0, b=0, l=15, r=15),
        showlegend=True,
        legend_title_text="Geography"
    )

    st.plotly_chart(fig8, use_container_width=True)

# High-Value Customer Churn Explorer

st.markdown(
    "<h3 style='font-size:18px; margin:15px 0 8px 0;'>💎 High-Value Customer Churn Explorer</h3>",
    unsafe_allow_html=True
)

high_value_total = len(
    filtered_df[filtered_df["Balance"] >= high_value_threshold]
)

high_value_churned = len(
    filtered_df[
        (filtered_df["Balance"] >= high_value_threshold) &
        (filtered_df["Exited"] == 1)
    ]
)

high_value_churn_rate = (
    high_value_churned / high_value_total * 100
    if high_value_total > 0 else 0
)

col1, col2, col3 = st.columns(3)

with col1:
    st.metric("High-Value Customers", high_value_total)

with col2:
    st.metric("High-Value Churners", high_value_churned)

with col3:
    st.metric("High-Value Churn Rate", f"{high_value_churn_rate:.2f}%")



with col8:
    # Revenue Risk from Churn

    st.markdown(
        "<h3 style='font-size:18px; margin:15px 0 8px 0;'>💰 Revenue Risk from Churn</h3>",
        unsafe_allow_html=True
    )

    revenue_df = filtered_df[filtered_df["Exited"] == 1]

    if selected_geo != "All":
        revenue_df = revenue_df[
            revenue_df["Geography"] == selected_geo
        ]

    revenue_risk = (
        revenue_df
        .groupby("Geography")["Balance"]
        .sum()
        .reset_index()
    )

    revenue_risk.columns = ["Geography", "Balance at Risk"]

    fig9 = px.bar(
        revenue_risk,
        x="Geography",
        y="Balance at Risk",
        text="Balance at Risk",
        color="Geography",
        color_discrete_map={
            "France": "#5DADE2",
            "Germany": "#F5B041",
            "Spain": "#58D68D"
        }
    )

    fig9.update_traces(
        texttemplate="%{text:,.0f}",
        textposition="outside"
    )

    fig9.update_layout(
        height=320,
        margin=dict(t=10, b=20, l=15, r=15),
        showlegend=False,
        xaxis_title="Geography",
        yaxis_title="Balance at Risk"
    )

    st.plotly_chart(fig9, use_container_width=True)

# Drill-down Customer Details
st.markdown(
    "<h3 style='font-size:18px; margin:20px 0 8px 0;'>🔎 High-Value Customer Drill-down</h3>",
    unsafe_allow_html=True
)

drilldown_df = filtered_df[
    (filtered_df["Balance"] >= high_value_threshold) &
    (filtered_df["Exited"] == 1)
].copy()

drilldown_df["Churn Status"] = "Churned"

drilldown_df = drilldown_df[
    [
        "CustomerId",
        "Geography",
        "Gender",
        "Age",
        "CreditScore",
        "Tenure",
        "Balance",
        "NumOfProducts",
        "HasCrCard",
        "IsActiveMember",
        "EstimatedSalary",
        "Churn Status"
    ]
].sort_values(
    by="Balance",
    ascending=False
)

st.dataframe(
    drilldown_df,
    use_container_width=True,
    hide_index=True
)