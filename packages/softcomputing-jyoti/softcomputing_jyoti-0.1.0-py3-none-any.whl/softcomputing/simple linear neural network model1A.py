# 1st part: take input from user
n = int(input("Enter no. of elements: "))
print("Enter the inputs:")
inputs = []
for i in range(n):
    ele = float(input())
    inputs.append(ele)
print(inputs)

print("Enter the weights:")
weights = []
for i in range(n):
    ele = float(input())
    weights.append(ele)
print(weights)

print("The net input can be calculated as Yin = x1w1 + x2w2 + x3w3")
Yin = []
for i in range(n):
    Yin.append(inputs[i] * weights[i])

print("Net input (Yin) =", round(sum(Yin), 3))
