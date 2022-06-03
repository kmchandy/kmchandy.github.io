def f(x, K=2):
    return x[-K-1: -1]

def g(y, N, InitialValue):
    output = InitialValue
    if len(y)%N > 0:
        y = y + "0"*(N - len(y)%N)
    blocks = [y[i: i+N] for i in range(0, len(y), N)]
    for block in blocks: output = f(output+block)
    return output


if __name__ == "__main__":
    g(y="abcdefgh", N=3, InitialValue="**")

    
    
