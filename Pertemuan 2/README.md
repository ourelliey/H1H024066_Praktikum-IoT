**Nama:** Aurellia Nabila Rahma Putri  
**NIM:** H1H024066  
**Shift Awal:** C  
**Shift Akhir:** D  

---

# Pertanyaan Praktikum – Percobaan 2A

## 1. Gambarkan diagram alur (flowchart) proses koneksi ESP32 ke jaringan WiFi pada program di atas!

<img width="2070" height="3603" alt="flowchartmodul2" src="https://github.com/user-attachments/assets/f1a763db-53b2-44ec-8709-2962b6c87e12" />


## 2. Apa fungsi dari perintah `WiFi.mode(WIFI_STA)` pada program tersebut?

Perintah `WiFi.mode(WIFI_STA)` digunakan untuk mengatur ESP32 agar bekerja dalam mode Station atau sebagai perangkat klien WiFi. Dalam mode ini, ESP32 akan terhubung ke jaringan yang telah tersedia, seperti router atau hotspot, menggunakan SSID dan password yang sudah ditentukan. Mode Station memungkinkan ESP32 memperoleh alamat IP dari jaringan tersebut sehingga dapat berkomunikasi dengan perangkat lain melalui jaringan WiFi.

## 3. Jelaskan apa yang terjadi apabila SSID atau password yang dimasukkan salah!

Apabila SSID yang dimasukkan tidak sesuai, ESP32 tidak dapat menemukan jaringan WiFi yang ingin dihubungkan. Sementara itu, jika SSID benar tetapi password salah, proses autentikasi akan gagal karena akses ke jaringan ditolak.

Dalam kedua kondisi tersebut, ESP32 tidak akan memperoleh status `WL_CONNECTED`. Akibatnya, program akan terus menjalankan perulangan untuk memeriksa status koneksi dan menampilkan tanda titik pada Serial Monitor. Jika tidak ditambahkan batas waktu atau mekanisme penanganan kesalahan, proses tersebut dapat berlangsung terus-menerus.

## 4. Modifikasi program agar ESP32 mencoba menghubungkan ulang (reconnect) secara otomatis apabila koneksi WiFi terputus, dan berikan penjelasan di setiap baris kode yang ditambahkan!

Modifikasi dilakukan dengan menambahkan fungsi untuk menghubungkan ESP32 ke WiFi kembali ketika koneksi terputus. Pemeriksaan koneksi dilakukan secara berkala menggunakan `millis()` dan ditambahkan timeout agar program tidak menunggu koneksi tanpa batas waktu.

```cpp
#include <WiFi.h>

const char* ssid = "NAMA_WIFI_ANDA";
const char* password = "PASSWORD_WIFI_ANDA";
const int ledPin = 2;

// Variabel untuk menyimpan waktu pemeriksaan koneksi terakhir
unsigned long waktuTerakhirCek = 0;

// Interval pemeriksaan koneksi setiap 5 detik
const unsigned long intervalCek = 5000;

// Fungsi untuk menghubungkan ESP32 ke WiFi
void hubungkanWiFi() {
  WiFi.mode(WIFI_STA);
  WiFi.begin(ssid, password);

  Serial.print("Menghubungkan ke WiFi");

  // Menyimpan waktu awal proses koneksi
  unsigned long waktuMulai = millis();

  // Mencoba menghubungkan WiFi maksimal selama 10 detik
  while (WiFi.status() != WL_CONNECTED &&
         millis() - waktuMulai < 10000) {
    delay(500);
    Serial.print(".");
  }

  // Memeriksa apakah koneksi berhasil
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println("\nWiFi berhasil terhubung!");
    digitalWrite(ledPin, HIGH);
  } else {
    Serial.println("\nGagal terhubung, akan dicoba lagi nanti.");
    digitalWrite(ledPin, LOW);
  }
}

void setup() {
  Serial.begin(115200);

  pinMode(ledPin, OUTPUT);
  digitalWrite(ledPin, LOW);

  // Melakukan koneksi WiFi pertama kali
  hubungkanWiFi();
}

void loop() {
  // Memeriksa koneksi setiap 5 detik
  if (millis() - waktuTerakhirCek >= intervalCek) {
    waktuTerakhirCek = millis();

    // Jika WiFi masih terhubung
    if (WiFi.status() == WL_CONNECTED) {
      Serial.println("Status: Terhubung");
    } else {
      // Jika koneksi terputus, lakukan reconnect
      Serial.println("Status: Terputus, mencoba menghubungkan ulang...");
      digitalWrite(ledPin, LOW);
      hubungkanWiFi();
    }
  }
}
```

