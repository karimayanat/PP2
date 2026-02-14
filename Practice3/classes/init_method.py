class Person:
    def __init__(self, name, age):
        self.name = name
        self.age = age
p1 = Person("Misha", 21)
print(p1.name)
print(p1.age)

class Person1:
  def __init__(self, name, age=18):
    self.name = name
    self.age = age
p1 = Person1("Emil")
p2 = Person1("Tobias", 25)
print(p1.name, p1.age)
print(p2.name, p2.age)