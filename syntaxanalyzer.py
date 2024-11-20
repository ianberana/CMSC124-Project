# Syntax Analyzer (Parser) for LOLcode
class SyntaxAnalyzer:
    def __init__(self, tokens):
        self.tokens = tokens
        self.index = 0
        self.expressions = [
            'NUMBR',
            'NUMBAR',
            'YARN',
            'TROOF',
            'VARIABLE',
            'SUMOF',
            'DIFFOF',
            'PRODUKTOF',
            'QUOSHUNTOF',
            'MODOF',
            'BIGGROF',
            'SMALLROF',
            'BOTHOF',
            'EITHEROF',
            'WONOF',
            'ALLOF',
            'ANYOF',
            'NOT',
            'BOTHSAEM',
            'DIFFRINT'
        ]
        self.statements = ['OBTW', 'WAZZUP', 'VARIABLE', 'ORLY', 'WTF', 'IMINYR', 'VISIBLE']

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
        if token and token["type"] == 'WAZZUP':
            self.next_token() # next token should be I HAS A
            self.parse_variable_declaration()  # Parse variable declaration
        elif token and token["type"] == 'VISIBLE':
            self.parse_visible_statement()  # Parse VISIBLE statement
        elif token and token["type"] in 'VARIABLE':
            self.parse_assignment()  # Parse variable assignment
        else:
            raise RuntimeError(f"Unexpected statement starting with {token}")


    def parse_variable_declaration(self):
        while self.current_token()["type"] != 'BUHBYE':
            self.next_token()  # Consume 'I HAS A'
            # The next token should be the variable name
            variable_token = self.next_token()
            if variable_token["type"] != 'VARIABLE':
                raise RuntimeError(f"Expected variable name, got {variable_token}")
            
            # Look ahead to see if there's an 'ITZ' (indicating an initialization)
            if self.current_token() and self.current_token()["type"] == 'ITZ':
                self.next_token()  # Consume 'ITZ'
                
                value_token = self.next_token()  # Value (number or variable)
                if value_token["type"] not in self.expressions:
                    raise RuntimeError(f"Expected valid expression, got {value_token}")

                # Handle initialization
                print(f"Declared variable {variable_token['value']} with initialization value {value_token['value']}")
            else:
                # No initialization, just declaration
                print(f"Declared variable {variable_token['value']} without initialization")
        self.next_token()

    def parse_visible_statement(self):
        self.next_token()  # Consume 'VISIBLE'
        value_token = self.next_token()  # The value to print
        if value_token["type"] in self.expressions:
            print(f"Visible: {value_token['value']}")
        else:
            raise RuntimeError(f"Expected an expression, got {value_token}")

    def parse_assignment(self):
        token = self.next_token()
        variable_token = token  # Variable to assign value to
        if variable_token["type"] != 'R':
            raise RuntimeError(f"Expected R, got {variable_token}")

        value_token = self.next_token()  # Value to assign
        if value_token["type"] not in self.expressions:
            raise RuntimeError(f"Expected number or variable, got {value_token}")

        print(f"Assigned {value_token['value']} to variable {variable_token['value']}")