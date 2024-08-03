import streamlit as st 
from streamlit_option_menu import option_menu
import psycopg2
import pandas as pd 
import plotly.express as px
import requests
import json
from PIL import Image

mydb=psycopg2.connect(host="localhost",
                            user="postgres",
                            password="sumareddy",
                            database="phonepe_data",
                            port="5432")
cursor = mydb.cursor()

url="https://gist.githubusercontent.com/jbrobst/56c13bbbf9d97d187fea01ca62ea5112/raw/e388c4cae20aa53cb5090210a42ebb9b765c0a36/india_states.geojson"
response=requests.get(url)
data=json.loads(response.content)
states_name=[]
for feature in data["features"]:
    states_name.append(feature["properties"]["ST_NM"])
states_name.sort()


#sql query for top charts


def top_chart_transaction_amount(table_name):
    mydb= psycopg2.connect(host="localhost",
                        user="postgres",
                        password="sumareddy",
                        database="phonepe_data",
                        port="5432")
    cursor= mydb.cursor()

    #plot_1
    query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name }
                GROUP BY states
                ORDER BY transaction_amount DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()
    df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="transaction_amount", title="TOP 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount
                LIMIT 10;'''
    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()
    df_2= pd.DataFrame(table_2, columns=("states", "transaction_amount"))
    
    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_amount", title="LAST 10 OF TRANSACTION AMOUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(transaction_amount) AS transaction_amount
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_amount;'''
    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()

    df_3= pd.DataFrame(table_3, columns=("states", "transaction_amount"))
    fig_amount_3= px.bar(df_3, y="states", x="transaction_amount", title="AVERAGE OF TRANSACTION AMOUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_transaction_count(table_name):
    mydb= psycopg2.connect(host="localhost",
                        user="postgres",
                        password="sumareddy",
                        database="phonepe_data",
                        port="5432")
    cursor= mydb.cursor()
    query1= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name }
                GROUP BY states
                ORDER BY transaction_count DESC
                LIMIT 10; '''

    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()
    df_1= pd.DataFrame(table_1, columns=("states", "transaction_count"))
    #plot_1
    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="transaction_count", title="TOP 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count
                LIMIT 10;'''

    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()
    df_2= pd.DataFrame(table_2, columns=("states", "transaction_count"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="transaction_count", title="LAST 10 OF TRANSACTION COUNT", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(transaction_count) AS transaction_count
                FROM {table_name}
                GROUP BY states
                ORDER BY transaction_count;'''
    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table_3, columns=("states", "transaction_count"))

    fig_amount_3= px.bar(df_3, y="states", x="transaction_count", title="AVERAGE OF TRANSACTION COUNT", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_registered_user(table_name, state):
    mydb= psycopg2.connect(host="localhost",
                        user="postgres",
                        password="sumareddy",
                        database="phonepe_data",
                        port="5432")
    cursor= mydb.cursor()
    #plot_1
    query1= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()
    df_1= pd.DataFrame(table_1, columns=("districts", "registereduser"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="registereduser", title="TOP 10 OF REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser
                LIMIT 10;'''
    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()
    df_2= pd.DataFrame(table_2, columns=("districts", "registereduser"))

    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="registereduser", title="LAST 10 REGISTERED USER", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(registereduser) AS registereduser
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY registereduser;'''
    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table_3, columns=("districts", "registereduser"))
    fig_amount_3= px.bar(df_3, y="districts", x="registereduser", title="AVERAGE OF REGISTERED USER", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_appopens(table_name, state):
    mydb= psycopg2.connect(host="localhost",
                        user="postgres",
                        password="sumareddy",
                        database="phonepe_data",
                        port="5432")
    cursor= mydb.cursor()
    #plot_1
    query1= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()
    df_1= pd.DataFrame(table_1, columns=("districts", "appopens"))

    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="districts", y="appopens", title="TOP 10 OF APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT districts, SUM(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens
                LIMIT 10;'''
    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()
    df_2= pd.DataFrame(table_2, columns=("districts", "appopens"))

    with col2:
        fig_amount_2= px.bar(df_2, x="districts", y="appopens", title="LAST 10 APPOPENS", hover_name= "districts",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT districts, AVG(appopens) AS appopens
                FROM {table_name}
                WHERE states= '{state}'
                GROUP BY districts
                ORDER BY appopens;'''
    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table_3, columns=("districts", "appopens"))
    fig_amount_3= px.bar(df_3, y="districts", x="appopens", title="AVERAGE OF APPOPENS", hover_name= "districts", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)

#sql connection
def top_chart_registered_users(table_name):
    mydb= psycopg2.connect(host="localhost",
                        user="postgres",
                        password="sumareddy",
                        database="phonepe_data",
                        port="5432")
    cursor= mydb.cursor()
    #plot_1
    query1= f'''SELECT states, SUM(registereduser) AS registereduser
                FROM {table_name}
                GROUP BY states
                ORDER BY registereduser DESC
                LIMIT 10;'''
    cursor.execute(query1)
    table_1= cursor.fetchall()
    mydb.commit()
    df_1= pd.DataFrame(table_1, columns=("states", "registereduser"))
    
    col1,col2= st.columns(2)
    with col1:
        fig_amount= px.bar(df_1, x="states", y="registereduser", title="TOP 10 OF REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl, height= 650,width= 600)
        st.plotly_chart(fig_amount)

    #plot_2
    query2= f'''SELECT states, SUM(registereduser) AS registereduser
                FROM {table_name}
                GROUP BY states
                ORDER BY registereduser
                LIMIT 10;'''
    cursor.execute(query2)
    table_2= cursor.fetchall()
    mydb.commit()
    df_2= pd.DataFrame(table_2, columns=("states", "registereduser"))

    with col2:
        fig_amount_2= px.bar(df_2, x="states", y="registereduser", title="LAST 10 REGISTERED USERS", hover_name= "states",
                            color_discrete_sequence=px.colors.sequential.Aggrnyl_r, height= 650,width= 600)
        st.plotly_chart(fig_amount_2)

    #plot_3
    query3= f'''SELECT states, AVG(registereduser) AS registereduser
                FROM {table_name}
                GROUP BY states
                ORDER BY registereduser;'''
    cursor.execute(query3)
    table_3= cursor.fetchall()
    mydb.commit()
    df_3= pd.DataFrame(table_3, columns=("states", "registereduser"))
    fig_amount_3= px.bar(df_3, y="states", x="registereduser", title="AVERAGE OF REGISTERED USERS", hover_name= "states", orientation= "h",
                        color_discrete_sequence=px.colors.sequential.Bluered_r, height= 800,width= 1000)
    st.plotly_chart(fig_amount_3)



#Streamlit part
st.set_page_config(layout="wide")

st.title("PHONEPE DATA VISUALIZATION AND EXPLORATION")

with st.sidebar:
    select= option_menu("Main Menu",["Home", "Data Exploration", "Top Charts"])

if select=="Home":
    col1,col2= st.columns(2)

    with col1:
        st.header("PHONEPE")
        st.subheader("INDIA'S BEST TRANSACTION APP")
        st.markdown("PhonePe  is an Indian digital payments and financial technology company")
        st.write("****FEATURES****")
        st.write("****Credit & Debit card linking****")
        st.write("****Bank Balance check****")
        st.write("****Money Storage****")
        st.write("****PIN Authorization****")
        st.download_button("DOWNLOAD THE APP NOW", "https://www.phonepe.com/app-download/")
    with col2:
        st.image(Image.open(r"C:\Users\Suma Reddy\Desktop\phonepe.jpg"),width= 400)

elif select=="Data Exploration":
    tab1, tab2,= st.tabs(["Transaction Analysis", "User Analysis"])

    with tab1:
            
        col1,col2,col3= st.columns(3)
        with col1:
            table=st.selectbox("Select the table",["aggregated_insurance","aggregated_transaction","map_insurance","map_transaction","top_insurance","top_transaction"])
        with col2:
            years=st.selectbox("Select the year",["2018","2019","2020","2021", "2022", "2023","2024"]) 
        with col3:
            quarters=st.selectbox("Select the Quarter",["1","2","3","4"])
        query1= f'''SELECT states, SUM(transaction_amount) AS transaction_amount,SUM(transaction_count) AS transaction_count
        FROM {table}
        where years={years} and quarter={quarters}
        GROUP BY states'''
        cursor.execute(query1)
        table_1= cursor.fetchall()
        mydb.commit()
        df_1= pd.DataFrame(table_1, columns=("states", "transaction_amount","transaction_count"))
        
        col1,col2=st.columns(2)
        with col1:
            fig_amount=px.bar(df_1,x="states",y="transaction_amount",title=f"{years} {quarters} Transaction_amount",color_discrete_sequence=px.colors.sequential.Aggrnyl,height=650,width=600)
            st.plotly_chart(fig_amount)
        with col2:
            fig_count=px.bar(df_1,x="states",y="transaction_count",title=f"{years} {quarters} Transaction_count",color_discrete_sequence=px.colors.sequential.Bluered_r,height=650,width=600)
            st.plotly_chart(fig_count)

        col1,col2= st.columns(2)
        with col1:
            
            fig_india_1=px.choropleth(df_1,geojson=data,locations="states",featureidkey="properties.ST_NM",color="transaction_amount",color_continuous_scale="Rainbow",range_color=(df_1["transaction_amount"].min(), df_1["transaction_amount"].max()), hover_name="states",title=f"{years} {quarters} TRANSACTION AMOUNT",fitbounds="locations",height=650,width=600)  
            fig_india_1.update_geos(visible= False)
            st.plotly_chart(fig_india_1)

        with col2:
            fig_india_2=px.choropleth(df_1,geojson=data,locations="states",featureidkey="properties.ST_NM",color="transaction_count",color_continuous_scale="Rainbow",range_color=(df_1["transaction_count"].min(), df_1["transaction_count"].max()), hover_name="states",title=f"{years} {quarters} TRANSACTION COUNT",fitbounds="locations",height=650,width=600) 
            fig_india_2.update_geos(visible= False)
            st.plotly_chart(fig_india_2)

        if table=="aggregated_transaction":
            states=st.selectbox("Select the UStates",["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himchal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"])
            query1=f'''SELECt transaction_type as transaction_type,  SUM(transaction_amount) AS transaction_amount,SUM(transaction_count) AS transaction_count
                FROM aggregated_transaction
                where  years={years}  and states='{states}' and quarter={quarters}
                GROUP BY transaction_type,states
				order by transaction_type'''
            cursor.execute(query1)
            table_1= cursor.fetchall()
            mydb.commit()
            df_1= pd.DataFrame(table_1, columns=("transaction_type", "transaction_amount","transaction_count"))

            col1,col2=st.columns(2)
            with col1:
                fig_pie_1= px.pie(df_1,names="transaction_type",values="transaction_amount",title=f"{years} Year {quarters} Quarter {states.upper()} Transaction Amount",hole=0.5)
                st.plotly_chart(fig_pie_1)
            with col2:
                fig_pie_2= px.pie(df_1,names="transaction_type",values="transaction_count",title=f"{years} Year {quarters} Quarter {states.upper()} Transaction Count",hole=0.5)
                st.plotly_chart(fig_pie_2)


        if table=="map_insurance":
            states=st.selectbox("Select the UStates",["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himchal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"])
            query1=f''' select district , SUM(transaction_amount) AS transaction_amount,SUM(transaction_count) AS transaction_count
                from map_insurance
                where years={years} and states='{states}' and quarter={quarters}
                group by district'''
            cursor.execute(query1)
            table_1= cursor.fetchall()
            mydb.commit()
            df_1= pd.DataFrame(table_1, columns=("district","transaction_amount","transaction_count"))

            col1,col2=st.columns(2)
            with col1:
                fig_bar_1=px.bar(df_1,x="transaction_amount",y="district",orientation="h",height=600,title=f"{years} Year {quarters} Quarter {states.upper()} Distric and Transaction Amount " ,color_discrete_sequence=px.colors.sequential.haline)
                st.plotly_chart(fig_bar_1)
            with col2:
                fig_bar_2=px.bar(df_1,x="transaction_count",y="district",orientation="h",height=600,title=f"{years} Year {quarters} Quarter {states.upper()} Distric and Transaction Count " ,color_discrete_sequence=px.colors.sequential.haline)
                st.plotly_chart(fig_bar_2)

        if table =="map_transaction":
            states=st.selectbox("Select the mStates",["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himchal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"])
            query1=f''' select district , SUM(transaction_amount) AS transaction_amount,SUM(transaction_count) AS transaction_count
                from map_transaction
                where years={years} and states='{states}' and quarter={quarters}
                group by district'''
            cursor.execute(query1)
            table_1= cursor.fetchall()
            mydb.commit()
            df_1= pd.DataFrame(table_1, columns=("district","transaction_amount","transaction_count"))

            col1,col2=st.columns(2)
            with col1:
                fig_bar_1=px.bar(df_1,x="transaction_amount",y="district",orientation="h",height=600,title=f"{years} Year {quarters} Quarter {states.upper()} District and Transaction Amount " ,color_discrete_sequence=px.colors.sequential.haline)
                st.plotly_chart(fig_bar_1)
            with col2:
                fig_bar_2=px.bar(df_1,x="transaction_count",y="district",orientation="h",height=600,title=f"{years} Year {quarters} Quarter {states.upper()} District and Transaction Count " ,color_discrete_sequence=px.colors.sequential.haline)
                st.plotly_chart(fig_bar_2)



    with tab2:
        method=st.radio("Select the User Analysis Method",["Aggregated User", "Map User", "Top User"])

        if method=="Aggregated User":
            col1,col2,col3= st.columns(3)
            with col1:
                years=st.selectbox("Select the AUyear",["2018","2019","2020","2021"])
            with col2:
                quarters=st.selectbox("Select the AUQuarter",["4"])
            with col3:
                states=st.selectbox("Select the AUStates",["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himchal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"])
            query1=f'''select percentage, brands, sum(transaction_count) as transaction_count
                from aggregated_user
                where years={years} and quarter={quarters} and states='{states}'
                group by brands,percentage'''
            cursor.execute(query1)
            table_1= cursor.fetchall()
            mydb.commit()
            df_1= pd.DataFrame(table_1, columns=("percentage","brands", "transaction_count"))
            fig_bar_1=px.line(df_1,x="brands", y="transaction_count", title=f"{states.upper()} Brands and Transaction count and Percentage",width=1000,hover_data="percentage",markers=True)
            st.plotly_chart(fig_bar_1)

        if method=="Map User":
            col1,col2,col3= st.columns(3)
            with col1:
                years=st.selectbox("Select the Myear",["2018","2019","2020","2021"])
            with col2:
                quarters=st.selectbox("Select the MUQuarter",["1","2","3","4"])
            with col3:
                states=st.selectbox("Select the MUStates",["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himchal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"])
           
            query1=f'''select states ,sum(registereduser) as registereduser ,districts,sum(appopens) as appopens
                from map_user
                where years={years} and quarter={quarters} and states='{states}'
                group by states,districts'''
            cursor.execute(query1)
            table_1= cursor.fetchall()
            mydb.commit()
            df_1= pd.DataFrame(table_1, columns=("states", "registereduser","districts","appopens"))

            col1,col2=st.columns(2)
            with col1:
                fig_bar_1=px.bar(df_1,y="districts", x="registereduser", title=f"{years} {quarters} Quarter {states} RegisteredUser ",width=650,height=650,color_discrete_sequence=px.colors.sequential.haline,orientation="h")
                st.plotly_chart(fig_bar_1)
            with col2:
                fig_bar_2=px.bar(df_1,y="districts", x="appopens", title=f"{years} {quarters} Quarter {states} AppOpens",width=650,height=650,color_discrete_sequence=px.colors.sequential.haline,orientation="h")
                st.plotly_chart(fig_bar_2)


        if method=="Top User":

                years=st.selectbox("Select the TuYear",["2018","2019","2020","2021", "2022", "2023","2024"])
        
                query1=f''' select states , registereduser ,quarter 
                from top_user
                where years={years}
                group by states , quarter,registereduser'''
                cursor.execute(query1)
                table_1= cursor.fetchall()
                mydb.commit()
                df_1= pd.DataFrame(table_1, columns=("states", "registereduser","quarter"))
                fig_top_user_1=px.bar(df_1,x="states",y="registereduser", title=f"{years} RegisteredUser",width=1000,height=800,color_discrete_sequence=px.colors.sequential.Burgyl,color="quarter",hover_name="states")
                st.plotly_chart(fig_top_user_1)
         

                states=st.selectbox("Select the TuStates",["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himchal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"])
            
                query1=f''' select states , registereduser ,quarter ,pincodes
                from top_user
                where years={years} and states='{states}'
                group by states , quarter,registereduser ,pincodes'''
                cursor.execute(query1)
                table_1= cursor.fetchall()
                mydb.commit()

                df_1= pd.DataFrame(table_1, columns=("states", "registereduser","quarter","pincodes"))
                fig_top_user_1=px.bar(df_1,x="quarter",y="registereduser", title=f"{years} {states} RegisteredUser",width=1000,height=800,color_discrete_sequence=px.colors.sequential.Burgyl,color="registereduser",hover_data="pincodes")
                st.plotly_chart(fig_top_user_1)


elif select=="Top Charts":
    question= st.selectbox("Select the Question",["1. Transaction Amount and Count of Aggregated Insurance",
                                                    "2. Transaction Amount and Count of Map Insurance",
                                                    "3. Transaction Amount and Count of Top Insurance",
                                                    "4. Transaction Amount and Count of Aggregated Transaction",
                                                    "5. Transaction Amount and Count of Map Transaction",
                                                    "6. Transaction Amount and Count of Top Transaction",
                                                    "7. Transaction Count of Aggregated User",
                                                    "8. Registered users of Map User",
                                                    "9. App opens of Map User",
                                                    "10. Registered users of Top User"])
    

    
    if question == "1. Transaction Amount and Count of Aggregated Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_insurance")

    elif question == "2. Transaction Amount and Count of Map Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_insurance")

    elif question == "3. Transaction Amount and Count of Top Insurance":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_insurance")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_insurance")

    elif question == "4. Transaction Amount and Count of Aggregated Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("aggregated_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_transaction")

    elif question == "5. Transaction Amount and Count of Map Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("map_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("map_transaction")

    elif question == "6. Transaction Amount and Count of Top Transaction":
        
        st.subheader("TRANSACTION AMOUNT")
        top_chart_transaction_amount("top_transaction")

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("top_transaction")

    elif question == "7. Transaction Count of Aggregated User":

        st.subheader("TRANSACTION COUNT")
        top_chart_transaction_count("aggregated_user")

    elif question == "8. Registered users of Map User":
        
        states= st.selectbox("Select the State",["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himchal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"])   
        st.subheader("REGISTERED USERS")
        top_chart_registered_user("map_user", states)

    elif question == "9. App opens of Map User":
        
        states= st.selectbox("Select the state", ["Andaman & Nicobar","Andhra Pradesh","Arunachal Pradesh","Assam","Bihar","Chandigarh","Chhattisgarh","Dadra and Nagar Haveli and Daman and Diu","Delhi","Goa","Gujarat","Haryana","Himchal Pradesh","Jammu & Kashmir","Jharkhand","Karnataka","Kerala","Ladakh","Lakshadweep","Madhya Pradesh","Maharashtra","Manipur","Meghalaya","Mizoram","Nagaland","Odisha","Puducherry","Punjab","Rajasthan","Sikkim","Tamil Nadu","Tripura","Uttar Pradesh","Uttarakhand","West Bengal"])   
        st.subheader("APPOPENS")
        top_chart_appopens("map_user", states)

    elif question == "10. Registered users of Top User":
          
        st.subheader("REGISTERED USERS")
        top_chart_registered_users("top_user")



