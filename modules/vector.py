import numpy as np
import math

def remap_number(old_value, old_min, old_max, new_min, new_max):
    old_range = old_max - old_min
    new_range = new_max - new_min
    if old_range != 0:
        new_value = (((old_value - old_min) * new_range) / old_range) + new_min
    else:
        new_value = 0
    return new_value

def vector_angle(vec1, vec2):
    unit_vec1 = unitize_vector(vec1)
    unit_vec2 = unitize_vector(vec2)
    vec_dif = unit_vec1 - unit_vec2
    return np.linalg.norm(vec_dif)

def unitize_vector(vec):
    return (vec / np.linalg.norm(vec))

def vector_to_value(index, srf_vectors, xy, yz, xy_old_min, xy_old_max, xy_new_min, xy_new_max, yz_old_min, yz_old_max, yz_new_min, yz_new_max):
    new_xy = remap_number(xy, xy_old_min, xy_old_max, xy_new_min, xy_new_max)
    new_yz = remap_number(yz, yz_old_min, yz_old_max, yz_new_min, yz_new_max)
    if index == 0:
        vec = np.array([math.sin(math.radians(new_xy)),math.cos(math.radians(new_xy)),math.sin(math.radians(new_yz)) * (math.cos(math.radians(new_xy))/math.cos(math.radians(new_yz)))])
    elif index == 1:
        vec = np.array([-(math.sin(math.radians(new_xy))),-(math.cos(math.radians(new_xy))),math.sin(math.radians(new_yz)) * (math.cos(math.radians(new_xy))/math.cos(math.radians(new_yz)))])
    else:
        return None, None, None
    vec = unitize_vector(vec)
    difs = []
    for srf_v in srf_vectors:
        difs.append(vector_angle(vec, srf_v))
    max_difs = max(difs)
    min_difs = min(difs)
    difs_remap = list(map(lambda x: remap_number(x, min_difs, max_difs, 1, 0), difs))

    # print(difs_remap)
    return min_difs, max_difs, difs_remap

def convert_to_servo_value(factor_a, factor_b, range_min, range_max, threshold, range_max_th, sound_level):
    new_factor = [factor_a[i] + factor_b[i] for i in range(len(factor_a))]
    mx = max(new_factor)
    mn = min(new_factor)

    if sound_level > threshold:
        range_max = range_max_th

    new_factor_remap = list(map(lambda x: remap_number(x, mn, mx, range_min, range_max), new_factor))
    return new_factor_remap

if __name__ == "__main__":
    index = 0
    xy = -12
    yz = -3
    xy_old_min = -20
    xy_old_max = 20
    xy_new_min = -20
    xy_new_max = 20
    yz_old_min = -20
    yz_old_max = 20
    yz_new_min = -20
    yz_new_max = 20
    srf_vectors = [np.array([-192.050001,695.041296,2.633177]), np.array([-41.198416,700.542839,123.918817]),
    np.array([154.810608,717.849009,44.629635]), np.array([277.317012,689.956832,74.136585])]


    min_difs, max_difs, factor_a = vector_to_value(index, srf_vectors, xy, yz, xy_old_min, xy_old_max, xy_new_min, xy_new_max, yz_old_min, yz_old_max, yz_new_min, yz_new_max)
    # print(factor_a)

    index = 1
    xy = -1
    yz = 9
    xy_old_min = -20
    xy_old_max = 20
    xy_new_min = -20
    xy_new_max = 20
    yz_old_min = -20
    yz_old_max = 20
    yz_new_min = -20
    yz_new_max = 20
    srf_vectors = [np.array([-192.050001,-704.958704,2.633177]), np.array([-41.198416,-699.457161,123.918817]),
    np.array([154.810608,-682.150991,44.629635]), np.array([277.317012,-710.043168,74.136585])]

    min_difs, max_difs, factor_b = vector_to_value(index, srf_vectors, xy, yz, xy_old_min, xy_old_max, xy_new_min, xy_new_max, yz_old_min, yz_old_max, yz_new_min, yz_new_max)
    # print(factor_b)

    range_min = 0
    range_max = 120
    sound_level = 70
    threshold = 80
    range_max_th = 180
    new_factor_remap = convert_to_servo_value(factor_a, factor_b, range_min, range_max, threshold, range_max_th, sound_level)

    print(new_factor_remap)
