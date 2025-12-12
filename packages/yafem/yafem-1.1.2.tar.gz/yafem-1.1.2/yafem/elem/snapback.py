import numpy as np
from yafem.elem.core_elem import core_elem
from yafem.elem.snapback_func import *

class snapback(core_elem):
    """
    my_nodes : nodes

    pars: dictionary:
        E           : float,   Young's modulus (default 1.0)
        L           : float,   element length (default 1.0)
        A           : float,   element cross-sectional area (default 1.0)
        W           : float,   stiffness ratio (default 0.3)
        a           : float,   displacement step (default L*sin(pi/3))
        nodal_labels: list[int], node labels (default [1,2])
        dofs_q      : array,   temperature-controlled DOFs (default empty array)
    """

    #%% class constructor
    def __init__(self, my_nodes, pars):

        # superclass constructor
        super().__init__(my_nodes,pars)

        # link the nodes to the element
        self.my_nodes = my_nodes
        
        # extract parameters and assign default values
        self.__extract_pars(pars)

        self.__element_dofs(1)

        # initialization of matrices
        self.M = np.zeros([2,2])
        self.C = self.M .copy()
        self.K = snapback_K(self.W,self.A,self.E,self.L,self.a,[0,0])

    #%% extract parameters
    def __extract_pars(self, pars):
        self.E            = pars.get("E", 1.0) # young's modulus
        self.L            = pars.get("L", 1.0) # element length
        self.A            = pars.get("A", 1.0) # element cross section area
        self.W            = pars.get("W", 0.3) # stiffness ratio
        self.a            = pars.get("a", self.L * np.sin(np.pi/3)) # displacement step
        self.nodal_labels = pars.get("nodal_labels", [1, 2])

        # temperature controlled dofs
        self.dofs_q = np.array(pars.get("dofs_q", []), dtype=np.int32).reshape(-1, 2) if "dofs_q" in pars else np.zeros((0, 2), dtype=np.int32)
    
    #%% Computing element dofs
    def __element_dofs(self, dofs_per_node):

        self.dofs = np.empty([dofs_per_node*2,2],dtype=int)

        self.dofs[0:dofs_per_node,0] = self.nodal_labels[0] # Label of first node
        self.dofs[dofs_per_node:,0]  = self.nodal_labels[1] # Label of second node
        self.dofs[:,1] = np.tile(np.arange(0,dofs_per_node), 2) + 1 # Dofs of both nodes
    
        return self.dofs

    #%% Restoring force
    def compute_r(self,u,v,gq,t,i):

        # Link to the restoring force vector
        r = snapback_r(self.W,self.A,self.E,self.L,self.a,u).squeeze()

        return r

    #%% Tangent stiffness
    def compute_K(self,u,v,gq,t,i):

        # Link to the restoring force vector
        K = snapback_K(self.W,self.A,self.E,self.L,self.a,u)

        return K
