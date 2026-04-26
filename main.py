import argparse
import pprint
import lexer
import parser
import JSToken as JST

pp = pprint.PrettyPrinter(indent=2, width=120, sort_dicts=False)

def parse_args():
    parser = argparse.ArgumentParser(description="Lex a JavaScript file.")
    parser.add_argument(
        "file",
        nargs="?",
        default="test-files/full_lexer_test.js",
        help="Path to the JavaScript file to lex",
    )
    parser.add_argument(
        "--parse",
        action="store_true",
        help="Parse tokens with CFG parser and print AST",
    )
    return parser.parse_args()


def classify_tokens(tokens):
    grouped = {
        "Reserve words": [],
        "Symbol": [],
        "Variabel": [],
        "Math equation": [],
        "Other": [],
    }

    reserve_word_tokens = set(JST.KEYWORDS.values())

    for tok in tokens:
        if tok.tokenType == JST.JSToken.ENDMARKER:
            continue
        if tok.tokenType in reserve_word_tokens:
            grouped["Reserve words"].append(tok)
        elif tok.tokenType in JST.SYMBOL_TOKENS:
            grouped["Symbol"].append(tok)
        elif tok.tokenType in JST.VARIABLE_TOKENS:
            grouped["Variabel"].append(tok)
        elif tok.tokenType in JST.MATH_EQUATION_TOKENS:
            grouped["Math equation"].append(tok)
        else:
            grouped["Other"].append(tok)

    return grouped


def print_group(name, tokens):
    print(f"\n{name}:")
    if not tokens:
        print("  (none)")
        return

    pretty_tokens = [
        {"type": tok.tokenType.name, "value": tok.value, "line": tok.line_num}
        for tok in tokens
    ]
    pp.pprint(pretty_tokens)


def main():
    args = parse_args()

    lex = lexer.Lexer()
    lex.read_from_file(args.file)
    lex.scan_tokens()

    grouped = classify_tokens(lex.tokens)
    print_group("Reserve words", grouped["Reserve words"])
    print_group("Symbol", grouped["Symbol"])
    print_group("Variabel", grouped["Variabel"])
    print_group("Math equation", grouped["Math equation"])
    print_group("Other", grouped["Other"])

    if args.parse:
        print("\nAST:")
        try:
            ast = parser.Parser(lex.tokens).parse()
            pp.pprint(ast)
        except parser.ParserError as err:
            print(f"Parse error: {err}")


if __name__ == "__main__":
    main()