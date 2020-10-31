# 環境構築
## Python
Python3.7.3をインストール
### 仮想環境作成
```bash
python -m venv env
```
### 仮想環境のアクティベート
```bash
source env/bin/activate
```
### ライブラリインストール
```Python
pip install -m requirements.txt
```
## 顔認識
- 参考記事
https://qiita.com/oozzZZZZ/items/1e68a7572bc5736d474e
- 顔認識学習モデル
http://dlib.net/files/shape_predictor_68_face_landmarks.dat.bz2
## 音声認識
- 参考記事
https://qiita.com/mix_dvd/items/adce7636e2ab33b25208
# Run
## Raspberry Piにアクセス
同じWiFiにアクセスしている必要あり
```bash
ssh pi@raspberrypi.local
```
```
password: corona
```
## 仮想環境のアクティベート
```bash
source env/bin/activate
```
## ファイルの場所に移動
```bash
cd dev/commons
```
## PythonファイルをRUN
```bash
python main.py
```
