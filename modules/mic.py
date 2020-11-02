import numpy as np
import threading
import pyaudio
import threading
import time

class Mic:
    def __init__(self, index):
        self.id = index

        # 音データフォーマット
        self.chunk = 1024
        FORMAT = pyaudio.paInt16
        CHANNELS = 1
        RATE = 16000
        RECORD_SECONDS = 1
        input_device_index=index

        # 閾値
        self.threshold = 0.01
        # 音量
        self.level = 0

        # 音の取込開始
        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(format = FORMAT,
            channels = CHANNELS,
            rate = RATE,
            input = True,
            frames_per_buffer = self.chunk,
            input_device_index = input_device_index
        )


    def record(self):

        # 音データの取得
        data = self.stream.read(self.chunk,exception_on_overflow = False)
        # ndarrayに変換
        x = np.frombuffer(data, dtype="int16") / 32768.0

        # 閾値以上の場合はファイルに保存
        # if x.max() > self.threshold:
        #     print(x.max())
        return x.max()

    def stop_recording(self):
        self.stream.close()
        self.p.terminate()

if __name__ == "__main__":
    mic = Mic(2)
    while True:
        try:
            print(mic.record())
            time.sleep(0.3)
        except KeyboardInterrupt:
            mic.stop_recording()
            print("stop")
