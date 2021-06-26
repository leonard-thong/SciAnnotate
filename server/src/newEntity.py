import os
import shutil
import re
from document import real_directory
from os.path import join as path_join
from projectconfig import __parse_configs, __default_configuration, __read_or_default, SECTION_ALIAS, SEPARATOR_STR
from configManager import *

def modify_entity(**kwargs):
    res = dict()
    entity = kwargs['entity_name']
    collection = kwargs['collection']
    type = kwargs['type']
    real_dir = real_directory(collection)
    config_dir = real_dir + "annotation.conf"
    config = global_config_manager.get_collection_anno_config(config_dir)
    if type == "create":
        config.push(AnnotationConfigOption.entities, entity)
    elif type == "delete":
        config.remove(AnnotationConfigOption.entities, entity)
    config.set_allow_duplicate(False)
    config.archive()

    res['status'] = 200

    return res