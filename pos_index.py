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

    def queryParsing(self):
        index=positionaIndex()
        connecting_word=list()
        diff_word=list()
        not_answer=[]

        if re.findall('/\d',self.query)==[]:
            self.query=re.sub(' ', ' /1 ', self.query)
        self.query=self.query.split()
        for word in self.query:
            if re.findall('/\d', word):
                connecting_word.append(word)
            else:
                if index.get(word):
                    diff_word.append(word)
                else:
                    print(f"'{word}' was not found!")
                    return
                
        results=self.compute(connecting_word[0], diff_word[:2])
        for i, skip in enumerate(connecting_word[1:]):
                word=diff_word[i+2]
                for result in results:
                    doc_id=list(result.keys())[0]
                    word_pos=index.get(word).get(doc_id)
                    if word_pos is None:
                        not_answer.append(result)
                        continue
                    new_index=(int(list(result.values())[0][-1])+int(skip.replace('/','')))
                    if new_index not in word_pos:
                        not_answer.append(result)
                    else:
                        new_result=list(result.values())[0]
                        new_result.append(new_index)
                        result[doc_id]=new_result

        answer=[result for result in results if result not in not_answer]
        if answer:
            return answer
        else:
            print("No Docs matched with the query!")
            return
    
    def compute(self,skip ,query):
        index=positionaIndex()

        word1 = index.get(query[0])
        word2 = index.get(query[1])

        anding = set(word1).intersection(word2)
        skip = re.sub("/", "", skip)
        answer = []
        skip = int(skip)

        for i in anding:
            pp1 = index.get(query[0])[i]
            pp2 = index.get(query[1])[i]

            plen1 = len(pp1)
            plen2 = len(pp2)

            ii = jj = 0

            while ii != plen1:
                while jj != plen2:
                    if abs(pp1[ii]-pp2[jj])==skip:
                        answer.append({i:[pp1[ii],pp2[jj]]})
                    elif pp2[jj] > pp1[ii]:
                        break 
                    jj+=1
                ii+=1

        return answer

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



query=QueryProcessing('model of retrieval')
print(query.queryParsing())