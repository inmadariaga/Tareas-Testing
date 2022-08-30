from . rule import *

class NeverReadedVariableVisitor(WarningNodeVisitor):
    def __init__(self):
        super().__init__()
        self.unused_variables = []

    def visit_Return(self, node: Return):
        unused_variables = [var.targets[0].id for var in self.unused_variables]
        if isinstance(node.value, Name):
            if node.value.id in unused_variables:
                index = unused_variables.index(node.value.id)
                unused_variables.pop(index)
                self.unused_variables.pop(index)
        NodeVisitor.generic_visit(self, node)

    def visit_BinOp(self, node: BinOp):
        unused_variables = [var.targets[0].id for var in self.unused_variables]
        if isinstance(node.left, Name):
            if node.left.id in unused_variables:
                index = unused_variables.index(node.left.id)
                unused_variables.pop(index)
                self.unused_variables.pop(index)
        if isinstance(node.right, Name):
            if node.right.id in unused_variables:
                index = unused_variables.index(node.right.id)
                unused_variables.pop(index)
                self.unused_variables.pop(index)
        NodeVisitor.generic_visit(self, node)

    def visit_Call(self, node: Call):
        unused_variables = [var.targets[0].id for var in self.unused_variables]
        for var in node.args:
            if var.id in unused_variables:
                index = unused_variables.index(var.id)
                unused_variables.pop(index)
                self.unused_variables.pop(index)
        NodeVisitor.generic_visit(self, node)

    def visit_Assign(self, node: Assign):
        self.unused_variables.append(node)
        NodeVisitor.generic_visit(self, node)

    def visit_FunctionDef(self, node: FunctionDef):
        NodeVisitor.generic_visit(self, node)
        if len(self.unused_variables) != 0:
            for unused_variable in self.unused_variables:
                self.addWarning("NeverReadedVariable", unused_variable.lineno, 'variable ' + unused_variable.targets[0].id + ' is never readed')
            self.unused_variables = []


class NeverReadedVariableRule(Rule):
    def analyze(self, ast):
        visitor = NeverReadedVariableVisitor()
        visitor.visit(ast)
        return visitor.warningsList()