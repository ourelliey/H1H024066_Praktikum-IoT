**Nama:** Aurellia Nabila Rahma Putri  
**NIM:** H1H024066  
**Shift Awal:** C  
**Shift Akhir:** D

---

# Pertanyaan Praktikum – Percobaan 4A

## 1. Gambarkan diagram alur (flowchart) proses penerimaan dan pemrosesan pesan pada fungsi callback!

<img width="380" height="692" alt="flowchart modul 4 IoT praktikum" src="https://github.com/user-attachments/assets/f5a66eb6-2e86-4437-a372-d52a9e11ecb0" />

## 2. Apa yang akan terjadi apabila pesan yang dipublikasikan bukan merupakan format JSON yang valid?

Apabila pesan yang diterima bukan merupakan format JSON yang valid, fungsi `deserializeJson()` akan menghasilkan kesalahan sehingga kondisi `if (error)` terpenuhi. Program kemudian menampilkan pesan kesalahan melalui Serial Monitor menggunakan `Serial.print()` dan `Serial.println(error.c_str())`.

Setelah itu, perintah `return` dijalankan sehingga proses callback dihentikan dan pesan tidak diproses lebih lanjut. Akibatnya, LED tidak menerima perintah baru dan tetap berada pada kondisi sebelumnya. Meskipun demikian, program ESP8266 tetap berjalan dan dapat menerima pesan MQTT berikutnya.

## 3. Mengapa fungsi `client.subscribe()` perlu dijalankan setelah ESP8266 berhasil terhubung ke broker MQTT?

Fungsi `client.subscribe()` digunakan untuk mendaftarkan perangkat agar dapat menerima pesan dari topic MQTT tertentu. Fungsi ini perlu dijalankan setelah koneksi ke broker berhasil dibuat karena perangkat harus terhubung terlebih dahulu agar dapat melakukan subscribe.

Pada program, fungsi subscribe diletakkan di dalam `hubungkanMQTT()`, tepat setelah `client.connect()` berhasil. Dengan demikian, ketika koneksi MQTT terputus dan perangkat melakukan koneksi ulang, ESP8266 akan mendaftarkan kembali topic yang ingin diterima.

Jika subscribe hanya dilakukan satu kali pada fungsi `setup()`, perangkat berisiko tidak lagi menerima pesan setelah koneksi MQTT terputus dan tersambung kembali.

## 4. Modifikasi program agar data JSON yang diterima juga memuat nilai intensitas yang digunakan untuk mengatur kecerahan LED menggunakan PWM!

Contoh pesan JSON yang dikirim melalui MQTT Explorer:

```json
{
  "perintah": "ON",
  "intensitas": 200
}
```

Pada modifikasi ini, nilai `intensitas` digunakan untuk menentukan tingkat kecerahan LED. Nilai intensitas dibatasi pada rentang 0–255, kemudian dikonversi menjadi nilai PWM ESP8266 pada rentang 0–1023.

Beberapa bagian kode yang ditambahkan atau diubah:

```cpp
// Membaca perintah dan intensitas dari JSON
const char* perintah = doc["perintah"] | "";
int intensitas = doc["intensitas"] | 255;

// Membatasi nilai intensitas antara 0 sampai 255
intensitas = constrain(intensitas, 0, 255);

if (String(perintah) == "ON") {
  // Mengubah nilai intensitas menjadi nilai PWM
  int duty = map(intensitas, 0, 255, 0, 1023);

  // Mengatur kecerahan LED menggunakan PWM
  analogWrite(ledPin, duty);

  Serial.print("Aktuator: ON, intensitas = ");
  Serial.println(intensitas);

} else if (String(perintah) == "OFF") {
  // Mematikan LED
  analogWrite(ledPin, 0);

  Serial.println("Aktuator: OFF");
}
```

Penjelasan kode tambahan:

