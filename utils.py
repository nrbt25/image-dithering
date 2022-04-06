from Color import Color


def color_addition(first_color: Color, second_color: Color):
    return Color(first_color.r + second_color.r, first_color.g + second_color.g, first_color.b + second_color.b)


def color_multiplication(value: float, color: Color):
    return Color(round(value * color.r), round(value * color.g), round(value * color.b))


def pixel_to_color(pixel):
    return Color(pixel[0], pixel[1], pixel[2])
