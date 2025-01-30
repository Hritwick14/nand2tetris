import os
from Parser import Parser
from CodeWriter import CodeWriter

# After executing the program enter either the full file path or the folder and the .asm file will be created in same directory
inputPath = input("Enter the path for either a Virtual Emulator File(xxx.vm) or Folder with multiple .vm files: ")

filesList = []
if inputPath.endswith(".vm"):
    fileDirectory = os.path.dirname(inputPath)
    filesList.append(inputPath)
else:
    fileDirectory = inputPath
    files = [x for x in os.listdir(inputPath) if x.endswith(".vm")]
    if "Sys.vm" not in files:
        raise "Sys.vm file missing"
    
    filesList = [f"{inputPath}/{x}" for x in files]

asmFileName = os.path.splitext(os.path.basename(inputPath))[0]
codeWriter = CodeWriter(f"{fileDirectory}/{asmFileName}.asm")

if not inputPath.endswith(".vm"):
    codeWriter.writeInit()

lineCount = -1
callCount = 0
for filePath in filesList:
    currentFileName = os.path.splitext(os.path.basename(filePath))[0]
    codeWriter.setFileName(currentFileName)

    with open(filePath, "r") as f1:
        parser = Parser(f1)

        while parser.hasMoreLines():
            parser.advance()
            lineCount += 1
            
            ct = parser.commandType()
            if ct == "C_PUSH" or ct == "C_POP":
                codeWriter.writePushPop(ct, *parser.arg2())
            elif ct == "C_LABEL":
                codeWriter.writeLabel(parser.arg2()[0])
            elif ct == "C_GOTO":
                codeWriter.writeGoto(parser.arg2()[0])
            elif ct == "C_IF":
                codeWriter.writeIf(parser.arg2()[0])
            elif ct == "C_FUNCTION":
                codeWriter.writeFunction(*parser.arg2())
            elif ct == "C_CALL":
                callCount += 1
                codeWriter.writeCall(*parser.arg2(), callCount)
            elif ct == "C_RETURN":
                codeWriter.writeReturn()
            else:
                codeWriter.writeArithmetic(parser.arg1(), lineCount)

codeWriter.close()