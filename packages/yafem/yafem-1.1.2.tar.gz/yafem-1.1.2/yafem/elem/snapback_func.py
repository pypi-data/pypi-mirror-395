import numpy

def snapback_r(W, A, E, L, a, _Dummy_34):
    [u1, u2] = _Dummy_34
    x0 = u1 - u2
    x1 = A*E
    return numpy.array([[W*x0*x1/L], [x1*(-L**2*W*x0 + 2*u2*(a**2 - 1.5*a*u2 + 0.5*u2**2))/L**3]])

def snapback_K(W, A, E, L, a, _Dummy_35):
    [u1, u2] = _Dummy_35
    x0 = A*E
    x1 = W*x0/L
    x2 = -x1
    return numpy.array([[x1, x2], [x2, x0*(L**2*W + 2*a**2 - 3.0*a*u2 + 1.0*u2**2 + 2*u2*(-1.5*a + 1.0*u2))/L**3]])

