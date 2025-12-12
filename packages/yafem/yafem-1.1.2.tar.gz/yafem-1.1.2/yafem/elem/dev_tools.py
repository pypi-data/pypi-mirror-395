import sympy as sp
import re
from itertools import chain

#%% Function to insert sub arrays into a larger array
def insert_subarray(A_large, A_small, indices):
    '''
    # A_large: pre-allocated main sympy array to insert a sympy sub-array
    # A_small: A sympy sub-array to fill into A_large
    # indices: Indices where A_small shall be filled into A_large ([rows],[cols])
    '''

    row_idx, col_idx = indices

    # Column vector
    if A_small.rows != 1 and A_small.cols == 1:
        for i, r in enumerate(row_idx):
            A_large[r, col_idx[0]] += A_small[i, 0]
    
    # row vector
    elif A_small.rows == 1 and A_small.cols != 1:
        for i, r in enumerate(col_idx): 
            A_large[row_idx[0], r] += A_small[0, i]

    # Full array
    else:  
        for i, r in enumerate(row_idx):
            for j, c in enumerate(col_idx):
                A_large[r, c] += A_small[i, j]

#%% Function to sort letters and numbers within a list
def sort_key(sym):

    match = re.match(r"([a-zA-Z]+)(\d+)", sym.name)  # Extract prefix and number
    if match:
        prefix, num = match.groups()
        return (prefix, int(num))  # Sort alphabetically, then numerically
    return (sym.name, 0)  # Default case (if no match)

#%% Function to extract common subexpressions in a sympy symbolic expression
def factoring(A):
    # Extract numerators and denominators separately
    numerators   = [sp.numer(x) for x in A]
    denominators = [sp.denom(x) for x in A]

    # Compute GCD of numerators and denominators
    gcd_numer = sp.gcd(tuple(numerators))  # Common factor from numerators
    gcd_denom = sp.lcm(tuple(denominators))  # Least Common Multiple of denominators

    # Compute the overall factor
    common_factor = sp.simplify(gcd_numer / gcd_denom)

    # Ensure no fractions remain inside the matrix
    factored_matrix = sp.simplify(A * gcd_denom / gcd_numer)  # Scale entries to be integer
    

    # Return the structured output
    result_A = sp.MatMul(common_factor, factored_matrix, evaluate=False)
    
    return result_A

#%% Function to convert dynamic symbols into regular symbols
# def dynSym_to_sym(sym):
#     # sym_set = sp.Matrix([sp.Symbol(str(s)) for s in sym])

#     sym_set = sp.Matrix([sp.Symbol((s.args[0].func.__name__ + ("_" + "d" * sum(pair[1] for pair in s.args[1:]))) 
#                                     if isinstance(s, sp.Derivative) else s.func.__name__) for s in sym])

#     return sym_set


def dynSym_to_sym(sym):
        sym_set_func = lambda sym: sp.Matrix([sp.Symbol((s.args[0].func.__name__ + ("_" + "d" * sum(pair[1] for pair in s.args[1:]))) 
                                if isinstance(s, sp.Derivative) else s.func.__name__) for s in sym])

        if isinstance(sym, sp.Matrix):
            sym_set = sym_set_func(sym)
        else:
            sym_set = sym_set_func(sp.Matrix([sym]))
            sym_set = sym_set[0]

        return sym_set


#%% replace dynamic symbols with regular symbols
def replace_dyn_symbols(expr, *symbol_pairs):
    symbol_pairs = [(sp.Matrix([sym_pair[0]]), sp.Matrix([sym_pair[1]])) for sym_pair in symbol_pairs[0]]

    q_replace = dict(chain.from_iterable(zip(dyn, reg) for dyn, reg in symbol_pairs))
    return expr.xreplace(q_replace)

