import numpy as np
import scipy as sp
import concurrent.futures
import jax
import jax.numpy as jnp
import matplotlib.pyplot as plt
import matplotlib.patches as patches
import scipy.sparse.linalg as spla
from scipy.sparse import eye as speye
from scipy.sparse import csr_array, coo_array, csc_array
from scipy.sparse.linalg import eigsh
from yafem.nodes import *
from yafem.elem.core_elem import core_elem
from mpl_toolkits.mplot3d.art3d import Line3DCollection, Poly3DCollection
import copy

# Caches
cache_eigenmodes = {} # Cache for eigenvectors
# cache_collocations = {} # Cache for collocations
# cache_M = {} # Cache for mass matrix
# cache_K = {} # Cache for stiffness matrix

class model:
    """
    my_nodes : nodes
        Node container providing coordinates and nodal information.

    my_elements : list
        List of element objects used in the model.

    pars : dictionary
        step        : int,    Number of simulation steps (default 10)
        dt          : float,  Time step size (default 1.0)
        dofs_c      : array,  List of constrained DOFs (default zeros((0,2), int32))
        dofs_m      : array,  List of master DOFs (default zeros((0,2), int32))
        dofs_s      : array,  List of slave DOFs (default zeros((0,2), int32))
        dofs_f      : array,  List of force-controlled DOFs (default zeros((0,2), int32))
        dofs_u      : array,  List of displacement-controlled DOFs (default zeros((0,2), int32))
        dofs_q      : array,  List of temperature-controlled DOFs (default zeros((0,2), int32))
        g_f         : array,  Force history applied to force-controlled DOFs (default zeros((dofs_f.size, step)))
        g_u         : array,  Displacement history applied to displacement-controlled DOFs (default zeros((dofs_u.size, step)))
        g_q         : array,  Temperature history applied to temperature-controlled DOFs (default zeros((dofs_q.size, step)))
        damping_model : str,  Damping model type, e.g., 'none' or 'proportional' (default 'none')
        alpha       : float,  Mass-proportional damping coefficient (default 0.0)
        beta        : float,  Stiffness-proportional damping coefficient (default 0.0)
    """
