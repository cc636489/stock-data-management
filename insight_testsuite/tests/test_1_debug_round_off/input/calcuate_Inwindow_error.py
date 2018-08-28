start = '347'
end = '350'
file1 = 'actual_'+start+'_'+end+'.txt'
file2 = 'predicted_'+start+'_'+end+'.txt'
fout = 'actual_'+start+'_'+end+'_removed.txt'

with open(file1, 'r') as f1, open(file2, 'r') as f2:
    a = f1.readlines()
    b = f2.readlines()

k = 0
f = open(fout, 'w')
while k < len(a):
    if any([a[k][11:20] in b[j] for j in range(len(b))]):
        f.write(a[k])
    k += 1
f.close()

with open(fout, 'r') as f3:
    c = f3.readlines()

sum = 0.0
for i in range(len(c)):
    tempc = float(c[i].split('|')[2])
    tempb = float(b[i].split('|')[2])
    sum += abs(tempb-tempc)

print sum/len(c)
