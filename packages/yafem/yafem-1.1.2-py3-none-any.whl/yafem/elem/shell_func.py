import numpy

def plate_N_lmd(s, t):
    x0 = s - 1.0
    x1 = 0.25*t - 0.25
    x2 = x0*x1
    x3 = s + 1.0
    x4 = -x1*x3
    x5 = 0.25*t + 0.25
    x6 = x3*x5
    x7 = -x0*x5
    return numpy.array([[x2, 0, 0, x4, 0, 0, x6, 0, 0, x7, 0, 0], [0, x2, 0, 0, x4, 0, 0, x6, 0, 0, x7, 0], [0, 0, x2, 0, 0, x4, 0, 0, x6, 0, 0, x7]])

def solid_N_lmd(s, t):
    x0 = s - 1.0
    x1 = 0.25*t - 0.25
    x2 = x0*x1
    x3 = s + 1.0
    x4 = -x1*x3
    x5 = 0.25*t + 0.25
    x6 = x3*x5
    x7 = -x0*x5
    return numpy.array([[x2, 0, x4, 0, x6, 0, x7, 0], [0, x2, 0, x4, 0, x6, 0, x7]])

def solid_B_lmd(s, t):
    x0 = 0.25*t
    x1 = x0 - 0.25
    x2 = -x1
    x3 = x0 + 0.25
    x4 = -x3
    x5 = 0.25*s
    x6 = x5 - 0.25
    x7 = x5 + 0.25
    x8 = -x7
    x9 = -x6
    return numpy.array([[x1, 0, x2, 0, x3, 0, x4, 0], [x6, 0, x8, 0, x7, 0, x9, 0], [0, x1, 0, x2, 0, x3, 0, x4], [0, x6, 0, x8, 0, x7, 0, x9]])

def plate_Bb_lmd(s, t):
    x0 = 0.25*t
    x1 = x0 - 0.25
    x2 = -x1
    x3 = x0 + 0.25
    x4 = -x3
    x5 = 0.25*s
    x6 = x5 - 0.25
    x7 = x5 + 0.25
    x8 = -x7
    x9 = -x6
    return numpy.array([[0, x1, 0, 0, x2, 0, 0, x3, 0, 0, x4, 0], [0, x6, 0, 0, x8, 0, 0, x7, 0, 0, x9, 0], [0, 0, x1, 0, 0, x2, 0, 0, x3, 0, 0, x4], [0, 0, x6, 0, 0, x8, 0, 0, x7, 0, 0, x9]])

def plate_Bs1_lmd(s, t):
    x0 = s - 1.0
    x1 = 0.25*t - 0.25
    x2 = -x0*x1
    x3 = s + 1.0
    x4 = x1*x3
    x5 = 0.25*t + 0.25
    x6 = -x3*x5
    x7 = x0*x5
    return numpy.array([[0, x2, 0, 0, x4, 0, 0, x6, 0, 0, x7, 0], [0, 0, x2, 0, 0, x4, 0, 0, x6, 0, 0, x7]])

def plate_Bs2_lmd(s, t):
    x0 = 0.25*t
    x1 = x0 - 0.25
    x2 = x0 + 0.25
    x3 = 0.25*s
    x4 = x3 - 0.25
    x5 = x3 + 0.25
    return numpy.array([[x1, 0, 0, -x1, 0, 0, x2, 0, 0, -x2, 0, 0], [x4, 0, 0, -x5, 0, 0, x5, 0, 0, -x4, 0, 0]])

def plate_Db_lmd(E, nu):
    x0 = nu - 1
    x1 = E/(2*nu**2 + x0)
    x2 = x0*x1
    x3 = -nu*x1
    return numpy.array([[x2, x3, 0], [x3, x2, 0], [0, 0, (1/2)*E/(nu + 1)]])

def plate_Ds_lmd(E, nu):
    x0 = (1/2)*E/(nu + 1)
    return numpy.array([[x0, 0], [0, x0]])

