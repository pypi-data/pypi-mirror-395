i will send you scripts

A = np.array([
    [2.,1.,-1.],
    [-3.,-1.,2.],
    [-2.,1.,2.]
])

b = np.array([8, -11,-3])
def gaus(A,b):
  N = len(A)
  #print(A)
  for i in range (N):
    for j in range(i+1,N):
      m = A[j,i] / A[i,i]
      #print (m)
      for k in range(i, N):
        A[j,k] = A[j, k] - m * A [i,k]
      #print (A)
      b[j] -= m* b[i]
      #print(b)
  x = np.zeros(N)
  x[N-1] = b[N-1] / A[N-1,N-1]
  print(x)
  for i in range(N-1, -1,-1):
    sum = 0
    for j in range(i+1, N):
      sum += A[i,j] * x[j]
    x[i] = (b[i]-sum)/A[i,i]
    print(x)
gaus(A,b)

A = np.array([
    [2.,1.,-1.],
    [-3.,-1.,2.],
    [-2.,1.,2.]
])

b = np.array([8, -11,-3])
def determinant(A):
  if len(A) == 2:
    return A[0,0] * A[1,1] - A[0,1]*A[1,0]
  sum = 0
  for i in range (len(A)):
    M = np.copy(A)
    M = np.delete(M, 0, axis=0)
    M = np.delete(M, i, axis=1)
    sum += (-1)**i * A[0,i] * determinant(M)
    #print(sum)
  return sum

def cramers(A,b):
  x = np.zeros(len(A))
  for i in range(len(A)):
    M=np.copy(A)
    M[:, i] = b
    x[i] = determinant(M) / determinant(A)
  return x

cramers(A,b)     
def Jacobi(A,b,x0, tol = 1e-5, N=1000):
  xnew = np.copy(x0)
  xold = np.copy(x0)
  for k in range(N):
    for i in range (len(A)):
      sum = 0
      for j in range (len(A)):
        if i!=j:
          sum += A[i,j]*xold[j]
      xnew[i] = (b[i] - sum) / A[i,i]
    if np.max(np.abs(xnew-xold)) < tol:
      print(f'converged at {k+1}')
      return  xnew
    xold = xnew
  return xnew
import numpy as np
import matplotlib.pyplot as plt

def leastsquares(x,b):
  n = len(x)
  sumx = sum(xi for xi in x)
  sumx2 = sum(xi*xi for xi in x)
  sumy = sum(y for y in b)
  sumxy = sum(x[i]*b[i] for i in range (n))

    # [sum_x2   sum_x ] [m] = [sum_xy]
    # [sum_x       n  ] [b]   [sum_y ]

  A = np.array([[sumx2, sumx], [sumx, n]])
  b = np.array([sumxy, sumy])

  print(cramers(A,b))
  return cramers(A,b)
x = np.array([1,2,3,4,5,6,7,8,9,10])
y = np.array([1.3,3.5,4.2,5.0,7.0,8.8,10.1,12.5,13.0,15.6])
m,b = leastsquares(x,y)
predict = [m*xi + b for xi in x]
te = sum((y[i] - predict[i])**2 for i in range (len(x)))
print(te)
print(m,b)
plt.scatter(x,y)
plt.plot(x, m*x+b)
plt.grid()
plt.show()
# 1.
def f(x):
  return 1/x
a, b = 1, 3
x = np.linspace(1, 3, 21)
y = f(x)

#Discrete Least Squares
def matrix_discreate(x, y):
  A_2 = np.array([          # degree two approximation
      [len(x), np.sum(x), np.sum(x**2)],
      [np.sum(x), np.sum(x**2), np.sum(x**3)],
      [np.sum(x**2), np.sum(x**3), np.sum(x**4)]
  ])
  b_2 = np.array([np.sum(y), np.sum(x*y), np.sum(x**2*y)])

  A_3 = np.array([          # degree three approximation
      [len(x), np.sum(x), np.sum(x**2), np.sum(x**3)],
      [np.sum(x), np.sum(x**2), np.sum(x**3), np.sum(x**4)],
      [np.sum(x**2), np.sum(x**3), np.sum(x**4), np.sum(x**5)],
      [np.sum(x**3), np.sum(x**4), np.sum(x**5), np.sum(x**6)]
  ])
  b_3 = np.array([np.sum(y), np.sum(x*y), np.sum(x**2*y), np.sum(x**3*y)])
  return A_2, b_2, A_3, b_3

