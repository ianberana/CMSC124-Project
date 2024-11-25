# Syntax Analyzer (Parser) for LOLcode
class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.is_not_finished = True
        self.literals = ['NUMBR','NUMBAR','YARN','TROOF',]
        self.arith_op = ['SUMOF','DIFFOF','PRODUKTOF','QUOSHUNTOF','MODOF', 'BIGGROF','SMALLROF']
        self.bool_bin_op = ['BOTHOF','EITHEROF','WONOF']
        self.bool_inf_op = ['ALLOF','ANYOF']
        self.com_op = ['BOTHSAEM', 'DIFFRINT']
        self.operations = self.arith_op + self.bool_bin_op + self.bool_inf_op + self.com_op + ['NOT', 'SMOOSH']
        self.expressions = self.literals + self.operations + ['VARIABLE']
        self.statements = ['BTW', 'OBTW', 'WAZZUP', 'ORLY', 'WTF', 'IMINYR', 'VISIBLE', 'GIMMEH'] + self.expressions

    def current_token(self):
        # Returns the current token.
        # return self.tokens[self.index] if self.index < len(self.tokens) else None
        if self.index < len(self.tokens):
            return self.tokens[self.index]
        
        return None

    def next_token(self):
        # Consume the current token and move to the next one.
        token = self.current_token()
        self.index += 1
        if self.index == len(self.tokens):
            self.is_not_finished = False
        return token

    def parse(self):
        self.parse_program()

    def parse_comments(self):
        token = self.current_token()
        if token['type'] == 'BTW':
            self.next_token()
            print(f"Single comment detected: {self.current_token()['value']}")
            self.next_token()

        elif token['type'] == 'OBTW':
            self.next_token()
            print(f"Multi comment detected:")
            while True:
                token = self.next_token()
                if token['type'] == 'TLDR':
                    break
                print(f"    : {token['value']}")

    def parse_program(self):
        self.parse_comments()
        start_token = self.current_token()['type']
        if self.is_not_finished and start_token == 'HAI':
            print("Parsing program...")
            # while self.current_token()["type"] != 'HAI': # iterate while HAI is not found
            #     self.next_token()
            # print("hai found: ",self.current_token()["type"])
            self.next_token()
            # Parse statements until we encounter 'KTHXBYE'
            while self.is_not_finished and self.current_token()['type'] != 'KTHXBYE':
                self.parse_statements()

            if self.is_not_finished and self.current_token()['type'] == 'KTHXBYE':
                print("Program ends with KTHXBYE")
                self.next_token()  # Consume 'KTHXBYE'
            else:
                raise RuntimeError("Expected KTHXBYE at the end of the program.")
        else:
            raise RuntimeError("Program must start with HAI or a valid comment BTW or OBTW.")
        
    def parse_statements(self):
        self.parse_comments()
        token = self.current_token()

        # if token and token["type"] == "BTW":
        #     # Parse comment
        #     pass
        if token and token['type'] in self.statements:
            self.parse_statement()
        else:
            raise RuntimeError(f"Unexpected statement starting with {token}")

    def parse_statement(self):
        token = self.current_token()
        if token:
            if token['type'] == 'BTW' or token['type'] == 'OBTW':
                self.parse_comments()
            elif token['type'] == 'WAZZUP':
                print("Variable declaration section start")
                self.parse_variable_declaration()  # Parse variable declaration
            elif token['type'] == 'VISIBLE':
                self.parse_visible_statement()  # Parse VISIBLE statement
            elif token['type'] == 'VARIABLE' and self.tokens[self.index+1]['type'] == 'R':
                self.parse_assignment()  # Parse variable assignment
            elif token['type'] == 'GIMMEH':
                self.parse_gimmeh_statement() # Parse GIMMEH statement
            elif token['type'] == 'ORLY':
                print("If-else (ORLY) section start")
                self.parse_if_else()  # Parse if-else (ORLY) assignment
            elif token['type'] == 'WTF':
                print("Switch (WTF) section start")
                self.parse_switch()
                # parse input 
            else:
                exp = self.parse_expression()
                if exp:
                    print(f"Expression ({exp}) stored in IT")
                    self.next_token()
                else:
                    raise RuntimeError(f"Unexpected statement starting with {token}")

    def parse_variable_declaration(self):
        self.next_token()
        self.parse_comments()
        while self.current_token()['type'] != 'BUHBYE':
            # if other statement (except comments) starts inside wazzup, raise error
            # if self.current_token()['type'] not in ['OBTW','BTW'] and  self.current_token()['type'] in self.statements:
            #     raise RuntimeError(f"Variable declaration section must end with BUHBYE, got {self.current_token()['type']}")
            
            # if self.current_token()['type'] in ['OBTW','BTW']:
            #     comment = self.current_token() # change to next_token if nahiwalay na ang text sa keyword
            #     print(f"Comment detected: {comment['value']}")
            #     # INSERT OBTW HANDLER
            #     self.next_token() # consume comment


            self.parse_comments()
            if self.current_token()['type'] == 'IHASA':
                self.next_token()
            # The next token should be the variable name
            variable_token = self.next_token()
            if variable_token['type'] != 'VARIABLE':
                raise RuntimeError(f"Expected variable name, got {variable_token}")
            
            # check if there's an 'ITZ' (indicating an initialization)
            if self.is_not_finished and self.current_token()['type'] == 'ITZ':
                self.next_token()  # Consume 'ITZ'
                # check whether the next token is a valid expression
                expression = self.parse_expression()

                # Handle initialization
                print(f"Declared variable ({variable_token['value']}) with initialization value {expression}")
                self.next_token() # consume expression
                # print(f"Declared variable {expression['value']} with initialization value {expression['value']}")
            else:
                # No initialization, just declaration
                print(f"Declared variable ({variable_token['value']}) without initialization")
        print("Variable declaration section end")
        self.next_token()

    def parse_expression(self):
        exp_token = self.current_token() # stores the current expression

        if self.is_not_finished:
            # return value if expression is a valid literal or a variable
            if exp_token['type'] in list(self.literals + ['VARIABLE']):
                return exp_token['value']
            # check if expression is a valid operation
            elif exp_token['type'] in self.operations:
                # print(f"declared an operation: {exp_token['value']}")
                exp = self.parse_operation()
                # returns value of operation
                return exp
            else:
                raise RuntimeError(f"Unexpected expression starting with {exp_token}")        

    def parse_operation(self):
        operation = self.next_token() # store operation used
        if self.is_not_finished:
            # Handle arithmetic operations
            if operation['type'] in self.arith_op:
                op = self.parse_arith_op()
            elif operation['type'] in self.bool_bin_op:
                op = self.parse_bool_bin_op()
            else:
                raise RuntimeError(f"Unexpected operation starting with {operation}")
        return f"{operation['value'] + str(op)}"

    def parse_arith_op(self):
        first_op = self.parse_expression()
        self.next_token() # move to "AN" token
        if first_op:
            if self.current_token()['type'] != 'AN':
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

    def parse_bool_bin_op(self):
        first_op = self.parse_expression()
        self.next_token() # move to "AN" token
        if first_op:
            if self.current_token()['type'] != 'AN':
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
        var = self.current_token()
        if var['type'] == 'VARIABLE':
            print(f"GIMMEH: {var['value']}")
            self.next_token()
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
        # if variable['type'] != 'VARIABLE':
        #     raise RuntimeError(f"Expected variable, got {variable}")
                                 
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

    def parse_if_else(self):
        self.next_token() # Consume 'ORLY'
        self.parse_comments() # Consume comments
        yarly = self.next_token() 
        if self.is_not_finished and yarly['type'] == 'YARLY': # Match If/YARLY token
            print("If (ORLY) section start")
            while self.is_not_finished and self.current_token()['type'] not in ['NOWAI', 'OIC']: # Consume statements until Else/NOWAI or If-end/OIC
                self.parse_statement()
            print("If (ORLY) section end")

            if self.current_token()['type'] == 'NOWAI': # Match Else/NOWAI token
                self.next_token()
                print("Else (NOWAI) section start")
                while self.is_not_finished and self.current_token()['type'] != 'OIC': # Consume statements until If-end/OIC
                    self.parse_statement()
                print("Else (NOWAI) section end")

            if self.current_token()['type'] == 'OIC': # Match If-end/OIC token
                print("If-else (YARLY) section end")
            else:
                raise RuntimeError(f"Expected If-end (OIC), got {yarly['value']}")

            self.next_token() # Go to next token
        else:
            raise RuntimeError(f"Expected If (ORLY) block , got {yarly['value']}")

    def parse_switch(self):
        self.next_token() # Consume 'WTF'
        self.parse_comments() # Consume comments
        omg = self.current_token() 
        if self.is_not_finished and omg['type'] == 'OMG': # Match Case/OMG token
            self.parse_omg() # Consume Case 'OMG' blocks

            print(self.current_token())
            if self.current_token()['type'] == 'OMGWTF': # Match default/OMGWTF token
                self.next_token()
                print("Default (OMGWTF) section start")
                while self.is_not_finished and self.current_token()['type'] != 'OIC': # Consume statements until Switch-end/OIC
                    self.parse_statement()

            if self.current_token()['type'] == 'OIC': # Match If-end/OIC token
                print("Switch (WTF) section end")
            else:
                raise RuntimeError(f"Expected Switch-end (OIC), got {omg['value']}")

            self.next_token() # Go to next token
        else:
            raise RuntimeError(f"Expected Case (OMG) block , got {omg['value']}")

    def parse_omg(self):
        self.next_token() # Consume 'OMG'
        literal = self.next_token() # Get literal and go to next token
        if literal['type'] in self.literals: # Match literal token
            print(f"OMG ({literal['value']}) section start")
            while self.is_not_finished and self.current_token()['type'] not in ['OMG', 'OMGWTF', 'OIC']: # Consume statements until Case/OMG, Default/OMGWTF, or Switch-end/OIC
                if self.current_token()['type'] == 'GTFO': # Match 'GTFO'
                    print(f"{self.current_token()['value']}")
                    self.next_token()
                else:
                    self.parse_statement() # Consume all statements within OMG block

            omg = self.current_token()
            if omg['type'] == 'OMG': # Match "OMG"
                self.parse_omg() # Recursively consume all 'OMG'
            else:
                return
        else:
            raise RuntimeError(f"Expected Literal, got {literal['value']}")