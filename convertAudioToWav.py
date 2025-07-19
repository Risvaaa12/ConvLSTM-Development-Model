from pydub import AudioSegment
import os

def convert_audio_folder(input_root, output_root):
    for subdir, _, files in os.walk(input_root):
        for file in files:
            file_ext = os.path.splitext(file)[1].lower()
            if file_ext in [".mp3", ".m4a"]:
                input_path = os.path.join(subdir, file)

                # Struktur path relatif dari raw_data
                relative_path = os.path.relpath(subdir, input_root)
                output_folder = os.path.join(output_root, relative_path)

                # Buat folder output jika belum ada
                os.makedirs(output_folder, exist_ok=True)

                # Path output file .wav
                output_file = os.path.splitext(file)[0] + ".wav"
                output_path = os.path.join(output_folder, output_file)

                try:
                    print(f"Mengonversi: {input_path} -> {output_path}")
                    if file_ext == ".mp3":
                        audio = AudioSegment.from_mp3(input_path)
                    elif file_ext == ".m4a":
                        audio = AudioSegment.from_file(input_path, format="m4a")

                    audio.export(output_path, format="wav")
                    print(f"✔️ Selesai: {output_path}")
                except Exception as e:
                    print(f"❌ Gagal konversi {input_path}: {e}")

# Ganti dengan path ke folder 'raw_data' dan tentukan output folder
input_folder = "E:/RISVA/streamlit/joged_bumbung"
output_folder = "joged_bumbung_wav"

convert_audio_folder(input_folder, output_folder)