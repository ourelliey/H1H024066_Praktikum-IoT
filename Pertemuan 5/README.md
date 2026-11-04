**Nama:** Aurellia Nabila Rahma Putri  
**NIM:** H1H024066  
**Shift Awal:** C  
**Shift Akhir:** C

---

# Pertanyaan Praktikum - Percobaan 5A

## 1. Gambarkan diagram alur (flowchart) proses perhitungan moving average pada fungsi hitungMovingAverage()!

<img width="901" height="1746" alt="flowchartmodul5lagi" src="https://github.com/user-attachments/assets/27f52f3e-5bdf-4986-b28c-4dda11603b00" />

## 2. Jelaskan fungsi dari operasi (indeks + 1) % N pada program tersebut!

Operasi ini mengimplementasikan logika *circular buffer*. Fungsi utamanya adalah memastikan indeks penulisan data selalu berputar dalam rentang 0 hingga N−1. Ketika indeks mencapai nilai N, operasi modulo akan mengembalikannya ke 0 sehingga data baru akan menimpa data paling lama secara otomatis tanpa perlu menggeser elemen array.

Dengan demikian, buffer selalu menyimpan sejumlah data terbaru sesuai kapasitas yang telah ditentukan.

## 3. Apa dampaknya terhadap data hasil filter apabila nilai N diperbesar menjadi 20 atau diperkecil menjadi 2?

- **N = 20 (Membesar):** Grafik menjadi lebih halus (*smooth*) dan noise berkurang secara signifikan. Namun, hasil filter menghasilkan *lag* atau keterlambatan respons yang lebih tinggi terhadap perubahan data sensor karena perhitungan menggunakan lebih banyak data sebelumnya.
- **N = 2 (Mengecil):** Respons sistem menjadi lebih cepat terhadap perubahan data, tetapi pemfilteran noise menjadi lebih sedikit sehingga grafik masih terlihat fluktuatif.

Jadi, ukuran N memengaruhi keseimbangan antara kehalusan data dan kecepatan respons sistem. Semakin besar ukuran jendela, semakin halus hasil filter tetapi semakin lambat responsnya. Sebaliknya, semakin kecil ukuran jendela, semakin cepat responsnya tetapi noise lebih terlihat.

## 4. Modifikasi program agar ESP32 juga menghitung simpangan baku dari data pada buffer, dan berikan penjelasan di setiap baris kode yang ditambahkan!

Berikut modifikasi program Percobaan 5A untuk menghitung simpangan baku dari data yang tersimpan pada buffer. Program tetap menggunakan mock function sebagai pengganti sensor DHT22 seperti pada program BCP.

```cpp
#include <Arduino.h>
#include <math.h>

// Pengaturan Moving Average
const int N = 5;
float buffer[N];
int indeks = 0;
int jumlah = 0;

// Statistik suhu
float suhuMin = 1000.0;
float suhuMax = -1000.0;

// Pencatatan waktu dan nomor pengukuran
unsigned long waktuMulai;
unsigned long nomorData = 0;

// Mock function pengganti sensor DHT22
float bacaSuhuMock() {
    static unsigned long jumlahBaca = 0;
    jumlahBaca++;

    float suhuDasar = 28.0 + 2.0 * sin(jumlahBaca * 0.08);

    float noise = random(-5, 6) * 0.1;

    float suhu = suhuDasar + noise;

    if (jumlahBaca % 25 == 0) {
        suhu += 8.0;
    }

    return suhu;
}

// Menghitung Moving Average
float hitungMovingAverage(float nilaiBaru) {
    buffer[indeks] = nilaiBaru;
    indeks = (indeks + 1) % N;

    if (jumlah < N) {
        jumlah++;
    }

    float total = 0.0;

    for (int i = 0; i < jumlah; i++) {
        total += buffer[i];
    }

    return total / jumlah;
}

// [BARU] Fungsi menghitung simpangan baku dari isi buffer
float hitungSimpanganBaku(float rataRata) {
    if (jumlah < 2) return 0.0;
    // [BARU] Memastikan jumlah data minimal 2 agar tidak terjadi pembagian nol.

    float jumlahKuadrat = 0;
    // [BARU] Variabel untuk menampung jumlah kuadrat selisih.

    for (int i = 0; i < jumlah; i++) {
        // [BARU] Mengulangi perhitungan untuk setiap data dalam buffer.

        float selisih = buffer[i] - rataRata;
        // [BARU] Menghitung selisih data terhadap rata-rata.

        jumlahKuadrat += selisih * selisih;
        // [BARU] Menguadratkan selisih kemudian menjumlahkannya.
    }

    return sqrt(jumlahKuadrat / (jumlah - 1));
    // [BARU] Menghitung akar dari varians sampel.
}

void setup() {
    Serial.begin(115200);
    randomSeed(micros());

    waktuMulai = millis();

    Serial.println();
    Serial.println("TABEL 5.1. PENGOLAHAN DATA SUHU PADA ESP32");
    Serial.println("No | Waktu(s) | Mentah(C) | Moving Average(C) | Min(C) | Max(C) | StdDev");
}

void loop() {
    float suhu = bacaSuhuMock();

    float suhuFilter = hitungMovingAverage(suhu);

    // [BARU] Menghitung simpangan baku dari data buffer.
    float simpangan = hitungSimpanganBaku(suhuFilter);

    if (suhu < suhuMin) {
        suhuMin = suhu;
    }

    if (suhu > suhuMax) {
        suhuMax = suhu;
    }

    unsigned long waktu = (millis() - waktuMulai) / 1000;

    nomorData++;

    Serial.print(nomorData);
    Serial.print(" | ");
    Serial.print(waktu);
    Serial.print(" | ");
    Serial.print(suhu, 2);
    Serial.print(" | ");
    Serial.print(suhuFilter, 2);
    Serial.print(" | ");
    Serial.print(suhuMin, 2);
    Serial.print(" | ");
    Serial.print(suhuMax, 2);
    Serial.print(" | ");

    // [BARU] Menampilkan nilai simpangan baku.
    Serial.println(simpangan, 4);

    delay(2000);
}
```

