# Syntax Analyzer (Parser) for LOLcode
class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.literals = ['NUMBR','NUMBAR','YARN','TROOF',]
        self.arith_op = ['SUMOF','DIFFOF','PRODUKTOF','QUOSHUNTOF','MODOF', 'BIGGROF','SMALLROF']
        self.bool_bin_op = ['BOTHOF','EITHEROF','WONOF']
        self.bool_inf_op = ['ALLOF','ANYOF']
        self.com_op = ['BOTHSAEM', 'DIFFRINT']
        self.operations = self.arith_op + self.bool_bin_op + self.bool_inf_op + self.com_op + ['NOT', 'SMOOSH']
        self.statements = ['OBTW', 'WAZZUP', 'VARIABLE', 'ORLY', 'WTF', 'IMINYR', 'VISIBLE', 'GIMMEH']

    def current_token(self):
        # Returns the current token.
        return self.tokens[self.index] if self.index < len(self.tokens) else None

    def next_token(self):
        # Consume the current token and move to the next one.
        token = self.current_token()
        self.index += 1
        return token

    def parse(self):
        self.parse_program()

    def parse_program(self):
        start_token = self.current_token()["type"]
        if start_token and (start_token in ['HAI','BTW','OBTW']):
            print("Parsing program...")
            while self.current_token()["type"] != 'HAI': # iterate while HAI is not found
                self.next_token()
            # print("hai found: ",self.current_token()["type"])
            self.next_token()
            # Parse statements until we encounter 'KTHXBYE'
            while self.current_token() and self.current_token()["type"] != 'KTHXBYE':
                self.parse_statements()

            if self.current_token() and self.current_token()["type"] == 'KTHXBYE':
                print("Program ends with KTHXBYE")
                self.next_token()  # Consume 'KTHXBYE'
            else:
                raise RuntimeError("Expected KTHXBYE at the end of the program.")
        else:
            raise RuntimeError("Program must start with HAI or a valid comment BTW or OBTW.")
        
    def parse_statements(self):
        token = self.current_token()

        if token and token["type"] == "BTW":
            # Parse comment
            pass
        elif token and token["type"] in self.statements:
            self.parse_statement()
        else:
            raise RuntimeError(f"Unexpected statement starting with {token}")

    def parse_statement(self):
        token = self.current_token()
        if token:
            if token["type"] == 'WAZZUP':
                self.next_token() # next token should be I HAS A
                print("Variable declaration section start")
                self.parse_variable_declaration()  # Parse variable declaration
            elif token["type"] == 'VISIBLE':
                self.parse_visible_statement()  # Parse VISIBLE statement
            elif token["type"] in 'VARIABLE':
                self.parse_assignment()  # Parse variable assignment
            elif token["type"] == 'GIMMEH':
                self.parse_gimmeh_statement()
                # parse input 
            elif token["type"] == 'HOWIZI':
                self.parse_function_definition()  # Parse function definition
            elif token["type"] == 'IIZ':
                self.parse_function_call()  # Parse function call
            elif token["type"] == 'FOUNDYR' or token["type"] == 'GTFO':
                self.parse_return_statement()  # Parse return statement
            else:
                raise RuntimeError(f"Unexpected statement starting with {token}")


    def parse_variable_declaration(self):
        while self.current_token()["type"] != 'BUHBYE':
            # if other statement (except comments) starts inside wazzup, raise error
            if self.current_token()['type'] not in ['OBTW','BTW'] and  self.current_token()['type'] in self.statements:
                raise RuntimeError(f"Variable declaration section must end with BUHBYE, got {self.current_token()['type']}")
            
            if self.current_token()['type'] in ['OBTW','BTW']:
                comment = self.current_token() # change to next_token if nahiwalay na ang text sa keyword
                print(f"Comment detected: {comment['value']}")
                # INSERT OBTW HANDLER
                self.next_token() # consume comment

            self.next_token()  # Consume 'I HAS A' 
            # The next token should be the variable name
            variable_token = self.next_token()
            if variable_token["type"] != 'VARIABLE':
                raise RuntimeError(f"Expected variable name, got {variable_token}")
            
            # check if there's an 'ITZ' (indicating an initialization)
            if self.current_token() and self.current_token()["type"] == 'ITZ':
                self.next_token()  # Consume 'ITZ'
                # check whether the next token is a valid expression
                expression = self.parse_expression()

                # Handle initialization
                print(f"Declared variable {variable_token['value']} with initialization value {expression}")
                self.next_token() # consume expression
                # print(f"Declared variable {expression['value']} with initialization value {expression['value']}")
            else:
                # No initialization, just declaration
                print(f"Declared variable {variable_token['value']} without initialization")
        print("Variable declaration section end")
        self.next_token()

    def parse_expression(self):
        exp_token = self.current_token()

        if exp_token:
            if exp_token["type"] in self.literals + ['VARIABLE']:
                value = exp_token['value']
                self.next_token()  # Consume the expression token
                return value
            elif exp_token["type"] in self.operations:
                exp = self.parse_operation()
                return exp
            elif exp_token["type"] == 'IIZ':
                value = self.parse_function_call()
                return value
            else:
                raise RuntimeError(f"Unexpected expression starting with {exp_token}")
        else:
            raise RuntimeError("Expected expression, but got None")
        

    def parse_operation(self):
        operation = self.next_token() # store operation used
        if operation:
            # Handle arithmetic operations
            if operation["type"] in self.arith_op:
                op = self.parse_arith_op()
            else:
                raise RuntimeError(f"Unexpected operation starting with {operation}")
        return f"{operation['value'] + str(op)}"

    def parse_arith_op(self):
        first_op = self.parse_expression()
        self.next_token() # move to "AN" token
        if first_op:
            if self.current_token()["type"] != "AN":
                raise RuntimeError(f"Expected AN, got {self.current_token()}")
            else:
                self.next_token() # consume AN
                # check if second operator is a valid expression
                second_op = self.parse_expression()
                if second_op:
                    return first_op, second_op
                else:
                    raise RuntimeError(f"Expected expression for second operand, got {second_op}")
        else:
            raise RuntimeError(f"Expected expression for first operand, got {first_op}")

    def parse_gimmeh_statement(self):
        self.next_token() # consume 'GIMMEH'
        var = self.next_token()
        if var['type'] == 'VARIABLE':
            print(f"GIMMEH: {var}")
        else:
            raise RuntimeError(f"Expected a valid variable, got {var}")

    def parse_visible_statement(self):
        # to fix: handle infinite arity delimited by '+'
        self.next_token()  # Consume 'VISIBLE'
        # value_token = self.next_token()  # The value to print
        exp = self.parse_expression()
        if exp:
            print(f"Visible: {exp}")
        else:
            raise RuntimeError(f"Expected an expression, got {exp}")
        self.next_token()

    def parse_assignment(self):
        variable = self.next_token()  # Variable to assign value to
        if variable['type'] != 'VARIABLE':
            raise RuntimeError(f"Expected variable, got {variable}")
                                 
        # self.next_token() # go to token 'R'
        if self.current_token()['type'] != 'R':
            raise RuntimeError(f"Expected R, got {self.current_token()}")
        self.next_token() # consume R
        value_token = self.current_token()  # Value to assign
        exp = self.parse_expression()
        if not exp:
            raise RuntimeError(f"Expected expression, got {value_token}")

        print(f"Assigned {exp} to variable {variable['value']}")
        self.next_token()

    def parse_function_definition(self):
        self.next_token()  # Consume 'HOWIZI'
        func_name_token = self.current_token()
        if func_name_token['type'] == 'LABEL':
            func_name = func_name_token['value']
            self.next_token()  # Consume function name
            # Now parse parameters
            params = self.parse_parameters()
            print(f"Function definition: {func_name} with parameters {params}")
            # Now parse the function body
            self.parse_function_body(func_name)
        else:
            raise RuntimeError(f"Expected function name after 'HOW IZ I', got {func_name_token}")

    def parse_function_body(self, func_name):
        # Parse statements inside function until 'IFUSAYSO'
        while self.current_token() and self.current_token()['type'] != 'IFUSAYSO':
            self.parse_statements()
        if self.current_token() and self.current_token()['type'] == 'IFUSAYSO':
            self.next_token()  # Consume 'IFUSAYSO'
            print(f"End of function definition: {func_name}")
        else:
            raise RuntimeError(f"Expected 'IF U SAY SO' at end of function definition {func_name}")

    def parse_parameters(self):
        params = []
        if self.current_token() and self.current_token()['type'] == 'YR':
            self.next_token()  # Consume 'YR'
            param = self.parse_expression()
            params.append(param)
            # Now check for more parameters
            while self.current_token() and self.current_token()['type'] == 'AN':
                self.next_token()  # Consume 'AN'
                if self.current_token() and self.current_token()['type'] == 'YR':
                    self.next_token()  # Consume 'YR'
                    param = self.parse_expression()
                    params.append(param)
                else:
                    raise RuntimeError(f"Expected 'YR' after 'AN' in parameter list, got {self.current_token()}")
        return params

    def parse_function_call(self):
        self.next_token()  # Consume 'IIZ'
        func_name_token = self.current_token()
        if func_name_token['type'] == 'LABEL':
            func_name = func_name_token['value']
            self.next_token()  # Consume function name
            # Now parse parameters
            params = self.parse_parameters()
            print(f"Function call: {func_name} with parameters {params}")
            return f"FunctionCall({func_name}, {params})"
        else:
            raise RuntimeError(f"Expected function name after 'I IZ', got {func_name_token}")

    def parse_return_statement(self):
        token = self.current_token()
        if token['type'] == 'FOUNDYR':
            self.next_token()  # Consume 'FOUNDYR'
            expr = self.parse_expression()
            print(f"Return with value: {expr}")
        elif token['type'] == 'GTFO':
            self.next_token()  # Consume 'GTFO'
            print("Return (GTFO) without value")
        else:
            raise RuntimeError(f"Expected 'FOUND YR' or 'GTFO', got {token}")