- `doc["perintah"] | ""` digunakan untuk membaca perintah dari data JSON. Jika tidak tersedia, nilai default berupa String kosong.
- `doc["intensitas"] | 255` digunakan untuk membaca nilai intensitas dengan nilai default 255.
- `constrain(intensitas, 0, 255)` membatasi nilai intensitas agar tidak kurang dari 0 atau lebih dari 255.
- `map(intensitas, 0, 255, 0, 1023)` mengubah rentang nilai intensitas menjadi rentang PWM ESP8266.
- `analogWrite(ledPin, duty)` mengatur tingkat kecerahan LED berdasarkan nilai PWM.
- `analogWrite(ledPin, 0)` digunakan untuk mematikan LED ketika perintah yang diterima adalah OFF.

**Catatan:** Untuk pengaturan kecerahan, LED harus dipasang pada pin ESP8266 yang mendukung PWM. Pada modifikasi ini, pin LED dapat menggunakan D1 sebagai pengganti D6.

---

# Pertanyaan Praktikum – Percobaan 4B

## 1. Mengapa penggunaan `delay()` yang lama sebaiknya dihindari pada program yang menggabungkan proses publish dan subscribe secara bersamaan?

Penggunaan `delay()` yang terlalu lama sebaiknya dihindari karena bersifat blocking, yaitu menghentikan sementara proses program selama waktu yang ditentukan. Ketika ESP8266 sedang menjalankan `delay()`, fungsi `client.loop()` tidak dapat dipanggil sehingga perangkat tidak dapat segera memproses pesan MQTT yang masuk.

Pada komunikasi dua arah, ESP8266 harus dapat mengirim data sensor sekaligus menerima perintah dari broker MQTT. Jika menggunakan `delay()` terlalu lama, perintah untuk mengendalikan LED dapat mengalami keterlambatan. Selain itu, komunikasi dengan broker dapat terganggu karena proses pengiriman paket keep-alive tidak berjalan secara teratur.

Oleh karena itu, pendekatan non-blocking menggunakan `millis()` lebih sesuai untuk menjaga komunikasi publish dan subscribe tetap berjalan.

## 2. Jelaskan cara kerja mekanisme non-blocking menggunakan fungsi `millis()` pada program di atas!

Fungsi `millis()` digunakan untuk mengetahui waktu yang telah berlalu sejak ESP8266 dinyalakan tanpa menghentikan jalannya program. Pada program Percobaan 4B, variabel `waktuTerakhirPublish` digunakan untuk menyimpan waktu terakhir pengiriman data sensor, sedangkan `intervalPublish` menentukan jarak waktu pengiriman data, yaitu 5000 milidetik atau 5 detik.

Program memeriksa selisih antara waktu sekarang dengan waktu terakhir pengiriman menggunakan kondisi:

```cpp
if (millis() - waktuTerakhirPublish > intervalPublish)
```

Apabila selisih waktu sudah lebih dari 5000 milidetik, program akan memperbarui `waktuTerakhirPublish`, membaca suhu dari sensor DHT11, mengubah data menjadi format JSON, kemudian mengirimkannya ke broker MQTT menggunakan `client.publish()`.

Jika interval belum terpenuhi, program tidak perlu berhenti menunggu. Fungsi `client.loop()` tetap dapat dijalankan untuk memproses pesan masuk. Dengan mekanisme ini, proses publish dan subscribe dapat berjalan bersamaan tanpa saling menghambat.

## 3. Apa yang akan terjadi apabila fungsi `client.loop()` jarang dipanggil, misalnya hanya sekali setiap 10 detik?

Apabila fungsi `client.loop()` jarang dipanggil, pesan yang dikirim melalui broker MQTT tidak dapat langsung diproses oleh ESP8266. Hal ini menyebabkan perintah yang diterima mengalami keterlambatan sebelum diteruskan ke fungsi callback untuk mengendalikan LED.

Selain itu, fungsi `client.loop()` juga bertanggung jawab untuk menjaga komunikasi dengan broker MQTT, termasuk menangani paket keep-alive. Jika fungsi ini tidak dipanggil secara teratur, koneksi MQTT dapat terputus karena broker menganggap perangkat tidak aktif.

Ketika koneksi terputus, ESP8266 perlu melakukan koneksi ulang ke broker. Pesan yang dikirim ketika perangkat tidak terhubung juga berpotensi tidak diterima. Oleh karena itu, `client.loop()` sebaiknya dipanggil pada setiap iterasi fungsi `loop()` agar komunikasi MQTT tetap berjalan dengan baik.

