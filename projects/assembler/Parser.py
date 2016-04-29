#!/usr/bin/evn python3

class Parser:
    """
    Encapsulates access to the input code. Reads an assembly language command,
    parses it, and provides convenient access to the command’s components
    (fields and symbols). In addition, removes all white space and comments.
    """

    __current = None
    __linesList = None
    __currentLine = 0
    __symbol = None
    __comp = None
    __dest = None
    __jump = None

    A_COMMAND = 1
    C_COMMAND = 2
    L_COMMAND = 3

    def __init__(self, file):
        """  Opens the input file/stream and gets ready to parse it. """
        self.__linesList = file.read().split("\n")

    def hasMoreCommands(self):
        """ Are there more commands in the input? """
        return self.__currentLine < len(self.__linesList)

    def reset(self):
        """ start reading file content again """
        self.__currentLine = 0

    def advance(self):
        """
        Reads the next command from the input and makes it the current
        command. Should be called only if hasMoreCommands() is true.
        """
        self.__current = self.__linesList[self.__currentLine]
        self.__currentLine += 1

    def commandType(self):
        """
        Returns the type of the current command:
        A_COMMAND for @Xxx where Xxx is either a symbol or a decimal number
        C_COMMAND for dest=comp;jump
        L_COMMAND (actually, pseudocommand) for (Xxx) where Xxx is a symbol.
        """
        if self.__current is None:
            return None
        self.__symbol, self.__comp, self.__dest, self.__jump = None, None, None, None
        command = self.__current.strip()
        commentStartIndex = command.find("//")
        if commentStartIndex == 0:
            return None
        if commentStartIndex != -1:
            command = command[:commentStartIndex].strip()
        atSign = command.find("@")
        if atSign == 0:
            self.__symbol = command[1:]
            return self.A_COMMAND
        elif atSign != -1:
            self.__symbol = None
            return self.A_COMMAND
        compSign = command.find("=")
        if compSign != -1:
            self.__comp, self.__dest = command[compSign+1:], command[:compSign]
            return self.C_COMMAND
        jumpSign = command.find(";")
        if jumpSign != -1:
            self.__jump, self.__comp = command[jumpSign+1:], command[:jumpSign]
            return self.C_COMMAND
        if command.startswith("(") and command.endswith(")"):
            self.__symbol = command[1:len(command)-1]
            return self.L_COMMAND
        return None

    def symbol(self):
        """
        Returns the symbol or decimal Xxx of the current command
        @Xxx or (Xxx). Should be called only when commandType() is
        A_COMMAND or L_COMMAND.
        """
        return self.__symbol

    def dest(self):
        """
        Returns the dest mnemonic in the current C-command (8 possibilities).
        Should be called only when commandType() is C_COMMAND.
        """
        return self.__dest

    def comp(self):
        """
        Returns the comp mnemonic in the current C-command (28 possibilities).
        Should be called only when commandType() is C_COMMAND.
        """
        return self.__comp

    def jump(self):
        """
        Returns the jump mnemonic in the current C-command (8 possibilities).
        Should be called only when commandType() is C_COMMAND.
        """
        return self.__jump


