
#running pandas dan numpy
import pandas as pd
import numpy as np

#menampilkan array 1-dimensi
ds = pd.Series([2, 4, 6, 8, 10])
print(ds)

#P2
data = pd.Series(['a','b','c']) #!sS
np1 = np.array(['x','y','z'])
data_np = pd.Series(np1)
print(data)
print(data_np)

#P3 contoh operasi
ds1 = pd.Series([2, 4, 6, 8, 10])
ds2 = pd.Series([1, 3, 5, 7, 9])
dsa = ds1 + ds2  #operasi jumlah
dsb = ds1 - ds2
dsc = ds1 * ds2
dsd = ds1 / ds2
print(dsa)
print(dsb)
print(dsc)
print(dsd)

# P6 https://numpy.org/doc/1.16/reference/generated/ numpy.random.RandomState.html
import pandas as pd
import numpy as np

#generate angka random
num_state = np.random.RandomState(100)
num_series = pd.Series(num_state.normal(10, 4, 20))
print(num_series)
#print(num_state)

#P7.2 LOAD DATA dari link
df = pd.read_csv('https://raw.githubusercontent.com/Alam-A99/Pandas_Latih/main/penjualan.csv')
print(df)

#10.1
penjual = ['penjual no ' + str(i) for i in range(1, 11)]
print(penjual)

#10.2
df['urutan'] = penjual
print(df)

#P.12.1 Menampilkan baris dengan indeks berlabel 0
df.loc[0]
df.iloc[0]
df[:1]

#P12.4 Menampilkan semua baris pada kolom **nama** dan **apr**
df.loc[:, ['nama', 'apr']]
df.iloc[:, [0, 4]]
df[['nama', 'apr']]

#P12.5 Menampilkan semua baris pada kolom nama sampai feb
df.loc[:, 'nama':'feb']
df.iloc[:, :3]
df[['nama', 'jan', 'feb']]

#Menampilkan semua baris dan semua kolom
df.loc[:, :]
df.loc[:,]
df.iloc[:, :]

#P13.2 Memilih Memilih Teks
df[df['nama'].str.contains('Andi')]
df[df['nama'].str.contains('Jul')]

# Abaikan Huruf Besar/Kecil
df[df['nama'].str.contains('in')]
import re
df[df['nama'].str.contains('in', flags=re.IGNORECASE)]

