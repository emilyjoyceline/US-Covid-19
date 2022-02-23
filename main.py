import pandas as pd
import numpy as np
import streamlit as st
import plotly.graph_objects as go
import plotly.express as px


covid_cnfrmd = pd.read_csv('covid_confirmed_usafacts.csv')
county_pop = pd.read_csv('covid_county_population_usafacts.csv')
covid_deaths = pd.read_csv('covid_deaths_usafacts.csv')


st.title("Covid-19 Data Visualization")


# Question 1 Solution


#Filtering the required columns
new_df_state = covid_cnfrmd.loc[:,'State':'2022-02-07']

#Grouping according to the state and finding the new total covid cases in each state
s_sum = new_df_state.groupby('State').sum().diff(axis=1)

#dropping the unwanted columns
s_sum.drop(columns=['StateFIPS','2020-01-22','2020-01-23','2020-01-24','2020-01-25','2022-02-06','2022-02-07'],inplace=True)

# finding the weeks and total new covid cases in that week.
new_s_sum_df = s_sum.groupby([i//7 for i in range(0,742)],axis = 1).sum().T

#creating a series of week dates since above cell's grouping will result in column name loss
date_range = pd.period_range(start = '2020-01-26', end = '2022-02-05',freq='W')
date_range = date_range.map(str)

#splitting since period range will return a week
date_range = date_range.str.split('/').str[1]

#creating a series of date range
date_range=pd.Series(date_range)

#assigning date range to a new column weeks in a new df
new_weekly_cases = new_s_sum_df.assign(weeks = date_range)

#making the weeks column as rows and row name as column name
new_weekly_cases.set_index(['weeks'],inplace=True)

#creating a new column in the dataframe and summing the row data to get the total cases
#in the united states in that particular week.
new_weekly_cases['Total weekly new cases'] = new_weekly_cases.sum(axis=1)
#new_weekly_cases.reset_index(level=0,inplace=True)


fig_new_cases = px.line(new_weekly_cases,
                #x = new_weekly_cases['weeks'],
                y = new_weekly_cases['Total weekly new cases'],
                title = 'Weekly new Covid-19 cases'
)

fig_new_cases.update_traces(line_color = "blue")






# Question 2 Solution
#Covid-19 weekly death cases

new_death_df = covid_deaths.loc[:,'State':'2022-02-07']
new_death_df = new_death_df.groupby('State').sum().diff(axis=1)
new_death_df.drop(columns =['StateFIPS','2020-01-22','2020-01-23','2020-01-24','2020-01-25','2022-02-06','2022-02-07'],inplace=True)
new_death_cases = new_death_df.groupby([i//7 for i in range(0,742)],axis = 1).sum().T


date_range_1 = pd.period_range(start = '2020-01-26',end = '2022-02-05',freq='W')
date_range_1 = date_range_1.map(str)
date_range_1 = date_range_1.str.split('/').str[1]
date_range_1= pd.Series(date_range_1)
weekly_death_cases = new_death_cases.assign(weeks = date_range_1)


weekly_death_cases.set_index(['weeks'],inplace = True)
weekly_death_cases['Total deaths'] = weekly_death_cases.sum(axis = 1)



fig_death = px.line(weekly_death_cases,
            y = weekly_death_cases['Total deaths'],
            title = 'Weekly Covid-19 Deaths')

fig_death.update_traces(line_color = "maroon")
#b = st.plotly_chart(fig_death)

option_1 = st.selectbox('Select the type of Visualization',('Line Chart','Maps'))
if option_1 == 'Line Chart':
    option = st.radio('',('Weekly new Covid cases','Weekly new Covid deaths', 'Both'))
    if option == 'Weekly new Covid cases':
        st.plotly_chart(fig_new_cases)
    elif option == 'Weekly new Covid deaths':
        st.plotly_chart(fig_death)

    elif option == 'Both':
        st.plotly_chart(fig_new_cases)
        st.plotly_chart(fig_death)


elif option_1 == 'Maps':
    option_2 = st.radio('',('Weekly new Covid-19 cases US map','Weekly new Covid-19 deaths'))
    if option_2 == 'Weekly new Covid-19 cases US map':
        #Question 3
        covid_county = covid_cnfrmd.loc[:,'countyFIPS':'2022-02-05']
        covid_county['County Name'] = covid_county['County Name'].str.strip()
        covid_county.drop(columns=['StateFIPS','2020-01-22','2020-01-23','2020-01-24','2020-01-25'],inplace=True)
        covid_county= covid_county.groupby(['countyFIPS']).sum().diff(axis =1)

        new_county_cases_1 = covid_county.groupby([i//7 for i in range(0,742)],axis = 1).sum().T
        date_range_2 = pd.period_range(start = '2020-01-26', end = '2022-02-05', freq = 'W')
        date_range_2 = date_range_2.map(str)
        date_range_2 = date_range_2.str.split('/').str[1]
        date_range_2 = pd.Series(date_range_2)

        county_weekly_cases = new_county_cases_1.assign(weeks = date_range_2)
        county_weekly_cases.set_index(['weeks'],inplace = True)


        county_weekly_cases_1 = county_weekly_cases.T

        ### Manipulating population dataframe and merging it with the county weekly cases
        county_population = county_pop.groupby(['countyFIPS']).sum()
        new_df = pd.merge(county_weekly_cases_1,county_population,how='outer',on=['countyFIPS'])
        new_df.dropna(how='any', inplace=True)
        new_df.reset_index(level=0,inplace=True)
        new_df['countyFIPS'] = new_df['countyFIPS'].astype(int)


        ### Finding the covid cases per 100 thousand of population

        new_df.iloc[:,1:106] = new_df.iloc[:,1:106].apply(lambda x: x/(new_df['population']))
        new_df.iloc[:,1:106] = new_df.iloc[:,1:106].apply(lambda y: y*100000).round(2)

        new_df.dropna(inplace=True)

        new_df['countyFIPS'] = new_df['countyFIPS'].astype(str)
        for i in range(1,len(new_df['countyFIPS'])+1):
            if len(new_df['countyFIPS'][i])<5:
                new_df['countyFIPS'][i] = new_df['countyFIPS'][i].zfill(5)

                ### Using plotly coropleth for creating US Map of weekly cases
        #new_data = new_death_df.T.iloc[1:107,:].reset_index(level=0).rename(columns={'index':'date'})


        import json
        from urllib.request import urlopen

        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            counties = json.load(response)


        fig_graph = px.choropleth(new_df,  # Input Pandas DataFrame
                    locations="countyFIPS",  # DataFrame column with locations
                    geojson= counties,
                    color= "2021-12-26",# DataFrame column with color values
                    #hover_name="County Name",
                    color_continuous_scale='burg',
                    range_color=(0,1000)
                    ) # Set to plot as US States
        fig_graph.update_layout(
            title_text = 'Covid-19 Weekly new cases in each US county', # Create a Title
            geo_scope='usa',  # Plot only the USA instead of globe
)

#graph_option = st.radio('',('Weekly new Covid cases US Map','Weekly new Covid deaths US Map', 'Both'))
#if graph_option == 'Weekly new Covid cases US Map':
        fig_graph.show()


    elif option_2 == 'Weekly new Covid-19 deaths':
        #Question 4
        new_death_df_1 = covid_deaths.loc[:,'countyFIPS':'2022-02-07']
        new_death_df_1 = new_death_df_1.groupby('countyFIPS').sum().diff(axis=1)
        new_death_df_1.drop(columns =['StateFIPS','2020-01-22','2020-01-23','2020-01-24','2020-01-25','2022-02-06','2022-02-07'],inplace=True)
        new_death_cases_1 = new_death_df_1.groupby([i//7 for i in range(0,742)],axis = 1).sum().T


        date_range_2 = pd.period_range(start = '2020-01-26',end = '2022-02-05',freq='W')
        date_range_2 = date_range_2.map(str)
        date_range_2 = date_range_2.str.split('/').str[1]
        date_range_2 = pd.Series(date_range_2)
        weekly_death_cases_4 = new_death_cases_1.assign(weeks = date_range_1)


        weekly_death_cases_4.set_index(['weeks'],inplace = True)
        weekly_death_cases_4 = weekly_death_cases_4.T

        county_population = county_pop.groupby(['countyFIPS']).sum()

        new_death_df = pd.merge(weekly_death_cases_4,county_population,how='outer',on=['countyFIPS'])
        new_death_df.reset_index(level =0,inplace = True)
#new_death_df.reset_index(level =0,inplace = True)
        new_death_df['countyFIPS'] = new_death_df['countyFIPS'].astype(int)
        new_death_df.iloc[:,1:106] = new_death_df.iloc[:,1:106].apply(lambda x: x/(new_death_df['population']))
        new_death_df.iloc[:,1:106] = new_death_df.iloc[:,1:106].apply(lambda y: y*100000).round(2)

        new_death_df.dropna(inplace=True)

        new_death_df['countyFIPS'] = new_death_df['countyFIPS'].astype(str)
        for i in range(1,len(new_death_df['countyFIPS'])+1):
            if len(new_death_df['countyFIPS'][i])<5:
                new_death_df['countyFIPS'][i] = new_death_df['countyFIPS'][i].zfill(5)

        import json
        from urllib.request import urlopen

        with urlopen('https://raw.githubusercontent.com/plotly/datasets/master/geojson-counties-fips.json') as response:
            counties = json.load(response)

        fig_death = px.choropleth(new_death_df,  # Input Pandas DataFrame
                    locations="countyFIPS",  # DataFrame column with locations
                    geojson= counties,
                    color= "2021-12-26",# DataFrame column with color values
                    #hover_name="County Name",
                    color_continuous_scale='blues',
                    range_color=(0,95)
                    ) # Set to plot as US States
        fig_death.update_layout(
        title_text = 'Covid 19 Weekly new deaths in each US county', # Create a Title
        geo_scope='usa',  # Plot only the USA instead of globe
)
        fig_death.show()
