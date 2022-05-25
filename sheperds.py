#!/usr/bin/python3
from collections import namedtuple
from wand.color import Color
from wand.image import Image
from wand.display import display
from wand.drawing import Drawing
import math, random, sys

assert(len(sys.argv) >= 3)

Point = namedtuple("Point", ["x", "y", "i", "j"])
n_distortions = int(sys.argv[2])
magnitude = 2  # smaller is bigger
box_size = 2
angle = 45

with Image(filename=sys.argv[1]) as img:
    a, b = img.height, img.width
    c = round(math.sqrt(a**2 + b**2))

    la = (a * (box_size - 1)) // (2 * box_size)
    lb = (b * (box_size - 1)) // (2 * box_size)
    print("offset is:", (la, lb))

    points: "list[Point]" = []
    clamp = lambda x, lim: min(max(round(x), 0), lim)
    for _ in range(n_distortions):
        x = random.randrange(lb, lb + b // box_size)
        y = random.randrange(la, la + a // box_size)
        d = random.randrange(c // magnitude)
        alpha = random.randrange(angle, 360 - angle)
        i = x + d * math.cos(alpha)
        j = y + d * math.sin(alpha)
        point = Point(x, y, clamp(i, b), clamp(j, a))
        points.append(point)

    print(points)

    with Drawing() as draw:
        with Color("red") as color:
            draw.fill_color = color
            for point in points:
                draw.line((point.x, point.y), (point.i, point.j))
            clone = img.clone()
            draw(clone)
            display(clone)

    img.virtual_pixel = "mirror"
    img.artifacts["shepards:power"] = "4.0"
    distortions = sum(points, ())
    img.distort("shepards", distortions)

    display(img)
