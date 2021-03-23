import os
import shutil
import re
from document import real_directory
from os.path import join as path_join
from projectconfig import __parse_configs, __default_configuration, __read_or_default, SECTION_ALIAS, SEPARATOR_STR

def create_new_entity(**kwargs):
    res = dict()
    entity = kwargs['entity_name']
    collection = kwargs['collection']
    real_dir = real_directory(collection)
    config_dir = real_dir + "annotation.conf"
    configstr = __read_or_default(config_dir, __default_configuration)
    configstr = configstr.split("\n")
    
    # section = "general"
    # section_lines = {section: []}
    # section_labels = {}

    # Check duplicate entit type
    if entity in configstr:
        res['status'] = 200
        return res
    for ln, l in enumerate(configstr):
        if l == "[relations]":
            configstr.insert(ln-2, entity)
            break
        
    with open(config_dir, 'w') as configFile:
        configFile.write("\n".join(configstr))


    res['status'] = 200

    return res