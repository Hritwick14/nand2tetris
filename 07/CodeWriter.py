class CodeWriter:
    def __init__(self, outputPath, fileName):
        self.fileName = fileName
        self.outputFileStream = open(outputPath, "w")

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
    
    def close(self):
        self.outputFileStream.close()