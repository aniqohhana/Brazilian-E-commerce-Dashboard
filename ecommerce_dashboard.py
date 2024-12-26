import pandas as pd
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px
import matplotlib.pyplot as plt

# Load the datasets
e_commerce = pd.read_csv('e_commerce.csv')

# Streamlit Dashboard
st.title('📊 Brazilian E-Commerce Dashboard 2016-2018')

e_commerce['order_purchase_timestamp'] = pd.to_datetime(e_commerce['order_purchase_timestamp'])
e_commerce['order_year'] = e_commerce['order_purchase_timestamp'].dt.year

st.sidebar.subheader('Filter by Year')
years = sorted(e_commerce['order_year'].unique())
selected_year = st.sidebar.selectbox('Select a Year', ['All'] + years)

if selected_year != 'All':
    filtered_data = e_commerce[e_commerce['order_year'] == selected_year]
else:
    filtered_data = e_commerce


col1, col2, col3 = st.columns(3)

col1.write('Number of Customers')
number_of_customers = filtered_data['customer_unique_id'].nunique()
col1.header(number_of_customers)

col2.write('Number of Orders')
number_of_orders = filtered_data['order_id'].nunique()
col2.header(number_of_orders)

col3.write('Total Revenue')
revenue = filtered_data['payment_value'].sum()
col3.header(f"{revenue:.2f}")

# Revenue per Year
st.subheader('Revenue per Year')
revenue_per_year = filtered_data.groupby('order_year')['payment_value'].sum().sort_index()
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

# Top 10 Most Purchased Product Categories
st.subheader('Top 10 Most Purchased Product Categories')
top_10_product_sales = filtered_data.groupby('product_category_name_english')['order_item_id'].count().sort_values(ascending=False).head(10)
fig = px.bar(top_10_product_sales.reset_index(),
             x='order_item_id',
             y='product_category_name_english',
             color='order_item_id',
             orientation='h',
             labels={'order_item_id': 'Number of Orders', 'product_category_name_english': 'Product Category'})
fig.update_layout(xaxis_title_font_size=12,
                  yaxis_title_font_size=12,
                  xaxis_tickfont_size=10,
                  yaxis_tickfont_size=10)
st.plotly_chart(fig)

# Payment Method Distribution
st.subheader('Payment Method Distribution')
payment_types = filtered_data['payment_type'].value_counts()
fig = px.pie(payment_types,
             values=payment_types.values,
             names=payment_types.index,
             hole=0.4,
             color_discrete_sequence=px.colors.sequential.Plasma)
st.plotly_chart(fig)

# Distribution of Review Score
st.subheader('Distribution of Review Score')
fig = px.histogram(filtered_data,
                   x='review_score',
                   nbins=5,
                   labels={'review_score': 'Review Score'})
fig.update_layout(xaxis=dict(tickmode='linear', tick0=1, dtick=1),
                  xaxis_title="Review Score",
                  yaxis_title="Frequency",
                  bargap=0.2)
st.plotly_chart(fig, use_container_width=False)

# Customer Segmentation Based on Total Payment Value
st.subheader('Customer Segmentation Based on Total Payment Value')
payment_values = filtered_data.groupby('customer_unique_id')['payment_value'].sum().reset_index()
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