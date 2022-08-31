from . rule import *

class VariableCounterVisitor(NodeVisitor):
    def __init__(self):
        self.variables = []
        self.args = []
        self.names = []

    def add_name(self, name):
        if len(self.names) == 0 and isinstance(name, Name):
            self.names.append(name)
        elif name.id not in [name.id for name in self.names]:
            self.names.append(name)

    def check_binop(self, node):
        if isinstance(node.left, BinOp):
            self.check_binop(node.left)
        elif isinstance(node.left, Name):
            self.add_name(node.left)
        if isinstance(node.right, Name):
            self.add_name(node.right)

    def check_call(self, node):
        for arg in node.args:
            if isinstance(arg, Name):
                self.add_name(arg)

    def check_assign(self, node):
        if isinstance(node.value, BinOp):
            self.check_binop(node.value)
        elif isinstance(node.value, Name):
            self.add_name(node.value)
        elif isinstance(node.value, Call):
            self.check_call(node.value)

    def check_return(self, node):
        if isinstance(node.value, BinOp):
            self.check_binop(node.value)
        elif isinstance(node.value, Call):
            self.check_call(node.value)
        elif isinstance(node.value, name):
            self.add_name(node.value)

    def visit_FunctionDef(self, node:FunctionDef):
        if len(node.args.args) != 0:
            for arg in node.args.args:
                self.args.append(arg)
        for element in node.body:
            if isinstance(element, Assign):
                if element.targets[0].id not in [var.targets[0].id for var in self.variables]:
                    self.variables.append(element)
        for element in node.body:
            if isinstance(element, Assign):
                self.check_assign(element)
            if isinstance(element, Return):
                self.check_return(element)
        variables = [var.targets[0].id for var in self.variables]
        args = [arg.arg for arg in self.args]
        for name in self.names:
            if name.id in variables:
                index = variables.index(name.id)
                variables.pop(index)
                self.variables.pop(index)
            if name.id in args:
                index = args.index(name.id)
                args.pop(index)
                self.args.pop(index)

class NeverReadedVariableVisitor(WarningNodeVisitor):
    def visit_FunctionDef(self, node: FunctionDef):
        visitor = VariableCounterVisitor()
        visitor.visit(node)
        if len(visitor.args) != 0:
            for arg in visitor.args:
                self.addWarning('NeverReadedVariable', arg.lineno, 'argument ' + arg.arg + ' is never used')
        if len(visitor.variables) != 0:
            for var in visitor.variables:
                self.addWarning('NeverReadedVariable', var.lineno, 'variable ' + var.targets[0].id + ' is defined and never used')


class NeverReadedVariableRule(Rule):
    def analyze(self, ast):
        visitor = NeverReadedVariableVisitor()
        visitor.visit(ast)
        return visitor.warningsList()