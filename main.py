import datetime
import streamlit as st
from streamlit_option_menu import option_menu
import matplotlib.pyplot as plt
import pandas as pd
import my_lib as nf


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
            "Zomato",
            "Test 1",
            "Test 2"
        ],
        icons=["", "", "", "", ""],
        menu_icon="cast",
        default_index=0,
    )

# seles report
if selected == "Sales Report":
    st.header("working on...")

# covid 19 report
if selected == "Covid 19 Report":
    st.header("working on...")

# zomato report
if selected == "Zomato":
    st.header("working on...")

if selected == "Test 1":
    report_form = st.form(key="annotation2")
    with report_form:
        row_1 = st.columns(4)
        start_date = row_1[0].date_input("Start Date:")
        end_date = row_1[1].date_input("End Date:")

        nifty_price = 17122
        ce_strike = nf.ce_strike_list(nifty_price)
        pe_strike = nf.pe_strike_list(nifty_price)

        ce_strike_list = row_1[2].selectbox("CE Strike :", ce_strike)
        pe_strike_list = row_1[3].selectbox("PE Strike :", pe_strike)

        row_2 = st.columns(4)

        entry_time = row_2[0].time_input(
            "Select Entry Time : ", datetime.time(9, 15)
        )
        exit_time = row_2[1].time_input(
            "Select Exit Time : ", datetime.time(9, 15))

        report_form_submitted = row_2[3].form_submit_button(label="Submit")

    if report_form_submitted:
        st.success("Your report loaded successfully!")
        st.write(f"Your start date : ({start_date})")
        st.write(f"Your end date : ({end_date})")
        st.write("Your CE selected strike is: ", ce_strike_list)
        st.write("Your PE selected strike is: ", pe_strike_list)
        st.write("your entry time : ", entry_time)
        st.write("your exit time : ", exit_time)

if selected == "Test 2":
    uploaded_file = st.file_uploader("Upload CSV", type=".csv")
    if uploaded_file:
        df = pd.read_csv(uploaded_file)

        st.table(df)
        st.write(df.describe().transpose())

        fig1, ax1 = plt.subplots()
        plt.ylabel("No. of Days")
        plt.title("Index Move Histogram")
        ax1.hist(df["Move"], bins=20, rwidth=0.6)
        st.pyplot(fig1)

        fig2, ax2 = plt.subplots()
        plt.ylabel("No. of Days")
        plt.title("Index Change % Histogram")
        ax2.hist(df["Change %"], bins=20, rwidth=0.6)
        st.pyplot(fig2)

        st.header("Index Move line Chart")
        st.line_chart(df["Move"])

        col1, col2 = st.columns(2)
        with col1:
            st.header("Top 5 Down Move")
            top_5_small_data = df.nsmallest(5, "Move")
            st.write("1st : ", top_5_small_data["Move"].iloc[0])
            st.write("2nd : ", top_5_small_data["Move"].iloc[1])
            st.write("3rd : ", top_5_small_data["Move"].iloc[2])
            st.write("4th : ", top_5_small_data["Move"].iloc[3])
            st.write("5th : ", top_5_small_data["Move"].iloc[4])

        with col2:
            st.header("Top 5 Up Move")

            top_5_larg_data = df.nlargest(5, "Move")

            st.write("1st : ", top_5_larg_data["Move"].iloc[0])
            st.write("2nd : ", top_5_larg_data["Move"].iloc[1])
            st.write("3rd : ", top_5_larg_data["Move"].iloc[2])
            st.write("4th : ", top_5_larg_data["Move"].iloc[3])
            st.write("5th : ", top_5_larg_data["Move"].iloc[4])
