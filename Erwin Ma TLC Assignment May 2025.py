'''
NYC Taxi and Limousine Commission data assessment project May 2025
Data Analyst Position
Applicant: Erwin Ma
I used ChatGPT to look up Python and statsmodels syntax, troubleshoot errors.
All code and analytical decisions were written and executed independently.
'''

import os
import openpyxl as ox
import pandas as pd
import pyarrow as pa
import pyarrow.parquet as pq
import scipy.stats as stats
import statsmodels.formula.api as smf


#Load Parquet Files
directory = 'C:/Users/erwin/PycharmProjects/NYC Taxi & Limo Commission/Parquet Files'
data_frames = []

for file in os.listdir(directory):
    if file.endswith('.parquet'):
        file_path = os.path.join(directory, file)
        df = pq.read_table(file_path)
        df = df.to_pandas()

        #Subset the data
        df = df.reset_index()
        df = df.loc[df['trip_distance'] <= 50]#only within nyc area
        df = df.loc[df['trip_distance'] > 0]#distances greater than 0
        df = df.loc[df['tip_amount'] >= 0] #no zero or negative values
        df = df.loc[df['total_amount'] > 0] #no zero or negative values
        df = df.loc[df['payment_type'] == 1] #adjust for tips, credit card only
        df = df.rename(columns=str.lower) #correct a column name bug
        df = df[df['tpep_pickup_datetime'].notna()]
        df = df[df['tpep_dropoff_datetime'].notna()]
        df = df.sample(n=30000, random_state=42)
        data_frames.append(df)

trips = pd.concat(data_frames)


#Examine data
'''
print(trips.head())
print(trips.describe())
print(trips['trip_distance'].describe(include='all'))
print(trips['tpep_pickup_datetime'].describe(include='all'))
print(trips['passenger_count'].describe(include='all'))
print(trips['tolls_amount'].describe(include='all'))
print(trips['congestion_surcharge'].describe(include='all'))
'''

#Format data types
trips['tpep_pickup_datetime'] = pd.to_datetime(trips['tpep_pickup_datetime'], format='%m/%d/%Y')
trips['tpep_dropoff_datetime'] = pd.to_datetime(trips['tpep_dropoff_datetime'], format='%m/%d/%Y')
trips['year'] = trips['tpep_pickup_datetime'].dt.year.astype(int)
#print('dtype:',trips['year'].dtype)
#print(trips['year'].describe())
trips['airport_fee'] = trips['airport_fee'].fillna(0)
trips['congestion_surcharge'] = trips['congestion_surcharge'].fillna(0)


#Create variables
trips['tip_pct'] = trips['tip_amount']/trips['total_amount'] #trips as a percentage of fares is the independent variable
print('average tips:',trips['tip_pct'].describe(include='all'))

trips['trip_duration'] = (trips['tpep_dropoff_datetime'] - trips['tpep_pickup_datetime']).dt.total_seconds()/60/60 #create trip duration, hours
print(trips['trip_duration'].describe(include='all'))


#Data Model
mean_tips_per_year = trips.groupby('year')['tip_pct'].mean()
print('average tips% per year:',mean_tips_per_year)


#Create sample t-tests
group1 = trips.loc[trips['year'] == 2020]
group2 = trips.loc[trips['year'] == 2021]
group3 = trips.loc[trips['year'] == 2022]
group4 = trips.loc[trips['year'] == 2023]
group5 = trips.loc[trips['year'] == 2024]


#two sample t-tests, alpha = 0.05
t_statistic1, p_value1 = stats.ttest_ind(group1['tip_pct'], group4['tip_pct'])
t_statistic2, p_value2 = stats.ttest_ind(group1['tip_pct'], group5['tip_pct'])

print("2020 vs 2023 t-stat and pval:", t_statistic1, p_value1)
print("2020 vs 2024 t-stat and pval:", t_statistic2, p_value2)

#get dummies
trips = pd.get_dummies(data=trips, columns=['year'], prefix='y', drop_first=False)

#formula, 2020 is dropped for multicollinearity and is featured in the intercept
formula = 'tip_pct ~ passenger_count + trip_distance + trip_duration + congestion_surcharge + airport_fee + y_2021 + y_2022 + y_2023 + y_2024'

model = smf.ols(formula=formula, data=trips).fit()

print(model.summary())


#print to Excel
#trips.to_excel('C:/Users/erwin/PycharmProjects/NYC Taxi & Limo Commission/yellow_trip_data 2022-2025.xlsx')