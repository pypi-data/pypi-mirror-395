import numpy as np
from yafem.elem.core_elem import core_elem
from yafem.elem.beam3d_circ_func import *
from yafem.elem.beam3d_gen_func import *

class beam3d(core_elem):
    """
    my_nodes : nodes

    pars: dictionary:
        shape        : str,     element shape, 'circular' or 'generic' (default 'circular')

        # Parameters for circular shape
        D1           : float,   outer diameter at first node (default 20.0)
        D2           : float,   outer diameter at second node (default 20.0)
        H            : float,   wall thickness of pipe (default 2.0)

        # Parameters for generic shape
        A            : float,   cross-sectional area (default 200.0)
        Ixx          : float,   second area moment about x-axis (default 1000.0)
        Iyy          : float,   second area moment about y-axis (default 1000.0)
        Jv           : float,   torsional constant (default Ixx + Iyy)

        # Common parameters
        E            : float,   Young's modulus (default 210e3)
        G            : float,   shear modulus (default 81e3)
        k0a          : float,   axial Winkler stiffness (default 0.0)
        k0b          : float,   lateral Winkler stiffness (default 0.0)
        rho          : float,   density (default 7850/1e9)
        fa           : float,   axial distributed force (default 0.0)
        fby          : float,   lateral distributed force in y (default 0.0)
        fbz          : float,   lateral distributed force in z (default 0.0)
        alpha        : float,   thermal expansion coefficient (default 0.0)
        theta        : float,   thermal loading (default 0.0)
        nodal_labels : list[int], node labels (default [1,2])
        dofs_q       : array,   temperature-controlled DOFs (default empty array)
    """

    #%% class constructor
    def __init__(self, my_nodes, pars):

        # superclass constructor
        super().__init__(my_nodes,pars)

        self.linear_M = True
        self.linear_K = True
        self.linear_C = True

        # extract parameters and assign default values
        self.__extract_pars(pars)

        # set the number of dofs per node
        self.__element_dofs(6)

        # Coordinate transformation matrix calculation
        r = self.nodal_coords[1] - self.nodal_coords[0]
        r /= np.linalg.norm(r)
        
        # Determine a perpendicular vector s and orthogonalize
        s = np.array([0.0, 1.0, 0.0]) if r[2] != 0 else np.array([-r[1], r[0], 0.0])
        s -= np.dot(s, r) * r
        s /= np.linalg.norm(s)

        # Compute t as the orthogonal cross product
        t = np.cross(r, s)
        t /= np.linalg.norm(t)

        # Create transformation matrix
        self.T = np.array([r, s, t])
        
        self.G = np.zeros((12, 12))
        self.G[0:3, 0:3] = self.T
        self.G[3:6, 3:6] = self.T
        self.G[6:9, 6:9] = self.T
        self.G[9:12, 9:12] = self.T

        if self.shape == 'circular':

            # Variables
            variables = [self.D1, 
                         self.D2, 
                         self.E, 
                         self.G1, 
                         self.H, 
                         self.L, 
                         self.alpha, 
                         self.fa, 
                         self.fby, 
                         self.fbz, 
                         self.k0a, 
                         self.k0b, 
                         self.rho, 
                         self.theta]
            
            self.Kl  = beam3d_circ_Kl(*variables)
            self.Ml  = beam3d_circ_Ml(*variables)
            self.rl  = beam3d_circ_rl(*variables)
            self.Nl  = beam3d_circ_Nl(*variables)
            self.Bl  = beam3d_circ_Bl(*variables)

            # cross-section stiffness matrix
            self.D = beam3d_circ_Dcs_mid(*variables)

        else: # self.shape == 'generic':
            
            # Variables
            variables = [self.A, 
                         self.E, 
                         self.G1, 
                         self.Ixx, 
                         self.Iyy, 
                         self.Jv, 
                         self.L, 
                         self.alpha, 
                         self.fa, 
                         self.fby, 
                         self.fbz, 
                         self.k0a, 
                         self.k0b, 
                         self.rho, 
                         self.theta]
            
            self.Kl  = beam3d_gen_Kl(*variables)
            self.Ml  = beam3d_gen_Ml(*variables)
            self.rl  = beam3d_gen_rl(*variables)
            self.Nl  = beam3d_gen_Nl(*variables)
            self.Bl  = beam3d_gen_Bl(*variables)

            # cross-section stiffness matrix
            self.D = beam3d_gen_Dcs_mid(*variables)

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
        self.my_pars['elem'] = 'beam3d'

        self.shape    = pars.get("shape", 'circular') # Youngs modulus

        if self.shape == 'circular':
            self.D1   = pars.get("D1", 20.0) # Outer diameter of pipe in firste node
            self.D2   = pars.get("D2", 20.0) # Outer diameter of pipe in second node
            self.H    = pars.get("H", 2) # thickness of pipe in both ends

            # Cross section area and inertia as functions of element diameter
            self.A1 = np.pi * (self.D1/2)**2 - np.pi * ((self.D1/2)-self.H)**2
            self.A2 = np.pi * (self.D2/2)**2 - np.pi * ((self.D2/2)-self.H)**2
            self.I1 = np.pi/4 * (self.D1/2)**4 - np.pi/4 * ((self.D1/2)-self.H)**4
            self.I2 = np.pi/4 * (self.D2/2)**4 - np.pi/4 * ((self.D2/2)-self.H)**4
            self.J1 = 2*self.I1  # Polar moment of inertia
            self.J2 = 2*self.I2  # Polar moment of inertia
        
        else: # self.shape == 'generic':
            self.A    = pars.get("A", 200.0) # Cross-sectional areal
            self.Ixx  = pars.get("Ixx", 1000.0) # second area moment about xx
            self.Iyy  = pars.get("Iyy", 1000.0) # second area moment about yy
            self.Jv   = pars.get("Jv", self.Ixx + self.Iyy) # Torsional constant
 
        self.E     = pars.get("E", 210e3) # Youngs modulus
        self.G1    = pars.get("G", 81e3) # Shear modulus
        self.k0a   = pars.get("k0a", 0.0) # Axial Winkler stiffness
        self.k0b   = pars.get("k0b", 0.0) # Lateral Winkler stiffness
        self.rho   = pars.get("rho", 7850/1e9) # Density
        self.fa    = pars.get("fa", 0.0) # Axial element destributed force
        self.fby   = pars.get("fby", 0.0) # Lateral element destributed force in y-direction
        self.fbz   = pars.get("fbz", 0.0) # Lateral element destributed force in z-direction
        self.alpha = pars.get("alpha", 0.0) # coefficient of thermal expansion 
        self.theta = pars.get("theta", 0.0) # Thermal loading
        self.nodal_labels = pars.get("nodal_labels", [1, 2])
        
        # extract nodal coordinates
        self.nodal_coords = self.my_nodes.find_coords(self.nodal_labels)
        self.L = np.linalg.norm(self.nodal_coords[1] - self.nodal_coords[0])
    
        # temperature controlled dofs
        self.dofs_q = np.array(pars.get("dofs_q", []), dtype=np.int32).reshape(-1, 2) if "dofs_q" in pars else np.zeros((0, 2), dtype=np.int32)

    #    self.nu    = pars.get("nu", 0.3)
    #    self.J     = pars.get("J", 1.0)
    
    #%% Computing element dofs
    # def __element_dofs(self, dofs_per_node):

    #     self.dofs = np.empty([dofs_per_node*2,2],dtype=int)

    #     self.dofs[0:dofs_per_node,0] = self.nodal_labels[0] # Label of first node
    #     self.dofs[dofs_per_node:,0]  = self.nodal_labels[1] # Label of second node
    #     self.dofs[:,1] = np.tile(np.arange(0,dofs_per_node), 2) + 1 # Dofs of both nodes
    
    #     return self.dofs
    
    def __element_dofs(self, dofs_per_node):
        n_nodes = len(self.nodal_labels)
        self.dofs = np.empty((n_nodes * dofs_per_node, 2), dtype=int)
        self.dofs[:, 0] = np.repeat(self.nodal_labels, dofs_per_node)
        self.dofs[:, 1] = np.tile(np.arange(1, dofs_per_node + 1), n_nodes)

        return self.dofs

    #%% Plot 3d elements
    def plot(self, ax, x=None, y=None, z=None, color='k-'):
        if x is None: x = self.nodal_coords[:, 0]
        if y is None: y = self.nodal_coords[:, 1]
        if z is None: z = self.nodal_coords[:, 2]

        # Collect lines
        lines = [[[x[0], y[0], z[0]],[x[1], y[1], z[1]]]]

        return lines, None
    
    def dump_to_paraview(self):
        # here it goes the dump_to_paraview implementation for the beam3d element
        pass
