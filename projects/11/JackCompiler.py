#!/usr/bin/evn python3
import sys
import os
from JackTokenizer import JackTokenizer
from CompilationEngine import CompilationEngine


class JackCompiler:

    """
    The compiler operates on a given source, where source is a file name of the
    form Xxx.jack. From Xxx.jack input file, the compiler creates a JackTokenizer
    and an output Xxx.vm file. Next, the compiler uses the CompilationEngine,
    SymbolTable, and VMWriter modules to write the output file.
    """

    def __init__(self, input_file):
        """
        :param input_file: file to compile
        :return:
        """
        self.__file = open(input_file)

    def compile(self):
        """
        compiles the .jack file to .vm file
        :return:
        """
        tok = JackTokenizer(self.__file)
        input_file = self.__file.name
        eng = CompilationEngine(tok, input_file.replace(".jack", ".vm"))
        eng.compile_class()

    def close(self):
        """
        :return: closes input file
        """
        self.__file.close()


# initializes JackCompiler and compiles it
def compile_file(file_name):
    jack_compiler = JackCompiler(file_name)
    jack_compiler.compile()
    jack_compiler.close()


# compiles
def compile_files(path):
    if os.path.isdir(path):
        for files in os.listdir(path):
            if files.find(".jack") != -1:
                compile_file(path + "\\" + files)
    elif path.find(".jack") != -1:
        compile_file(path)
    else:
        raise Exception("can't compile " + path)

# main program the compiles jack program
if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Not valid argument number")
    try:
        compile_files(sys.argv[1])
        print("finished successfully")
    except Exception as e:
        print(e)
