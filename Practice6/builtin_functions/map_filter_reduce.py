from functools import reduce
numbers = [1, 2, 3, 4, 5]

#map() – square numbers
squares = list(map(lambda x: x**2, numbers))
print("Squares:", squares)

#filter() – keep even numbers
evens = list(filter(lambda x: x % 2 == 0, numbers))
print("Even numbers:", evens)

#reduce() – sum all numbers
total = reduce(lambda a, b: a + b, numbers)
print("Sum:", total)

#type checking and conversion
values = ["10", "20", "30"]
converted = list(map(int, values))
print("Converted to integers:", converted)
for v in converted:
    print(v, "is int:", isinstance(v, int))