A_2, b_2, A_3, b_3 = matrix_discreate(x, y)
a2 = np.linalg.solve(A_2, b_2)
a3 = np.linalg.solve(A_3, b_3)
plt.title('Discrete Least Squares Approximation')
plt.scatter(x, y)
plt.plot(x, a2[0] + a2[1]*x + a2[2]*x**2, label='Degree two')
plt.plot(x, a3[0] + a3[1]*x + a3[2]*x**2 + a3[3]*x**3, label='Degree three')
plt.legend()
plt.show()

#Continuous Least Squares
def f(x):
  return 1/x
def f1(x):
  return x*f(x)
def f2(x):
  return x**2*f(x)
def f3(x):
  return x**3*f(x)

def coeff(a, b, k):
  return 1 / (k+1) * (np.power(b, k+1) - np.power(a, k+1))

def matrix_continuous(a, b):
  A2 = np.array([
      [coeff(a, b, 0), coeff(a, b, 1), coeff(a, b, 2)],
      [coeff(a, b, 1), coeff(a, b, 2), coeff(a, b, 3)],
      [coeff(a, b, 2), coeff(a, b, 3), coeff(a, b, 4)]
  ])

  A3 = np.array([
      [coeff(a, b, 0), coeff(a, b, 1), coeff(a, b, 2), coeff(a, b, 3)],
      [coeff(a, b, 1), coeff(a, b, 2), coeff(a, b, 3), coeff(a, b, 4)],
      [coeff(a, b, 2), coeff(a, b, 3), coeff(a, b, 4), coeff(a, b, 5)],
      [coeff(a, b, 3), coeff(a, b, 4), coeff(a, b, 5), coeff(a, b, 6)]
  ])
  return A2, A3

def simpsons_integration(f, a, b):
  h = (b - a) / 1000
  S = 0
  for i in range(1000):
    a_i = a + i * h
    b_i = a_i + h
    S = S + h / 6 * (f(a_i) + 4 * f((a_i + b_i) / 2) + f(b_i))
  return S

A2, A3 = matrix_continuous(a, b)

int_f = simpsons_integration(f, a, b)
int_f1 = simpsons_integration(f1, a, b)
int_f2 = simpsons_integration(f2, a, b)
int_f3 = simpsons_integration(f3, a, b)

b2 = np.array([int_f, int_f1, int_f2])
b3 = np.array([int_f, int_f1, int_f2, int_f3])

a2 = np.linalg.solve(A_2, b_2)
a3 = np.linalg.solve(A_3, b_3)
x = np.linspace(a, b, 1000)
plt.title('Continuous Least Squares Approximation')
plt.plot(x, f(x), label='f(x)')
plt.plot(x, a2[0] + a2[1]*x + a2[2]*x**2, label='Degree two')
plt.plot(x, a3[0] + a3[1]*x + a3[2]*x**2 + a3[3]*x**3, label='Degree three')
plt.legend()
plt.show()
eps = 1e-5
N = 1000
def power_method(A):
  x0 = np.random.rand(len(A))
  lamb0 = 0
  for i in range(N):
    x = A @ x0
    x = x / np.max(np.abs(x))
    lamb = x @ (A@x) / (x@x)
    if np.abs(lamb - lamb0) < eps:
      break
    lamb0 = lamb
    x0 = x
  return lamb, x

def inverse_power_method(A):
  x0 = np.random.rand(len(A))
  lamb0 = 0
  for i in range(N):
    y = gaussian_elimination(A, x0)
    x = y / np.max(np.abs(y))
    lamb = x @ (A@x) / (x@x)
    if np.abs(lamb - lamb0) < eps:
      break
    lamb0 = lamb
    x0 = x
  return lamb, x

def shifted_inverse_power_method(A, shift):
  x0 = np.random.rand(len(A))
  I = np.eye(len(A))
  lamb0 = 0
  for i in range(N):
    y = np.linalg.solve(A - shift*I, x0)
    x = y / np.max(np.abs(y))
    lamb = x @ (A@x) / (x@x)
    if np.abs(lamb - lamb0) < eps:
      break
    lamb0 = lamb
    x0 = x
  return lamb, x