**Penjelasan bagian yang ditambahkan (bertanda `[BARU]`):**

- `hitungSimpanganBaku(float rataRata)`: Membuat fungsi untuk menghitung simpangan baku dari data yang tersimpan di dalam buffer.
- `if (jumlah < 2) return 0.0;`: Memeriksa jumlah data. Jika data kurang dari dua, fungsi mengembalikan nilai 0 agar tidak terjadi pembagian dengan nol.
- `float jumlahKuadrat = 0;`: Menyediakan variabel untuk menyimpan total kuadrat selisih setiap data.
- `for (int i = 0; i < jumlah; i++)`: Melakukan perulangan untuk menghitung setiap data yang terdapat di dalam buffer.
- `float selisih = buffer[i] - rataRata;`: Menghitung selisih setiap nilai suhu terhadap rata-rata.
- `jumlahKuadrat += selisih * selisih;`: Menguadratkan setiap selisih kemudian menjumlahkannya.
- `sqrt(jumlahKuadrat / (jumlah - 1))`: Menghitung akar dari varians sampel untuk memperoleh nilai simpangan baku.
- `float simpangan = hitungSimpanganBaku(suhuFilter);`: Memanggil fungsi simpangan baku pada setiap pembacaan data.
- `Serial.println(simpangan, 4);`: Menampilkan hasil simpangan baku pada Serial Monitor dengan empat angka di belakang koma.

---

# Pertanyaan Praktikum - Percobaan 5B

## 1. Jelaskan fungsi dari blok try-except pada fungsi on_message() dan apa yang terjadi apabila blok tersebut dihilangkan!

Blok `try-except` berfungsi untuk menangani kesalahan (*exception*) saat program memproses pesan MQTT yang diterima. Pada bagian `try`, payload diubah menjadi teks menggunakan `decode()`, kemudian diproses menggunakan `json.loads()` untuk mendapatkan nilai suhu dalam format angka.

Jika payload memiliki format JSON yang tidak valid, nilai suhu tidak dapat dikonversi menjadi angka, atau key `"suhu"` tidak ditemukan, program akan menghasilkan kesalahan seperti `ValueError`, `KeyError`, `TypeError`, atau `JSONDecodeError`.

Kesalahan tersebut ditangkap oleh blok `except`, kemudian program menampilkan pesan `"Pesan tidak valid, diabaikan."` dan menjalankan `return` agar data yang tidak valid tidak diproses lebih lanjut.

Jika blok `try-except` dihilangkan, kesalahan pembacaan satu payload saja dapat menyebabkan script Python berhenti (*crash*). Akibatnya, proses penerimaan data MQTT akan terhenti dan pengumpulan data tidak dapat diselesaikan.

## 2. Jelaskan arti nilai z-score dan mengapa batas |z| > 2 digunakan sebagai penentu anomali!

**Z-score** merupakan nilai statistik yang digunakan untuk mengukur seberapa jauh suatu titik data menyimpang dari nilai rata-rata (*mean*) dalam satuan simpangan baku (*standard deviation*).

