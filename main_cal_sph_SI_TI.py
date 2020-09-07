import os
import numpy as np
from math import floor
from math import ceil
from math import atan2, pi, cos
import cv2
import time
import _thread
import sys


video_filename = sys.argv[1]  # video path
save_path = sys.argv[2]  # save folder path

s_x = np.array([[-1, 0, 1],
                [-2, 0, 2],
                [-1, 0, 1]])
s_y = np.array([[1, 2, 1],
                [0, 0, 0],
                [-1, -2, -1]])   # Sobel kernel


def patchSph(img, phi0, theta0, window_size, pix_angle, width, height):
    phi = np.zeros((window_size, window_size), dtype=float)
    theta = np.zeros((window_size, window_size), dtype=float)
    u_w = np.zeros((window_size, window_size), dtype=float)
    v_w = np.zeros((window_size, window_size), dtype=float)
    M_w = np.zeros((window_size, window_size), dtype=float)
    N_w = np.zeros((window_size, window_size), dtype=float)
    P_w = np.zeros((window_size, window_size), dtype=float)
    for i in range(window_size):
        for j in range(window_size):
            phi[i, j] = phi0 + (i+1 - ceil(window_size / 2)) * pix_angle
            theta[i, j] = theta0 + (j+1 - ceil(window_size / 2)) * pix_angle
            if phi[i, j] > 180:
                phi[i, j] = phi[i, j] - 2 * 180
            elif phi[i, j] < -180:
                phi[i, j] = phi[i, j] + 2 * 180

            if theta[i, j] > 180/2:
                theta[i, j] = 180-theta[i, j]
            elif theta[i, j] < -180/2:
                theta[i, j] = -180 - theta[i, j]

    u_w = phi/(2*180)+0.5
    v_w = 0.5 - theta / 180
    N_w = np.round(width * u_w + 0.5)-1
    M_w = np.round(height * v_w + 0.5)-1

    for i in range(window_size):
        for j in range(window_size):
            P_w[i, j] = img[int(M_w[i, j]), int(N_w[i, j])]
    return P_w


def getSiFeature(frame):
    (height, width) = frame.shape
    weight = np.zeros((height, width), dtype=float)
    for i in range(height):
        weight[i, :] = cos(((i + 1 + 0.5 - (height / 2)) * pi) / height)

    pix_angle = (2*180)/width
    u = np.zeros((height, width), dtype=float)
    v = np.zeros((height, width), dtype=float)
    sobel_h = np.zeros((height, width), dtype=float)
    sobel_v = np.zeros((height, width), dtype=float)
    for n in range(width):
        u[:, n] = (n + 1 - 0.5) / width
    for m in range(height):
        v[m, :] = (m + 1 - 0.5) / height

    for m in range(height):
        TimeStamp = time.time()
        for n in range(width):
            phi0 = 2 * 180 * (u[m, n] - 0.5)
            theta0 = 180 * (0.5 - v[m, n])
            P_w = patchSph(frame, phi0, theta0, 3, pix_angle, width, height)
            sob_x = sum(sum(P_w * s_x))
            sob_y = sum(sum(P_w * s_y))
            sobel_h[m, n] = sob_x
            sobel_v[m, n] = sob_y
        # print("Line", m, "Time Cost", time.time()-TimeStamp, "s.")
    SobelTotal = np.sqrt(sobel_v ** 2 + sobel_h ** 2)
    Sobel_mean_w = sum(sum(SobelTotal * weight)) / sum(sum(weight))
    SI_frame_w = np.sqrt(
        sum(sum((SobelTotal * weight - Sobel_mean_w) ** 2)) / sum(sum(weight)))
    return SI_frame_w


def getTiFeature(prev_frame, frame):
    (height, width) = frame.shape
    weight = np.zeros((height, width), dtype=float)
    for i in range(height):
        weight[i, :] = cos(((i + 1 + 0.5 - (height / 2)) * pi) / height)
    pix_dif = abs(frame - prev_frame)
    pix_dif_mean = sum(sum(pix_dif * weight)) / sum(sum(weight))
    TI_frame_w = np.sqrt(
        sum(sum((pix_dif * weight - pix_dif_mean) ** 2)) / sum(sum(weight)))
    return TI_frame_w


def colorCVT(frame):
    B = frame[:, :, 0]
    G = frame[:, :, 1]
    R = frame[:, :, 2]
    Gray = R * 0.299 + G * 0.587 + B * 0.114
    return Gray


if __name__ == '__main__':
    cap = cv2.VideoCapture(video_filename)
    start_index = 0
    end_index = int(cap.get(7))
    frameIndex = 0
    save_video_filename = video_filename.split(
        "/")[-1].split(".")[0].split("_")[0]
    resolution = video_filename.split(
        "/")[-1].split(".")[0].split("_")[1].split("x")
    width = int(resolution[0])
    height = int(resolution[1])
    prevFrame = np.zeros((height, width), dtype=float)
    currFrame = np.zeros((height, width), dtype=float)
    frame = np.zeros((height, width), dtype=float)
    print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
          "Filename", save_video_filename)
    file_handle = open(os.path.join(
        save_path, save_video_filename + '.txt'), mode='w')
    cap.set(cv2.CAP_PROP_POS_FRAMES, start_index)
    frameIndex = start_index


    while cap.isOpened() and frameIndex < end_index:
        ret, frame = cap.read()
        currFrame = colorCVT(frame)
        si = getSiFeature(currFrame)
        if prevFrame.any() != 0:
            ti = getTiFeature(prevFrame, currFrame)
        else:
            ti = 0
        file_handle.write("Frame Index " + str(frameIndex) +
                          " SI " + str(si) + " TI " + str(ti) + ".\n")
        print(time.strftime("%Y-%m-%d %H:%M:%S", time.localtime()),
              "Frame Index", frameIndex, "SI", si, "TI", ti, ".")
        prevFrame = currFrame
        frameIndex += 1

    file_handle.close()
