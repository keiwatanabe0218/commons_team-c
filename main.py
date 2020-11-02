from modules.servo import ServoMotor
from modules.mic import Mic
from modules.camera import  Camera
from modules.vector import vector_to_value, convert_to_servo_value
import random, time
import numpy as np

if __name__ == "__main__":

    # Camera
    path = "./modules/data/shape_predictor_68_face_landmarks.dat"
    cam0 = Camera(0, path)
    cam1 = Camera(2, path)
    cams = [cam0, cam1]

    # Mic
    mic0=Mic(0)
    mic1=Mic(2)
    mics = [mic0, mic1]
    sound_level = 0
    level_count = 0
    level_count_limit = 10

    # Servo
    servoMotors = []
    servoMotors.append(ServoMotor(Channel=3, ZeroOffset=0))
    servoMotors.append(ServoMotor(Channel=0, ZeroOffset=0))
    servoMotors.append(ServoMotor(Channel=1, ZeroOffset=0))
    servoMotors.append(ServoMotor(Channel=2, ZeroOffset=0))
    # intialize servo angle
    for i,servoMotor in enumerate(servoMotors):
        servoMotor.setAngle(180)

    # vector
    index = 0
    xy_old_min = -20
    xy_old_max = 20
    xy_new_min = -20
    xy_new_max = 20
    yz_old_min = -20
    yz_old_max = 20
    yz_new_min = -20
    yz_new_max = 20
    srf_vectors0= [np.array([-192.050001,695.041296,2.633177]), np.array([-41.198416,700.542839,123.918817]),
        np.array([154.810608,717.849009,44.629635]), np.array([277.317012,689.956832,74.136585])]
    srf_vectors1 = [np.array([-192.050001,-704.958704,2.633177]), np.array([-41.198416,-699.457161,123.918817]),
        np.array([154.810608,-682.150991,44.629635]), np.array([277.317012,-710.043168,74.136585])]


    cams[0].srf_vectors = srf_vectors0
    cams[1].srf_vectors = srf_vectors1

    range_min = 180
    range_max = 30
    threshold = 0.1
    range_max_th = 0

    # initialize cams factor
    cams[0].factor = [0 for i in range(len(cams[0].srf_vectors))]

    cams[1].factor = [0 for i in range(len(cams[1].srf_vectors))]



    while True:
        faces = []
        try:
            # mic
            for mic in mics:
                mic.level = mic.record()
            max_level = max([mic.level for mic in mics])
            if max_level < threshold:
                level_count += 1
                if level_count > level_count_limit:
                    sound_level = max_level
                else:
                    pass
            else:
                level_count = 0
                sound_level = max_level
            # camera
            for cam in cams:
                cam.min_difs = []
                cam.max_difs = []

                face = cam.get_angle()
                if face is not None:
                    cam.none_count = 0
                    cam.is_none = False
                    xy = face["yaw"]
                    yz = face["pitch"]
                    cam.min_difs, cam.max_difs, cam.factor = vector_to_value(cam.id, cam.srf_vectors, xy, yz, xy_old_min, xy_old_max, xy_new_min, xy_new_max, yz_old_min, yz_old_max, yz_new_min, yz_new_max)
                    # print(cam.id, cam.factor)
                else:
                    cam.is_none = True
                    cam.none_count += 1
            # Noneがどちらも5回連続したら
            if cams[0].none_count > 5 and cams[1].none_count > 5:
                factor_a = [0 for i in range(len(cams[0].srf_vectors))]
                factor_b = [0 for i in range(len(cams[1].srf_vectors))]
                # cams[1].none_count = 0
            # cam0のNoneが５回連続したら
            elif cams[0].none_count > 5:
                factor_a = cams[1].factor
                factor_b = cams[1].factor
            elif cams[1].none_count > 5:
                factor_a = cams[0].factor
                factor_b = cams[0].factor
            # とっちも認識してないのが5回以内だったら
            else:
                factor_a = cams[0].factor
                factor_b = cams[1].factor
            # # どっちも認識してる場合
            # elif not(cams[0].is_none) and not(cams[1].is_none):
            #     factor_a = cams[0].factor
            #     factor_b = cams[1].factor
            # # cam0だけ認識してる場合
            # elif not(cams[0].is_none) and cams[1].is_none:
            #     factor_a = cams[0].factor
            #     factor_b = cams[0].factor
            # # cam1だけ認識してる場合
            # elif cams[0].is_none and not(cams[1].is_none):
            #     factor_a = cams[1].factor
            #     factor_b = cams[1].factor
            new_factor_remap = convert_to_servo_value(factor_a, factor_b, range_min, range_max, threshold, range_max_th, sound_level)
            print([cam.none_count for cam in cams], new_factor_remap, max_level,sound_level, level_count)
            # calculation

            # servo
            for i,servoMotor in enumerate(servoMotors):
                if i==3:
                    servoMotor.setAngle(new_factor_remap[i])
            #     print("Moved")
            time.sleep(0.1)
        except KeyboardInterrupt:   # exceptに例外処理を書く
            for i,servoMotor in enumerate(servoMotors):
                servoMotor.setAngle(180)
            print('stop!')
            mic0.stop_recording()
            break
