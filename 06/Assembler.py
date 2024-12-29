import os
from Parser import Parser
from Code import Code
from SymbolTable import SymbolTable

# After executing the program enter the full file path and the .hack file will be created in same directory
filePath = input("Enter Hack Assembly File name(xxx.asm): ")

fileDirectory = os.path.dirname(filePath)
fileName = os.path.splitext(os.path.basename(filePath))[0]

result = ""
with open(filePath, "r") as f1:
    parser = Parser(f1)
    symbolTable = SymbolTable()
    code = Code()

    lineCount = -1

    while parser.hasMoreLines():
        parser.advance()

        if parser.instructionType() == "L_INSTRUCTION":
            symbolTable.addEntry(parser.symbol(), lineCount + 1)
        else:
            lineCount += 1

    f1.seek(0)
    varAddress = 16

    while parser.hasMoreLines():
        parser.advance()

        if parser.instructionType() == "A_INSTRUCTION":
            s = parser.symbol()
            c = ""
            if s.isnumeric():
                c = code.decimalToBinary(parser.symbol())
            else:
                if symbolTable.contains(s):
                    c = code.decimalToBinary(symbolTable.getAddress(parser.symbol()))
                else:
                    symbolTable.addEntry(s,varAddress)
                    c = code.decimalToBinary(varAddress)
                    varAddress += 1

            result += c + "\n"
        elif parser.instructionType() == "C_INSTRUCTION":
            dt = code.dest(parser.dest())
            cp = code.comp(parser.comp())
            jp = code.jump(parser.jump())

            result += "111" + cp + dt + jp + "\n"

with open(fileDirectory + "/" + fileName + ".hack", "w", newline="\n") as f2:
    f2.write(result[:-1])