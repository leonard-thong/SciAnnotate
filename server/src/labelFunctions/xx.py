import sys
import re
label_text_map = {

  'Material': ['SnO 2', 'Graphene', 'graphite oxide', 'graphite', 'SnCl4*5H2O', 'water', 'solution','precipitate', 'RGO', 'SnO2NC@N-RGO', 'mixture', 'suspension', 'SnO2 nanocrystals/graphene oxide', 'hydrazine monohydrate', 'graphene oxide', 'product', 'byproducts', 'SnO2 nanocrystal/RGO', 'Ar', 'N-RGO', 'SnO2NC + N-RGO', 'hydrazine'],
  
  'Property-Misc':['Nanocrystals', 'Nitrogen-Doped', 'Sheets', 'Anode', 'nanocrystal aqueous suspension', 'SnO2 nanocrystal/nitrogen-doped', 'hybrid', 'physical', 'mixture', ],
 
  'Property-Type':['concentration'],
  
  'Property-Unit':['mg mL-1'],
  
  #'Operation': ['Fabrication', 'produced', 'Synthesis', 'dissolved', 'transferred', 'heated', 'produce', 'harvested', 'centrifugation', 'dispersed', 'achieve', 'addition','sonicated', 'form', 'lyophilization', 'freeze-drying', 'obtained', 'put', 'placed', 'sealing', 'maintained', 'reduce', 'cooling', 'washed', 'remove', 'adsorbed', 'drying', 'obtain', 'synthesized', 'thermal reduction', 'added', 'prepared', 'stirred'],
  
  'Number': ['2.0', '100', 'two', '120', '28', '35', '10', '10.0', '90', '300', '6', '99', 'six', '500', '100', '3.5', '150', '30', '1'],
  
  'Material-Descriptor': ['natural', 'flakes', 'deionized', 'DI', 'white', 'DI', 'aqueous suspension', 'nanocrystal aqueous suspension', 'homogeneous', 'gray', 'powder', 'nanocrystals', 'aqueous solution', 'SnO2NC/N-RGO-HS'],
  
  'Condition-Misc':['continuously', 'in situ', 'vacuum', 'no', 'not', 'vigorously'],
  
  'Condition-Unit': ['mL', 'degC', 'h', 'times', 'degC min-1'],
  
  'Amount-Unit':['g', 'mL', 'mg', 'μL'],
  
  'Brand':['Alfa Aesar, 325 mesh', 'Sinopharm Chemical Reagent Co., Ltd', 'Alfa Aesar'],
  
  'Operation-Misc':[],
  
  'Condition-Type':['flow', 'heating rate'],
  
  'Apparatus-Descriptor':['poly(tetrafluoroethylene) (Teflon)-lined stainless steel', 'small glass', 'glass', 'tube'],
  
  'Synthesis-Apparatus':['autoclaves', 'oven', 'beaker', 'bottle', 'furnace', 'flask', 'oil bath'],
  
  'Apparatus-Unit': ['mL'],
  
  'Unit':[],
  
  'Reference':['Hummers method.57']
  
}
def xx(text="", entity_index=None):
    res = dict()
    entities = []
    labeled = [False for _ in range(len(text))]
    labels = set()
    for label, text_lists in label_text_map.items():
      for txt in text_lists:
        labels.add((label, txt))
    labels = list(labels)
    labels.sort(key=lambda x:len(x[1]), reverse=True)
    for label, txt in labels:
      for pos in re.finditer(r"\b{}\b".format(txt), text):
        if not labeled[pos.start()]:
          entities.append(["F" + str(next(entity_index)), label, [(pos.start(), pos.end())], text[pos.start(): pos.end()]])
          for i in range(pos.start(), pos.end()):
              labeled[i] = True
    entity_list = set()
    for index, entity in enumerate(entities):
        entity_list.add(entity[1])
        entities[index][1] = '{}_{}'.format(str(sys._getframe().f_code.co_name), entity[1])
    res["entities"] = entities
    return res

if __name__ == "__main__":
    pass
