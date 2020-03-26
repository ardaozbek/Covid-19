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
Comparison = ['Italy', 'Turkey', 'Spain']

# Download raw data
dfConfirmed = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_confirmed_global.csv')
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

# Initialize loop-bucket dataframes
dfTemp = pd.DataFrame()
dfCases = pd.DataFrame()

# Pick records with selected countries and confirmed cases more than a certain amount
for i in Comparison:
	dfTemp = dfConfirmed[(dfConfirmed['Country/Region'] == i) & (dfConfirmed['Confirmed'] > 95)].reset_index()
	dfTemp.rename(columns={'Confirmed':i}, inplace=True)
	dfTemp.drop(['Date', 'Country/Region'], axis=1, inplace=True)
	dfCases = pd.merge(dfCases, dfTemp, left_index=True, right_index=True, how='outer')

del dfConfirmed, dfTemp

dfDead = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_deaths_global.csv')
dfDead.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
dfDead = dfDead[dfDead['Country/Region'].isin(Comparison)]
dfDead = pd.melt(dfDead.groupby('Country/Region').sum().reset_index(), id_vars=['Country/Region'], var_name='Date', value_name='Dead')
dfDead.Date = pd.to_datetime(dfDead.Date, format='%m/%d/%y')
dfDead.set_index('Date', inplace=True)

# Initialize loop-bucket dataframes
dfTemp = pd.DataFrame()
dfDeath = pd.DataFrame()

# Pick records with selected countries and confirmed cases more than a certain amount
for i in Comparison:
	dfTemp = dfDead[(dfDead['Country/Region'] == i) & (dfDead['Dead'] > 0)].reset_index()
	dfTemp.rename(columns={'Dead':i}, inplace=True)
	dfTemp.drop(['Date', 'Country/Region'], axis=1, inplace=True)
	dfDeath = pd.merge(dfDeath, dfTemp, left_index=True, right_index=True, how='outer')

del dfDead, dfTemp

dfRecovered = pd.read_csv('https://raw.githubusercontent.com/CSSEGISandData/COVID-19/master/csse_covid_19_data/csse_covid_19_time_series/time_series_covid19_recovered_global.csv')
dfRecovered.drop(['Province/State', 'Lat', 'Long'], axis=1, inplace=True)
dfRecovered = dfRecovered[dfRecovered['Country/Region'].isin(Comparison)]
dfRecovered = pd.melt(dfRecovered.groupby('Country/Region').sum().reset_index(), id_vars=['Country/Region'], var_name='Date', value_name='Recovered')
dfRecovered.Date = pd.to_datetime(dfRecovered.Date, format='%m/%d/%Y')
dfRecovered.set_index('Date', inplace=True)

# Initialize loop-bucket dataframes
dfTemp = pd.DataFrame()
dfRecov = pd.DataFrame()

# Pick records with selected countries and confirmed cases more than a certain amount
for i in Comparison:
	dfTemp = dfRecovered[(dfRecovered['Country/Region'] == i) & (dfRecovered['Recovered'] > 0)].reset_index()
	dfTemp.rename(columns={'Recovered':i}, inplace=True)
	dfTemp.drop(['Date', 'Country/Region'], axis=1, inplace=True)
	dfRecov = pd.merge(dfRecov, dfTemp, left_index=True, right_index=True, how='outer')

del dfRecovered, dfTemp

plt.style.use('fivethirtyeight')

# # Incase an upper bound needed
UpperBound = sum(~dfCases.Turkey.isnull()) + 2
# UpperBound = 10

# Plot data
fig, (ax1, ax2) = plt.subplots(2)
fig.suptitle('Covid-19 Comparison')
for i in dfCases:
	ax1.plot(dfCases.loc[:UpperBound,[i]], label=i)
ax1.legend(loc='upper right')
# ax1.set_title('Cases')
ax1.set(xlabel='Days following 100th Case', ylabel='Cases')

for i in dfDeath:
	ax2.plot(dfDeath.loc[:UpperBound,[i]], label=i)
# ax2.set_title('Deaths')
ax2.set(xlabel='Days following 1st Death', ylabel='Deaths')

# for i in dfRecov:
# 	plt.plot(dfRecov.loc[:UpperBound,[i]], label=i)
# plt.legend(loc='upper right')
# plt.xlabel('Recoveries')
# plt.ylabel('Covid-19 Recoveries')

plt.tight_layout()
plt.show()

