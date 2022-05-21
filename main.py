import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import my_lib as my_lib_obj
import streamlit as st
from streamlit_option_menu import option_menu


def load_sales_data():
    sales_data = pd.read_csv('./data/sales_data.csv')
    sales_data.dropna(axis="index", how="all", inplace=True)
    sales_data['Month'] = sales_data['Order Date'].str[0:2]
    sales_data.set_index('Order ID')

    filt = sales_data['Quantity Ordered'] == 'Quantity Ordered'
    new_df = sales_data.loc[-filt]

    new_df['Quantity Ordered'] = new_df['Quantity Ordered'].astype('int32')
    new_df['Price Each'] = new_df['Price Each'].astype('float64')
    new_df['Sales'] = (new_df['Quantity Ordered'] * new_df['Price Each'])
    return new_df


def monthly_sales_report():
    df = load_sales_data()
    df = df.groupby('Month').sum()
    df['Month Name'] = df.index
    df['Month Name'] = df['Month Name'].apply(my_lib_obj.number_to_month)

    fig = plt.figure(figsize=(8, 4))
    # sns.set_style('darkgrid')
    sns.barplot(df['Month Name'], df['Sales'])
    sns.lineplot(x=df['Month Name'], y=df['Sales'], data=df)
    st.pyplot(fig)

    # sns.barplot(x, y, color='blue')


def best_city_sales_report():
    df = load_sales_data()
    df['City'] = df['Purchase Address'].apply(lambda x: x.split(',')[1])
    city_grp = df.groupby(['City'])
    new_df = city_grp['Sales'].sum()
    return new_df


def best_product_sold_report():
    df = load_sales_data()
    new_df = df.groupby(['Product']).sum()
    data = new_df.sort_values(by='Quantity Ordered')
    return data


def monthly_sales_report_line_chart():
    df = load_sales_data()
    df = df.groupby('Month').sum()
    df['Month Name'] = df.index
    df['Month Name'] = df['Month Name'].apply(my_lib_obj.number_to_month)

    fig = plt.figure(figsize=(8, 4))
    # sns.set_style('darkgrid')
    month = df.index
    sales = df['Sales']
    plt.plot(month, sales)
    st.pyplot(fig)


def product_sold():
    df = load_sales_data()
    new_df = df.groupby(['Product']).sum()
    data = new_df.sort_values(by='Quantity Ordered')

    products = data.index
    quantity = data['Quantity Ordered']

    # plt.style.use('seaborn')
    fig = plt.figure(figsize=(8, 4))

    plt.barh(products, quantity)
    plt.xlabel('Units')
    plt.xticks(size=10)
    plt.yticks(size=10)
    st.pyplot(fig)


# page configuration for wide area
st.set_page_config(
    page_title="POC Project", page_icon=":chart_with_upwards_trend:", layout="wide"
)

# sidebar menu
with st.sidebar:
    selected = option_menu(
        menu_title="Reporting Tool",
        options=[
            "Sales Report",
            "Covid 19 Report",
            "Zomato"
        ],
        icons=["", "", ""],
        menu_icon="cast",
        default_index=0,
    )

# seles report
if selected == "Sales Report":

    monthly_sales_report_line_chart()

    monthly_sales_report()

    product_sold()

    st.title(
        "Thus, December was the best month for sales. and the money earned was more than 45M usd")
    # st.line_chart(data['Sales'])

    st.title("title...")
    # st.bar_chart(data['Sales'])

    st.title('Which city had the highest sales?')

    best_city_report = best_city_sales_report()
    st.bar_chart(best_city_report)

    st.title('Which product was sold the most?')
    best_product_sold = best_product_sold_report()
    st.bar_chart(best_product_sold)


# covid 19 report
if selected == "Covid 19 Report":
    st.header("working on...")


# zomato report
if selected == "Zomato":
    st.header("working on...")