# System 1:
#Fixed-point
x = np.array([0.5, 0.5, 0.5])
x_new = np.zeros(len(x))
eps = 1e-5
N = 10
for i in range(N):
    x_new[0] = (2*np.cos(x[1] * x[2]) + 1) / 6
    x_new[1] = (np.sqrt(x[0]**2 + np.sin(x[2]) + 1.06) + 0.9) / (-9)
    x_new[2] = (3 - 10*np.pi - 3 * np.exp(-x[0]*x[1])) / 60

    diff = x_new - x
    if np.max(np.abs(diff)) < eps:
        break
    x = x_new.copy()
print(f"Fixed-point: {x}")

#Newton's Method
def F(x):
  f1 = 6*x[0] - 2*np.cos(x[1]*x[2]) - 1
  f2 = 9*x[1] + np.sqrt(x_new[0]**2 + np.sin(x_new[2]) + 1.06) + 0.9
  f3 = 60*x[2] + 3*np.exp(-x[0]*x[1]) + 10*np.pi - 3
  return np.array([f1, f2, f3])

def J(x):
  J11, J12, J13 = 6, 2*x[2]*np.sin(x[1]*x[2]), 2*x[1]*np.sin(x[1]*x[2])
  J21, J22, J23 = (2*x[0])/(2*np.sqrt(x[0]**2 + np.sin(x[2]) + 1.06)), 9, (np.cos(x[2]))/(2*np.sqrt(x[0]**2 + np.sin(x[2]) + 1.06))
  J31, J32, J33 = -3*x[1]*np.exp(-x[0]*x[1]), -3*x[0]*np.exp(-x[0]*x[1]), 60
  return np.array([[J11, J12, J13], [J21, J22, J23], [J31, J32, J33]])

for i in range(N):
  j = J(x)
  f = F(x)
  y = np.linalg.solve(j, -f)
  x_new = x + y
  diff = x_new - x
  if np.max(np.abs(diff)) < eps:
    break
  x = x_new.copy()
print(f"Newton's Method: {x}")
def Y(x):
  return np.exp(2) * (np.exp(4) - 1)**(-1) * (np.exp(2*x) - np.exp(-2*x)) + x

# IVP 1  | y1'' = 4y1 - 4x | u=y1, v=y1'
def f1(v): # = u'= v
  return v
def f2(x, u): # = v'= 4u - 4x
  return 4*u - 4*x
a, b = 0, 1 # alpha=0 betta=2
h = 0.1
N = 10
x = np.linspace(a, b, N+1)
v = np.zeros(N+1)
u = np.zeros(N+1)
u[0] = 0
v[0] = 0
for i in range(N):
  k1u = h*f1(v[i])
  k1v = h*f2(x[i], u[i])
  k2u = h*f1(v[i] + k1v/2)
  k2v = h*f2(x[i]+h/2, u[i] + k1u/2)
  k3u = h*f1(v[i]+k2v/2)
  k3v = h*f2(x[i]+h/2, u[i]+k2u/2)
  k4u = h*f1(v[i]+k3v)
  k4v = h*f2(x[i]+h, u[i]+k3u)
  u[i+1] = u[i] + (k1u + 2*k2u + 2*k3u + k4u)/6
  v[i+1] = v[i] + (k1v + 2*k2v + 2*k3v + k4v)/6

# IVP 2 | y2'' = 4y2 | p=y2, q=y2'
def g1(q): # = p'= q
  return q
def g2(p): # = q'= 4p
  return 4*p
p = np.zeros(N+1)
q = np.zeros(N+1)
p[0] = 0
q[0] = 1
for i in range(N):
  k1p = h*g1(q[i])
  k1q = h*g2(p[i])
  k2p = h*g1(q[i] + k1q/2)
  k2q = h*g2(p[i] + k1p/2)
  k3p = h*g1(q[i]+k2q/2)
  k3q = h*g2(p[i]+k2p/2)
  k4p = h*g1(q[i]+k3q)
  k4q = h*g2(p[i]+k3p)
  p[i+1] = p[i] + (k1p + 2*k2p + 2*k3p + k4p)/6
  q[i+1] = q[i] + (k1q + 2*k2q + 2*k3q + k4q)/6

gamma = (2 - u[-1]) / p[-1]
y = u + gamma * p
print(gamma)
plt.plot(x, u, label='IVP 1')
plt.plot(x, p, label='IVP 2')
plt.plot(x, y, label='BVP', linewidth=4)
plt.plot(x, Y(x), label='Exact solution')
plt.legend()
plt.show()