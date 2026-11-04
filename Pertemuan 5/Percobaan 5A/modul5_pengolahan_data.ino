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

    // Suhu dasar berubah secara bertahap
    float suhuDasar = 28.0 + 2.0 * sin(jumlahBaca * 0.08);

    // Noise untuk mensimulasikan fluktuasi sensor
    float noise = random(-5, 6) * 0.1;

    float suhu = suhuDasar + noise;

    // Lonjakan suhu setiap 25 pembacaan
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

void setup() {
    Serial.begin(115200);
    randomSeed(micros());

    waktuMulai = millis();

    // Header tabel
    Serial.println();
    Serial.println("TABEL 5.1. PENGOLAHAN DATA SUHU PADA ESP32");
    Serial.println("No | Waktu(s) | Mentah(C) | Moving Average(C) | Min(C) | Max(C)");
    Serial.println("---------------------------------------------------------------");
}

void loop() {
    // Menghasilkan data suhu simulasi
    float suhu = bacaSuhuMock();

    // Menghitung rata-rata bergerak
    float suhuFilter = hitungMovingAverage(suhu);

    // Memperbarui suhu minimum dan maksimum
    if (suhu < suhuMin) {
        suhuMin = suhu;
    }

    if (suhu > suhuMax) {
        suhuMax = suhu;
    }

    // Menghitung waktu sejak program dimulai
    unsigned long waktu = (millis() - waktuMulai) / 1000;

    nomorData++;

    // Menampilkan satu baris tabel
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
    Serial.println(suhuMax, 2);

    // Interval pengukuran 2 detik
    delay(2000);
}
