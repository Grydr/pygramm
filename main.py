import pprint
import lexer

pp = pprint.PrettyPrinter()

def main():

    lex = lexer.Lexer()
    lex.read_from_file("test-files/test_file.js")
    lex.scan_tokens()

    for tok in lex.tokens:
        print(tok)

if __name__ == "__main__":
    main()
