import numpy as np
import jax
import jax.numpy as jnp
from jax import jacrev, jit
jax.config.update("jax_enable_x64", True)
from yafem.elem.core_elem import core_elem

#%% element_MCK class
class beam2d_cr(core_elem):
    """
    my_nodes : nodes
        Node container providing coordinates and connectivity.

    pars : dictionary
        E            : float,   Young's modulus (default 210e3)
        I            : float,   Second moment of area (default 1000)
        A            : float,   Cross-sectional area (default 200)
        rho          : float,   Material density (default 7850)
        nodal_labels : list[int], Node connectivity (default [1, 2])
    """

    # class constructor
    def __init__(self, my_nodes, pars):

        # superclass constructor
        super().__init__(my_nodes,pars)

        self.linear_M = False
        self.linear_K = False
        self.linear_C = False

        # extract parameters and assign default values
        self.__extract_pars(pars)

        # element dofs
        self.dofs = np.array([[self.nodal_labels[0],1],   
                              [self.nodal_labels[0],2],   
                              [self.nodal_labels[0],3],   
                              [self.nodal_labels[1],1],
                              [self.nodal_labels[1],2],
                              [self.nodal_labels[1],3]],dtype=np.int32)
        
        # jax variables
        # u = jnp.array()
        # v = jnp.array()
        # a = jnp.array()
        # q = jnp.array()
        # t = jnp.array()
        # i = jnp.array()

        # nodal coordinates
        x1 = self.nodal_coords[0,0]
        x2 = self.nodal_coords[1,0]
        z1 = self.nodal_coords[0,1]
        z2 = self.nodal_coords[1,1]

        #%% fixed numbers

        # inition length
        l0 = ((x2-x1)**2 + (z2-z1)**2)**0.5 # E6 #### fixed

        # cosine parameters
        c0 = (x2-x1)/l0 #E8 #### fixed
        s0 = (z2-z1)/l0 #E9 #### fixed

        beta0 = jnp.atan2(s0,c0) #### fixed

        # axial stiffness
        ka = self.E*self.A/l0 #### fixed

        # bending stiffness
        kb = 6*self.E*self.I/l0**2 #### fixed

        # local stiffness matrix
        Kl = jnp.array([[ka ,  0  , 0 ],
                        [0  ,  kb ,-kb],
                        [0  , -kb , kb]]) #### fixed
        
        Ml2 = self.rho*self.I/(30*l0) * jnp.array([[0 , 0    , 0       ,0  ,  0    , 0       ] ,
                                                   [0 , 36   , 3*l0    ,0  , -36   , 3*l0    ] ,
                                                   [0 , 3*l0 , 4*l0**2 ,0  , -3*l0 ,-l0**2   ] ,
                                                   [0 , 0    , 0       ,0  ,  0    , 0       ] ,
                                                   [0 ,-36   ,-3*l0    ,0  ,  36   ,-3*l0    ] ,
                                                   [0 , 3*l0 ,-l0**2   ,0  , -3*l0 , 4*l0**2 ]]) # E45B #### fixed

        I1 = jnp.array([[ 0 ,1 ,0, 0 ,0 ,0],
                        [-1 ,0 ,0, 0 ,0 ,0],
                        [ 0 ,0 ,0, 0 ,0 ,0],
                        [ 0 ,0 ,0, 0 ,1 ,0],
                        [ 0 ,0 ,0,-1 ,0 ,0],
                        [ 0 ,0 ,0, 0 ,0 ,0]]) #E53 #### fixed
        
        Mt1bl = self.rho*l0*self.A/60*jnp.array([[ 0 , 3 , 0 , 0 ,-3 , 0],
                                                 [ 3 , 0 , 0 , 2 , 0 , 0],
                                                 [ 0 , 0 , 0 , 0 , 0 , 0],
                                                 [ 0 , 2 , 0 , 0 ,-2 , 0],
                                                 [-3 , 0 , 0 ,-2 , 0 , 0],
                                                 [ 0 , 0 , 0 , 0 , 0 , 0]]) #E55 #### fixed

        Mt2bl = self.rho*l0*self.A/60*jnp.array([[ 0 ,-2 , 0 , 0 , 2 , 0],
                                                 [-2 , 0 , 0 ,-3 , 0 , 0],
                                                 [ 0 , 0 , 0 , 0 , 0 , 0],
                                                 [ 0 ,-3 , 0 , 0 , 3 , 0],
                                                 [ 2 , 0 , 0 , 3 , 0 , 0],
                                                 [ 0 , 0 , 0 , 0 , 0 , 0]]) #56 #### fixed

        self.cr_params = (
            x1,
            x2,
            z1,
            z2,
            l0,
            beta0,
            self.E,
            self.A,
            self.I,
            self.rho,
            Kl,
            Ml2,
            I1,
            Mt1bl,
            Mt2bl
            )

        u = np.zeros_like(self.nodal_coords.flatten())
        v = np.zeros_like(u)
        a = v.copy()

        self.f = self.compute_f(u,v,a)
        self.M = self.compute_M(u,v,a)
        self.C = self.compute_C(u,v,a)
        self.K = self.compute_K(u,v,a)


        #%% updated numbers

    def __compute_f_jax(u, v, a, cr_params):
        (x1, x2, z1, z2, l0, beta0, E, A, I, rho, Kl, Ml2, I1, Mt1bl, Mt2bl) = cr_params

        # Unpack inputs
        u1, w1, t1, u2, w2, t2 = u
        u1d, w1d, t1d, u2d, w2d, t2d = v
        u1dd, w1dd, t1dd, u2dd, w2dd, t2dd = a
        
         # current length
        ln = (((x2+u2)-(x1+u1))**2 + ((z2+w2)-(z1+w1))**2)**0.5 #E7
        
        # cosine parameters
        c = (x2+u2-x1-u1)/ln #E8
        s = (z2+w2-z1-w1)/ln #E9

        beta  = jnp.atan2(s,c)

        z = jnp.array([ s,-c, 0,-s, c, 0])

        # local displacements (scalar)
        ub  = ln-l0
        t1b = t1 - beta - beta0
        t2b = t2 - beta - beta0

        ql = jnp.array([ub,t1b,t2b])

        # deformation interpolation matrix
        b1 = jnp.array([-c   ,-s   , 0,    c,    s, 0]) #E12
        b2 = jnp.array([-s/ln, c/ln, 1, s/ln,-c/ln, 0]) #E12
        b3 = jnp.array([-s/ln, c/ln, 0, s/ln,-c/ln, 1]) #E12

        B = jnp.array([b1,b2,b3]) #E12
        
        # local restoring force vector
        fl = Kl @ ql

        # global restoring force vector
        rg = B.T @ fl # E14

        T = jnp.array([[ c,s,0, 0,0,0],
                       [-s,c,0, 0,0,0],
                       [ 0,0,1, 0,0,0],
                       [ 0,0,0, c,s,0],
                       [ 0,0,0,-s,c,0],
                       [ 0,0,0, 0,0,1]])
        
        m1 = 21*t1b-14*t2b
        m2 = 14*t1b-21*t2b

        Ml1 = rho*A*l0/420 * jnp.array([[ 140 ,  m1    , 0       , 70  ,-m1    , 0       ] ,
                                        [ m1  ,  156   , 22*l0   , m2  , 54    ,-13*l0   ] ,
                                        [ 0   ,  22*l0 , 4*l0**2 , 0   , 13*l0 ,-3*l0**2 ] ,
                                        [ 70  ,  m2    , 0       , 140 ,-m2    , 0       ] ,
                                        [-m1  ,  54    , 13*l0   , -m2 , 156   ,-22*l0   ] ,
                                        [ 0   , -13*l0 ,-3*l0**2 , 0   , -22*l0, 4*l0**2 ]]) #E45A 

        Ml = Ml1 + Ml2 # E45
        M = T.T @ Ml @ T # E43
        
        Mbeta = T.T @ (I1.T @ Ml + Ml @ I1) @ T # E54

        Mt1b = T.T @ Mt1bl @ T #E55
        Mt2b = T.T @ Mt2bl @ T #E56

        Md = Mbeta * (z @ v)/ln + Mt1b*(b2 @ v) + Mt2b*(b3 @ v) #E49

        rk = M @ a + Md @ v - 1/2 * (v @ Mbeta @ v) * z/ln - 1/2 * (v @ Mt1b @ v) * b2 - 1/2 * (v @ Mt2b @ v) * b3 #E51

        r = rg + rk

        return r

    # def compute_M(self,u,v,q,t,i): # Check the inputs here
    #     pass

    # def compute_C(self,u,v,q,t,i): # Check the inputs here
    #     pass

    # def compute_K(self,u,v,q,t,i): # Check the inputs here
    #     pass

    def compute_f(self,u,v,a,q=None,t=None,i=None): # Check the inputs here
        f_jit = jit(beam2d_cr.__compute_f_jax)
        f = f_jit(u,v,a,self.cr_params)
        return f

    def compute_M(self,u,v,a,q=None,t=None,i=None): # Check the inputs here
        M_jit = jit(jacrev(beam2d_cr.__compute_f_jax,argnums=2))
        M = M_jit(u,v,a,self.cr_params)
        return M

    def compute_C(self,u,v,a,q=None,t=None,i=None): # Check the inputs here
        C_jit = jit(jacrev(beam2d_cr.__compute_f_jax,argnums=1))
        C = C_jit(u,v,a,self.cr_params)
        return C

    def compute_K(self,u,v,a,q=None,t=None,i=None): # Check the inputs here
        K_jit = jit(jacrev(beam2d_cr.__compute_f_jax,argnums=0))
        K = K_jit(u,v,a,self.cr_params)
        return K

    #%% extract parameters and assign default values
    def __extract_pars(self,pars):

        self.E   = pars.get('E', 210e3)
        self.I   = pars.get('I', 1000)
        self.A   = pars.get('A', 200)
        self.rho = pars.get('rho', 7850)

        # this is the element class used in packing/unpacking
        self.my_pars['elem'] = 'beam2d_cr'


        #%% plot the element       
    def plot(self, ax, x=None, y=None, z=None, color='k-'):
        if x is None: x = self.nodal_coords[:, 0]
        if y is None: y = self.nodal_coords[:, 1]
        if z is None: z = self.nodal_coords[:, 2]

        # Collect lines
        lines = [[[x[0], y[0], 0],[x[1], y[1], 0]]]

        return lines, None

