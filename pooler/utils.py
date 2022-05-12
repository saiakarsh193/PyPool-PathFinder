def constrain(val, minv, maxv):
    return max(minv, min(maxv, val))

def colToHash(*argv):
    r, g, b = 0, 0, 0
    tmp = ()
    if(len(argv) == 3):
        tmp = argv
    elif(len(argv) == 1):
        if(type(argv[0]) is tuple):
            if(len(argv[0]) == 3):
                tmp = argv[0]
            elif(len(argv[0]) == 1):
                tmp = (argv[0][0], argv[0][0], argv[0][0])
        elif(type(argv[0]) is int):
            tmp = (argv[0], argv[0], argv[0])
    if(len(tmp) == 3 and type(tmp[0]) is int and type(tmp[1]) is int and type(tmp[2]) is int):
        r, g, b = tmp
    r, g, b = constrain(r, 0, 255), constrain(g, 0, 255), constrain(b, 0, 255)
    def hconv(val):
        tmp = hex(val)[2: ]
        if(len(tmp) == 1):
            return '0' + tmp
        return tmp
    r, g, b = hconv(r), hconv(g), hconv(b)
    return '#' + r + g + b

def colToHash2(rgb):
    return "#%02x%02x%02x" % rgb  

def hashToCol(tstr):
    r, g, b = tstr[1: 3], tstr[3: 5], tstr[5: ]
    r, g, b = int(r, 16), int(g, 16), int(b, 16)
    return (r, g, b)

if __name__ == '__main__':
    print(colToHash((10, 11, 255)))
    print(colToHash2((10, 11, 255)))
    print(hashToCol('#0a0bff'))