#AxiomX-0.0.57721 the Euler-Mascheroni Edition
#For info, view README.md.

import time

print("AxiomX loading...")
time.sleep(3)
print("AxiomX is ready to use!")

version = "0.0.57721"

pi = 3.141592653589793
e = 2.718281828459045
tau = 2 * pi
lemniscate = 2.622057554292119

def absolute(x):
    if (x > 0):
        return x
    else:
        return -x
        
# integrating integrals
def integrate(function, lowlim, uplim, n=10000):
    h = (uplim - lowlim) / n
    s = function(lowlim) + function(uplim)

    for i in range(1, n):
        x = lowlim + i * h
        if i % 2 == 0:
            s += 2 * function(x)
        else:
            s += 4 * function(x)

    return s * h / 3
    
def summation(lowlim, uplim, function):
    sum = 0
    for _ in range(lowlim, uplim + 1):
        sum += function(_)
    return sum
    
def sqrt(n):
    if n < 0:
        raise ValueError("square root of a negative number is complex, not real")
    x1 = int(n**0.5)
    x2 = 0
    for _ in range(100000):
        x2 = 0.5*(x1 + (n / x1))
        x1 = x2
    return x1

def cbrt(N, tolerance=1e-10, max_iterations=1000):
    x = N / 3.0 if N != 0 else 0.0
    for i in range(max_iterations):
        x_next = x - (x**3 - N) / (3 * x**2)
        if abs(x_next - x) < tolerance:
            return x_next
        x = x_next 
    return x

def gamma(x):
    # Lanczos approximation constants
    p = [
        0.99999999999980993,
        676.5203681218851,
        -1259.1392167224028,
        771.32342877765313,
        -176.61502916214059,
        12.507343278686905,
        -0.13857109526572012,
        9.9843695780195716e-6,
        1.5056327351493116e-7
    ]

    if x < 0.5:
        # Reflection formula
        return pi / (sin(pi * x) * gamma(1 - x))

    x -= 1
    t = p[0]
    for i in range(1, len(p)):
        t += p[i] / (x + i)

    g = 7
    return sqrt(2 * pi) * (x + g + 0.5)**(x + 0.5) * (e**(-(x + g + 0.5))) * t
    
