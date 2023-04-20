import glob,re
from nltk.tokenize import word_tokenize
from nltk.corpus import stopwords
Stopwords = set(stopwords.words('english'))

class QueryProcessing:
    def __init__(self, query) -> None:
        self.query=query
        self.stack=[]
        self.temp=""
        self.skip=0

    def compute(self):
        index=positionaIndex()
        if re.findall('/\d',self.query)==[]:
            self.query=re.sub(' ', ' /1 ', self.query)
        self.query=self.query.split()
        word1 = index.get(self.query[0])
        word2 = index.get(self.query[2])
        anding = set(word1).intersection(word2)
        self.query[1] = re.sub("/", "", self.query[1])
        answer = []
        skip = int(self.query[1])

        for i in anding:
            pp1 = index.get(self.query[0])[i]
            pp2 = index.get(self.query[2])[i]

            plen1 = len(pp1)
            plen2 = len(pp2)

            ii = jj = 0

            while ii != plen1:
                jj=0
                while jj != plen2:
                    if abs(pp1[ii]-pp2[jj])==skip:
                        answer.append({i:[pp1[ii],pp2[jj]]})
                    elif pp2[jj] > pp1[ii]:
                        break 
                    jj+=1
                ii+=1
        if answer:
            return answer
        else:
            print('No Docs matched !')
            return 0


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
    # words = [word for word in words if word not in Stopwords]
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



query=QueryProcessing('explicitly read')
for match in query.compute():
    print(match)