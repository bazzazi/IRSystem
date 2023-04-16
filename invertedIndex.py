import glob,re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
Stopwords = set(stopwords.words('english'))


def remove_special_characters(text):
    regex = re.compile('[^a-zA-Z0-9\s]')
    text_returned = re.sub(regex,'',text)
    return text_returned

def preprocessing(filePath):
    file=open(filePath)
    text=file.read()
    text = remove_special_characters(text)
    text = re.sub(re.compile('\d'),'',text)
    words = word_tokenize(text)
    words = [word for word in words if len(words)>1]
    words = [word.lower() for word in words]
    words = [word for word in words if word not in Stopwords]
    return words

def inverted_index():
    folderPath='data/*'
    inverted_index=dict()
    document_map=dict()

    for docID, filePath in enumerate(glob.glob(folderPath)):
        words=preprocessing(filePath)
        
        document_map[docID+1]=filePath

        for word in words:
            inverted_index.setdefault(word, []) # set default list for words that is not present in dictionary
            inverted_index[word].append(docID+1) # and doc ID


    inverted_index={a:list(set(b)) for a, b in inverted_index.items()} # remove duplicate values in posting list

    return inverted_index, document_map

def query_process(query):
    words=query.split()
    connecting_words=list()
    different_words=list()
    for word in words:
        if word.lower() in ['and', 'or', 'not']:
            connecting_words.append(word.lower())
        else:
            different_words.append(word.lower())

    index, doc_map=inverted_index()
    index_keys=index.keys()

    zeros_and_ones=list()
    all_zeros_and_ones=list()

    for word in different_words:
        if word in index_keys:
            zeros_and_ones=[0]*len(doc_map)
            all_zeros_and_ones.append(zeros_and_ones)
        else:
            print(f"{word} not found!")
            return 0

    doc_ids=doc_map.keys()
    for id, word in enumerate(different_words):
        posting=index.get(word)
        for key in doc_ids:
            if key in posting:
                all_zeros_and_ones[id][key-1]=1

    for word in connecting_words:
        word1=all_zeros_and_ones[0]
        word2=all_zeros_and_ones[1]
        if word == 'and':
            new_zeros_and_ones=[w1 and w2 for (w1,w2) in zip(word1, word2)]
            all_zeros_and_ones.remove(word1)
            all_zeros_and_ones.remove(word2)
            all_zeros_and_ones.append(new_zeros_and_ones)
        elif word == 'or':
            new_zeros_and_ones=[w1 or w2 for (w1,w2) in zip(word1, word2)]
            all_zeros_and_ones.remove(word1)
            all_zeros_and_ones.remove(word2)
            all_zeros_and_ones.append(new_zeros_and_ones)
        elif word == 'not':
            not_word2=[not w2 for w2 in word2]
            new_zeros_and_ones=[w1 and w2 for (w1,w2) in zip(word1,not_word2)]
            all_zeros_and_ones.remove(word1)
            all_zeros_and_ones.remove(word2)
            all_zeros_and_ones.append(new_zeros_and_ones)

    answer=list()
    result=all_zeros_and_ones[0]
    for i, bit in enumerate(result):
        if bit == 1:
            answer.append(doc_map.get(i+1))

    return answer

query=input('Enter your query: ')
result=query_process(query)
print(result)