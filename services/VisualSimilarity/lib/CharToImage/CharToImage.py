#!/usr/env/bin python
# encoding: utf-8

from PIL import Image, ImageDraw, ImageFont
import os

FONT_SIZE = 40
WIDTH, HEIGHT = 50, 50

def convert(char):
    current_file_path = os.path.dirname(os.path.abspath(__file__))
    ttf_file = os.path.join(current_file_path, 'arial.ttf')

    image = Image.new('L', (WIDTH, HEIGHT), 'white')
    draw = ImageDraw.Draw(image)
    font = ImageFont.truetype(ttf_file, FONT_SIZE)

    w, h = draw.textsize(char, font=font)
    draw.text(((WIDTH - w) / 2, (HEIGHT - FONT_SIZE) / 2), char, font=font, fill='black')
    return image
