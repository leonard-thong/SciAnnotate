import random
import os
import hashlib
import time

def _prehandle_data(txt_file_path, ann_file_path, function_ann_file_path):
    out = []
    sentence = dict()
    sentence['sentence'] = ''
    sentence['annotation'] = []
    with open(ann_file_path, 'r') as ann_file:
        for line in ann_file.readlines():
            data = []
            line = line.replace('\t', ' ')
            info = line.split(' ')
            source_name = info[1].split('_')[0]
            temp = info[1].split('_')[1:]
            label = ''
            for i in range(len(temp)):
                label += temp[i]
            data.append(source_name)
            data.append(label)
            start = int(info[2])
            end = int(info[3])
            line_dict = judge_line(txt_file_path)
            line_start_index = [key for key in line_dict]
            line_start_index = sorted(line_start_index)
            for i in range(len(line_start_index)):
                if start > int(line_start_index[i]) and end < (int(line_start_index[i]) + len(line_dict[line_start_index[i]])):
                    sentence['sentence'] = line_dict[line_start_index[i]]
                    start -= int(line_start_index[i])
                    end -= int(line_start_index[i])
                    break
                '''
                elif start > line_start_index[i] and end > (line_start_index[i] + len(line_dict[line_start_index[i]])):
                '''
            data.append(start)
            data.append(end)
            sentence['annotation'].append(data)     
    
    with open(function_ann_file_path, 'r') as function_ann_file:
        for line in function_ann_file.readlines():
            data = []
            line = line.replace('\t', ' ')
            info = line.split(' ')
            source_name = info[1].split('_')[0]
            temp = info[1].split('_')[1:]
            label = ''
            for i in range(len(temp)):
                label += temp[i]
            data.append(source_name)
            data.append(label)
            start = int(info[2])
            end = int(info[3])
            line_dict = judge_line(txt_file_path)
            line_start_index = [key for key in line_dict]
            line_start_index = sorted(line_start_index)
            for i in range(len(line_start_index)):
                if start > int(line_start_index[i]) and end < (int(line_start_index[i]) + len(line_dict[line_start_index[i]])):
                    sentence['sentence'] = line_dict[line_start_index[i]]
                    start -= int(line_start_index[i])
                    end -= int(line_start_index[i])
                    break
                '''
                elif start > line_start_index[i] and end > (line_start_index[i] + len(line_dict[line_start_index[i]])):
                '''
            data.append(start)
            data.append(end)
            sentence['annotation'].append(data)     
            
    out.append(sentence)
    return out


def judge_line(txt_file_path):
    count = 0
    line_dict = dict()
    with open(txt_file_path, 'r') as txt_file:
        for line in  txt_file.readlines():
            line_dict[count] = line
            count += len(line)
    return line_dict

txt_file_path = '/Users/robin/research/brat/data/Local/test.txt'
function_ann_file_path= '/Users/robin/research/brat/data/Local/test_func.ann'
ann_file_path = '/Users/robin/research/brat/data/Local/test.ann'
out = _prehandle_data(txt_file_path, ann_file_path, function_ann_file_path)
print(out)