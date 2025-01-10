class Parser:
    def __init__(self, fileStream):
        self.fileStream = fileStream
        self.currentCommand = None

    def hasMoreLines(self):
        pos = self.fileStream.tell()
        t = bool(self.fileStream.readline())
        self.fileStream.seek(pos)
        return t
    
    def advance(self):
        while True:
            t = self.fileStream.readline()
            t = t.partition("//")[0] #removing comments
            t = t.replace("\n","") #removing next lines

            if t:
                break

        self.currentCommand = t

    def commandType(self):
        t = self.currentCommand.split()
        if t[0] == "push":
            return "C_PUSH"
        elif t[0] == "pop":
            return "C_POP"
        else:
            return "C_ARITHMETIC"

    def arg1(self):
        t = self.currentCommand.split()
        return t[0]
    
    def arg2(self):
        t1, *t2 = self.currentCommand.split()
        return t2