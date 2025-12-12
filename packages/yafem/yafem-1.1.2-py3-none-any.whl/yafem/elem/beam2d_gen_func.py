import numpy

def beam2d_gen_Kl(A, E, I, L, alpha, fa, fb, k0a, k0b, rho, theta):
    x0 = L**(-1.0)
    x1 = A*E*x0
    x2 = (1/3)*L*k0a + x1
    x3 = (1/6)*L*k0a - x1
    x4 = E*I
    x5 = 12*x4/L**3
    x6 = (13/35)*L*k0b + x5
    x7 = L**4*k0b
    x8 = 1260*x4 + 11*x7
    x9 = L**(-2.0)
    x10 = (1/210)*x9
    x11 = x10*x8
    x12 = (9/70)*L*k0b - x5
    x13 = 2520*x4 - 13*x7
    x14 = (1/420)*x9
    x15 = x13*x14
    x16 = (1/105)*x0*(420*x4 + x7)
    x17 = -x13*x14
    x18 = (1/140)*x0*(280*x4 - x7)
    x19 = -x10*x8
    return numpy.array([[x2, 0, 0, x3, 0, 0], [0, x6, x11, 0, x12, x15], [0, x11, x16, 0, x17, x18], [x3, 0, 0, x2, 0, 0], [0, x12, x17, 0, x6, x19], [0, x15, x18, 0, x19, x16]])

def beam2d_gen_Ml(A, E, I, L, alpha, fa, fb, k0a, k0b, rho, theta):
    x0 = A*rho
    x1 = L*x0
    x2 = (1/3)*x1
    x3 = (1/6)*x1
    x4 = (13/35)*x1
    x5 = L**2*x0
    x6 = (11/210)*x5
    x7 = (9/70)*x1
    x8 = (13/420)*x5
    x9 = -x8
    x10 = L**3*x0
    x11 = (1/105)*x10
    x12 = -1/140*x10
    x13 = -x6
    return numpy.array([[x2, 0, 0, x3, 0, 0], [0, x4, x6, 0, x7, x9], [0, x6, x11, 0, x8, x12], [x3, 0, 0, x2, 0, 0], [0, x7, x8, 0, x4, x13], [0, x9, x12, 0, x13, x11]])

def beam2d_gen_rl(A, E, I, L, alpha, fa, fb, k0a, k0b, rho, theta):
    x0 = A*E*alpha*theta
    x1 = (1/2)*L
    x2 = fb*x1
    x3 = (1/12)*L**2*fb
    return numpy.array([[(1/2)*L*fa - x0], [x2], [x3], [fa*x1 + x0], [x2], [-x3]])

def beam2d_gen_Nl(A, E, I, L, alpha, fa, fb, k0a, k0b, rho, theta):
    return numpy.array([[0, 0, 0, 1, 0, 0], [0, 1, 0, 0, 0, 0], [0, 0, 0, 0, 1, 0]])

def beam2d_gen_Bl(A, E, I, L, alpha, fa, fb, k0a, k0b, rho, theta):
    x0 = L**(-1.0)
    x1 = 6/L**2
    x2 = -x1
    x3 = 4*x0
    x4 = 2*x0
    return numpy.array([[-x0, 0, 0, x0, 0, 0], [0, x2, -x3, 0, x1, -x4], [0, x1, x4, 0, x2, x3]])

def beam2d_gen_Dcs_mid(A, E, I, L, alpha, fa, fb, k0a, k0b, rho, theta):
    x0 = E*I
    return numpy.array([[A*E, 0, 0], [0, x0, 0], [0, 0, x0]])

