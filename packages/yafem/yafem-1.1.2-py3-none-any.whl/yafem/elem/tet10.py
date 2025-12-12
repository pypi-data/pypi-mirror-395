import numpy as np
from yafem.elem.core_elem import core_elem
from yafem.elem.tet10_func import *

#%% element_MCK class
class tet10(core_elem):
    """
    my_nodes : nodes

    pars: dictionary:
        E           : float,   Young's modulus (default 210e9)
        nu          : float,   Poisson's ratio (default 0.3)
        rho         : float,   material density (default 7850)
        h           : float,   element thickness (default 5e-3)
        k           : float,   shear factor (default 5/6)
        nodal_labels: list[int], node labels (default [1,2,3,4,5,6,7,8,9,10])
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
        self.__element_dofs(3)

        D_mat = D(self.E,self.nu)

        self.gp = gp()
        self.gw = gw()

        n_coord_flattend = self.nodal_coords.flatten()

        B1 = np.array([[1,0,0 , 0,0,0 , 0,0,0],
                       [0,0,0 , 0,1,0 , 0,0,0],
                       [0,0,0 , 0,0,0 , 0,0,1],
                       [0,0,0 , 0,0,1 , 0,1,0],
                       [0,0,1 , 0,0,0 , 1,0,0],
                       [0,1,0 , 1,0,0 , 0,0,0]], dtype=bool)
        
        I = np.array([[0, 0, 0], 
                      [1, 0, 0], 
                      [0, 1, 0], 
                      [0, 0, 1]], dtype=bool)

        # allocating K and M
        self.K = np.zeros([30,30])
        self.M = np.zeros([30,30])

        self.vol = V(*n_coord_flattend)
        jac3 = np.zeros((12, 9))

        for i, gpi in enumerate(self.gp):     

                # displacement interpolation matrix
                N_mat = N(n_coord_flattend, gpi)

                # jacobian matrix
                P_val = np.linalg.solve(jac(n_coord_flattend, gpi),I)
                
                # block diagonal
                jac3[0:4, 0:3]  = P_val
                jac3[4:8, 3:6]  = P_val
                jac3[8:12, 6:9] = P_val

                # strain interpolation matrix
                B_mat = B1 @ jac3.T @ B2(n_coord_flattend, gpi)

                # Gauss weights
                weight = self.gw[i]
                    
                # stiffness and mass matrix
                self.K += B_mat.T @ D_mat @ B_mat * self.vol * weight
                self.M += N_mat.T @ N_mat * self.rho * self.vol * weight

#%% extract parameters and assign default values
    def __extract_pars(self,pars):

        # this is the element class used in packing/unpacking
        self.my_pars['elem'] = 'tet10'

        self.E   = pars.get('E', 210e9) # young's modulus
        self.nu  = pars.get('nu', 0.3) # poisson's ratio
        self.rho = pars.get('rho', 7850) # material density
        self.h   = pars.get('h', 5e-3) # element thickness
        self.k   = pars.get('k', 5/6)  # shear factor
        self.nodal_labels = pars.get("nodal_labels", [1, 2, 3, 4, 5, 6, 7, 8, 9, 10])
        self.nodal_coords = self.my_nodes.find_coords(self.nodal_labels) # extract nodal coordinates
        self.gauss_order  = pars.get("gauss_order", 2)  # number of Gauss points
        self.type    = pars.get("type", "ps")  # type of analysis (ps = plane stress, pe = plane strain, ax = axisymmetric)

        # temperature controlled dofs
        self.dofs_q = pars.get('dofs_q', np.zeros((0, 2), dtype=np.int32)).astype(np.int32)

#%% element dofs
    # def __element_dofs(self, dofs_per_node):
    #     self.dofs = np.empty([dofs_per_node*10,2],dtype=int)

    #     self.dofs[0:dofs_per_node,0]                  = self.nodal_labels[0] # Label of first node
    #     self.dofs[dofs_per_node*1:dofs_per_node*2,0]  = self.nodal_labels[1] # Label of second node
    #     self.dofs[dofs_per_node*2:dofs_per_node*3,0]  = self.nodal_labels[2] # Label of third node
    #     self.dofs[dofs_per_node*3:dofs_per_node*4,0]  = self.nodal_labels[3] # Label of fourth node
    #     self.dofs[dofs_per_node*4:dofs_per_node*5,0]  = self.nodal_labels[4] # Label of fifth node
    #     self.dofs[dofs_per_node*5:dofs_per_node*6,0]  = self.nodal_labels[5] # Label of sixth node
    #     self.dofs[dofs_per_node*6:dofs_per_node*7,0]  = self.nodal_labels[6] # Label of sevetnth node
    #     self.dofs[dofs_per_node*7:dofs_per_node*8,0]  = self.nodal_labels[7] # Label of eigthth node
    #     self.dofs[dofs_per_node*8:dofs_per_node*9,0]  = self.nodal_labels[8] # Label of ninthth node
    #     self.dofs[dofs_per_node*9:dofs_per_node*10,0] = self.nodal_labels[9] # Label of tenth node
    #     self.dofs[:,1] = np.tile(np.arange(0,dofs_per_node), 10) + 1 # Dofs of all nodes
    
    #     return self.dofs
    
    def __element_dofs(self, dofs_per_node):
        n_nodes = 10
        self.dofs = np.empty((n_nodes * dofs_per_node, 2), dtype=int)
        self.dofs[:, 0] = np.repeat(self.nodal_labels, dofs_per_node)
        self.dofs[:, 1] = np.tile(np.arange(1, dofs_per_node + 1), n_nodes)

        return self.dofs

#%% Plot 3d elements
    def plot(self, ax, x=None, y=None, z=None, color='cyan'):
        if x is None: x = self.nodal_coords[:, 0]
        if y is None: y = self.nodal_coords[:, 1]
        if z is None: z = self.nodal_coords[:, 2]
            
        # Subdivide 6-node triangle into 4 smaller 3-node triangles
        triangles = np.array([[0, 4, 6],    # Node 1 5 7 # xy triangle
                              [4, 1, 5],    # Node 5 2 6
                              [6, 5, 2],    # Node 7 6 3
                              [4, 5, 6],    # Node 5 6 7

                              [0, 7, 4],    # Node 1 8 5 # xz triangle
                              [4, 9, 1],    # Node 5 10 2
                              [7, 3, 9],    # Node 8 4 10
                              [7, 9, 4],    # Node 8 10 5

                              [0, 6, 7],    # Node 1 7 8  # yz triangle
                              [6, 2, 8],    # Node 7 3 9
                              [7, 8, 3],    # Node 8 9 4
                              [7, 6, 8],    # Node 8 7 9

                              [5, 1, 9],    # Node 2 6 10 # incline triangle
                              [2, 5, 8],    # Node 6 3 9
                              [8, 9, 3],    # Node 9 10 4
                              [8, 5, 9],    # Node 9 6 10
                              ]) 

         # Collect surface triangles using a lambda function
        surfaces_func = lambda row: \
            [[x[triangles[row, 0]], y[triangles[row, 0]], z[triangles[row, 0]]],
             [x[triangles[row, 1]], y[triangles[row, 1]], z[triangles[row, 1]]],
             [x[triangles[row, 2]], y[triangles[row, 2]], z[triangles[row, 2]]]]

        surfaces = [surfaces_func(0), # xy triangle
                    surfaces_func(1),
                    surfaces_func(2),
                    surfaces_func(3),

                    surfaces_func(4), # xz triangle
                    surfaces_func(5),
                    surfaces_func(6),
                    surfaces_func(7),

                    surfaces_func(8), # yz triangle
                    surfaces_func(9),
                    surfaces_func(10),
                    surfaces_func(11),

                    surfaces_func(12), # incline triangle
                    surfaces_func(13),
                    surfaces_func(14),
                    surfaces_func(15),
                    ]

        line_func = lambda N1,N2: [[x[N1], y[N1], z[N1]], [x[N2], y[N2], z[N2]]]

        # Convert edges to line segments in the correct format
        lines = [line_func(0,4), # xy triangle
                 line_func(4,1),
                 line_func(1,5),
                 line_func(5,2),
                 line_func(2,6),
                 line_func(6,0),

                 line_func(0,7), # xz triangle
                 line_func(7,3),
                 line_func(1,9),
                 line_func(9,3),

                 line_func(3,8), # xz triangle
                 line_func(8,2),
                ]

        return lines, surfaces
    