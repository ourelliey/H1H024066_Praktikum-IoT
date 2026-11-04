**Nama:** Aurellia Nabila Rahma Putri  
**NIM:** H1H024066  
**Shift Awal:** C  
**Shift Akhir:** D  

---

# Pertanyaan Praktikum - Percobaan 5A

## 1. Gambarkan diagram alur (flowchart) proses perhitungan moving average pada fungsi hitungMovingAverage()!

<img width="901" height="1746" alt="flowchartmodul5lagi" src="https://github.com/user-attachments/assets/59e45b98-f436-42a0-bb93-099fa63504bf" />

## 2. Jelaskan fungsi dari operasi (indeks + 1) % N pada program tersebut!

Operasi ini membuat indeks buffer bergerak secara melingkar (*circular buffer*). Setiap data baru ditulis pada `buffer[indeks]`, lalu indeks bertambah satu. Operasi modulo `% N` mengembalikan indeks ke 0 ketika nilainya mencapai N, sehingga indeks selalu berada pada rentang 0 sampai N−1 dan tidak melewati batas array.

Dengan cara ini, setelah buffer penuh, data baru otomatis menimpa data yang paling lama sehingga buffer selalu berisi N pembacaan terakhir tanpa perlu menggeser seluruh isi array.

## 3. Apa dampaknya terhadap data hasil filter apabila nilai N diperbesar menjadi 20 atau diperkecil menjadi 2?

Jika N diperbesar menjadi 20, rata-rata dihitung dari lebih banyak data sehingga hasil filter lebih halus dan lebih tahan terhadap derau sesaat. Namun, responsnya menjadi lebih lambat karena perubahan suhu yang sebenarnya baru terlihat setelah beberapa pembacaan. Selain itu, memori buffer yang digunakan juga lebih besar.

Jika N diperkecil menjadi 2, hasil filter akan lebih cepat mengikuti perubahan suhu, tetapi kurang halus sehingga derau masih terlihat dan hasilnya lebih mendekati data mentah.

Jadi, ukuran N merupakan kompromi antara kehalusan data dan kecepatan respons sistem.

## 4. Modifikasi program agar ESP32 juga menghitung simpangan baku dari data pada buffer, dan berikan penjelasan di setiap baris kode yang ditambahkan!

Berikut modifikasi program untuk menghitung simpangan baku dari data pada buffer. Bagian yang ditambahkan diberi tanda `[BARU]`.

```cpp
// =====================================================
// Modul 5 - Percobaan 5A (Modifikasi)
// Moving Average (N = 5) + Min/Max + Simpangan Baku
// =====================================================

#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT22

DHT dht(DHTPIN, DHTTYPE);

const int N = 5;
float buffer[N];
int indeks = 0;
int jumlah = 0;

float suhuMin = 1000.0;
float suhuMax = -1000.0;

float hitungMovingAverage(float nilaiBaru) {
  buffer[indeks] = nilaiBaru;
  indeks = (indeks + 1) % N;

  if (jumlah < N) jumlah++;

  float total = 0;

  for (int i = 0; i < jumlah; i++) {
    total += buffer[i];
  }

  return total / jumlah;
}

// [BARU] Fungsi menghitung simpangan baku (sampel) dari isi buffer
float hitungSimpanganBaku(float rataRata) {
  if (jumlah < 2) return 0.0; 
  // [BARU] Simpangan baku tidak bisa dihitung dengan kurang dari 2 data.

  float jumlahKuadrat = 0;
  // [BARU] Penampung total kuadrat selisih.

  for (int i = 0; i < jumlah; i++) {
    // [BARU] Mengulang untuk setiap data yang sudah terisi di buffer.

    float selisih = buffer[i] - rataRata;
    // [BARU] Menghitung selisih data terhadap rata-rata.

    jumlahKuadrat += selisih * selisih;
    // [BARU] Menguadratkan selisih lalu menjumlahkannya.
  }

  return sqrt(jumlahKuadrat / (jumlah - 1));
  // [BARU] Menghitung akar dari total kuadrat dibagi (n-1).
}

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  float suhu = dht.readTemperature();

  if (isnan(suhu)) {
    Serial.println("Pembacaan gagal, data diabaikan");
  } else {
    float suhuFilter = hitungMovingAverage(suhu);

    float simpangan = hitungSimpanganBaku(suhuFilter);
    // [BARU] Menghitung simpangan baku menggunakan rata-rata hasil filter.

    if (suhu < suhuMin) suhuMin = suhu;
    if (suhu > suhuMax) suhuMax = suhu;

    Serial.print("Mentah: ");
    Serial.print(suhu);

    Serial.print(" | Filter: ");
    Serial.print(suhuFilter);

    Serial.print(" | StdDev: ");
    // [BARU] Menampilkan label simpangan baku.

    Serial.print(simpangan);
    // [BARU] Menampilkan nilai simpangan baku.

    Serial.print(" | Min: ");
    Serial.print(suhuMin);

    Serial.print(" | Max: ");
    Serial.println(suhuMax);
  }

  delay(2000);
}
```

