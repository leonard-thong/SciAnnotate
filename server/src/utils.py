from expandLogger import Logger
import random
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

def generate_color_config(name, entities):
    # TODO: Define entities and color config source
    entity_color_items = []
    for entity in entities:
        entity_color_items.append('\n{}\tbgColor:{}'.format(entity, next(COLOR_PICKER)))
    with open('./data/visualCofigs/drawings.conf', 'a') as color_config:
        color_config.write(''.join(entity_color_items))
    os.system('sh ./data/build_visual_conf.sh')
