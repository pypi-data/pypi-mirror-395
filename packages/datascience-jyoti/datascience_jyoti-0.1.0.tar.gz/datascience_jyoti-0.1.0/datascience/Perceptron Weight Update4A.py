import math

def main():
    coeff = 0.1
    s = [{'val': 0, 'out': 0, 'wo': 0, 'wi': 0, 'top': 0} for _ in range(3)]

    # Taking input values
    for i in range(3):
        s[i]['val'] = float(input("Enter the input value to target output: "))
        s[i]['top'] = int(input("Enter the target value: "))

    for i in range(3):
        if i == 0:
            s[i]['wo'] = -1.0
            s[i]['wi'] = -0.3
        else:
            s[i]['wo'] = s[i-1]['wo']
            s[i]['wi'] = s[i-1]['wi']

        s[i]['aop'] = s[i]['wo'] + (s[i]['wi'] * s[i]['val'])
        s[i]['out'] = s[i]['aop']
        delta = (s[i]['top'] - s[i]['out']) * s[i]['out'] * (1 - s[i]['out'])
        corr = coeff * delta * s[i]['out']
        s[i]['wo'] += corr
        s[i]['wi'] += corr

    print("VALUE\tTarget\tActual\two\twi")
    for i in range(3):
        print(f"{s[i]['val']}\t{s[i]['top']}\t{s[i]['out']}\t{s[i]['wo']}\t{s[i]['wi']}")

if __name__ == "__main__":
    main()