Rumus perhitungan z-score adalah:

\[
z = \frac{x-\bar{x}}{s}
\]

Keterangan:
- \(x\) = nilai data yang dianalisis.
- \(\bar{x}\) = nilai rata-rata.
- \(s\) = simpangan baku.

Nilai z-score positif menunjukkan bahwa data berada di atas rata-rata, sedangkan nilai negatif menunjukkan bahwa data berada di bawah rata-rata. Nilai z-score sebesar 0 berarti data berada tepat pada rata-rata.

Batas \(|z| > 2\) digunakan karena berdasarkan konsep distribusi normal (*Empirical Rule*), sekitar 95,4% data normal berada pada rentang −2 hingga +2 simpangan baku. Oleh karena itu, data yang memiliki nilai absolut z-score lebih dari 2 dianggap memiliki penyimpangan yang cukup besar dan berpotensi menjadi anomali (*outlier*).

## 3. Apa kelemahan metode z-score apabila data memiliki tren naik atau turun yang tajam?

Metode z-score menggunakan nilai rata-rata (*global mean*) dan simpangan baku (*standard deviation*) dari keseluruhan data. Jika data memiliki tren naik atau turun yang tajam, nilai rata-rata keseluruhan tidak selalu dapat mewakili kondisi data pada setiap waktu.

Akibatnya, data yang sebenarnya masih normal sebagai bagian dari tren dapat terdeteksi sebagai anomali karena memiliki jarak yang cukup jauh dari rata-rata keseluruhan. Kondisi ini dapat menghasilkan *false positive*, yaitu data normal yang salah dikategorikan sebagai anomali.

Selain itu, perubahan tren dapat memengaruhi nilai simpangan baku sehingga deteksi anomali menjadi kurang akurat. Oleh karena itu, metode z-score lebih sesuai digunakan pada data yang memiliki pola relatif stabil. Untuk data yang memiliki tren, dapat digunakan pendekatan seperti *rolling z-score* atau penghilangan tren sebelum proses deteksi anomali.

## 4. Modifikasi program agar menggunakan metode moving average (jendela 5 data) pada data hasil CSV sebelum dihitung z-score-nya, kemudian bandingkan jumlah anomali yang terdeteksi!

Modifikasi dilakukan pada program Python dengan membaca kembali data dari `data_suhu.csv`, kemudian menghitung moving average menggunakan jendela 5 data sebelum melakukan perhitungan z-score. Hasilnya dibandingkan dengan deteksi anomali pada data suhu mentah.

```python
import pandas as pd
import matplotlib.pyplot as plt

JENDELA = 5  # [BARU] Menentukan ukuran jendela moving average.
BATAS_Z = 2  # [BARU] Menentukan batas z-score untuk anomali.

df = pd.read_csv("data_suhu.csv")
# [BARU] Membaca data hasil akuisisi dari file CSV.

def hitung_zscore(seri):
    # [BARU] Fungsi untuk menghitung z-score dari suatu kolom data.

    rata2 = seri.mean()
    # [BARU] Menghitung nilai rata-rata.

    std = seri.std()
    # [BARU] Menghitung simpangan baku.

    if std == 0:
        # [BARU] Menghindari pembagian dengan nol.
        return pd.Series(0.0, index=seri.index)

    return (seri - rata2) / std
    # [BARU] Menghasilkan nilai z-score.


# METODE A: Z-score pada data mentah

df["z_mentah"] = hitung_zscore(df["suhu"])
# [BARU] Menghitung z-score berdasarkan data suhu mentah.

df["anomali_mentah"] = df["z_mentah"].abs() > BATAS_Z
# [BARU] Menentukan data mentah yang termasuk anomali.


# METODE B: Moving Average kemudian Z-score

df["suhu_ma"] = df["suhu"].rolling(
    window=JENDELA,
    min_periods=1
).mean()
# [BARU] Menghitung moving average dari lima data terakhir.

df["z_ma"] = hitung_zscore(df["suhu_ma"])
# [BARU] Menghitung z-score berdasarkan hasil moving average.

df["anomali_ma"] = df["z_ma"].abs() > BATAS_Z
# [BARU] Menentukan anomali setelah proses moving average.


# PERBANDINGAN HASIL

print(f"Jumlah data: {len(df)}")
# [BARU] Menampilkan jumlah data yang dianalisis.

print(f"Anomali data mentah: {df['anomali_mentah'].sum()}")
# [BARU] Menampilkan jumlah anomali pada data mentah.

print(f"Anomali setelah MA ({JENDELA}): {df['anomali_ma'].sum()}")
# [BARU] Menampilkan jumlah anomali setelah moving average.

print(f"Std data mentah: {df['suhu'].std():.4f}")
# [BARU] Menampilkan simpangan baku data mentah.

print(f"Std data setelah MA: {df['suhu_ma'].std():.4f}")
# [BARU] Menampilkan simpangan baku setelah moving average.


df.to_csv("data_suhu_ma.csv", index=False)
# [BARU] Menyimpan hasil analisis ke file CSV baru.

print("Hasil tersimpan di data_suhu_ma.csv")


# VISUALISASI PERBANDINGAN

fig, ax = plt.subplots(2, 1, figsize=(10, 7), sharex=True)
# [BARU] Membuat dua grafik untuk membandingkan kedua metode.

# Grafik data mentah
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


# Grafik setelah moving average
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
# [BARU] Menyimpan grafik hasil perbandingan.

plt.show()
```

