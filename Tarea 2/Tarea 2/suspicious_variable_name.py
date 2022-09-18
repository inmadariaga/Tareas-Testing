from . rule import *


class SuspiciousVariableNameVisitor(WarningNodeVisitor):

    def visit_Assign(self, node: Assign):
        if isinstance(node.targets[0], Attribute):
            if len(node.targets[0].attr) == 1:
                self.addWarning('SuspiciousVariableName', node.lineno, 'variable ' + node.targets[0].value.id + '.' + node.targets[0].attr + ' has suspicious name')
        else:
            if len(node.targets[0].id) == 1:
                self.addWarning('SuspiciousVariableName', node.lineno, 'variable ' + node.targets[0].id + ' has suspicious name')

class SuspiciousVariableNameRule(Rule):
    def analyze(self, ast):
        visitor = SuspiciousVariableNameVisitor()
        #print(dump(ast))
        visitor.visit(ast)
        return visitor.warningsList()