Nama: Aurellia Nabila Rahma Putri  
NIM: H1H024066  
Shift Awal: C  
Shift Akhir: D

---

# Pertanyaan Praktikum - Percobaan 1

## 1. Gambarkan diagram alur (flowchart) proses akuisisi data sensor DHT11 pada program di atas!

```mermaid
<img width="458" height="373" alt="flowchartmodul1" src="https://github.com/user-attachments/assets/503ee52e-bafb-4852-aa20-9e900b6ced81" />

```

## 2. Apa fungsi dari perintah `isnan()` pada program tersebut?

Fungsi `isnan()` digunakan untuk memeriksa apakah hasil pembacaan sensor menghasilkan nilai NaN (*Not a Number*) atau bukan angka yang valid. Kondisi tersebut dapat terjadi karena adanya gangguan pada koneksi kabel, komunikasi sensor, atau proses pembacaan yang belum selesai.

Dengan menggunakan fungsi ini, program dapat mendeteksi kegagalan pembacaan sebelum data ditampilkan atau digunakan untuk proses selanjutnya. Hal tersebut membantu mencegah sistem mengambil keputusan berdasarkan data yang tidak valid.

## 3. Jelaskan mengapa diperlukan jeda (delay) minimal sekitar 2 detik antar pembacaan sensor DHT11!

Sensor DHT11 memiliki keterbatasan dalam melakukan pengambilan data secara berulang, yaitu membutuhkan waktu sekitar 2 detik untuk menghasilkan pembacaan baru. Apabila proses pembacaan dilakukan terlalu cepat, sensor berpotensi memberikan data sebelumnya atau menghasilkan nilai NaN karena proses pengukuran belum selesai.

Oleh karena itu, penggunaan `delay(2000)` diperlukan agar sensor memiliki waktu yang cukup untuk menyelesaikan proses pembacaan sehingga data yang diperoleh lebih stabil dan dapat digunakan dengan baik.

## 4. Modifikasi program agar data suhu dan kelembaban dirata-ratakan dari 5 kali pembacaan sebelum ditampilkan, dan berikan penjelasan di setiap baris kode yang ditambahkan dalam bentuk README.md!

### Kode Program

```cpp
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11

DHT dht(DHTPIN, DHTTYPE);

// Menentukan jumlah pengambilan data sensor
const int JUMLAH_SAMPLING = 5;

void setup() {
  Serial.begin(115200);
  dht.begin();
}

void loop() {
  // Menyimpan total hasil pembacaan suhu dan kelembaban
  float totalSuhu = 0;
  float totalKelembaban = 0;

  // Menghitung jumlah pembacaan yang berhasil
  int jumlahValid = 0;

  // Melakukan pembacaan sensor sebanyak lima kali
  for (int i = 0; i < JUMLAH_SAMPLING; i++) {
    float kelembaban = dht.readHumidity();
    float suhu = dht.readTemperature();

    // Memeriksa apakah hasil pembacaan sensor valid
    if (isnan(kelembaban) || isnan(suhu)) {
      Serial.println("Gagal membaca data dari sensor DHT11! (pembacaan dilewati)");
    } else {
      // Menambahkan data valid ke total pembacaan
      totalSuhu += suhu;
      totalKelembaban += kelembaban;

      // Menambahkan jumlah data yang berhasil dibaca
      jumlahValid++;
    }

    // Memberikan jeda antar pembacaan sensor
    delay(2000);
  }

  // Menghitung rata-rata setelah lima kali pembacaan
  if (jumlahValid > 0) {
    float rataSuhu = totalSuhu / jumlahValid;
    float rataKelembaban = totalKelembaban / jumlahValid;

    // Menampilkan hasil rata-rata
    Serial.print("Rata-rata Suhu: ");
    Serial.print(rataSuhu);
    Serial.print(" °C, Rata-rata Kelembaban: ");
    Serial.print(rataKelembaban);
    Serial.println(" %");

  } else {
    // Menampilkan pesan jika seluruh pembacaan gagal
    Serial.println("Seluruh pembacaan gagal, rata-rata tidak dapat dihitung.");
  }
}
```

### Penjelasan Kode

