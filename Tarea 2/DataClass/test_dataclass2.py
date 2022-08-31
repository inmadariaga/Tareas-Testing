class Dog:
    def __init__(self, name, breed, age):
        self.name = name
        self.breed = breed
        self.age = age
    
    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setBreed(self, breed):
        self.breed = breed

    def getBreed(self):
        return self.breed
    
    def setAge(self, age):
        self.age = age
    
    def getAge(self):
        return self.age