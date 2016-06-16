

class VMWriter:
    """
    VMWriter: Emits VM commands into a file, using the VM command syntax.
    """

    CONST = "constant"
    ARG = "argument"
    LOCAL = "local"
    STATIC = "static"
    THIS = "this"
    THAT = "that"
    POINTER = "pointer"
    TEMP = "temp"

    ADD = "add"
    SUB = "sub"
    NEG = "neg"
    EQ = "eq"
    GT = "gt"
    LT = "lt"
    AND = "and"
    OR = "or"
    NOT = "not"

    def __init__(self, output_file):
        """ Creates a new file and prepares it for writing. """
        self.__stream = open(output_file, "w")

    def write_push(self, segment, index):
        """ Writes a VM push command. """
        self.__stream.write("push " + segment + " " + str(index) + "\n")

    def write_pop(self, segment, index):
        """ Writes a VM pop command. """
        self.__stream.write("pop " + segment + " " + str(index) + "\n")

    def write_arithmetic(self, command):
        """ Writes a VM arithmetic command. """
        self.__stream.write(command + "\n")

    def write_label(self, label):
        """ Writes a VM label command. """
        self.__stream.write("label " + label + "\n")

    def write_goto(self, label):
        """ Writes a VM goto command. """
        self.__stream.write("goto " + label + "\n")

    def write_if(self, label):
        """ Writes a VM If-goto command. """
        self.__stream.write("if-goto " + label + "\n")

    def write_call(self, name, n_args):
        """ Writes a VM call command. """
        self.__stream.write("call " + name + " " + str(n_args) + "\n")

    def write_function(self, name, n_locals):
        """ Writes a VM function command. """
        self.__stream.write("function " + name + " " + str(n_locals) + "\n")

    def write_return(self):
        """ Writes a VM return command."""
        self.__stream.write("return\n")

    def close(self):
        """ Closes the output file. """
        self.__stream.close()
