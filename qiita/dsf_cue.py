import os
import io
import subprocess
import librosa
import numpy as np

# SETTINGS
MASTER_VINYL = "Babyfather - meditation - Recording_20201107063330.dsf"

# Librosa parameters
top_db = 30  # 10パーセンタイルより約6～8dB低い値に設定する。
frame_length = 8192   # トラック間の狭い隙間を捉えるために、より小さなフレームを設定する
hop_length = 2048  # librosaがボリュームを確認する頻度
sr = 16000


def split_to_flac():

    print(f"--- Analyzing {MASTER_VINYL} ---")
    cmd = ['ffmpeg', '-i',  MASTER_VINYL, '-f',
           'wav', '-ar', str(sr), '-ac', '1', '-']
    proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                            stderr=subprocess.PIPE)
    stdout, _ = proc.communicate()

    audio_data, _ = librosa.load(io.BytesIO(stdout), sr=sr)

    rms = librosa.feature.rms(
        y=audio_data, frame_length=frame_length, hop_length=hop_length)
    rms_db = librosa.amplitude_to_db(rms, ref=np.max)
    p10_db = np.percentile(rms_db, 10)
    min_db = np.min(rms_db)

    print(f"最も静かな10% dB: {p10_db:.2f} dB")
    print(f"リードインの無音 dB: {min_db:.2f} dB")

    intervals = librosa.effects.split(
        audio_data, top_db=top_db, frame_length=frame_length, hop_length=hop_length)

    valid_tracks = []
    for start_sample, end_sample in intervals:
        duration_sec = (end_sample - start_sample) / sr
        if duration_sec > 45:
            valid_tracks.append((start_sample, end_sample))

    print(f"{len(intervals)}個のセグメントから {len(valid_tracks)}個のトラックをしぼりこみました。")

    cue_lines = [f'FILE "{MASTER_VINYL}" BINARY']

    for i, (start_sample, end_sample) in enumerate(valid_tracks):
        raw_seconds = librosa.samples_to_time(start_sample, sr=sr).item()

        # 音声の開始位置を処理し、浮動小数点数を整数に変換します。
        total_frames = max(0, int(round(raw_seconds * 75)) - 75)

        total_seconds, frames = divmod(total_frames, 75)
        minutes, seconds = divmod(total_seconds, 60)

        timestamp = f"{minutes:02d}:{seconds:02d}:{frames:02d}"

        cue_lines.append(f'  TRACK {i+1:02d} AUDIO')
        cue_lines.append(f'    TITLE "Track {i+1:02d}"')
        cue_lines.append(f'    INDEX 01 {timestamp}')

    with open(f"{MASTER_VINYL}.cue", "w", encoding="utf-8") as f:
        f.write("\n".join(cue_lines))

    print(f"{len(valid_tracks)}個のトラックを含むキューシートを生成しました。")
    return audio_data, valid_tracks


if __name__ == "__main__":
    audio, intervals = split_to_flac()
