This project analyzes tipping behavior among NYC taxi passengers using trip record data provided by the Taxi & Limousine Commission (TLC). The primary goal is to identify trends in tip percentages over time and determine whether recent years show a statistically significant change in tipping behavior, potentially influenced by economic or social factors.

Research Question: Has tipping behavior changed significantly over the years 2020–2024?

Method: Filtered and sampled TLC Yellow Taxi trip data, engineered tip_pct, and used OLS regression and t-tests to evaluate year-over-year changes.

Key Insight: Tipping patterns show statistically significant shifts in 2023–2024 compared to 2020, controlling for distance, duration, and surcharges. However the effect size in 2023 and 2024 show nearly a 1-point decline. The R-squared value suggests other factors outside of the model play a larger role in tip variation over time. 

Language: Python
Libraries: pandas, pyarrow, statsmodels, scipy, openpyxl


Methodology
1. Data Cleaning
Filtered out invalid or extreme values (e.g., 0-distance trips, negative fares).

Focused on credit card payments to ensure tip amounts were available.

Converted timestamps, filled missing values, and sampled 30,000 observations per file.

2. Feature Engineering
tip_pct = tip amount ÷ total fare

Created trip duration (in hours) and extracted year.

3. Statistical Tests
T-tests compared 2020 vs. 2023 and 2020 vs. 2024.

OLS Regression modeled tip_pct as a function of:

Passenger count

Trip distance

Duration

Congestion and airport fees

Year fixed effects (2021–2024, with 2020 as baseline)

Key Results
Average tip_pct increased in some years, with notable differences in 2023 and 2024.

T-tests and regression confirmed statistically significant changes in tipping behavior.

Year dummies allowed inference on temporal trends while controlling for trip characteristics.

Limitations
Sample size capped at 30,000 per file for processing speed.

Only Yellow Taxi data with credit card tips were analyzed.

No geographic data (e.g., pickup/dropoff zones) used—future versions could include spatial controls.

How to Reproduce
Download and extract TLC Parquet data from the TLC Trip Record Data site.

Modify the directory variable in the script to point to your local file path.

Run the Python script to generate outputs and model summary.

License
This code is shared for educational and analytical purposes. Attribution appreciated.
