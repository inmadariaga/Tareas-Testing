def fib(n):
    a = 1
    b = 1
    if n == 1:
        return a
    elif n == 2:
        return b
    elif n == 3:
        return a + b
    else:
        return fib(n - 1) + fib(n - 2)