import numpy as np
import jax
import jax.numpy as jnp
from scipy.sparse import coo_array
import copy

#%% element class
class core_elem:

    #%% class constructor
    def __init__(self, my_nodes,pars):

        self.linear_M = True
        self.linear_K = False
        self.linear_C = False

         # link the nodes to the element
        self.my_nodes = my_nodes       
        
        # extract parameters and assign default values
        self.__extract_pars_core(pars)

    def __extract_pars_core(self,pars):
        
        # this is stored for packing/unpacking
        self.my_pars = copy.deepcopy(pars)

        # set the default element tag
        self.tag = pars.get("tag",0)

        # extract nodal labels
        self.nodal_labels = pars.get("nodal_labels", np.array([1]))
        
        # extract nodal coordinates
        self.nodal_coords = self.my_nodes.find_coords(self.nodal_labels)
    
        # temperature controlled dofs
        self.dofs_q = np.array(pars.get("dofs_q", []), dtype=np.int32).reshape(-1, 2) if "dofs_q" in pars else np.zeros((0, 2), dtype=np.int32)

    #%% compute the mass matrix
    def compute_M(self,u=None,v=None,q=None,t=None,i=None):
        return self.M
    
    #%% compute the damping matrix
    def compute_C(self,u,v,q=None,t=None,i=None):
        return self.C

    #%% compute the stiffness matrix
    def compute_K(self,u,v,q=None,t=None,i=None):
        return self.K
    
     #%% compute the internal force
    def compute_f(self,u,v,a,q=None,t=None,i=None):

        # compute the restoring force
        f = self.K @ u + self.C @ v + self.M @ a

        if hasattr(self, 'B'):

            # compute the strain/cross-sectional deformation
            self.e = self.B @ u

            # compute the stress/cross-sectional force
            self.s = self.D @ self.e

        # store the state variables
        self.u = u
        self.v = v
        self.a = a
        self.f = f
        self.t = t 
        self.i = i

        # return the internal force
        return f

    #%% compute the restoring force
    def compute_r(self,u,v,q=None,t=None,i=None):

        # compute the restoring force
        r = self.K @ u + self.C @ v

        if hasattr(self, 'B'):

            # compute the strain/cross-sectional deformation
            self.e = self.B @ u

            # compute the stress/cross-sectional force
            self.s = self.D @ self.e

        # store the state variables
        self.u = u
        self.v = v
        self.r = r
        self.t = t 
        self.i = i

        # return the restoring force
        return r

    #%% Function for compute the collocation matrix Zu and Zq
    @jax.jit
    def __compute_collocation(dof_e, dofs):
        def indices(dof_e, dofs):
            match = jnp.all(dofs == dof_e, axis=1)
            return jnp.argmax(match), jnp.any(match)

        idx, found = jax.vmap(indices, in_axes=(0, None))(dof_e, dofs)
        rows = jnp.where(found, jnp.arange(jnp.shape(found)[0]), 0)
        cols = jnp.take(idx, rows)
        data = jnp.ones_like(rows, dtype=bool)

        return rows, cols, data, found, found.all()

    def __compute_collocation_matrix(self, dof_e, dofs):
        if jnp.shape(dofs)[0] != 0:
            rows, cols, data, found, all_true = core_elem.__compute_collocation(dof_e, dofs)

            if not all_true:
                rows = rows[found]
                cols = cols[found]
                data = np.ones_like(rows, dtype=bool)
        else:
            rows, cols, data = [], [], []

        return coo_array((data, (rows, cols)), shape=(dof_e.shape[0], dofs.shape[0]), dtype=bool).tocsr()

    def compute_Zu(self, dofs):
        self.Zu = self.__compute_collocation_matrix(self.dofs, dofs)

    def compute_Zq(self, dofs_q):
        self.Zq = self.__compute_collocation_matrix(self.dofs_q, dofs_q)

    #%% reset the element state
    def reset(self):

        self.u = np.zeros(self.dofs.shape[0], dtype=int)
        self.v = self.u.copy()
        self.a = self.u.copy()
        self.q = np.zeros(self.dofs_q.shape[0], dtype=int)

    #%% plot the element
    def plot(self,ax,x=None, y=None, z=None, color=None):
        pass
    
    #%% compute element results (e.g., strain and stress)
    def __compute_results(self):
        pass

    #%% save element results in paraview
    def __dump_to_paraview(self):
        pass
