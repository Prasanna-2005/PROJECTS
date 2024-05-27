MAX_LINE_LEN = 90

def justify_lines(inp, width):
    output = []
    line = []
    current_length = 0
    
    for word in inp:
        if current_length + len(word) + len(line) > width:
            space_to_be_filled = width - current_length
            for i in range(space_to_be_filled):
                if len(line) > 1:
                    line[i % (len(line) - 1)] += ' '
                else:
                    line[0] += ' '
            output.append(''.join(line))
            line = []
            current_length = 0
        
        line.append(word)
        current_length += len(word)
    
    output.append(' '.join(line).ljust(width))
    return output   #list of strings where each string is a line

try:
    fname = input("ENTER VALID FILE NAME(TXT FILES)::")
    
    if not fname.endswith(".txt"):
        print("PLEASE CHECK YOUR FILE NAME ONCE, MUST BE A TXT FILE")
        exit()
            
    try:
        fileobj = open(fname, "r")
    except FileNotFoundError:
        print("FILE NOT FOUND, PLEASE CHECK THE FILE NAME AND PATH")
        exit()
    
    num_col = input("ENTER NO OF COLUMNS ")
    
    if not num_col.isnumeric():
        print("ENTER A VALID NUMBER!!!")
        exit()
    num_col = int(num_col)
    
    if num_col > 20:
        print("ENTER COL VALUE LESS THAN 20")
        exit()
    if num_col <= 0:
        print("Invalid number of columns")
        exit()
    l = fileobj.readlines()
    para = [i.strip('\n') for i in l if i.strip('\n') != '']
    
    width = len_per_line = MAX_LINE_LEN // num_col
    final_list = []
    
    for i in para:
        spl_list = i.split()
        
        for w in spl_list:
            if len(w) >= width:
                s1 = w[:width//2]
                s2 = w[width//2:]
                ind = spl_list.index(w)
                spl_list.remove(w)
                spl_list.insert(ind, s1)
                spl_list.insert(ind + 1, s2)
        
        x = justify_lines(spl_list, len_per_line)
        
        for k in x:
            final_list.append(k)
        
        final_list.append(" " * len_per_line)
    
    lines_per_part = len(final_list) // num_col
    extra = len(final_list) % num_col
    
    if extra != 0:
        lines_per_part += 1
    
    partitions = []
    
    for i in range(num_col):
        l = i * lines_per_part
        r = (i + 1) * lines_per_part
        
        if r >= len(final_list):
            r = len(final_list)
        
        partitions.append(final_list[l:r])
    
    for j in range(lines_per_part):
        for k in range(num_col):
            if j < len(partitions[k]):
                print(partitions[k][j], end="   ")
            else:
                print(" " * len_per_line,end="   ")
        print()
    
    fileobj.close()
    
except FileNotFoundError :
    print("FILE_NOT_FOUND")

