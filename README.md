# Brazilian E-Commerce Dashboard

[Brazilian e-commerce dashboard](https://brazilian-ecommerce-dashboard1.streamlit.app/) is a final project for the Dicoding class. The dashboard visualizes KPIs (Key Performance Indicators) of Brazilian e-commerce sales.

You can find the original dataset [here](https://www.kaggle.com/datasets/olistbr/brazilian-ecommerce)

### Setup Environment - Anaconda
conda create --name main-ds python=3.10

conda activate main-ds

pip install -r requirements.txt

### Setup Environment - Terminal
mkdir proyek_analisis_data

cd proyek_analisis_data

pipenv install

pipenv shell

pip install -r requirements.txt

### Run Streamlit Application
streamlit run ecommerce_dashboard.py