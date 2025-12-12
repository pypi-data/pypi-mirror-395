import numpy as np
from yafem.elem.core_elem import core_elem
from yafem.elem.beam2d_gen_func import *

#%% element_beam2d class
class beam2d(core_elem):
    """
    my_nodes : nodes

    pars: dictionary:
        A           : float,     cross-sectional area (default 200.0)
        I           : float,     second area moment (default 1000.0)
        E           : float,     Young's modulus (default 210e3)
        G           : float,     shear modulus (default 81e3)
        k0a         : float,     axial Winkler stiffness (default 0.0)
        k0b         : float,     lateral Winkler stiffness (default 0.0)
        rho         : float,     density (default 7850/1e9)
        fa          : float,     axial distributed force (default 0.0)
        fb          : float,     lateral distributed force (default 0.0)
        alpha       : float,     thermal expansion coefficient (default 0.0)
        theta       : float,     thermal loading (default 0.0)
        nodal_labels: list[int], node labels (default [1,2])
        dofs_q      : array,     temperature-controlled DOFs (default empty array)
    """

    # class constructor
    def __init__(self, my_nodes, pars):

        # superclass constructor
        super().__init__(my_nodes,pars)

        self.linear_M = True
        self.linear_K = True
        self.linear_C = True

        # extract parameters and assign default values
        self.__extract_pars(pars)

        # element dofs
        self.dofs = np.array([[self.nodal_labels[0],1],   
                              [self.nodal_labels[0],2],   
                              [self.nodal_labels[0],3],   
                              [self.nodal_labels[1],1],
                              [self.nodal_labels[1],2],
                              [self.nodal_labels[1],3]],dtype=np.int32)
        
        # # rotation matrix in the xy plane
        r = (self.nodal_coords[1,:2] - self.nodal_coords[0,:2])/self.L
        s = np.array([-r[1],r[0]])

        # Local reference system
        self.T = np.array([r, s])

        # global to local transformation matrix in the xy plane
        self.G = np.zeros((6, 6))
        self.G[0:2, 0:2] = self.T
        self.G[2:3, 2:3] = 1
        self.G[3:5, 3:5] = self.T
        self.G[5:6, 5:6] = 1

        # Variables
        variables = [self.A, 
                     self.E, 
                     self.I, 
                     self.L, 
                     self.alpha, 
                     self.fa, 
                     self.fb, 
                     self.k0a, 
                     self.k0b, 
                     self.rho, 
                     self.theta]

        self.Kl  = beam2d_gen_Kl(*variables)
        self.Ml  = beam2d_gen_Ml(*variables)
        self.rl  = beam2d_gen_rl(*variables)
        self.Nl  = beam2d_gen_Nl(*variables)
        self.Bl  = beam2d_gen_Bl(*variables)

        # cross-section stiffness matrix
        self.D = beam2d_gen_Dcs_mid(*variables)

        #%% Global reference

        # Stiffness matrix in global coordinate system
        self.K = self.G.T @ self.Kl @ self.G
        self.M = self.G.T @ self.Ml @ self.G

        # damping matrix in global coordinates
        self.C = np.zeros_like(self.K)

        # strain interpolation matrix in global coordinates
        self.B = self.Bl @ self.G

        # displacement interpolation matrix in global coordinates
        self.N = self.Nl @ self.G

        # local to global coordinate transformation
        self.r = self.G.T @ self.rl     
 
        #%% extract parameters
    def __extract_pars(self, pars):
        
        # this is the element class used in packing/unpacking
        self.my_pars['elem'] = 'beam2d'

        self.A     = pars.get("A", 200.0) # Cross-sectional areal
        self.I     = pars.get("I", 1000.0) # second area moment
        self.E     = pars.get("E", 210e3) # Youngs modulus
        self.G1    = pars.get("G", 81e3) # Shear modulus
        self.k0a   = pars.get("k0a", 0.0) # Axial Winkler stiffness
        self.k0b   = pars.get("k0b", 0.0) # Lateral Winkler stiffness
        self.rho   = pars.get("rho", 7850/1e9) # Density
        self.fa    = pars.get("fa", 0.0) # Axial element destributed force
        self.fb    = pars.get("fb", 0.0) # Lateral element destributed force in y-direction
        self.alpha = pars.get("alpha", 0.0) # coefficient of thermal expansion 
        self.theta = pars.get("theta", 0.0) # Thermal loading
        self.nodal_labels = pars.get("nodal_labels", [1, 2])
        
        # extract nodal coordinates
        self.nodal_coords = self.my_nodes.find_coords(self.nodal_labels)
        self.L = np.linalg.norm(self.nodal_coords[1] - self.nodal_coords[0])
    
        # temperature controlled dofs
        self.dofs_q = np.array(pars.get("dofs_q", []), dtype=np.int32).reshape(-1, 2) if "dofs_q" in pars else np.zeros((0, 2), dtype=np.int32)


    #%% plot the element       
    def plot(self, ax, x=None, y=None, z=None, color='k-'):
        if x is None: x = self.nodal_coords[:, 0]
        if y is None: y = self.nodal_coords[:, 1]
        if z is None: z = self.nodal_coords[:, 2]

        # Collect lines
        lines = [[[x[0], y[0], 0],[x[1], y[1], 0]]]

        return lines, None
