#!/usr/bin/evn python3
from JackTokenizer import JackTokenizer
from VMWriter import VMWriter
from SymbolTable import SymbolTable


class CompilationEngine:
    """
    This class does the compilation itself. It reads its input from a JackTokenizer and
    writes its output into a VMWriter. It is organized as a series of compilexxx() routines,
    where xxx is a syntactic element of the Jack language. The contract between
    these routines is that each compilexxx() routine should read the syntactic construct
    xxx from the input, advance() the tokenizer exactly beyond xxx, and emit to the
    output VM code effecting the semantics of xxx. Thus compilexxx() may only be
    called if indeed xxx is the next syntactic element of the input. If xxx is a part of an
    expression and thus has a value, the emitted code should compute this value and
    leave it at the top of the VM stack.
    """

    def __init__(self, input_tokenizer, output_vm_writer):
        """
        Creates a new compilation engine with the given input and output.
        The next routine called must be compile_class().
        """
        self.__tokenizer = input_tokenizer
        self.__vm_writer = VMWriter(output_vm_writer)
        self.__symbol_table = SymbolTable()
        self.__class_name = None
        self.__count_while_cycle = -1
        self.__count_if = -1
        self.__op = {'+': VMWriter.ADD, '-': VMWriter.SUB, '*': None, '/': None, '&amp;': VMWriter.AND,
                     '|': VMWriter.OR, '&lt;': VMWriter.LT, '&gt;': VMWriter.GT, '=': VMWriter.EQ}
        self.__unary_op = {'-': VMWriter.NEG, '~': VMWriter.NOT}
        self.__key_word_constant = ['true', 'false', 'null', 'this']

    @staticmethod
    def __check_name(name, name_to_check):
        if name != name_to_check:
            raise Exception("Expected " + name + " but got " + name_to_check)
    
    # advances tokenizer if it has more tokens, if not raises exception
    def __advance_tokenizer(self):
        if not self.__tokenizer.has_more_tokens():
            raise Exception("error, tokenizer should have next element")
        self.__tokenizer.advance()

    # className, varName, subroutineName: identifier
    # returns the name of identifier
    def __compile_identifier_name(self):
        self.__advance_tokenizer()
        if self.__tokenizer.token_type() != JackTokenizer.IDENTIFIER:
            raise Exception("expected identifier")
        return self.__tokenizer.identifier()

    # class: 'class' className '{' classVarDec* subroutineDec* '}'
    def compile_class(self):
        """ Compiles a complete class. """
        self.__advance_tokenizer()
        if self.__tokenizer.token_type() != JackTokenizer.KEYWORD:
            raise Exception("expected keyword class")
        self.__check_name("class", self.__tokenizer.key_word())
        self.__class_name = self.__compile_identifier_name()
        self.__compile_symbol("{")
        self.compile_class_var_dec()
        self.compile_subroutine()
        self.__compile_symbol("}")
        if self.__tokenizer.has_more_tokens():
            raise Exception("class shouldn't have tokens after }")

    # type: 'int' | 'char' | 'boolean' | className
    # if void is True type also is 'void'
    # returns the type of next token
    def __compile_type(self, void=False):
        self.__advance_tokenizer()
        token_type = self.__tokenizer.token_type()
        if token_type == JackTokenizer.IDENTIFIER:
            return self.__tokenizer.identifier()
        elif token_type == JackTokenizer.KEYWORD and self.__tokenizer.key_word() in ["int", "char", "boolean"]:
            return self.__tokenizer.key_word()
        elif void and token_type == JackTokenizer.KEYWORD and self.__tokenizer.key_word() == "void":
            return self.__tokenizer.key_word()
        else:
            raise Exception("expected 'type' of declared variables")

    # compile symbol, check if tokenizer has symbol type and it is same as symbol_name
    def __compile_symbol(self, symbol_name):
        self.__advance_tokenizer()
        token_type = self.__tokenizer.token_type()
        if token_type != JackTokenizer.SYMBOL or self.__tokenizer.symbol() != symbol_name:
            res = "token type " + str(token_type) + " symbol: " + str(self.__tokenizer.symbol()) + " "
            raise Exception("expected symbol '" + symbol_name + "' " + res)

    # compile (',' varName)*
    # adds variable names in var_list
    def __compile_more_var_names(self, var_list):
        self.__advance_tokenizer()
        if self.__tokenizer.token_type() != JackTokenizer.SYMBOL or self.__tokenizer.symbol() != ",":
            self.__tokenizer.back()
            return
        var_list.append(self.__compile_identifier_name())
        self.__compile_more_var_names(var_list)

    # type varName (',' varName)* ';'
    # inserts new variables to symbol table
    def __compile_var_body(self, keyword_kind):
        keyword_type = self.__compile_type()
        var_list = [self.__compile_identifier_name()]
        self.__compile_more_var_names(var_list)
        self.__compile_symbol(";")
        for keyword_name in var_list:
            self.__symbol_table.define(keyword_name, keyword_type, keyword_kind)

    # classVarDec: ('static'|'field') type varName (',' varName)* ';'
    def compile_class_var_dec(self):
        """ Compiles a static declaration or a field declaration. """
        self.__advance_tokenizer()
        token_type = self.__tokenizer.token_type()
        if token_type != JackTokenizer.KEYWORD or \
                (self.__tokenizer.key_word() != "static" and self.__tokenizer.key_word() != "field"):
            self.__tokenizer.back()
            return
        self.__compile_var_body(self.__tokenizer.key_word())
        self.compile_class_var_dec()

    # subroutineDec: ('constructor'|'function'|'method')
    #               ('void' | type) subroutineName '(' parameterList ')' '{' varDec* statements '}'
    def compile_subroutine(self):
        """ Compiles a complete method, function, or constructor. """
        self.__advance_tokenizer()
        token_type = self.__tokenizer.token_type()
        if token_type != self.__tokenizer.KEYWORD and self.__tokenizer.key_word() \
                not in ['constructor', 'function', 'method']:
            self.__tokenizer.back()
            return
        self.__symbol_table.start_subroutine()
        keyword_name = self.__tokenizer.key_word()
        if keyword_name == "method":
            self.__symbol_table.define("this", self.__class_name, SymbolTable.ARG)
        self.__compile_type(True)
        function_name = self.__class_name + "." + self.__compile_identifier_name()
        field_num = self.__symbol_table.var_count(SymbolTable.FIELD)
        self.__compile_symbol("(")
        self.compile_parameter_list()
        self.__compile_symbol(")")
        self.__compile_symbol("{")
        self.compile_var_dec()
        n_locals = self.__symbol_table.var_count(SymbolTable.VAR)
        self.__vm_writer.write_function(function_name, n_locals)
        if keyword_name == "constructor":
            self.__vm_writer.write_push(VMWriter.CONST, field_num)
            self.__vm_writer.write_call("Memory.alloc", 1)
            self.__vm_writer.write_pop(VMWriter.POINTER, 0)
        elif keyword_name == "method":
            self.__vm_writer.write_push(VMWriter.ARG, 0)
            self.__vm_writer.write_pop(VMWriter.POINTER, 0)
        self.compile_statements()
        self.__compile_symbol("}")
        self.compile_subroutine()

    # parameterList: ((type varName) (',' type varName)*)?
    def compile_parameter_list(self):
        """ Compiles a (possibly empty) parameter list, not including the enclosing ‘‘()’’. """
        self.__advance_tokenizer()
        token_type = self.__tokenizer.token_type()
        if token_type == JackTokenizer.IDENTIFIER:
            arg_type = self.__tokenizer.identifier()
        elif token_type == JackTokenizer.KEYWORD and self.__tokenizer.key_word() in ["int", "char", "boolean"]:
            arg_type = self.__tokenizer.key_word()
        else:
            self.__tokenizer.back()
            return
        arg_list = [(self.__compile_identifier_name(), arg_type)]
        self.__compile_parameter_more_args(arg_list)
        for arg_name, arg_type in arg_list:
            self.__symbol_table.define(arg_name, arg_type, SymbolTable.ARG)

    # (',' type varName)*
    def __compile_parameter_more_args(self, arg_list):
        self.__advance_tokenizer()
        if self.__tokenizer.token_type() != JackTokenizer.SYMBOL or self.__tokenizer.symbol() != ",":
            self.__tokenizer.back()
            return
        arg_type = self.__compile_type()
        arg_name = self.__compile_identifier_name()
        arg_list.append((arg_name, arg_type))
        self.__compile_parameter_more_args(arg_list)

    # varDec: 'var' type varName (',' varName)* ';'
    def compile_var_dec(self):
        """ Compiles a var declaration. """
        self.__advance_tokenizer()
        if self.__tokenizer.token_type() == JackTokenizer.KEYWORD and self.__tokenizer.key_word() != "var":
            self.__tokenizer.back()
            return
        self.__compile_var_body(SymbolTable.VAR)
        self.compile_var_dec()

    # statements: statement*
    def compile_statements(self):
        """ Compiles a sequence of statements, not including the enclosing ‘‘{}’’."""
        self.__advance_tokenizer()
        token_type = self.__tokenizer.token_type()
        if token_type != self.__tokenizer.KEYWORD:
            self.__tokenizer.back()
            return
        if self.__tokenizer.key_word() == "let":
            self.compile_let()
        elif self.__tokenizer.key_word() == "if":
            self.compile_if()
        elif self.__tokenizer.key_word() == "while":
            self.compile_while()
        elif self.__tokenizer.key_word() == "do":
            self.compile_do()
        elif self.__tokenizer.key_word() == "return":
            self.compile_return()
        else:
            raise Exception("not valid statement get:", token_type,
                            " type and keyword is:", self.__tokenizer.key_word())
        self.compile_statements()

    # doStatement: 'do' subroutineCall ';'
    def compile_do(self):
        """ Compiles a do statement. """
        self.__compile_subroutine_call()
        self.__compile_symbol(";")
        self.__vm_writer.write_pop(VMWriter.TEMP, 0)

    # subroutineCall: subroutineName '(' expressionList ')' |
    #                  (className | varName) '.' subroutineName '(' expressionList ')'
    def __compile_subroutine_call(self):
        identifier = self.__compile_identifier_name()
        function_name = self.__class_name + "." + identifier
        self.__advance_tokenizer()
        token_type = self.__tokenizer.token_type()
        if token_type != JackTokenizer.SYMBOL:
            raise Exception("expected symbol in subroutine call")
        this_arg = 0
        if self.__tokenizer.symbol() == ".":
            subroutine_name = self.__compile_identifier_name()
            if self.__symbol_table.kind_of(identifier) is not None:   # is varName
                this_arg = 1
                function_name = self.__symbol_table.type_of(identifier) + "." + subroutine_name
                self.__vm_writer.write_push(self.__convert_to_vm_write(self.__symbol_table.kind_of(identifier)),
                                            self.__symbol_table.index_of(identifier))
            else:  # is className
                function_name = identifier + "." + subroutine_name
        else:
            this_arg = 1
            self.__vm_writer.write_push(VMWriter.POINTER, 0)
            self.__tokenizer.back()
        self.__compile_symbol("(")
        num_arg = self.compile_expression_list()  # push arguments
        self.__compile_symbol(")")
        self.__vm_writer.write_call(function_name, num_arg + this_arg)

    # converts the kind of variable from symbol table to vm segment type
    @staticmethod
    def __convert_to_vm_write(kind):
        if kind == SymbolTable.STATIC:
            return VMWriter.STATIC
        elif kind == SymbolTable.FIELD:
            return VMWriter.THIS
        elif kind == SymbolTable.ARG:
            return VMWriter.ARG
        elif kind == SymbolTable.VAR:
            return VMWriter.LOCAL
        raise Exception(str(kind) + " is not supported")

    # letStatement: 'let' varName ('[' expression ']')? '=' expression ';'
    def compile_let(self):
        """ Compiles a let statement. """
        var_name = self.__compile_identifier_name()
        self.__advance_tokenizer()
        token_type = self.__tokenizer.token_type()
        is_array = False
        if token_type == JackTokenizer.SYMBOL and self.__tokenizer.symbol() == "[":
            self.compile_expression()
            self.__compile_symbol("]")
            self.__vm_writer.write_push(self.__convert_to_vm_write(self.__symbol_table.kind_of(var_name)),
                                        self.__symbol_table.index_of(var_name))
            self.__vm_writer.write_arithmetic(VMWriter.ADD)
            is_array = True
        else:
            self.__tokenizer.back()
        self.__compile_symbol("=")
        self.compile_expression()
        self.__compile_symbol(";")
        if is_array:
            self.__vm_writer.write_pop(VMWriter.TEMP, 0)
            self.__vm_writer.write_pop(VMWriter.POINTER, 1)
            self.__vm_writer.write_push(VMWriter.TEMP, 0)
            self.__vm_writer.write_pop(VMWriter.THAT, 0)
        else:
            self.__vm_writer.write_pop(self.__convert_to_vm_write(self.__symbol_table.kind_of(var_name)),
                                       self.__symbol_table.index_of(var_name))

    # whileStatement: 'while' '(' expression ')' '{' statements '}'
    def compile_while(self):
        """ Compiles a while statement. """
        self.__count_while_cycle += 1
        while_count = self.__count_while_cycle
        self.__vm_writer.write_label("WHILE_EXP" + str(while_count))
        self.__compile_symbol("(")
        self.compile_expression()
        self.__compile_symbol(")")
        self.__vm_writer.write_arithmetic(VMWriter.NOT)
        self.__vm_writer.write_if("WHILE_END" + str(while_count))
        self.__compile_symbol("{")
        self.compile_statements()
        self.__compile_symbol("}")
        self.__vm_writer.write_goto("WHILE_EXP" + str(while_count))
        self.__vm_writer.write_label("WHILE_END" + str(while_count))

    # ReturnStatement 'return' expression? ';'
    def compile_return(self):
        """ Compiles a return statement. """
        self.__advance_tokenizer()
        if self.__tokenizer.token_type() != JackTokenizer.SYMBOL:
            self.__tokenizer.back()
            self.compile_expression()
        else:
            self.__tokenizer.back()
            self.__vm_writer.write_push(VMWriter.CONST, 0)
        self.__compile_symbol(";")
        self.__vm_writer.write_return()

    # ifStatement: 'if' '(' expression ')' '{' statements '}'
    #              ('else' '{' statements '}')?
    def compile_if(self):
        """ Compiles an if statement, possibly with a trailing else clause. """
        self.__compile_symbol("(")
        self.compile_expression()
        self.__compile_symbol(")")
        self.__count_if += 1
        count_if = self.__count_if
        self.__vm_writer.write_if("IF_TRUE" + str(count_if))
        self.__vm_writer.write_goto("IF_FALSE" + str(count_if))
        self.__vm_writer.write_label("IF_TRUE" + str(count_if))
        self.__compile_symbol("{")
        self.compile_statements()
        self.__compile_symbol("}")
        # code for 'else'
        self.__advance_tokenizer()
        if self.__tokenizer.token_type() != JackTokenizer.KEYWORD or self.__tokenizer.key_word() != "else":
            self.__tokenizer.back()
            self.__vm_writer.write_label("IF_FALSE" + str(count_if))
            return
        self.__vm_writer.write_goto("IF_END" + str(count_if))
        self.__vm_writer.write_label("IF_FALSE" + str(count_if))
        self.__compile_symbol("{")
        self.compile_statements()
        self.__compile_symbol("}")
        self.__vm_writer.write_label("IF_END" + str(count_if))

    # expression: term (op term)*
    def compile_expression(self):
        """ Compiles an expression. """
        self.compile_term()
        self.__compile_op_term()

    # compile (op term)*
    def __compile_op_term(self):
        self.__advance_tokenizer()
        token_type = self.__tokenizer.token_type()
        if token_type != JackTokenizer.SYMBOL or self.__tokenizer.symbol() not in self.__op.keys():
            self.__tokenizer.back()
            return
        arithmetic_symbol = self.__tokenizer.symbol()
        self.compile_term()
        if arithmetic_symbol == "*":
            self.__vm_writer.write_call("Math.multiply", 2)
        elif arithmetic_symbol == "/":
            self.__vm_writer.write_call("Math.divide", 2)
        else:
            self.__vm_writer.write_arithmetic(self.__op[arithmetic_symbol])
        self.__compile_op_term()

    # push string
    def __push_string(self, string):
        self.__vm_writer.write_push(VMWriter.CONST, len(string))
        self.__vm_writer.write_call("String.new", 1)
        for c in string:
            self.__vm_writer.write_push(VMWriter.CONST, ord(c))
            self.__vm_writer.write_call("String.appendChar", 2)

    # push keyword constant
    def __push_keyword_constant(self, keyword):
        if keyword == "this":
            self.__vm_writer.write_push(VMWriter.POINTER, 0)
        elif keyword == "null" or keyword == "false":
            self.__vm_writer.write_push(VMWriter.CONST, 0)
        else:   # keyword is true
            self.__vm_writer.write_push(VMWriter.CONST, 0)
            self.__vm_writer.write_arithmetic(VMWriter.NOT)

    # term: integerConstant | stringConstant | keywordConstant | varName |
    #       varName '[' expression ']' | subroutineCall | '(' expression ')' | unaryOp term
    def compile_term(self):
        """
        Compiles a term. This routine is faced with a slight difficulty
        when trying to decide between some of the alternative parsing
        rules. Specifically, if the current token is an identifier, the routine
        must distinguish between a variable, an array entry, and a
        subroutine call. A single look-ahead token, which may be one
        of ‘‘[’’, ‘‘(’’, or ‘‘.’’ suffices to distinguish between the three possibilities.
        Any other token is no part of this term and should not be advanced over.
        """
        self.__advance_tokenizer()
        token_type = self.__tokenizer.token_type()
        if token_type == JackTokenizer.INT_CONST:
            self.__vm_writer.write_push(VMWriter.CONST, self.__tokenizer.int_val())
        elif token_type == JackTokenizer.STRING_CONST:
            self.__push_string(self.__tokenizer.string_val())
        elif token_type == JackTokenizer.KEYWORD and self.__tokenizer.key_word() in self.__key_word_constant:
            self.__push_keyword_constant(self.__tokenizer.key_word())
        elif token_type == JackTokenizer.IDENTIFIER:
            identifier_name = self.__tokenizer.identifier()
            self.__advance_tokenizer()
            if self.__tokenizer.token_type() == JackTokenizer.SYMBOL:
                if self.__tokenizer.symbol() == "." or self.__tokenizer.symbol() == "(":    # is subroutineCall
                    self.__tokenizer.back()
                    self.__tokenizer.back()
                    self.__compile_subroutine_call()
                elif self.__tokenizer.symbol() == "[":      # is varName[expression]
                    self.compile_expression()
                    self.__compile_symbol("]")
                    self.__vm_writer.write_push(
                            self.__convert_to_vm_write(self.__symbol_table.kind_of(identifier_name)),
                            self.__symbol_table.index_of(identifier_name))
                    self.__vm_writer.write_arithmetic(VMWriter.ADD)
                    self.__vm_writer.write_pop(VMWriter.POINTER, 1)
                    self.__vm_writer.write_push(VMWriter.THAT, 0)
                else:   # is varName
                    self.__tokenizer.back()
                    self.__vm_writer.write_push(
                            self.__convert_to_vm_write(self.__symbol_table.kind_of(identifier_name)),
                            self.__symbol_table.index_of(identifier_name))
            else:
                self.__tokenizer.back()
        elif token_type == JackTokenizer.SYMBOL:
            if self.__tokenizer.symbol() == "(":    # is (expression)
                self.compile_expression()
                self.__compile_symbol(")")
            elif self.__tokenizer.symbol() in self.__unary_op.keys():  # is unaryOp term
                unary_symbol = self.__tokenizer.symbol()
                self.compile_term()
                self.__vm_writer.write_arithmetic(self.__unary_op[unary_symbol])
        else:
            raise Exception("not valid command in term")

    # expressionList: expression (',' expression)*
    def compile_expression_list(self):
        """ Compiles a (possibly empty) comma-separated list of expressions. """
        self.__advance_tokenizer()
        if self.__tokenizer.token_type() == JackTokenizer.SYMBOL and self.__tokenizer.symbol() == ")":
            self.__tokenizer.back()
            return 0
        self.__tokenizer.back()
        self.compile_expression()
        return 1 + self.__compile_more_expression_list()

    # (',' expression)*
    def __compile_more_expression_list(self):
        self.__advance_tokenizer()
        if self.__tokenizer.token_type() != JackTokenizer.SYMBOL or self.__tokenizer.symbol() != ",":
            self.__tokenizer.back()
            return 0
        self.compile_expression()
        return 1 + self.__compile_more_expression_list()
