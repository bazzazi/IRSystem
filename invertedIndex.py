import glob

def preprocessing(filePath):
    file=open(filePath)
    text=file.read()
    return text.split()

def inverted_index():
    folderPath='data/*'
    inverted_index=dict()
    document_map=dict()

    for docID, filePath in enumerate(glob.glob(folderPath)):
        words=preprocessing(filePath)
        
        document_map[docID]=filePath

        for word in words:
            inverted_index.setdefault(word, []) # set default list for words that is not present in dictionary
            inverted_index[word].append(docID+1) # and doc ID


    inverted_index={a:list(set(b)) for a, b in inverted_index.items()} # remove duplicate values in posting list

    return inverted_index


indexes=inverted_index()

for key, value in indexes.items():
    print(' ________________________')
    print(f'|Term: {key}')
    print(f'|Posting: {value}')
    print('|________________________')