import JSToken as JST


class Lexer:
    hadError = False

    def __init__(self):
        self.source_code = ""
        self.tokens = []

        self.start = 0
        self.current = 0
        self.line = 1

    def read_from_file(self, file_path):
        with open(file_path, "r") as file:
            curr_line = file.readline()
            while curr_line:
                curr_line = curr_line.strip()
                self.source_code += curr_line + "\n"
                curr_line = file.readline()

    def error(self, line, err):
        err = f"Line: {line}; Error: {err}"
        print(err)
        Lexer.hadError = True
        raise Exception(err)

    def is_at_source_ends(self):
        if self.current >= len(self.source_code):
            return True
        else:
            return False

    def ret_and_advance(self):
        char = self.source_code[self.current]
        if not self.is_at_source_ends():
            self.current += 1
        return char

    def add_token(self, token_type):
        tok_str = self.source_code[self.start : self.current]
        tok = JST.Token(token_type, tok_str, self.line)
        self.tokens.append(tok)

    def add_token_val(self, token_type, val):
        tok = JST.Token(token_type, val, self.line)
        self.tokens.append(tok)

    def match(self, char):
        if self.is_at_source_ends():
            return False

        if self.source_code[self.current] == char:
            self.current += 1
            return True
        else:
            return False

    def peek(self):
        if self.is_at_source_ends():
            return "\0"
        return self.source_code[self.current]

    def handle_string(self):
        while self.peek() != '"' and not self.is_at_source_ends():
            if self.peek() == "\n":
                self.line += 1
            self.ret_and_advance()

        if self.is_at_source_ends():
            self.error(self.line, "Unterminated string.")
            return

        self.ret_and_advance()

        str_val = self.source_code[self.start + 1 : self.current - 1]
        self.add_token_val(JST.JSToken.STRING, str_val)

    def handle_num(self):
        have_decimal = False
        num_str = f"{self.source_code[self.start : self.current]}"
        next_c = self.peek()

        while next_c.isdigit() or next_c == ".":
            if next_c == "." and not have_decimal:
                have_decimal = True

            num_str += f"{self.source_code[self.current]}"
            self.ret_and_advance()
            next_c = self.peek()

        if num_str[0] == "." or num_str[-1] == ".":
            self.error(self.line, "No Leading or Trailing decimal allowed")
            return

        self.add_token_val(JST.JSToken.NUMBER, float(num_str))

    def handle_identifier(self):
        while self.peek().isalnum() or self.peek() == "_":
            self.ret_and_advance()

        word = self.source_code[self.start : self.current]
        token_type = (
            JST.KEYWORDS[word] if word in JST.KEYWORDS else JST.JSToken.IDENTIFIER
        )

        self.add_token(token_type)

    def scan_token(self):
        c = self.ret_and_advance()
        match c:
            case "{":
                self.add_token(JST.JSToken.LBRACE)
            case "}":
                self.add_token(JST.JSToken.RBRACE)
            case "(":
                self.add_token(JST.JSToken.LPAR)
            case ")":
                self.add_token(JST.JSToken.RPAR)
            case ";":
                self.add_token(JST.JSToken.SEMI)
            case "+":
                self.add_token(
                    JST.JSToken.PLUSEQUAL if self.match("=") else JST.JSToken.PLUS
                )
            case "-":
                self.add_token(
                    JST.JSToken.MINUSEQUAL if self.match("=") else JST.JSToken.MINUS
                )
            case "*":
                self.add_token(
                    JST.JSToken.STAREQUAL if self.match("=") else JST.JSToken.STAR
                )
            case ".":
                if self.peek().isdigit():
                    self.handle_num()
                else:
                    self.add_token(JST.JSToken.DOT)
            case ",":
                self.add_token(JST.JSToken.COMMA)
            case "!":
                self.add_token(
                    JST.JSToken.NOTEQUAL if self.match("=") else JST.JSToken.EXCLAMATION
                )
            case "=":
                self.add_token(
                    JST.JSToken.EQEQUAL if self.match("=") else JST.JSToken.EQUAL
                )
            case "<":
                self.add_token(
                    JST.JSToken.LESSEQUAL if self.match("=") else JST.JSToken.LESS
                )
            case ">":
                self.add_token(
                    JST.JSToken.GREATEREQUAL if self.match("=") else JST.JSToken.GREATER
                )
            case "/":
                if self.match("/"):
                    while self.peek() != "\n" and not self.is_at_source_ends():
                        self.ret_and_advance()
                elif self.match("="):
                    self.add_token(JST.JSToken.SLASHEQUAL)
                else:
                    self.add_token(JST.JSToken.SLASH)
            case "&":
                self.add_token(
                    JST.JSToken.AND if self.match("&") else JST.JSToken.AMPER
                )
            case "|":
                self.add_token(
                    JST.JSToken.OR if self.match("|") else JST.JSToken.VBAR
                )
            case " ":
                pass
            case "\r":
                pass
            case "\t":
                pass
            case "\n":
                self.line += 1
            case '"':
                self.handle_string()

            case _:
                if c.isdigit():
                    self.handle_num()
                elif c.isalpha() or c == "_":
                    self.handle_identifier()
                else:
                    self.error(self.line, "Unexpected character")

    def scan_tokens(self):
        while not self.is_at_source_ends():
            self.start = self.current
            self.scan_token()

        self.tokens.append(JST.Token(JST.JSToken.ENDMARKER, "\0", self.line))
        return self.tokens
