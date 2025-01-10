import os
from Parser import Parser
from CodeWriter import CodeWriter

# After executing the program enter the full file path and the .asm file will be created in same directory
filePath = input("Enter Virtual Emulator File name(xxx.vm): ")

fileDirectory = os.path.dirname(filePath)
fileName = os.path.splitext(os.path.basename(filePath))[0]

result = ""
with open(filePath, "r") as f1:
    parser = Parser(f1)
    codeWriter = CodeWriter(fileDirectory + "/" + fileName + ".asm", fileName)

    lineCount = -1
    while parser.hasMoreLines():
        parser.advance()
        lineCount += 1
        
        ct = parser.commandType()
        if ct == "C_PUSH" or ct == "C_POP":
            codeWriter.writePushPop(ct, *parser.arg2())
        else:
            codeWriter.writeArithmetic(parser.arg1(), lineCount)

    codeWriter.close()