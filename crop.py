# -*- coding: utf-8 -*-
from PIL import Image
from PIL import ImageFilter

f = open("random.txt", "r")

rows = 12
cols = 12
header_ratio = 16.5/(16.5+42)

for page in range(1,4):
    img = Image.open(str(page) +"-crop.png").convert('L')
    img = img.point(lambda x : 0 if x < 192 else x, 'L')
    img = img.point(lambda x : 255 if x > 192 else x, 'L')
    img = img.filter(ImageFilter.MedianFilter)
    width, height = img.size
    cell_width = width/cols
    cell_height = height/rows
    header_offset = height/rows * header_ratio
    width_margin = cell_width * 0.05
    height_margin = cell_height * 0.05

    for j in range(0,12):
        for i in range(0,12):
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
            print(code.strip())
            if not code:
                break
            else:
                name = "image/HandWriting/uni" + code.strip() + ".png"
                print(name)
                crop_image = img.crop((left, upper, right, lower))
                crop_image = crop_image.resize((128,128), Image.LANCZOS)
                crop_image.save(name)
