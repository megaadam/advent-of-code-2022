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