#%% this is the class constructor
    def __init__(self, my_nodes, my_elements, pars):

        # Assumed the model is model is non-linear in M, C and K 
        # so the model is assembled at least once
        self.linear_M = False
        self.linear_C = False
        self.linear_K = False

        # save the link the object my_nodes
        self.my_nodes = my_nodes

        # save the link the list object list my_elements
        self.my_elements = my_elements

        # extract the parameters and assign default values
        self.__extract_pars(pars)

        # list of model dofs
        self.dofs = np.zeros((0, 2), dtype=int)

        # assembly of the list of model dofs
        for my_element in self.my_elements:

            # for each dof of the element
            for idx_e, dof_e in enumerate(my_element.dofs):
                # loop over the slave dofs
                for idx_s, dof_s in enumerate(self.dofs_s):
                    # if the element dof is a slave dof
                    if np.array_equal(dof_e, dof_s):
                        # replace the element slave dof with the corresponding master dof
                        my_element.dofs[idx_e] = self.dofs_m[idx_s]

            # add the element dofs to the model dofs
            self.dofs = np.concatenate((self.dofs, my_element.dofs), axis=0)

        # remove repeated dofs
        self.dofs = np.unique(self.dofs, axis=0)

        # Removal of constraint dofs (dofs_c)
        if jnp.shape(self.dofs_c)[0] != 0:
            @jax.jit
            def collocation_indices(dof_c, dofs):

                def indices(dof_c, dofs):
                    match = jnp.all(dofs == dof_c, axis=1)
                    return jnp.argmax(match)

                idx = jax.vmap(indices, in_axes=(0, None))(dof_c, dofs)  

                return idx            

            idx = collocation_indices(self.dofs_c, self.dofs)
            self.dofs = np.delete(self.dofs, idx, axis=0)          

        # compute the collocation matrices of all elements
        self.__compute_collocations()

        # if there are master-slave equations
        if self.dofs_m.shape[0] > 0:
            # master-slave matrix
            self.Tu = speye(self.dofs.shape[0]).todense()
            # link slave to master dofs
            self.Tu[self.find_dofs(self.dofs_s), self.find_dofs(self.dofs_m)] = speye(self.dofs_m.shape[0]).todense()
            # eliminate slave dofs columns
            self.Tu = np.delete(self.Tu, self.find_dofs(self.dofs_s), axis=1)
            # eliminate slave dofs from dofs
            self.dofs = np.delete(self.dofs, self.find_dofs(self.dofs_s), axis=0)
            # update element incidence matrices based on master-slave equations
            for e, element in enumerate(self.my_elements, start=1):
                if e % 100 == 0:
                    print(f'update Zu element {e} of {len(self.my_elements)}')
                element.Zu = coo_array(element.Zu @ self.Tu, dtype=np.int8)

        # number of dofs
        self.ndof = self.dofs.shape[0]

        # compute the mass, stiffness and damping matrix
        self.__compute_MCK_matricies()

        # compute the proportional damping matrix
        self.compute_Cp()

        # compute collocation matrix for controlled forces
        self.compute_Bf()

        # compute collocation matrix for controlled displacements
        self.compute_Bu()

        # initialization of state vectors
        self.u = np.zeros((self.ndof), dtype=int)
        self.v = self.u.copy()
        self.a = self.u.copy()
        self.r = self.u.copy()
        self.f = self.u.copy()
        self.l = np.zeros((self.dofs_u.shape[0]), dtype=int)

        # Extended list of model DOFs for plot (6 DOFs per node)
        self.dofs_x = np.column_stack((np.repeat(self.my_nodes.nodal_labels, 6),
                                       np.tile(np.array([1, 2, 3, 4, 5, 6]), 
                                               self.my_nodes.nodal_labels.shape[0]))).astype(int)

        # indices of the model dofs on the extended dofs
        self.ind_x = self.find_dofs_x(self.dofs)

        # number of extended dofs
        self.ndofs_x = self.dofs_x.shape[0]
        
        # extended quantities for mesh plots
        self.u_x = np.zeros((self.ndofs_x), dtype=int)
        self.v_x = self.u_x.copy()
        self.a_x = self.u_x.copy()

        # check the linearity of the model
        self.linear_M = True
        self.linear_C = True
        self.linear_K = True
    
        for my_element in self.my_elements:
            self.linear_K = self.linear_K & my_element.linear_K
            self.linear_M = self.linear_M & my_element.linear_M
            self.linear_C = self.linear_C & my_element.linear_C

        # if the model is linear in M, C and K it is fully linear
        self.linear = self.linear_K & self.linear_M & self.linear_C


#%% concurrent processes 
    def __compute_collocations(self):
        with concurrent.futures.ThreadPoolExecutor() as executor:
                executor.map(self.__proces_collocations, self.my_elements)
        
        # global cache_collocations

        # Zu = cache_collocations.get("Zu", None)
        # Zq = cache_collocations.get("Zq", None)

        # if Zu is None or Zq is None:
        #     print('No cache')
        #     with concurrent.futures.ThreadPoolExecutor() as executor:
        #         executor.map(self.__proces_collocations, self.my_elements)

        #     cache_collocations["Zu"] = [elem.Zu for elem in self.my_elements]
        #     cache_collocations["Zq"] = [elem.Zq for elem in self.my_elements]

        # else:
        #     print('use cache')
        #     for elem, zu_val, zq_val in zip(self.my_elements, Zu, Zq):
        #         elem.Zu = zu_val
        #         elem.Zq = zq_val

    def __proces_collocations(self, element):
        element.compute_Zu(self.dofs)
        element.compute_Zq(self.dofs_q)

    def __compute_MCK_matricies(self):
        dofs0   = np.zeros_like(self.dofs[:, 0])    # Assumes dofs is (N, D), this gives length-N
        dofs0_q = np.zeros_like(self.dofs_q[:, 0])

        args = (dofs0, dofs0, dofs0_q, 0.0, 0)

        with concurrent.futures.ThreadPoolExecutor() as executor:
            futures = [executor.submit(self.compute_M, *args),
                       executor.submit(self.compute_K, *args),
                       executor.submit(self.compute_C, *args),
                       ]
            concurrent.futures.wait(futures)


