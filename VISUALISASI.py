
%matplotlib inline
import matplotlib.pyplot as plt
import seaborn as sns
import numpy as np
import pandas as pd

# buat garfik seperti biasa

plt.style.use('fivethirtyeight')

x = np.linspace(0, 10, 100)
y = np.cos(x)

plt.plot(x, y)
plt.title("Contoh Grafik Dengan Style")
plt.xlabel("X")
plt.ylabel("Cos(X)")
plt.show()


#1.data
x = [2, 4, 6, 8]
y = [3, 5, 7, 9]

# membuat grafik
plt.plot(x, y)

#judul
plt.title("GRAFIK SIMPLE")
plt.xlabel("Nilai x")
plt.ylabel("Nilai y")

#3. menampilkan chart
plt.show()


#numpy.random
import numpy as np
from numpy.random import rand

x = rand(20)
y = rand(20)

plt.scatter(x, y)

plt.title("Scatter Plot")
plt.xlabel("X")
plt.ylabel("Y")

plt.show()


#Data
bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei']
penjualan = [150, 200, 180, 250, 125]

#6X4 inci adalah ukuran kecil yang tidak full screen
plt.figure(figsize=(6, 4))

plt.bar(bulan, penjualan)
plt.title("Penjualan Per Bulan")
plt.xlabel("Bulan")
plt.ylabel("Jumlah Penjualan")

plt.show()


#######
import seaborn as sns
import matplotlib.pyplot as plt

# Data
bulan = ['Jan', 'Feb', 'Mar', 'Apr', 'Mei', 'Juni', 'Juli']
penjualan = [150, 200, 180, 250, 125, 220, 130]

plt.figure(figsize=(8, 4)) # Diperlebar sedikit agar 7 bulan muat dengan rapi

# 1. Buat Grafik Batang
sns.barplot(x=bulan, y=penjualan, palette='muted')

# 2. Tambahkan Garis Tren (Menghubungkan puncak batang)
# range(len(bulan)) menghasilkan [0, 1, 2, 3, 4, 5, 6] sebagai posisi sumbu X
plt.plot(
    range(len(bulan)), # Posisi X (tengah setiap batang)
    penjualan,         # Posisi Y (nilai penjualan)
    color='blue',       # Warna garis
    marker='o',        # Tambahkan titik bulat di setiap persimpangan
    linestyle='-',     # Gaya garis (solid)
    linewidth=2,       # Ketebalan garis
    label='Garis Tren' # Nama untuk legenda
)

# 3. Kustomisasi Tampilan
plt.title("Penjualan per Bulan dengan Garis Tren", fontsize=12, fontweight='bold')
plt.xlabel('Bulan')
plt.ylabel('Jumlah Penjualan')
plt.legend() # Menampilkan kotak legenda

plt.tight_layout()
plt.show()


####
import plotly.express as px
import pandas as pd

# Data (Plotly lebih suka data dalam bentuk DataFrame)
df = pd.DataFrame({
    'Bulan': ['Jan', 'Feb', 'Mar', 'Apr', 'Mei'],
    'Penjualan': [150, 200, 180, 250, 300]
})

# A. Dictionary
# B. Tuple
# C. List

# Membuat grafik dasar
fig = px.bar(df, x='Bulan', y='Penjualan', title='Penjualan per Bulan')

fig.update_layout(width=700, height=400) # pixel

# Menampilkan grafik
fig.show()


####

# Data untuk grafik terakhir
df = pd.DataFrame({
    'nama': ['Andi', 'Budi', 'Citra', 'Dina', 'Eka'],
    'jan': [100, 150, 120, 200, 180],
    'feb': [120, 130, 140, 180, 160],
    'mar': [150, 170, 160, 190, 200],
    'apr': [130, 160, 180, 210, 170]
})

# 2. Tambahkan kolom total untuk memudahkan beberapa grafik
df['total'] = df[['jan', 'feb', 'mar', 'apr']].sum(axis=1)

# Atur style seaborn agar lebih rapi
sns.set_theme(style="whitegrid")

# Bar Chart
plt.figure(figsize=(8, 5)) # Ukuran kompak (lebar 8, tinggi 5 inci)

