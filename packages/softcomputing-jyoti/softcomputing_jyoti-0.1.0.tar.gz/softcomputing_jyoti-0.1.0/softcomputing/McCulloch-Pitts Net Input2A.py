num_ip = int(input("Enter the number of inputs: "))
w1 = 1
w2 = 1

x1 = []
x2 = []
print(f"For the {num_ip} inputs calculate the net input using yin = x1*w1 + x2*w2")

for j in range(num_ip):
    ele1 = int(input("x1 = "))
    ele2 = int(input("x2 = "))
    x1.append(ele1)
    x2.append(ele2)

print("x1 =", x1)
print("x2 =", x2)

n = [val * w1 for val in x1]
m = [val * w2 for val in x2]

Yin = [n[i] + m[i] for i in range(num_ip)]
print("Yin =", Yin)

# One weight excitatory, other inhibitory
Yin = [n[i] - m[i] for i in range(num_ip)]
print("After assuming one weight excitatory and other inhibitory Yin =", Yin)

Y = [1 if val >= 1 else 0 for val in Yin]
print("Y =", Y)
