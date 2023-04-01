import pandas as pd
from PIL import Image
import streamlit as st
import webbrowser
from streamlit_option_menu import option_menu
import plotly.express as px
import plotly.figure_factory as ff
from sqlalchemy import create_engine, text
from urllib.parse import quote 


#Function to Create Connection with MySQL Database

def read_data_from_mysql(table_name):
    engine = create_engine(
        'mysql+mysqlconnector://root:%s@localhost:3306/Phonepe_Pulse' % quote('Your_Password')) #Password with Special Characters Also Works in this Connection  
    query = f"SELECT * FROM {table_name}"
    df = pd.read_sql_query(sql=text(query), con= engine.connect())
    df = df.drop('id', axis=1)
    return df


# Read data from MySQL database
df_aggregated_transaction = read_data_from_mysql('aggregated_transactions')
df_aggregated_user = read_data_from_mysql('aggregated_user')
df_map_transaction = read_data_from_mysql('map_transaction')
df_map_user = read_data_from_mysql('map_user')
df_top_transaction = read_data_from_mysql('top_transaction')
df_top_user = read_data_from_mysql('top_user')

# Setting the background color of the page:


def set_background_color(color):
    st.markdown(
        f'<style>body {{ margin: 0; padding: 0; background-color: {color}; }}</style>', unsafe_allow_html=True)

# Set page configuration


def set_page_config(im, bgcolor):
    st.set_page_config(
        page_title="Phonepe Pulse Insights",
        page_icon=im,
        layout="wide",
    )
    set_background_color(bgcolor)


def display_navigation():
    selected = option_menu(
        menu_title=None,
        options=["HOME", "GEO-INSIGHTS", "DASHBORD"],
        icons=["house", "map", "bar-chart"],
        orientation="horizontal",
        styles={
            "container": {"margin": "0", "padding": "0!important", "background-color": "#0c7ded"},
            "icon": {"color": "black", "font-size": "17px"},
            "nav-link": {"font-size": "17px", "text-align": "center", "margin": "2px", "--hover-color": "#1e0ead"},
            "nav-link-selected": {"background-color": "#1e0ead"},
        }
    )
    return selected


def display_title(title):
    st.title(title)
    st.markdown(
        "<style>div.st-cc { margin: 0; padding: 0; }</style>", unsafe_allow_html=True)

# Define app functions


def home():
    st.subheader("Introduction")
    st.write("""The Indian digital payments story has truly captured the world's imagination. From the largest towns to the remotest villages, there is a payments revolution 
            being driven by the penetration of mobile phones, mobile internet and State-of-the-art payments infrastructure built as Public Goods championed by the 
            central bank and the government. Founded in December 2015, PhonePe has been a strong beneficiary of the API driven digitisation of payments in India. 
            When we started, we were constantly looking for granular and definitive data sources on digital payments in India. PhonePe Pulse is our way of giving 
            back to the digital payments ecosystem.""")
    st.subheader("GUIDE")
    st.write(""" This data has been structured to provide details on data cuts of Transactions and Users on the Explore tab.""")
    with st.expander("Aggregated"):
        st.write(
            "Aggregated values of various payment categories as shown under Categories section")
    with st.expander("Map"):
        st.write("Total values at the State and District levels")
    with st.expander("Top"):
        st.write("Totals of top States / Districts / Pin Codes")

    st.subheader("Github")
    st.write("A home for the data that powers the PhonePe Pulse website.")
    if st.button('Open'):
        webbrowser.open_new_tab("https://github.com/PhonePe/pulse#readme")