#%% this method extract the parameters and assigns default values
    def __extract_pars(self,pars):

        # storage of input for packing/unpacking
        self.my_pars = copy.deepcopy(pars)

        self.step = int(pars.get('step', 10)) # number of simulation steps
        self.dt = float(pars.get('dt', 1.0)) # time step size

        self.dofs_c = pars.get('dofs_c', np.zeros((0, 2), dtype=np.int32)).astype(np.int32) # list of constrained dofs
        self.dofs_m = pars.get('dofs_m', np.zeros((0, 2), dtype=np.int32)).astype(np.int32) # list of master dofs
        self.dofs_s = pars.get('dofs_s', np.zeros((0, 2), dtype=np.int32)).astype(np.int32) # list of slave dofs
        self.dofs_f = np.array(pars.get('dofs_f', np.zeros((0, 2), dtype=np.int32)), dtype=np.int32)  # list of force-controlled dofs
        self.dofs_u = np.array(pars.get('dofs_u', np.zeros((0, 2), dtype=np.int32)), dtype=np.int32)  # list of displacement-controlled dofs
        self.dofs_q = np.array(pars.get('dofs_q', np.zeros((0, 2), dtype=np.int32)), dtype=np.int32)  # list of temperature-controlled dofs

         # Determine the number of steps from g_f, g_u, and g_q
        steps = []
        if 'g_f' in pars: steps.append(np.shape(pars['g_f'])[-1]) 
        if 'g_u' in pars: steps.append(np.shape(pars['g_u'])[-1]) 
        if 'g_q' in pars: steps.append(np.shape(pars['g_q'])[-1]) 

        # Set the number of steps, defaulting to 10 if no steps are provided
        self.step = max(steps) if steps else int(pars.get('step', 10))

        # Handle time step size
        self.dt = float(pars.get('dt', 1.0))

        # loading/force/temperature history applied to force/displacement/temperature-controlled dofs
        self.g_f = np.array(pars.get('g_f', np.zeros((self.dofs_f.shape[0], self.step), dtype=np.float64)), dtype=np.float64)
        self.g_u = np.array(pars.get('g_u', np.zeros((self.dofs_u.shape[0], self.step), dtype=np.float64)), dtype=np.float64)
        self.g_q = np.array(pars.get('g_q', np.zeros((self.dofs_q.shape[0], self.step), dtype=np.float64)), dtype=np.float64)

        # Ensure that g_f, g_u, and g_q are 2D arrays
        if len(self.g_f.shape) == 1: self.g_f = np.array([self.g_f])
        if len(self.g_u.shape) == 1: self.g_u = np.array([self.g_u])
        if len(self.g_q.shape) == 1: self.g_q = np.array([self.g_q])

        self.damping_model = pars.get('damping_model', 'none') # damping model - 'none' is proportional
        self.alpha = float(pars.get('alpha', 0.0)) # mass-proportional damping coefficient
        self.beta = float(pars.get('beta', 0.0)) # stiffness-proportional damping coefficient

        '''
        # damping ratio for modal damping
        if 'zeta' in pars:
            self.zeta = pars['zeta']
        else:
            self.zeta = 0.0
        '''
        # checks on the input
        if self.dofs_s.shape[0] != self.dofs_m.shape[0]:
            raise Exception('number of master/slave dofs do not match!')

#%% compute the model internal force
    def compute_f(self,u,v,a,q,t,i):
        
        f = np.zeros((self.dofs.shape[0]))

        # loop over the elements
        for my_element in self.my_elements:

            # compute the element restoring force vector
            fe = my_element.compute_f(my_element.Zu @ u, my_element.Zu @ v, my_element.Zu @ a, my_element.Zq @ q, t, i)
            # assemble the model restoring force vector
            f += my_element.Zu.transpose() @ fe

        # return the model restoring force vector
        return f            


#%% compute the model restoring force
    def compute_r(self,u,v,q,t,i):

        # initialize the restoring force vector
        r = np.zeros((self.dofs.shape[0]))

        # loop over the elements
        for my_element in self.my_elements:

            # compute the element restoring force vector
            re = my_element.compute_r(my_element.Zu @ u,my_element.Zu @ v, my_element.Zq @ q, t, i)

            # assemble the model restoring force vector
            r += my_element.Zu.transpose() @ re

        # return the model restoring force vector
        return r

