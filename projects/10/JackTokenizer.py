import re

class JackTokenizer:
    """
    Removes all comments and white space from the input stream and
    breaks it into Jack-language tokens, as specified by the Jack grammar.
    """
    KEYWORD = 1
    SYMBOL = 2
    IDENTIFIER = 3
    INT_CONST = 4
    STRING_CONST = 5

    def __init__(self, stream):
        """ Opens the input file/stream and gets ready to tokenize it."""
        self.__token_index = 0
        self.__current_token = None
        self.__key_words = ['class', 'constructor', 'function', 'method', 'field', 'static', 'var',
                            'int', 'char', 'boolean', 'void', 'true', 'false', 'null', 'this', 'let',
                            'do', 'if', 'else', 'while', 'return']
        self.__symbols = ['{', '}', '(', ')', '[', ']', '.', ',', ';', '+', '-', '*', '/', '&', '|', '<', '>', '=', '~']
        text = self.__change_symbol(re.sub(r'//.*', "", re.sub(r'/\*.*?\*/', "", stream.read(), flags=re.DOTALL)))
        self.__tokens = self.__generate_tokens(text)
        self.__key_word_name = None
        self.__symbol = None
        self.__identifier = None
        self.__int_value = None
        self.__string_constant = None
        self.__to_xml_symbols = {"<": "&lt;", ">": "&gt;", "\"": "&quot;", "&": "&amp;"}

    # generate tokens from text input string
    @staticmethod
    def __generate_tokens(text):
        tokens = []
        prev_token = 0
        for quote in re.findall("\".*\"", text):
            tokens.extend(text[prev_token:text.find(quote)].split())
            prev_token = text.find(quote) + len(quote)
            tokens.append(quote)
        tokens.extend(text[prev_token:].split())
        return tokens

    # add symbols spaces around them
    def __change_symbol(self, text):
        for symbol in self.__symbols:
            text = text.replace(symbol, " " + symbol + " ")
        return text

    def has_more_tokens(self):
        """ Do we have more tokens in the input? """
        return self.__token_index < len(self.__tokens)

    def advance(self):
        """
        Gets the next token from the input and makes it the current token. This
        method should only be called if hasMoreTokens() is true. Initially
        there is no current token.
        """
        self.__current_token = self.__tokens[self.__token_index]
        self.__token_index += 1

    def token_type(self):
        """ :return: Returns the type of the current token. """
        if self.__key_words.__contains__(self.__current_token):
            self.__key_word_name = self.__current_token
            self.__symbol, self.__identifier, self.__int_value, self.__string_constant, = None, None, None, None
            return self.KEYWORD
        if self.__symbols.__contains__(self.__current_token):
            self.__symbol = self.__to_xml_symbols.get(str(self.__current_token), self.__current_token)
            self.__key_word_name, self.__identifier, self.__int_value, self.__string_constant, = None, None, None, None
            return self.SYMBOL
        if self.__current_token.find("\"") != -1:
            self.__string_constant = self.__current_token.replace("\"", "")
            self.__key_word_name, self.__identifier, self.__int_value, self.__symbol, = None, None, None, None
            return self.STRING_CONST
        if self.__current_token.isdigit():
            self.__int_value = self.__current_token
            self.__key_word_name, self.__identifier, self.__string_constant, self.__symbol, = None, None, None, None
            return self.INT_CONST
        self.__identifier = self.__current_token
        self.__key_word_name, self.__string_constant, self.__int_value, self.__symbol, = None, None, None, None
        return self.IDENTIFIER

    def key_word(self):
        """
        :return: Returns the keyword which is the current token. Should be called only
        when tokenType() is KEYWORD.
        """
        return self.__key_word_name

    def symbol(self):
        """
        :return: Returns the character which is the current token. Should be called only
        when tokenType() is SYMBOL.
        """
        return self.__symbol

    def identifier(self):
        """
        :return: Returns the identifier which is the current token. Should be called only
        when tokenType() is IDENTIFIER.
        """
        return self.__identifier

    def int_val(self):
        """
        :return: Returns the integer value of the current token. Should be called only
        when tokenType() is INT_CONST.
        """
        return self.__int_value

    def string_val(self):
        """
        :return: Returns the string value of the current token, without the double quotes.
        Should be called only when tokenType() is STRING_CONST.
        """
        return self.__string_constant
