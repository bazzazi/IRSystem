# Developer: Mohammad Ali Bazzazi
############# starting code #############
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
        pos_index, inverted_index, doc_map=positionaIndex()
        connecting_word=list()
        diff_word=list()
        pos_idx=0
        invert_idx=0
        self.query=self.query.split()
        j=0
        for word in self.query:
            if re.findall('/\d', word):
                pos_idx=1
                invert_idx=0
                connecting_word.append(word)
                j+=1
            elif word in ['and', 'or', 'not']:
                invert_idx=1
                pos_idx=0
                j+=1
                connecting_word.append(word)
            else:
                if j%2==1:
                    connecting_word.append('/0')
                    pos_idx=1
                    invert_idx=0
                    diff_word.append(word)
                    continue
                if pos_index.get(word):
                    diff_word.append(word)
                else:
                    print(f"'{word}' was not found!")
                    return
                j+=1
            
        ##################################
        if invert_idx:
            return self.compute_inverted_index(diff_word, connecting_word, inverted_index, doc_map)

        ##################################
        elif pos_idx:   
            return self.compute_pos_index(diff_word,connecting_word ,pos_index, doc_map)

    def compute_inverted_index(self, diff_word, connecting_word, inverted_index, doc_map):
        zeros_and_ones=list()
        all_zeros_and_ones=list()

        for word in diff_word:
            zeros_and_ones=[0]*len(doc_map)
            all_zeros_and_ones.append(zeros_and_ones)

        doc_ids=doc_map.keys()
        for id, word in enumerate(diff_word):
            posting=list(set(inverted_index.get(word)))
            for key in doc_ids:
                if key-1 in posting:
                    all_zeros_and_ones[id][key-1]=1

        for word in connecting_word:
            word1=all_zeros_and_ones[0]
            word2=all_zeros_and_ones[1]
            if word == 'and':
                new_zeros_and_ones=[w1 & w2 for (w1,w2) in zip(word1, word2)]
                all_zeros_and_ones.remove(word1)
                all_zeros_and_ones.remove(word2)
                all_zeros_and_ones.append(new_zeros_and_ones)
            elif word == 'or':
                new_zeros_and_ones=[w1 | w2 for (w1,w2) in zip(word1, word2)]
                all_zeros_and_ones.remove(word1)
                all_zeros_and_ones.remove(word2)
                all_zeros_and_ones.append(new_zeros_and_ones)
            elif word == 'not':
                not_word2=[not w2 for w2 in word2]
                new_zeros_and_ones=[w1 & w2 for (w1,w2) in zip(word1,not_word2)]
                all_zeros_and_ones.remove(word1)
                all_zeros_and_ones.remove(word2)
                all_zeros_and_ones.append(new_zeros_and_ones)
        answer=list()
        result=all_zeros_and_ones[0]
        for i, bit in enumerate(result):
            if bit == 1:
                answer.append(doc_map.get(i+2))
        return answer

    def compute_pos_index(self, diff_word, connecting_word, pos_index ,doc_map):
        final_result=dict()
        temp_result=self.compute(connecting_word[0], diff_word[:2])
        k=0
        answer=[]
        for i, skip in enumerate(connecting_word[1:]):
            k=1
            word=diff_word[i+2]
            for result in temp_result:
                doc_id=list(result.keys())[0]
                word_pos=pos_index.get(word).get(doc_id)
                if word_pos is None:
                    continue
                new_index=(int(list(result.values())[0][-1])+int(skip.replace('/','')))+1
                if new_index in word_pos:
                    new_result=list(result.values())[0]
                    new_result.append(new_index)
                    final_result[doc_map[doc_id]]=new_result

        if k==1:
            answer=[{doc:pos} for doc, pos in final_result.items()]
        else:
            for result in temp_result:
                for doc, pos in result.items():
                    answer.append({doc_map[doc]:pos})


        if answer:
            return answer
        else:
            print("No Docs matched with the query!")
            return

    def compute(self,skip ,query):
        index=positionaIndex()[0]

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
                    if abs(pp1[ii]-pp2[jj])==skip+1:
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
    inverted_index={}
    for docID, file in enumerate(glob.glob(doc_folder)):
        doc_map[docID+1]=file
        words=preprocessing(file)
        temp_dict=dict()
        for pos, word in enumerate(words):
            temp_dict.setdefault(word, [])
            temp_dict[word].append(pos)
            inverted_index.setdefault(word, [])
            inverted_index[word].append(docID)

        for i in temp_dict:
            result.setdefault(i, {})
            result[i][docID+1]=temp_dict[i]

    return result, inverted_index, doc_map


query=input("Enter you query: ")
queryProcess=QueryProcessing(query)
print(queryProcess.queryParsing())

############# ending code #############
