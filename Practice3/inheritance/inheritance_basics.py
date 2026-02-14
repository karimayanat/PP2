class Person:
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
    def print_name(self):
        print(self.fname, self.lname)
x = Person("Jhon", "Doe")
x.print_name()

class Student(Person):
    def __init__(self, fname, lname):
        Person.__init__(self, fname, lname)
x = Student("Mike", "Olsen")
x.print_name()