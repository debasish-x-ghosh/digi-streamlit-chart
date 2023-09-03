import pandas as pd
import streamlit as st
import plotly.express as px
from PIL import Image


# Tabs
tab1, tab2, tab3 = st.tabs(["Survey_Results", "project2", "project3"])

with tab1: 
        #st.set_page_config(page_title='Survey Results')
        st.header('Survey Results 2021')
        st.subheader('Drill down all options')
        

with tab2:
        st.header("project2") 

with tab3:
        st.header("project3") 


# !!! --- Tab1 Body starts
### --- LOAD DATAFRAME
excel_file = 'Survey_Results.xlsx'
sheet_name = 'DATA'

df = pd.read_excel(excel_file,
                sheet_name=sheet_name,
                usecols='B:D',
                header=3)

df_participants = pd.read_excel(excel_file,
                                sheet_name= sheet_name,
                                usecols='F:G',
                                header=3)
df_participants.dropna(inplace=True)

# --- STREAMLIT SELECTION
department = df['Department'].unique().tolist()
ages = df['Age'].unique().tolist()

age_selection = tab1.slider('Age:',
                        min_value= min(ages),
                        max_value= max(ages),
                        value=(min(ages),max(ages)))

department_selection = tab1.multiselect('Department:',
                                department,
                                default=department)

# --- FILTER DATAFRAME BASED ON SELECTION
mask = (df['Age'].between(*age_selection)) & (df['Department'].isin(department_selection))
number_of_result = df[mask].shape[0]
tab1.markdown(f'*Available Results: {number_of_result}*')

# --- GROUP DATAFRAME AFTER SELECTION
df_grouped = df[mask].groupby(by=['Rating']).count()[['Age']]
df_grouped = df_grouped.rename(columns={'Age': 'Votes'})
df_grouped = df_grouped.reset_index()

# --- PLOT BAR CHART
bar_chart = px.bar(df_grouped,
                x='Rating',
                y='Votes',
                text='Votes',
                color_discrete_sequence = ['#F63366']*len(df_grouped),
                template= 'plotly_white')
tab1.plotly_chart(bar_chart)

# --- DISPLAY IMAGE & DATAFRAME
col1, col2 = tab1.columns(2)
image = Image.open('images/survey.jpg')
col1.image(image,
        caption='Designed by slidesgo / Freepik',
        use_column_width=True)
col2.dataframe(df[mask])

# --- PLOT PIE CHART
pie_chart = px.pie(df_participants,
                title='Total No. of Participants',
                values='Participants',
                names='Departments')

tab1.plotly_chart(pie_chart)
# !!! --- Tab1 Body ends
