import numpy as np
import threading
import pyaudio
import threading
import time
# import matplotlib.pyplot as plt

class Mic2:
    def __init__(self, index):
        self.chunk = 1024
        self.FORMAT = pyaudio.paInt16
        self.CHANNELS = 1
        #サンプリングレート、マイク性能に依存
        self.RATE = 16000
        self.RECORD_SECONDS = 1
        #pyaudio
        self.audio = pyaudio.PyAudio()
        #plot time
        self.plottime = 100
        self.loopcounter = 0
        self.data_rms = []
        self.input_device_index=index



        #マイクからデータ取得
        self.stream = self.audio.open(  format = self.FORMAT,
                                    channels = self.CHANNELS,
                                    rate = self.RATE,
                                    input = True,
                                    input_device_index = self.input_device_index,
                                    frames_per_buffer = self.chunk)

        self.all = []
        for i in range(0, int(self.RATE / self.chunk * self.RECORD_SECONDS)):
            self.data = self.stream.read(self.chunk)
            self.all.append(self.data)
        self.data = b''.join(self.all)
        self.data=np.frombuffer(self.data, dtype="int16")

        #converting numpy-type-array
        self.np_data=np.array(self.data, dtype = np.float64)

        #downsampling
        self.overhang = len(self.np_data) % 100
        self.down_data=self.np_data[:-self.overhang]
        self.down_data=np.reshape(self.down_data, [int(len(self.down_data)/100),100])
        self.down_data=np.average(self.down_data, 1)

        #RMS calculation
        self.rms=np.sqrt(np.mean(np.square(self.down_data)))
        # print(self.input_device_index, self.rms)
        # self.data_rms.append(self.rms)

        self.stream.close()
        self.loopcounter = self.loopcounter + 1
    def plot_sound(self):
        return self.rms

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
    mic = Mic2(0)
    while True:
        try:
            mic.record()
            time.sleep(0.3)
        except KeyboardInterrupt:
            mic.stop_recording()
            print("stop")
