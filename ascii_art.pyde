import sys

from string import printable, whitespace
from random import choice

BASE_FONT = 10
IMGNAME = "shimmi.jpg"

OUT_FILE = sys.stdout

EXEC_PER_FRAME = 100

BIAS_EXP = 0.7

def gen_chars():
    intensity_lookup = []

    for ch in (set(printable) - set(whitespace)) | {" "}:
        char_graphic = createGraphics(chwidth, BASE_FONT * 2)
        char_graphic.beginDraw()
        char_graphic.textFont(f)
        char_graphic.fill(255)
        char_graphic.text(ch, 0, BASE_FONT)
        char_graphic.endDraw()
        
        char_graphic.loadPixels()
        intensity = sum(map(brightness, char_graphic.pixels)) / float(chwidth * BASE_FONT)
        char_graphic.updatePixels()
        
        intensity_lookup.append([intensity, char_graphic, ch])

    intensity_lookup.sort()
    max_int = intensity_lookup[-1][0]
    for data in intensity_lookup:
        data[0] /= max_int
        data[0] **= BIAS_EXP
    
    return intensity_lookup

def draw_image():
    current_txt = ""
    img = loadImage(IMGNAME)
    img.loadPixels()

    scalefac = min(height / float(img.height), width / float(img.width))

    img_x = int(chwidth / scalefac)
    img_y = int(BASE_FONT / scalefac)

    for y in range(0, img.height - img_y, img_y):
        for x in range(0, img.width - img_x, img_x):
            intensity = (sum(brightness(img.pixels[(y + yd) * img.width + x + xd])
                                            for yd in range(img_y)
                                            for xd in range(img_x))
                        / float(img_x * img_y))

            for i, ch, chv in intensity_lookup:
                if i > intensity / 255.0:
                    break

            current_txt += chv
            yield current_txt
        current_txt += "\n"
    yield current_txt

def setup():
    global intensity_lookup, f, chwidth, drawer
    size(1280, 720)    
    background(0)
    fill(255)
    f = createFont("courier", BASE_FONT, True)
    textFont(f)
    chwidth = int(textWidth("x"))

    intensity_lookup = gen_chars()

    drawer = draw_image()

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