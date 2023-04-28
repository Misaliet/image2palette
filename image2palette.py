import sys, getopt
import os
import numpy as np
import cv2
import extcolors
import math


def is_sqr(n):
    a = int(math.sqrt(n))
    return a * a == n

def extract_color(path, tolerance, limit):
    df_rgb = []
    colors = extcolors.extract_from_path(path, tolerance, limit)
    colors_pre_list = str(colors).replace('([(','').split(', (')[0:-1]
    df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
    # make sure
    while len(df_rgb) < limit-1:
        if tolerance >= 1:
            tolerance -= 1
            colors = extcolors.extract_from_path(path, tolerance, limit)
            colors_pre_list = str(colors).replace('([(','').split(', (')[0:-1]
            df_rgb = [i.split('), ')[0] + ')' for i in colors_pre_list]
        else:
            print("cannot find " + str(limit) + " colors with tolerance=0.")
            sys.exit()

    print("tolerance change to: " + str(tolerance))
    df_percent = [i.split('), ')[1].replace(')','') for i in colors_pre_list]

    return df_rgb, df_percent

def save_palette(rgb_list, percent_list, img_size, limit, path):
    # TODO: use percent_list to change color patch size
    tgt = np.zeros((img_size, img_size, 3))
    slice_number = int(math.sqrt(limit-1))
    patch_size = int(img_size / slice_number)
    k = 0
    for i in range(0, slice_number):
        for j in range(0, slice_number):
            tgt[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)*patch_size, 0] = int(rgb_list[k][1:-1].split(',')[0])
            tgt[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)*patch_size, 1] = int(rgb_list[k][1:-1].split(',')[1])
            tgt[i*patch_size:(i+1)*patch_size, j*patch_size:(j+1)*patch_size, 2] = int(rgb_list[k][1:-1].split(',')[2])
            k += 1

    cv2.imwrite(path, tgt)

def main(args):
    input_path = args[0]
    output_path = args[1]
    tolerance = 5
    limit = 17
    if len(args) > 2:
        tolerance = int(args[2])
    if len(args) > 3:
        limit = int(args[3])
        if not is_sqr(limit-1):
            print("The limit number should be a number of squares plus 1 like 4(2x2)+1, 9(3x3)+1, and so on.")
            sys.exit()
    
    rgb_list, percent_list = extract_color(input_path, tolerance, limit)

    img_size = cv2.imread(input_path).shape[0]
    save_palette(rgb_list, percent_list, img_size, limit, output_path)

    

if __name__ == "__main__":
    # print(len(sys.argv))
    main(sys.argv[1:])