**Penjelasan kode tambahan:**

- `waktuTerakhirCek` digunakan untuk menyimpan waktu terakhir ESP32 memeriksa koneksi WiFi.
- `intervalCek` menentukan jeda pemeriksaan koneksi, yaitu 5.000 milidetik atau 5 detik.
- `hubungkanWiFi()` merupakan fungsi khusus untuk menjalankan proses koneksi WiFi sehingga dapat dipanggil kembali ketika koneksi terputus.
- `millis()` digunakan untuk menghitung waktu berjalan sejak ESP32 dinyalakan.
- Batas waktu 10 detik digunakan agar ESP32 tidak terus menunggu apabila koneksi gagal.
- `WiFi.status()` digunakan untuk mengetahui kondisi koneksi WiFi.
- LED akan menyala ketika koneksi berhasil dan mati ketika koneksi gagal atau terputus.

---

# Pertanyaan Praktikum – Percobaan 2B

## 1. Mengapa alamat IP default Access Point pada ESP32 umumnya bernilai 192.168.4.1?

Alamat IP `192.168.4.1` merupakan alamat bawaan yang umum digunakan ESP32 ketika beroperasi dalam mode Access Point. Alamat tersebut termasuk dalam rentang IP privat yang digunakan untuk komunikasi jaringan lokal dan tidak dapat diakses secara langsung melalui internet publik.

Penggunaan alamat default ini memudahkan pengguna untuk mengakses ESP32 ketika perangkat berfungsi sebagai penyedia jaringan WiFi. Alamat tersebut juga dapat diubah sesuai kebutuhan melalui konfigurasi jaringan menggunakan fungsi `WiFi.softAPConfig()`.

## 2. Apa perbedaan mendasar antara mode Station dan mode Access Point pada ESP32?

Mode Station (STA) dan Access Point (AP) memiliki fungsi yang berbeda.

- **Station (STA):** ESP32 bertindak sebagai klien yang terhubung ke jaringan WiFi yang sudah tersedia, seperti router atau hotspot. Untuk terhubung, ESP32 membutuhkan SSID dan password jaringan tersebut.
- **Access Point (AP):** ESP32 bertindak sebagai penyedia jaringan WiFi dengan membuat SSID dan password sendiri. Perangkat lain dapat terhubung langsung ke jaringan yang dibuat oleh ESP32.

Dengan demikian, mode Station digunakan untuk menghubungkan ESP32 ke jaringan yang sudah ada, sedangkan mode Access Point digunakan agar ESP32 dapat menyediakan jaringan bagi perangkat lain.

## 3. Jelaskan risiko keamanan apabila password Access Point tidak diberikan atau terlalu sederhana!

Access Point yang tidak menggunakan password atau memiliki password yang mudah ditebak dapat diakses oleh orang lain tanpa izin. Kondisi tersebut dapat menimbulkan berbagai risiko keamanan, seperti akses tidak sah ke perangkat ESP32, penyalahgunaan jaringan, serta kemungkinan perubahan konfigurasi atau pengiriman perintah yang tidak diinginkan.

Selain itu, perangkat yang tidak dikenal dapat menggunakan jaringan sehingga menyebabkan peningkatan beban koneksi. Oleh karena itu, penggunaan password yang kuat dan tidak mudah ditebak diperlukan untuk melindungi jaringan Access Point.

