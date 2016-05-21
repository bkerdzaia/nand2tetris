#!/usr/bin/evn python3
from Parser import Parser
from os import path


class CodeWriter:
    """
    Translates VM commands into Hack assembly code.
    """

    __TRUE = -1
    __FALSE = 0

    def __init__(self, file_name):
        """  Opens the output file/stream and gets ready to write into it. """
        self.__stream = open(file_name, "w")
        self.__vm_file_name = None
        self.__function_name = None
        self.__add_suffix_recursive_function = ""
        self.__label_index = 0
        self.__binary_arithmetic_commands = {"add": "+", "sub": "-", "and": "&", "or": "|"}
        self.__unary_arithmetic_commands = {"neg": "-", "not": "!"}
        self.__comparative_commands = {"lt": "JLT", "gt": "JGT", "eq": "JEQ"}
        self.__segment_offsets = {"pointer": 3, "temp": 5}
        self.__pointers_offsets = {"this": 3, "local": 1, "argument": 2, "that": 4}

    def set_file_name(self, file_name):
        """ Informs the code writer that the translation of a new VM file is started. """
        self.__vm_file_name = file_name[len(path.dirname(file_name)) + 1:file_name.find(".vm")]

    # decrements sp pointer and saves to A register and memory
    @staticmethod
    def __decrement_SP():
        return "@SP\n" \
               "AM=M-1\n"

    # increments sp pointer and saves to A register and memory
    @staticmethod
    def __increment_SP():
        return "@SP\n" \
               "AM=M+1\n"

    # pops two items from stack and first popped item saves to D register
    @staticmethod
    def __pop_two_items():
        return CodeWriter.__decrement_SP() + "D=M\n" + CodeWriter.__decrement_SP()

    # creates a label and writes boolean value in the stack where sp points to and jumps to CONTINUE label
    def __write_boolean_value(self, value):
        return "(" + self.__change_label("WRITE") + str(value) + ")\n" + "@SP\n" + "A=M\n" + \
               "M=" + str(value) + "\n" + "@" + self.__change_label("CONTINUE") + "\n" + "0;JMP\n"

    # make all labels unique
    def __change_label(self, name):
        return name + str(self.__label_index) + "."

    def write_arithmetic(self, command):
        """ Writes the assembly code that is the translation of the given arithmetic command. """
        command_type = self.__unary_arithmetic_commands.get(command)
        if command_type is not None:  # unary operation
            self.__stream.write(self.__decrement_SP() + "M=" + command_type + "M\n" + self.__increment_SP())
            return
        command_type = self.__binary_arithmetic_commands.get(command)
        if command_type is not None:  # binary operations except comparative
            self.__stream.write(self.__pop_two_items() + "M=M" +
                                command_type + "D\n" + self.__increment_SP())
            return
        command_type = self.__comparative_commands.get(command)
        if command_type is not None:
            self.__stream.write(self.__pop_two_items() + "D=M-D\n" + "@" + self.__change_label("WRITE") +
                                str(self.__TRUE) + "\n" + "D;" + command_type + "\n" + "@" +
                                self.__change_label("WRITE") + str(self.__FALSE) + "\n" + "0;JMP\n" +
                                self.__write_boolean_value(self.__FALSE) + self.__write_boolean_value(self.__TRUE) +
                                "(" + self.__change_label("CONTINUE") + ")\n" + self.__increment_SP())
            self.__label_index += 1
            return
        raise Exception("Not valid arithmetic command: " + command)

    # push the value from D register into stack and increment stack pointer
    def __push(self):
        return self.__increment_SP() + "A=A-1\n" + "M=D\n"

    def write_push_pop(self, command, segment, index):
        """
        Writes the assembly code that is the translation of the given command,
        where command is either C_PUSH or C_POP.
        """
        if self.__vm_file_name is None:
            raise Exception("file names is not set")
        if not index.isdigit():
            raise Exception("not valid index expression " + index + ", expected digit")
        if command == Parser.C_PUSH:
            if segment == "constant":
                self.__stream.write("@" + index + "\n" + "D=A\n" + self.__push())
                return
            if segment == "static":
                self.__stream.write("@" + self.__vm_file_name + "." + index + "\n" + "D=M\n" + self.__push())
                return
            offset = self.__segment_offsets.get(segment)
            if offset is not None:
                self.__stream.write("@" + str(offset + int(index)) + "\n" + "D=M\n" + self.__push())
                return
            offset = self.__pointers_offsets.get(segment)
            if offset is None:
                raise Exception("Not valid segment - " + segment)
            self.__stream.write("@" + str(offset) + "\n" + "D=M\n" + "@" + str(index) + "\n" +
                                "A=D+A\n" + "D=M\n" + self.__push())
            return
        if command == Parser.C_POP:
            if segment == "static":
                self.__stream.write(self.__decrement_SP() + "D=M\n" + "@" + self.__vm_file_name + "." + index + "\n" + "M=D\n")
                return
            offset = self.__segment_offsets.get(segment)
            if offset is not None:
                self.__stream.write(self.__decrement_SP() + "D=M\n" + "@" + str(offset + int(index)) + "\n" + "M=D\n")
                return
            offset = self.__pointers_offsets.get(segment)
            if offset is None:
                raise Exception("Not valid segment - " + segment)
            self.__stream.write("@" + str(offset) + "\n" + "D=M\n" + "@" + str(index) + "\n" +
                                "D=D+A\n" + "@R13\n" + "M=D\n" + self.__decrement_SP() + "D=M\n" +
                                "@R13\n" + "A=M\n" + "M=D\n")
            return
        raise Exception("exception in " + self.write_push_pop.__name__ + " not valid command argument")

    def close(self):
        """ Closes the output file. """
        self.__stream.close()
