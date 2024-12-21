import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px

# Load the datasets
e_commerce = pd.read_csv('e_commerce.csv')

# Streamlit Dashboard
st.title('📊 Brazilian E-Commerce Dashboard 2016-2018')

col1, col2, col3, col4 = st.columns(4)

col1.write('Number of Customers')
number_of_customers = e_commerce['customer_unique_id'].nunique()
col1.header(number_of_customers)

col2.write('Number of Orders')
number_of_orders = e_commerce['order_id'].nunique()
col2.header(number_of_orders)

col3.write('AVG Revenue')
avg_revenue = e_commerce['payment_value'].mean()
col3.header(f"{avg_revenue:.2f}")

col4.write('AVG Review Score')
avg_reviews_score = e_commerce['review_score'].mean()
col4.header(f"{avg_reviews_score:.2f}")

st.subheader('Revenue per Year')
e_commerce['order_purchase_timestamp'] = pd.to_datetime(e_commerce['order_purchase_timestamp'])
e_commerce['order_year'] = e_commerce['order_purchase_timestamp'].dt.year.astype(int)
revenue_per_year = e_commerce.groupby('order_year')['payment_value'].sum().sort_index()
revenue_per_year.index = revenue_per_year.index.map(str)
fig = go.Figure()
fig.add_trace(go.Scatter(x=revenue_per_year.index, 
                         y=revenue_per_year.values, 
                         mode='lines+markers', 
                         name='Revenue'))
fig.update_layout(xaxis_title='Year',
                  yaxis_title='Revenue',
                  template='plotly_white')
st.plotly_chart(fig)

st.subheader('Reviews Score per Year')
e_commerce['order_purchase_timestamp'] = pd.to_datetime(e_commerce['order_purchase_timestamp'])
e_commerce['order_year'] = e_commerce['order_purchase_timestamp'].dt.year.astype(int)
years = e_commerce['order_year'].unique()
year = st.selectbox('Select Year', sorted(years), key='order_year_select')
filtered_reviews = e_commerce[e_commerce['order_year'] == year]
reviews_score = filtered_reviews['review_score'].value_counts().reset_index()
reviews_score.columns = ['Review Score', 'Count']
fig = px.bar(reviews_score, x='Review Score', y='Count', 
             labels={'Review Score': 'Score', 'Count': 'Number of Reviews'},
             color='Review Score', 
             color_continuous_scale='Blues')
st.plotly_chart(fig)

st.subheader('Payment Type per Year')
e_commerce['order_purchase_timestamp'] = pd.to_datetime(e_commerce['order_purchase_timestamp'])
e_commerce['order_year'] = e_commerce['order_purchase_timestamp'].dt.year.astype(int)
available_years = e_commerce['order_year'].unique()
selected_year = st.selectbox('Select Year', sorted(available_years))
filtered_orders = e_commerce[e_commerce['order_year'] == selected_year]
payment_methods = filtered_orders['payment_type'].value_counts().reset_index()
payment_methods.columns = ['Payment Method', 'Count']
fig = px.bar(payment_methods, x='Payment Method', y='Count',
             labels={'Payment Method': 'Payment Method', 'Count': 'Number of Transactions'},
             color='Payment Method', color_continuous_scale='Blues')
st.plotly_chart(fig)

st.subheader('Customer Segmentation Based on Total Payment Value')
payment_values = e_commerce.groupby('customer_unique_id')['payment_value'].sum().reset_index()
bronze_limit = payment_values['payment_value'].quantile(0.5)
silver_limit = payment_values['payment_value'].quantile(0.9)
def classify_payment(value, bronze, silver):
    if value <= bronze:
        return 'Bronze Customer'
    elif bronze < value <= silver:
        return 'Silver Customer'
    else:
        return 'Golden Customer'
payment_values['customer_group'] = payment_values['payment_value'].apply(lambda x: classify_payment(x, bronze_limit, silver_limit))
customer_group_counts = payment_values['customer_group'].value_counts().reset_index()
customer_group_counts.columns = ['Customer Group', 'Count']
fig = px.bar(customer_group_counts, x='Customer Group', y='Count',
             labels={'Customer Group': 'Customer Group', 'Count': 'Number of Customers'},
             color='Customer Group', color_discrete_sequence=['brown', 'silver', 'gold'])
st.plotly_chart(fig)