#%% compute the model stiff and damping matrix
    def __compute_matrix(self, matrix_type, u, v, q, t, i):
        # Preallocate lists for assembling the matrix
        data = [[]] * len(self.my_elements)
        row_indices = data.copy()
        col_indices = data.copy()

        # Loop over the elements
        for idx, my_element in enumerate(self.my_elements):
            # Compute local quantities
            u_local = my_element.Zu @ u
            v_local = my_element.Zu @ v
            q_local = my_element.Zq @ q

            # Compute the local matrix using the matrix_type
            local_matrix = csr_array(matrix_type(my_element, u_local, v_local, q_local, t, i))

            # Assemble the global matrix
            coo_assembled = coo_array(my_element.Zu.transpose() @ local_matrix @ my_element.Zu)

            # Append data, rows, and columns to the respective lists
            data[idx]        = coo_assembled.data
            row_indices[idx] = coo_assembled.row
            col_indices[idx] = coo_assembled.col

        # Concatenate the collected data and indices
        data = np.concatenate(data)
        row_indices = np.concatenate(row_indices)
        col_indices = np.concatenate(col_indices)

        # Construct the final matrix in COO format, then convert to CSR
        return coo_array((data, (row_indices, col_indices)), shape=(len(self.dofs), len(self.dofs))).tocsr()
       
    def compute_K(self, u, v, q, t, i):
        # Compute the stiffness matrix
        if self.linear_K == False:
            self.K = self.__compute_matrix(core_elem.compute_K, u, v, q, t, i)
        return self.K
    
    def compute_C(self, u, v, q, t, i):
        # Compute the damping matrix
        if self.linear_C == False:
            self.C = self.__compute_matrix(core_elem.compute_C, u, v, q, t, i)
        return self.C

    def compute_M(self, u, v, q, t, i):
        # Compute the mass matrix
        if self.linear_M == False:
            self.M = self.__compute_matrix(core_elem.compute_M, u, v, q, t, i)
        return self.M

# #%% compute the model mass matrix
#     def compute_M(self):
#         # Preallocate lists for assembling the mass matrix
#         data = [[]] * len(self.my_elements)
#         row_indices =  data.copy()
#         col_indices =  data.copy()

#         # Loop over the elements
#         for idx, my_element in enumerate(self.my_elements):
#             # Compute element mass matrix
#             Me = csr_array(my_element.compute_M())

#             # Collect the non-zero values and indices for final assembly
#             coo_assembled_M = coo_array(my_element.Zu.transpose() @ Me @ my_element.Zu)

#             # Append data, rows, and columns to the respective lists
#             data[idx]        = coo_assembled_M.data
#             row_indices[idx] = coo_assembled_M.row
#             col_indices[idx] = coo_assembled_M.col

#         # Concatenate the collected data and indices
#         data = np.concatenate(data)
#         row_indices = np.concatenate(row_indices)
#         col_indices = np.concatenate(col_indices)

#         # Construct the final mass matrix in COO format, then convert to CSR
#         self.M = coo_array((data, (row_indices, col_indices)), shape=(len(self.dofs), len(self.dofs))).tocsr()

#         return self.M

#%% compute the proportional damping
    def compute_Cp(self):

        if self.damping_model == 'none':
            self.Cp = coo_array((len(self.dofs),len(self.dofs))).tocsr()

        elif self.damping_model == 'proportional':
            
            # compute the mass and stiffness matrices
            if np.shape(self.M) == 0 and np.shape(self.K) == 0:

                # initialize the displacement, velocity and acceleration
                u = np.zeros((self.dofs.shape[0],1))
                v = u.copy()
                q = np.zeros((self.dofs_q.shape[0],1))

                self.M = self.compute_M(u,v,q,0.0,0)
                self.K = self.compute_K(u,v,q,0.0,0)

            # compute the proportional damping
            self.Cp = self.M*self.alpha + self.K*self.beta     

        # return the proportional damping matrix
        return self.Cp    

#%% compute the collocation matrix for controlled forces or controlled displacements
    def __compute_collocation_B(self, ind_dofs, ind_dofs_uf):

        # Convert to numpy arrays for broadcasting, if not already
        dofs    = np.array(ind_dofs)
        dofs_uf = np.array(ind_dofs_uf)

        # Create a boolean matrix where True represents a match between dofs and dofs_u/dofs_f
        matches = np.all(dofs[:, None] == dofs_uf, axis=2)

        # Find indices where matches are True
        rows, cols = np.where(matches)

        # Create and return the sparse matrix
        return coo_array((np.ones_like(rows, dtype=bool), (rows, cols)), shape=(dofs.shape[0], dofs_uf.shape[0])).tocsc()

    def compute_Bf(self):
        self.Bf = self.__compute_collocation_B(self.dofs, self.dofs_f)

    def compute_Bu(self):
        self.Bu = self.__compute_collocation_B(self.dofs, self.dofs_u)

