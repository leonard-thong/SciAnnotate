# Brat Rapid Annotation Tool (brat) #

## Quick start installation: standalone server ##

First, please note the following:

- The brat standalone server only is available in brat v1.3 and above.
- The standalone server is experimental and should not be used for sensitive data or systems accessible from the internet.


Run the installation script in “unprivileged” mode

    ./install.sh -u

Start the standalone server

    python standalone.py


You should then be able to access the brat server from the address printed out by standalone.py.

## Add New Labeling Functions

- Access the file labelFunctionExecutor.py
- Implement / Import your labeling function
- Add your function and corresponding alias to LABELING_FUNCTION_SET

```
LABELING_FUNCTION_SET = {"alias": your_new_function}
```

## Release Note Sept.4 2020
### Feature:
* Labeling Function Real Time Debug
* Labeling Function Hot Append
* MD5 Color Generation, Stable color for each added labeing function


## Release Note Dec.17 2020
- Recontruct basic storage logic of annotations from labeling function
- Color of annotations which are not defined in visual.conf will be assigned a color based on MD5 hash (Frontend control)
- Remove unnecessary error comments to improve visual effect
### To developers
- All feature returns which will be rendered by frontend must use get_document to return a complete object
### New Labeling Function Example
```python
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
```