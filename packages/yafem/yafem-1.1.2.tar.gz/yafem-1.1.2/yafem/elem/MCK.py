import numpy as np
from yafem.elem.core_elem import core_elem

#%% element_MCK class
class MCK(core_elem):
    """
    my_nodes : nodes

    pars: dictionary:
        K       : array,    stiffness matrix (required)
        M       : array,    mass matrix (default zeros with shape of K)
        C       : array,    damping matrix (default zeros with shape of K)
        dofs    : array,    list of degrees of freedom (default [[0,0],[1,0],...])
        dofs_q  : array,    temperature-controlled DOFs (default empty array)
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

    #%% extract parameters and assign default values
    def __extract_pars(self,pars):

        # this is the element class used in packing/unpacking
        self.my_pars['elem'] = 'MCK'

        # stiffness matrix
        if 'K' in pars:
            self.K = pars['K'].astype(np.float64)
        else:
            raise Exception('the stiffness parameter must be defined')

        self.M = pars.get('M', np.zeros(self.K.shape).astype(np.float64)) # mass matrix
        self.C = pars.get('C', np.zeros(self.K.shape).astype(np.float64)) # damping matrix

        # list of dofs
        self.dofs = pars.get('dofs', np.transpose([np.arange(0, self.K.shape[0], dtype=np.int32), 
                                     np.zeros(self.K.shape[0], dtype=np.int32)])).astype(np.int32)

        # temperature controlled dofs
        self.dofs_q = pars.get('dofs_q', np.zeros((0, 2), dtype=np.int32)).astype(np.int32)