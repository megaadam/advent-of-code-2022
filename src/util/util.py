def readlines():
    lines = []
    while True:
        try: 
            lines.append(input())
        except EOFError:
            break
    
    return lines
