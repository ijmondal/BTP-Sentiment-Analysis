data = []
with open(r'3_CMI_values.txt') as f:
    for line in f:
        fields = line.split()
        rowdata = map(float, fields)
        data.extend(rowdata)

print(sum(data)/len(data))
