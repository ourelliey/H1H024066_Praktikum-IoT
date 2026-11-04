
import json
import time
import os

import paho.mqtt.client as mqtt
import pandas as pd
import matplotlib.pyplot as plt

# ==================================================
# KONFIGURASI MQTT
# ==================================================
BROKER = "broker.hivemq.com"
PORT = 1883

# HARUS SAMA PERSIS dengan topicData di program Arduino
TOPIC = "unsoed/tk245004/kelompok1/data"

JUMLAH_SAMPEL = 20

# Simpan hasil di folder yang sama dengan file Python
FOLDER_HASIL = os.path.dirname(os.path.abspath(__file__))
FILE_CSV = os.path.join(FOLDER_HASIL, "data_suhu.csv")
FILE_GRAFIK = os.path.join(FOLDER_HASIL, "grafik_suhu.png")

data = []
waktu_mulai = time.time()
waktu_mulai_pengumpulan = None

# ==================================================
# CALLBACK KONEKSI MQTT
# ==================================================
def on_connect(client, userdata, flags, reason_code, properties):
    print("Status koneksi MQTT:", reason_code)

    if reason_code == 0:
        print("Berhasil terhubung ke broker MQTT.")
        print("Topik:", TOPIC)
        client.subscribe(TOPIC)
        print(f"\nMenunggu {JUMLAH_SAMPEL} data suhu...\n")
    else:
        print("Koneksi MQTT gagal.")

# ==================================================
# CALLBACK PENERIMAAN DATA
# ==================================================
def on_message(client, userdata, msg):
    global waktu_mulai_pengumpulan

    try:
        payload = json.loads(msg.payload.decode("utf-8"))
        suhu = float(payload["suhu"])

        if not pd.notna(suhu):
            raise ValueError("Nilai suhu tidak valid")

    except (ValueError, KeyError, TypeError, json.JSONDecodeError):
        print("Pesan tidak valid, diabaikan.")
        return

    # Waktu penerimaan di komputer
    waktu_penerimaan = time.strftime(
        "%Y-%m-%d %H:%M:%S",
        time.localtime()
    )

    # Waktu relatif sejak data pertama diterima
    waktu_sekarang = time.time()

    if waktu_mulai_pengumpulan is None:
        waktu_mulai_pengumpulan = waktu_sekarang

    waktu_detik = round(
        waktu_sekarang - waktu_mulai_pengumpulan, 2
    )

    # Simpan data mentah
    data.append({
        "waktu_penerimaan": waktu_penerimaan,
        "waktu_detik": waktu_detik,
        "suhu": suhu
    })

    nomor = len(data)

    print(
        f"[{nomor:02d}/{JUMLAH_SAMPEL}] "
        f"Waktu: {waktu_penerimaan} | "
        f"Suhu: {suhu:.2f} °C"
    )

    # Hentikan pengumpulan setelah 20 data
    if len(data) >= JUMLAH_SAMPEL:
        print("\n20 data sudah diterima.")
        client.disconnect()

# ==================================================
# TAHAP 1: AKUISISI DATA MELALUI MQTT
# ==================================================
client = mqtt.Client(
    callback_api_version=mqtt.CallbackAPIVersion.VERSION2
)

client.on_connect = on_connect
client.on_message = on_message

print("Menghubungkan ke broker MQTT...")

try:
    client.connect(BROKER, PORT, 60)
    client.loop_forever()

except KeyboardInterrupt:
    print("\nPengumpulan data dihentikan oleh pengguna.")

except Exception as error:
    print("\nTerjadi kesalahan koneksi MQTT:", error)

# ==================================================
# PERIKSA DATA
# ==================================================
if len(data) == 0:
    print("\nTidak ada data yang diterima.")
    print("Periksa Wi-Fi, ESP8266, broker, dan topik MQTT.")
    raise SystemExit

if len(data) < JUMLAH_SAMPEL:
    print(
        f"\nPeringatan: hanya {len(data)} data diterima, "
        f"belum mencapai {JUMLAH_SAMPEL}."
    )

# ==================================================
# TAHAP 2: ANALISIS Z-SCORE
# ==================================================
df = pd.DataFrame(data)

rata_rata = df["suhu"].mean()
std_deviasi = df["suhu"].std(ddof=1)

