class Person:
    def __init__(self):
        self.numbers = []

    def addNumber(self, number):
        self.numbers.append(number)

    def get_average(self):
        if len(self.numbers) == 0:
            return 0
        sum = 0
        for i in numbers:
            sum = sum + i
        return sum / i