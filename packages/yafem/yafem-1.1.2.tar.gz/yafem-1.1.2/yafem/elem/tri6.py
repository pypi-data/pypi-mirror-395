import numpy as np
from scipy.linalg import block_diag
from yafem.elem.core_elem import core_elem
from yafem.elem.tri6_func import *

#%% element_MCK class
class tri6(core_elem):
    """
    my_nodes : nodes

    pars: dictionary:
        E           : float,   Young's modulus (default 210e9)
        nu          : float,   Poisson's ratio (default 0.3)
        rho         : float,   material density (default 7850)
        h           : float,   element thickness (default 5e-3)
        k           : float,   shear factor (default 5/6)
        nodal_labels: list[int], node labels (default [1,2,3,4,5,6])
        dofs_q      : array,   temperature-controlled DOFs (default empty array)
    """

#%% class constructor
    def __init__(self, my_nodes, pars):

        # superclass constructor
        super().__init__(my_nodes,pars)

        self.linear_M = True
        self.linear_K = True
        self.linear_C = True

        # link the nodes to the element
        self.my_nodes = my_nodes

        # extract parameters and assign default values
        self.__extract_pars(pars)

        # element dofs
        self.__element_dofs(6)

        # vector to corners node 1 to 2 and node 1 to 3
        nodal_corners = self.nodal_coords
        
        # node 2 - node 1
        xp = nodal_corners[1,:] - nodal_corners[0,:]
        
        # normal vector to the plane
        zp = np.linalg.cross(xp,nodal_corners[2,:] - nodal_corners[0,:])

        xp = xp / np.linalg.norm(xp)
        zp = zp / np.linalg.norm(zp)

        # unit vector in the y-direction
        yp = np.cross(zp, xp)

        pc = np.mean(self.nodal_coords,axis=0)

        # Local axis xp, yp and zp shall be column vector
        self.T = np.array([xp, yp, zp])

        self.xp = xp
        self.yp = yp
        self.zp = zp

        xe = (self.nodal_coords - pc) @ np.array([xp, yp]).T
        self.xe = xe

        # Transformation matrix for the displacement vector of a single node
        # This is a triangle element, look into Filippa's book for further theoretical basis
        self.G = np.kron(np.eye(12), self.T)
        self.G = np.delete(self.G, np.arange(5,36,6), axis=0)

        self.gp_xy = gp_xy_6()
        self.gw_xy = gw_xy_6().squeeze()
        self.gp_z  = gp_z().squeeze()
        self.gw_z  = gw_z().squeeze()

        D_val = D_func(self.E,self.nu)
        I_val = I()
        h_half = self.h * 0.5

        self.Kl = np.zeros([30,30])
        self.Ml = np.zeros([30,30])

        xe_flattend = xe.flatten()

        # volume of the element
        self.area = A_func(xe_flattend)
        self.vol = self.area * self.h

        gp_plot = []

        # loop over the gauss points (in-plane)
        for i, gp_xyi in enumerate(self.gp_xy):

            # jacobian matrix
            J_val = jac(xe_flattend, gp_xyi)
            det_J_val = np.linalg.det(J_val)/2
                
            # inverse of jacobian matrix
            P_val = np.linalg.solve(J_val, I_val)
            P_val_block = block_diag(P_val, P_val, P_val).T

            gp_plot.append(self.nodal_coords.T @ phi(gp_xyi))

            B2 = B_z(xe_flattend, gp_xyi)

            # loop over the lobatto points (thickness)
            for j, gp_zj in enumerate(self.gp_z):
                  
                # half the height of the element multiplied with the gauss point
                zj = gp_zj * h_half
                  
                # displacement interpolation matrix
                N_val = N_func(xe_flattend, gp_xyi, zj)

                # strain interpolation matrix                  
                B1 = P_val_block @ B_xy(xe_flattend, gp_xyi, zj)
                B_val = B_b() @ np.vstack((B1, B2))

                # Gauss and Lobatto weights
                weight = self.gw_xy[i] * self.gw_z[j] * det_J_val * h_half

                # stiffness and mass matrix
                self.Kl += B_val.T @ D_val @ B_val * weight
                self.Ml += N_val.T @ N_val * self.rho * weight

        self.K = self.G.T @ self.Kl @ self.G
        self.M = self.G.T @ self.Ml @ self.G

        self.gp_plot = np.hstack(gp_plot).T

