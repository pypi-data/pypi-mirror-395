# import pyzjr.Z as Z
# -i https://pypi.tuna.tsinghua.edu.cn/simple
import numpy as np

def get_color(color_name, to_rgb=False):
    bgr_colors = {
        'blue': (255, 0, 0),
        'green': (0, 255, 0),
        'red': (0, 0, 255),
        "dark_blue": (128, 0, 0),
        'dark_green': (0, 128, 0),
        "dark_red": (0, 0, 128),
        "blue_green": (128, 128, 0),
        'magenta': (255, 0, 255),
        "black": (0, 0, 0),
        "grey": (128, 128, 128),
        "silvery": (192, 192, 192),
        "white": (255, 255, 255),
        "yellow": (0, 255, 255),
        "orange": (0, 97, 255),
        "purple": (255, 0, 255),
        "violet": (240, 32, 160),
        "brown": (19, 69, 139),
        "pink": (203, 192, 255),
    }
    bgr_color = bgr_colors.get(color_name, None)
    if bgr_color is not None and to_rgb:
        return bgr_color[::-1]
    return bgr_color

e = 2.718281828459045
pi = 3.141592653589793
half_pi = pi / 2
double_pi = 2 * pi

NUMPY_DTYPE = {
    np.dtype("uint8"): 255,
    np.dtype("uint16"): 65535,
    np.dtype("uint32"): 4294967295,
    np.dtype("float32"): 1.0,
}

IMG_FORMATS = ('bmp', 'dng', 'jpeg', 'jpg', 'mpo', 'png', 'tif', 'tiff', 'webp', 'pfm')  # include image suffixes
VID_FORMATS = ('asf', 'avi', 'gif', 'm4v', 'mkv', 'mov', 'mp4', 'mpeg', 'mpg', 'ts', 'wmv')  # include video suffixes

# 颜色空间转换
BGR2RGB = 4
BGR2HSV = 40
BGR2GRAY = 6
RGB2GRAY = 7
GRAY2BGR = 8
GRAY2RGB = 8
HSV2BGR = 54
HSV2RGB = 55
RGB2HSV = 41
RGB2BGR = 4

# keyboard
Esc = ESC =  27
Enter = ENTER = 13
Space = 32


# BGR
blue = get_color('blue')
green = get_color('green')
red = get_color('red')
dark_blue = get_color('dark_blue')
dark_green = get_color('dark_green')
dark_red = get_color('dark_red')
blue_green = get_color('blue_green')
magenta = get_color('magenta')
black = get_color('black')
grey = get_color('grey')
silvery = get_color('silvery')
white = get_color('white')
yellow = get_color('yellow')
orange = get_color('orange')
purple = get_color('purple')
violet = get_color('violet')
brown = get_color('brown')
pink = get_color('pink')
# RGB
rgb_blue = get_color('blue', to_rgb=True)
rgb_green = get_color('green', to_rgb=True)
rgb_red = get_color('red', to_rgb=True)
rgb_dark_blue = get_color('dark_blue', to_rgb=True)
rgb_dark_green = get_color('dark_green', to_rgb=True)
rgb_dark_red = get_color('dark_red', to_rgb=True)
rgb_blue_green = get_color('blue_green', to_rgb=True)
rgb_magenta = get_color('magenta', to_rgb=True)
rgb_black = get_color('black', to_rgb=True)
rgb_grey = get_color('grey', to_rgb=True)
rgb_silvery = get_color('silvery', to_rgb=True)
rgb_white = get_color('white', to_rgb=True)
rgb_yellow = get_color('yellow', to_rgb=True)
rgb_orange = get_color('orange', to_rgb=True)
rgb_purple = get_color('purple', to_rgb=True)
rgb_violet = get_color('violet', to_rgb=True)
rgb_brown = get_color('brown', to_rgb=True)
rgb_pink = get_color('pink', to_rgb=True)


if __name__=="__main__":
    import cv2
    import numpy as np

    height, width = 300, 400
    image = np.zeros((height, width, 3), dtype=np.uint8)
    image[:] = (255, 0, 255)
    cv2.imshow('Color', image)
    cv2.waitKey(0)
    cv2.destroyAllWindows()