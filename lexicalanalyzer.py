import re
import syntaxanalyzer as s

# used regex 
TOKEN_PATTERNS = [
    ('HAI', r'^HAI\b'),                           # Program start keyword
    ('KTHXBYE', r'^KTHXBYE\b'),                         # Program end keyword
    ('WAZZUP', r'^WAZZUP\b'),     # Variable declaration keyword
    ('BUHBYE', r'^BUHBYE\b'),   
    ('IHASA', r'^I HAS A\b'),          # Variable initialization keyword
    ('ITZ', r'^ITZ\b'),
    ('VAR_ASSIGN', r'^R\b'), # Variable assignment keyword
    ('VISIBLE', r'^VISIBLE\b'),                      # Output statement keyword
    ('PLUS', r'^(\+)\s'),                  # Output statement separator
    ('GIMMEH', r'^GIMMEH\b'),                        # Input statement keyword
    ('BTW', r'^\b(BTW) (.*)\b'),                # Single-line comment
    ('OBTW', r'^OBTW\b'),            # Start of multi-line comment
    ('TLDR', r'^TLDR\b'),              # End of multi-line comment
    ('NUMBAR', r'(\+|-)?\d*\.\d+'),                    # Float (NUMBAR) literal
    ('NUMBR', r'(\+|-)?\d+'),                          # Integer (NUMBR) literal
    ('YARN', r'"([^"\\]|\\.)*"'),                         # String (YARN) literal
    ('TROOF', r'^(WIN|FAIL)\b'),                   # Boolean (TROOF) literals WIN/FAIL
    ('ISNOWA', r'^IS NOW A\b'),
    ('SUMOF', r'^SUM OF\b'),
    ('DIFFOF', r'^DIFF OF\b'),
    ('PRODUKTOF', r'^PRODUKT OF\b'),
    ('QUOSHUNTOF', r'^QUOSHUNT OF\b'),
    ('MODOF', r'^MOD OF\b'),
    ('BIGGROF', r'^BIGGR OF\b'),
    ('SMALLROF', r'^SMALLR OF\b'),
    ('BOTHOF', r'^BOTH OF\b'),
    ('EITHEROF', r'^EITHER OF\b'),
    ('WONOF', r'^WON OF\b'),
    ('ANYOF', r'^ANY OF\b'),
    ('ALLOF', r'^ALL OF\b'),
    ('NOT', r'^NOT\b'),
    ('BOTHSAEM', r'^BOTH SAEM\b'),
    ('DIFFRINT', r'^DIFFRINT\b'),
    # ('MATH_OP', r'(SUM OF|DIFF OF|PRODUKT OF|QUOSHUNT OF|MOD OF|BIGGR OF|SMALLR OF)\b'),  # Math operations
    # ('BOOL_OP', r'(BOTH OF|EITHER OF|WON OF|NOT |ANY OF|ALL OF)\b'),  # Boolean operations
    # ('COMP_OP', r'(BOTH SAEM|DIFFRINT)\b'),         # Comparison operations
    ('AN', r'AN\b'),
    ('ORLY', r'^O RLY\?$'),                      # If-statement start
    ('YARLY', r'^YA RLY\b'),                      # If-true branch
    ('NOWAI', r'^NO WAI\b'),                     # If-false branch
    ('OIC', r'^OIC\b'),                          # End of if-statement
    ('WTF', r'^WTF\?$'),                  # Switch-case start
    ('OMG', r'^OMG\b'),                            # Case keyword
    ('OMGWTF', r'^OMGWTF\b'),                 # Default case keyword
    ('IMINYR', r'^(IM IN YR) ([A-Za-z_][A-Za-z0-9_]*)\b'),                 # Loop start
    ('IMOUTTAYR', r'^(IM OUTTA YR) ([A-Za-z_][A-Za-z0-9_]*)\b'),                # Loop end
    ('UPPIN', r'^UPPIN\b'),                # Increment operation in loops
    ('NERFIN', r'^NERFIN\b'),               # Decrement operation in loops
    ('YR', r'^YR\b'),
    ('R', r'^R$'),
    # ('A', r'^A$'),
    ('SMOOSH', r'^SMOOSH\b'),
    ('MAEK', r'^MAEK\b'),
    ('TIL', r'^TIL\b'),
    ('WILE', r'^WILE\b'),
    ('MKAY', r'^MKAY\b'),
    ('IFUSAYSO', r'^IF U SAY SO\b'),
    ('HOWIZI', r'^(HOW IZ I) ([A-Za-z_][A-Za-z0-9_]*)\b'), 
    ('IIZ', r'^(I IZ) ([A-Za-z_][A-Za-z0-9_]*)\b'), 
    ('GTFO', r'^GTFO\b'), 
    ('FOUNDYR', r'^FOUND YR\b'), 
    ('VARIABLE', r'^[A-Za-z_][A-Za-z0-9_]*\b'),      # Variable names
    ('WHITESPACE', r'\s+'),
    # add pa po kayo if may kulang paaaa
]

