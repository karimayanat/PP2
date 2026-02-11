students = [("Emil", 25), ("Tobias", 22), ("Linus", 28)]
sorted_students = sorted(students, key=lambda x: x[1])
print(sorted_students)

sorted_students1 = sorted(students, key=lambda x: x[0])
print(sorted_students1)

words = ["KBTU", "student", "home_work", "lesson"]
sorted_words = sorted(words, key=lambda x: len(x))
print(sorted_words)