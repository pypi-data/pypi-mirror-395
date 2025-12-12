import numpy as np
from scipy.sparse import coo_array
from scipy.linalg import block_diag
from yafem.elem.core_elem import core_elem
from yafem.elem.shell_func import *

#TODO look into flattening correcting it

class shell4(core_elem):
    """
    my_nodes : nodes

    pars: dictionary:
        E           : float,   Young's modulus (default 210e9)
        nu          : float,   Poisson's ratio (default 0.3)
        rho         : float,   density (default 7850)
        h           : float,   shell thickness (default 5e-3)
        I           : float,   moment of inertia (default h**3/12)
        alpha       : float,   thermal expansion coefficient (default 0.3)
        epsilon     : float,   hourglass control parameter (default 0.01)
        bx          : float,   distributed load in x (default 0.0)
        by          : float,   distributed load in y (default 0.0)
        bz          : float,   distributed load in z (default 0.0)
        type        : str,     analysis type: 'ps', 'pe', or 'ax' (default 'ps')
        nodal_labels: list[int], node labels (default [1,2,3,4])
        dofs_q      : array,   temperature-controlled DOFs (default empty array)
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

        # element dofs
        self.dofs = self.__element_dofs(6)
        
        # Calculate the mean of nodal coordinates
        r0 = np.mean(self.nodal_coords, axis=0)

        r = (self.nodal_coords[1, :] + self.nodal_coords[2, :]) * 0.5 - r0
        r /= np.linalg.norm(r)

        s = (self.nodal_coords[2, :] + self.nodal_coords[3, :]) * 0.5 - r0
        s -= np.dot(s, r)
        s /= np.linalg.norm(s)

        t = np.cross(r, s)

        self.xe = self.nodal_coords
        self.xe_plot = self.xe

        self.xep = np.dot(self.xe - r0, np.column_stack((r, s)))
        self.xe = self.xep

        # Local reference system
        T = np.array([r, s, t])

        # Transformation matrix 
        G = np.zeros((24, 24))
        G[0:3, 0:3]     = T
        G[3:6, 3:6]     = T
        G[6:9, 6:9]     = T
        G[9:12, 9:12]   = T
        G[12:15, 12:15] = T
        G[15:18, 15:18] = T
        G[18:21, 18:21] = T
        G[21:24, 21:24] = T

        #%% Gauss-Legendre quadrature
        self.gpr, self.gwr = GL1_lmd() # reduced quadrature
        self.gpf, self.gwf = GL2_lmd() # full quadrature

        # collocation matricies
        Zs = self.__fun_mapping(np.array([1, 2]))     # solid
        Zp = self.__fun_mapping(np.array([3, -5, 4])) # plate
        Zd = self.__fun_mapping(np.array([6]))        # drilling

        self.Kl  = np.zeros((24, 24))
        self.Ml  = np.copy(self.Kl)

        self.fcl = np.zeros((24, 1))
        self.ftg = np.copy(self.fcl)
        d        = np.copy(self.fcl)

        Gd = G.dot(d)
        self.ds = Zs.dot(Gd)
        self.dp = Zp.dot(Gd)
        self.dd = Zd.dot(Gd)

        # compute solid, plate and drilling
        Ks, Kp, Kd, \
        Ms, Mp, Md, \
        fcs, fcp, fcd = self.__compute_shell()

        Zs_T = Zs.T
        Zp_T = Zp.T
        Zd_T = Zd.T
        G_T  = G.T

        # Local stiffness matrix of the shell element
        self.Kl += Zs_T @ Ks @ Zs # solid
        self.Kl += Zp_T @ Kp @ Zp # plate
        self.Kl += Zd_T @ Kd @ Zd # drilling

        # Local mass matrix of the shell element
        self.Ml += Zs_T @ Ms @ Zs # solid
        self.Ml += Zp_T @ Mp @ Zp # plate
        self.Ml += Zd_T @ Md @ Zd # drilling

        # Local consistent nodal load vector
        self.fcl += Zs_T @ fcs # solid
        self.fcl += Zp_T @ fcp # plate
        self.fcl += Zd_T @ fcd # drilling

        # Thermo mechanical load vector
        # self.ftl += Zs_T @ ftgs # solid
        # self.ftl += Zp_T @ ftgp # plate
        # self.ftl += Zd_T @ ftgd # drilling

        # Element matrices and vectors in global reference system (model)
        self.Kg  = G_T @ self.Kl @ G
        self.Mg  = G_T @ self.Ml @ G
        self.fcg = G_T @ self.fcl
        # self.ftg = G_T @ self.ftl
        self.ftg = np.zeros_like(self.fcg)

        self.K = self.Kg
        self.M = self.Mg
        self.C = np.zeros(self.K.shape)

    def __element_dofs(self, dofs_per_node): 
        self.dofs = np.empty([dofs_per_node*4,2],dtype=int)

        self.dofs[0:dofs_per_node,0]                  = self.nodal_labels[0] # Label of first node
        self.dofs[dofs_per_node*1:dofs_per_node*2,0]  = self.nodal_labels[1] # Label of second node
        self.dofs[dofs_per_node*2:dofs_per_node*3,0]  = self.nodal_labels[2] # Label of third node
        self.dofs[dofs_per_node*3:dofs_per_node*4,0]  = self.nodal_labels[3] # Label of fourth node
        self.dofs[:,1] = np.tile(np.arange(0,dofs_per_node), 4) + 1 # Dofs of all nodes
    
        return self.dofs
       
    #%% Mapping
    def __fun_mapping(self, ind):
        Z = np.zeros((len(ind), 6))

        Z[range(len(ind)), abs(ind) - 1] = np.sign(ind)
        Z = block_diag(Z,Z,Z,Z)
                      
        return coo_array(Z,dtype=np.int8).tocsr()

    #%% compute shell element
    def __compute_shell(self, ds=None, dp=None):

        xe_flattend = self.xe.flatten()

        if ds is None: ds = np.zeros((8, 1))
        if dp is None: dp = np.zeros((12, 1))
        self.ds = ds
        self.dp = dp
    
        # initialize for plate
        Kp_b  = np.zeros((12, 12))
        Ks  = np.zeros((8, 8))
        Kp_s1 = np.copy(Kp_b)
        Kp_s2 = np.copy(Kp_b)
        Mp  = np.copy(Kp_b)
        Ms  = np.copy(Ks)
        fcp = np.zeros((12, 1))
        fcs = np.zeros((8, 1))

        self.solid_Dh  = solid_Dps_lmd(self.E, self.nu) * self.h
        self.plate_Dbh = plate_Db_lmd(self.E, self.nu) * self.I
        self.plate_Dsh = plate_Ds_lmd(self.E, self.nu) * self.h

        # self.defb = np.empty((4), dtype=object)
        # self.forb = np.copy(self.defb)
        # self.defs = np.empty((2), dtype=object)
        # self.fors = np.copy(self.defs)

        # self.eps_n = np.copy(self.defb)
        # self.sig_n = np.copy(self.defb)
        # self.eps_s = np.copy(self.defs)
        # self.sig_s = np.copy(self.defs)

        # Create the diagonal matrix
        plate_rho = np.diag([self.h, self.I, self.I]) * self.rho
        # plate_rho = np.diag([self.h, self.h, self.h]) * self.rho #TODO: this is wrong
        solid_rho = np.diag([self.h, self.h]) * self.rho
        
        #%% full integration
        # for i, gp in enumerate(self.gpf):
        for i in range(4):

            gpfi = self.gpf[i]
            gwfi = self.gwf[i]

            Jac_val, Jac_det , Jac_blc , Jac_blc_inv = self.__compute_jac(gpfi)
            # N_plate, N_solid, Bb_plate, B_solid    = self.__compute_interpolation_full(gp)
            # plate_N , plate_Bb, solid_N, solid_B = self.__compute_interpolation_full(gp)

            ## solid behavior
            # Strain interpolation matrix
            solid_N = solid_N_lmd(*gpfi)
            solid_B = np.dot(np.array([[1, 0, 0, 0], 
                                       [0, 0, 0, 1]]), Jac_blc_inv.T) @ solid_B_lmd(*gpfi)

            # Strain interpolation matrix
            plate_N = plate_N_lmd(*gpfi)
            plate_Bb = np.dot(np.array([[1, 0, 0, 0], 
                                        [0, 0, 0, 1], 
                                        [0, 1, 1, 0]]), np.linalg.solve(Jac_blc, plate_Bb_lmd(*gpfi)))
            plate_Bs = plate_Bs1_lmd(*gpfi) + np.linalg.solve(Jac_val, plate_Bs2_lmd(*gpfi))

            # normal behavior
            Ks += solid_B.T @ self.solid_Dh[:2, :2] @ solid_B * Jac_det * gwfi # Gauss-Legendre sum for stiffness
            Kp_b += plate_Bb.T @ self.plate_Dbh @ plate_Bb * Jac_det * gwfi
            Kp_s2 += plate_Bs.T @ self.plate_Dsh @ plate_Bs * Jac_det * gwfi

            Ms += solid_N.T @ solid_rho @ solid_N * Jac_det * gwfi # Gauss-Legendre sum for mass
            Mp += plate_N.T @ plate_rho @ plate_N * Jac_det * gwfi

            fcs += (solid_N.T @ np.array([self.bx, self.by]).reshape(-1, 1)) * Jac_det * gwfi
            fcp += plate_N.T @ np.array([self.bz, 0, 0]).reshape(-1, 1) * Jac_det * gwfi
            
            # TODO fix
            # self.eps_n[i] = solid_B @ ds                     # strain (e_rr,e_yy,e_tt)
            # self.sig_n[i] = self.solid_Dh[:2, :2] @ self.eps_n[i] # stress (e_rr,e_yy,e_tt)
            # self.defb[i] = plate_Bb @ dp
            # self.forb[i] = self.plate_Dbh @ self.defb[i]            

        #%% reduced integration

        gpri = self.gpr[0]
        gwri = self.gwr[0]

        Jac_val, Jac_det, Jac_blc, Jac_blc_inv   = self.__compute_jac(gpri)
                
        # Strain interpolation matrix
        solid_B = np.dot(np.array([[0, 1, 1, 0]]), Jac_blc_inv.T) @ solid_B_lmd(*gpri)              
        plate_Bs = plate_Bs1_lmd(*gpri) + np.linalg.solve(Jac_val,  plate_Bs2_lmd(*gpri))

        # Gauss-Legendre sum for stiffness
        Ks += solid_B.T @ solid_B * self.solid_Dh[2, 2] * Jac_det * gwri
        Kp_s1 += plate_Bs.T @ self.plate_Dsh @ plate_Bs * Jac_det * gwri

        #TODO fix internal force calc
        # self.defs[0] = plate_Bs @ dp
        # self.fors[0] = self.plate_Dsh @ self.defs[0]
        # self.eps_s[0] = solid_B @ ds
        # self.sig_s[0] = self.solid_Dh[2, 2] * self.eps_s[0]

        #%% Hourglass control
        Kp_s = Kp_s1 + plate_delta_lmd(xe_flattend, self.h, self.epsilon) * (Kp_s2 - Kp_s1)

        Kp  = Kp_b + Kp_s
        
        #%% compute drilling
        Kd = drill_K_lmd(xe_flattend, self.h, self.E, self.alpha)
        Md = Kd/1e10
        fcd = np.zeros((4, 1))
        
        return Ks, Kp, Kd, Ms, Mp, Md, fcs, fcp, fcd

    #%% functions

    def __compute_jac(self, gp):
        # Jacobian and inverse jacobian
        Jac_val = Jac_lmd(gp, self.xe).reshape((2, 2))
        Jac_inv = np.linalg.inv(Jac_val)

        # determinant of jacobian
        Jac_det = np.linalg.det(Jac_val)
        
        if Jac_det < 0:
            raise ValueError('negative determinant of the jacobian')
        
        zeros = np.zeros((2,2))

        # blockdiagonal of jacobian and inverse jacobian
        Jac_blc     = np.block([[Jac_val,zeros],[zeros,Jac_val]])
        Jac_blc_inv = np.block([[Jac_inv,zeros],[zeros,Jac_inv]])

        return Jac_val, Jac_det, Jac_blc, Jac_blc_inv
    
    def __compute_interpolation_full(self, gp):

        # displacement (N) and strain (B) interpolation matrix
        plate_N = plate_N_lmd(*gp)
        plate_Bb = plate_Bb_lmd(*gp)
        solid_N = solid_N_lmd(*gp)
        solid_B = solid_B_lmd(*gp)

        return plate_N , plate_Bb, solid_N, solid_B
    
    def __compute_interpolation_red(self, gp):

        # strain (B) interpolation matrix
        plate_Bs1 = plate_Bs1_lmd(*gp)
        plate_Bs2 = plate_Bs2_lmd(*gp)

        return plate_N , plate_Bb, solid_N, solid_B

    #%% Extract parameters

    def __extract_pars(self, pars):
        # this is the element class used in packing/unpacking
        self.my_pars['elem'] = 'shell4'

        self.E   = pars.get("E", 210e9)
        self.nu  = pars.get("nu", 0.3)
        self.rho = pars.get("rho", 7850)
        self.h   = pars.get("h", 5e-3)
        self.I   = self.h**3/12
        self.nodal_labels = pars.get("nodal_labels", [1, 2, 3, 4]) # node labels
        self.nodal_coords = self.my_nodes.find_coords(self.nodal_labels) # extract nodal coordinates
        self.alpha   = pars.get("alpha", 0.3)
        self.epsilon = pars.get("epsilon", 0.01)
        self.bx      = pars.get("bx", 0.0)
        self.by      = pars.get("by", 0.0)
        self.bz      = pars.get("bz", 0.0)
        self.type    = pars.get("type", "ps")  # type of analysis (ps = plane stress, pe = plane strain, ax = axisymmetric)
        self.dofs_q  = pars.get("dofs_q", np.zeros((0, 2), dtype=np.int32))
        
    #%% Plot 3d elements
    def plot(self, ax, x=None, y=None, z=None, color='cyan'):
        if x is None: x = self.nodal_coords[:, 0]
        if y is None: y = self.nodal_coords[:, 1]
        if z is None: z = self.nodal_coords[:, 2]
            
        # Use nodal coordinates directly to form a quadrilateral grid
        surfaces = [[[x[0], y[0], z[0]], 
                     [x[1], y[1], z[1]], 
                     [x[2], y[2], z[2]], 
                     [x[3], y[3], z[3]]]]

        # Collect lines
        lines = [[[x[0], y[0], z[0]], [x[1], y[1], z[1]]],
                 [[x[1], y[1], z[1]], [x[2], y[2], z[2]]],
                 [[x[2], y[2], z[2]], [x[3], y[3], z[3]]],
                 [[x[3], y[3], z[3]], [x[0], y[0], z[0]]]]

        return lines, surfaces

    def dump_to_paraview(self):
        # here it goes the dump_to_paraview implementation for the beam3d element
        pass