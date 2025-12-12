from importlib import import_module

def skip_nlines(fp,n):
    for i in range(n): 
        fp.readline()

def read_columns(fp,*index,sep = " "):
    np = import_module("numpy")
    y = [[] for i in index]

    for line in fp:
        for i in index:
            y[i].append(float(line.strip().split(sep)[i]))
    return (np.array(y[i]) for i in index)

def read_2columns(fp,i,j,is_csv = False):
    np = import_module("numpy")
    a_list = []
    b_list = []
    for line in fp:
        if is_csv == False:
            line_list = line.strip().split()
        else:
            line_list = line.strip().split(",")
        a_list.append(float(line_list[i]))
        b_list.append(float(line_list[j]))
    return np.array(a_list),np.array(b_list)

def read_3columns(fp,i,j,k,is_csv = False):
    np = import_module("numpy")
    a_list = []
    b_list = []
    c_list = []
    for line in fp:
        if is_csv == False:
            line_list = line.strip().split()
        else:
            line_list = line.strip().split(",")
        a_list.append(float(line_list[i]))
        b_list.append(float(line_list[j]))
        c_list.append(float(line_list[k]))
    return np.array(a_list),np.array(b_list),np.array(c_list)