## 4. Modifikasi program agar menambahkan satu topic perintah baru untuk mengendalikan aktuator kedua, misalnya buzzer!

Pada modifikasi ini ditambahkan topic baru bernama `buzzer` untuk mengendalikan aktuator kedua. Fungsi callback digunakan untuk membedakan pesan yang diterima berdasarkan topic MQTT. Jika pesan berasal dari topic perintah, program akan mengendalikan LED. Sementara itu, jika pesan berasal dari topic buzzer, program akan mengendalikan buzzer.

Contoh bagian kode yang ditambahkan atau diubah:

```cpp
// Menambahkan topic baru untuk buzzer
const char* topicBuzzer =
  "unsoed/tk245004/kelompokaurelula/buzzer";

// Menentukan pin buzzer
const int buzzerPin = D5;
```

Pada fungsi `callback()`:

```cpp
// Membaca perintah dari JSON
const char* perintah = doc["perintah"] | "";
bool aktif = (String(perintah) == "ON");

// Membedakan topic yang menerima pesan
if (strcmp(topic, topicPerintah) == 0) {
  digitalWrite(ledPin, aktif ? HIGH : LOW);
  Serial.print("LED -> ");

} else if (strcmp(topic, topicBuzzer) == 0) {
  digitalWrite(buzzerPin, aktif ? HIGH : LOW);
  Serial.print("Buzzer -> ");
}

Serial.println(perintah);
```

Pada fungsi `hubungkanMQTT()`:

```cpp
// Subscribe ke topic perintah LED
client.subscribe(topicPerintah);

// Subscribe ke topic perintah buzzer
client.subscribe(topicBuzzer);
```

Pada fungsi `setup()`:

```cpp
// Mengatur pin buzzer sebagai OUTPUT
pinMode(buzzerPin, OUTPUT);

// Memastikan buzzer dalam kondisi mati saat awal
digitalWrite(buzzerPin, LOW);
```

Penjelasan kode tambahan:

- `topicBuzzer` digunakan untuk menentukan topic MQTT khusus yang menerima perintah pengendalian buzzer.
- `buzzerPin` menentukan pin ESP8266 yang terhubung dengan buzzer.
- `strcmp(topic, topicPerintah) == 0` digunakan untuk memeriksa apakah pesan berasal dari topic pengendalian LED.
- `strcmp(topic, topicBuzzer) == 0` digunakan untuk memeriksa apakah pesan berasal dari topic pengendalian buzzer.
- `digitalWrite()` digunakan untuk mengaktifkan atau menonaktifkan aktuator berdasarkan perintah yang diterima.
- `client.subscribe(topicBuzzer)` membuat ESP8266 dapat menerima pesan dari topic buzzer.
- `pinMode(buzzerPin, OUTPUT)` mengatur pin buzzer sebagai keluaran.

Dengan penambahan tersebut, ESP8266 dapat mengendalikan dua aktuator, yaitu LED dan buzzer, melalui topic MQTT yang berbeda.

---

# Pertanyaan Analisis

## 1. Uraikan hasil tugas pada praktikum yang telah dilakukan pada setiap percobaan!

Pada Percobaan 4A, ESP8266 berhasil terhubung ke jaringan WiFi dan broker MQTT menggunakan `broker.hivemq.com` dengan port 1883. Perangkat kemudian melakukan subscribe pada topic `unsoed/tk245004/kelompokaurelula/perintah` untuk menerima perintah dari MQTT Explorer. Pesan JSON yang berisi perintah ON dan OFF berhasil diterima dan diproses oleh fungsi callback sehingga LED dapat menyala dan mati sesuai perintah yang diberikan.

Pada Percobaan 4B, ESP8266 berhasil menggabungkan proses publish dan subscribe secara bersamaan. Sensor DHT11 digunakan untuk membaca suhu, kemudian data dikirimkan dalam format JSON ke topic `unsoed/tk245004/kelompokaurelula/data` setiap 5 detik. Selain mengirimkan data sensor, ESP8266 juga dapat menerima perintah dari topic perintah untuk mengendalikan LED. Penggunaan fungsi `millis()` memungkinkan proses pengiriman data berlangsung secara non-blocking sehingga perangkat tetap dapat menerima pesan MQTT.