#%% reset the model
    def reset(self):
        
        self.u = np.zeros_like(self.u)
        self.v = np.zeros_like(self.v)
        self.a = np.zeros_like(self.a)
        self.r = np.zeros_like(self.r)
        self.f = np.zeros_like(self.f)
        self.l = np.zeros_like(self.l)

        self.u_x = np.zeros_like(self.u_x)
        self.v_x = np.zeros_like(self.v_x)
        self.a_x = np.zeros_like(self.a_x)

        # loop over the elements
        for my_element in self.my_elements:

            # reset the element
            my_element.reset()

#%% compute the modal analysis of the model
    def compute_modal(self,mode=1):

        # compute the mass and stiffness matrices
        if np.shape(self.M) == 0 and np.shape(self.K) == 0:

            # initialize the displacement, velocity and acceleration
            u = np.zeros((self.dofs.shape[0]))
            v = u.copy()
            q = np.zeros((self.dofs_q.shape[0]))
                
            # compute the mass and stiffness matrices
            self.M = self.compute_M(u,v,q,0.0,0)
            self.K = self.compute_K(u,v,q,0.0,0)
        
        global cache_eigenmodes
        v0  = cache_eigenmodes.get("phi", None)
        
        # solve the eigenvalue problem
        self.omega, self.phi = spla.eigsh(self.K, M=self.M, k=mode, which='LM', sigma=0, v0=v0, mode='normal')

        cache_eigenmodes["phi"] = self.phi[:, 0]
        
        # extended modal shape (for plots)
        self.phi_x = np.zeros((self.dofs_x.shape[0],self.phi.shape[1]))
        self.phi_x[self.ind_x,:] = self.phi

        # Compute natural frequencies (in Hz)
        self.omega = np.real(np.sqrt(self.omega))/(2*np.pi)

        return self.omega, self.phi
    
#%% compute the modal stress/strain
    # def compute_modal_se(self,mode=1):

    #     # compute the mass and stiffness matrices
    #     if not hasattr(self, "omega") and not hasattr(self, "phi"):
    #         self.omega, self.phi = self.compute_modal(mode)

    #     for i in range(len(self.my_elements)):
    #         if hasattr(self.my_elements[i], 'B'):
    #             self.my_elements[i].e_phi = []
    #             self.my_elements[i].s_phi = []
    #             for j in range(np.shape(self.phi)[1]):
    #                 B   = self.my_elements[i].B[:,self.find_dofs_e(self.my_elements[i].dofs)]
    #                 phi = self.phi[self.find_dofs(self.my_elements[i].dofs), j]

    #                 self.my_elements[i].e_phi.append(B @ phi)
    #                 self.my_elements[i].s_phi.append(self.my_elements[i].D @ self.my_elements[i].e_phi[j].T)

    #     return self.omega, self.phi
    
    def compute_modal_ss(self,mode_sel=1,dofs_sel=np.array([[1,1]])):
    
        # Convert to a numpy array
        mode_sel = np.atleast_1d(mode_sel)

        if np.shape(dofs_sel)[0] < np.shape(mode_sel)[0]:
            raise ValueError("Number of selected dofs (" + str(np.shape(dofs_sel)[0]) + 
                            ") and selected modes (" + str(np.shape(mode_sel)[0]) + ") have to match"
                            )

        # compute the mass and stiffness matrices
        if not hasattr(self, "omega") and not hasattr(self, "phi"):
            self.omega, self.phi = self.compute_modal(mode_sel.max())

        # Indicies of the selected dofs
        idxs_sel = self.find_dofs(dofs_sel)

        # Select the dofs
        if np.shape(self.phi)[1] == 1:
            phi_m = np.atleast_2d(self.phi[idxs_sel,:])
        else:   
            phi_m = self.phi[idxs_sel,:]

        # Select the modes
        phi_m = phi_m[:,mode_sel-1]

        # modal shapes for virtual sensing
        self.phi_vs = self.phi[:,mode_sel-1] @ np.linalg.solve(phi_m.T @ phi_m, phi_m.T)

        # Loop through all elements
        for i in range(len(self.my_elements)):
            if hasattr(self.my_elements[i], 'B'):
                self.my_elements[i].e_phi = self.my_elements[i].B @ self.my_elements[i].Zu @ self.phi_vs
                self.my_elements[i].s_phi = self.my_elements[i].D @ self.my_elements[i].e_phi

        return self.omega, self.phi
    
    # def compute_ss_modes(self,dofs_sel,mode_sel):

    #     # if mode_sel > dofs_sel trow an error

    #     self.compute_modal(mode_sel.max())
    #     idxs_sel = self.find_dofs(dofs_sel)

    #     print(self.phi)
    #     print(idxs_sel)
    #     print(mode_sel)

    #     phi_m = self.phi[idxs_sel,mode_sel-1] # modal shape on measured dofs
    #     self.phi_vs = self.phi[:,mode_sel-1] @ np.linalg.inv((phi_m.T @ phi_m)) @ phi_m.T # modal shapes for virtual sensing

    #     print(phi_m)
    #     print(self.phi_vs)

    #     for i in range(len(self.my_elements)):
    #         if hasattr(self.my_elements[i], 'B'):
    #             #self.my_elements[i].e_phi = np.zeros((self.my_elements[i].B.shape[0],dofs_sel))
    #             #self.my_elements[i].s_phi = np.zeros((self.my_elements[i].D.shape[0],dofs_sel))
    #             #for j in range(np.shape(phi_vs)[1]):
    #             self.my_elements[i].e_phi = self.my_elements[i].B @ self.my_elements[i].Zu @ self.phi_vs
    #             self.my_elements[i].s_phi = self.my_elements[i].D @ self.my_elements[i].e_phi
                
    #             #phi = self.phi[self.find_dofs(self.my_elements[i].dofs), j]
    #             #self.my_elements[i].e_phi.append(B @ phi)
    #             #self.my_elements[i].s_phi.append(self.my_elements[i].D @ self.my_elements[i].e_phi[j].T)

    #     return self.omega, self.phi
    
