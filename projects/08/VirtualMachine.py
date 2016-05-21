#!/usr/bin/evn python3
from Parser import Parser
from CodeWriter import CodeWriter
import sys
import os


# opens a vm_file, parses it and writes an assembly code in writer
def write_from_vm_file(vm_file, writer):
    file = open(vm_file)
    parser = Parser(file)
    file.close()
    writer.set_file_name(vm_file)
    while parser.has_more_commands():
        parser.advance()
        command = parser.command_type()
        if command == parser.C_ARITHMETIC:
            writer.write_arithmetic(parser.arg1())
        elif command == parser.C_POP or command == parser.C_PUSH:
            writer.write_push_pop(command, parser.arg1(), parser.arg2())
        elif command == parser.C_LABEL:
            writer.write_label(parser.arg1())
        elif command == parser.C_GOTO:
            writer.write_goto(parser.arg1())
        elif command == parser.C_IF:
            writer.write_if(parser.arg1())
        elif command == parser.C_CALL:
            writer.write_call(parser.arg1(), parser.arg2())
        elif command == parser.C_FUNCTION:
            writer.write_function(parser.arg1(), parser.arg2())
        elif command == parser.C_RETURN:
            writer.write_return()
        else:
            raise Exception("not supported command " + command)


# if the path is directory, all .vm file in this directory is translated to
# assembly code in one file. If the path is a .vm file, simply translates to assembly file
def generate_assembly_code(path):
    if os.path.isdir(path):
        writer = CodeWriter(path + "\\" + os.path.basename(path) + ".asm")
        writer.write_init()
        for files in os.listdir(path):
            if files.find(".vm") != -1:
                write_from_vm_file(path + "\\" + files, writer)
        writer.close()
    elif path.find(".vm") != -1:
        writer = CodeWriter(path[:path.find(".vm")] + ".asm")
        writer.write_init()
        write_from_vm_file(path, writer)
        writer.close()
    else:
        raise Exception("can't generate assembly code")
    print("finished successfully")


# main program, generates assembly code.
if __name__ == '__main__':
    if len(sys.argv) != 2:
        raise Exception("Not valid argument number")
    try:
        generate_assembly_code(sys.argv[1])
    except Exception as e:
        print(e)
