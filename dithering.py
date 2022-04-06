from PIL import Image, ImageDraw
from math import sqrt
from time import time
import sys
from Color import Color
from utils import *

# colors = [
#     Color(0, 0, 0),
#     Color(255, 255, 255)
# ]

"""todo: read color palette from json files + convert hex to rgb"""
colors = [
    Color(190, 0, 57),
    Color(255, 69, 0),
    Color(255, 168, 0),
    Color(255, 214, 53),
    Color(0, 163, 104),
    Color(0, 204, 120),
    Color(126, 237, 86),
    Color(0, 117, 111),
    Color(0, 158, 170),
    Color(36, 80, 164),
    Color(54, 144, 234),
    Color(81, 233, 244),
    Color(73, 58, 193),
    Color(106, 92, 255),
    Color(129, 30, 159),
    Color(180, 74, 192),
    Color(255, 56, 129),
    Color(255, 153, 170),
    Color(109, 72, 47),
    Color(212, 215, 217),
    Color(156, 105, 38),
    Color(0, 0, 0),
    Color(137, 141, 144),
    Color(255, 255, 255),
]


def render(image: Image):
    """put all pixel data inside a 2d array for faster operations"""

    for y in range(image.height):
        for x in range(image.width):
            pixel = image.getpixel((x, y))
            color = Color(pixel[0], pixel[1], pixel[2])
            new_color = nearest_color(color)
            distance_error = Color(color.r - new_color.r,
                                   color.g - new_color.g, color.b - new_color.b)

            draw = ImageDraw.Draw(image)
            draw.point((x, y), (new_color.r, new_color.g, new_color.b))

            if (x+1 < image.width and y+1 < image.height):
                """ugly Floyd–Steinberg dithering

                https://en.wikipedia.org/wiki/Floyd%E2%80%93Steinberg_dithering

                todo: find a way to do each step on one line
                """
                temp_color = color_addition(
                    pixel_to_color(image.getpixel((x+1, y))),
                    color_multiplication(7/16, distance_error))

                draw.point((x+1, y), (temp_color.r,
                           temp_color.g, temp_color.b))

                temp_color = color_addition(
                    pixel_to_color(image.getpixel((x-1, y+1))),
                    color_multiplication(3/16, distance_error))

                draw.point((x-1, y+1), (temp_color.r,
                           temp_color.g, temp_color.b))

                temp_color = color_addition(
                    pixel_to_color(image.getpixel((x, y+1))),
                    color_multiplication(5/16, distance_error))

                draw.point((x, y+1), (temp_color.r,
                           temp_color.g, temp_color.b))

                temp_color = color_addition(
                    pixel_to_color(image.getpixel((x+1, y+1))),
                    color_multiplication(1/16, distance_error))

                draw.point((x+1, y+1), (temp_color.r,
                           temp_color.g, temp_color.b))

    image.save("./out/" + str(time()) + ".png")


def nearest_color(old_color: Color):
    """change the current color to the nearest color available"""

    new_color = colors[0]
    min_distance = distance(old_color, colors[0])

    for color in colors:
        new_distance = distance(color, old_color)

        if (new_distance < min_distance):
            new_color = color
            min_distance = new_distance

    return new_color


def distance(first_color: Color, second_color: Color):
    """return the distance between 2 colors"""
    return sqrt((first_color.r - second_color.r) ** 2 + (first_color.g - second_color.g) ** 2 + (first_color.b - second_color.b) ** 2)


def start():
    """render the image with the provided image"""
    try:

        with Image.open(sys.argv[1]) as image:
            data = render(image)

    except IndexError:
        """if an image is not specified return an error"""
        print("Missing argument")


if __name__ == "__main__":
    start()
