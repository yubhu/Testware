f = open('temp.txt')
output = []
for line in f:
    line = line.strip()
    line = line.strip(';')
    output.append(line.split('\t'))
f.close()