def geo_insights():

    col_1, col_2 = st.columns(2)
    with col_1:
        st.subheader("Select Transactions/User Data")
        Menu = st.selectbox("", ('Transactions', "User"))
        st.subheader("Select Transactions count/amount")
        metric = st.selectbox('', options=['count', 'amount'])
    with col_2:
        st.subheader("Select Year")
        year = st.selectbox("", ("2018", "2019", "2020", "2021", "2022"))
        st.subheader("Select Quarter")
        Quarter = st.selectbox('', ('1', '2', '3', '4'))
    insights, map_ = st.columns(2)

    if Menu == "Transactions":
        df_agg = df_aggregated_transaction[(df_aggregated_transaction['Year'] == year) & (
            df_aggregated_transaction['Quarter'] == Quarter)]

        df_map = df_map_transaction[(df_map_transaction['Year'] == year) & (
            df_map_transaction['Quarter'] == Quarter)]
        df_top = df_top_transaction[(df_top_transaction['Year'] == year) & (
            df_top_transaction['Quarter'] == Quarter)]
        with map_:
            df_agg_m = df_agg[['State', metric]].groupby(
                ['State']).sum().reset_index()
            df_map_m = df_map[['State', metric]].groupby(
                ['State']).sum().reset_index()
            df_top_m = df_top[['State', metric]].groupby(
                ['State']).sum().reset_index()

            df = pd.merge(df_agg_m, df_map_m, on='State',
                          suffixes=('_left', '_right'))
            if metric == 'count':
                df[metric] = df['count_left'] + df['count_right']
            if metric == 'amount':
                df[metric] = df['amount_left'] + df['amount_right']
            df = df[['State', metric]]

            df = pd.merge(df, df_top_m, on='State',
                          suffixes=('_left', '_right'))
            if metric == 'count':
                df[metric] = df['count_left'] + df['count_right']
            if metric == 'amount':
                df[metric] = df['amount_left'] + df['amount_right']
            df = df[['State', metric]]

            # Create a Plotly Choropleth map using the filtered dataframe
            fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color_continuous_scale='PuBu',
                color=metric,
                title=" Total Transaction "+metric+" in india",
            )

            fig.update_geos(fitbounds="locations", visible=False)

            fig.update_layout(
                width=600,
                height=600
            )

            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

        with insights:
            col1, col2 = st.columns(2)
            with col1:
                df_agg_t = df_agg[['State', 'amount']].groupby(
                    ['State']).sum().reset_index()
                df_map_t = df_map[['State', 'amount']].groupby(
                    ['State']).sum().reset_index()
                df_top_t = df_top[['State', 'amount']].groupby(
                    ['State']).sum().reset_index()
                total_trans_amount = df_agg_t['amount'].sum(
                )+df_map_t['amount'].sum()+df_top_t['amount'].sum()

                total_trans_amount = round(total_trans_amount / 10000000, 2)

                header_style = '<h3 style="text-align:center;">Total amount</h3>'
                subheader_style = '<h3 style="text-align:center;">{0} crores </h3>'.format(
                    total_trans_amount)

                st.markdown(header_style, unsafe_allow_html=True)
                st.markdown(subheader_style, unsafe_allow_html=True)

            with col2:
                df_agg_c = df_agg[['State', 'count']].groupby(
                    ['State']).sum().reset_index()
                df_map_c = df_map[['State', 'count']].groupby(
                    ['State']).sum().reset_index()
                df_top_c = df_top[['State', 'count']].groupby(
                    ['State']).sum().reset_index()

                total_trans = df_agg_c['count'].sum(
                )+df_map_c['count'].sum()+df_top_c['count'].sum()
                header_style = '<h3 style="text-align:center;">Total Transactions</h3>'
                subheader_style = '<h3 style="text-align:center;">{0}</h3>'.format(
                    total_trans)
                st.markdown(header_style, unsafe_allow_html=True)
                st.markdown(subheader_style, unsafe_allow_html=True)
            col1, col2 = st.columns(2)
            with col1:

                df = df_agg[['Transaction_type', 'amount']].groupby(
                    ['Transaction_type']).sum().reset_index()

                # Convert the amounts to crores and round off to two decimal places
                df['amount'] = (df['amount'] / 10000000).round(2)

                # Add 'cr' to the amount column
                df['amount'] = df['amount'].astype(str) + ' cr'

                # Rename the column to indicate the amount is in crores
                df = df.rename(columns={'amount': 'Amount (in crores)'})

                header_style = '<h4 style="text-align:center;">Categories</h4>'
                st.markdown(header_style, unsafe_allow_html=True)

                colorscale = [[0, '#7e40ad'], [.5, '#ffffff'], [1, '#f2e5ff']]
                fig = ff.create_table(df, colorscale=colorscale)
                fig.layout.width = 270
                st.plotly_chart(fig, use_container_width=False,
                                theme="streamlit")
            with col2:

                header_style = '<h4 style="text-align:center;">Statewise Transactions</h4>'
                st.markdown(header_style, unsafe_allow_html=True)
                df_agg_ts = df_agg[['State', 'amount']].groupby(
                    ['State']).sum().reset_index()
                df_map_ts = df_map[['State', 'amount']].groupby(
                    ['State']).sum().reset_index()
                df_top_ts = df_top[['State', 'amount']].groupby(
                    ['State']).sum().reset_index()

                df = pd.merge(df_agg_ts, df_map_ts, on='State',
                              suffixes=('_left', '_right'))
                df['amount'] = df['amount_left'] + df['amount_right']
                df = df[['State', "amount"]]
                df = pd.merge(df, df_top_ts, on='State',
                              suffixes=('_left', '_right'))
                df['amount'] = df['amount_left'] + df['amount_right']
                df = df[['State', 'amount']]
                df['amount'] = (df['amount'] / 10000000).round(2)

                df = df.sort_values('amount', ascending=False).head(10)
                df['amount'] = df['amount'].astype(str) + ' cr'

                # Apply CSS styling to the table
                colorscale = [[0, '#7e40ad'], [.5, '#ffffff'], [1, '#f2e5ff']]
                fig = ff.create_table(df, colorscale=colorscale)
                fig.layout.width = 300
                st.plotly_chart(fig, use_container_width=False,
                                theme="streamlit")

    if Menu == "User":
        df_agg = df_aggregated_user[(df_aggregated_user['Year'] == year) & (
            df_aggregated_user['Quarter'] == Quarter)]

        df_map = df_map_user[(df_map_user['Year'] == year)
                             & (df_map_user['Quarter'] == Quarter)]
        df_top = df_top_user[(df_top_user['Year'] == year)
                             & (df_top_user['Quarter'] == Quarter)]

        col1, col2 = st.columns(2)
        with col1:

            total_users = df_map['RegisteredUser'].sum(
            )+df_top['RegisteredUser'].sum()
            total_users = round(total_users / 1000000, 2)
            header_style = '<h3 style="text-align:center;">Total Registered Users</h3>'
            subheader_style = '<h3 style="text-align:center;">{0} M </h3>'.format(
                total_users)
            st.markdown(header_style, unsafe_allow_html=True)
            st.markdown(subheader_style, unsafe_allow_html=True)

            header_style = '<h3 style="text-align:center;">Top 10 States by Users</h3>'
            st.markdown(header_style, unsafe_allow_html=True)
            df_map_us = df_map[['State', 'RegisteredUser']
                               ].groupby(['State']).sum().reset_index()
            df_top_us = df_top[['State', 'RegisteredUser']
                               ].groupby(['State']).sum().reset_index()

            df = pd.merge(df_map_us, df_top_us, on='State',
                          suffixes=('_left', '_right'))
            df['RegisteredUser'] = df['RegisteredUser_left'] + \
                df['RegisteredUser_right']
            df = df[['State', "RegisteredUser"]]

            df['RegisteredUser'] = (df['RegisteredUser'] / 1000000).round(2)

            df = df.sort_values('RegisteredUser', ascending=False).head(10)
            df['RegisteredUser'] = df['RegisteredUser'].astype(str) + ' M'

            colorscale = [[0, '#7e40ad'], [.5, '#ffffff'], [1, '#f2e5ff']]
            fig = ff.create_table(df, colorscale=colorscale)
            fig.layout.width = 600

            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

        with col2:
            df_map_m = df_map[['State', 'RegisteredUser']
                              ].groupby(['State']).sum().reset_index()
            df_top_m = df_top[['State', 'RegisteredUser']
                              ].groupby(['State']).sum().reset_index()

            df = pd.merge(df_map_m, df_top_m, on='State',
                          suffixes=('_left', '_right'))
            df['RegisteredUser'] = df['RegisteredUser_left'] + \
                df['RegisteredUser_right']
            df = df[['State', 'RegisteredUser']]

            # Create a Plotly Choropleth map using the filtered dataframe
            fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color_continuous_scale='PuBu',
                color='RegisteredUser',
                title="Total Registered Users in India"
            )

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
                width=600,
                height=600
            )

            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")


