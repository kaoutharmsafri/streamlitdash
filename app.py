import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go

st.set_page_config(
    page_title='My Streamlit Data Dashboard',
    page_icon=':bar_chart:',
    layout='wide'
)


st.title('My Streamlit Data Dashboard')
def load_data():
    # csv_path = "./Road_Accident_Data.csv"
    # data = pd.read_csv(csv_path, delimiter=';')
    uploaded_file = st.file_uploader("Road Accident Data.csv", type="csv")
    data = pd.read_csv(uploaded_file, delimiter=';')
    data['Accident Date'] = pd.to_datetime(data['Accident Date'], format='%d/%m/%Y')
    # Extract year, month, and date into separate columns
    data['Year'] = data['Accident Date'].dt.year
    data['Month'] = data['Accident Date'].dt.month
    data['Day'] = data['Accident Date'].dt.day
    # with st.expander('Accident Date Preview'):
    #     st.dataframe(data[['Accident Date', 'Year', 'Month', 'Day']])
    return data 

data_load_state = st.text('Loading data...')
data = load_data()
data_load_state.text('Loading data...done!')

st.subheader('Data')
with st.expander('Data Preview'):
    st.dataframe(data)

monthly_casualties = data.groupby(['Year', 'Month'])['Number_of_Casualties'].sum().reset_index()

fig = go.Figure()

year_2021_data = monthly_casualties[monthly_casualties['Year'] == 2021]
fig.add_trace(go.Scatter(x=year_2021_data['Month'], y=year_2021_data['Number_of_Casualties'],
                         fill='tozeroy', mode='lines+markers',line_color='#8743e2', name='Year 2021'))

# Add a trace for 2022
year_2022_data = monthly_casualties[monthly_casualties['Year'] == 2022]
fig.add_trace(go.Scatter(x=year_2022_data['Month'], y=year_2022_data['Number_of_Casualties'],
                         fill='tozeroy', mode='lines+markers',line_color='#ffffff', name='Year 2022'))

# Update layout
fig.update_layout(title='Monthly Casualties for 2021 and 2022',
                  xaxis_title='Month',
                  yaxis_title='Number of Casualties',
                  xaxis=dict(tickmode='linear', tick0=1, dtick=1))

# Display the chart using Streamlit
st.plotly_chart(fig,use_container_width=True)


#=============================================
# Static path to the Excel file with multiple sheets
excel_path = "./Guide.xlsx"
xls = pd.ExcelFile(excel_path)
sheet_names = xls.sheet_names
# selected_sheet = st.selectbox("Select a sheet", sheet_names)
selected_sheet = 'Urban_or_Rural_Area'
st.subheader('File with multiple sheets')
df = pd.read_excel(excel_path, sheet_name=selected_sheet)
with st.expander('Data Preview'):
    st.dataframe(df)

#=============================================.
data['CY_Casualties'] = data.groupby('Year')['Number_of_Casualties'].cumsum()
fig = px.pie(data, values=data['CY_Casualties'], names=selected_sheet,color_discrete_sequence=['#ffffff', '#8743e2'])
fig.update_traces(textposition='inside', textinfo='percent+label',textfont_size=20,)
st.plotly_chart(fig,use_container_width=True)

#=============================================.
selected_sheet = 'Light_Conditions'
df = pd.read_excel(excel_path, sheet_name=selected_sheet)
data['CY_Casualties'] = data.groupby('Year')['Number_of_Casualties'].cumsum()
fig = px.pie(data, values=data['CY_Casualties'], names=selected_sheet,color_discrete_sequence=px.colors.sequential.Blues_r)
fig.update_traces(textposition='inside', textinfo='percent+label',textfont_size=20,)
st.plotly_chart(fig,use_container_width=True)

#=============================================

df['label'] = df['label'].replace({
    "Darkness - lights lit": "Darkness",
    "Darkness - lighting unknown": "Darkness",
    "Darkness - no lighting": "Darkness",
    "Darkness - lights unlit": "Darkness",
    "Daylight": "Daylight"
})
df['CY_Casualties'] = data.groupby('Year')['Number_of_Casualties'].cumsum()

# fig = px.pie(df, names='label', title='Light Conditions Distribution')
fig = px.pie(df, names='label', values='CY_Casualties', title='Light Conditions Distribution with Cumulative Casualties')

st.plotly_chart(fig)

#=============================================
