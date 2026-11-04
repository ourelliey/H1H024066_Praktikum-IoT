**Nama:** Aurellia Nabila Rahma Putri  
**NIM:** H1H024066  
**Shift Awal:** C
**Shift Akhir:** D

---

# E. Pertanyaan Praktikum

## Percobaan 3A: Komunikasi Data Menggunakan HTTP

### 1. Gambarkan diagram alur (flowchart) proses pengiriman data melalui HTTP POST pada program di atas!

<img width="2070" height="3493" alt="flowchartmodul3" src="https://github.com/user-attachments/assets/09f7b8d4-7a00-4123-812c-fb253bd9a0cc" />

### 2. Apa fungsi dari perintah `http.addHeader("Content-Type", "application/json")` pada program tersebut?

Perintah `http.addHeader("Content-Type", "application/json")` digunakan untuk menambahkan informasi header pada HTTP request yang dikirimkan oleh ESP8266. Header tersebut memberi tahu server bahwa isi data pada bagian body request menggunakan format JSON.

Dengan adanya informasi ini, server dapat mengenali dan memproses data yang diterima sesuai dengan formatnya. Jika header tidak disertakan atau tidak sesuai, server berpotensi mengalami kesalahan ketika membaca dan menginterpretasikan isi data yang dikirimkan.

### 3. Jelaskan arti dari kode response HTTP 200 dan sebutkan salah satu contoh kode response HTTP lain beserta artinya!

HTTP response code `200 OK` menunjukkan bahwa request yang dikirimkan oleh client berhasil diterima dan diproses oleh server. Pada percobaan ini, kode tersebut menunjukkan bahwa pengiriman data JSON dari ESP8266 ke server `httpbin.org` berhasil dilakukan.

Contoh kode response HTTP lainnya adalah `404 Not Found`. Kode tersebut menunjukkan bahwa server tidak menemukan alamat atau resource yang diminta oleh client. Kode ini dapat muncul ketika URL atau endpoint yang dituju tidak tersedia pada server.

### 4. Modifikasi program agar ESP32 dapat mengirimkan data tambahan berupa waktu (dalam milidetik sejak dinyalakan menggunakan millis()) ke dalam JSON yang dikirim, dan berikan penjelasan di setiap baris kode yang ditambahkan!

Modifikasi dilakukan dengan menambahkan variabel waktu menggunakan fungsi `millis()`. Nilai waktu tersebut kemudian dimasukkan ke dalam objek JSON dengan nama key `waktu_ms`, sehingga data yang dikirimkan memiliki informasi suhu, kelembaban, dan waktu sejak perangkat dinyalakan.

**Kode program hasil modifikasi:**

```cpp
#include <ESP8266WiFi.h>
#include <ESP8266HTTPClient.h>
#include <WiFiClientSecure.h>
#include <ArduinoJson.h>

const char* ssid = "NAMA_WIFI";
const char* password = "PASSWORD_WIFI";
const char* serverUrl = "https://httpbin.org/post";

void setup() {
  Serial.begin(115200);
  WiFi.begin(ssid, password);

  Serial.print("Menghubungkan ke WiFi");

  while (WiFi.status() != WL_CONNECTED) {
    delay(500);
    Serial.print(".");
  }

  Serial.println("\nWiFi berhasil terhubung!");
}

void loop() {
  if (WiFi.status() == WL_CONNECTED) {
    WiFiClientSecure client;
    client.setInsecure();

    HTTPClient http;
    http.begin(client, serverUrl);
    http.addHeader("Content-Type", "application/json");

    JsonDocument doc;

    doc["suhu"] = 28.5;
    doc["kelembaban"] = 65.0;

    // Menambahkan waktu sejak ESP8266 dinyalakan
    unsigned long waktu = millis();

    // Memasukkan nilai waktu ke dalam objek JSON
    doc["waktu_ms"] = waktu;

    String requestBody;
    serializeJson(doc, requestBody);

    Serial.print("Mengirim data: ");
    Serial.println(requestBody);

    int httpResponseCode = http.POST(requestBody);

    if (httpResponseCode > 0) {
      Serial.print("Kode Response HTTP: ");
      Serial.println(httpResponseCode);

      Serial.println("Isi Response: ");
      Serial.println(http.getString());
    } else {
      Serial.print("Pengiriman gagal, error: ");
      Serial.println(http.errorToString(httpResponseCode));
    }

    http.end();
  }

  delay(10000);
}
```

**Penjelasan bagian kode yang ditambahkan:**

1. `unsigned long waktu = millis();`

   Digunakan untuk mengambil waktu yang telah berlalu sejak ESP8266 mulai dijalankan. Fungsi `millis()` menghasilkan nilai waktu dalam satuan milidetik.

