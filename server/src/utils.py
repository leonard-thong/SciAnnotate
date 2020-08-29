import random
import os
import hashlib

from expandLogger import Logger
def color_generator(num):
    return '0' + str(hex(num)).replace('0x', '') if num < 15 else str(hex(num)).replace('0x', '') 

def random_color_generator():
    while 1:
        r = random.randint(128, 255)
        g = random.randint(128, 255)
        b = random.randint(128, 255)
        yield '#' + color_generator(r) + color_generator(g) + color_generator(b)

GLOBAL_LOGGER = Logger()
COLOR_PICKER = random_color_generator()

def generate_color_config(name, entities):
    # TODO: Define entities and color config source
    md5_obj = hashlib.md5()
    md5_obj.update(name.encode('utf-8'))
    hash_code = md5_obj.hexdigest()
    color = '#{}'.format(str(hash_code)[0:6])
    color = list(color)
    for i in range(1, 6, 2):
        if '7' >= color[i] >= '0':
            color[i] = str(hex(int(color[i]) + 8)).replace('0x', '') 
    color = ''.join(color)
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