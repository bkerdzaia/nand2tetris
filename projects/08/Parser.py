#!/usr/bin/evn python3
from multiprocessing.spawn import prepare

from builtins import print


class Parser:
    """
    Handles the parsing of a single .vm file, and encapsulates access to the input
    code. It reads VM commands, parses them, and provides convenient access to their
    components. In addition, it removes all white space and comments.
    """

    C_ARITHMETIC = 1
    C_PUSH = 2
    C_POP = 3
    C_LABEL = 4
    C_GOTO = 5
    C_IF = 6
    C_FUNCTION = 7
    C_RETURN = 8
    C_CALL = 9

    def __init__(self, stream):
        """ Opens the output file/stream and gets ready to parse it. """
        self.__lines = list(filter(lambda x: x != '', [self.__remove_comment(line) for line in stream.read().split("\n")]))
        self.__line_index = 0
        self.__current_line = None
        self.__arg1 = None
        self.__arg2 = None
        self.__command_three_types = {"push": self.C_PUSH, "pop": self.C_POP, "function": self.C_FUNCTION, "call": self.C_CALL}
        self.__command_two_types = {"label": self.C_LABEL, "goto": self.C_GOTO, "if-goto": self.C_IF}
        self.__command_arithmetic = ["add", "sub", "neg", "eq", "gt", "lt", "and", "or", "not"]

    @staticmethod
    def __remove_comment(line):
        """ removes comments """
        comment_index = line.find("//")
        return line[:comment_index if comment_index != -1 else len(line)].strip()

    def has_more_commands(self):
        """ Are there more commands in the input? """
        return self.__line_index != len(self.__lines)

    def advance(self):
        """
        Reads the next command from the input and makes it the current command.
        Should be called only if hasMoreCommands is true.
        Initially there is no current command.
        """
        self.__current_line = self.__lines[self.__line_index]
        self.__line_index += 1

    def command_type(self):
        """ Returns the type of the current VM command. """
        self.__arg1, self.__arg2 = None, None
        commands = self.__current_line.split(" ")
        if len(commands) == 1:
            if commands[0] == "return":
                return self.C_RETURN
            if commands[0] not in self.__command_arithmetic:
                return None
            self.__arg1 = commands[0]
            return self.C_ARITHMETIC
        if len(commands) == 2:
            self.__arg1 = commands[1]
            return self.__command_two_types.get(commands[0])
        if len(commands) == 3:
            self.__arg1, self.__arg2 = commands[1], commands[2]
            return self.__command_three_types.get(commands[0])
        return None

    def arg1(self):
        """
        Returns the first arg. of the current command.
        In the case of C_ARITHMETIC, the command itself
        (add, sub, etc.) is returned. Should not be called
        if the current command is C_RETURN.
        """
        return self.__arg1

    def arg2(self):
        """
        Returns the second argument of the current
        command. Should be called only if the current
        command is C_PUSH, C_POP, C_FUNCTION, or
        C_CALL.
        """
        return self.__arg2