def dashboard():

    with st.sidebar:
        selected = option_menu(menu_title=None,
                               options=["Aggregated Data Insights",
                                        "Map Data Insights",
                                        "Top Data Insights"
                                        ],
                               orientation="vertical",
                               styles={
                                   "container": {"padding": "0!important", "background-color": "#09dbc3"},
                                   "icon": {"color": "black", "font-size": "15px"},
                                   "nav-link": {"font-size": "15px", "text-align": "center", "margin": "6px", "--hover-color": "white"},
                                   "nav-link-selected": {"background-color": "#1e0ead"},
                               })
        col_1, col_2 = st.columns(2)
        with col_1:
            menu = st.selectbox("Transactions data or User Data",
                                ('Transactions', "User"))
        states_list = df_map_user["State"].unique()
        State = st.selectbox("Select State", (states_list))

    # Quarter = st.selectbox('select a Quarter', ('1', '2', '3', '4'))

    if selected == "Aggregated Data Insights":
        if menu == 'Transactions':
            st.header(State+" State Insights")
            with col_2:
                menu2 = st.selectbox(
                    'Transaction Count or Transaction Amount', ("count", "amount"))
            df = df_aggregated_transaction[df_aggregated_transaction['State'] == State]

            df = df.sort_values(menu2)

            fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color_continuous_scale='PuBu',
                color=menu2,
                animation_frame="Year",
                title=State + " - Transaction "+menu2,

            )

            fig.update_geos(fitbounds="locations", visible=False)
            fig.update_layout(
                width=600,
                height=400
            )
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

            fig = px.sunburst(df,
                              path=['Year', 'Quarter', 'Transaction_type'],
                              values=menu2,
                              title="Transaction " + menu2 + " by Year and Quarter",
                              )
            fig.update_layout(
                width=600,
                height=500
            )
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

            fig = px.bar(df, x=menu2, y="Transaction_type", color="Quarter", animation_frame="Year",
                         title=" Transaction  "+menu2 +
                         "  by Transaction type and its Contribution with respect to Quarter of the year",
                         orientation='h', width=600)

            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

        if menu == 'User':
            st.header(State+" State Insights")
            with col_2:
                menu2 = st.selectbox(
                    'Transaction Count or Transaction Percentage', ("count", "Percentage"))

            df = df_aggregated_user[df_aggregated_user['State'] == State]
            df['Percentage'] = df['Percentage']*100
            df = df.sort_values(menu2)

            fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color_continuous_scale='PuBu',
                color=menu2,
                animation_frame="Year",
                title=State + " - Transaction "+menu2
            )

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)

            fig = px.sunburst(df,
                              path=['Year', 'Quarter', 'brand'],
                              values=menu2,
                              title="Transaction " + menu2 + " by Year and Quarter", height=500)

            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

            fig = px.bar(df, x=menu2, y="brand", color="Quarter", animation_frame="Year",
                         title="Brands by Transaction  "+menu2+"  with respect to Quarter of the year", orientation='h', width=600)
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

    if selected == "Map Data Insights":
        if menu == 'Transactions':
            st.header(State+" State Insights")
            with col_2:
                menu2 = st.selectbox(
                    'Transaction Count or Transaction amount', ("count", "amount"))
            df = df_map_transaction[df_map_transaction['State'] == State]
            df = df.sort_values(menu2)

            fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color_continuous_scale='PuBu',
                color=menu2,
                animation_frame="Year",
                title=State + " - Transaction "+menu2,
            )

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig)

            fig = px.sunburst(df,
                              path=['Year', 'Quarter'],
                              values=menu2,
                              title="Transaction " + menu2 + " by Year and Quarter", height=500)
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

            fig = px.bar(df, x=menu2, y='District', color="Quarter", animation_frame="Year",
                         title="District by Transaction  "+menu2, orientation='h', width=600)
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

        if menu == 'User':
            st.header(State+" State Insights")

            df = df_map_user[df_map_user['State'] == State]

            df = df.sort_values('RegisteredUser')

            fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color_continuous_scale='PuBu',
                color='RegisteredUser',
                animation_frame="Year",
                title=State + ' - RegisteredUser',
            )
            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

            fig = px.sunburst(df, path=[
                              'Year', 'Quarter'], values='RegisteredUser', title="Registered users by Year and Quarter")
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

            fig = px.bar(df, x="RegisteredUser", y='District', color="Quarter", animation_frame="Year",
                         title="Registered users by District", orientation='h', height=900)
            fig.update_layout(barmode='stack')
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

    if selected == "Top Data Insights":
        if menu == 'Transactions':
            st.header(State+" State Insights")
            with col_2:
                menu2 = st.sidebar.selectbox(
                    'Transaction Count or Transaction amount', ("count", "amount"))
            df = df_top_transaction[df_top_transaction['State'] == State]

            fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color_continuous_scale='PuBu',
                color=menu2,
                animation_frame="Year",
                title=State + " - Transaction "+menu2,
            )

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

            fig = px.sunburst(df, path=[
                              'Year', 'Quarter'], values=menu2, title=" Transaction  "+menu2+"  by Year and Quarter")
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

        if menu == 'User':
            st.header(State+" State Insights")

            df = df_top_user[df_top_user['State'] == State]
            fig = px.choropleth(
                df,
                geojson="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson",
                featureidkey='properties.ST_NM',
                locations='State',
                color_continuous_scale='PuBu',
                color='RegisteredUser',
                animation_frame="Year",
                title="Total Registered users in  "+State,
            )

            fig.update_geos(fitbounds="locations", visible=False)
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")

            fig = px.sunburst(df, path=[
                'Year', 'Quarter'], values='RegisteredUser', title="Registered users by Year and Quarter")
            st.plotly_chart(fig, use_container_width=False,
                            theme="streamlit")


if __name__ == '__main__':
    set_page_config(Image.open("phonepe-logo-icon.PNG"), '#3498db')
    display_title(":violet[PhonePe Pulse]")
    selected = display_navigation()
    if selected == "HOME":
        home()
    elif selected == "GEO-INSIGHTS":
        geo_insights()

    elif selected == "DASHBORD":
        dashboard()
