# Deep Learning Weak Label Reinforcement Annotation Tool (dlwlrat) #

## Quick start installation: standalone server ##

First, please note the following:

- The dlwlrat standalone server only is available in dlwlrat v1.0 and above.
- The standalone server is experimental and should not be used for sensitive data or systems accessible from the internet.


Run the installation script in “unprivileged” mode

    ./install.sh -u

Start the standalone server

    python standalone.py


You should then be able to access the dlwlrat server from the address printed out by standalone.py.

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
- Recontruct basic storage logic of annotations from labeling function, annotations from labeling function will appear in ann file like F1, F2, etc...
- Color of annotations which are not defined in visual.conf will be assigned a color based on MD5 hash (Frontend control)
- Remove unnecessary error comments to improve visual effect
### To developers
- All feature returns which will be rendered by frontend must use get_document to return a complete object
### New Labeling Function Example
```python
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
```

## Release Note Jan.15 2021
- Add Sign Up Entry, User now can create their own account without asking administor for help
