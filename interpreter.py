from tokens import Integer, Float, Reserved

class Interpreter:
    def __init__(self, tree, base):
        self.tree = tree
        self.data = base
    
    def readINT(self, val):
        return int(val)
    
    def readFLT(self, val):
        return float(val)
    
    def readVAR(self, id):
        variable = self.data.read(id)
        variableType = variable.type

        return getattr(self, f"read{variableType}")(variable.val)
    
    def computeBinary(self, left, op, right):
        leftType = "VAR" if str(left.type).startswith("VAR") else str(left.type)
        rightType = "VAR" if str(right.type).startswith("VAR") else str(right.type)

        # Compute variable assignment
        if op.val == "=":
            left.type = f"VAR({rightType})"
            self.data.write(left, right)
            return self.data.readAll()

        # getattr = find method, and () = values passed to the method
        left = getattr(self, f"read{leftType}")(left.val)
        right = getattr(self, f"read{rightType}")(right.val)
        
        if op.val == "+":
            output = left + right
        elif op.val == "-":
            output = left - right
        elif op.val == "*":
            output = left * right
        elif op.val == "/":
            output = left / right
        elif op.val == ">":
            output = 1 if left > right else 0
        elif op.val == ">=":
            output = 1 if left >= right else 0
        elif op.val == "<":
            output = 1 if left < right else 0
        elif op.val == "<=":
            output = 1 if left <= right else 0
        elif op.val == "?=":
            output = 1 if left == right else 0
        elif op.val == "and":
            output = 1 if left and right else 0
        elif op.val == "or":
            output = 1 if left or right else 0
        
        return Integer(output) if (leftType == "INT" and rightType == "INT") else Float(output)
    
    def computeUnary(self, operator, operand):
        operandType = "VAR" if str(operand.type).startswith("VAR") else str(operand.type)
        operand = getattr(self, f"read{operandType}")(operand.val)

        if operator.val == "+":
            output = +operand
        elif operator.val == "-":
            output = -operand
        elif operator.val == "not":
            output = 1 if not operand else 0
        
        return Integer(output) if (operandType == "INT") else Float(output)
    
    def interpret(self, tree = None):
        # PostOrder traversal = LeftSubTree -> RightSubTree -> Root
        if tree is None:
            tree = self.tree

        if isinstance(tree, list):
            if isinstance(tree[0], Reserved):
                if tree[0].val == "if":
                    for idx, condition in enumerate(tree[1][0]):
                        evaluation = self.interpret(condition)
                        if evaluation.val == 1:
                            return self.interpret(tree[1][1][idx])
                    
                    if len(tree[1]) == 3:
                        return self.interpret(tree[1][2])
                    else:
                        return
                elif tree[0].val == "while":
                    condition = self.interpret(tree[1][0])

                    while condition.val == 1:
                        print(self.interpret(tree[1][1]))

                        condition = self.interpret(tree[1][0])
                    
                    return

        
        if isinstance(tree, list) and len(tree) == 2: # Unary operation
            expression = tree[1]

            if isinstance(expression, list):
                expression = self.interpret(expression)

            return self.computeUnary(tree[0], expression)
        elif not isinstance(tree, list): # No operation
            return tree
        else:
            leftNode = tree[0]
            if isinstance(leftNode, list):
                leftNode = self.interpret(leftNode) # recursive descent parsing to evalue leftSubTree

            rightNode = tree[2]
            if isinstance(rightNode, list):
                rightNode = self.interpret(rightNode) # recursive descent parsing to evalue rightSubTree

            operator = tree[1] # Root

            return self.computeBinary(leftNode, operator, rightNode)
