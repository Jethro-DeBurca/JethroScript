class Token:
    def __init__(self, type, val):
        self.type = type
        self.val = val
    
    def __repr__(self):
        return str(self.val)

class Integer(Token):
    def __init__(self, val):
        super().__init__("INT", val)

class Float(Token):
    def __init__(self, val):
        super().__init__("FLT", val)

class Operation(Token):
        def __init__(self, val):
            super().__init__("OP", val)

class Declaration(Token):
        def __init__(self, val):
            super().__init__("DECL", val)

class Variable(Token):
        def __init__(self, val):
            super().__init__("VAR(?)", val)

class Boolean(Token):
        def __init__(self, val):
            super().__init__("BOOL", val)

class Comparison(Token):
        def __init__(self, val):
            super().__init__("COMP", val)

class Reserved(Token):
        def __init__(self, val):
            super().__init__("RSV", val)