**Penjelasan baris yang ditambahkan (bertanda `[BARU]`):**

- `hitungSimpanganBaku(float rataRata)`: Fungsi yang menerima rata-rata buffer dari hasil `hitungMovingAverage()` agar rata-rata tidak dihitung ulang.
- `if (jumlah < 2) return 0.0;`: Simpangan baku sampel membagi dengan jumlah data dikurangi satu. Oleh karena itu, jika data kurang dari dua, nilai dikembalikan menjadi 0 untuk menghindari pembagian dengan nol.
- `float jumlahKuadrat = 0;`: Variabel untuk menampung total kuadrat selisih setiap data.
- `for (int i = 0; i < jumlah; i++)`: Perulangan untuk memproses setiap data yang tersimpan di buffer.
- `float selisih = buffer[i] - rataRata;`: Menghitung selisih setiap data terhadap nilai rata-rata.
- `jumlahKuadrat += selisih * selisih;`: Menguadratkan selisih kemudian menjumlahkannya.
- `sqrt(jumlahKuadrat / (jumlah - 1))`: Menghitung akar dari varians sampel untuk memperoleh nilai simpangan baku.
- `hitungSimpanganBaku(suhuFilter)`: Memanggil fungsi simpangan baku menggunakan rata-rata hasil filter.
- `Serial.print(" | StdDev: ")` dan `Serial.print(simpangan)`: Menampilkan label dan nilai simpangan baku pada Serial Monitor.

---

# Pertanyaan Praktikum - Percobaan 5B

## 1. Jelaskan fungsi dari blok try-except pada fungsi on_message() dan apa yang terjadi apabila blok tersebut dihilangkan!

Blok `try-except` berfungsi untuk melindungi program dari data yang tidak valid. Pada bagian `try`, payload diubah menjadi teks menggunakan `decode()`, kemudian diurai menggunakan `json.loads()` dan nilai `"suhu"` diubah menjadi tipe data `float`.

Jika payload bukan JSON yang valid atau nilainya bukan angka, akan terjadi `ValueError`. Jika key `"suhu"` tidak ditemukan, akan terjadi `KeyError`. Kedua kesalahan tersebut ditangkap oleh blok `except`, kemudian program menampilkan pesan `"Data tidak valid, diabaikan"` dan menjalankan `return` sehingga data yang rusak tidak dimasukkan ke dalam list `data`.

Apabila blok `try-except` dihilangkan, kesalahan tersebut menjadi exception yang tidak tertangani pada callback sehingga program dapat berhenti secara mendadak. Akibatnya, proses akuisisi data dapat terhenti dan data yang telah terkumpul tidak tersimpan ke CSV karena tahap penyimpanan tidak pernah dijalankan.

## 2. Jelaskan arti nilai z-score dan mengapa batas |z| > 2 digunakan sebagai penentu anomali!

Z-score menunjukkan seberapa jauh suatu data menyimpang dari nilai rata-rata dalam satuan simpangan baku. Rumus perhitungannya adalah:

\[
z = \frac{x-\text{rata-rata}}{\text{simpangan baku}}
\]

Nilai z-score sebesar 0 berarti data berada tepat pada rata-rata. Nilai positif menunjukkan data berada di atas rata-rata, sedangkan nilai negatif menunjukkan data berada di bawah rata-rata.

Pada data yang berdistribusi mendekati normal, sekitar 95% data berada dalam rentang ±2 simpangan baku dari rata-rata. Oleh karena itu, data dengan nilai absolut z-score lebih dari 2 dianggap jarang terjadi dan patut dicurigai sebagai anomali.

Batas 2 merupakan batas praktis yang digunakan agar penyimpangan yang cukup jauh dapat terdeteksi tanpa terlalu banyak menandai data normal sebagai anomali. Batas ini juga dapat disesuaikan, misalnya menggunakan nilai 3 untuk deteksi yang lebih ketat.

## 3. Apa kelemahan metode z-score apabila data memiliki tren naik atau turun yang tajam?

