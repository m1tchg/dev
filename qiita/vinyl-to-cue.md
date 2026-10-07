# ffmpegとlibrosaでレコードをトラックに分割

在宅勤務に切り替えてから、仕事中にレコードを聴くようになりました。何百枚ものレコードをDSD形式でリッピングしたのですが、トラックマーカーを設定するのをスキップしてしまったら、今では「Recording_2021040111010000.dsf」のようなファイルが何百個もできてしまい、どれがどのアーティストやアルバムなのか全く分からない状態です。

そこで、FFmpegとPythonのlibrosaを使って、DSFファイルから個々のトラックを抽出するスクリプトを作成してみました。

CUEシートを出力します。CUEファイルをfoobar2000や[dsf_split](https://github.com/shinkarenko/dsf-toolkit)などに渡して分割できます。

librosaとffmpegの基礎が、プロジェクトのヒントになれば幸いです。

全体のスクリプトは [GitHub](https://github.com/m1tchg/dev/blob/main/qiita/dsf_cue.py) に配置している。

## 依存関係

FFmpegライブラリと下のPythonのライブラリが必要です。

- librosa
- numpy

## インポートブロック

``` python
import os
import io
import subprocess
import librosa
import numpy as np
```

## スクリプトを実行する

スクリプトの先頭に \`MASTER_VINYL\` と \`OUTPUT_DIR\` を指定して、スクリプトを実行します。

``` bash
$ ~/.venvs/dsf_cue/bin/python3 dsf_cue.py

--- Recording_20220203223743.dsf を分析中 ---
最も静かな10% dB: -12.60 dB
リードインの無音 dB: -27.64 dB
43個のセグメントから、7個のトラックに絞り込みました。
7個のトラックを含むCUEシートを生成しました。
```

トラック数が正しく分割されなかったですよね？ ノイズフロアを見つけるのは難しいです。出力のdB値は、ffmpegおよびlibrosa関数のパラメータを調整する際に役立ちます。

## Pythonからffmpegを呼び出す

`subprocess`でFFmpegを呼び出し、出力をパイプ経由で `librosa.load` へ渡します。

``` python
sr = 16000
print(f"--- {MASTER_VINYL} を分析中 ---")
cmd = ['ffmpeg', '-i', MASTER_VINYL, '-f',
       'wav', '-ar', str(sr), '-ac', '1', '-']
proc = subprocess.Popen(cmd, stdout=subprocess.PIPE,
                        stderr=subprocess.PIPE)
stdout, _ = proc.communicate()
audio_data, _ = librosa.load(io.BytesIO(stdout), sr=sr)
```

解析を高速化するには、`-ar`で、16000 HzのサンプルレートへDSFをダウンサンプリングします。`-ac 1`と、ステレオをモノラルにダウンミックスします。

それで、`librosa`と音響データを分析しましょう。

## librosaで無音部分でばらする

`librosa.effects.split`を呼び出して、無音部分でばらします。

``` python
intervals = librosa.effects.split(
    audio_data, top_db=top_db, frame_length=frame_length, hop_length=hop_length)
```
librosa.splitは有音部分のみを抽出し、無音部分は除外します。そこで、`split` の `top_db` パラメータを使用して、最大ピークを基準に、残したい音のレベルです。

top_dbを推測します。そこで、推測の助けになるデータをいくつか集めましょう。dBの配列を撮って、いくつかの計算を行います。
配列に最大ピークが 0 dB になるよう正規化（ノーマライズ）されます。

``` python
rms = librosa.feature.rms(
    y=audio_data, frame_length=frame_length, hop_length=hop_length)
rms_db = librosa.amplitude_to_db(rms, ref=np.max)
p10_db = np.percentile(rms_db, 10)
min_db = np.min(rms_db)
```

10パーセンタイルには、静かな鐘やフェードインが含まれるでしょう。 同時に、最小dB値は針が動く前のレベルになるでしょう。10パーセンタイルより約6～8dB低い値に設定します。ただし、リードインレベルを下回らないようにします。

`top_db`が最も重要ですが、他にも調整できるダイヤルがいくつかあります。

## 仮設のセグメントをトラックに接着する

`librosa.effects.split`は何百もの小さなトラックが生成されます。誤ったトラックマーカーを非表示にします。
45秒未満のトラックは前のトラックと合されます。

``` python
valid_tracks = []
for start_sample, end_sample in intervals:
    duration_sec = (end_sample - start_sample) / sr
    if duration_sec > 45:  
        valid_tracks.append((start_sample, end_sample))
```

実際のトラックマーカーが決まったので、CUEファイルを作成しましょう。

## CUEを作成る

`librosa.samples_to_time`は`librosa.effects.split`のサンプルマーカーを受け取って、開始時刻に変換します。そのあと、CUEシートの形式に合わせるために、開始時刻を75フレーム/秒のグリッドに量子化します。 

CUEシートの形式では「分:秒:フレーム」のようなタイムコードが指定されます。そこで、まずは最小単位であるフレームから始めましょう。秒数に75を掛けて、フレーム総数を求めます。そこから、タイムコードの各要素を算出するのは、進法の変換みたいです。

フレーム総数は10進法ベースです。これを75で割って75進法の計算に変換します。余りがフレーム数になります。商が秒数総数になります。Pythonの`divmod`は商と余りを返します。

タイムコードの秒と分を求めるには、60進法に変換します。秒数総数を60で割ります。余りが秒となり、商が分となります。

そして、開始時刻を1秒戻します。針が落ちる音を聞き逃さないようにし、クリッピングを防ぐためです。

``` python
cue_lines = [f'FILE "{MASTER_VINYL}" BINARY']

for i, (start_sample, end_sample) in enumerate(valid_tracks):
    raw_seconds = librosa.samples_to_time(start_sample, sr=16000).item()

    # 音響の開始位置を処理し、浮動小数点数を整数に変換します。
    total_frames = max(0, int(round(raw_seconds * 75)) - 75)

    total_seconds, frames  = divmod(total_frames, 75)
    minutes, seconds = divmod(total_seconds, 60)
    
    timestamp = f"{minutes:02d}:{seconds:02d}:{frames:02d}"

    cue_lines.append(f'  TRACK {i+1:02d} AUDIO')
    cue_lines.append(f'    TITLE "Track {i+1:02d}"')
    cue_lines.append(f'    INDEX 01 {timestamp}')

with open(f"{MASTER_VINYL}.cue", "w", encoding="utf-8") as f:
    f.write("\n".join(cue_lines))
```

CUEをfoobar2000などに使えます。

CUEファイルの最上位レベルで「TITLE」および「PERFORMER」フィールドを設定しました。別なフィールドがあります。例えば、TRACKのレベルで、「INDEX 00」のフィールドを設定することができます。CDプレーヤーと同じように-0:03みたいマイナスからゼロまでカウントダウンします 💿。

ffmpegとlibrosaは、最初は敷居が高く感じました。分析のためにDSFファイルをダウンサンプリングしたり、無音部分からオーディオを抽出したり、CUEシートのタイムコードを生成するしたりすることは、あまり「基本」とは言えません。
どちらかといえば、「ダクトテープ」に近いでしょう。とはいえ、他人の手による「クリエイティブなダクトテープの使い方」を目にすることは、日常の解像度を上げてくれます。