#%% extract parameters and assign default values
    def __extract_pars(self,pars):

        # this is the element class used in packing/unpacking
        self.my_pars['elem'] = 'tri6'

        self.E   = pars.get('E', 210e9) # young's modulus
        self.nu  = pars.get('nu', 0.3) # poisson's ratio
        self.rho = pars.get('rho', 7850) # material density
        self.h   = pars.get('h', 5e-3) # element thickness
        self.k   = pars.get('k', 5/6)  # shear factor
        self.nodal_labels = pars.get("nodal_labels", [1, 2, 3, 4, 5, 6])
        self.nodal_coords = self.my_nodes.find_coords(self.nodal_labels) # extract nodal coordinates
        self.type    = pars.get("type", "ps")  # type of analysis (ps = plane stress, pe = plane strain, ax = axisymmetric)

        # temperature controlled dofs
        self.dofs_q = pars.get('dofs_q', np.zeros((0, 2), dtype=np.int32)).astype(np.int32)

#%% element dofs
    def __element_dofs(self, dofs_per_node):
        self.dofs = np.empty([dofs_per_node*6,2],dtype=int)

        self.dofs[0:dofs_per_node,0]                 = self.nodal_labels[0] # Label of first node
        self.dofs[dofs_per_node*1:dofs_per_node*2,0] = self.nodal_labels[1] # Label of second node
        self.dofs[dofs_per_node*2:dofs_per_node*3,0] = self.nodal_labels[2] # Label of third node
        self.dofs[dofs_per_node*3:dofs_per_node*4,0] = self.nodal_labels[3] # Label of fourth node
        self.dofs[dofs_per_node*4:dofs_per_node*5,0] = self.nodal_labels[4] # Label of fifth node
        self.dofs[dofs_per_node*5:dofs_per_node*6,0] = self.nodal_labels[5] # Label of sixth node
        self.dofs[:,1] = np.tile(np.arange(0,dofs_per_node), 6) + 1 # Dofs of all nodes
    
        return self.dofs

#%% Plot 3d elements
    def plot(self, ax, x=None, y=None, z=None, color='cyan'):
        if x is None: x = self.nodal_coords[:, 0]
        if y is None: y = self.nodal_coords[:, 1]
        if z is None: z = self.nodal_coords[:, 2]
            
        # Subdivide 6-node triangle into 4 smaller 3-node triangles
        triangles = np.array([[0, 3, 5],    # Node 1 4 6
                              [3, 1, 4],    # Node 4 2 5
                              [5, 4, 2],    # Node 6 5 3
                              [3, 4, 5]])   # Node 4 5 6

         # Collect surface triangles using a lambda function
        surfaces_func = lambda row: \
            [[x[triangles[row, 0]], y[triangles[row, 0]], z[triangles[row, 0]]],
             [x[triangles[row, 1]], y[triangles[row, 1]], z[triangles[row, 1]]],
             [x[triangles[row, 2]], y[triangles[row, 2]], z[triangles[row, 2]]]]

        surfaces = [surfaces_func(0),
                    surfaces_func(1),
                    surfaces_func(2),
                    surfaces_func(3)]

        # Convert edges to line segments in the correct format
        lines = [[[x[0], y[0], z[0]], [x[3], y[3], z[3]]], # [0, 3]
                 [[x[3], y[3], z[3]], [x[1], y[1], z[1]]], # [3, 1]
                 [[x[1], y[1], z[1]], [x[4], y[4], z[4]]], # [1, 4]
                 [[x[4], y[4], z[4]], [x[2], y[2], z[2]]], # [4, 2]
                 [[x[2], y[2], z[2]], [x[5], y[5], z[5]]], # [2, 5]
                 [[x[5], y[5], z[5]], [x[0], y[0], z[0]]]] # [5, 0]

        return lines, surfaces