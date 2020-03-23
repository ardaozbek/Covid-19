# -*- coding: utf-8 -*-
"""
Created on Sun Mar 22 21:26:04 2020

@author: Arda ÖZBEK

This code compares selected countries by days from the first instance of 
the SARS-CoV-2 case, death or recovery

"""

import pandas as pd
import matplotlib.pyplot as plt

# Countries to compare
Comparison = ['Italy', 'Turkey']

# Download raw data
dfConfirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Confirmed.csv')
# Drop unused columns
dfConfirmed.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
# Drop rows not in comparison countries
dfConfirmed = dfConfirmed[dfConfirmed['Country/Region'].isin(Comparison)]
# Sum and pivot selected rows
dfConfirmed = pd.melt(dfConfirmed.groupby('Country/Region').sum().reset_index(), id_vars=['Country/Region'], var_name='Date', value_name='Confirmed')
# Convert melted dates to datetime
dfConfirmed.Date = pd.to_datetime(dfConfirmed.Date, format='%m/%d/%y')
# Set date index
dfConfirmed.set_index('Date', inplace=True)
# 
dfConfirmedA = dfConfirmed[(dfConfirmed['Country/Region'] == Comparison[1]) & (dfConfirmed['Confirmed'] > 0)].reset_index()
dfConfirmedA.rename(columns={'Confirmed':'Confirmed'+Comparison[1]}, inplace=True)
dfConfirmedB = dfConfirmed[(dfConfirmed['Country/Region'] == Comparison[0]) & (dfConfirmed['Confirmed'] > 0)].reset_index()
dfConfirmedB.rename(columns={'Confirmed':'Confirmed'+Comparison[0]}, inplace=True)
dfConfirmed = pd.merge(dfConfirmedA, dfConfirmedB, left_index=True, right_index=True, how='outer')
dfConfirmed.drop(['Date_x', 'Date_y','Country/Region_x','Country/Region_y'], axis=1, inplace=True)

dfDead = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Deaths.csv')
dfDead.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
dfDead = dfDead[dfDead['Country/Region'].isin(Comparison)]
dfDead = pd.melt(dfDead.groupby('Country/Region').sum().reset_index(), id_vars=['Country/Region'], var_name='Date', value_name='Dead')
dfDead.Date = pd.to_datetime(dfDead.Date, format='%m/%d/%y')
dfDead.set_index('Date', inplace=True)
dfDeadA = dfDead[(dfDead['Country/Region'] == Comparison[1]) & (dfDead['Dead'] > 0)].reset_index()
dfDeadA.rename(columns={'Dead':'Dead'+Comparison[1]}, inplace=True)
dfDeadB = dfDead[(dfDead['Country/Region'] == Comparison[0]) & (dfDead['Dead'] > 0)].reset_index()
dfDeadB.rename(columns={'Dead':'Dead'+Comparison[0]}, inplace=True)
dfDead = pd.merge(dfDeadA, dfDeadB, left_index=True, right_index=True, how='outer')
dfDead.drop(['Date_x', 'Date_y','Country/Region_x','Country/Region_y'], axis=1, inplace=True)

# dfRecovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_19-covid-Recovered.csv')
# dfRecovered.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
# dfRecovered = dfRecovered[dfRecovered['Country/Region'].isin(Comparison)]
# dfRecovered = pd.melt(dfRecovered.groupby('Country/Region').sum().reset_index(), id_vars=['Country/Region'], var_name='Date', value_name='Recovered')
# dfRecovered.Date = pd.to_datetime(dfRecovered.Date, format='%m/%d/%y')
# dfRecovered.set_index('Date', inplace=True)
# dfRecoveredA = dfRecovered[(dfRecovered['Country/Region'] == Comparison[1]) & (dfRecovered['Confirmed'] > 0)].reset_index()
# dfRecoveredA.rename(columns={'Recovered':'Recovered'+Comparison[1]}, inplace=True)
# dfRecoveredB = dfRecovered[(dfRecovered['Country/Region'] == Comparison[0]) & (dfRecovered['Confirmed'] > 0)].reset_index()
# dfRecoveredB.rename(columns={'Recovered':'Recovered'+Comparison[0]}, inplace=True)
# dfRecovered = pd.merge(dfRecoveredA, dfRecoveredB, left_index=True, right_index=True, how='outer')
# dfRecovered.drop(['Date_x', 'Date_y','Country/Region_x','Country/Region_y'], axis=1, inplace=True)

dfCovid = pd.merge(dfConfirmed, dfDead, left_index=True, right_index=True, how='outer')

plt.style.use('fivethirtyeight')
plt.subplot(2, 1, 1)
plt.plot(dfCovid.loc[0:12,['ConfirmedTurkey', 'ConfirmedItaly']])
plt.xlabel('Days following the first case')
plt.legend(loc='upper right', labels=['Turkey', 'Italy'])
plt.ylabel('Confirmed Cases')
plt.title('Covid-19 Italy - Turkey Comparison')

plt.subplot(2, 1, 2)
plt.plot(dfCovid.loc[0:12,['DeadTurkey', 'DeadItaly']])
plt.xlabel('Days following the first mortality')
plt.legend(loc='upper right', labels=['Turkey', 'Italy'])
plt.ylabel('Covid-19 Deaths')
# plt.title('Covid-19 Italy - Turkey Comparison')

plt.tight_layout()
plt.show()
