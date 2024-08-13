import pandas as pd
from lifelines import KaplanMeierFitter
import numpy as np
import matplotlib
import matplotlib.pyplot as plt
import math

data_url = "https://raw.githubusercontent.com/karinabik1/Survival-Curve-on-Scientific-Papers/main/780%20papers%20for%20survival%20-%20Simplified.csv"
data = pd.read_csv(data_url, encoding='latin-1')

# empty cells filled with 0 to resolve errors
data['RT'] = data['RT'].fillna(0)
data['EoC'] = data['EoC'].fillna(0)
data['CR'] = data['CR'].fillna(0)

# Convert dates to datetime format if they are not already
data['Email to Editor'] = pd.to_datetime(data['Email to Editor'])
data['Correction or Retraction Date'] = pd.to_datetime(data['Correction or Retraction Date'])

# Calculate survival time from 'Email to Editor' to 'Correction or Retraction Date'
data['Survival Time'] = (data['Correction or Retraction Date'] - data['Email to Editor']).dt.days

# some helpful metrics:
#print(data['Survival Time'])
t = 0
n = 0
u = 0
for x in data['Survival Time']:
  t += 1
  if x < 0:
    n += 1
  if math.isnan(x):
    u += 1
print('Total', t)
print('Negative', n)
print('NaN', u)

# Create a binary survival indicator
# If all of 'CR', 'EoC', or 'RT' columns are 0, set 'Survival' to False (not corrected or retracted)
# Otherwise, set 'Survival' to True (corrected or retracted)
data['Survival'] = data.apply(lambda row: False if row['CR'] == 0 and row['EoC'] == 0 and row['RT'] == 0 else True, axis=1)

# more helpful metrics:
tt = 0
s = 0
for x in data['Survival']:
  tt += 1
  if  not x:
    s += 1
print('Total', tt)
print('Survived', s)
print('Not Survived', t - s)

# Fill NaNs in 'Survival Time' with the maximum non-NaN value
data['Survival Time'] = data['Survival Time'].fillna(np.nanmax(data['Survival Time']))

# Initialize KaplanMeierFitter for all data
kmf = KaplanMeierFitter()

# Fit the data to Kaplan-Meier estimator
kmf.fit(data['Survival Time'], event_observed=data['Survival'])

# Plot the survival curve
plt.figure(figsize=(10, 6))
#kmf.plot()
kmf.plot_survival_function()

plt.title('Survival Curve for Scientific Papers')
plt.xlabel('Time (days)')
plt.ylabel('Survival')
plt.xlim(0)  # Set x-axis limit to start from 0
plt.ylim(0,1)  # Set y-axis limit to start from 0
plt.grid()
plt.show()


