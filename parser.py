import JSToken as JST

class Parser:
    """
        CFG:
            program          -> declaration* EOF
            declaration      -> function_decl | variable_decl | if_stmt | while_stmt | for_stmt | switch_stmt | block | statement
            function_decl    -> FUNCTION IDENTIFIER "(" parameters? ")" block
            parameters       -> IDENTIFIER ("," IDENTIFIER)*
            variable_decl    -> (LET | CONST | VAR) IDENTIFIER (assign_op expression)? ";"
            if_stmt          -> IF "(" expression ")" declaration (ELSE declaration)?
            while_stmt       -> WHILE "(" expression ")" declaration
            for_stmt         -> FOR "(" for_init? ";" expression? ";" expression? ")" declaration
            for_init         -> variable_decl_no_semi | expression
            switch_stmt      -> SWITCH "(" expression ")" "{" switch_case* "}"
            switch_case      -> CASE expression ":" declaration* | DEFAULT ":" declaration*
            block            -> "{" declaration* "}"
            statement        -> return_stmt | break_stmt | expression_stmt
            return_stmt      -> RETURN expression? ";"
            break_stmt       -> BREAK ";"
            expression_stmt  -> expression ";"

            expression       -> assignment
            assignment       -> logic_or (assign_op assignment)?
            logic_or         -> logic_and ((OR | VBAR) logic_and)*
            logic_and        -> equality ((AND | AMPER) equality)*
            equality         -> comparison ((EQEQUAL | NOTEQUAL) comparison)*
            comparison       -> term ((GREATER | GREATEREQUAL | LESS | LESSEQUAL) term)*
            term             -> factor ((PLUS | MINUS) factor)*
            factor           -> unary ((STAR | SLASH) unary)*
            unary            -> (EXCLAMATION | PLUS | MINUS | TYPEOF | DELETE | VOID) unary | call
            call             -> primary (("(" arguments? ")") | ("." IDENTIFIER))*
            arguments        -> expression ("," expression)*
            primary          -> NUMBER | STRING | TRUE | FALSE | NULL | IDENTIFIER | "(" expression ")"
            assign_op        -> EQUAL | PLUSEQUAL | MINUSEQUAL | STAREQUAL | SLASHEQUAL
    """

    ASSIGNMENT_OPS = {
        JST.JSToken.EQUAL,
        JST.JSToken.PLUSEQUAL,
        JST.JSToken.MINUSEQUAL,
        JST.JSToken.STAREQUAL,
        JST.JSToken.SLASHEQUAL,
    }

    def __init__(self, tokens):
        self.tokens = tokens
        self.current = 0

    def parse(self):
        statements = []
        while not self._is_at_end():
            statements.append(self._declaration())
        return {"type": "Program", "body": statements}

    def _declaration(self):
        if self._match(JST.JSToken.FUNCTION):
            return self._function_declaration()
        if self._match(JST.JSToken.LET, JST.JSToken.CONST, JST.JSToken.VAR):
            keyword = self._previous()
            return self._variable_declaration(keyword)
        if self._match(JST.JSToken.IF):
            return self._if_statement()
        if self._match(JST.JSToken.WHILE):
            return self._while_statement()
        if self._match(JST.JSToken.FOR):
            return self._for_statement()
        if self._match(JST.JSToken.SWITCH):
            return self._switch_statement()
        if self._match(JST.JSToken.LBRACE):
            return self._block_statement()
        return self._statement()

    def _function_declaration(self):
        keyword = self._previous()
        name = self._consume(JST.JSToken.IDENTIFIER, "Expected function name.")
        self._consume(JST.JSToken.LPAR, "Expected '(' after function name.")

        parameters = []
        if not self._check(JST.JSToken.RPAR):
            parameters.append(
                self._consume(JST.JSToken.IDENTIFIER, "Expected parameter name.").value
            )
            while self._match(JST.JSToken.COMMA):
                parameters.append(
                    self._consume(
                        JST.JSToken.IDENTIFIER, "Expected parameter name after ','."
                    ).value
                )

        self._consume(JST.JSToken.RPAR, "Expected ')' after parameters.")
        self._consume(JST.JSToken.LBRACE, "Expected '{' before function body.")
        body = self._block_statement()
        return {
            "type": "FunctionDeclaration",
            "name": name.value,
            "params": parameters,
            "body": body,
            "line": keyword.line_num,
        }

    def _variable_declaration(self, keyword_token, require_semicolon=True):
        name = self._consume(JST.JSToken.IDENTIFIER, "Expected variable name.")

        initializer = None
        assign_op = None
        if self._check_any(self.ASSIGNMENT_OPS):
            assign_op = self._advance().tokenType.name
            initializer = self._expression()

        if require_semicolon:
            self._consume(JST.JSToken.SEMI, "Expected ';' after variable declaration.")
        return {
            "type": "VariableDeclaration",
            "kind": keyword_token.tokenType.name.lower(),
            "name": name.value,
            "operator": assign_op,
            "initializer": initializer,
            "line": keyword_token.line_num,
        }

    def _if_statement(self):
        keyword = self._previous()
        self._consume(JST.JSToken.LPAR, "Expected '(' after 'if'.")
        condition = self._expression()
        self._consume(JST.JSToken.RPAR, "Expected ')' after if condition.")

        then_branch = self._declaration()
        else_branch = None
        if self._match(JST.JSToken.ELSE):
            else_branch = self._declaration()

        return {
            "type": "IfStatement",
            "condition": condition,
            "then": then_branch,
            "else": else_branch,
            "line": keyword.line_num,
        }

    def _while_statement(self):
        keyword = self._previous()
        self._consume(JST.JSToken.LPAR, "Expected '(' after 'while'.")
        condition = self._expression()
        self._consume(JST.JSToken.RPAR, "Expected ')' after while condition.")
        body = self._declaration()
        return {
            "type": "WhileStatement",
            "condition": condition,
            "body": body,
            "line": keyword.line_num,
        }

    def _for_statement(self):
        keyword = self._previous()
        self._consume(JST.JSToken.LPAR, "Expected '(' after 'for'.")

        initializer = None
        if self._match(JST.JSToken.SEMI):
            initializer = None
        elif self._match(JST.JSToken.LET, JST.JSToken.CONST, JST.JSToken.VAR):
            init_keyword = self._previous()
            initializer = self._variable_declaration(init_keyword, require_semicolon=False)
            self._consume(JST.JSToken.SEMI, "Expected ';' after for-loop initializer.")
        else:
            initializer = self._expression()
            self._consume(JST.JSToken.SEMI, "Expected ';' after for-loop initializer.")

        condition = None
        if not self._check(JST.JSToken.SEMI):
            condition = self._expression()
        self._consume(JST.JSToken.SEMI, "Expected ';' after for-loop condition.")

        increment = None
        if not self._check(JST.JSToken.RPAR):
            increment = self._expression()
        self._consume(JST.JSToken.RPAR, "Expected ')' after for clauses.")

        body = self._declaration()
        return {
            "type": "ForStatement",
            "initializer": initializer,
            "condition": condition,
            "increment": increment,
            "body": body,
            "line": keyword.line_num,
        }

    def _switch_statement(self):
        keyword = self._previous()
        self._consume(JST.JSToken.LPAR, "Expected '(' after 'switch'.")
        discriminant = self._expression()
        self._consume(JST.JSToken.RPAR, "Expected ')' after switch expression.")
        self._consume(JST.JSToken.LBRACE, "Expected '{' before switch cases.")

        cases = []
        while not self._check(JST.JSToken.RBRACE) and not self._is_at_end():
            if self._match(JST.JSToken.CASE):
                case_expr = self._expression()
                self._consume(JST.JSToken.COLON, "Expected ':' after case expression.")
                body = self._case_body()
                cases.append({"type": "SwitchCase", "test": case_expr, "consequent": body})
            elif self._match(JST.JSToken.DEFAULT):
                self._consume(JST.JSToken.COLON, "Expected ':' after default.")
                body = self._case_body()
                cases.append({"type": "SwitchCase", "test": None, "consequent": body})
            else:
                raise self._error(self._peek(), "Expected 'case' or 'default' in switch.")

        self._consume(JST.JSToken.RBRACE, "Expected '}' after switch body.")
        return {
            "type": "SwitchStatement",
            "discriminant": discriminant,
            "cases": cases,
            "line": keyword.line_num,
        }

    def _case_body(self):
        body = []
        while (
            not self._check(JST.JSToken.CASE)
            and not self._check(JST.JSToken.DEFAULT)
            and not self._check(JST.JSToken.RBRACE)
            and not self._is_at_end()
        ):
            body.append(self._declaration())
        return body

    def _block_statement(self):
        statements = []
        while not self._check(JST.JSToken.RBRACE) and not self._is_at_end():
            statements.append(self._declaration())
        self._consume(JST.JSToken.RBRACE, "Expected '}' after block.")
        return {"type": "BlockStatement", "body": statements}

    def _statement(self):
        if self._match(JST.JSToken.RETURN):
            return self._return_statement()
        if self._match(JST.JSToken.BREAK):
            return self._break_statement()
        return self._expression_statement()

    def _return_statement(self):
        keyword = self._previous()
        value = None
        if not self._check(JST.JSToken.SEMI):
            value = self._expression()
        self._consume(JST.JSToken.SEMI, "Expected ';' after return value.")
        return {"type": "ReturnStatement", "value": value, "line": keyword.line_num}

    def _break_statement(self):
        keyword = self._previous()
        self._consume(JST.JSToken.SEMI, "Expected ';' after break.")
        return {"type": "BreakStatement", "line": keyword.line_num}

    def _expression_statement(self):
        expr = self._expression()
        self._consume(JST.JSToken.SEMI, "Expected ';' after expression.")
        return {"type": "ExpressionStatement", "expression": expr}

    def _expression(self):
        return self._assignment()

    def _assignment(self):
        expr = self._logic_or()

        if self._check_any(self.ASSIGNMENT_OPS):
            operator = self._advance().tokenType.name
            value = self._assignment()

            if expr["type"] == "Identifier" or expr["type"] == "MemberExpression":
                return {
                    "type": "AssignmentExpression",
                    "operator": operator,
                    "target": expr,
                    "value": value,
                }
            raise self._error(self._previous(), "Invalid assignment target.")

        return expr

    def _logic_or(self):
        expr = self._logic_and()
        while self._match(JST.JSToken.OR, JST.JSToken.VBAR):
            operator = self._previous().tokenType.name
            right = self._logic_and()
            expr = {"type": "BinaryExpression", "operator": operator, "left": expr, "right": right}
        return expr

    def _logic_and(self):
        expr = self._equality()
        while self._match(JST.JSToken.AND, JST.JSToken.AMPER):
            operator = self._previous().tokenType.name
            right = self._equality()
            expr = {"type": "BinaryExpression", "operator": operator, "left": expr, "right": right}
        return expr

    def _equality(self):
        expr = self._comparison()
        while self._match(JST.JSToken.EQEQUAL, JST.JSToken.NOTEQUAL):
            operator = self._previous().tokenType.name
            right = self._comparison()
            expr = {"type": "BinaryExpression", "operator": operator, "left": expr, "right": right}
        return expr

    def _comparison(self):
        expr = self._term()
        while self._match(
            JST.JSToken.GREATER,
            JST.JSToken.GREATEREQUAL,
            JST.JSToken.LESS,
            JST.JSToken.LESSEQUAL,
        ):
            operator = self._previous().tokenType.name
            right = self._term()
            expr = {"type": "BinaryExpression", "operator": operator, "left": expr, "right": right}
        return expr

    def _term(self):
        expr = self._factor()
        while self._match(JST.JSToken.PLUS, JST.JSToken.MINUS):
            operator = self._previous().tokenType.name
            right = self._factor()
            expr = {"type": "BinaryExpression", "operator": operator, "left": expr, "right": right}
        return expr

    def _factor(self):
        expr = self._unary()
        while self._match(JST.JSToken.STAR, JST.JSToken.SLASH):
            operator = self._previous().tokenType.name
            right = self._unary()
            expr = {"type": "BinaryExpression", "operator": operator, "left": expr, "right": right}
        return expr

    def _unary(self):
        if self._match(
            JST.JSToken.EXCLAMATION,
            JST.JSToken.PLUS,
            JST.JSToken.MINUS,
            JST.JSToken.TYPEOF,
            JST.JSToken.DELETE,
            JST.JSToken.VOID,
        ):
            operator = self._previous().tokenType.name
            right = self._unary()
            return {"type": "UnaryExpression", "operator": operator, "argument": right}
        return self._call()

    def _call(self):
        expr = self._primary()

        while True:
            if self._match(JST.JSToken.LPAR):
                args = []
                if not self._check(JST.JSToken.RPAR):
                    args.append(self._expression())
                    while self._match(JST.JSToken.COMMA):
                        args.append(self._expression())
                self._consume(JST.JSToken.RPAR, "Expected ')' after arguments.")
                expr = {"type": "CallExpression", "callee": expr, "arguments": args}
            elif self._match(JST.JSToken.DOT):
                name = self._consume(JST.JSToken.IDENTIFIER, "Expected property name after '.'.")
                expr = {"type": "MemberExpression", "object": expr, "property": name.value}
            else:
                break

        return expr

    def _primary(self):
        if self._match(JST.JSToken.FALSE):
            return {"type": "Literal", "value": False}
        if self._match(JST.JSToken.TRUE):
            return {"type": "Literal", "value": True}
        if self._match(JST.JSToken.NULL):
            return {"type": "Literal", "value": None}

        if self._match(JST.JSToken.NUMBER, JST.JSToken.STRING):
            token = self._previous()
            return {"type": "Literal", "value": token.value}

        if self._match(JST.JSToken.IDENTIFIER):
            return {"type": "Identifier", "name": self._previous().value}

        if self._match(JST.JSToken.LPAR):
            expr = self._expression()
            self._consume(JST.JSToken.RPAR, "Expected ')' after expression.")
            return {"type": "Grouping", "expression": expr}

        raise self._error(self._peek(), f"Expected expression, got {self._peek().tokenType.name}.")

    def _match(self, *types):
        for token_type in types:
            if self._check(token_type):
                self._advance()
                return True
        return False

    def _check_any(self, token_types):
        if self._is_at_end():
            return False
        return self._peek().tokenType in token_types

    def _check(self, token_type):
        if self._is_at_end():
            return False
        return self._peek().tokenType == token_type

    def _advance(self):
        if not self._is_at_end():
            self.current += 1
        return self._previous()

    def _is_at_end(self):
        return self._peek().tokenType == JST.JSToken.ENDMARKER

    def _peek(self):
        return self.tokens[self.current]

    def _previous(self):
        return self.tokens[self.current - 1]

    def _consume(self, token_type, message):
        if self._check(token_type):
            return self._advance()
        raise self._error(self._peek(), message)

    def _error(self, token, message):
        err = f"Line: {token.line_num}; Error: {message}"
        raise Exception(err)
