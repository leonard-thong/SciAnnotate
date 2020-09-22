import random
import os
import hashlib
import time

from expandLogger import Logger
from tokenise import whitespace_token_boundary_gen

GLOBAL_LOGGER = Logger()

def generate_color_config(name, entities):
    md5_obj = hashlib.md5()
    entity_color_items = []
    for entity in entities:
        md5_obj.update("{}_{}".format(name, entity).encode('utf-8'))
        hash_code = md5_obj.hexdigest()
        color = '#{}'.format(str(hash_code)[0:6])
        color = list(color)
        for i in range(1, 6, 2):
            if '7' >= color[i] >= '0':
                color[i] = str(hex(int(color[i]) + 8)).replace('0x', '') 
        color = ''.join(color)
        entity_color_items.append('\n{}_{}\tbgColor:{}'.format(name, entity, color))
    entity_color_items.append('\n{}_unlabeled\tbgColor:#000000'.format(name))
    if not os.path.exists('./data/visualConfigs/drawings.conf'):
        with open('./data/visualConfigs/drawings.conf', 'w') as color_config:
            with open('./data/visualConfigs/drawing.conf', 'r') as drawing_content:
                color_config.write(drawing_content.read())
                color_config.write(''.join(entity_color_items))
    else:
       with open('./data/visualConfigs/drawings.conf', 'a') as color_config:
            color_config.write(''.join(entity_color_items)) 
    os.system('sh ./data/build_visual_conf.sh')

def get_entity_index():
    index = 0
    while 1:
        index += 1
        yield index


def get_entity_index_exist(indexNo):
    index = indexNo
    while 1:
        index += 1
        yield index

def clean_cached_config():
    os.system('rm ./data/visualConfigs/drawings.conf')

def add_common_info(text, res):
    res["text"] = text
    res["token_offsets"] = [o for o in whitespace_token_boundary_gen(text)]
    res["ctime"] = time.time()
    res["source_files"] = ["ann", "txt"]
    return res

if __name__ == "__main__":
    entity_list = ['Location', 'Person']
    generate_color_config('spam2', entity_list)