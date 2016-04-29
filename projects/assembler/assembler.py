#!/usr/bin/evn python3

from Parser import Parser
from Code import Code
import sys

# add constant symbols to symbol table
def initSymbolTable():
    symbolTable = {"SCREEN": 16384, "KBD": 24576, "SP": 0, "LCL": 1, "ARG": 2, "THIS": 3, "THAT": 4}
    for i in range(0, 16):
        symbolTable["R" + str(i)] = i
    return symbolTable

# check if given value is none and if so raise an exception with given message
def checkForNull(value, exceptionMessage):
    if value is None:
        raise Exception(exceptionMessage)

# iterate firstly through file and add labels to symbol table
def addLabelsToSymbolTable(parser, symbolTable):
    countLines = 0
    while parser.hasMoreCommands():
        parser.advance()
        if parser.commandType() == parser.A_COMMAND or parser.commandType() == parser.C_COMMAND:
            countLines += 1
        if parser.commandType() == parser.L_COMMAND:
            symbolTable[parser.symbol()] = countLines

# parses the symbol to decimal number and if it can't parse
# checks if the symbol is in symbol table and if not adds it
# with its memory location and increases this location.
# returns the tuple of the value of symbol from symbol table
# and memory location
def getSymbolValue(symbol, symbolTable, currentMemoryLocation):
    try:
        return int(symbol), currentMemoryLocation
    except ValueError:
        if symbolTable.get(symbol) is None:
            symbolTable[symbol] = currentMemoryLocation
            currentMemoryLocation += 1
        return symbolTable[symbol], currentMemoryLocation

# construct a A-incstruction
# return 16-bit number which starts at least one zero and memory
# location as tuple
def constructAInstruction(symbol, symbolTable, currentMemoryLocation):
    decimalNumber, currentMemoryLocation = getSymbolValue(symbol, symbolTable, currentMemoryLocation)
    binaryNumber = bin(decimalNumber)[2:]
    if len(binaryNumber) >= 15:
        binaryNumber = binaryNumber[len(binaryNumber)-15:]
    return "0"*(16-len(binaryNumber)) + binaryNumber, currentMemoryLocation

# constructs a C-instruction
# checks if comp, jump, and dest binary values is valid (is
# not None) and returns 16-bit binary incstruction. if isn't
# valid raises an exception.
def constructCInstruction(parser, linesNumber):
    codeJump = Code.jump(Code, parser.jump())
    checkForNull(codeJump,"exception at line: " + str(linesNumber) + " not valid jump symbol")
    codeComp = Code.comp(Code, parser.comp())
    checkForNull(codeComp,"exception at line: " + str(linesNumber) + " not valid compute symbol")
    codeDest = Code.dest(Code, parser.dest())
    checkForNull(codeDest,"exception at line: " + str(linesNumber) + " not valid destination symbol")
    return "111" + codeComp + codeDest + codeJump

# opens the file with the exctension .asm, parses it
# and generates new .hack file with 16-bit values of
# instructions. if there was problem in parsing
# raises an exception.
def main(fileName):
    file = open(fileName)
    dotIndex = file.name.find(".asm")
    if dotIndex == -1:
        raise Exception("file has not valid extension, expected - .asm")
    parser = Parser(file)
    toWriteContent = ""
    symbolTable = initSymbolTable()
    addLabelsToSymbolTable(parser, symbolTable)
    parser.reset()
    currentMemoryLocation = 16
    lines = 1
    while parser.hasMoreCommands():
        parser.advance()
        if parser.commandType() == parser.A_COMMAND:
            checkForNull(parser.symbol(), "in line " + str(lines) + " expression expected")
            writeString, currentMemoryLocation = constructAInstruction(parser.symbol(), symbolTable, currentMemoryLocation)
            toWriteContent += writeString+'\n'
        elif parser.commandType() == parser.C_COMMAND:
            toWriteContent += constructCInstruction(parser, lines)+'\n'
        lines += 1
    toWrite = open(file.name[:dotIndex] + ".hack", "w")
    toWrite.write(toWriteContent)
    file.close()
    toWrite.close()
    print("finish working")

# main program
# reads the text file name from.
# if there was an exception during reading prints it.
if __name__ == '__main__':
    if len(sys.argv)==2:
        try:
            main(sys.argv[1])
        except Exception as e:
            print(e)