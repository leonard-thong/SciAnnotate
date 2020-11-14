#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Nov 13 20:28:19 2020

@author: robin
"""

import torch



    
def get_ann(value, file, index, entity_index, keys, text, span_no):
    for key in value:
        result = "T" + str(entity_index) + '\tspan'+str(span_no) +'_' + keys + '_' + value[key]
        result += ' ' + str(index + int(key[0])) + ' ' + str(index + int(key[1])) + '\t'
        start = int(key[0])
        end = int(key[1])
        result += text[start:end] + '\n'
        entity_index += 1
        f1.write(result)
    span_no += 1
    return entity_index, span_no
        
        
        
        


data = torch.load('weak_lb_results.pt')

index = 0
entity_index = 0
span_no = 1
no = 0
for i in data: 
    f = open( 'data/testfunction' + str(no) +'.txt', 'w')
    f1 = open( 'data/testfunction' + str(no) +'_func.ann', 'w')
    text = i['text']
    f.write(text)
    for key in i:
        if key !=  'text':
            entity_index, span_no = get_ann(i[key], f1, index, entity_index,  key, text, span_no)
    no += 1
    
    

    
    
    