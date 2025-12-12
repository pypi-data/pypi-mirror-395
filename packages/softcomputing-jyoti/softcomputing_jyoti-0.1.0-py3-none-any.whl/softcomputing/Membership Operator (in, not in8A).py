# PRACTICAL 8A
# Membership Operators: in, not in

list1 = [1, 2, 3, 4, 5]
list2 = [6, 7, 8, 9]

overlap = any(i in list2 for i in list1)

if overlap:
    print("Lists are overlapping")
else:
    print("Lists are NOT overlapping")
