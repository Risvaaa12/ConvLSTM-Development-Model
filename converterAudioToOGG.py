import os
from pydub import AudioSegment

# Folder input dan output
input_folder = "soal_audio"    # Ganti dengan folder yang berisi file .wav hasil potongan
output_folder = "soal_audio_ogg"     # Folder hasil .ogg

# Buat folder output jika belum ada
os.makedirs(output_folder, exist_ok=True)

# Iterasi semua file .wav di folder input
for filename in os.listdir(input_folder):
    if filename.endswith(".wav"):
        file_path = os.path.join(input_folder, filename)
        print(f"Mengonversi: {filename}")

        # Load file .wav
        audio = AudioSegment.from_wav(file_path)

        # Nama file output .ogg
        output_filename = os.path.splitext(filename)[0] + ".ogg"
        output_path = os.path.join(output_folder, output_filename)

        # Export sebagai .ogg
        audio.export(output_path, format="ogg")

print("Selesai mengonversi semua file .wav ke .ogg.")
