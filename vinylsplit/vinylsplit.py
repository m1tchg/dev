import matplotlib.pyplot as plt
import os
import io
import subprocess
import librosa
import numpy as np
from beets.util import syspath

# SETTINGS
 MASTER_VINYL = "Recording_20220203223743.dsf"
OUTPUT_DIR = "./split_tracks/Recording_20220203223743"
TOP_DB = 30  # Adjust if it misses gaps


def split_to_flac():
    os.makedirs(OUTPUT_DIR, exist_ok=True)

    # Downsample and pipe to librosa
    print(f"--- Analyzing { MASTER_VINYL} ---")
    cmd = ['ffmpeg', '-i',  MASTER_VINYL, '-f',
           'wav', '-ar', '16000', '-ac', '1', '-']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, _ = proc.communicate()

    audio_data, _ = librosa.load(io.BytesIO(stdout), sr=16000)

    # 1. Smaller frames to catch narrow gaps between songs
    frame_length = 4096
    hop_length = 1024

    # 2. Calculate the noise floor to help you pick TOP_DB
    rms = librosa.feature.rms(
        y=audio_data, frame_length=frame_length, hop_length=hop_length)
    rms_db = librosa.amplitude_to_db(rms, ref=np.max)
    avg_loudness = np.mean(rms_db)
    min_loudness = np.min(rms_db)

    print(f"Average volume: {avg_loudness:.2f} dB")
    print(f"Quietest point: {min_loudness:.2f} dB")

    # We must be less sensitive than your noise floor (-28.5)
    # Try 20 or 22.
    # This says: "If it's 22dB quieter than the loudest part, it's a gap."
    # 1. Detect everything at that sensitive threshold
    intervals = librosa.effects.split(
        audio_data, top_db=TOP_DB, frame_length=8192, hop_length=2048)

    # 2. Filter: Only keep segments longer than 90 seconds
    # (Heliocentrics tracks are usually long, so this kills the '32 tracks' noise)
    valid_tracks = []
    for start_sample, end_sample in intervals:
        duration_sec = (end_sample - start_sample) / 16000
        if duration_sec > 45:  # Adjust to 60 if you have short interludes
            valid_tracks.append((start_sample, end_sample))

    print(f"Filtered {len(intervals)} raw segments down to {
          len(valid_tracks)} real tracks.")

    # 3. Create cut points from the start of the valid tracks (after the first track)
    cut_points = [librosa.samples_to_time(
        t[0], sr=16000) for t in valid_tracks[1:]]
    print(f"Detected {len(cut_points) + 1} potential tracks.")

    # 2. Split Loop
    start_time = 0.0
    # Add a None at the end to represent the end of the file
    all_points = list(cut_points) + [None]

    for i, end_time in enumerate(all_points):
        out_path = os.path.join(OUTPUT_DIR, f"track_{i+1:02d}.flac")

        split_cmd = ['ffmpeg', '-y', '-ss', str(start_time)]
        if end_time:
            duration = end_time - start_time
            split_cmd += ['-t', str(duration)]

        split_cmd += [
            '-i',  MASTER_VINYL,
            '-c:a', 'flac', '-sample_fmt', 's32',
            '-compression_level', '5', out_path
        ]

        print(f"Writing {out_path}...")
        subprocess.check_call(
            split_cmd, stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)

        if end_time:
            start_time = end_time

    print(f"\nSUCCESS! Tracks are in {OUTPUT_DIR}")
    return audio_data, valid_tracks


def plot_splits(audio_data, intervals, sr=16000):
    plt.figure(figsize=(15, 5))
    # Convert audio to dB for easier viewing
    S = librosa.amplitude_to_db(np.abs(librosa.stft(audio_data, hop_length=2048)), ref=np.max)
    librosa.display.specshow(S, sr=sr, hop_length=2048,x_axis='time', y_axis='hz')

    # Draw vertical lines for every cut
    for start, end in intervals:
        plt.axvline(librosa.samples_to_time(start, sr=sr),
                    color='green', linestyle='--', alpha=0.5)
        plt.axvline(librosa.samples_to_time(end, sr=sr),
                    color='red', linestyle='--', alpha=0.5)

# Add this inside your plotting logic
    rms_energy = librosa.feature.rms(
        y=audio, frame_length=2048, hop_length=2048)[0]
    plt.plot(librosa.frames_to_time(range(len(rms_energy))),
             rms_energy, color='orange', label='RMS Energy')

    plt.title("Vinyl Split Map (Green=Start, Red=End)")
    plt.savefig("split_map.png")
    print("Graph saved to split_map.png")


def plot_envelope(audio_data, valid_tracks, sr=16000):
    import matplotlib.pyplot as plt

    # Create a low-res version for plotting
    resampled = audio_data[::100]
    times = np.linspace(0, len(audio_data)/sr, len(resampled))

    plt.figure(figsize=(15, 5))
    plt.plot(times, resampled, color='gray', alpha=0.5)

    # Highlight the detected songs in green
    for start, end in valid_tracks:
        plt.axvspan(start/sr, end/sr, color='green', alpha=0.3)

# Add this inside your plotting logic
    rms_energy = librosa.feature.rms(
        y=audio, frame_length=2048, hop_length=512)[0]
    plt.plot(librosa.frames_to_time(range(len(rms_energy))),
             rms_energy, color='orange', label='RMS Energy')

    plt.title("Heliocentrics Rip: Detected Songs (Green)")
    plt.xlabel("Time (seconds)")
    plt.savefig("split_map.png")
    print("Visual map saved to split_map.png")


if __name__ == "__main__":
    audio, intervals = split_to_flac()
    plot_splits(audio, intervals)
