class Person:
    def __init__(self, fname, lname):
        self.fname = fname
        self.lname = lname
    def print_name(self):
        print(self.fname, self.lname)
x = Person("Jhon", "Doe")
x.print_name()
class Student(Person):
    def __init__(self, fname, lname, grade):
        super().__init__(fname, lname)
        self.grade = grade
    def welcome(self):
        print("Welcome,", self.fname, self.lname + ",", "your grade is", self.grade)
x = Student("Mike", "Olsen", "Exelent")
x.welcome()