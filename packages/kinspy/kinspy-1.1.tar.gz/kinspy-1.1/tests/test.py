import numpy as np

def read_columns(fp,*index,sep = " "):
    y = [[] for i in index]
    print(y)
    for line in fp:
        for i in index:
            y[i].append(float(line.strip().split(sep)[i]))
    return (np.array(y[i]) for i in index)

a,b = read_columns(open("espvr_data1.csv"),0,1)
print(a)