#%% extract the dof indices of selected dofs
    @jax.jit
    def __compute_find_dofs(dofs, dofs_sel):
        # Force "dofs_sel" to a 2D array
        dofs_sel = jnp.atleast_2d(dofs_sel)

        # Convert to JAX arrays
        dofs     = jnp.array(dofs)
        dofs_sel = jnp.array(dofs_sel)

        def find_index(dofs_sel):
            match = jnp.all(dofs == dofs_sel, axis=1)
            return jnp.argmax(match),  match

        # Use jax.vmap to apply the helper function over all selected DOFs
        idx, found = jax.vmap(find_index)(dofs_sel)
        rows = jnp.any(found, axis=1)

        return jnp.array(idx), rows, rows.all()

    def __check_find_dofs(self, dofs, dofs_sel):
        idx,  rows, all_true = model.__compute_find_dofs(dofs, dofs_sel)
        if not all_true: idx = idx[rows]
        return np.array(idx), rows
    
    # Find dofs in the constrained system
    def find_dofs(self, dofs_sel):
        return self.__check_find_dofs(self.dofs, dofs_sel)[0]
    
    # Find dofs in the full plotting system
    def find_dofs_x(self, dofs_sel):
        return self.__check_find_dofs(self.dofs_x, dofs_sel)[0]

    # Find indicies of dofs present/not present in the system
    def find_dofs_e(self, dofs_sel):
        return self.__check_find_dofs(self.dofs, dofs_sel)[1]


#%% extract the dof indices of selected nodes
    def find_nodes(self, nodes_sel):

        # force "nodes_sel" to a 2d array
        nodes_sel = np.atleast_2d(nodes_sel)

        nodes_sel = np.array(nodes_sel)
        
        nodes_in_dofs = np.array(self.dofs)[:, 0]
        matches = np.isin(nodes_in_dofs, nodes_sel)
        
        # Get the indices of matching elements
        idxs_sel = np.atleast_2d(np.where(matches)[0])

        if np.min(np.shape(nodes_sel)) != np.shape(idxs_sel)[0]:
            raise Exception("Warning! Number of selected nodes, do not match with detected indices")
        
        return idxs_sel

