#!/usr/bin/evn python3
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine
import os
import sys

"""
The analyzer program operates on a given source, where source is either a file name
of the form Xxx.jack or a directory name containing one or more such files. For
each source Xxx.jack file, the analyzer goes through the following logic:

1. Create a JackTokenizer from the Xxx.jack input file.
2. Create an output file called Xxx.xml and prepare it for writing.
3. Use the CompilationEngine to compile the input JackTokenizer into the output file.
"""


# makes terminal
def generate_terminal(terminal_type, value):
    return "<" + terminal_type + "> " + value + " </" + terminal_type + ">\n"


# generates a xml tree  
def generate_xml_token_code(filename):
    name = os.path.basename(filename).replace(".jack", "T.xml")
    dirname = os.path.dirname(filename) + "2/"
    xml = open(dirname + name, "w")
    xml.write("<tokens>\n")
    stream = open(filename)
    token = JackTokenizer(stream)
    while token.has_more_tokens():
        token.advance()
        tok_type = token.token_type()
        if tok_type == token.KEYWORD:
            xml.write(generate_terminal("keyword", token.key_word()))
            print("keyword:", token.key_word())
        elif tok_type == token.SYMBOL:
            xml.write(generate_terminal("symbol", token.symbol()))
            print("symbol:", token.symbol())
        elif tok_type == token.STRING_CONST:
            xml.write(generate_terminal("stringConstant", token.string_val()))
            print("string const:", token.string_val())
        elif tok_type == token.INT_CONST:
            xml.write(generate_terminal("integerConstant", token.int_val()))
            print("int const:", token.int_val())
        elif tok_type == token.IDENTIFIER:
            xml.write(generate_terminal("identifier", token.identifier()))
            print("identifier:", token.identifier())
        else:
            print("not valid token:", tok_type)
    xml.write("</tokens>")
    stream.close()


# generate a xml tree for tokenizer module
def generate_xml_token_dir(dirname):
    for files in os.listdir(dirname):
        if files.find(".jack") != -1:
            generate_xml_token_code(dirname + "\\" + files)

# filename = "ArrayTest\Main.jack"
# generate_xml_token_code(filename)
# generate_xml_token_dir("ExpressionlessSquare")


# Create a JackTokenizer from the Xxx.jack input file.
# Pass an output file name called Xxx.xml to compilation engine and prepare it for writing.
# Use the CompilationEngine to compile the input JackTokenizer into the output file.
def generate_xml_code_parser(dirname, filename):
    file = open(dirname + "\\" + filename)
    tokenizer = JackTokenizer(file)
    engine = CompilationEngine(tokenizer, dirname + "2\\" + filename.replace(".jack", ".xml"))
    engine.compile_class()
    file.close()
    engine.close()


# generate a xml tree for parser module
def generate_xml_parser(dirname):
    for files in os.listdir(dirname):
        if files.find(".jack") != -1:
            generate_xml_code_parser(dirname, files)

# main program
if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Not valid argument number")
    try:
        generate_xml_parser(sys.argv[1])
        print("finished successfully")
    except Exception as e:
        print(e)
