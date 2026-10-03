# European Banking – Customer Churn & Segmentation Analytics

## Project Overview

This project analyzes customer churn patterns and customer segments in the European banking sector using an interactive Streamlit dashboard.

The dashboard provides insights into overall churn, geographic churn patterns, customer demographics, financial stability, customer engagement, and high-value customer churn.

## Key Features

- Overall Churn Analysis
- Geography-wise Churn Analysis
- Geographic Risk Index
- Churn Contribution by Geography
- Churned vs Retained Customer Analysis
- Gender-based Churn Analysis
- Geography & Age Interaction Analysis
- Age & Tenure Churn Comparison
- Financial Stability vs Churn
- Salary vs Balance Churn Analysis
- High-Balance Churner Analysis
- Revenue Risk from Churn
- High-Value Customer Churn Explorer
- High-Value Customer Drill-down
- Dynamic Segment Filters
- Dynamic KPI Updates

## Customer Segmentation

The project segments customers based on:

- Geography
- Age Group
- Credit Score
- Tenure
- Balance

## Key Performance Indicators

- Overall Churn Rate
- High-Value Churn Ratio
- Engagement Drop Indicator
- Geographic Risk Index
- Segment Churn Rate

## Technologies Used

- Python
- Pandas
- Streamlit
- Plotly

## Project Structure

- `app.py` – Streamlit dashboard application
- `requirements.txt` – Required Python libraries
- `data/` – Dataset used for the analysis
- `Screenshots/` – Dashboard screenshots
- `Customer_Segmentation_Churn_Analytics_Project_Report.pdf` – Project report
- `README.md` – Project documentation

## Dataset

The dataset contains customer information including:

- Customer ID
- Geography
- Gender
- Age
- Credit Score
- Tenure
- Balance
- Number of Products
- Credit Card Status
- Active Member Status
- Estimated Salary
- Churn/Exit Status

## How to Run

Install the required libraries:

```bash
pip install -r requirements.txt

Run the Streamlit dashboard:

streamlit run app.py
Project Purpose

The purpose of this project is to identify customer segments with higher churn risk, understand demographic and financial patterns associated with churn, and highlight high-value customers who may represent greater business risk.

Conclusion

The dashboard provides an interactive analytical view of customer churn and segmentation patterns in European banking. It can support data-driven customer retention analysis and help identify customer groups requiring further attention.