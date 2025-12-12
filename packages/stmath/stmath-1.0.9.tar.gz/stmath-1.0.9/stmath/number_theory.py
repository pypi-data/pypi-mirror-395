# number_theory.py
import math

def gcd(a, b):
    return math.gcd(a, b)

def lcm(a, b):
    return abs(a*b) // math.gcd(a, b)

def is_prime(n):
    if n < 2:
        return False
    for i in range(2, int(math.sqrt(n)) + 1):
        if n % i == 0:
            return False
    return True

def prime_factors(n):
    factors = []
    i = 2
    while i * i <= n:
        while n % i == 0:
            factors.append(i)
            n //= i
        i += 1
    if n > 1:
        factors.append(n)
    return factors

def totient(n):
    result = n
    for p in set(prime_factors(n)):
        result -= result // p
    return result

def mod_inverse(a, m):
    # Extended Euclidean Algorithm
    def egcd(a, b):
        if a == 0:
            return (b, 0, 1)
        g, y, x = egcd(b % a, a)
        return (g, x - (b // a) * y, y)
    g, x, _ = egcd(a, m)
    if g != 1:
        return None
    return x % m

def modular_pow(base, exp, mod):
    return pow(base, exp, mod)

def fibonacci(n):
    a, b = 0, 1
    for _ in range(n):
        a, b = b, a + b
    return a

def pell_number(n):
    if n == 0: return 0
    if n == 1: return 1
    p0, p1 = 0, 1
    for _ in range(2, n+1):
        p0, p1 = p1, 2*p1 + p0
    return p1

def catalan_number(n):
    return math.comb(2*n, n) // (n+1)

def divisor_count(n):
    count = 0
    for i in range(1, int(math.sqrt(n))+1):
        if n % i == 0:
            count += 2 if i != n//i else 1
    return count

def divisor_sum(n):
    total = 0
    for i in range(1, int(math.sqrt(n))+1):
        if n % i == 0:
            total += i
            if i != n//i:
                total += n//i
    return total
