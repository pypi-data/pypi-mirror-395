def main():
    w = float(input("Consider a single neuron perceptron with a single input weight: "))
    d = float(input("Enter the learning coefficient: "))
    x = float(input("Enter the input value: "))
    t = float(input("Enter the target output: "))

    for i in range(10):
        net = x * w
        a = 1 if net >= 0 else 0
        div = d * (t - a)
        w = w + div
        print(f"Iteration: {i+1}, Output: {a}, Change in weight: {div}, Adjusted weight: {w}")

if __name__ == "__main__":
    main()