if pd.isna(std_deviasi) or std_deviasi == 0:
    df["zscore"] = 0.0
else:
    df["zscore"] = (
        (df["suhu"] - rata_rata) / std_deviasi
    ).round(4)

# Batas anomali sesuai DAPENG: |z| > 2
df["anomali"] = df["zscore"].abs() > 2

df["status_anomali"] = df["anomali"].apply(
    lambda nilai: "Anomali" if nilai else "Normal"
)

# ==================================================
# TAHAP 3: SIMPAN DATA KE CSV
# ==================================================
df["status_penyimpanan_csv"] = ""

kolom_csv = [
    "waktu_penerimaan",
    "waktu_detik",
    "suhu",
    "zscore",
    "status_anomali",
    "status_penyimpanan_csv"
]

try:
    # Status awal; file ditulis terlebih dahulu
    df["status_penyimpanan_csv"] = "Tersimpan"

    df[kolom_csv].to_csv(
        FILE_CSV,
        index=False,
        encoding="utf-8-sig"
    )

    print(f"\nCSV berhasil disimpan: {FILE_CSV}")

except Exception as error:
    df["status_penyimpanan_csv"] = f"Gagal: {error}"
    print("\nGagal menyimpan CSV:", error)

    # Coba simpan ulang informasi status kegagalan
    try:
        df[kolom_csv].to_csv(
            FILE_CSV,
            index=False,
            encoding="utf-8-sig"
        )
    except Exception:
        pass

# ==================================================
# TAHAP 4: TAMPILKAN TABEL 5.2 DI TERMINAL
# ==================================================
print("\n" + "=" * 112)
print("TABEL 5.2. HASIL AKUISISI DAN ANALISIS DATA SUHU MELALUI MQTT")
print("=" * 112)

print(
    f"{'No.':<4} "
    f"{'Waktu Penerimaan':<20} "
    f"{'Suhu (°C)':>10} "
    f"{'Z-score':>10} "
    f"{'Status Anomali':<16} "
    f"{'Status CSV':<14}"
)

print("-" * 112)

for nomor, baris in df.iterrows():
    print(
        f"{nomor + 1:<4} "
        f"{baris['waktu_penerimaan']:<20} "
        f"{baris['suhu']:>10.2f} "
        f"{baris['zscore']:>10.4f} "
        f"{baris['status_anomali']:<16} "
        f"{baris['status_penyimpanan_csv']:<14}"
    )

print("-" * 112)

# ==================================================
# RINGKASAN STATISTIK
# ==================================================
print("\nRINGKASAN STATISTIK")
print(f"Jumlah data      : {len(df)}")
print(f"Rata-rata suhu   : {rata_rata:.2f} °C")
print(f"Standar deviasi  : {std_deviasi:.4f}")
print(f"Suhu minimum     : {df['suhu'].min():.2f} °C")
print(f"Suhu maksimum    : {df['suhu'].max():.2f} °C")
print(f"Jumlah anomali   : {int(df['anomali'].sum())}")
print(f"File CSV         : {FILE_CSV}")

# ==================================================
# TAHAP 5: VISUALISASI DATA
# ==================================================
plt.figure(figsize=(10, 5))

nomor_data = range(1, len(df) + 1)

plt.plot(
    nomor_data,
    df["suhu"],
    marker="o",
    label="Suhu"
)

data_anomali = df[df["anomali"]]

if not data_anomali.empty:
    plt.scatter(
        data_anomali.index + 1,
        data_anomali["suhu"],
        color="red",
        s=100,
        label="Anomali",
        zorder=3
    )

plt.axhline(
    rata_rata,
    linestyle="--",
    label=f"Rata-rata: {rata_rata:.2f} °C"
)

plt.xlabel("Nomor Data")
plt.ylabel("Suhu (°C)")
plt.title("Percobaan 5B: Akuisisi dan Deteksi Anomali Suhu")
plt.xticks(list(nomor_data))
plt.grid(True, alpha=0.3)
plt.legend()
plt.tight_layout()

try:
    plt.savefig(FILE_GRAFIK, dpi=150)
    print(f"Grafik berhasil disimpan: {FILE_GRAFIK}")
    plt.show()

except Exception as error:
    print("Gagal membuat grafik:", error)

print("\nProses Percobaan 5B selesai.")
