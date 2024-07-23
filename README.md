# Ojbect Detction

[![NumPy](https://custom-icon-badges.herokuapp.com/badge/NumPy-9C8AF9.svg?logo=NumPy&logoColor=white)]()
[![Python](https://custom-icon-badges.herokuapp.com/badge/Python-3572A5.svg?logo=Python&logoColor=white)]()
![Static Badge](https://img.shields.io/badge/OpenCV-orange)
![Static Badge](https://img.shields.io/badge/YOLO-skyblue)
![Static Badge](https://img.shields.io/badge/motpy-purple)
![Static Badge](https://img.shields.io/badge/PyYAML-pink)
![Static Badge](https://img.shields.io/badge/ultralytics-lightgreen)
![Static Badge](https://img.shields.io/badge/multiprocessing-yellow)

# Introduction
映像の中にいる人、自動車、自転車を検出して、矩形で囲むシステムとなっている。

バージョンが分かれており、それぞれのバージョンで以下のような機能が追加されている。

`ver1`
- シングルプロセスによる人物検出

`ver2`
- `multiprocessing`による並列処理の追加
- 人物に加えて、自転車、バイク、自動車、バス、トラックを検出の対象に

`ver2.1`
- `motpy`を使用して検出したそれぞれの物体をトラッキングできるように(仮)

## Directories
- `config`: pythonで実行するときの設定ファイル(.yml)を入れる
- `data`: 動画データなどを入れる
- `log`: 処理の内容の出力先
- `outputs`: 処理後の映像の出力先
- `pts`: YOLOの学習済みモデルの保存先
- `util`: 今回のシステムを動かす上で必要なサブシステム

# Quick Start
### 注意点
使用しているPythonのバージョンは3.12.3となっている。

**クローン&必要なライブラリ類のインストール**
```
git clone git@github.com:215725A/object_detection.git
cd object_detection
pip install -r requirements.txt
```

**実行(例)**
実行する際には `config/template.yml`を参考にymlファイルを作成すること。

```
python detect.py -c config/template.yml
```

