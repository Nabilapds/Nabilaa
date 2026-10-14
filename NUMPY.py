
import numpy as np

# Membuat array
nilai = np.array([85,55,40,90])
# Mengakses data pada array
print(nilai[3])

#T2.2
import numpy as np
a = np.array([[1,2,3,4],[5,66,7,8]])
print(a)

# #T2.4
# a = np.array([[1,2,3],[4,5,6]])
# b = a.reshape(3,2)
# print(a)
# b = a.reshape(3,2)
# print(b)
# c = a.reshape(2,4,3)
# print(c)

#T2.5 membuat array sebanyak 24, dari 0-23
a = np.arange(24)
b = a.reshape(2, 4, 3)
print(b)

#T3.3
a = np.arange(2,6,5)
print(a)

#T3.4
import numpy as np
a = np.arange(3, 10, 3)
print(a)

#T4.2 Membuat urutan bilangan bulat dari 0 hingga 10 dengan 4 elemen dan tipe data integer
urutan = np.linspace(0, 10, 4, dtype=int)
print("Urutan:", urutan)

#T9 Pembagian antar elemen matriks
import numpy as np
a = np.array([[2,4],[10,12]])
b = np.array([[1,2],[5,6]])
c = a/b
print(c)

#T10.1 numpy.reshape
import numpy as np
a = np.array([[1,2,3],[4,5,6]])
b = a.reshape(3,2)
print(b)

#Koding T10.19
import numpy as np
arr1 = np.array([1,2,3])
arr2 = np.array([4,5,6])
hasil = np.append(arr1,arr2)
print(hasil)

#Koding T10.20  Membuat array NumPy
arr1 = np.array([1, 2, 3, 4, 5])
# Menyisipkan beberapa nilai sekaligus pada indeks ke-2
arr1_baru = np.insert(arr1, 2, [9, 9, 9])
print("Arr1 asli:", arr1)
print("Arr1 baru:", arr1_baru)

#Koding T13.7b
import numpy as np
# Data berkelompok
interval = np.array([20, 30, 40, 50, 60, 70])  # Batas interval
frekuensi = np.array([5, 12, 18, 10, 7])  # Frekuensi
# Menghitung midpoint dari setiap interval
midpoints = (interval[:-1] + interval[1:]) / 2
# Menghitung mean dari data berkelompok
mean = np.sum(midpoints * frekuensi) / np.sum(frekuensi)
# Menghitung variansi dari data berkelompok
varians = np.sum(((midpoints - mean) ** 2) * frekuensi) / np.sum(frekuensi)
# Menghitung standar deviasi dari data berkelompok
std_deviation = np.sqrt(varians)
print("Mean:", mean)
print("Varians:", varians)
print("Standard Deviation:", std_deviation)

