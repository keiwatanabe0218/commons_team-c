import cv2 #OpenCV:画像処理系ライブラリ
import dlib #機械学習系ライブラリ
import imutils #OpenCVの補助
from imutils import face_utils
import numpy as np

class Camera:
    def __init__(self, id, path):
        # VideoCapture オブジェクトを取得します
        self.id = id
        DEVICE_ID = self.id #ID 0は標準web cam
        self.capture = cv2.VideoCapture(DEVICE_ID)#dlibの学習済みデータの読み込み
        predictor_path = path

        self.detector = dlib.get_frontal_face_detector() #顔検出器の呼び出し。ただ顔だけを検出する。
        self.predictor = dlib.shape_predictor(predictor_path) #顔から目鼻などランドマークを出力する

        self.max_difs = []
        self.min_difs = []
        self.srf_vectors = []
        self.factor = []
        self.none_count = 0
        self.is_none = True
    def get_angle(self):
        ret, frame = self.capture.read() #カメラからキャプチャしてframeに１コマ分の画像データを入れる

        frame = imutils.resize(frame, width=200) #frameの画像の表示サイズを整える
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY) #gray scaleに変換する
        rects = self.detector(gray, 0) #grayから顔を検出
        image_points = None

        for rect in rects:
            shape = self.predictor(gray, rect)
            shape = face_utils.shape_to_np(shape)

            for (x, y) in shape: #顔全体の68箇所のランドマークをプロット
                cv2.circle(frame, (x, y), 1, (255, 255, 255), -1)

            image_points = np.array([
                    tuple(shape[30]),#鼻頭
                    tuple(shape[21]),
                    tuple(shape[22]),
                    tuple(shape[39]),
                    tuple(shape[42]),
                    tuple(shape[31]),
                    tuple(shape[35]),
                    tuple(shape[48]),
                    tuple(shape[54]),
                    tuple(shape[57]),
                    tuple(shape[8]),
                    ],dtype='double')

        if len(rects) > 0:
            model_points = np.array([
                    (0.0,0.0,0.0), # 30
                    (-30.0,-125.0,-30.0), # 21
                    (30.0,-125.0,-30.0), # 22
                    (-60.0,-70.0,-60.0), # 39
                    (60.0,-70.0,-60.0), # 42
                    (-40.0,40.0,-50.0), # 31
                    (40.0,40.0,-50.0), # 35
                    (-70.0,130.0,-100.0), # 48
                    (70.0,130.0,-100.0), # 54
                    (0.0,158.0,-10.0), # 57
                    (0.0,250.0,-50.0) # 8
                    ])

            size = frame.shape

            focal_length = size[1]
            center = (size[1] // 2, size[0] // 2) #顔の中心座標

            camera_matrix = np.array([
                [focal_length, 0, center[0]],
                [0, focal_length, center[1]],
                [0, 0, 1]
            ], dtype='double')

            dist_coeffs = np.zeros((4, 1))

            (success, rotation_vector, translation_vector) = cv2.solvePnP(model_points, image_points, camera_matrix,
                                                                          dist_coeffs, flags=cv2.SOLVEPNP_ITERATIVE)
            #回転行列とヤコビアン
            (rotation_matrix, jacobian) = cv2.Rodrigues(rotation_vector)
            mat = np.hstack((rotation_matrix, translation_vector))

            #yaw,pitch,rollの取り出し
            (_, _, _, _, _, _, eulerAngles) = cv2.decomposeProjectionMatrix(mat)
            yaw = eulerAngles[1]
            pitch = eulerAngles[0]
            roll = eulerAngles[2]
            return {"yaw":int(yaw),"pitch":int(pitch),"roll":int(roll) }

if __name__ == "__main__":
    # Camera
    path = "./data/shape_predictor_68_face_landmarks.dat"
    cam0 = Camera(0, path)
    cam1 = Camera(2, path)
    cams = [cam0, cam1]
    while True:
        try:
            for cam in cams:
                face = cam.get_angle()
                if face is not None:
                    xy = face["yaw"]
                    yz = face["pitch"]
                    print(cam.id, xy, yz)
        except KeyboardInterrupt:   # exceptに例外処理を書く
            print('stop!')
            break
