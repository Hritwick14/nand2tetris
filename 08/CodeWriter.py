class CodeWriter:
    def __init__(self, outputPath):
        self.outputFileStream = open(outputPath, "w")

        self.fileName = ""
        self.functionName = ""


    def setFileName(self, fileName):
        self.fileName = fileName

    def writeInit(self):
        self.outputFileStream.writelines([
            "@261\n",
            "D=A\n",
            "@SP\n",
            "M=D\n",

            f"@Sys.init\n",
            "0;JMP\n"
        ])
    
    def writeArithmetic(self, command, lineCount):
        binaryOperatorDict = {
            "add": "D+M",
            "sub": "M-D",
            "and": "D&M",
            "or": "D|M",
        }
        unaryOperatorDict = {
            "neg": "-M",
            "not": "!M",
        }
        logicDict = {
            "eq": "JEQ",
            "gt": "JGT",
            "lt": "JLT",
        }

        self.outputFileStream.writelines([
            f"\n//{command}\n",
        ])

        if command in binaryOperatorDict:
            self.outputFileStream.writelines([
                "@SP\n",
                "AM=M-1\n",
                "D=M\n",
                "A=A-1\n",
                f"M={binaryOperatorDict[command]}\n",
            ])
        elif command in unaryOperatorDict:
            self.outputFileStream.writelines([
                "@SP\n",
                "A=M-1\n",
                f"M={unaryOperatorDict[command]}\n",
            ])
        elif command in logicDict:
            self.outputFileStream.writelines([
                "@SP\n",
                "AM=M-1\n",
                "D=M\n",
                "A=A-1\n",
                "D=M-D\n",
                f"@TRUE_{lineCount}\n",
                f"D;{logicDict[command]}\n",
                "D=0\n",
                f"@CEND_{lineCount}\n",
                "0;JMP\n",
                f"(TRUE_{lineCount})\n",
                "D=-1\n",
                f"(CEND_{lineCount})\n",
                "@SP\n",
                "A=M-1\n",
                "M=D\n",
            ])

    def writePushPop(self, commandType, segment, index):
        segmentDict = {
            "local": "LCL",
            "argument": "ARG",
            "this": "THIS",
            "that": "THAT",
        }
        pointerList = ["THIS","THAT"]

        if commandType == "C_PUSH":
            self.outputFileStream.writelines([
                f"\n//push {segment} {index}\n",
            ])

            if segment in segmentDict:
                self.outputFileStream.writelines([
                    f"@{segmentDict[segment]}\n",
                    "D=M\n",
                    f"@{index}\n",
                    "A=D+A\n",
                    "D=M\n",
                ])
            elif segment == "pointer":
                self.outputFileStream.writelines([
                    f"@{pointerList[int(index)]}\n",
                    "D=M\n",
                ])
            elif segment == "temp":
                self.outputFileStream.writelines([
                    f"@R{5+int(index)}\n",
                    "D=M\n",
                ])
            elif segment == "constant":
                self.outputFileStream.writelines([
                    f"@{index}\n",
                    "D=A\n",
                ])
            elif segment == "static":
                self.outputFileStream.writelines([
                    f"@{self.fileName}.{index}\n",
                    "D=M\n",
                ])

            self.outputFileStream.writelines([
                "@SP\n",
                "A=M\n",
                "M=D\n",
                "@SP\n",
                "M=M+1\n",
            ])
        else:
            p1 = [
                "@SP\n",
                "AM=M-1\n",
                "D=M\n",
            ]

            self.outputFileStream.writelines([
                f"\n//pop {segment} {index}\n",
            ])

            if segment in segmentDict:
                self.outputFileStream.writelines([
                    f"@{segmentDict[segment]}\n",
                    "D=M\n",
                    f"@{index}\n",
                    "D=D+A\n",
                    "@R13\n",
                    "M=D\n",
                    *p1,
                    "@R13\n",
                    "A=M\n",
                    "M=D\n",
                ])
            elif segment == "pointer":
                self.outputFileStream.writelines([
                    *p1,
                    f"@{pointerList[int(index)]}\n",
                    "M=D\n",
                ])
            elif segment == "temp":
                self.outputFileStream.writelines([
                    *p1,
                    f"@R{5+int(index)}\n",
                    "M=D\n",
                ])
            elif segment == "static":
                self.outputFileStream.writelines([
                    *p1,
                    f"@{self.fileName}.{index}\n",
                    "M=D\n",
                ])

    def writeLabel(self, label):
        self.outputFileStream.writelines([
            f'\n//label {label}\n',
            f"({self.functionName}${label})\n",
        ])

    def writeGoto(self, label):
        self.outputFileStream.writelines([
            f'\n//goto {label}\n',
            f"@{self.functionName}${label}\n",
            "0;JMP\n",
        ])

    def writeIf(self, label):
        self.outputFileStream.writelines([
            f'\n//if-goto {label}\n',
            "@SP\n",
            "AM=M-1\n",
            "D=M\n",
            f"@{self.functionName}${label}\n",
            "D;JNE\n",
        ])

    def writeFunction(self, functionName, nVars):
        self.functionName = functionName

        self.outputFileStream.writelines([
            f'\n//function {functionName} {nVars}\n',
            f"({functionName})\n",
            f"@{nVars}\n",
            "D=A\n",
            f"({functionName}$LCL_INIT)\n",
            f"@{functionName}$LCL_SKIP\n",
            "D;JEQ\n",
            "@SP\n",
            "A=M\n",
            "M=0\n",
            "@SP\n",
            "M=M+1\n",
            "D=D-1\n",
            f"@{functionName}$LCL_INIT\n",
            "0;JMP\n",
            f"({functionName}$LCL_SKIP)\n",
        ])

    def writeCall(self, functionName, nArgs, callCount):
        # why does this "push returnAddress" pushes the linecount of the vmcode in vm emulator as return address, how does it translate to assembly

        com = [
            "@SP\n",
            "A=M\n",
            "M=D\n",
            "@SP\n",
            "M=M+1\n",
        ]

        self.outputFileStream.writelines([
            f'\n//call {functionName} {nArgs}\n',

            f"@{functionName}$ret{callCount}\n",
            "D=A\n",
            *com,

            "@LCL\n",
            "D=M\n",
            *com,
            "@ARG\n",
            "D=M\n",
            *com,
            "@THIS\n",
            "D=M\n",
            *com,
            "@THAT\n",
            "D=M\n",
            *com,

            f"@{5 + int(nArgs)}\n",
            "D=A\n",
            "@SP\n",
            "D=M-D\n",
            "@ARG\n",
            "M=D\n",

            "@SP\n",
            "D=M\n",
            "@LCL\n",
            "M=D\n",

            f"@{functionName}\n",
            "0;JMP\n"
            
            f"({functionName}$ret{callCount})\n", # what does the running number mean, it should be callCount
        ])

    def writeReturn(self):
        com = lambda seg: [
            "@R13\n",
            "AM=M-1\n",
            "D=M\n",
            f"@{seg}\n",
            "M=D\n",
        ]

        self.outputFileStream.writelines([
            f'\n//return\n'

            "@LCL\n",
            "D=M\n",
            "@R13\n",
            "M=D\n",
            "@5\n",
            "A=D-A\n",
            "D=M\n",
            "@R14\n",
            "M=D\n",

            "@SP\n",
            "AM=M-1\n",
            "D=M\n",
            "@ARG\n",
            "A=M\n",
            "M=D\n",

            "@ARG\n",
            "D=M+1\n",
            "@SP\n",
            "M=D\n",

            *com("THAT"),
            *com("THIS"),
            *com("ARG"),
            *com("LCL"),

            "@R14\n",
            "A=M\n",
            "0;JMP\n"
        ])
    
    def close(self):
        self.outputFileStream.close()