1. `JUMLAH_SAMPLING = 5` menentukan jumlah pengambilan data sensor yang akan dilakukan.
2. `totalSuhu` digunakan untuk menyimpan akumulasi nilai suhu dari setiap pembacaan yang valid.
3. `totalKelembaban` digunakan untuk menyimpan akumulasi nilai kelembaban.
4. `jumlahValid` berfungsi menghitung banyaknya data yang berhasil diperoleh.
5. Perulangan `for` digunakan untuk menjalankan proses pembacaan sebanyak lima kali.
6. `readHumidity()` mengambil nilai kelembaban, sedangkan `readTemperature()` mengambil nilai suhu.
7. `isnan()` memeriksa apakah data yang diperoleh valid atau mengalami kegagalan.
8. `totalSuhu += suhu` dan `totalKelembaban += kelembaban` digunakan untuk menjumlahkan hasil pembacaan yang valid.
9. `jumlahValid++` menambah penghitung setiap kali pembacaan berhasil.
10. `delay(2000)` memberikan jeda selama dua detik antar pembacaan agar sesuai dengan karakteristik sensor DHT11.
11. `rataSuhu` dan `rataKelembaban` digunakan untuk menghitung nilai rata-rata berdasarkan total data valid.
12. Hasil perhitungan ditampilkan melalui Serial Monitor. Jika semua pembacaan gagal, program akan menampilkan pesan bahwa rata-rata tidak dapat dihitung.

---

# Pertanyaan Praktikum - Percobaan 2

## 1. Mengapa diperlukan nilai ambang batas (threshold) dalam sistem kendali aktuator berbasis sensor?

Threshold diperlukan sebagai nilai acuan bagi mikrokontroler untuk menentukan kapan aktuator harus diaktifkan atau dinonaktifkan. Data sensor yang terus berubah membutuhkan batas tertentu agar sistem dapat menentukan tindakan yang sesuai berdasarkan kondisi lingkungan.

Dengan adanya threshold, sistem dapat merespons perubahan suhu secara otomatis. Sebagai contoh, kipas dapat diaktifkan ketika suhu melebihi batas yang telah ditentukan tanpa harus dikendalikan secara manual.

## 2. Jelaskan apa yang akan terjadi apabila nilai `suhuThreshold` diturunkan menjadi sangat rendah, misalnya 20.0!

Jika nilai `suhuThreshold` diturunkan menjadi 20°C, aktuator kemungkinan akan menyala hampir sepanjang waktu karena suhu ruangan normal umumnya berada di atas nilai tersebut.

Akibatnya, aktuator akan terus bekerja meskipun kondisi lingkungan sebenarnya masih normal. Jika diterapkan pada perangkat seperti kipas atau pompa, hal ini dapat meningkatkan konsumsi energi listrik dan mempercepat keausan komponen.

## 3. Apa perbedaan antara kendali aktuator secara terus-menerus (kondisi tunggal) dengan kendali menggunakan histerisis (dua ambang batas)?

Kendali dengan satu threshold menggunakan satu nilai batas sebagai penentu kondisi aktuator. Ketika suhu melewati nilai tersebut, aktuator akan langsung berubah menjadi ON atau OFF. Namun, apabila suhu mengalami perubahan kecil di sekitar nilai threshold, aktuator dapat mengalami pergantian kondisi secara berulang dalam waktu singkat atau disebut *chattering*.

Sementara itu, kendali histerisis menggunakan dua nilai ambang batas, yaitu batas atas untuk mengaktifkan aktuator dan batas bawah untuk menonaktifkannya. Adanya jarak antara kedua batas tersebut membuat kondisi aktuator lebih stabil karena perubahan suhu kecil tidak langsung menyebabkan pergantian status.

## 4. Modifikasi program agar menggunakan dua ambang batas (histerisis), misalnya aktuator menyala pada suhu di atas 30°C dan baru mati pada suhu di bawah 28°C, dan berikan penjelasan di setiap baris kode nya dalam bentuk README.md!

### Kode Program