## 4. Modifikasi program agar ESP32 berjalan pada mode AP+STA (terhubung ke WiFi rumah sekaligus menyediakan Access Point), dan berikan penjelasan di setiap baris kodenya!

Mode AP+STA memungkinkan ESP32 menjalankan dua fungsi WiFi secara bersamaan, yaitu terhubung ke jaringan WiFi rumah sebagai Station sekaligus menyediakan jaringan sendiri sebagai Access Point.

```cpp
#include <WiFi.h>

// Data jaringan WiFi rumah untuk mode Station
const char* sta_ssid = "NAMA_WIFI_RUMAH";
const char* sta_password = "PASSWORD_WIFI_RUMAH";

// Data jaringan yang akan dibuat ESP32 sebagai Access Point
const char* ap_ssid = "ESP32_AccessPoint";
const char* ap_password = "12345678";

void setup() {
  Serial.begin(115200);

  // Mengaktifkan mode gabungan Station dan Access Point
  WiFi.mode(WIFI_AP_STA);

  // Membuat jaringan WiFi dari ESP32
  WiFi.softAP(ap_ssid, ap_password);

  // Menampilkan alamat IP Access Point
  Serial.print("AP IP Address : ");
  Serial.println(WiFi.softAPIP());

  // Menghubungkan ESP32 ke jaringan WiFi rumah
  WiFi.begin(sta_ssid, sta_password);

  Serial.print("Menghubungkan ke WiFi rumah");

  // Menyimpan waktu awal proses koneksi
  unsigned long waktuMulai = millis();

  // Menunggu koneksi maksimal selama 10 detik
  while (WiFi.status() != WL_CONNECTED &&
         millis() - waktuMulai < 10000) {
    delay(500);
    Serial.print(".");
  }

  // Memeriksa keberhasilan koneksi Station
  if (WiFi.status() == WL_CONNECTED) {
    Serial.println();
    Serial.print("STA IP Address : ");
    Serial.println(WiFi.localIP());
  } else {
    Serial.println("\nGagal terhubung ke WiFi rumah (mode AP tetap aktif).");
  }
}

void loop() {
  // Menghitung jumlah perangkat yang terhubung ke Access Point
  int jumlahClient = WiFi.softAPgetStationNum();

  // Menampilkan jumlah perangkat yang terhubung
  Serial.print("Jumlah client AP: ");
  Serial.println(jumlahClient);

  delay(5000);
}
```

**Penjelasan kode:**

- `WiFi.mode(WIFI_AP_STA)` mengaktifkan mode gabungan Station dan Access Point.
- `sta_ssid` dan `sta_password` menyimpan identitas jaringan WiFi rumah yang akan dihubungkan.
- `ap_ssid` dan `ap_password` digunakan untuk menentukan nama dan password jaringan yang dibuat ESP32.
- `WiFi.softAP()` digunakan untuk mengaktifkan Access Point pada ESP32.
- `WiFi.softAPIP()` digunakan untuk menampilkan alamat IP jaringan Access Point.
- `WiFi.begin()` digunakan untuk memulai koneksi ESP32 ke jaringan WiFi rumah.
- `WiFi.localIP()` digunakan untuk menampilkan alamat IP yang diperoleh ESP32 dari jaringan rumah.
- `WiFi.softAPgetStationNum()` digunakan untuk mengetahui jumlah perangkat yang sedang terhubung ke Access Point ESP32.
- `delay(5000)` memberikan jeda selama 5 detik sebelum jumlah perangkat diperiksa kembali.

---

# Pertanyaan Analisis

## 1. Uraikan hasil tugas pada praktikum yang telah dilakukan pada setiap percobaan!

Pada Percobaan 2A, ESP32 dikonfigurasikan menggunakan mode Station agar dapat terhubung ke jaringan WiFi yang telah ditentukan. Ketika proses koneksi berhasil, perangkat akan memperoleh alamat IP dan menampilkan informasi koneksi melalui Serial Monitor. Pengujian dengan SSID atau password yang tidak sesuai dapat menyebabkan koneksi gagal sehingga ESP32 tidak memperoleh status `WL_CONNECTED`.

