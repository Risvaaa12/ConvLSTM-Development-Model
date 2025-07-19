import os
import glob
import random
from pydub import AudioSegment
from pydub.silence import detect_nonsilent


DATASET_FOLDER = "dataset/joged"
TRAIN_FOLDER = os.path.join(DATASET_FOLDER, "train")
VALIDATION_FOLDER = os.path.join(DATASET_FOLDER, "validation")
SEGMENT_DURATION = 10000   # in milliseconds (e.g., 10000 ms = 10 seconds)
MIN_CONTENT_RATIO = 0.9    # minimum ratio of nonsilent content in a segment
VALIDATION_SPLIT = 0.2     # fraction for validation (exact split)
RANDOM_SEED = 42           # for reproducibility

CLASS_LABELS = {
    # 1: "angklung",
    # 2: "baleganjur",
    # 3: "gong_gede",
    # 4: "gong_kebyar",
    1: "joged_bumbung",
}

# ---------------- Utility Functions (Fungsi Bawaan Anda, Tanpa Perubahan) ----------------
def ensure_folders_exist():
    """
    Create train/validation folders for each class.
    """
    for base in [TRAIN_FOLDER, VALIDATION_FOLDER]:
        for class_name in CLASS_LABELS.values():
            path = os.path.join(base, class_name)
            os.makedirs(path, exist_ok=True)


def collect_valid_segments():
    segments = []
    for class_id, class_name in CLASS_LABELS.items():
        folder = class_name
        pattern = os.path.join(folder, "*.wav")
        
        files = sorted(glob.glob(pattern))

        if not files:
            # Pesan error ini sekarang lebih akurat
            print(f"No audio files found in folder '{class_name}'")
            continue

        for file_path in files:
            print(f"Loading: {file_path}")
            try:
                audio = AudioSegment.from_file(file_path)
            except Exception as e:
                print(f"Error loading {file_path}: {e}")
                continue

            for start_ms in range(0, len(audio), SEGMENT_DURATION):
                chunk = audio[start_ms:start_ms + SEGMENT_DURATION]
                nonsilent = detect_nonsilent(
                    chunk,
                    min_silence_len=500,
                    silence_thresh=chunk.dBFS - 16
                )
                total_nonsilent = sum(end - start for start, end in nonsilent)
                if total_nonsilent >= SEGMENT_DURATION * MIN_CONTENT_RATIO:
                    segments.append((chunk, class_name))
    return segments


def split_and_export(segments):
    random.seed(RANDOM_SEED)
    random.shuffle(segments)
    total = len(segments)
    
    if total == 0:
        print("No valid segments were collected. Cannot split or export.")
        return
        
    split_idx = int((1 - VALIDATION_SPLIT) * total)

    train_segs = segments[:split_idx]
    val_segs = segments[split_idx:]

    print(f"Total valid segments: {total}")
    print(f" - Training  : {len(train_segs)} segments")
    print(f" - Validation: {len(val_segs)} segments")

    def save_list(seg_list, base_folder):
        counters = {cls: 1 for cls in CLASS_LABELS.values()}
        for chunk, cls in seg_list:
            fname = f"{cls}_{counters[cls]}.wav"
            out_path = os.path.join(base_folder, cls, fname)
            chunk.export(out_path, format="wav")
            counters[cls] += 1

    save_list(train_segs, TRAIN_FOLDER)
    save_list(val_segs, VALIDATION_FOLDER)


# ---------------- Main Execution (Tanpa Perubahan) ----------------
if __name__ == "__main__":
    ensure_folders_exist()
    all_segments = collect_valid_segments()
    if all_segments:
        split_and_export(all_segments)
    else:
        print("No valid segments to process.")