def solid_Dps_lmd(E, nu):
    x0 = E/(nu**2 - 1)
    x1 = -x0
    x2 = -nu*x0
    return numpy.array([[x1, x2, 0], [x2, x1, 0], [0, 0, (1/2)*E/(nu + 1)]])

def solid_Dpe_lmd(E, nu):
    x0 = nu - 1
    x1 = E/(2*nu**2 + x0)
    x2 = x0*x1
    x3 = -nu*x1
    return numpy.array([[x2, x3, 0], [x3, x2, 0], [0, 0, (1/2)*E/(nu + 1)]])

def phi_lmd(s, t):
    x0 = s - 1.0
    x1 = 0.25*t - 0.25
    x2 = s + 1.0
    x3 = 0.25*t + 0.25
    return numpy.array([[x0*x1], [-x1*x2], [x2*x3], [-x0*x3]])

def Jac_lmd(_Dummy_34, xe):
    [s, t] = _Dummy_34
    x0 = xe[:, :1].T
    x1 = 0.25*t
    x2 = x1 - 0.25
    x3 = -x2
    x4 = x1 + 0.25
    x5 = -x4
    x6 = xe[:, 1:].T
    x7 = 0.25*s
    x8 = x7 - 0.25
    x9 = x7 + 0.25
    x10 = -x9
    x11 = -x8
    return numpy.array([[(x0).dot(numpy.array([[x2], [x3], [x4], [x5]])), (x6).dot(numpy.array([[x2], [x3], [x4], [x5]]))], [(x0).dot(numpy.array([[x8], [x10], [x9], [x11]])), (x6).dot(numpy.array([[x8], [x10], [x9], [x11]]))]])

def GL1_lmd():
    return (numpy.array([[0, 0]]), numpy.array([[4]]),)

def GL2_lmd():
    return (numpy.array([[-0.577350269189626, -0.577350269189626], [-0.577350269189626, 0.577350269189626], [0.577350269189626, -0.577350269189626], [0.577350269189626, 0.577350269189626]]), numpy.array([[1], [1], [1], [1]]),)

def drill_K_lmd(_Dummy_35, h, E, alpha):
    [x1, y1, x2, y2, x3, y3, x4, y4] = _Dummy_35
    x0 = x1*y3
    x5 = x3*y1
    x6 = -x1*y4 + x4*y1
    x7 = x3*y4 - x4*y3
    x8 = numpy.abs(x0 - x5 + x6 + x7)
    x9 = x1*y2 - x2*y1
    x10 = x2*y3 - x3*y2
    x11 = numpy.abs(-x0 + x10 + x5 + x9)
    x12 = x2*y4
    x13 = x4*y2
    x14 = numpy.abs(x12 - x13 + x6 + x9)
    x15 = x11 + x14
    x16 = E*alpha*h
    x17 = 0.25*x16
    x18 = 0.125*x16
    x19 = -x15*x18
    x20 = x11 + x8
    x21 = -x18*x20
    x22 = x14 + x8
    x23 = -x18*x22
    x24 = numpy.abs(x10 - x12 + x13 + x7)
    x25 = -x18*(x11 + x24)
    x26 = x18*(-x14 - x24)
    x27 = x18*(-x24 - x8)
    return numpy.array([[x17*(x15 + x8), x19, x21, x23], [x19, x17*(x15 + x24), x25, x26], [x21, x25, x17*(x20 + x24), x27], [x23, x26, x27, x17*(x22 + x24)]])

def plate_delta_lmd(_Dummy_36, h, epsilon):
    [x1, y1, x2, y2, x3, y3, x4, y4] = _Dummy_36
    return 2.0*epsilon*h**2/numpy.abs(x1*y2 - x1*y4 - x2*y1 + x2*y3 - x3*y2 + x3*y4 + x4*y1 - x4*y3)

