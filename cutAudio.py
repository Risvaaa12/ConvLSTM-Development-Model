import os
from pydub import AudioSegment

# Folder tempat file .wav berada
folder_path = "soal"  # ganti dengan nama folder kamu
output_folder = "soal_audio"  # folder untuk menyimpan hasil potongan

# Buat folder output jika belum ada
os.makedirs(output_folder, exist_ok=True)

# Iterasi semua file di folder
for filename in os.listdir(folder_path):
    if filename.endswith(".wav"):
        file_path = os.path.join(folder_path, filename)
        print(f"Memproses: {filename}")

        # Load audio
        audio = AudioSegment.from_wav(file_path)

        # Potong 3 menit pertama (180000 ms)
        tiga_menit = 3 * 60 * 1000
        potongan = audio[:tiga_menit]

        # Simpan hasil potongan
        output_path = os.path.join(output_folder, f"{filename}")
        potongan.export(output_path, format="wav")

print("Selesai memotong semua audio.")