Z-score menggunakan rata-rata dan simpangan baku dari seluruh data sehingga mengasumsikan bahwa data berfluktuasi di sekitar satu nilai tengah yang relatif tetap.

Jika data memiliki tren naik atau turun yang tajam, simpangan baku dapat menjadi besar karena ikut memperhitungkan perubahan tren. Akibatnya, data yang sebenarnya masih wajar sebagai bagian dari tren dapat ditandai sebagai anomali, sedangkan lonjakan yang benar-benar tidak normal justru dapat tidak terdeteksi.

Kelemahan lainnya adalah rata-rata dan simpangan baku dapat dipengaruhi oleh nilai anomali itu sendiri. Metode ini juga mengasumsikan distribusi data mendekati normal. Pada data yang hampir konstan seperti hasil percobaan ini, simpangan baku yang sangat kecil dapat menyebabkan perbedaan suhu sebesar 0,1 °C pun terdeteksi sebagai anomali.

Salah satu solusinya adalah menggunakan z-score pada jendela bergerak (*rolling z-score*) atau menghilangkan tren terlebih dahulu sebelum melakukan deteksi anomali.

## 4. Modifikasi program agar menggunakan metode moving average (jendela 5 data) pada data hasil CSV sebelum dihitung z-score-nya, kemudian bandingkan jumlah anomali yang terdeteksi!

Berikut modifikasi program Python untuk menerapkan moving average dengan jendela 5 data sebelum menghitung z-score. Program juga membandingkan jumlah anomali pada data mentah dengan data yang telah difilter.

Bagian yang ditambahkan diberi tanda `[BARU]`.

```python
# =====================================================
# Modul 5 - Percobaan 5B (Modifikasi)
# Moving average (jendela 5) pada data CSV sebelum z-score,
# lalu membandingkan jumlah anomali
# =====================================================

import pandas as pd
import matplotlib.pyplot as plt

JENDELA = 5  # [BARU] Ukuran jendela moving average
BATAS_Z = 2  # [BARU] Batas |z| untuk anomali

df = pd.read_csv("data_suhu.csv")
# [BARU] Membaca data hasil akuisisi dari file CSV.

def hitung_zscore(seri):
    # [BARU] Fungsi z-score agar dapat digunakan dua kali.

    rata2 = seri.mean()
    std = seri.std()

    if std == 0:
        # [BARU] Menghindari pembagian dengan nol.
        return pd.Series(0.0, index=seri.index)

    return (seri - rata2) / std


# --- Metode A: z-score pada data mentah ---

df["z_mentah"] = hitung_zscore(df["suhu"])
# [BARU] Menghitung z-score data mentah.

df["anomali_mentah"] = df["z_mentah"].abs() > BATAS_Z
# [BARU] Menentukan anomali pada data mentah.


# --- Metode B: moving average dulu, baru z-score ---

df["suhu_ma"] = df["suhu"].rolling(
    window=JENDELA,
    min_periods=1
).mean()
# [BARU] Menghitung rata-rata bergerak 5 data terakhir.

df["z_ma"] = hitung_zscore(df["suhu_ma"])
# [BARU] Menghitung z-score dari data hasil filter.

df["anomali_ma"] = df["z_ma"].abs() > BATAS_Z
# [BARU] Menentukan anomali setelah moving average.


# --- Perbandingan ---

print(f"Jumlah data : {len(df)}")
# [BARU] Menampilkan jumlah keseluruhan data.

print(f"Anomali data mentah : {df['anomali_mentah'].sum()}")
# [BARU] Menampilkan jumlah anomali data mentah.

print(f"Anomali setelah MA ({JENDELA}) : {df['anomali_ma'].sum()}")
# [BARU] Menampilkan jumlah anomali setelah moving average.

print(f"Std data mentah : {df['suhu'].std():.4f}")
# [BARU] Menampilkan simpangan baku data mentah.

print(f"Std data setelah MA : {df['suhu_ma'].std():.4f}")
# [BARU] Menampilkan simpangan baku setelah moving average.


df.to_csv("data_suhu_ma.csv", index=False)
# [BARU] Menyimpan hasil analisis ke file CSV baru.

print("Hasil tersimpan di data_suhu_ma.csv")


# --- Visualisasi perbandingan ---

fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
# [BARU] Membuat dua grafik secara vertikal.

ax[0].plot(df.index, df["suhu"], marker="o", label="Suhu mentah")
a1 = df[df["anomali_mentah"]]

ax[0].scatter(
    a1.index,
    a1["suhu"],
    color="red",
    s=100,
    label="Anomali",
    zorder=3
)

ax[0].axhline(
    df["suhu"].mean(),
    color="gray",
    linestyle="--",
    label="Rata-rata"
)

ax[0].set_title("Z-score pada data mentah")
ax[0].set_ylabel("Suhu (°C)")
ax[0].legend()


ax[1].plot(
    df.index,
    df["suhu_ma"],
    marker="o",
    color="green",
    label=f"Suhu MA ({JENDELA})"
)

a2 = df[df["anomali_ma"]]

ax[1].scatter(
    a2.index,
    a2["suhu_ma"],
    color="red",
    s=100,
    label="Anomali",
    zorder=3
)

ax[1].axhline(
    df["suhu_ma"].mean(),
    color="gray",
    linestyle="--",
    label="Rata-rata"
)

ax[1].set_title(
    f"Z-score setelah moving average (jendela {JENDELA})"
)

ax[1].set_xlabel("Urutan data")
ax[1].set_ylabel("Suhu (°C)")
ax[1].legend()

plt.tight_layout()
plt.savefig("grafik_perbandingan.png")
# [BARU] Menyimpan grafik perbandingan.

plt.show()
```

