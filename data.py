class Data:
    def __init__(self):
        self.variables = {}
    
    def read(self, id):
        return self.variables[id]
    
    def readAll(self):
        return self.variables
    
    def write(self, variable, expression):
        variableName = variable.val
        self.variables[variableName] = expression
