from . rule import *

class logicFunctionCounterVisitor(NodeVisitor):
    def __init__(self):
        self.functions = 0

    def check_function(self, nodeFunction):
        if nodeFunction.name != '__init__':
            if len(nodeFunction.body) <= 1:
                if isinstance(nodeFunction.body[0], Return):
                    if isinstance(nodeFunction.body[0].value, Attribute):
                        return nodeFunction.body[0].value.value.id != 'self'
                    return True
                elif isinstance(nodeFunction.body[0], Assign):
                    return nodeFunction.body[0].targets[0].value.id != 'self'
                else:
                    return True
            else:
                return True
        return False

    def visit_ClassDef(self, node: ClassDef):
        for function in node.body:
            if self.check_function(function):
                self.functions = self.functions + 1

    def total(self):
        return self.functions

class DataclassVisitor(WarningNodeVisitor):
    def visit_ClassDef(self, node: ClassDef):
        visitor = logicFunctionCounterVisitor()
        visitor.visit(node)
        if visitor.total() == 0:
            self.addWarning('DataClassWarning', node.lineno, 'class ' + node.name + ' is a DataClass')

class DataclassRule(Rule):
    def analyze(self, ast):
        visitor = DataclassVisitor()
        visitor.visit(ast)
        return visitor.warningsList()