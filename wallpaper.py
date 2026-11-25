import math
import random
import sys
from PIL import Image, ImageDraw

WIDTH, HEIGHT = 2560, 1440

seed = int(sys.argv[1]) if len(sys.argv) > 1 else random.randrange(1_000_000)
rng = random.Random(seed)
print("seed:", seed)

hue = rng.randrange(360)

def colour(hue_shift, saturation, lightness):
    return f"hsl({(hue + hue_shift) % 360}, {saturation}%, {lightness}%)"

image = Image.new("RGB", (WIDTH, HEIGHT))
draw = ImageDraw.Draw(image)

for y in range(HEIGHT):
    t = y / HEIGHT
    draw.line([(0, y), (WIDTH, y)], fill=colour(40 * t, 70, 88 - 30 * t))

sun_x = rng.randrange(WIDTH // 5, WIDTH * 4 // 5)
sun_y = rng.randrange(HEIGHT // 6, HEIGHT // 2)
r = rng.randrange(80, 200)
draw.ellipse([sun_x - r, sun_y - r, sun_x + r, sun_y + r], fill=colour(20, 90, 94))

LAYERS = 6

for layer in range(LAYERS):
    t = layer / (LAYERS - 1)
    base = HEIGHT * (0.5 + 0.4 * t)
    waves = [
        (rng.uniform(20, 90) / (i + 1), rng.uniform(1, 3) * (i + 1), rng.uniform(0, math.tau))
        for i in range(5)
    ]

    ridge = []
    for x in range(0, WIDTH + 8, 8):
        height = sum(size * math.sin(x / WIDTH * math.tau * speed + shift)
                     for size, speed, shift in waves)
        ridge.append((x, base + height))

    draw.polygon(ridge + [(WIDTH, HEIGHT), (0, HEIGHT)], fill=colour(40, 45, 62 - 48 * t))

image.save(f"wallpaper-{seed}.png")