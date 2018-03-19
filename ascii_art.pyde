import sys

from string import printable, whitespace
from random import choice

BASE_FONT = 10
IMGNAME = "shimmi.jpg"

OUT_FILE = open("shimmi.txt", "w") #sys.stdout

EXEC_PER_FRAME = 100

def gen_chars():
    intensity_lookup = []

    for ch in (set(printable) - set(whitespace)) | {" "}:
        char_graphic = createGraphics(chwidth, BASE_FONT)
        char_graphic.beginDraw()
        char_graphic.textFont(f)
        char_graphic.background(0)
        char_graphic.fill(255)
        char_graphic.text(ch, 0, 12)
        char_graphic.endDraw()
        
        char_graphic.loadPixels()
        intensity = sum(map(brightness, char_graphic.pixels)) / float(chwidth * BASE_FONT)
        char_graphic.updatePixels()
        
        intensity_lookup.append((intensity, char_graphic, ch))

    intensity_lookup.sort()
    return intensity_lookup

def draw_image():
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
                if i > intensity * intensity_lookup[-1][0] / 255.0:
                    break

            image(ch, x * scalefac, y * scalefac)
            OUT_FILE.write(chv)
            yield

        OUT_FILE.write("\n")

def setup():
    global intensity_lookup, f, chwidth, drawer

    size(1280, 720)    
    f = createFont("courier", BASE_FONT, True)
    chwidth = int(textWidth("x"))

    intensity_lookup = gen_chars()

    drawer = draw_image()

def draw():
    for _ in range(EXEC_PER_FRAME):
        try:
            next(drawer)
        except StopIteration:
            break