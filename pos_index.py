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

def queryProcessing(query):
    pass