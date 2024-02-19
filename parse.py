# Create a binary tree from tokens

class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.idx = 0
        self.token = self.tokens[self.idx]
    
    def factor(self):
        if self.token.type == "INT" or self.token.type == "FLT":
            return self.token
        elif self.token.val == "(":
            self.move()
            expression = self.booleanExpression()
            return expression
        elif self.token.val == "not":
            operator = self.token
            self.move()
            return [operator, self.booleanExpression()]
        elif self.token.type.startswith("VAR"):
            return self.token
        elif self.token.val == "+" or self.token.val == "-":
            operator = self.token
            self.move()
            operand = self.factor()

            return [operator, operand]
    
    def term(self):
        # term = a factor multiplied, or divided by another factor 0 or more times
        # Left: 1 Root: * Right: 2 -> term = [1, *, 2]
        leftNode = self.factor()
        self.move()

        while self.token.val == "*" or self.token.val == "/":
            operation = self.token
            self.move()
            rightNode = self.factor()
            self.move()
            leftNode = [leftNode, operation, rightNode]
        
        return leftNode
    
    def if_statement(self):
        self.move()
        condition = self.booleanExpression()

        if self.token.val == "do":
            self.move()
            action = self.statement()

            return condition, action
        elif self.token[self.idx - 1].val == "do": # Unary operations
            action = self.statement()

            return condition, action

    def if_statements(self):
        conditions = []
        actions = []
        if_statement = self.if_statement()

        conditions.append(if_statement[0])
        actions.append(if_statement[1])

        while self.token.val == "elif":
            if_statement = self.if_statement()
            conditions.append(if_statement[0])
            actions.append(if_statement[1])
        
        if self.token.val == "else":
            self.move()
            self.move()
            else_action = self.statement()

            return [conditions, actions, else_action]
        
        return [conditions, actions]
    
    def whileStatement(self):
        self.move()
        condition = self.booleanExpression()

        if self.token.val == "do":
            self.move()
            action = self.statement()
            
            return [condition, action]
        elif self.token[self.idx - 1].val == "do": # Unary operations
            action = self.statement()

            return [condition, action]
    
    def compExpression(self):
        leftNode = self.expression()

        while self.token.type == "COMP":
            operation = self.token
            self.move()
            rightNode = self.expression()
            leftNode = [leftNode, operation, rightNode]
        
        return leftNode
    
    def booleanExpression(self):
        leftNode = self.compExpression()

        while self.token.type == "BOOL":
            operation = self.token
            self.move()
            rightNode = self.compExpression()
            leftNode = [leftNode, operation, rightNode]
        
        return leftNode
    
    def expression(self):
        leftNode = self.term()

        while self.token.val == "+" or self.token.val == "-":
            operation = self.token
            self.move()
            rightNode = self.term()
            leftNode = [leftNode, operation, rightNode]
        
        return leftNode

    def variable(self):
        if self.token.type.startswith("VAR"):
            return self.token
    
    def statement(self):
        if self.token.type == "DECL":
            # Variable assignment
            self.move()
            leftNode = self.variable()
            self.move()

            if self.token.val  == "=":
                operation = self.token
                self.move()
                rightNode = self.booleanExpression()

                return [leftNode, operation, rightNode]
        elif self.token.type == "INT" or self.token.type == "FLT" or self.token.type == "OP" or self.token.val == "not":
            # Arithmetic expression
            return self.booleanExpression()
        elif self.token.val == "if":
            return [self.token, self.if_statements()]
        elif self.token.val == "while":
            return [self.token, self.whileStatement()]
    
    def parse(self):
        # Define grammar rules for non terminals
        return self.statement()
    
    def move(self):
        self.idx += 1
        if self.idx < len(self.tokens):
            self.token = self.tokens[self.idx]
