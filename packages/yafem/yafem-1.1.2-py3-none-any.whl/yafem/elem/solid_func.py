import numpy

def solid_phi(s, t):
    x0 = s - 1
    x1 = (1/4)*t - 1/4
    x2 = s + 1
    x3 = (1/4)*t + 1/4
    return [x0*x1, -x1*x2, x2*x3, -x0*x3]

def solid_N(s, t):
    x0 = s - 1
    x1 = (1/4)*t - 1/4
    x2 = x0*x1
    x3 = s + 1
    x4 = -x1*x3
    x5 = (1/4)*t + 1/4
    x6 = x3*x5
    x7 = -x0*x5
    return numpy.array([[x2, 0, x4, 0, x6, 0, x7, 0], [0, x2, 0, x4, 0, x6, 0, x7]])

def solid_B(s, t):
    x0 = (1/4)*t
    x1 = x0 - 1/4
    x2 = -x1
    x3 = x0 + 1/4
    x4 = -x3
    x5 = (1/4)*s
    x6 = x5 - 1/4
    x7 = x5 + 1/4
    x8 = -x7
    x9 = -x6
    return numpy.array([[x1, 0, x2, 0, x3, 0, x4, 0], [x6, 0, x8, 0, x7, 0, x9, 0], [0, x1, 0, x2, 0, x3, 0, x4], [0, x6, 0, x8, 0, x7, 0, x9]])

def solid_Dax(E, nu):
    x0 = nu - 1
    x1 = E/(2*nu**2 + x0)
    x2 = x0*x1
    x3 = -nu*x1
    return numpy.array([[x2, x3, x3, 0], [x3, x2, x3, 0], [x3, x3, x2, 0], [0, 0, 0, (1/2)*E/(nu + 1)]])

def solid_Dpe(E, nu):
    x0 = nu - 1
    x1 = E/(2*nu**2 + x0)
    x2 = x0*x1
    x3 = -nu*x1
    return numpy.array([[x2, x3, 0], [x3, x2, 0], [0, 0, (1/2)*E/(nu + 1)]])

def solid_Dps(E, nu):
    x0 = E/(nu**2 - 1)
    x1 = -x0
    x2 = -nu*x0
    return numpy.array([[x1, x2, 0], [x2, x1, 0], [0, 0, (1/2)*E/(nu + 1)]])

def solid_Jac(s, t, xe):
    x0 = xe[:, :1].T
    x1 = (1/4)*t
    x2 = x1 - 1/4
    x3 = -x2
    x4 = x1 + 1/4
    x5 = -x4
    x6 = xe[:, 1:].T
    x7 = (1/4)*s
    x8 = x7 - 1/4
    x9 = x7 + 1/4
    x10 = -x9
    x11 = -x8
    return numpy.array([[(x0).dot(numpy.array([[x2], [x3], [x4], [x5]])), (x6).dot(numpy.array([[x2], [x3], [x4], [x5]]))], [(x0).dot(numpy.array([[x8], [x10], [x9], [x11]])), (x6).dot(numpy.array([[x8], [x10], [x9], [x11]]))]])

