import datetime
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import my_lib as my_lib_obj
import streamlit as st
from streamlit_option_menu import option_menu

# sales report


def load_sales_data():
    sns.set_style('darkgrid')
    data = pd.read_csv('./data/sales_data.csv')
    data.dropna(axis="index", how="all", inplace=True)
    data['Month'] = data['Order Date'].str[0:2]
    data.set_index('Order ID')

    filt = data['Quantity Ordered'] == 'Quantity Ordered'
    df = data.loc[-filt]

    df['Quantity Ordered'] = df['Quantity Ordered'].astype('int32')
    df['Price Each'] = df['Price Each'].astype('float64')
    df['Sales'] = (df['Quantity Ordered'] * df['Price Each'])
    columns = df.columns
    print("Sales data all columns : ", columns)
    return df


def monthly_sales_report_line_chart():
    df = load_sales_data()
    df = df.groupby('Month').sum()
    df['Month Name'] = df.index
    df['Month Name'] = df['Month Name'].apply(my_lib_obj.number_to_month)

    fig = plt.figure(figsize=(8, 4))
    sns.lineplot(df['Month Name'], df['Sales'], marker='o')
    st.pyplot(fig)


def monthly_sales_report_bar_chart():
    data = load_sales_data()
    df = data.groupby('Month').sum()
    df['Month Name'] = df.index
    df['Month Name'] = df['Month Name'].apply(my_lib_obj.number_to_month)

    fig = plt.figure(figsize=(8, 4))
    sns.barplot(df['Month Name'], df['Sales'])
    st.pyplot(fig)


def best_city_sales_report_chart():
    data = load_sales_data()
    data['City'] = data['Purchase Address'].apply(lambda x: x.split(',')[1])
    city_grp = data.groupby(['City'])
    df = city_grp['Sales'].sum()
    df.rename('Units')
    st.bar_chart(df)


def best_product_sold_report_chart():
    data = load_sales_data()
    df = data.groupby(['Product']).sum()
    new_df = df.sort_values(by='Quantity Ordered')

    fig = plt.figure(figsize=(8, 4))
    plt.barh(new_df.index, new_df['Quantity Ordered'])
    plt.xlabel('Units')
    plt.xticks(size=10)
    plt.yticks(size=10)
    st.pyplot(fig)


def most_expensive_sold_product():
    data = load_sales_data()
    df = data.groupby(['Product']).sum()
    df = df.sort_values(by='Sales')

    products = df.index
    sales = df['Sales']

    fig = plt.figure(figsize=(8, 4))
    plt.barh(products, sales)
    plt.xlabel('Sales in USD')
    plt.xticks(size=10)
    plt.yticks(size=10)
    st.pyplot(fig)


def most_sold_mackbook_laptop_in_city():
    data = load_sales_data()
    data['City'] = data['Purchase Address'].apply(lambda x: x.split(',')[1])
    df = data.groupby(['City'])

    mac_users = df['Product'].apply(
        lambda x: x.str.contains('Macbook Pro Laptop').sum())

    fig = plt.figure(figsize=(8, 4))
    plt.style.use('seaborn')
    plt.bar(mac_users.index, mac_users, width=0.5)

    plt.title('MacBooks Sales \n Across the US')
    plt.xlabel('City')
    plt.ylabel('Units Sold')
    plt.xticks(rotation='45', size=13)
    plt.yticks(size=13)
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

    st.subheader(' Monthly Sales')
    monthly_sales_report_line_chart()
    monthly_sales_report_bar_chart()

    st.subheader('Which city had the highest sales?')
    best_city_sales_report_chart()

    st.subheader('Which product was sold the most?')
    best_product_sold_report_chart()

    st.subheader("Which sold product was the most expensive?")
    most_expensive_sold_product()

    st.subheader("In which city is Macbook pro laptop sold the most?")
    most_sold_mackbook_laptop_in_city()


# covid 19 report
if selected == "Covid 19 Report":
    st.markdown("working on...")


# zomato report
if selected == "Zomato":
    st.markdown("working on...")
