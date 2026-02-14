class Animal:
    def speak(self):
        print("Animal makes a sound")
class Dog(Animal):
    def speak(self):
        print("Dog barks")
a = Animal()
d = Dog()
a.speak()
d.speak()

class Person:
    def describe(self):
        print("I am a person")
class Student(Person):
    def describe(self):
        super().describe()
        print("I am also a student")
s = Student()
s.describe()