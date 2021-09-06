#!/usr/bin/env python3

import random
import string
from PIL import Image, ImageDraw


def set_dimentions(width=600, height=600):
    '''Set the width and height of the square'''

    return (height, width)


def random_color():
    '''Select from the 12 main RGB colors'''

    rgb_colors = ['#FF0000', '#FF8000', '#FFFF00', '#80FF00',
                  '#00FF00', '#00FF80', '#00FFFF', '#0080FF',
                  '#0000FF', '#8000FF', '#FF00FF', '#FF0080']

    return random.choice(rgb_colors)


def add_fill_color(color):
    '''Randomly add color to a majority of shapes'''

    add_color = [True, False]
    if random.choices(add_color, weights=(80, 20), k=1)[0]:
        return color
    return None


def create_circle(img):
    '''Create a circle pattern'''

    color = random_color()
    draw = ImageDraw.Draw(img)

    column_1 = [55, 55, 145, 145]
    for item in range(5):
        draw.ellipse((column_1), fill=add_fill_color(color))
        column_1[1] += 100
        column_1[3] += 100

    column_2 = [155, 55, 245, 145]
    for item in range(5):
        draw.ellipse((column_2), fill=add_fill_color(color))
        column_2[1] += 100
        column_2[3] += 100

    column_3 = [255, 55, 345, 145]
    for item in range(5):
        draw.ellipse((column_3), fill=add_fill_color(color))
        column_3[1] += 100
        column_3[3] += 100

    column_4 = [355, 55, 445, 145]
    for item in range(5):
        draw.ellipse((column_4), fill=add_fill_color(color))
        column_4[1] += 100
        column_4[3] += 100

    column_5 = [455, 55, 545, 145]
    for item in range(5):
        draw.ellipse((column_5), fill=add_fill_color(color))
        column_5[1] += 100
        column_5[3] += 100

    return draw


def create_image():
    '''Generate and save the image'''

    img = Image.new(mode='RGB', size=set_dimentions(600, 600),
                    color=(255, 255, 255))
    create_circle(img)

    chars = ''.join(string.ascii_letters)
    filename = ''.join(random.choice(chars) for _ in range(16))
    img.save(f'application/static/images/{filename}.png')
    return f'{filename}.png'
