def readlines():
    print("-->")
    lines = []
    while True:
        try:
            line = input()
            if len(line) > 0:
                lines.append(line)
        except EOFError:
            break
    
    return lines

def extract(str, before, after):
    return(str[str.rfind(before)+len(before):str.find(after)])