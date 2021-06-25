import os

from collections import defaultdict
from enum import Enum
from document import real_directory

__all__ = ['AnnotationConfigOption', 'AnnotationConfig', 'global_config_manager', 'ConfigManager']

class AnnotationConfigOption(Enum):

    entities = 1
    relations = 2
    events = 3
    attributes = 4


class AnnotationConfig(object):

    @staticmethod
    def parse_config_file(path):
        pkg = defaultdict(list)
        if not os.path.exists(path):
            return pkg
        with open(path, 'r') as f:
            current_section = None
            lines = f.readlines()
            for line in lines:
                line = line.replace('\n', '')
                if len(line.strip()) ==0 or line[0] == '#':
                    continue
                if line == '[entities]':
                    current_section = 'entities'
                elif line == '[relations]':
                    current_section = 'relations'
                elif line == '[events]':
                    current_section = 'events'
                elif line == '[attributes]':
                    current_section = 'attributes'
                else:
                    if current_section != None and len(line.strip()) > 0:
                        pkg[current_section].append(line)
        return pkg


    def __init__(self, path):
        self.path = path
        self.allow_duplicate = False
        pkg = self.parse_config_file(path)
        self.entities = pkg['entities']
        self.relations = pkg['relations']
        self.events = pkg['events']
        self.attributes = pkg['attributes']
    
    def set_allow_duplicate(self, flag=True):
        self.allow_duplicate = flag

    def push(self, config_option, elem):
        if config_option == AnnotationConfigOption.entities:
            self.entities.append(elem)
        elif config_option == AnnotationConfigOption.relations:
            self.relations.append(elem)
        elif config_option == AnnotationConfigOption.events:
            self.events.append(elem)
        elif config_option == AnnotationConfigOption.attributes:
            self.attributes.append(elem)
    
    def remove(self, config_option, elem):
        if config_option == AnnotationConfigOption.entities:
            self.entities.remove(elem)
        elif config_option == AnnotationConfigOption.relations:
            self.relations.remove(elem)
        elif config_option == AnnotationConfigOption.events:
            self.events.remove(elem)
        elif config_option == AnnotationConfigOption.attributes:
            self.attributes.remove(elem)
    
    def update(self, config_option, old, new):
        if config_option == AnnotationConfigOption.entities:
            self.entities.remove(old)
            self.entities.append(new)
        elif config_option == AnnotationConfigOption.relations:
            self.relations.remove(old)
            self.relations.append(new)
        elif config_option == AnnotationConfigOption.events:
            self.events.remove(old)
            self.events.append(new)
        elif config_option == AnnotationConfigOption.attributes:
            self.attributes.remove(old)
            self.attributes.append(new)
    
    def archive(self):
        file_string = ''
        for config_option in ['entities', 'relations', 'events', 'attributes']:
            elems = getattr(self, config_option)
            if not self.allow_duplicate:
                elems = list(set(elems))
            file_string += f'[{config_option}]\n\n'
            for elem in elems:
                file_string += f'{elem}\n'
            file_string += '\n'
        with open(self.path, 'w') as f:
            f.write(file_string)

class ConfigManager(object):
    __instance = None
    _postfix = "annotation.conf"
    def __new__(cls, *args, **kwargs):
        if cls.__instance == None:
            cls.__instance = super().__new__(cls)
        return cls.__instance
    
    def get_general_anno_config(self, general_path='/'):
        general_path = real_directory(general_path) + self._postfix
        return AnnotationConfig(general_path)

    def get_collection_anno_config(self, collection):
        return AnnotationConfig(collection)

    def get_general_visual_config(self, general_path):
        pass

    def get_collection_visual_config(self, collection):
        pass

global_config_manager = ConfigManager()

if __name__ == "__main__":
    config_manager = ConfigManager()
    anno_config = config_manager.get_general_anno_config()
    anno_config.push(AnnotationConfigOption.entities, 'asdasfasf')
    print(anno_config.entities)
    # anno_config.archive()
    