#include <Arduino.h>
#include <math.h>
#include <ESP8266WiFi.h>
#include <PubSubClient.h>

// ===== KONFIGURASI WIFI =====
const char* ssid = "oyell";
const char* password = "12345678";

// ===== KONFIGURASI MQTT =====
const char* broker = "broker.hivemq.com";
const int port = 1883;

// Ganti dengan topik unik milikmu
const char* topicData = "unsoed/tk245004/kelompokaurelula/data";

WiFiClient espClient;
PubSubClient client(espClient);

// Interval pengiriman data
unsigned long waktuTerakhir = 0;
const unsigned long interval = 2000;

// ===== SUHU SIMULASI PENGGANTI DHT22 =====
float bacaSuhuMock() {
    static unsigned long jumlahBaca = 0;
    jumlahBaca++;

    float suhuDasar =
        28.0 + 2.0 * sin(jumlahBaca * 0.08);

    float noise = random(-5, 6) * 0.1;

    float suhu = suhuDasar + noise;

    // Anomali setiap 25 pembacaan
    if (jumlahBaca % 25 == 0) {
        suhu += 8.0;
    }

    return suhu;
}

// ===== KONEKSI WIFI =====
void setupWiFi() {
    Serial.print("Menghubungkan ke WiFi");

    WiFi.begin(ssid, password);

    while (WiFi.status() != WL_CONNECTED) {
        delay(500);
        Serial.print(".");
    }

    Serial.println("\nWiFi terhubung");
    Serial.println(WiFi.localIP());
}

// ===== KONEKSI MQTT =====
void reconnectMQTT() {
    while (!client.connected()) {
        Serial.print("Menghubungkan ke MQTT...");

        String clientId =
            "ESP32-Mock-" + String(random(0xffff), HEX);

        if (client.connect(clientId.c_str())) {
            Serial.println("berhasil");
        } else {
            Serial.print("gagal, kode: ");
            Serial.println(client.state());
            delay(2000);
        }
    }
}

void setup() {
    Serial.begin(115200);
    randomSeed(micros());

    setupWiFi();

    client.setServer(broker, port);
}

void loop() {
    if (WiFi.status() != WL_CONNECTED) {
        setupWiFi();
    }

    if (!client.connected()) {
        reconnectMQTT();
    }

    client.loop();

    if (millis() - waktuTerakhir >= interval) {
        waktuTerakhir = millis();

        float suhu = bacaSuhuMock();

        // Format pesan JSON untuk Python
        String payload = "{\"suhu\":" + String(suhu, 2) + "}";

        bool berhasil = client.publish(
            topicData,
            payload.c_str()
        );

        Serial.print("Suhu: ");
        Serial.print(suhu, 2);
        Serial.print(" C | MQTT: ");
        Serial.println(berhasil ? "Terkirim" : "Gagal");
    }
}