**Penjelasan bagian yang ditambahkan (bertanda `[BARU]`):**

- `JENDELA = 5`: Menentukan jumlah data yang digunakan dalam perhitungan moving average.
- `BATAS_Z = 2`: Menentukan batas nilai z-score untuk mendeteksi anomali.
- `pd.read_csv("data_suhu.csv")`: Membaca data hasil akuisisi yang sebelumnya sudah disimpan ke dalam file CSV.
- `hitung_zscore(seri)`: Membuat fungsi untuk menghitung z-score agar dapat digunakan pada data mentah maupun data hasil moving average.
- `seri.mean()` dan `seri.std()`: Menghitung rata-rata dan simpangan baku dari data.
- `if std == 0`: Memeriksa apakah simpangan baku bernilai nol agar tidak terjadi pembagian dengan nol.
- `rolling(window=JENDELA, min_periods=1).mean()`: Menghitung moving average menggunakan lima data terakhir. Parameter `min_periods=1` memungkinkan perhitungan dilakukan meskipun jumlah data belum mencapai lima.
- `df["z_mentah"]`: Menyimpan nilai z-score dari data suhu mentah.
- `df["anomali_mentah"]`: Menandai data mentah yang memiliki nilai absolut z-score lebih dari 2.
- `df["suhu_ma"]`: Menyimpan hasil moving average ke dalam kolom baru.
- `df["z_ma"]`: Menghitung z-score berdasarkan data yang telah difilter.
- `df["anomali_ma"]`: Menentukan anomali setelah proses moving average.
- `print(...sum())`: Menampilkan dan membandingkan jumlah anomali dari kedua metode.
- `df.to_csv("data_suhu_ma.csv", index=False)`: Menyimpan hasil perhitungan ke file CSV baru.
- `plt.subplots(2, 1, ...)`: Membuat dua grafik untuk membandingkan hasil deteksi anomali pada data mentah dan data hasil moving average.
- `plt.plot()` dan `plt.scatter()`: Menggambar grafik suhu dan memberikan penanda pada titik yang terdeteksi sebagai anomali.
- `plt.savefig("grafik_perbandingan.png")`: Menyimpan grafik perbandingan ke dalam file gambar.

---

# Pertanyaan Analisis

## 1. Uraikan hasil tugas pada praktikum yang telah dilakukan pada setiap percobaan!

Pada Percobaan 5A, ESP32 berhasil melakukan pengolahan data suhu menggunakan mock function sebagai pengganti sensor DHT22. Data suhu dihasilkan setiap 2 detik, kemudian diproses menggunakan metode moving average dengan lima pembacaan terakhir. Program juga menghitung suhu minimum dan maksimum serta menampilkan hasil pengolahan melalui Serial Monitor. Berdasarkan hasil pengamatan, suhu mentah mengalami perubahan dari 29,03 °C hingga 30,14 °C pada sepuluh data yang dicatat. Hasil moving average membuat perubahan suhu terlihat lebih halus dibandingkan data mentah.

Pada Percobaan 5B, ESP32 berhasil mengirimkan data suhu ke broker MQTT menggunakan topic `unsoed/tk245004/kelompok1/data`. Program Python pada komputer menerima 20 data suhu melalui mekanisme subscribe, kemudian melakukan analisis menggunakan metode z-score. Data yang diterima disimpan dalam file `data_suhu.csv`, sedangkan hasil analisis ditampilkan dalam bentuk tabel dan grafik. Berdasarkan hasil pengamatan, terdapat satu data anomali, yaitu suhu 36,56 °C dengan nilai z-score 2,7353. Data lainnya dikategorikan normal.

