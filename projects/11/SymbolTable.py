#!/usr/bin/evn python3


class SymbolTable:

    """
    This module provides services for creating and using a symbol table. Recall that each
    symbol has a scope from which it is visible in the source code. The symbol table
    implements this abstraction by giving each symbol a running number (index) within
    the scope. The index starts at 0, increments by 1 each time an identifier is added to
    the table, and resets to 0 when starting a new scope. The following kinds of identifiers
    may appear in the symbol table:
        Static:      Scope: class.
        Field:       Scope: class.
        Argument:    Scope: subroutine (method/function/constructor).
        Var:         Scope: subroutine (method/function/constructor).
    """

    STATIC = "static"
    FIELD = "field"
    ARG = "argument"
    VAR = "local"

    def __init__(self):
        """ Creates a new empty symbol table. """
        self.__class_scope = {}
        self.__subroutine_scope = {}

    def start_subroutine(self):
        """ Starts a new subroutine scope (i.e., resets the subroutine’s symbol table)."""
        self.__subroutine_scope.clear()

    def define(self, name, type, kind):
        """
        Defines a new identifier of a given name, type, and kind and assigns it a running index.
        STATIC and FIELD identifiers have a class scope, while ARG and VAR identifiers have a subroutine scope.
        """
        dict_kind = self.__get_dictionary_type(kind)
        if name in dict_kind:
            raise Exception(name, "this name was inserted already")
        dict_kind[name] = (type, kind, self.var_count(kind))

    def __get_dictionary_type(self, kind):
        if kind == self.STATIC or kind == self.FIELD:
            return self.__class_scope
        elif kind == self.ARG or kind == self.VAR:
            return self.__subroutine_scope
        else:
            raise Exception("not valid kind argument in var_count")

    def var_count(self, kind):
        """ Returns the number of variables of the given kind already defined in the current scope. """
        # print("filter:", list(filter(lambda v: v[1] == kind, self.__get_dictionary_type(kind).values())))
        return len(list(filter(lambda value: value[1] == kind, self.__get_dictionary_type(kind).values())))

    def kind_of(self, name):
        """
        Returns the kind of the named identifier in the current scope.
        If the identifier is unknown in the current scope, returns NONE.
        """
        return self.__subroutine_scope.get(name, self.__class_scope.get(name, (None, None, None)))[1]

    def type_of(self, name):
        """ Returns the type of the named identifier in the current scope. """
        return self.__subroutine_scope.get(name, self.__class_scope.get(name, (None, None, None)))[0]

    def index_of(self, name):
        """ Returns the index assigned to the named identifier. """
        return self.__subroutine_scope.get(name, self.__class_scope.get(name, (None, None, None)))[2]
