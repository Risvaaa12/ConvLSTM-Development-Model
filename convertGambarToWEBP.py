import os
from PIL import Image

# Folder input dan output
input_folder = "Gambar untuk Soal"     # Ganti dengan nama folder tempat gambar asli
output_folder = "Gambar untuk Soal_PNG"     # Folder untuk menyimpan hasil .webp

# Buat folder output jika belum ada
os.makedirs(output_folder, exist_ok=True)

# Ekstensi gambar yang didukung
supported_formats = ('.jpg', '.jpeg', '.bmp', '.tiff', '.webp')

# Iterasi semua file gambar di folder
for filename in os.listdir(input_folder):
    if filename.lower().endswith(supported_formats):
        file_path = os.path.join(input_folder, filename)
        print(f"Mengonversi: {filename}")

        # Buka gambar
        with Image.open(file_path) as img:
            # Konversi ke RGB jika gambar punya alpha channel
            if img.mode in ("RGBA", "P"):
                img = img.convert("RGB")

            # Simpan sebagai WebP
            output_filename = os.path.splitext(filename)[0] + ".png"
            output_path = os.path.join(output_folder, output_filename)
            img.save(output_path, format="PNG", quality=100)  # kamu bisa ubah kualitas (0–100)

print("Selesai mengonversi semua gambar ke .PNG.")