**Penjelasan baris yang ditambahkan (bertanda `[BARU]`):**

- `JENDELA = 5`: Menentukan ukuran jendela moving average sebanyak lima data.
- `BATAS_Z = 2`: Menentukan batas z-score untuk mendeteksi anomali.
- `pd.read_csv("data_suhu.csv")`: Membaca kembali data hasil akuisisi dari file CSV, bukan dari memori.
- `hitung_zscore(seri)`: Membuat fungsi perhitungan z-score agar dapat digunakan pada data mentah maupun data hasil moving average.
- `if std == 0`: Memeriksa apakah simpangan baku bernilai nol untuk menghindari pembagian dengan nol.
- `rolling(window=JENDELA, min_periods=1).mean()`: Menghitung rata-rata bergerak lima data terakhir. Penggunaan `min_periods=1` membuat data awal tetap dapat dihitung meskipun jumlah data belum mencapai lima.
- `df["z_mentah"]`: Menyimpan hasil z-score dari data suhu mentah.
- `df["anomali_mentah"]`: Menentukan data mentah yang memiliki nilai absolut z-score lebih dari batas 2.
- `df["suhu_ma"]`: Menyimpan hasil moving average ke kolom baru.
- `df["z_ma"]`: Menghitung z-score berdasarkan data yang sudah difilter.
- `df["anomali_ma"]`: Menentukan anomali setelah proses moving average.
- `print(...sum())`: Menampilkan dan membandingkan jumlah anomali dari data mentah dengan data hasil moving average.
- `df.to_csv("data_suhu_ma.csv", index=False)`: Menyimpan hasil perhitungan ke file CSV baru tanpa kolom indeks.
- `plt.subplots(2, 1, ...)`: Membuat dua grafik secara vertikal untuk membandingkan data mentah dan data hasil moving average.
- `plt.plot()` dan `plt.scatter()`: Menggambar garis suhu serta menandai titik-titik yang terdeteksi sebagai anomali.
- `plt.savefig("grafik_perbandingan.png")`: Menyimpan hasil grafik perbandingan ke dalam file gambar.

Berdasarkan hasil percobaan pada BCP, jumlah anomali pada data mentah sebanyak 3, sedangkan setelah diterapkan moving average dengan jendela 5 data, jumlah anomali turun menjadi 0.

---

# Pertanyaan Analisis

## 1. Uraikan hasil tugas pada praktikum yang telah dilakukan pada setiap percobaan!

Pada Percobaan 5A, ESP32 membaca suhu menggunakan mock function setiap 2 detik, kemudian menghitung moving average dari lima pembacaan terakhir serta mencatat suhu minimum dan maksimum. Serial Monitor menampilkan data suhu mentah, hasil filter, suhu minimum, dan suhu maksimum. Berdasarkan hasil pengamatan, suhu mentah mengalami penurunan dari 29,5 °C menjadi 29,3 °C, sedangkan hasil moving average mengikuti perubahan tersebut secara lebih halus. Pada tugas tambahan, program dikembangkan untuk menghitung simpangan baku dari data yang tersimpan di buffer.

Pada Percobaan 5B, program Python menerima data suhu dari broker MQTT, menyimpannya ke dalam file `data_suhu.csv` beserta waktu penerimaan, menghitung statistik, mendeteksi anomali menggunakan metode z-score, serta menghasilkan grafik dengan penanda anomali. Berdasarkan hasil pengamatan, terdapat 3 data anomali dari 20 data yang dicatat. Pada tugas tambahan, moving average dengan jendela 5 data diterapkan sebelum perhitungan z-score sehingga jumlah anomali turun dari 3 menjadi 0.

