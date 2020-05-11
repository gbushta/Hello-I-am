# Write your code here :-)
# pygamer_dancing_fid_rev_1.py
# ** Cleaning up the code.
#
# I am now using Lists (arrays)
# for a few of the variables groups.
# **
# Press Button A to speed up the LEDs cycling.
# Press Button B to slow down the LEDs cycling.
# Press Start to change the color of the LEDs.
# Press Select to change the color of the name, fid.
#
# text_area3 through 5 now handles the name fid.
# Each letter is handled separately.
# You can change it in there.
#
import board
import neopixel
import digitalio
import displayio
import gamepadshift
import array
import math
import random
import audioio
from adafruit_display_text import label
from adafruit_bitmap_font import bitmap_font
from adafruit_display_shapes.rect import Rect

display = board.DISPLAY

FREQUENCY = 2093  # 440 Hz middle 'A'
SAMPLERATE = 2 * FREQUENCY  # 8000 samples/second, recommended!

# Generate one period of sine wav.
length = SAMPLERATE // FREQUENCY
sine_wave = array.array("H", [0] * length)
for irange in range(length):
    sine_wave[irange] = int(math.sin(math.pi * 2 * irange / 18) * (2 ** 15) + 2 ** 15)

# enable the speaker
speaker_enable = digitalio.DigitalInOut(board.SPEAKER_ENABLE)
speaker_enable.direction = digitalio.Direction.OUTPUT
speaker_enable.value = True

audio = audioio.AudioOut(board.A0)
sine_wave_sample = audioio.RawSample(sine_wave)

led = neopixel.NeoPixel(board.NEOPIXEL, 5)
i = 0
led_speed = 200
red = (5, 0, 0)
blue = (0, 0, 5)
yellow = (5, 5, 0)
green = (0, 5, 0)
white = (5, 5, 5)
purple = (5, 0, 5)
pushed = 0
the_color = [red, blue, yellow, green, white, purple]
fid_color = [0xFF0000, 0x0000FF, 0xFFFF00, 0x00FF00, 0xFFFFFF, 0xFF00FF, 0x000000]
myX = 0
myY = 0
ledCheck = 0
ledOn = 0
soundTimer = 0
ledDirection = 1
fid_sine = [0, 1, 3, 4, 4, 5, 4, 4, 3, 1, 0, -1, -3, -4, -4, -5, -4, -4, -3, -1]
fid_count = 0
f_sine_count = 10
i_sine_count = 5
d_sine_count = 0

font2 = bitmap_font.load_font("SourceSerifPro_25.bdf")
font4 = bitmap_font.load_font("SourceSerifPro_52.bdf")
text_area = label.Label(font2, text="Hello", color=0xFFFFFF)
text_area.x = 48
text_area.y = 10
text_area2 = label.Label(font2, text="I am", color=0xFFFF00)
text_area2.x = 53
text_area2.y = 30
text_area3 = label.Label(font4, text="f", color=0xFF0000)
text_area3.x = 45
text_area3.y = 80
text_area4 = label.Label(font4, text="i", color=0xFF0000)
text_area4.x = 70
text_area4.y = 80
text_area5= label.Label(font4, text="d", color=0xFF0000)
text_area5.x = 85
text_area5.y = 80
j = 0
k = 0
my_color = the_color[j]
speedCheck = 10

pad = gamepadshift.GamePadShift(digitalio.DigitalInOut(board.BUTTON_CLOCK),
                   digitalio.DigitalInOut(board.BUTTON_OUT),
				   digitalio.DigitalInOut(board.BUTTON_LATCH))

rect = [0] * 40
slow = [0] * 40

bitmap = displayio.Bitmap(display.width, display.height, 2)
palette = displayio.Palette(2)
palette[0] = 0x000000  # This is the background of the display
palette[1] = 0x8A2BE2  # This is the foreground, Purple

# TileGrid for the bitmap
bitmap_grid = displayio.TileGrid(bitmap, pixel_shader=palette)

rect_back = Rect(0, 0, 160, 128, fill=0x000000)
for irange in range(40):
    rect[irange] = Rect(irange * 4, random.randint(0, 120), 3, 3, fill=0x00FF00)

for irange in range(40):
    slow[irange] = (random.randint(0, 10) * 20) + speedCheck

speed = [0] * 40

# Create a Group to hold the TileGrid
group = displayio.Group(max_size=50)

# Add the TileGrid to the Group
group.append(rect_back)
group.append(text_area)
group.append(text_area2)
group.append(text_area3)
group.append(text_area4)
group.append(text_area5)
for irange in range(40):
    group.append(rect[irange])

# Add the Group to the Display
display.show(group)

while True:
    if ledCheck > led_speed:
        if ledOn == 0:
            led[i] = (my_color)
            ledOn = 1
        else:
            led[i] = (0, 0, 0)
            ledOn = 0
            i += ledDirection
            if i < 1 or i > 3:
                ledDirection *= -1
        ledCheck = 0
    ledCheck += 1

    if pushed == 1:
        soundTimer += 1
        if soundTimer == 300:
            audio.stop()
        pressed = pad.get_pressed()
        if pressed == 0:
            pushed = 0
            audio.stop()

    if pushed == 0:
        pressed = pad.get_pressed()
        if pressed == 0x01:
            led_speed += .05
        if pressed == 0x02:
            led_speed -= .05
        if led_speed > 500:
            led_speed = 500
        if led_speed < 10:
            led_speed = 10
        if pressed == 0x04:
            j += 1
            if j > len(the_color) - 1:
                j = 0
            my_color = the_color[j]
            pushed = 1
            soundTimer = 0
            audio.play(sine_wave_sample, loop=True)
        if pressed == 0x08:
            pushed = 1
            k += 1
            if k > len(fid_color) - 1:
                k = 0
            text_area3.color = fid_color[k]
            text_area4.color = fid_color[k]
            text_area5.color = fid_color[k]
    for irange in range(40):
        speed[irange] += 1

    for irange in range(40):
        if speed[irange] > slow[irange]:
            speed[irange] = 0
            slow[irange] = (random.randint(0, 10) * 20) + speedCheck
            rect[irange].y += 4
            if rect[irange].y > 126:
                rect[irange].y = 0

    fid_count += 1
    if fid_count > 15:
        fid_count = 0
        f_sine_count += 1
        if f_sine_count == len(fid_sine):
            f_sine_count = 0
        text_area3.y = 80 + fid_sine[f_sine_count] * 3
        i_sine_count += 1
        if i_sine_count == len(fid_sine):
            i_sine_count = 0
        text_area4.y = 80 + fid_sine[i_sine_count] * 3
        d_sine_count += 1
        if d_sine_count == len(fid_sine):
            d_sine_count = 0
        text_area5.y = 80 + fid_sine[d_sine_count] * 3