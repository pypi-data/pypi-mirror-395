import re

token_specs = [
    ("NUMBER", r"\d+(\.\d+)?"),  # Числа (int/float)
    ("PR", r"\bpr\b"),           # print
    ("IND", r"\bind\b"),         # input
    ("ST", r"\bst\b"),           # str()
    ("IN", r"\bin\b"),           # int()
    ("LEN", r"\blen\b"),         # len()
    ("SR", r"\bsr\b"),           # str reverse
    ("SQUARE", r"\bsquare\b"),   # square
    ("SQ", r"\bnosq\b"),         # non-zero check
    ("DEF", r"\bdef\b"),         # def function
    ("HELP", r"\bhelp\b"),       # help
    ("BIT", r"\bbit\b"),         # binary
    ("AB", r"\bab\b"),           # abs
    ("MX", r"\bmx\b"),           # max
    ("MN", r"\bmn\b"),           # min
    ("SM", r"\bsm\b"),           # sum
    ("FL", r"\bfl\b"),           # float
    ("RN", r"\brn\b"),           # round
    # Новые Python команды
    ("LIST", r"\blist\b"),
    ("DICT", r"\bdict\b"),
    ("RANGE", r"\brange\b"),
    ("SORT", r"\bsort\b"),
    ("REV", r"\brev\b"),
    # C++ стиль
    ("IF", r"\bif\b"),
    ("ELSE", r"\belse\b"),
    ("WHILE", r"\bwhile\b"),
    ("FOR", r"\bfor\b"),
    ("CPP_PRINT", r"\bcout\b"),
    ("VEC", r"\bvec\b"),         # vector
    ("ARR", r"\barr\b"),         # array
    # Rust стиль
    ("VEC_NEW", r"\bvec!\b"),
    ("MATCH", r"\bmatch\b"),
    ("ENUM", r"\benum\b"),
    # Переменные
    ("ID", r"[a-zA-Z_][a-zA-Z0-9_]*"),
    # Операторы
    ("PLUS", r"\+"),
    ("MINUS", r"-"),
    ("MUL", r"\*"),
    ("DIV", r"/"),
    ("EQ", r"="),
    ("RAV", r":="),
    ("LPAREN", r"\("),
    ("RPAREN", r"\)"),
    ("LBRACKET", r"\["),
    ("RBRACKET", r"\]"),
    ("COMMA", r","),
    ("SEMICOLON", r";"),
    ("STRING", r'"[^"]*"|\'[^\']*\''),
    ("WHITESPACE", r"\s+"),
    ("COMMENT", r"//.*"),
]

def tokenize(code):
    tokens = []
    while code:
        for name, pattern in token_specs:
            match = re.match(pattern, code)
            if match:
                value = match.group(0)
                if name not in ("WHITESPACE", "COMMENT"):
                    tokens.append((name, value))
                code = code[len(value):]
                break
        else:
            raise SyntaxError(f"Unknown symbol: '{code[0]}' at position {len(tokens)}")
    return tokens
