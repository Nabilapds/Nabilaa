import numpy as np
import pandas as pd
import statsmodels.api as sm

data = {
    'Partisipan' : np.arange(1, 11),
    'p Makan' : [50, 40, 60, 55, 45, 65, 70, 75, 80, 90],
    'p Transportasi' : [20, 25, 30, 35, 40, 50, 55, 60, 65, 70],
    'BB' : [60, 55, 65, 70, 62, 75, 80, 85, 90, 95]}
df = pd.DataFrame(data)

x = df[['p Makan', 'p Transportasi']]
y = df['BB']

x = sm.add_constant(x)

model = sm.OLS(y, x)
results = model.fit()

print(results.summary())

import pandas as pd

df = pd.read_csv('dataset_fiskal_97_hipoFull.csv')
print(df.shape)

X = df[['DBH_PAJAK', 'DAU_Grant', 'DAK_Nonfisik']]
y = df['PAD']

from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score

model = LinearRegression()
model.fit(X, y)