## 2. Bandingkan pengolahan data di sisi perangkat (Percobaan 5A) dengan pengolahan data di sisi komputer (Percobaan 5B) dari segi kecepatan, kompleksitas analisis, dan kebutuhan sumber daya!

Perbandingan kedua pendekatan pada percobaan ini dapat dilihat pada tabel berikut.

| Aspek | Sisi perangkat (5A, ESP32) | Sisi komputer (5B, Python) |
|---|---|---|
| Kecepatan | Hasil tersedia setiap pembacaan (2 detik) tanpa menunggu jaringan sehingga respons lebih cepat. | Bergantung pada pengiriman melalui WiFi dan broker MQTT. Analisis dilakukan setelah data terkumpul sehingga prosesnya lebih lambat. |
| Kompleksitas analisis | Relatif sederhana, meliputi moving average, min/max, dan simpangan baku. | Lebih kompleks karena mencakup statistik deskriptif, z-score, deteksi anomali, dan visualisasi menggunakan pustaka Python. |
| Sumber daya | Menggunakan memori dan kemampuan komputasi ESP32 yang terbatas. | Membutuhkan komputer, Python, pustaka pendukung, memori, serta penyimpanan untuk CSV. |
| Data yang dikirim | Data dapat diringkas atau difilter terlebih dahulu sebelum dikirim. | Menerima data mentah sehingga lalu lintas data yang dikirim lebih besar. |

Kedua pendekatan tersebut saling melengkapi. Pengolahan ringan di sisi perangkat digunakan untuk mendapatkan respons cepat dan menghemat pengiriman data, sedangkan analisis yang lebih kompleks dan penyimpanan data historis dapat dilakukan di sisi komputer atau cloud.

## 3. Bagaimana pengaruh pemilihan ukuran jendela moving average terhadap kualitas data dan kecepatan respons sistem kendali apabila data tersebut digunakan untuk mengendalikan aktuator?

Ukuran jendela moving average memengaruhi tingkat kehalusan data dan kecepatan respons sistem kendali. Jendela yang besar menghasilkan data lebih halus sehingga aktuator tidak mudah menyala dan mati akibat derau sesaat. Namun, hasil filter menjadi lebih lambat dalam mengikuti perubahan suhu yang sebenarnya sehingga aktuator dapat terlambat merespons ketika suhu mengalami kenaikan.

Sebaliknya, jendela yang kecil membuat sistem lebih cepat merespons perubahan suhu, tetapi data menjadi kurang halus dan lebih rentan terhadap derau. Hal tersebut dapat menyebabkan aktuator aktif secara tidak tepat akibat perubahan data yang bersifat sementara.

Oleh karena itu, ukuran jendela perlu disesuaikan dengan kebutuhan sistem. Untuk proses yang berubah secara perlahan seperti suhu ruangan, jendela lebih besar dapat digunakan. Sementara itu, untuk sistem yang membutuhkan respons cepat, jendela lebih kecil lebih sesuai.

## 4. Bagaimana hasil analisis dan deteksi anomali dapat dimanfaatkan untuk meningkatkan keandalan sistem IoT, misalnya pada sistem smart farming atau smart home?

Deteksi anomali membantu memisahkan data yang normal dari data yang tidak wajar sebelum digunakan untuk mengambil keputusan. Dengan demikian, sistem IoT dapat menghindari kesalahan pengambilan keputusan yang disebabkan oleh pembacaan sensor yang tidak normal.

Pada sistem smart farming, pembacaan kelembapan tanah yang tiba-tiba meningkat atau menurun secara tidak wajar dapat ditandai sebagai anomali. Hal tersebut mencegah pompa penyiram menyala hanya karena kesalahan pembacaan sensor. Jika anomali terjadi berulang kali, sistem juga dapat memberikan pemberitahuan bahwa sensor perlu diperiksa.

Pada sistem smart home, lonjakan suhu yang tidak wajar dapat dikenali sebagai gejala awal masalah, misalnya kebakaran atau kerusakan AC. Sistem kemudian dapat memberikan alarm atau notifikasi kepada pengguna.

Data yang telah difilter dan diverifikasi juga dapat membuat pengendalian aktuator menjadi lebih stabil, mengurangi alarm palsu, serta menyediakan data historis yang dapat digunakan untuk perawatan sensor secara prediktif. Dengan demikian, analisis dan deteksi anomali dapat meningkatkan keandalan sistem IoT.
