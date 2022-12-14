from model import *
# visitador que cuenta cuantos nodo de tipo number existen en el arbol


class NumberCounter(Visitor):
    def __init__(self):
        self.counter = 0

    def visit_Number(self, node):
        self.counter = self.counter + 1

    def total(self):
        return self.counter


# visitador que cuenta cuantos nodo de tipo addition existen en el arbol
class AdditionCounter(Visitor):
    def __init__(self):
        self.counter = 0

    def visit_Addition(self, node):
        # los nodos compuestos deben propagar la visita
        node.leftNode.accept(self)
        node.rightNode.accept(self)
        self.counter = self.counter + 1

    def total(self):
        return self.counter


class UnaryOperatorCounter(Visitor):
    def __init__(self):
        self.counter = 0

    def visit_UnaryOperator(self, node):
        node.oneNode.accept(self)
        self.counter = self.counter + 1
    
    def total(self):
        return self.counter
