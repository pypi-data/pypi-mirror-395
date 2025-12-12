def main():
    inputs = [float(input(f"Enter input {i+1}: ")) for i in range(3)]
    weights = [float(input(f"Initialize weight {i+1}: ")) for i in range(3)]
    desired_output = float(input("Enter the desired output: "))

    while True:
        net_input = sum(w * x for w, x in zip(weights, inputs))
        output = 1 if net_input >= 0 else 0
        delta = desired_output - output
        if delta == 0:
            print("\nOutput is correct")
            break
        for i in range(3):
            weights[i] += delta * inputs[i]
        print(f"\nDelta: {delta}")
        print("Adjusted Weights:", weights)

if __name__ == "__main__":
    main()
print("Enter input 1: 1")
print("Enter input 2: 0")
print("Enter input 3: 1")

#Initialize weight 1: 0
#Initialize weight 2: 0
#Initialize weight 3: 0
#Enter the desired output: 1