# keywords = [
#     'HAI', 'KTHXBYE', 'WAZZUP', 'BUHBYE', 'BTW', 'OBTW', 'TLDR', 'ITZ', 'R', 'NOT', 'DIFFRINT',
#     'SMOOSH', 'MAEK', 'A', 'VISIBLE', 'GIMMEH', 'MEBBE', 'OIC', 'WTF?', 'OMG', 'OMGWTF', 'UPPIN', 'NERFIN', 'YR',
#     'TIL', 'WILE', 'GTFO', 'MKAY'
# ]

token_regex = '|'.join(f'(?P<{pair[0]}>{pair[1]})' for pair in TOKEN_PATTERNS)

def append_token(tokens, token_type, value, line_num):
    tokens.append({
        'type': token_type,
        'value': value,
        'line': line_num
    })

# tokenizer function to process the LOLCode source code
def tokenize(source_code):
    tokens = []                  
    in_multiline_comment = False # tracker to check if we're inside a multi-line comment
    multiline_comments = ""

    for line_num, line in enumerate(source_code, start=1):
        index = 0
        line = line.strip() 
        substring = line[index:]

        if not line: # skip empty lines
            continue
        
        while index < len(substring):
            match = None
            for token_type, pattern in TOKEN_PATTERNS:
                match = re.match(pattern, substring[index:])
                # for match in matches:
                if match:
                    break
            
            if match:
                # token_type = match.lastgroup
                value = match.group(0)

                if token_type == "WHITESPACE":
                    index += len(value)
                    continue

                # if in_multiline_comment:
                #     print(token_type)
                #     multiline_comments = multiline_comments+ value + "\n"
                #     index += len(value)
                if token_type == 'BTW':
                    append_token(tokens, token_type, match.group(1), line_num)
                    append_token(tokens, 'SINGLECOMMENT', match.group(2), line_num)
                    index += len(value)
                    continue
                elif token_type == 'OBTW':
                    # print("multiline found")
                    in_multiline_comment = True
                    append_token(tokens, token_type, value, line_num)
                    # index += len(value)
                    # continue
                elif token_type == "TLDR":
                    # print("multiline: ",multiline_comments)
                    # append_token(tokens, token_type, multiline_comments, line_num)
                    in_multiline_comment = False
                    multiline_comments = ""
                    # index += len(value)
                    # continue  #  skip since comment sha

                elif token_type == 'IMINYR' or token_type == 'IMOUTTAYR' or token_type == 'HOWIZI' or token_type == 'IIZ':
                    append_token(tokens, token_type, match.group(1), line_num)
                    append_token(tokens, 'LABEL', match.group(2), line_num)
                    index += len(value)
                    continue
                if not in_multiline_comment:
                    append_token(tokens, token_type, value, line_num)
                index += len(value)
            elif in_multiline_comment:
                multiline_comments+ value + "\n"
                append_token(tokens, 'MULTICOMMENT', value, line_num)
                index += len(value)
                continue
            else:
                raise RuntimeError(f'Unexpected character {substring[index]} at line {line_num}')
            # index += len(value)
            # append_token(tokens, token_type, value, line_num)      
    return tokens

def read_file():
    with open("input_files/01_variables.lol", 'r') as file: # read input.txt
        lines = file.readlines()
        return lines

# source_code = """
# HAI
# I HAS A var ITZ 3
# VISIBLE "Hello, World!"
# BTW this is a comment
# OBTW
# Multi-line comment
# TLDR
# SUM OF 2 AN 3
# KTHXBYE
# """

# pwede rin file input

source_code = read_file()
tokens = tokenize(source_code)
# for token in tokens:
#     print(token)
for token in tokens:
    print(f"{token['line'] : <5} {token['type'] : <25} {token['value']}")
parse = s.SyntaxAnalyzer(tokens)
parse.parse()