## 2. Bandingkan mekanisme komunikasi satu arah (publish saja, seperti pada Modul Praktikum 3) dengan komunikasi dua arah (publish dan subscribe) yang diimplementasikan pada modul ini!

Komunikasi satu arah pada Modul Praktikum 3 menggunakan mekanisme publish, yaitu ESP8266 hanya mengirimkan data sensor ke broker MQTT. Perangkat berfungsi sebagai publisher sehingga data dapat diterima dan dipantau melalui aplikasi MQTT Explorer, tetapi perangkat belum dapat menerima perintah untuk mengendalikan aktuator dari jarak jauh.

Sementara itu, komunikasi dua arah pada Modul Praktikum 4 menggunakan mekanisme publish dan subscribe. ESP8266 tidak hanya mengirimkan data sensor ke broker, tetapi juga menerima pesan dari topic tertentu untuk mengendalikan aktuator. Dengan demikian, komunikasi dapat berlangsung dari perangkat menuju aplikasi maupun dari aplikasi menuju perangkat.

Perbedaan lainnya terletak pada pengelolaan program. Komunikasi dua arah membutuhkan fungsi callback untuk memproses pesan masuk, `client.loop()` untuk menangani komunikasi MQTT, serta mekanisme non-blocking menggunakan `millis()` agar proses publish tidak menghambat penerimaan pesan.

## 3. Mengapa pendekatan non-blocking menggunakan `millis()` lebih sesuai dibandingkan pendekatan blocking menggunakan `delay()` pada sistem IoT yang memerlukan komunikasi dua arah secara real-time?

Pendekatan non-blocking menggunakan `millis()` lebih sesuai karena sistem IoT dengan komunikasi dua arah harus dapat mengirim data sekaligus menerima perintah tanpa mengalami keterlambatan. Penggunaan `delay()` dapat menghentikan sementara jalannya program sehingga fungsi `client.loop()` tidak dapat dijalankan selama waktu tunggu berlangsung.

Sebaliknya, `millis()` memungkinkan program memeriksa apakah waktu pengiriman data sudah terpenuhi tanpa menghentikan proses lainnya. Dengan begitu, ESP8266 tetap dapat memproses pesan MQTT yang masuk, menjaga koneksi dengan broker, dan mengirimkan data sensor secara berkala.

Oleh karena itu, pendekatan non-blocking membuat komunikasi menjadi lebih responsif, menjaga koneksi MQTT tetap berjalan, serta memungkinkan perangkat menjalankan beberapa proses secara bersamaan.

## 4. Berikan contoh penerapan komunikasi dan pertukaran data dua arah pada sistem IoT nyata dan jelaskan manfaatnya dibandingkan sistem yang hanya satu arah!

Salah satu contoh penerapan komunikasi dua arah pada sistem IoT adalah sistem smart home. Pada sistem ini, ESP8266 dapat digunakan untuk membaca suhu ruangan menggunakan sensor DHT11, kemudian mengirimkan data suhu ke broker MQTT agar dapat dipantau melalui aplikasi dashboard.

Selain mengirimkan data, pengguna juga dapat mengirimkan perintah melalui aplikasi untuk mengendalikan perangkat seperti kipas, lampu, atau buzzer. Sebagai contoh, ketika suhu ruangan terlalu tinggi, pengguna dapat mengirimkan perintah untuk menyalakan kipas melalui topic MQTT tertentu.

Manfaat komunikasi dua arah dibandingkan komunikasi satu arah adalah pengguna tidak hanya dapat memantau kondisi perangkat, tetapi juga dapat mengendalikannya dari jarak jauh. Sistem juga menjadi lebih fleksibel karena dapat menggabungkan proses pemantauan sensor dan pengendalian aktuator dalam satu jaringan komunikasi. Dengan demikian, komunikasi dua arah dapat meningkatkan efisiensi, kemudahan pemantauan, dan respons sistem IoT.
