import sys
import re
def contactLabeler(text="", entity_index=None):
    res = dict()
    entities = [
        ["F" + str(next(entity_index)), "Contact-Email", [(pos.start(), pos.end())], text[pos.start(): pos.end()]]
        for pos in re.finditer("^[a-zA-Z0-9_-]+@[a-zA-Z0-9_-]+(\.[a-zA-Z0-9_-]+)+$", text)
    ]
    entities.extend(
        [
            ["F" + str(next(entity_index)), "Contact-Phone", [(pos.start(), pos.end())], text[pos.start(): pos.end()]]
            for pos in re.finditer("(\d{3}[-\.\s]??\d{3}[-\.\s]??\d{4}|\(\d{3}\)\s*\d{3}[-\.\s]??\d{4}|\d{3}[-\.\s]??\d{4})", text)
        ]
    )
    entity_list = set()
    for index, entity in enumerate(entities):
        entity_list.add(entity[1])
        entities[index][1] = '{}_{}'.format(str(sys._getframe().f_code.co_name), entity[1])
    res["entities"] = entities
    return res
if __name__ == "__main__":
    pass