```cpp
#include <DHT.h>

#define DHTPIN 4
#define DHTTYPE DHT11
#define RELAYPIN 14

DHT dht(DHTPIN, DHTTYPE);

// Menentukan dua nilai ambang batas suhu
const float batasAtas = 30.0;
const float batasBawah = 28.0;

// Menyimpan kondisi aktuator saat ini
bool statusAktuator = false;

void setup() {
  Serial.begin(115200);
  dht.begin();

  // Mengatur pin relay sebagai output
  pinMode(RELAYPIN, OUTPUT);

  // Memastikan aktuator mati saat awal program
  digitalWrite(RELAYPIN, LOW);
  statusAktuator = false;
}

void loop() {
  // Membaca suhu dari sensor DHT11
  float suhu = dht.readTemperature();

  // Memeriksa apakah pembacaan suhu berhasil
  if (isnan(suhu)) {
    Serial.println("Gagal membaca suhu dari sensor DHT11!");

  } else {

    // Mengaktifkan aktuator jika suhu melebihi 30°C
    if (suhu > batasAtas) {
      statusAktuator = true;

    // Menonaktifkan aktuator jika suhu kurang dari 28°C
    } else if (suhu < batasBawah) {
      statusAktuator = false;
    }

    // Mengatur keluaran relay berdasarkan status aktuator
    digitalWrite(RELAYPIN, statusAktuator ? HIGH : LOW);

    // Menampilkan hasil pembacaan suhu
    Serial.print("Suhu: ");
    Serial.print(suhu);
    Serial.print(" °C, Aktuator: ");

    // Menampilkan kondisi aktuator
    Serial.println(statusAktuator ? "ON" : "OFF");
  }

  // Memberikan jeda dua detik sebelum pembacaan berikutnya
  delay(2000);
}
```

### Penjelasan Kode

1. `DHTPIN 4` menentukan GPIO 4 sebagai pin data sensor DHT11.
2. `DHTTYPE DHT11` menentukan jenis sensor yang digunakan.
3. `RELAYPIN 14` menentukan GPIO 14 sebagai pin kendali relay atau LED indikator sesuai rangkaian praktikum.
4. `batasAtas = 30.0` menentukan batas suhu untuk mengaktifkan aktuator.
5. `batasBawah = 28.0` menentukan batas suhu untuk menonaktifkan aktuator.
6. `statusAktuator` merupakan variabel Boolean untuk menyimpan kondisi aktuator, yaitu `true` untuk ON dan `false` untuk OFF.
7. `pinMode(RELAYPIN, OUTPUT)` mengatur pin relay sebagai keluaran.
8. `digitalWrite(RELAYPIN, LOW)` memastikan aktuator berada dalam kondisi mati saat program dimulai.
9. `readTemperature()` digunakan untuk mengambil data suhu dari sensor DHT11.
10. `isnan(suhu)` memeriksa apakah hasil pembacaan suhu valid.
11. Kondisi `if (suhu > batasAtas)` mengubah status aktuator menjadi ON ketika suhu melebihi 30°C.
12. Kondisi `else if (suhu < batasBawah)` mengubah status aktuator menjadi OFF ketika suhu berada di bawah 28°C.
13. Jika suhu berada di antara 28°C sampai 30°C, status aktuator tidak diubah sehingga tetap mengikuti kondisi sebelumnya.
14. `digitalWrite(RELAYPIN, statusAktuator ? HIGH : LOW)` mengirimkan sinyal keluaran sesuai kondisi aktuator.
15. `Serial.println()` menampilkan status aktuator pada Serial Monitor.
16. `delay(2000)` memberikan jeda sebelum sistem melakukan pembacaan berikutnya.

Dengan menggunakan metode histerisis, perubahan kondisi aktuator menjadi lebih stabil karena sistem memiliki dua batas yang berbeda untuk proses mengaktifkan dan menonaktifkan perangkat.

---

# Pertanyaan Analisis

## 1. Uraikan hasil tugas pada praktikum yang telah dilakukan pada setiap percobaan!

Pada Percobaan 1A, ESP32 berhasil membaca data suhu dan kelembaban menggunakan sensor DHT11. Hasil pembacaan ditampilkan melalui Serial Monitor setiap dua detik. Berdasarkan pengujian, seluruh data yang diperoleh berstatus valid. Ketika sensor disentuh atau didekati tangan, nilai suhu dan kelembaban mengalami peningkatan, sedangkan ketika sensor didekatkan ke AC, suhu mengalami penurunan.

