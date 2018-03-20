import sys

from string import printable, whitespace
from random import choice

from pprint import pprint

BASE_FONT = 10
IMGNAME = "swan.jpg"

OUT_FILE = sys.stdout

EXEC_PER_FRAME = 100

BIAS_EXP = 1.3

def gen_chars():
    intensity_lookup = []

    for ch in (set(printable) - set(whitespace)) | {" "}:
        char_graphic = createGraphics(int(chwidth), BASE_FONT * 2)
        char_graphic.beginDraw()
        char_graphic.textFont(f)
        char_graphic.fill(255)
        char_graphic.text(ch, 0, BASE_FONT)
        char_graphic.endDraw()
        
        char_graphic.loadPixels()
        intensity = sum(map(brightness, char_graphic.pixels))
        char_graphic.updatePixels()
        
        intensity_lookup.append([intensity, char_graphic, ch])

    intensity_lookup.sort()
    max_int = intensity_lookup[-1][0]
    for data in intensity_lookup:
        data[0] /= max_int
        if data[0] > 0.5:
            data[0] = (data[0] - 0.5) ** BIAS_EXP * 2 ** (BIAS_EXP - 1) + 0.5
        else:
            data[0] = -(0.5 - data[0]) ** BIAS_EXP * 2 ** (BIAS_EXP - 1) + 0.5

    return intensity_lookup

def draw_image():
    current_txt = ""
    img.loadPixels()
    
    scalefac = min(height / float(img.height), width / float(img.width))
    
    img_x = chwidth / scalefac
    img_y = BASE_FONT / scalefac

    y = 0
    while y < img.height - img_y:
        x = 0
        while x < img.width - img_x:
            intensity = (sum(brightness(img.pixels[(int(y) + yd) * img.width + int(x) + xd])
                                            for yd in range(int(img_y))
                                            for xd in range(int(img_x)))
                        / float(img_x * img_y))

            for i, ch, chv in intensity_lookup:
                if i > intensity / 255.0:
                    break

            current_txt += chv
            yield current_txt
            x += img_x
        y += img_y
            
        current_txt += "\n"
    yield current_txt

def setup():
    global intensity_lookup, f, chwidth, drawer, img
    size(1280, 720)
    img = loadImage(IMGNAME)
    fill(255)
    f = createFont("courier", BASE_FONT, True)
    textFont(f)
    chwidth = textWidth("x")
    intensity_lookup = gen_chars()
    drawer = draw_image()
    background(0)

def draw():
    global current_txt
    background(0)
    for _ in range(EXEC_PER_FRAME):
        try:
            current_txt = next(drawer)
        except StopIteration:
            noLoop()
            OUT_FILE.write(current_txt)
            break
    text(current_txt, 0, 0)

def keyPressed():
    if key == " ":
        setup()