#%% extract the dof indices of selected directions
    def find_dirs(self,dirs_sel):
        dirs_sel = np.array(dirs_sel)
        
        nodes_in_dofs = np.array(self.dofs)[:, 1]
        matches = np.isin(nodes_in_dofs, dirs_sel)
        
        # Get the indices of matching elements
        idxs_sel = np.where(matches)[0]
        
        return idxs_sel
        
#%% post-processing
    def dump_to_paraview(self):
        # save nodal coordinates
        self.my_nodes.dump_to_paraview()
        # save element results
        for element in self.my_elements:
            element.dump_to_paraview()
        
    # dump the model results to the elements
    def dump_to_elements(self):
        for element in self.my_elements:
            element.u = element.Zu @ self.u
            element.v = element.Zu @ self.v
            element.q = element.Zq @ self.q
            # compute the element results (e.g., stress/strain)
            element.compute_results()
            
    #%% plots
    def plot(self, labels=False, rotate=(30,30), figsize=8, zoom=1.0, axis='on', response=None, scale=1):
        # plotting nodes
        ax = self.my_nodes.plot(labels=labels, rotate=rotate, figsize=figsize, zoom=zoom, axis=axis)
        
        # Collect all lines and surfaces for Line3DCollection and Poly3DCollection
        all_lines, all_surfaces = [], []
        for plot_properties in (element.plot(ax) for element in self.my_elements):
            
            # Applying line and surface features
            if plot_properties is None: continue  # Skip elements that return None (MCK elements)
            lines, surfaces = plot_properties
            if lines is not None:    all_lines.extend(lines)
            if surfaces is not None: all_surfaces.extend(surfaces)

        # Plotting response, if response is provided
        all_response_lines, all_response_surfaces = [], []
        if response is not None:
            # modal response expanded to full dofs array
            res = np.zeros([np.shape(self.dofs_x)[0]])
            res[self.find_dofs_x(self.dofs)] = np.atleast_1d(response)

            def process_element(element):
                idx = self.find_dofs_x(element.dofs)

                # Maximum dof number app
                max_dof_num = max(element.dofs[:, 1])

                # Storing model responses
                res_x = res[idx[0::max_dof_num]] * scale + np.atleast_1d(element.nodal_coords[:, 0])
                res_y = res[idx[1::max_dof_num]] * scale + np.atleast_1d(element.nodal_coords[:, 1])
                res_z = res[idx[2::max_dof_num]] * scale + np.atleast_1d(element.nodal_coords[:, 2])

                # Extracting element plot properties
                plot_properties = element.plot(ax, x=res_x, y=res_y, z=res_z, color='r')

                # Return the plot properties
                return plot_properties

            # Use ThreadPoolExecutor for concurrency
            with concurrent.futures.ThreadPoolExecutor() as executor:
                futures = [executor.submit(process_element, element) for element in self.my_elements]

                for future in futures:
                    plot_properties = future.result()

                    # Applying line and surface features
                    if plot_properties is None:
                        continue  # Skip elements that return None (MCK elements)
                    lines, surfaces = plot_properties
                    if lines: all_response_lines.extend(lines)
                    if surfaces: all_response_surfaces.extend(surfaces)

        # Combine all_surfaces and all_response_surfaces
        combined_lines = all_lines + all_response_lines
        combined_surfaces = all_surfaces + all_response_surfaces

        # Convert nested lists to arrays, flattening points
        lines_arr = np.array(all_response_lines).reshape(-1,3) if all_response_lines else np.empty((0,3))
        surfaces_arr = np.array(all_response_surfaces).reshape(-1,3) if all_response_surfaces else np.empty((0,3))

        # Get unique points
        combined_dots = np.unique(np.vstack((lines_arr, surfaces_arr)), axis=0)

        # Add all collected lines and surfaces to collections for plotting
        if combined_surfaces:
            facecolors = ['cyan'] * len(all_surfaces) + ['red'] * len(all_response_surfaces)
            poly_collection = Poly3DCollection(combined_surfaces, facecolors=facecolors, shade=True, lightsource=None, alpha=0.5, edgecolor=None)
            ax.add_collection3d(poly_collection)
        if combined_lines:
            colors = ['black'] * len(all_lines) + ['red'] * len(all_response_lines)
            line_collection = Line3DCollection(combined_lines, color=colors, linewidth=0.5)
            ax.add_collection(line_collection)

        ax.scatter(combined_dots[:, 0], combined_dots[:, 1], combined_dots[:, 2], c='r', marker='.',depthshade=False)

        return ax
