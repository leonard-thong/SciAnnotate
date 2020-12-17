import sys
import re
def executor1(text="", entity_index=None):
    res = dict()
    entities = [
        ["T" + str(next(entity_index)), "Type", [(pos.start(), pos.end())], text[pos.start(): pos.end()]]
        for pos in re.finditer("in", text)
    ]
    entities.extend(
        [
            ["T" + str(next(entity_index)), "NoneType", [(pos.start(), pos.end())], text[pos.start(): pos.end()]]
            for pos in re.finditer("for", text)
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
