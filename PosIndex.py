import glob

def preprocessing(filePath):
    file=open(filePath)
    text=file.read()

    return text.split()

def positionaIndex():
    doc_folder='data/*'
    result={}
    doc_map={}
    for docID, file in enumerate(glob.glob(doc_folder)):
        doc_map[docID]=file
        words=preprocessing(file)
        temp_dict=dict()
        for pos, word in enumerate(words):
            temp_dict.setdefault(word, [])
            temp_dict[word].append(pos)

        for i in temp_dict:
            result.setdefault(i, {})
            result[i][docID+1]=temp_dict[i]

    return result

