# -*- coding: utf-8 -*-
import os
import argparse
from PIL import Image
from PIL import ImageFilter

f = open("399chars.txt", "r")

def crop_image(src_dir, dst_dir):
    if not os.path.exists(dst_dir):
        os.makedirs(dst_dir)
    for page in range(1,4):
        img = Image.open( src_dir + "/" + str(page) +"-crop.png").convert('L')
        img = img.point(lambda x : 0 if x < 192 else x, 'L')
        img = img.point(lambda x : 255 if x > 192 else x, 'L')
        img = img.filter(ImageFilter.MedianFilter)
        width, height = img.size
        cell_width = width/cols
        cell_height = height/rows
        header_offset = height/rows * header_ratio
        width_margin = cell_width * 0.05
        height_margin = cell_height * 0.05

        for j in range(0,rows):
            for i in range(0,cols):
                left = i * cell_width
                upper = j * cell_height + header_offset
                right = left + cell_width
                lower = (j+1) * cell_height

                left += width_margin
                upper += height_margin
                right -= width_margin
                lower -= height_margin

                crop_width = right - left
                crop_height = lower - upper

                if crop_width > crop_height:
                    right = left + crop_height
                else:
                    lower = upper + crop_width

                code = f.readline()
                #  print(code.strip())
                if not code:
                    break
                else:
                    name = dst_dir + "/uni" + code.strip() + ".png"
                    #  print(name)
                    cropped_image = img.crop((left, upper, right, lower))
                    cropped_image = cropped_image.resize((128,128), Image.LANCZOS)
                    cropped_image.save(name)
        print("Processed page " + str(page))

parser = argparse.ArgumentParser(description='Crop scanned images to character images')
parser.add_argument('--src_dir', dest='src_dir', required=True, help='directory to read scanned images')
parser.add_argument('--dst_dir', dest='dst_dir', required=True, help='directory to save character images')

args = parser.parse_args()

if __name__ == "__main__":
    rows = 12
    cols = 12
    header_ratio = 16.5/(16.5+42)
    crop_image(args.src_dir, args.dst_dir)
