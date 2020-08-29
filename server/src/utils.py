import random
import os

from expandLogger import Logger
def color_generator(num):
    return '0' + str(hex(num)).replace('0x', '') if num < 15 else str(hex(num)).replace('0x', '') 

def random_color_generator():
    while 1:
        r = random.randint(180, 255)
        g = random.randint(180, 255)
        b = random.randint(180, 255)
        yield '#' + color_generator(r) + color_generator(g) + color_generator(b)

GLOBAL_LOGGER = Logger()
COLOR_PICKER = random_color_generator()

def generate_color_config(name, entities):
    # TODO: Define entities and color config source
    color = next(COLOR_PICKER)
    entity_color_items = []
    for entity in entities:
        entity_color_items.append('\n{}_{}\tbgColor:{}'.format(name, entity, color))
    if not os.path.exists('./data/visualConfigs/drawings.conf'):
        with open('./data/visualConfigs/drawings.conf', 'w') as color_config:
            with open('./data/visualConfigs/drawing.conf', 'r') as drawing_content:
                color_config.write(drawing_content.read())
                color_config.write(''.join(entity_color_items))
    else:
       with open('./data/visualConfigs/drawings.conf', 'a') as color_config:
            color_config.write(''.join(entity_color_items)) 
    os.system('sh ./data/build_visual_conf.sh')

if __name__ == "__main__":
    entity_list = ['Location', 'Person']
    generate_color_config('spam2', entity_list)