Pada Percobaan 2A, ESP32 berhasil mengendalikan aktuator berdasarkan perbandingan nilai suhu dengan threshold sebesar 30°C. Berdasarkan hasil pengamatan, aktuator berada dalam kondisi OFF ketika suhu 28,60°C, berubah menjadi ON ketika suhu mencapai 30,30°C, dan kembali OFF ketika suhu turun menjadi 29,70°C. Hal ini menunjukkan bahwa sistem dapat mengatur kondisi aktuator secara otomatis berdasarkan hasil pembacaan sensor.

## 2. Bagaimana pengaruh akurasi dan waktu tanggap (response time) sensor terhadap kecepatan reaksi aktuator pada sistem IoT?

Akurasi sensor menentukan seberapa tepat hasil pembacaan menggambarkan kondisi lingkungan yang sebenarnya. Apabila sensor memiliki tingkat akurasi yang rendah, sistem berpotensi mengambil keputusan yang kurang sesuai, seperti mengaktifkan aktuator ketika suhu sebenarnya belum mencapai batas yang ditentukan.

Sementara itu, *response time* menunjukkan waktu yang diperlukan sensor untuk mendeteksi perubahan kondisi lingkungan dan menghasilkan data baru. Jika proses pembacaan membutuhkan waktu lebih lama, respons aktuator juga dapat mengalami keterlambatan. Oleh karena itu, akurasi yang baik dan waktu tanggap yang cepat diperlukan agar sistem dapat bekerja secara lebih tepat dan responsif.

## 3. Bagaimana cara kerja sistem dalam mengubah data sensor menjadi keputusan kendali aktuator (proses akuisisi hingga aktuasi)?

Proses dimulai ketika sensor DHT11 membaca kondisi lingkungan berupa suhu dan kelembaban. Hasil pengukuran kemudian dikirimkan ke ESP32 melalui jalur komunikasi digital dan dibaca menggunakan fungsi `dht.readTemperature()` serta `dht.readHumidity()` dari library DHT.

Data yang diterima selanjutnya diperiksa menggunakan fungsi `isnan()` untuk memastikan hasil pembacaan valid. Setelah itu, nilai suhu dibandingkan dengan threshold yang telah ditentukan melalui kondisi `if-else` pada program.

Berdasarkan hasil perbandingan tersebut, ESP32 mengirimkan sinyal digital HIGH atau LOW melalui pin GPIO yang terhubung dengan relay atau LED. Sinyal tersebut digunakan untuk mengaktifkan atau menonaktifkan aktuator sesuai kondisi suhu yang terdeteksi.

## 4. Bagaimana kombinasi antara akuisisi data sensor dan kendali aktuator dapat digunakan untuk membangun sistem IoT yang responsif terhadap perubahan kondisi lingkungan, misalnya pada sistem smart farming atau smart home?

Kombinasi antara akuisisi data sensor dan kendali aktuator memungkinkan sistem IoT untuk memantau kondisi lingkungan sekaligus memberikan respons secara otomatis berdasarkan informasi yang diperoleh.

Pada penerapan smart farming, sensor dapat digunakan untuk memantau suhu dan kelembaban lingkungan tanaman. Data tersebut kemudian diproses oleh mikrokontroler untuk mengendalikan perangkat seperti pompa irigasi atau kipas ventilasi sesuai kebutuhan.

Pada smart home, data sensor dapat digunakan untuk mengatur perangkat elektronik seperti AC, kipas, atau sistem peringatan secara otomatis berdasarkan kondisi ruangan. Dengan adanya koneksi internet, sistem juga dapat dikembangkan agar kondisi perangkat dapat dipantau dan dikendalikan dari jarak jauh.

Dengan demikian, penggabungan kedua proses tersebut dapat meningkatkan efisiensi penggunaan perangkat, mengurangi pengoperasian secara manual, dan membuat sistem lebih responsif terhadap perubahan lingkungan.
