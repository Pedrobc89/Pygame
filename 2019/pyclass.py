class Student(Person):
    def __init__(self, firstname, lastname, age, registration, classroom):

    

    def __init__(self, firstname, lastname, age):
        self.firstname = firstname
        self.lastname = lastname
        self.age = age
        self.name = self.firstname + " " + self.lastname 
    
    def __repr__(self):
        return " Name {}, {} years old".format(self.name, self.age)


    def YearBorn(self):
        return 2019 - age

a = Person("Lucas", "Silva", 16)
print(a)
b = Person("Pedro", "Costa", 29)
print(b)