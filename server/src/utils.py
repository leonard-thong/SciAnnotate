from expandLogger import Logger
def color_generator(num):
    return '0' + str(hex(num)).replace('0x', '') if num > 15 else str(hex(num)).replace('0x', '') 

def random_color_generator():
    while 1:
        r = random.randint(0, 255)
        g = random.randint(0, 255)
        b = random.randint(0, 255)
        yield '#' + color_generator(r) + color_generator(g) + color_generator(b)


GLOBAL_LOGGER = Logger()
COLOR_PICKER = random_color_generator()