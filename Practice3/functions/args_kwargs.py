def my_function(greeting, *names):
    for name in names:
        print(greeting, name)
my_function("Hello,", "Emil", "Tobias", "Linus")

def sum_num(*args):
    total = 0
    for num in args:
        total += num
    return total
print(sum_num(1, 2, 3))
print(sum_num(10, 20, 30, 40))

def information(**myvar):
    print("Type:", type(myvar))
    print("Name:", myvar["name"])
    print("Age:", myvar["age"])
    print("All data:", myvar)
information(name = "Tobias", age = 30, city = "Bergen")

def mixed_function(normal_arg, *args, **kwargs):
    print("normal:", normal_arg)
    print("args:", args)
    print("kwargs:", kwargs)
mixed_function("Hello", 1, 2, 3, a=10, b=20)