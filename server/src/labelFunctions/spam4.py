import re
import sys

from utils import generate_color_config

def spam4(text="", entity_index=None):
    res = dict()
    entities = [
        ["T" + str(next(entity_index)), "Location", [(pos.start(), pos.end())]]
        for pos in re.finditer("year", text)
    ]
    entities.extend(
        [
            ["T" + str(next(entity_index)), "NoneType", [(pos.start(), pos.end())]]
            for pos in re.finditer("was", text)
        ]
    )
    entity_list = set()
    for index, entity in enumerate(entities):
        entity_list.add(entity[1])
        entities[index][1] = '{}_{}'.format(str(sys._getframe().f_code.co_name), entity[1])
    generate_color_config(sys._getframe().f_code.co_name, entity_list)
    res["entities"] = entities
    return res

if __name__ == "__main__":
    pass
if __name__ == "__main__":
    pass
