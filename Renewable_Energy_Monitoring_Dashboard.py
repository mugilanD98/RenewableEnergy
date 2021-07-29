import pandas as pd
import streamlit as st 
import numpy as np 
import plotly.figure_factory as ff 
import plotly.express as px
import plotly.offline as pyo
import plotly.graph_objs as go

import time
from sqlalchemy import create_engine
from datetime import datetime
from datetime import timedelta
from datetime import date
from dateutil.relativedelta import relativedelta



# Set Min Date
min_dt = (date.today() - relativedelta(months=1)).strftime("%Y-%m-01")

db_connection_str = 'mysql+pymysql://admin:VRhmqZPY@mysql-41080-0.cloudclusters.net:18738/energy'
db_connection = create_engine(db_connection_str)

#For Overall Summary - 3 Cards

overall_summary_df = pd.read_sql('SELECT * FROM daily_overall_summary', con=db_connection)

co2 = overall_summary_df.loc[0, 'co']

report_date = overall_summary_df.loc[0, 'report_date']

report_date_format = overall_summary_df.loc[0, 'report_date_format']

latest_sw_df = pd.read_sql('SELECT * FROM energy_state_level WHERE lower(state) like "all india" and report_date = "'+str(report_date_format)+'"', con=db_connection)

solar_number = latest_sw_df.loc[0, 'solar']

solar_number = round(solar_number,1)

wind_number = latest_sw_df.loc[0, 'wind']

wind_number = round(wind_number,1)

solar_perc = latest_sw_df.loc[0, 'solar']*100/ latest_sw_df.loc[0, 'total']

solar_perc = str(round(solar_perc,1)) + '%'

wind_perc = latest_sw_df.loc[0, 'wind']*100/ latest_sw_df.loc[0, 'total']

wind_perc = str(round(wind_perc,1)) + '%'

st.markdown('''
            <p><h1>Dialy Renewable Energy Generation - Monitoring Dashboard</h1></p>
            <div style="height:150px;width: 30%;background-color: #d1f0a2; float:left; left: 0px; border-radius: 2px;">
                    <div>
                        <div style="font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size: 30px; padding: 20px 0px 0px 25px;">'''+str(co2)+''' <span style="font-size: 15px; font-weight: normal">tCO<sub>2</sub></span> </div>
                        <div style="padding: 0px 0px 0px 25px;">CO<sub>2</sub> emissions mitigated</div>                        
                        <div style="font-family: Arial, Helvetica, sans-serif; font-weight: bold; color: #33adff; font-size: 12px; padding: 5px 0px 0px 25px;">'''+ report_date +'''</div>
                    </div>
            </div>  

            <div style="height:150px;width: 2%; background-color: white; float:left;">
            </div>

            <div style="height:150px;width: 20%; background-color: white; float:left; left: 700px; border-radius: 2px; border: 2px solid #d9d9d9; border-right: None;">
                    <div>
                        <div style="font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size: 30px; padding: 10px 0px 0px 25px;">'''+ str(solar_number) +''' <span style="font-size: 15px; font-weight: normal">MU</span> </div>
                        <div style="padding: 0px 0px 0px 25px;">Solar<br>generation</br></div>                        
                        <div style="font-family: Arial, Helvetica, sans-serif; font-weight: bold; color: #33adff; font-size: 12px; padding: 5px 0px 0px 25px;">'''+ report_date +'''</div>
                    </div>
            </div>

            <div style="height:150px;width: 13%; background-color: white; float:left; left: 850px; border-radius: 2px; border: 2px solid #d9d9d9; border-left: None;">
                    <div>
                        <div style="font-family: Arial, Helvetica, sans-serif; font-weight: bold; color: #ff661a; font-size: 20px; padding: 35px 0px 0px 25px;">'''+ str(solar_perc) +''' </div>
                        <div style="padding: 10px 0px 0px 0px;font-size: 12px; font-weight: normal; text-align: center;">of total RE generation</br></div>                        
                    </div>
            </div>

            <div style="height:150px;width: 2%; background-color: white; float:left;">
            </div>

            <div style="height:150px;width: 20%; background-color: white; float:left; left: 1200px; border-radius: 2px; border: 2px solid #d9d9d9; border-right: None;">
                    <div>
                        <div style="font-family: Arial, Helvetica, sans-serif; font-weight: bold; font-size: 30px; padding: 10px 0px 0px 25px;">'''+ str(wind_number) +''' <span style="font-size: 15px; font-weight: normal">MU</span> </div>
                        <div style="padding: 0px 0px 0px 25px;">Wind<br>generation</br></div>                        
                        <div style="font-family: Arial, Helvetica, sans-serif; font-weight: bold; color: #33adff; font-size: 12px; padding: 5px 0px 0px 25px;">'''+ report_date +'''</div>
                    </div>
            </div>

            <div style="height:150px;width: 13%; background-color: white; float:left; left: 1350px; border-radius: 2px; border: 2px solid #d9d9d9; border-left: None;">
                    <div>
                        <div style="font-family: Arial, Helvetica, sans-serif; font-weight: bold; color: #1a8cff; font-size: 20px; padding: 35px 0px 0px 25px;">'''+ str(wind_perc) +''' </div>
                        <div style="padding: 10px 0px 0px 0px;font-size: 12px; font-weight: normal; text-align: center;">of total RE generation</br></div>                        
                    </div>
            </div>                                         
    ''' , unsafe_allow_html=True);