Pada Percobaan 2B, ESP32 dikonfigurasikan menggunakan mode Access Point sehingga dapat membuat jaringan WiFi sendiri. Jaringan tersebut memiliki nama dan password yang telah ditentukan dalam program. ESP32 juga dapat menampilkan alamat IP Access Point serta memantau jumlah perangkat yang terhubung.

*Catatan: Sesuaikan uraian ini dengan hasil Serial Monitor dan pengujian yang benar-benar kamu peroleh.*

## 2. Bagaimana pengaruh kekuatan sinyal (RSSI) terhadap kestabilan koneksi WiFi pada perangkat IoT?

RSSI (Received Signal Strength Indicator) merupakan indikator yang digunakan untuk mengetahui kekuatan sinyal WiFi yang diterima oleh perangkat. Nilai RSSI biasanya dinyatakan dalam satuan dBm dan memiliki nilai negatif. Semakin mendekati nol nilainya, semakin kuat sinyal yang diterima.

Apabila nilai RSSI semakin kecil atau semakin jauh dari nol, kualitas sinyal akan semakin lemah. Hal ini dapat menyebabkan koneksi menjadi tidak stabil, kecepatan pengiriman data menurun, hingga terjadinya kehilangan paket data atau terputusnya koneksi. Oleh sebab itu, perangkat IoT sebaiknya ditempatkan pada lokasi dengan penerimaan sinyal WiFi yang baik agar proses komunikasi data dapat berlangsung dengan stabil.

## 3. Bagaimana cara kerja ESP32 dalam membedakan peran sebagai klien (Station) dan sebagai penyedia jaringan (Access Point)?

ESP32 membedakan kedua peran tersebut melalui pengaturan mode WiFi menggunakan fungsi `WiFi.mode()`.

Ketika menggunakan mode `WIFI_STA`, ESP32 berfungsi sebagai klien yang mencari dan menghubungkan diri ke jaringan WiFi eksternal menggunakan fungsi `WiFi.begin()`. Setelah berhasil terhubung, ESP32 akan memperoleh alamat IP dari router melalui mekanisme DHCP.

Sementara itu, ketika menggunakan mode `WIFI_AP`, ESP32 berfungsi sebagai penyedia jaringan dengan membuat SSID sendiri melalui fungsi `WiFi.softAP()`. Perangkat lain dapat terhubung ke jaringan tersebut tanpa memerlukan router eksternal. ESP32 juga menyediakan alamat IP dan mengatur koneksi perangkat yang bergabung ke jaringan Access Point-nya.

## 4. Bagaimana kombinasi mode Station dan Access Point (AP+STA) dapat dimanfaatkan dalam skenario nyata sistem IoT, misalnya pada proses konfigurasi awal perangkat (provisioning)?

Mode AP+STA dapat dimanfaatkan dalam proses provisioning atau konfigurasi awal perangkat IoT. Ketika pertama kali dinyalakan, ESP32 dapat membuat jaringan Access Point sendiri agar pengguna dapat menghubungkan smartphone atau laptop secara langsung ke perangkat.

Melalui jaringan tersebut, pengguna dapat mengakses halaman konfigurasi untuk memasukkan SSID dan password WiFi rumah atau kantor. Setelah informasi jaringan dimasukkan, ESP32 dapat menggunakan mode Station untuk terhubung ke jaringan tersebut, sementara Access Point tetap dapat digunakan sesuai konfigurasi perangkat.

Penerapan ini memudahkan proses pengaturan perangkat IoT karena pengguna tidak harus menghubungkan ESP32 ke komputer untuk mengubah konfigurasi jaringan secara langsung. Contoh penerapannya dapat ditemukan pada perangkat smart home seperti lampu pintar, smart plug, dan perangkat pemantauan berbasis IoT.
