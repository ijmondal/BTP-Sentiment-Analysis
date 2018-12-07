f=open("codemixed_w2vec.txt","r")
data={}
for i in f.readlines():
    temp=i.split()
    data[temp[0]]=[float(k) for k in temp[1:]]
f = open("tfidf.csv","r")
data1={}
for i in f.readlines():
    temp1=i.split(",")
    data1[temp1[0]]=float(temp[1])
print(data)
print(data1)


for i in data.keys():
    if i.lower() in data1:
        data[i] = [str(data1[i.lower()]* l) for l in data[i]]
    else:
        data[i] = [str(l) for l in data[i]]
y = open("result.txt","w")
for i in data.keys():
    y.write(i+" "+" ".join(data[i])+"\n")