allindia_sw_df = pd.read_sql('SELECT report_date, solar, wind, others FROM energy_state_level WHERE lower(state) like "all india" and report_date >= "'+min_dt+'" order by report_date asc', con=db_connection)


#Renewable Energy - Current and Last Month Trend

trace0 = go.Scatter(x=allindia_sw_df['report_date'], y=allindia_sw_df['solar'], mode='markers+lines', name='Solar Energy')
trace1 = go.Scatter(x=allindia_sw_df['report_date'], y=allindia_sw_df['wind'], mode='markers+lines', name='Wind Energy')
trace2 = go.Scatter(x=allindia_sw_df['report_date'], y=allindia_sw_df['others'], mode='markers+lines', name='Other RE Energy')

trend_lines = [trace0, trace1, trace2]
layout = go.Layout(title = 'All India Renewable Energy - Current and Last Month Trend')
line_fig = go.Figure(data = trend_lines, layout=layout)
line_fig.update_layout(xaxis_title = 'Report Date', yaxis_title = 'Energy (MU)')

st.write(line_fig)


st.markdown('''<p><h2>State/ Region Level - Daily Renewalble Energy Generation ('''+report_date+')'+'''</h2></p>''', unsafe_allow_html=True)

host_source = st.selectbox('Select EnergySource:',('Wind Energy', 'Solar Energy', 'Other Renewable Energy', 'Total Renewable Energy'))
st.write('You selected:', host_source)


state_sw_df = pd.read_sql('SELECT state as "State", solar as "Solar Energy", wind as "Wind Energy", total as "Total Renewable Energy", others as "Other Renewable Energy" FROM energy_state_level WHERE lower(state) not in ("all india","northern region","western region","southern region","eastern region","north-eastern region") and report_date = "'+str(report_date_format)+'" order by total asc', con=db_connection)

state_sw_df = state_sw_df.sort_values(by=[host_source], ascending=True)

bar_fig = px.bar(state_sw_df, x=host_source,y='State')
bar_fig.update_layout(xaxis_title = host_source + ' (MU)', yaxis_title = 'State')

st.write(bar_fig)


region_sw_df = pd.read_sql('SELECT state as "Region", solar as "Solar Energy", wind as "Wind Energy", total as "Total Renewable Energy", others as "Other Renewable Energy" FROM energy_state_level WHERE lower(state) in ("northern region","western region","southern region","eastern region","north-eastern region") and report_date = "'+str(report_date_format)+'" order by total asc', con=db_connection)

region_sw_df = region_sw_df.sort_values(by=[host_source], ascending=True)

reg_bar_fig = px.bar(region_sw_df, x=host_source,y='Region')
reg_bar_fig.update_layout(xaxis_title = host_source + ' (MU)', yaxis_title = 'Region')

st.write(reg_bar_fig)


st.markdown('''<p><h2>State/ Sector Level Vs Capacity/ Generation - ISGS ('''+report_date+')'+'''</h2></p>''', unsafe_allow_html=True)

host_isgs_source = st.selectbox('Select Capacity/ Generation:',('Installed Capacity', 'Actual Capacity'))
st.write('You selected:', host_isgs_source)


state_isgs_df = pd.read_sql('SELECT state as "State", type as "Energy Type", sum(installed) as "Installed Capacity", sum(actual) as "Actual Capacity" FROM isgs_data group by 1, 2', con=db_connection)

state_isgs_df = state_isgs_df.sort_values(by=[host_isgs_source], ascending=True)

state_isgs_bar_fig = px.bar(state_isgs_df, x=host_isgs_source,y='State', color='Energy Type', barmode='group')
state_isgs_bar_fig.update_layout(xaxis_title = host_isgs_source + ' (MU)', yaxis_title = 'State')

st.write(state_isgs_bar_fig)



sector_isgs_df = pd.read_sql('SELECT sector as "Sector", type as "Energy Type", sum(installed) as "Installed Capacity", sum(actual) as "Actual Capacity" FROM isgs_data group by 1, 2', con=db_connection)

sector_isgs_df = sector_isgs_df.sort_values(by=[host_isgs_source], ascending=True)

sector_isgs_bar_fig = px.bar(sector_isgs_df, x=host_isgs_source,y='Sector', color='Energy Type', barmode='group')
sector_isgs_bar_fig.update_layout(xaxis_title = host_isgs_source + ' (MU)', yaxis_title = 'Sector')

st.write(sector_isgs_bar_fig)