def factorial(x):
    if (x // 1 == x):
        f = 1
        while x > 0:
            f *= x
            x -= 1
        return f
    else:
        return gamma(x+1)

def zeta(n):
    zetval = 0
    if n <= 1:
        raise ValueError("zeta(n) diverges for n <= 1")
    for _ in range(1, 100001):
        zetval += (1 / _**n)
    return zetval
    
def beta(n):
    if n == 0:
        return 0.5
    total = 0.0
    for i in range(100000):
        total += ((-1)**i) / ((2*i + 1)**n)
    return total
    
def bernoulli(n):
    if n % 2 == 1 and n != 1:
        return 0
    A = [0.0] * (n+1)
    for m in range(n+1):
        A[m] = 1.0 / (m+1)
        for j in range(m, 0, -1):
            A[j-1] = j * (A[j-1] - A[j])
    return A[0]

def stieltjes(n, m=20000, corrections=4):
    # main summation
    S = sum(ln(k)**n / k for k in range(1, m+1))
    
    # principal term
    S -= ln(m)**(n+1) / (n+1)
    
    # Euler–Maclaurin corrections
    for j in range(1, corrections+1):
        b = bernoulli(2*j)
        term = b / factorial(2*j)
        # derivative simplified:
        term *= (-1)**(2*j-1) * n * ln(m)**(n-1) / (m**(2*j))
        S += term
        
    return (-1)**n * S
        
    
def continued_fraction(constant, terms=5):
    denominator = []
    denominator.append(int(constant))
    for i in range(terms-1):
        constant = constant - denominator[i]
        denominator.append(int(float(1) / float(constant)))
        constant = 1 / constant
    return denominator
    
def evaluate_continued_fraction(denominators):
    result = 0
    for denominator in reversed(denominators):
        result = denominator + (1 / result) if result != 0 else denominator
    return result

    
#more constants
gelfond = e**pi
sqrt_2 = sqrt(2)
sqrt_3 = sqrt(3)
sqrt_5 = sqrt(5)
golden_ratio = (1+sqrt_5) / 2
silver_ratio = 1 + sqrt_2
apery = zeta(3)
catalan = beta(2)
ramanujan = gelfond**sqrt(163)
euler_mascheroni = 0.577215664901533
gauss = lemniscate / pi
gelfond_schneider = 2**sqrt_2

#now we can represent symbols using greek letters and common symbols

π = pi
τ = tau
ϖ = lemniscate
G = gauss
γ = euler_mascheroni
φ = golden_ratio
σ = silver_ratio
g = catalan

# logarithmic functions

def exp(n):
    return e**n

def ln(x):
    if x <= 0:
        raise ValueError("ln(x) is undefined for x <= 0")
    k = 0
    while x >= 2.0:
        x *= 0.5
        k += 1
    while x < 1.0:
        x *= 2.0
        k -= 1
    y = (x - 1) / (x + 1)
    y2 = y * y
    s = 0.0
    term = y
    n = 1
    while absolute(term) > 1e-17:
        s += term / n
        term *= y2
        n += 2
    return 2*s + k * (0.693147180559945309417232121458176568) # ln 2
    
def log10(x):
    return ln(x) / ln(10)
    
def log2(x):
    return log10(x) / log10(2)
    
def log(arg, base):
    return log2(arg) / log2(base)

# trigonometric function

def radians(deg):
    return (pi/180)*deg
    
def degrees(rad):
    return (180/pi)*rad
    
def sin(x, terms=20):
    quarter = ((x // tau) + 1) % 4
    if x == pi:
        return 0
    x = x % tau
    # Input validation
    if not isinstance(x, (int, float)):
        raise TypeError("x must be a number (int or float).")
    if not isinstance(terms, int) or terms <= 0:
        raise ValueError("terms must be a positive integer.")
    sine_value = 0.0
    for n in range(terms):
        term = ((-1)**n) * (x**(2*n + 1)) / factorial(2*n + 1)
        sine_value += term
    return sine_value
    if quarter == 1:
        return sine_value
    elif quarter == 2:
        return sqrt(1 - (sine_value**2))
    elif quarter == 3:
        return -sine_value
    elif quarter == 0:
        return -sqrt(1 - (sine_value**2))
        
def cos(x):
    return sin((pi/2)-x)
    
def tan(x):
    return sin(x) / cos(x)

def cot(x):
    return 1 / tan(x)

def sec(x):
    return 1 / cos(x)
    
def cosec(x):
    return 1 / sin(x)

def arcsin(x, iterations=10):
    if abs(x) > 1:
        raise ValueError("x must be in [-1, 1]")
    y = x
    for _ in range(iterations):
        y -= (sin(y) - x) / cos(y)
    return y
    
def arccos(x):
    return (pi / 2) - arcsin(x)
    
def arctan(x):
    return arcsin(x / sqrt(1+ x**2))
    
def arccot(x):
    return (pi/2) - arctan(x)

def arcsec(x):
    return arccos(1/x)
    
def arccosec(x):
    return arcsin(1/x)
    
def sinh(x):
    return (e**x - e**(-x))/2
    
def cosh(x):
    return (e**x + e**(-x))/2
    
def tanh(x):
    return sinh(x) / cosh(x)
    
def coth(x):
    return cosh(x) / sinh(x)
    
def sech(x):
    return 1 / cosh(x)
    
def cosech(x):
    return 1 / sinh(x)
    
def arcsinh(x):
    return ln(x + sqrt(x**2 + 1))
    
def arccosh(x):
    return abs(arcsinh(sqrt(x**2 - 1)))
    
def arccoth(x):
    return 0.5 * ((x+1)/(x-1))
    
def arctanh(x):
    return arccoth(1/x)
    
def arcsech(x):
    return arccosh(1/x)
    
def arccosech(x):
    return arcsinh(1/x)