2. `doc["waktu_ms"] = waktu;`

   Digunakan untuk menambahkan nilai waktu ke dalam objek JSON dengan nama key `waktu_ms`. Dengan demikian, informasi waktu ikut dikirim bersama data suhu dan kelembaban.

3. `serializeJson(doc, requestBody);`

   Bagian ini tetap digunakan untuk mengubah seluruh isi objek JSON menjadi String agar dapat dikirimkan melalui HTTP POST. Karena objek JSON sudah ditambahkan dengan `waktu_ms`, data waktu juga akan ikut dimasukkan ke dalam request body.

**Contoh format JSON setelah modifikasi:**

```json
{
  "suhu": 28.5,
  "kelembaban": 65.0,
  "waktu_ms": 10000
}
```

Nilai `waktu_ms` pada contoh tersebut menunjukkan bahwa perangkat telah berjalan selama 10.000 milidetik atau 10 detik. Nilainya akan terus bertambah selama perangkat beroperasi.

*Catatan: Kode ini menggunakan sintaks ArduinoJson versi 7 (`JsonDocument`). Jika menggunakan ArduinoJson versi 6, deklarasi dokumen dapat diganti dengan `StaticJsonDocument<200> doc;`.*

---

## Percobaan 3B: Komunikasi MQTT

### 1. Apa fungsi dari topic pada protokol MQTT, dan mengapa topic yang digunakan perlu dibuat unik?

Topic pada MQTT berfungsi sebagai alamat atau jalur untuk mengelompokkan pesan yang dikirimkan oleh publisher. Broker menggunakan topic tersebut untuk menentukan pesan harus diteruskan kepada subscriber yang berlangganan pada topic yang sesuai.

Topic perlu dibuat unik, terutama ketika menggunakan broker publik seperti `broker.hivemq.com`, karena broker tersebut digunakan oleh banyak perangkat dari berbagai pengguna. Apabila beberapa perangkat menggunakan topic yang sama, pesan yang dikirimkan dapat tercampur dengan data milik perangkat lain. Oleh karena itu, penggunaan topic yang memiliki identitas khusus dapat membantu menjaga agar pertukaran data lebih terorganisasi dan mudah dikenali.

Pada praktikum ini, topic yang digunakan adalah:

```text
unsoed/tk246466/kelompok7/sensor
```

### 2. Jelaskan fungsi dari perintah `client.loop()` yang dipanggil pada setiap iterasi `loop()`!

Perintah `client.loop()` berfungsi untuk menjaga komunikasi antara ESP8266 dengan broker MQTT agar tetap berjalan. Fungsi ini membantu memproses paket komunikasi yang masuk, menangani pesan yang diterima dari broker, serta menjalankan callback apabila terdapat pesan masuk.

Selain itu, pemanggilan `client.loop()` secara berulang diperlukan agar koneksi MQTT tetap terpelihara selama program berjalan. Jika fungsi ini tidak dipanggil secara rutin, perangkat dapat mengalami gangguan dalam memproses komunikasi sehingga koneksi MQTT berpotensi terputus.

### 3. Apa yang akan terjadi apabila koneksi ke broker MQTT terputus di tengah program berjalan?

Ketika koneksi ESP8266 dengan broker MQTT terputus, proses pengiriman pesan menggunakan `client.publish()` tidak dapat berjalan sebagaimana mestinya. Pesan yang dikirim ketika perangkat sedang tidak terhubung dapat gagal terkirim ke broker.

Pada program praktikum, kondisi koneksi diperiksa menggunakan perintah `client.connected()`. Apabila hasil pemeriksaan menunjukkan bahwa koneksi terputus, program akan memanggil fungsi `hubungkanMQTT()` untuk mencoba menghubungkan perangkat kembali ke broker.

Proses tersebut dilakukan berulang sampai koneksi berhasil dibangun kembali. Dengan mekanisme ini, ESP8266 dapat melanjutkan proses pengiriman data setelah koneksi MQTT kembali tersedia.

---

# Pertanyaan Analisis

### 1. Uraikan hasil tugas pada praktikum yang telah dilakukan pada setiap percobaan!

**Percobaan 3A – Komunikasi Data Menggunakan HTTP**

Pada percobaan ini, ESP8266 berhasil terhubung ke jaringan WiFi dan mengirimkan data dalam format JSON menuju server `https://httpbin.org/post` menggunakan metode HTTP POST. Data yang dikirimkan berisi informasi suhu sebesar 28.5°C dan kelembaban sebesar 65%.

