
def prehandle_data(**kwargs):
    collection = kwargs['collection']
    document = kwargs['document']
    directory = collection
    real_dir = real_directory(directory)
    document = path_join(real_dir, document)
    txt_file_path = document + '.txt'
    ann_file_path = txt_file_path[:-4] + '.ann'
    function_ann_file_path = txt_file_path[:-4] + '_func.ann'
    out = []
    with open(txt_file_path, 'r') as txt_file:
        for line in txt_file.readlines():
            sentence = dict()
            sentence['sentence'] = line
            sentence['annotation'] = []
            out.append(sentence)
    return _prehandle_data(out, txt_file_path, ann_file_path,function_ann_file_path)

def _prehandle_data(out, txt_file_path, ann_file_path, function_ann_file_path):
    res = dict()
    with open(ann_file_path, 'r') as ann_file:
        for line in ann_file.readlines():
            line_num = -1
            sentence = dict()
            sentence['sentence'] = ''
            sentence['annotation'] = []
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
                    sentence['sentence']=line_dict[line_start_index[i]]
                    start -= int(line_start_index[i])
                    end -= int(line_start_index[i])
                    line_num = i
                    break
                '''
                elif start > line_start_index[i] and end > (line_start_index[i] + len(line_dict[line_start_index[i]])):
                '''
            data.append(start)
            data.append(end)
            out[line_num]['annotation'].append(data)

    with open(function_ann_file_path, 'r') as function_ann_file:
        
        for line in function_ann_file.readlines():
            line_num = -1
            sentence = dict()
            sentence['sentence'] = ''
            sentence['annotation'] = []
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
                    sentence['sentence']=line_dict[line_start_index[i]]
                    start -= int(line_start_index[i])
                    end -= int(line_start_index[i])
                    line_num = i
                    break
                '''
                elif start > line_start_index[i] and end > (line_start_index[i] + len(line_dict[line_start_index[i]])):
                '''
            data.append(start)
            data.append(end)
            out[line_num]['annotation'].append(data)
    res['processedData'] = out
    return res



def judge_line(txt_file_path):
    count = 0
    line_dict = dict()
    with open(txt_file_path, 'r') as txt_file:
        for line in  txt_file.readlines():
            line_dict[count] = line
            count += len(line)
    return line_dict


txt_file_path = '/Users/robin/research/dlmat/data/Local/test.txt'
out = []
with open(txt_file_path, 'r') as txt_file:
        for line in txt_file.readlines():
            sentence = dict()
            sentence['sentence'] = line
            sentence['annotation'] = []
            out.append(sentence)
res = _prehandle_data(out, '/Users/robin/research/dlmat/data/Local/test.txt', '/Users/robin/research/dlmat/data/Local/test.ann','/Users/robin/research/dlmat/data/Local/test_func.ann')
print(res)