# def replace_dyn_symbols(expr, sym):
#     if isinstance(sym, (tuple, list)):
#         sym = list(sym) 
#         for i, sym_i in enumerate(sym):
#             if isinstance(sym_i, sp.Matrix):
#                 sym[i] = sym_i
#             else:
#                 sym[i] = sp.Matrix([sym_i])
#     elif isinstance(sym, sp.Matrix):
#         sym = (sym,)
#     else: sym = (sp.Matrix([sym]),)



#     sym_static = [dynSym_to_sym(dyn) for dyn in sym]
#     symbol_pairs = [(dyn, dynSym_to_sym(dyn)) for dyn in sym]
#     q_replace = dict(chain.from_iterable(zip(dyn, reg) for dyn, reg in symbol_pairs))
    
#     return expr.xreplace(q_replace), tuple(sym_static)



#%% Function to extract the time independent symbols and store sorted in a Matrix
def get_free_symbols(*args, discard_t=False):

    p = set()
    
    for expr in args:
        p.update(expr.free_symbols)

    if discard_t == True:
        t = sp.symbols('t')
        p.discard(t)
    
    p = sp.Matrix(list(sorted(p, key=lambda sym: sym.name)))
    
    return p

#%% Function to dot product with a nested list of partial velocities
def dot_partial_velocities(VP, quant):

    n_VP = len(VP)    # number of partial velocities (rows)
    n_u  = len(VP[0]) # number of generalized speeds (columns)

    # Column-wise sum of dot products
    result = [sum(VP[idx_VP][idx_u].dot(quant[idx_VP]) for idx_VP in range(n_VP)) 
                                                       for idx_u in range(n_u)]

    return sp.Matrix(result)

#%% Function to convert sympy expressions to a numerical framework (Numpy, Jax, etc.)
def function_save(FileName, functions_to_save, module='numpy'):
    '''
    # FileName:          Name of the generated .py file
    # functions_to_save: A Python Dictonary of varibale name and the lambdified function "{var: lambdified_func}"
    # module:            Set the numerical framework "numpy", "jax" etc.
    '''
    import inspect
    import ast
    import importlib

    # Importing module (Switch to include e.g., jax or numpy)
    if module == "jax":
        module = "jax.numpy"
    # Import the module dynamically
    try:
        mod = importlib.import_module(module)
    except ImportError:
        print(f"Error: Module '{module}' could not be imported.")
        return

    # Write module import statement at the beginning of the file
    with open(FileName, "w") as file:
        file.write(f"import {module}\n\n")

    # Extracting source code adding prefix (e.g., numpy.cos or jax.numpy.sin)
    functions = {}

    # Looping though each function
    for name, func in functions_to_save.items():
        Module_attribute = set()

        # Obtaining the source code along with it's abtract syntax tree (ast)
        source_code = inspect.getsource(func) 
        tree = ast.parse(source_code) 
        input_params = list(inspect.signature(func).parameters.keys())

        # Walk through the AST to detect module attributes
        for node in ast.walk(tree):
            # Check if instance contain a "Name" e.g., "Name(id='x')" or "Name(id='cos')" AND check if "id" within said "Name" exists in the module
            if isinstance(node, ast.Name) and hasattr(node, "id") and node.id in dir(mod):
                if node.id in input_params:  # Avoid prefixing input parameters
                    print(f"Warning! Input parameter '{node.id}' conflicts with '{module}'. Ignoring prefix.")
                elif f"{module}.{node.id}" not in source_code:  # Avoid duplicate prefixing
                    Module_attribute.add(node.id)
                    source_code = source_code.replace(node.id, f"{module}.{node.id}")

        # Store modified function source and rename it
        functions[name] = source_code.replace('_lambdifygenerated', name)

        # Append modified function to the file
        with open(FileName, "a") as file:
            file.write(functions[name] + "\n")

        # Print detected attributes and final function source for debugging
        print('-' * 90)
        print(f"Detected attributes in function '{name}': {Module_attribute}\n")
        print(functions[name])