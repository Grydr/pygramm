from enum import Enum, auto
import token

class JSToken(Enum):
    LBRACE = auto()
    RBRACE = auto()
    LPAR = auto()
    RPAR = auto()
    SEMI = auto()
    PLUS = auto()
    PLUSEQUAL = auto()
    MINUS = auto()
    MINUSEQUAL = auto()
    STAR = auto()
    STAREQUAL = auto()
    DOT = auto()
    COMMA = auto()
    NOTEQUAL = auto()
    EXCLAMATION = auto()
    EQEQUAL = auto()
    EQUAL = auto()
    LESSEQUAL = auto()
    LESS = auto()
    GREATEREQUAL = auto()
    GREATER = auto()
    SLASHEQUAL = auto()
    SLASH = auto()
    STRING = auto()
    NUMBER = auto()
    IDENTIFIER = auto()
    ENDMARKER = auto()
    AMPER = auto()
    AND = auto()
    VBAR = auto()
    OR = auto()

    # Keywords
    AWAIT = auto()
    BREAK = auto()
    CASE = auto()
    CATCH = auto()
    CLASS = auto()

    CONST = auto()
    CONTINUE = auto()
    DEBUGGER = auto()
    DEFAULT = auto()
    DELETE = auto()

    DO = auto()
    ELSE = auto()
    ENUM = auto()
    EXPORT = auto()
    EXTENDS = auto()

    FALSE = auto()
    FINALLY = auto()
    FOR = auto()
    FUNCTION = auto()
    IF = auto()

    IMPLEMENTS = auto()
    IMPORT = auto()
    IN = auto()
    INSTANCEOF = auto()
    INTERFACE = auto()

    LET = auto()
    NEW = auto()
    NULL = auto()
    PACKAGE = auto()
    PRIVATE = auto()

    PROTECTED = auto()
    PUBLIC = auto()
    RETURN = auto()
    SUPER = auto()
    SWITCH = auto()

    STATIC = auto()
    THIS = auto()
    THROW = auto()
    TRY = auto()
    TRUE = auto()

    TYPEOF = auto()
    VAR = auto()
    VOID = auto()
    WHILE = auto()
    WITH = auto()

    YIELD = auto()


Keywords = {
    "await": JSToken.AWAIT,
    "break": JSToken.BREAK,
    "case": JSToken.CASE,
    "catch": JSToken.CATCH,
    "class": JSToken.CLASS,
    "const": JSToken.CONST,
    "continue": JSToken.CONTINUE,
    "debugger": JSToken.DEBUGGER,
    "default": JSToken.DEFAULT,
    "delete": JSToken.DELETE,
    "do": JSToken.DO,
    "else": JSToken.ELSE,
    "enum": JSToken.ENUM,
    "export": JSToken.EXPORT,
    "extends": JSToken.EXTENDS,
    "false": JSToken.FALSE,
    "finally": JSToken.FINALLY,
    "for": JSToken.FOR,
    "function": JSToken.FUNCTION,
    "if": JSToken.IF,
    "implements": JSToken.IMPLEMENTS,
    "import": JSToken.IMPORT,
    "in": JSToken.IN,
    "instanceof": JSToken.INSTANCEOF,
    "interface": JSToken.INTERFACE,
    "let": JSToken.LET,
    "new": JSToken.NEW,
    "null": JSToken.NULL,
    "package": JSToken.PACKAGE,
    "private": JSToken.PRIVATE,
    "protected": JSToken.PROTECTED,
    "public": JSToken.PUBLIC,
    "return": JSToken.RETURN,
    "super": JSToken.SUPER,
    "switch": JSToken.SWITCH,
    "static": JSToken.STATIC,
    "this": JSToken.THIS,
    "throw": JSToken.THROW,
    "try": JSToken.TRY,
    "true": JSToken.TRUE,
    "typeof": JSToken.TYPEOF,
    "var": JSToken.VAR,
    "void": JSToken.VOID,
    "while": JSToken.WHILE,
    "with": JSToken.WITH,
    "yield": JSToken.YIELD,
}


class Token:
    def __init__(self, tokenType, value, line_num):
        self.tokenType = tokenType
        self.value = value
        self.line_num = line_num

    def __str__(self):
        return f"[TokenType: {self.tokenType.name}, Value: {self.value}, Line: {self.line_num}]"
