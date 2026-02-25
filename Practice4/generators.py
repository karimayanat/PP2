# task1_squares
def squares(n):
    for i in range(n + 1):
        yield i * i
n = int(input())
for num in squares(n):
    print(num)

# task2_even
def even_numbers(n):
    for i in range(0, n + 1):
        if i % 2 == 0:
            yield i
n = int(input())
print(",".join(str(num) for num in even_numbers(n)))

# task3_divisible
def divisible_by_3_and_4(n):
    for i in range(n + 1):
        if i % 12 == 0:
            yield i
n = int(input())
for num in divisible_by_3_and_4(n):
    print(num)

# task4_range_squares
def squares(a, b):
    for i in range(a, b + 1):
        yield i * i
a, b = map(int, input().split())
for num in squares(a, b):
    print(num)

# task5_countdown
def countdown(n):
    while n >= 0:
        yield n
        n -= 1
n = int(input())
for num in countdown(n):
    print(num)