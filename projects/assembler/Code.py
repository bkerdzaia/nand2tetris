#!/usr/bin/evn python3

class Code:
    """
    Translates Hack assembly language mnemonics into binary codes.
    """

    def dest(self, mnemonic):
        """ Returns the binary code of the dest mnemonic. """
        translated = ['0', '0', '0']
        if mnemonic is None:
            return "".join(translated)
        for i in range(0, len(mnemonic)):
            if mnemonic[i] == 'M':
                translated[2] = '1'
            elif mnemonic[i] == 'A':
                translated[0] = '1'
            elif mnemonic[i] == 'D':
                translated[1] = '1'
            else:
                return None
        return "".join(translated)

    def comp(self, mnemonic):
        """  Returns the binary code of the comp mnemonic. """
        mnemonic = mnemonic.replace(" ", "")
        if mnemonic == "0":
            return "0101010"
        if mnemonic == "1":
            return "0111111"
        if mnemonic == "-1":
            return "0111010"
        if mnemonic == "D":
            return "0001100"
        if mnemonic == "A":
            return "0110000"
        if mnemonic == "M":
            return "1110000"
        if mnemonic == "!D":
            return "0001101"
        if mnemonic == "!A":
            return "0110001"
        if mnemonic == "!M":
            return "1110001"
        if mnemonic == "-D":
            return "0001111"
        if mnemonic == "-A":
            return "0110011"
        if mnemonic == "-M":
            return "1110011"
        if mnemonic == "D+1" or mnemonic == "1+D":
            return "0011111"
        if mnemonic == "A+1" or mnemonic == "1+A":
            return "0110111"
        if mnemonic == "M+1" or mnemonic == "1+M":
            return "1110111"
        if mnemonic == "D-1":
            return "0001110"
        if mnemonic == "A-1":
            return "0110010"
        if mnemonic == "M-1":
            return "1110010"
        if mnemonic == "D+A" or mnemonic == "A+D":
            return "0000010"
        if mnemonic == "D+M" or mnemonic == "M+D":
            return "1000010"
        if mnemonic == "D-A":
            return "0010011"
        if mnemonic == "D-M":
            return "1010011"
        if mnemonic == "A-D":
            return "0010011"
        if mnemonic == "M-D":
            return "1000111"
        if mnemonic == "D&A" or mnemonic == "A&D":
            return "0000000"
        if mnemonic == "D&M" or mnemonic == "M&D":
            return "1000000"
        if mnemonic == "D|A" or mnemonic == "A|D":
            return "0010101"
        if mnemonic == "D|M" or mnemonic == "M|D":
            return "1010101"
        return None

    def jump(self, mnemonic):
        """ Returns the binary code of the jump mnemonic. """
        if mnemonic is None:
            return "000"
        elif mnemonic == "JGT":
            return "001"
        elif mnemonic == "JEQ":
            return "010"
        elif mnemonic == "JGE":
            return "011"
        elif mnemonic == "JLT":
            return "100"
        elif mnemonic == "JNE":
            return "101"
        elif mnemonic == "JLE":
            return "110"
        elif mnemonic == "JMP":
            return "111"
        return None