# Urutkan data dari total tertinggi
df_sorted = df.sort_values('total', ascending=False)

sns.barplot(data=df_sorted, x='nama', y='total', palette='viridis')

plt.title('Total Penjualan per Orang', fontsize=12)
plt.xlabel('Nama Karyawan')
plt.ylabel('Total Penjualan')
plt.xticks(rotation=45) # Miringkan label agar tidak tumpang tindih
plt.tight_layout()
plt.show()


import plotly.express as px
import pandas as pd

df = pd.DataFrame({
    'Bulan' : ('jan', 'Feb', 'Mar', 'Apr', 'Mei'),
    'Penjualan' : (150, 200, 180, 250, 300)

})

fig = px.bar(df, x='Bulan', y='Penjualan', title='Penjualan per Bulan')
fig.update_layout(width=700, height=400)
fig.show()

import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# 1. Muat dataset
df = pd.read_csv('https://raw.githubusercontent.com/Alam-A99/Pandas_Latih/10ebb3af000e930a44989075733f495d5c2f4be5/penjualan.csv')
df
# 2. Menambahkan kolom total untuk mempermudah beberapa grafik
df['total'] = df[['jan', 'feb', 'mar', 'apr']].sum(axis=1)
sns.set_theme(style="whitegrid")

# Bar Chart
plt.figure(figsize=(8, 5))  # Ukuran kompak (lebar 8, tinggi 5 inci)

# Urutkan data dari total tertinggi
df_sorted = df.sort_values("total", ascending=False)

sns.barplot(data=df_sorted, x="nama", y="total", palette="viridis")

plt.title("Total Penjualan per Orang", fontsize=12)
plt.xlabel("Nama Karyawan")
plt.ylabel("Total Penjualan")
plt.xticks(rotation=45)  # Miringkan label agar tidak tumpang tindih
plt.tight_layout()
plt.show()

#Pie Chart
plt.figure(figsize=(5, 5)) #Ukuran persegi agar pie chart tidak gepeng

#Hitung total penjualan per bulan
total_per_bulan = df[['jan', 'feb', 'mar', 'apr']].sum()

plt.pie(total_per_bulan, labels=total_per_bulan.index, autopct='%1.1f%%', startangle=140, colors = sns.color_palette('muted'))
plt.title('proporsi penjualan per bulan', fontsize=12)
plt.tight_layout()
plt.show()

# 3. Stack Plot (Stacked Bar Chart)
# Menampilkan komposisi penjualan per bulan untuk setiap orang secara bertumpuk

plt.figure(figsize=(8, 5))

# Set nama sebagai index, lalu plot sebagai stacked bar
df.set_index('nama')[['jan', 'feb', 'mar', 'apr']].plot(
    kind='bar',
    stacked=True,
    colormap='Pastel1',
    ax=plt.gca()
)

plt.title('Komposisi Penjualan Bulanan per Orang (Stacked)', fontsize=12)
plt.xlabel('Nama Karyawan')
plt.ylabel('Jumlah Penjualan')
plt.xticks(rotation=45)
plt.legend(title='Bulan')
plt.tight_layout()
plt.show()

# Histogran
plt.figure(figsize=(6, 4))
sns.histplot(df['total'], bins=5, kde=True, color='blue') # bins=5 membagi d
plt.title('Distribusi Frekuensi Total Penjualan', fontsize=12)
plt.xlabel('Range Total Penjualan')
plt.ylabel('Jumlah Karyawan (Frekuensi)')
plt.tight_layout()
plt.show()


# Scatter Plot
plt.figure(figsize=(6, 4))

sns.scatterplot(
    data=df,
    x='jan',
    y='feb',
    s=100,
    color='coral',
    hue='nama'
)

# Menambahkan label nama di dekat titik scatter
for i in range(df.shape[0]):
    plt.text(
        df['jan'].iloc[i] + 5,
        df['feb'].iloc[i],
        df['nama'].iloc[i],
        fontsize=9
    )

plt.title('Korelasi Penjualan: Januari vs Februari', fontsize=12)
plt.xlabel('Penjualan Januari')
plt.ylabel('Penjualan Februari')

plt.tight_layout()
plt.show()


