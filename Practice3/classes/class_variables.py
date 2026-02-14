class Student:
    count = 0   #class variable
    def __init__(self, name):
        self.name = name
        Student.count += 1
s1 = Student("Alice")
print(s1.count)
s2 = Student("Bob")
print(s2.count)
s3 = Student("Charlie")
print(s3.count)
print(Student.count)