Berdasarkan hasil pengamatan, pengiriman dilakukan sebanyak 10 kali dengan interval 10 detik. Setiap pengiriman memperoleh HTTP response code `200`, sehingga seluruh proses pengiriman data dinyatakan berhasil. Server juga mengembalikan response body yang berisi data JSON yang telah dikirimkan.

**Percobaan 3B – Komunikasi Data Menggunakan MQTT**

Pada percobaan ini, ESP8266 berhasil terhubung ke broker MQTT publik `broker.hivemq.com` melalui port 1883. Perangkat kemudian mengirimkan data suhu dan kelembaban dalam format JSON menggunakan mekanisme publish-subscribe.

Data dikirimkan ke topic `unsoed/tk246466/kelompok7/sensor` dengan interval 5 detik. Berdasarkan hasil pengamatan pada Serial Monitor dan MQTT Explorer, data yang dipublikasikan berhasil diterima oleh subscriber. Hal tersebut menunjukkan bahwa komunikasi antara publisher, broker, dan subscriber berhasil dilakukan.

### 2. Bandingkan besar overhead data dan pola komunikasi antara protokol HTTP dan MQTT berdasarkan hasil percobaan yang telah dilakukan!

HTTP dan MQTT memiliki perbedaan dari segi pola komunikasi maupun overhead data.

**HTTP:**
- Menggunakan pola komunikasi request-response, yaitu client mengirimkan request dan server memberikan response.
- Memiliki overhead yang relatif lebih besar karena setiap request membawa informasi header HTTP.
- Pada percobaan ini, ESP8266 mengirimkan data menggunakan metode POST dan menerima response code dari server.
- Pengiriman dilakukan secara berkala setiap 10 detik.

**MQTT:**
- Menggunakan pola komunikasi publish-subscribe melalui broker.
- Publisher mengirimkan pesan ke topic tertentu, kemudian broker meneruskannya kepada subscriber yang berlangganan pada topic tersebut.
- Memiliki overhead protokol yang relatif lebih kecil dibandingkan HTTP.
- Koneksi MQTT dapat dipertahankan sehingga perangkat tidak perlu membangun koneksi baru untuk setiap pesan.
- Pada percobaan ini, pengiriman dilakukan setiap 5 detik.

Berdasarkan perbandingan tersebut, MQTT lebih efisien untuk komunikasi data sensor secara berkala karena memiliki overhead protokol yang lebih kecil dan menggunakan koneksi yang dapat dipertahankan. Sementara itu, HTTP lebih sesuai untuk komunikasi yang membutuhkan pola request-response antara client dan server.

### 3. Untuk skenario pengiriman data sensor secara terus-menerus setiap beberapa detik dalam jangka waktu lama, protokol manakah (HTTP atau MQTT) yang lebih sesuai digunakan? Jelaskan alasannya!

Protokol MQTT lebih sesuai digunakan untuk pengiriman data sensor secara terus-menerus dalam interval beberapa detik dan jangka waktu yang lama.

Hal ini karena MQTT menggunakan mekanisme publish-subscribe dengan koneksi yang dapat dipertahankan antara perangkat dan broker. Selain itu, ukuran overhead protokol MQTT relatif lebih kecil sehingga penggunaan bandwidth jaringan menjadi lebih efisien.

Dengan karakteristik tersebut, MQTT cocok diterapkan pada sistem IoT yang membutuhkan pengiriman data secara berkala, seperti pemantauan suhu, kelembaban, kondisi lingkungan, dan monitoring perangkat secara real-time.

### 4. Bagaimana peran format JSON dalam mendukung interoperabilitas data antara perangkat IoT dan berbagai platform/aplikasi yang berbeda?

JSON (JavaScript Object Notation) merupakan format pertukaran data berbasis teks yang menggunakan struktur pasangan key dan value. Format ini memudahkan perangkat IoT untuk menyimpan serta mengirimkan informasi dengan susunan yang teratur dan mudah dipahami.

JSON mendukung interoperabilitas karena dapat digunakan dan dibaca oleh berbagai bahasa pemrograman maupun platform, seperti Python, JavaScript, PHP, dan aplikasi berbasis web. Dengan demikian, data yang dikirimkan oleh ESP8266 dapat diterima serta diolah oleh server, database, maupun dashboard tanpa memerlukan format khusus yang hanya dapat digunakan oleh satu jenis perangkat.

Pada praktikum ini, JSON digunakan untuk mengirimkan data suhu dan kelembaban melalui HTTP maupun MQTT. Penggunaan format yang sama pada kedua protokol tersebut memudahkan proses pertukaran dan pengolahan data antarperangkat dan aplikasi.

