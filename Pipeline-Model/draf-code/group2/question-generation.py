import glob,json

def clean_data(data):
    i=0
    final=[]
    flag=0
    done = set()
    while i < len(data):
        if data[i]=='?' or data[i]=='.':
            break
        if data[i].encode('ascii','ignore').isalpha():
            if not ((i==0 or i==1) and (data[i]=='alexa' or data[i]=='siri' or data[i]=='google')):
                final.append(data[i].encode('ascii','ignore').lower().encode('utf-8'))
        i+=1
    return final

path = 'data-for-ml-approach/*.json'
files = glob.glob(path)
questions = []

for filename in files:
    f = open(filename,'r')
    data = json.load(f)
    question= clean_data(data["question"])
    questions.append(question)
    f.close()

f = open('questions.txt','w+')
for q in questions:
    s = ' '.join(q)
    f.write(s+'\n')