## 2. Bandingkan pengolahan data di sisi perangkat (Percobaan 5A) dengan pengolahan data di sisi komputer (Percobaan 5B) dari segi kecepatan, kompleksitas analisis, dan kebutuhan sumber daya!

Perbandingan pengolahan data pada kedua percobaan dapat dilihat pada tabel berikut.

| Aspek | Sisi perangkat (5A, ESP32) | Sisi komputer (5B, Python) |
|---|---|---|
| Kecepatan | Pengolahan dilakukan langsung pada ESP32 setiap 2 detik sehingga memiliki respons cepat dan tidak perlu menunggu proses pengiriman data ke komputer. | Bergantung pada komunikasi WiFi dan broker MQTT. Data harus diterima terlebih dahulu sebelum dilakukan analisis. |
| Kompleksitas analisis | Relatif sederhana, meliputi moving average, pencatatan suhu minimum, dan maksimum. | Lebih kompleks karena melibatkan akuisisi MQTT, pengolahan data menggunakan Pandas, perhitungan z-score, penyimpanan CSV, dan visualisasi menggunakan Matplotlib. |
| Sumber daya | Menggunakan memori dan kemampuan komputasi ESP32 yang terbatas. | Membutuhkan komputer dengan Python serta pustaka pendukung, tetapi memiliki kapasitas memori dan komputasi yang lebih besar. |
| Penyimpanan data | Pengolahan dilakukan langsung pada perangkat dan hanya menyimpan data yang dibutuhkan dalam buffer. | Data dapat disimpan dalam file CSV sehingga dapat digunakan kembali untuk analisis dan dokumentasi. |

Kedua pendekatan tersebut memiliki kelebihan masing-masing. Pengolahan di sisi perangkat lebih sesuai untuk proses yang membutuhkan respons cepat, sedangkan pengolahan di sisi komputer lebih sesuai untuk analisis data yang kompleks dan penyimpanan data historis.

## 3. Bagaimana pengaruh pemilihan ukuran jendela moving average terhadap kualitas data dan kecepatan respons sistem kendali apabila data tersebut digunakan untuk mengendalikan aktuator?

Ukuran jendela moving average memengaruhi kehalusan data dan kecepatan respons sistem kendali. Jendela yang besar dapat mengurangi noise sehingga data menjadi lebih stabil. Hal ini membuat aktuator tidak mudah mengalami perubahan kondisi secara berulang akibat fluktuasi data sensor.

Namun, penggunaan jendela yang besar menyebabkan keterlambatan respons karena nilai rata-rata dihitung berdasarkan lebih banyak data sebelumnya. Akibatnya, aktuator dapat terlambat merespons perubahan kondisi lingkungan.

Sebaliknya, jendela yang kecil memberikan respons lebih cepat terhadap perubahan data sensor, tetapi noise lebih mudah memengaruhi hasil pengukuran. Kondisi tersebut dapat menyebabkan aktuator sering menyala dan mati secara tidak stabil atau mengalami *chattering*.

Oleh karena itu, pemilihan ukuran jendela harus disesuaikan dengan kebutuhan sistem. Jendela besar lebih sesuai untuk kondisi yang membutuhkan kestabilan, sedangkan jendela kecil lebih sesuai untuk sistem yang membutuhkan respons cepat.

## 4. Bagaimana hasil analisis dan deteksi anomali dapat dimanfaatkan untuk meningkatkan keandalan sistem IoT, misalnya pada sistem smart farming atau smart home?

Analisis dan deteksi anomali dapat digunakan untuk mengetahui adanya kondisi tidak normal pada sistem IoT sebelum menimbulkan kerusakan atau gangguan yang lebih besar.

Pada sistem **smart farming**, deteksi anomali dapat digunakan untuk mengetahui kegagalan pompa irigasi, penyumbatan pipa, atau kerusakan sensor kelembapan tanah. Dengan demikian, sistem dapat memberikan peringatan kepada pengguna agar gangguan dapat segera diperiksa sebelum memengaruhi kondisi tanaman.

Pada sistem **smart home**, analisis data dapat membantu mendeteksi penggunaan energi listrik yang tidak wajar akibat korsleting, kebocoran gas, atau aktivitas mencurigakan ketika penghuni sedang tidak berada di rumah. Jika ditemukan kondisi yang tidak normal, sistem dapat memberikan notifikasi atau mengaktifkan alarm.

Dengan adanya analisis dan deteksi anomali, sistem IoT dapat melakukan pemantauan secara lebih efektif, mengurangi risiko kesalahan pembacaan sensor, dan membantu pengguna melakukan tindakan lebih cepat ketika terjadi gangguan.
