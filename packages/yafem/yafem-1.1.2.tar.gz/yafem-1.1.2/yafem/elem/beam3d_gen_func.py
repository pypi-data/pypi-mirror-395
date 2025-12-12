import numpy

def beam3d_gen_Kl(A, E, G, Ixx, Iyy, Jv, L, alpha, fa, fby, fbz, k0a, k0b, rho, theta):
    x0 = L**(-1.0)
    x1 = A*E*x0
    x2 = (1/3)*L*k0a + x1
    x3 = (1/6)*L*k0a - x1
    x4 = (13/35)*L*k0b
    x5 = E*Iyy
    x6 = 12/L**3
    x7 = x5*x6
    x8 = x4 + x7
    x9 = L**4*k0b
    x10 = 11*x9
    x11 = x10 + 1260*x5
    x12 = L**(-2.0)
    x13 = (1/210)*x12
    x14 = x11*x13
    x15 = -9/70*L*k0b
    x16 = -x15 - x7
    x17 = -13*x9
    x18 = x17 + 2520*x5
    x19 = (1/420)*x12
    x20 = x18*x19
    x21 = E*Ixx
    x22 = x21*x6
    x23 = x22 + x4
    x24 = x10 + 1260*x21
    x25 = -x13*x24
    x26 = -x15 - x22
    x27 = x17 + 2520*x21
    x28 = -x19*x27
    x29 = G*Jv*x0
    x30 = -x29
    x31 = (1/105)*x0
    x32 = x31*(420*x21 + x9)
    x33 = x19*x27
    x34 = -x9
    x35 = (1/140)*x0
    x36 = x35*(280*x21 + x34)
    x37 = x31*(420*x5 + x9)
    x38 = -x18*x19
    x39 = x35*(x34 + 280*x5)
    x40 = -x11*x13
    x41 = x13*x24
    return numpy.array([[x2, 0, 0, 0, 0, 0, x3, 0, 0, 0, 0, 0], [0, x8, 0, 0, 0, x14, 0, x16, 0, 0, 0, x20], [0, 0, x23, 0, x25, 0, 0, 0, x26, 0, x28, 0], [0, 0, 0, x29, 0, 0, 0, 0, 0, x30, 0, 0], [0, 0, x25, 0, x32, 0, 0, 0, x33, 0, x36, 0], [0, x14, 0, 0, 0, x37, 0, x38, 0, 0, 0, x39], [x3, 0, 0, 0, 0, 0, x2, 0, 0, 0, 0, 0], [0, x16, 0, 0, 0, x38, 0, x8, 0, 0, 0, x40], [0, 0, x26, 0, x33, 0, 0, 0, x23, 0, x41, 0], [0, 0, 0, x30, 0, 0, 0, 0, 0, x29, 0, 0], [0, 0, x28, 0, x36, 0, 0, 0, x41, 0, x32, 0], [0, x20, 0, 0, 0, x39, 0, x40, 0, 0, 0, x37]])

def beam3d_gen_Ml(A, E, G, Ixx, Iyy, Jv, L, alpha, fa, fby, fbz, k0a, k0b, rho, theta):
    x0 = L*rho
    x1 = A*x0
    x2 = (1/3)*x1
    x3 = (1/6)*x1
    x4 = A*L**2
    x5 = 13*x4
    x6 = rho/L
    x7 = (1/35)*x6
    x8 = x7*(42*Iyy + x5)
    x9 = 11*x4
    x10 = (1/210)*rho
    x11 = x10*(21*Iyy + x9)
    x12 = 3*x4
    x13 = (3/70)*x6
    x14 = x13*(-28*Iyy + x12)
    x15 = -42*Iyy + x5
    x16 = (1/420)*rho
    x17 = -x15*x16
    x18 = 42*Ixx
    x19 = x7*(x18 + x5)
    x20 = x10*(21*Ixx + x9)
    x21 = -x20
    x22 = x13*(-28*Ixx + x12)
    x23 = -x18 + x5
    x24 = x16*x23
    x25 = Jv*x0
    x26 = (1/3)*x25
    x27 = (1/6)*x25
    x28 = 14*Ixx
    x29 = (1/105)*x0
    x30 = x29*(x28 + x4)
    x31 = -x16*x23
    x32 = L*x16
    x33 = -x32*(x12 + x28)
    x34 = 14*Iyy
    x35 = x29*(x34 + x4)
    x36 = x15*x16
    x37 = -x32*(x12 + x34)
    x38 = -x11
    return numpy.array([[x2, 0, 0, 0, 0, 0, x3, 0, 0, 0, 0, 0], [0, x8, 0, 0, 0, x11, 0, x14, 0, 0, 0, x17], [0, 0, x19, 0, x21, 0, 0, 0, x22, 0, x24, 0], [0, 0, 0, x26, 0, 0, 0, 0, 0, x27, 0, 0], [0, 0, x21, 0, x30, 0, 0, 0, x31, 0, x33, 0], [0, x11, 0, 0, 0, x35, 0, x36, 0, 0, 0, x37], [x3, 0, 0, 0, 0, 0, x2, 0, 0, 0, 0, 0], [0, x14, 0, 0, 0, x36, 0, x8, 0, 0, 0, x38], [0, 0, x22, 0, x31, 0, 0, 0, x19, 0, x20, 0], [0, 0, 0, x27, 0, 0, 0, 0, 0, x26, 0, 0], [0, 0, x24, 0, x33, 0, 0, 0, x20, 0, x30, 0], [0, x17, 0, 0, 0, x37, 0, x38, 0, 0, 0, x35]])

def beam3d_gen_rl(A, E, G, Ixx, Iyy, Jv, L, alpha, fa, fby, fbz, k0a, k0b, rho, theta):
    x0 = A*E*alpha*theta
    x1 = (1/2)*L
    x2 = fby*x1
    x3 = fbz*x1
    x4 = (1/12)*L**2
    x5 = fbz*x4
    x6 = fby*x4
    return numpy.array([[(1/2)*L*fa - x0], [x2], [x3], [0], [-x5], [x6], [fa*x1 + x0], [x2], [x3], [0], [x5], [-x6]])

def beam3d_gen_Nl(A, E, G, Ixx, Iyy, Jv, L, alpha, fa, fby, fbz, k0a, k0b, rho, theta):
    x0 = (1/8)*L
    x1 = -x0
    return numpy.array([[1/2, 0, 0, 0, 0, 0, 1/2, 0, 0, 0, 0, 0], [0, 1/2, 0, 0, 0, x0, 0, 1/2, 0, 0, 0, x1], [0, 0, 1/2, 0, x1, 0, 0, 0, 1/2, 0, x0, 0]])

def beam3d_gen_Bl(A, E, G, Ixx, Iyy, Jv, L, alpha, fa, fby, fbz, k0a, k0b, rho, theta):
    x0 = L**(-1.0)
    x1 = -x0
    return numpy.array([[x1, 0, 0, 0, 0, 0, x0, 0, 0, 0, 0, 0], [0, 0, 0, 0, x0, x1, 0, 0, 0, 0, x1, x0], [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]])

def beam3d_gen_Dcs_mid(A, E, G, Ixx, Iyy, Jv, L, alpha, fa, fby, fbz, k0a, k0b, rho, theta):
    return numpy.array([[A*E, 0, 0], [0, E*Iyy, 0], [0, 0, E*Ixx]])

