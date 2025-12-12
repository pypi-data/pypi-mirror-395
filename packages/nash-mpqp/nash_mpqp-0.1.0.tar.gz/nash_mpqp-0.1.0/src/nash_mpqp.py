# Solving multiparametric QP-GNEP problems.
#
# (c) A. Bemporad, S. Hall, 2025


import numpy as np
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from pdaqp import MPQP
import daqp
import joblib
from scipy.linalg import solve
import pypoman
from scipy.spatial import ConvexHull
from mpl_toolkits.mplot3d.art3d import Poly3DCollection
from scipy.optimize import linprog
import itertools
import warnings
import importlib.util
import dill
import gzip
from tqdm import tqdm
import time

def chebyshev_center(A, b, tol=1.e-10):
    # Finds the Chebyshev center of the polyhedron defined by Ax <= b. Rows of A whose norm is less than tol are considered as zero.
    nA = np.sqrt(np.sum(A**2, axis=1)) # norms of the rows of A
    is_zero = nA <= tol
    A[is_zero,:] = 0.  # consider small rows as zero
    nA[is_zero] = 0.  # consider small norms as zero. If the corresponding coefficient is negative, the LP will be infeasible
    c = np.zeros(A.shape[1]+1)
    c[-1] = -1.  # maximize radius: maximize_{x_c,r} (r) s.t. A*x_c + r*norm_ai <= b
    res = linprog(c, A_ub=np.hstack((A, nA.reshape(-1, 1))), b_ub=b, bounds=(-np.inf, np.inf))
    status = res.status # 0 = optimization terminated successfully, 2 = problem appears to be infeasible
    if status==0:
        x = res.x[:-1]
        radius = np.maximum(res.x[-1],0.)
    else:
        x = np.zeros(A.shape[1])
        radius = 0.
    return x, radius

def bounding_box(A,b,xmin,xmax):
    # Find the bounding box of the intersection of the polyhedron Ax <= b with the hyper-box xmin <= x <= xmax
    n = A.shape[1]
    bmin = np.empty(n)
    bmax = np.empty(n)
    for i in range(n):
        c = np.zeros(n)
        c[i] = 1.
        res = linprog(c, A_ub=np.vstack((A, np.eye(n), -np.eye(n))), b_ub=np.hstack((b.reshape(-1), xmax.reshape(-1), -xmin.reshape(-1))), bounds=(-np.inf, np.inf))
        bmin[i] = res.fun
        res = linprog(-c, A_ub=np.vstack((A, np.eye(n), -np.eye(n))), b_ub=np.hstack((b.reshape(-1), xmax.reshape(-1), -xmin.reshape(-1))), bounds=(-np.inf, np.inf))
        bmax[i] = -res.fun
    return bmin, bmax

def vertex_enumeration_region(A, b, lb, ub):
    nx = A.shape[1]  # number of variables
    return np.array(pypoman.compute_polytope_vertices(
            # self.regions[i]["A"], self.regions[i]["b"])).T
            np.vstack((A, np.eye(nx), -np.eye(nx))),
            np.hstack((b.reshape(-1,), ub, -lb)))).T

def polyplot(A, b, lb, ub, alpha=0.4, color=None, label=None, ax=None):
    """ Plots the polyhedron defined by Ax <= b, with bounds lb <= x <= ub. Only 2D and 3D plots are supported.
    """
    if ax is None:
        ax = plt.gca()
    
    if A.shape[1]==2:
        V = list(vertex_enumeration_region(A,b,lb,ub).T)
        hull = ConvexHull(V)
        V = np.array(V)[hull.vertices.tolist(), :]
        ax.set_xlim(lb[0], ub[0])
        ax.set_ylim(lb[1], ub[1])
        thecolor = np.array(color) if color is not None else np.random.rand(3)
        
        #if label is None:
        #    pypoman.plot_polygon(V, color = thecolor, alpha=alpha)
        #else:
        poly = Polygon(V, closed=True, facecolor=thecolor, edgecolor=thecolor/2., alpha=alpha, label=label)
        ax.add_patch(poly)
    
    elif A.shape[1]==3:
            # Get vertices from the polyhedron Ax <= b
            vertices = vertex_enumeration_region(A, b, lb, ub).round(8)
            
            # Transpose to get points in the right format for ConvexHull
            V = np.array(vertices).T  # Shape should be (n_points, 3)
            
            # Compute convex hull
            hull = ConvexHull(V)
            
            # Extract faces using the simplices
            faces = []
            for simplex in hull.simplices:
                faces.append(V[simplex])  # Use V, not vertices
            
            # Create the 3D polygon collection
            poly = Poly3DCollection(faces, color=np.random.rand(3), alpha=0.5, facecolor = color, edgecolor = color, label = label)
            ax.add_collection3d(poly)    
            
    else:
        raise ValueError("polyplot only supports 2D and 3D polyhedra.")

def polyreduce(A, b, removetol=1.e-10, checkempty=True, x0=None, zerotol=1.e-8):
    """
    Given a polyhedron Ax<=b, computes an equivalent polyhedron A[keptrows]*x<=b[keptrows] by eliminating redundant constraints.

    Parameters:
    removetol (float, optional): The tolerance for removing redundant constraints. Default is 1.e-10.
    checkempty (bool, optional): Flag indicating whether to check if the polyhedron is empty. Default is True.
    x0 (numpy.ndarray, optional): A point in the polyhedron. Default is None.
    zerotol (float, optional): The tolerance for considering a row of zeros. Default is 1.e-8.

    Returns:
    A (numpy.ndarray): The reduced matrix of constraints.
    b (numpy.ndarray): The reduced vector of bounds.
    isempty (bool): True if the polyhedron is empty, False otherwise.
    keptrows (numpy.ndarray): The indices of the rows kept in the reduced polyhedron.
    lpsolved (int): The number of LP problems solved.
    x0 (numpy.ndarray): A point in the original polyhedron. NaN if the original polyhedron is empty.
    
    Notes:
    - The function uses linear programming to eliminate redundant constraints.
    - The reduced polyhedron is obtained by solving a series of linear programming problems.
    - The function assumes that the polyhedron is in H-representation.

    This function is a Python porting of function POLYREDUCE.M in the Hybrid Toolbox for MATLAB.
    
    (C) 2003 by A. Bemporad, September 29, 2003
    (C) 2001 by A. Bemporad, 12/7/2001
    (C) 2024 A. Bemporad, Lucca, March 10, 2024
    """
    q, n = A.shape
    keptrows = np.arange(q)
    if q < 2:
        # Only one (or none) facet inequality
        lpsolved = 0
        if q == 0:
            x0 = np.zeros(n)
        else:
            x0 = np.random.rand(n)
            if A@x0 > b:
                # symmetrical with respect to the hyperplane
                x0 = x0-2*A.T@(A@x0-b)/(A@A.T)
        isempty = False
        return keptrows, lpsolved, x0, isempty

    lpsolved = 0
    keptrows = np.arange(q)
    i0 = np.where(np.sum(np.abs(A), axis=1) <= zerotol)[0]  # 0*x
    j0 = np.where(b[i0] < -zerotol)[0]  # 0*x<=b with b<0

    if len(j0) > 0:
        x0 = np.full(n, np.nan)
        lpsolved = 0
        isempty = True
        return A, b, isempty, keptrows, lpsolved, x0

    # Remove rows of the type 0*x<=b
    keptrows = np.delete(keptrows, i0)

    if keptrows.size == 0:
        # no more rows left
        x0 = np.zeros(n)
        isempty = False
        A = np.zeros((0, n))
        b = np.zeros((0, 1))
        return A, b, isempty, keptrows, lpsolved, x0

    if checkempty:
        # Determine if the polyhedron is empty
        res = linprog(
            np.zeros(n), A_ub=A[keptrows], b_ub=b[keptrows], bounds=(None, None))
        # res = glpk(c=np.zeros(n), A_ub=A[keptrows], b_ub=b[keptrows], bounds=(None, None))
        lpsolved += 1
        if res.status == 2:  # Infeasible
            # if res.status == GLPK.GLP_INFEAS or res.status == GLPK.GLP_NOFEAS:
            x0 = np.full(n, np.nan)
            isempty = True
            return A, b, isempty, keptrows, lpsolved, x0
        x0 = res.x  # Use this for a warm start for the following LP's

    isempty = False

    # Remove redundant constraints
    j = 0
    while j < len(keptrows):
        f = A[keptrows[j]]
        g = b[keptrows[j]]
        ii = np.setdiff1d(keptrows, keptrows[j])
        if ii.size > 0:
            res = linprog(-f, A_ub=A[ii], b_ub=b[ii], bounds=(None, None))
            # res = glpk(c=-f, A_ub=A[ii], b_ub=b[ii], bounds=(None, None))
            lpsolved += 1
            flag = res.status
            if flag == 0:
                # if flag == GLPK.GLP_OPT or flag == GLPK.GLP_FEAS:
                val = f @ res.x - g  # LP should be always feasible
            elif flag == 3:
                val = 1.e6
                flag = 0
        if flag != 0 or (flag == 0 and val <= removetol):
            # remove the constraint
            keptrows = ii
        else:
            j += 1

    A = A[keptrows]
    b = b[keptrows]
    return A, b, isempty, keptrows, lpsolved, x0

def project(A, b, Ind):
    """
    Projects the polyhedron P = {A*x <= b} onto the space of x[j] for j not in Ind,
    that is, gets rid of the components x[Ind], using Fourier-Motzkin elimination.

    A,b: Polyhedron to project
    Ind: Indices of components to be eliminated (starting from 0)
    """
    
    def one_projection(A, b, j, n):
        # Reduces the dimension of the polyhedron by eliminating the j-th component x[j]
        J = list(range(j)) + list(range(j+1, n))
        zerotol = 1e-8
        a = A[:, j]
        E = np.where(np.abs(a) < zerotol)[0]
        G = np.where(a >= zerotol)[0]
        N = np.where(a <= -zerotol)[0]
        nG = len(G)
        nN = len(N)
        
        A1 = np.vstack([A[E][:, J], np.zeros((nG * nN, n - 1))])
        b1 = np.vstack([b[E].reshape(-1,1), np.zeros((nG * nN,1))]).reshape(-1)
        
        if nG > 0 and nN > 0:
            ne = len(E)
            
            # a1g*x1+a2g*x2<=bg:   x1<=-a2g/a1g*x2+bg/a1, a1g>0   ---> -a2n/a1n*x2+bn/a1n<=-a2g/a1g*x2+bg/a1g
            # a1n*x1+a2n*x2<=bn:   x1>=-a2n/a1n*x2+bn/a1, a1n<0
            bG = b[G].reshape(-1) / a[G].reshape(-1)
            AG = -A[G][:, J] / (a[G].reshape(-1,1)@np.ones((1,n-1)))
            bN = b[N].reshape(-1) / a[N].reshape(-1)
            AN = -A[N][:, J] / (a[N].reshape(-1,1)@np.ones((1,n-1)))
            
            for i in range(nG):
                for j in range(nN):
                    A1[(i * nN + j + ne), :] = AN[j, :] - AG[i, :]
                    b1[(i * nN + j + ne)] = bG[i] - bN[j]
            
            A1, b1, _, _, _, _ = polyreduce(A1, b1, removetol=1.e-4, zerotol=1.e-6)
        return A1, b1

    # Reduce the polyhedron by removing redundant constraints and check if it is empty
    A, b, isempty, _, _, _ = polyreduce(A, b)
    n = A.shape[1]
    AA = A
    bb = b
    Ind = sorted(set(Ind))
    
    N = 25  # Warning threshold for large polyhedron
    for i in range(len(Ind)):
        if len(bb) > N:
            warnings.warn('Polytope projection may take some time to compute ...')
        
        AA, bb = one_projection(AA, bb, Ind[i], n)
        
        # Having deleted variable x(I(i)), all other remaining indices scale
        # down by 1 to properly index the remaining n-1 columns of matrix AA
        Ind = [index - 1 if index > Ind[i] else index for index in Ind]
        n -= 1
    return AA, bb

def get_indices(i, dim, nvar):
    # Get indices of the variables optimized by the i-th agent and the complementary indices
    isi = np.arange(np.sum(dim[:i]),np.sum(dim[:i+1]), dtype=int)
    nisi = np.hstack((np.arange(0, np.sum(dim[:i]), dtype=int), np.arange(np.sum(dim[:i+1]), nvar, dtype=int)))    
    return isi, nisi

def augment_CRs_with_lambda(mpQP):
    """Add explicit function of the Lagrange multipliers lambda(param) = Klambda*param + klambda to each critical region.
    """
    mp = mpQP.mpQP
    Q_inv = np.linalg.inv(mp.H)    
    for i, cr in enumerate(mpQP.CRs):
        Klambda = np.zeros((len(mp.A), mp.F.shape[1]))
        klambda = np.zeros(len(mp.A))
        
        nAS = len(cr.AS)
        if nAS>0:
            
            if np.linalg.matrix_rank(mp.A[cr.AS]) < nAS:
                print("Warning: Active constraints not linearly independent!")
            
            # Q*x+c+F*theta + A'*lambda = 0 -> x = -Q^-1*(c + F*theta + A'*lambda)
            # A*x - b - B*theta = 0 -> A*(-Q^-1*(c + F*theta + A'*lambda)) - b - B*theta = 0
            # => lambda = - (A*Q^-1*A')^-1 * (B + A*Q^-1*F)*theta - (A*Q^-1*A')^-1 * (b+A*Q^-1*c)
            M_inv = np.linalg.inv(mp.A[cr.AS] @ Q_inv @ mp.A[cr.AS].T)
            Klambda[cr.AS] = -M_inv @ (mp.B[cr.AS] + mp.A[cr.AS] @ Q_inv @ mp.F)
            klambda[cr.AS] = -M_inv @ (mp.b[cr.AS]+ mp.A[cr.AS] @ Q_inv @ mp.f)
        
        mpQP.CRs[i].Klambda = Klambda
        mpQP.CRs[i].klambda = klambda        
        
    return mpQP

class NashMPQP:
    """ Class for solving Multiparametric Generalized Nash Equilibrium Problems defined by quadratic costs and linear constraints.
    
    (C) A. Bemporad, S. Hall, 2025
    """

    def __init__(self, dim, pmin, pmax, xmin, xmax, Q, c, F, A, b, S, lb=None, ub=None, split="min-norm", parallel_processing=True, verbose=True):
        """ Initializes the Nash-mpQP problem.
        
        Parameters:
        ------------
        dim (list): List of number of variables for each agent. The total number of variables is nvar = sum(dim), the total number of agents is N = len(dim).
        
        pmin (numpy.ndarray): Lower bounds on parameters.
        
        pmax (numpy.ndarray): Upper bounds on parameters.
                
        xmin (numpy.ndarray): Lower bounds on variables for which the solution is computed. These are not considered as constraints in the mpQPs of each agent, but are only used for computing the parametric solution within the box defined by xmin and xmax. Lower bounds on variables must be included in the lb argument.
        
        xmax (numpy.ndarray): Upper bounds on variables for which the solution is computed. 

        Q (list): List of quadratic cost matrices for each agent. Each Qi must be symmetric positive definite of size (nvar, nvar), where nvar = sum(dim).
        
        c (list): List of linear cost vectors for each agent. Each ci must be of size (nvar).
        
        F (list): List of parameter gain matrices for each agent. Each Fi must be of size (nvar, npar), where npar is the number of parameters.
        
        A (numpy.ndarray): Constraint matrix. Matrix A must be of size (ncon, nvar), where ncon is the number of coupling constraints and nvar = sum(dim).
        
        b (numpy.ndarray): Constraint vector. Vector b must be of size (ncon).
        
        S (numpy.ndarray): Constraint parameter gain matrix. Matrix S must be of size (ncon, npar).
        
        lb (numpy.ndarray): Lower bounds on variables. Entries equal to -inf can be used to indicate unbounded variables.
        If None, no lower bounds are considered.
        
        ub (numpy.ndarray): Upper bounds on variables. Entries equal to +inf can be used to indicate unbounded variables.
        If None, no upper bounds are considered.
        
        split (string): how to handle critical regions with infinitely-many solutions:
            split = "min-norm" (default): split the critical region into subregions, each with a unique minimum-norm equilibrium solution;

            split = "welfare": split the critical region into subregions, each with a unique welfare equilibrium solution where the sum of all agents' costs is minimized;
        
            split = "variational": overlaps a (sub)region of unique variational GNE solution (if it exists) over a region of infinitely-many solutions;

            split = "variational-split": split the critical region into a subregion characterized by a unique variational GNE solution (if it exists), plus a partition of the remaining set into polyhedral subregions with infinitely-many solutions;
            
            split = None: keep an entire critical region with infinitely-many solutions as a single region.
        
        parallel_processing (bool): If True, solves the mpQPs in parallel using all available CPU cores.
        
        verbose (bool): If True, prints additional progress messages.
        """
        
        pmin=np.array(pmin).reshape(-1)
        pmax=np.array(pmax).reshape(-1)
        if not pmin.size==pmax.size:
            raise ValueError(f"Length of lower bounds vector pmin = {pmin.size} does not match length of upper bounds vector pmax = {pmax.size}.")
        self.npar = pmin.size
        self.nvar = sum(dim)
        self.ncon = A.shape[0]
        
        N = len(dim) # number of agents
        if not len(Q)==N:
            raise ValueError(f"Number of quadratic cost matrices {len(Q)} does not match number of agents = {N}.")
        if not len(c)==N:
            raise ValueError(f"Number of linear cost vectors {len(c)} does not match number of agents = {N}.")
        if not len(F)==N:
            raise ValueError(f"Number of parameter gain matrices {len(F)} does not match number of agents = {N}.")
        
        for i in range(N):
            if not Q[i].shape==(self.nvar,self.nvar):
                raise ValueError(f"Quadratic cost matrix Q[{i}] has shape {Q[i].shape}, expected ({self.nvar},{self.nvar}).")
            if not c[i].size==self.nvar:
                raise ValueError(f"Linear cost vector c[{i}] has length {c[i].shape}, expected {self.nvar}.")
            if not F[i].shape==(self.nvar,self.npar):
                raise ValueError(f"Parameter gain matrix F[{i}] has shape {F[i].shape}, expected ({self.nvar},{self.npar}).")   
        
        if (lb is not None) and (not len(lb)==self.nvar):
            raise ValueError(f"Length of lower bounds vector lb = {len(lb)} does not match total number of variables = {self.nvar}.")
        if (ub is not None) and (not len(ub)==self.nvar):
            raise ValueError(f"Length of upper bounds vector ub = {len(ub)} does not match total number of variables = {self.nvar}.")   

        if not (A.shape[1]==self.nvar):
            raise ValueError(f"Coupling constraint matrix A has {A.shape[1]} columns, expected {self.nvar}.")
        if not (b.shape[0]==self.ncon):
            raise ValueError(f"Coupling constraint vector b has {b.shape[0]} rows, expected {A.shape[0]}.")
        if not (S.shape[0]==self.ncon and S.shape[1]==self.npar):
            raise ValueError(f"Coupling constraint parameter gain matrix S has shape {S.shape}, expected ({self.ncon},{self.npar}).")

        xmin = np.array(xmin).reshape(-1)
        xmax = np.array(xmax).reshape(-1)
        if not (xmin.size==self.nvar):
            raise ValueError(f"Length of variable lower range xmin = {len(xmin)} does not match total number of variables = {self.nvar}.")
        if not (xmax.size==self.nvar):
            raise ValueError(f"Length of variable upper range xmax = {len(xmax)} does not match total number of variables = {self.nvar}.")  

        # Add finite bounds lb <= x <= ub to constraint matrices A, b, S
        for i in range(self.nvar):
            if lb is not None and lb[i] > -np.inf:
                Ai = np.zeros((1,self.nvar))
                Ai[0,i] = -1.
                bi = np.array([-lb[i]])
                Si = np.zeros((1,self.npar))
                A = np.vstack((A, Ai))
                b = np.hstack((b, bi))
                S = np.vstack((S, Si))
                xmin[i] = max(xmin[i], lb[i]) # update xmin
            if ub is not None and ub[i] < np.inf:
                Ai = np.zeros((1,self.nvar))
                Ai[0,i] = 1.
                bi = np.array([ub[i]])
                Si = np.zeros((1,self.npar))
                A = np.vstack((A, Ai))
                b = np.hstack((b, bi))
                S = np.vstack((S, Si))
                xmax[i] = min(xmax[i], ub[i]) # update xmax
                
        self.ncon = A.shape[0] # update number of constraints
        
        self.N = N
        self.dim = dim
        self.Q = Q
        self.c = c
        self.F = F
        self.A = A
        self.b = b
        self.S = S
        self.lb = lb
        self.ub = ub
        self.xmin = xmin
        self.xmax = xmax
        self.pmin = pmin
        self.pmax = pmax
        
        if parallel_processing and importlib.util.find_spec("joblib") is None:
            parallel_processing = False # joblib is not installed, disable parallel processing
        self.parallel_processing = parallel_processing
        self.verbose = verbose

        self.split_method = split
        self.split = True # split by default when infinitely-many solutions occur
        self.min_norm = False
        self.variational = False
        self.variational_split = False
        self.welfare = False
        match split:
            case "min-norm":
                self.min_norm = True
            case "variational":
                self.variational = True
                self.split = False
            case "variational-split":
                self.variational_split = True
            case "welfare":
                self.welfare = True
            case None:
                self.split = False
            case _:
                raise ValueError(f"Unknown split method '{split}'.")

    def solve(self):
        elapsed_time = time.time()
        
        dim = self.dim
        Q=self.Q
        c=self.c
        F=self.F
        A=self.A
        b=self.b
        S=self.S
        N=self.N
        npar=self.npar
        nvar=self.nvar
        ncon=self.ncon
        pmin=self.pmin
        pmax=self.pmax
        xmin=self.xmin
        xmax=self.xmax
        
        def solve_mpQP(i):
            """ Solves the i-th agent's multiparametric QP problem to get explicit best-response
            """
            isi, nisi = get_indices(i, dim, nvar)
            Qi = Q[i][isi][:,isi].reshape(dim[i], dim[i])
            fi = c[i][isi]
            Fi = np.hstack((Q[i][isi][:,nisi].reshape(dim[i],-1),F[i][isi, :].reshape(dim[i],-1)))
            thmin = np.hstack((xmin[nisi], pmin))
            thmax = np.hstack((xmax[nisi], pmax))
            Ai = A[:, isi]
            bi = b
            Bi = np.hstack((-A[:,nisi],S))
            
            # Solve the following mpQP:
            # 
            # min_z  1/2 z' Qi z + (fi+Fi θ)' z  
            # s.t    Ai z <= bi + Bi θ
            #
            # for parameters theta in the hyper-box [thmin, thmax]
            mpQP = MPQP(Qi, fi, Fi, Ai, bi, Bi, thmin, thmax)
            mpQP.solve()
            return mpQP

        def vprint(msg, end="\n"):
            if self.verbose:
                print(msg, end=end)
                
        if self.parallel_processing:
            mpQPs = joblib.Parallel(n_jobs=joblib.cpu_count())(joblib.delayed(solve_mpQP)(i) for i in range(N))
            mpQPs = [augment_CRs_with_lambda(mpQP) for mpQP in mpQPs]
        else:
            # Sequential execution to create mpQPs list
            mpQPs = []
            vprint("Solving multiparametric QPs sequentially...")
            for i in range(N):
                vprint(f"  Solving agent {i}/{N}...", end=" ")
                try:
                    mpQP = solve_mpQP(i)            
                    mpQP = augment_CRs_with_lambda(mpQP)            
                    mpQPs.append(mpQP)
                    vprint("\u2713")
                except Exception as e:
                    vprint(f"\u2717")
                    raise RuntimeError(f"Failed to solve agent {i}: {e}")
        vprint(f"mpQPs successfully solved for all {N} agents!")

        self.mpQPs = mpQPs # store agents' mpQPs in the object, in case one wants to inspect them
        
        # Solve the multiparametric QP-GNEP problem for all combinations of critical regions
        self.CRs = list()  
        self.gains_all = list()
        self.gains_CRs = list()
        
        combinations = list(itertools.product(*[range(len(mpQPs[i].CRs)) for i in range(N)]))

        # Find coupling constraints among agents
        G = np.zeros((ncon,N), dtype=bool) # G[i,j] = 1 if constraint i depends on agent j's variables
        ki = 0
        for i in range(N):
            G[:,i] = np.any(A[:,ki:ki+dim[i]]!=0, axis=1)
            ki += dim[i]

        for comb in tqdm(combinations, total=len(combinations),
                         ncols=60, bar_format="{l_bar}{bar}| {n_fmt}/{total_fmt}", colour="black", leave=True):

            # Check whether the combination is valid, i.e., active/inactive constraints are consistent
            active_sets = [mpQPs[i].CRs[comb[i]].AS for i in range(N)]
            G_act = np.zeros((ncon,N), dtype=bool) # G_act[j,i] = True if constraint j is active for agent i
            for i in range(N):
                G_act[active_sets[i],i] = True
            cond = [sum(G_act[j,G[j,:]]) % sum(G[j,:]) ==0 for j in range(ncon)] # check if the entries of G_act[j,G[j,:]], which are nj=sum(G[j,:]) entries, are either all False (their sum is 0, and hence 0 % nj = 0) or all True (their sum is nj, and again nj % nj = 0), for each constraint j
            if not all(cond):
                # active sets are inconsistent, skip this combination
                continue
            
            bi = [mpQPs[i].CRs[comb[i]].bth for i in range(N)]
            Ai = [mpQPs[i].CRs[comb[i]].Ath for i in range(N)]
            gains = list()
            AA = list()
            for i in range(N):
                # expand Ai[x(-i),p] to Ai[x,p], i.e., include also the components related to x(i)
                n1 = int(np.sum(dim[:i]))  # dim[0]+...+dim[i-1]
                nA = Ai[i].shape[0]
                AA.append(np.hstack([Ai[i][:,:n1].reshape(nA,n1), # part related to x(-i)
                                    np.zeros((nA,dim[i])), # zeros for x(i)
                                    Ai[i][:,n1:].reshape(nA,nvar-dim[i]-n1+npar) # part related to the rest of x(-i) and p
                                    ]))
                # expand gain[x(-i),p] to gain[x,p], i.e., include also the components related to x(i)
                gains.append(np.hstack([
                    mpQPs[i].CRs[comb[i]].z[:,:n1].reshape(dim[i],n1), # part related to x(-i)
                    np.zeros((dim[i],dim[i])), # zeros for x(i)
                    mpQPs[i].CRs[comb[i]].z[:,n1:].reshape(dim[i],nvar-dim[i]-n1+npar+1) # part related to the rest of x(-i), p, and offset
                    ]))

            gains = np.vstack(gains)
            self.gains_all.append(gains)
            
            Mx = np.eye(nvar)
            for j in range(N):
                isj = np.arange(np.sum(dim[:j]),np.sum(dim[:j+1]), dtype=int)
                nisj = np.hstack((np.arange(0, np.sum(dim[:j]), dtype=int), np.arange(np.sum(dim[:j+1]), nvar, dtype=int)))
                Mx[np.ix_(isj,nisj)] = -gains[np.ix_(isj,nisj)]
            Mp = gains[:,-npar-1:]

            U,s,Vt = np.linalg.svd(Mx)
            rank_Mx = np.sum(s >= 1.e-6)  # count number of singular values above threshold.
            if rank_Mx==nvar:
                Gp = solve(Mx, Mp) # explicit solution x=Gp*[p;1]
                # Critical region for the parametric Nash equilibrium
                # A[:,:nvar]@Gp@[p;1] + A[:,nvar:nvar+npar]@p <= bi
                Ap = np.vstack(([AA[i][:, :nvar] @ Gp[:, :-1] + AA[i][:, nvar:nvar+npar] for i in range(N)]))
                bp = np.hstack(([bi[i].reshape(-1) - AA[i][:, :nvar] @ Gp[:,npar] for i in range(N)]))
                x,r = chebyshev_center(Ap,bp)  # compute Chebyshev center
                if r>=1.e-6:                     
                    keep = np.sqrt(np.sum(Ap**2, axis=1)) > 1.e-10 # Remove possible rows of Ap with small norm
                    self.CRs.append({"Ath": Ap[keep,:], "bth": bp[keep], "z": Gp, "dim": 0, "x_cheby": x, "r_cheby": r, "combination": comb, "Ath_ext": None, "bth_ext": None, "gain_y": None, "Mx": Mx, "Mp": Mp[:,:-1], "M1": Mp[:,-1], "type": "unique"})
                    self.gains_CRs.append(gains)

            else:
                U2 = U[:,rank_Mx:]  
                if np.linalg.norm(U2.T@Mp) <= 1.e-12:
                    # Infinitely many solutions exist
                    
                    # Mx @ x = [U1,U2] @ diag(s) @ [V1';V2'] @x = Mp @ [p;1]
                    # Set y1=V1'@x and  y2=V2'@x -> x=V1@y1 + V2@y2
                    # diag(s1) @ V1' @ x = U1' @ Mp @ [p;1] -> y1 = diag(1/s1)@U1' @ Mp @ [p;1]
                    # diag(0)  @ V2' @ x = U2' @ Mp @ [p;1] -> y2 free
                    K1 = np.diag(1./s[:rank_Mx])@U[:,:rank_Mx].T@Mp # y1 = K1@[p;1], y2 free
                    Gp = np.hstack([Vt[:rank_Mx,:].T@K1[:,:npar],Vt[rank_Mx:,:].T,Vt[:rank_Mx,:].T@(K1[:,-1]).reshape(-1,1)]) # explicit solution x=Gp@[p;y2;1], y2 free
                    
                    # Ax+Bp<=b becomes: A@V1@y1 + A@V2@y2 + Bp <= b -> A@V1@K1@[p;1] + A@V2@[y2] + B[p] <= b
                    Ap_ext = np.vstack(([np.hstack((
                            AA[i][:, :nvar] @ Vt[:rank_Mx,:].T@K1[:,:npar] + AA[i][:, nvar:nvar+npar],
                            AA[i][:, :nvar] @ Vt[rank_Mx:,:].T)) for i in range(N)]))
                    bp_ext = np.hstack(([bi[i].reshape(-1) - AA[i][:, :nvar] @ Vt[:rank_Mx,:].T@K1[:,npar] for i in range(N)]))
                    
                    # Eliminate redundant constraints to avoid potential duplicate regions in mpQP solver
                    Ap_ext, bp_ext, _, _, _, _ = polyreduce(Ap_ext, bp_ext)
                    _,r = chebyshev_center(Ap_ext, bp_ext)  # compute Chebyschev center in (p, y2)-space
                    if r>=1.e-6: 
                      
                        # Project the polyhedron onto the p-space
                        n2 = nvar-rank_Mx
                        Ap, bp = project(Ap_ext, bp_ext, np.arange(npar, npar+n2))
                        x_proj, r_proj = chebyshev_center(Ap,bp)  # compute Chebyshev center
                        
                        if r_proj>=1.e-6: 
                            solve_mpQP2 = False
                            if self.split or self.variational:
                                if self.split:
                                    solve_mpQP2 = True
                                    # split region into subregions by finding suitable y2(p) functions
                                    pmin2, pmax2 = bounding_box(Ap,bp,pmin,pmax)
                                
                                if self.welfare:
                                    # Find welfare GNE which minimizes sum of costs of all agents
                                    # Objective of agent i : 1/2 x' Qi x + (ci+Fi p)' x
                                    # explicit solution x = Gp @ [p;y2;1]
                                    # Need to formulate objective in terms of y_2 : 
                                    # 1/2 y2' (Gp_y2' Qi Gp_y2) y2 + (Gp_y2' Qi Gp_1 + Gp_y2' ci)' y2 + p' (Gp_p' Qi Gp_y2 + Fi' Gp_y2) y2
                                    # with constraints
                                    # Ap_ext[:,npar:] @ y_2 ≤ bp_ext + Ap_ext[:,:npar] @ p
                                    
                                    # Extract blocks from Gp = [Gp_p | Gp_y2 | Gp_1]
                                    
                                    Gp_p = Gp[:, :npar] # (nx × npar)
                                    Gp_y2 = Gp[:, npar:npar+n2] # (nx × n2)
                                    Gp_1 = Gp[:, -1:].flatten() # # (nx,)

                                    H = np.zeros((n2, n2))
                                    f = np.zeros(n2)
                                    F = np.zeros((n2, npar))
                                    
                                    for i in range(N):
                                        H += Gp_y2.T @ self.Q[i] @ Gp_y2
                                        f += Gp_y2.T @ (self.Q[i] @ Gp_1 + self.c[i].flatten())  # constant term: f = sum_i(Gp_y2' * (Qi * Gp_1 + ci))
                                        F += Gp_y2.T @ (self.Q[i] @ Gp_p + self.F[i]) # parametric term
      
                                    mpQP2 = MPQP(H, f, F, Ap_ext[:,npar:], bp_ext, -Ap_ext[:,:npar], pmin2, pmax2)
  
                                if self.min_norm:
                                     # Find the y2 with minimum norm          
                                     mpQP2 = MPQP(np.eye(n2), np.zeros(n2), np.zeros((n2,npar)), Ap_ext[:,npar:], bp_ext, -Ap_ext[:,:npar], pmin2, pmax2)
                                     
                                if self.variational or self.variational_split:
                                
                                    # Check if a variational GNE solution exists and, if it does, split region so that a full subregion of vGNE solution is characterized, by minimizing the distance between dual variables of agents.
                                    
                                    Mx2 = list()
                                    Mp2 = list()

                                    if self.variational_split:
                                        H = np.zeros((n2, n2))
                                        F = np.zeros((n2, npar))
                                        f = np.zeros((n2, 1))

                                    # Matrix G_act contains info about which constraints are active for each agent. As consistency of active shared constraints among agents was already checked above, if a row of G_act has at least two True values, the corresponding constraint is an active shared one
                                    
                                    for c in range(ncon):
                                        if sum(G_act[c,:])<2:
                                            continue # not a shared active constraint
                                        Ic= np.where(G_act[c,:])[0] # indices of agents sharing active constraint c
                                        i1=Ic[0]
                                        
                                        # Lambda_i1 = Klambda_i1 @ [x(-i1);p;y2] + klambda_i1
                                        Klambda_i1 = mpQPs[i1].CRs[comb[i1]].Klambda[c]
                                        klambda_i1 = mpQPs[i1].CRs[comb[i1]].klambda[c]
                                        _, nisi1 = get_indices(i1, dim, nvar)
                                        n1 = len(nisi1) # dim(x(-i1))

                                        for jx in range(1, len(Ic)):
                                            j = Ic[jx]
                                            # Lambda_j = Klambda_i1 @ [x(-j);p;y2] + klambda_j
                                            Klambda_j = mpQPs[j].CRs[comb[j]].Klambda[c] 
                                            klambda_j = mpQPs[j].CRs[comb[j]].klambda[c]
                                            _, nisj = get_indices(j, dim, nvar)
                                            nj = len(nisj) # dim(x(-j))
                                            
                                            # Impose Lambda_i1 - Lambda_j = 0
                                            Mxrow = np.zeros(nvar)
                                            Mprow = np.zeros(npar+1)
                                            Mxrow[nisi1] = Klambda_i1[:n1]
                                            Mxrow[nisj] -= Klambda_j[:nj]
                                            Mprow[:npar] = -Klambda_i1[n1:] + Klambda_j[nj:]
                                            Mprow[-1] = -klambda_i1 + klambda_j
                                                      
                                            Mx2.append(Mxrow.reshape(1,-1))
                                            Mp2.append(Mprow.reshape(1,-1))
                                            
                                            if self.variational_split:
                                                # Build objective to minimize the difference between dual variables
                                                Lambda_y2_diff = (Klambda_i1[:n1] @ Gp[nisi1, npar:npar+n2] - Klambda_j[:nj] @ Gp[nisj, npar:npar+n2]).reshape(1,-1)
                                                
                                                Lambda_p_diff = (Klambda_i1[:n1] @ Gp[nisi1, :npar] + Klambda_i1[n1:] - Klambda_j[:nj] @ Gp[nisj, :npar] - Klambda_j[nj:]).reshape(1,-1)                                                                   
                                                Lambda_const_diff = (Klambda_i1[:n1] @ Gp[nisi1, -1] + klambda_i1 - Klambda_j[:nj] @ Gp[nisj, -1] - klambda_j).reshape(1,)

                                                H += Lambda_y2_diff.T @ Lambda_y2_diff
                                                F += Lambda_y2_diff.T @ Lambda_p_diff
                                                f += Lambda_y2_diff.T @ Lambda_const_diff.reshape(-1, 1)
                                        
                                    # Solve equilibrium condition with additional constraints Lambda_i1 - Lambda_j = 0 for all j in Ic
                                    Mx2 = np.vstack(Mx2)
                                    Mp2 = np.vstack(Mp2)
                                    Mx2 = np.vstack((Mx, Mx2))
                                    Mp2 = np.vstack((Mp, Mp2))
                                    
                                    U,s,Vt = np.linalg.svd(Mx2)
                                    rank_Mx2 = np.sum(s >= 1.e-6)  
                                    if rank_Mx2==nvar:
                                        if not self.split:
                                            # Unique variational GNE solution
                                            # Mx2*x = U*[diag(s);0]@Vt*x = Mp2
                                            # Set y=Vt*x -> diag(s)@y = U[:,:nvar].T@Mp2 -> y = diag(1/s)@U[:,:nvar].T@Mp2 -> x=Vt.T@y
                                            Gp2 = Vt.T@np.diag(1./s)@U[:,:nvar].T@Mp2 # explicit solution x=Gp2*[p;1]
                                            # Critical region for the parametric Nash equilibrium
                                            # A[:,:nvar]@Gp2@[p;1] + A[:,nvar:nvar+npar]@p <= bb
                                            Ap2 = np.vstack(([AA[i][:, :nvar] @ Gp2[:, :-1] + AA[i][:, nvar:nvar+npar] for i in range(N)]))
                                            bp2 = np.hstack(([bi[i].reshape(-1) - AA[i][:, :nvar] @ Gp2[:,npar] for i in range(N)]))
                                            solve_mpQP2 = False
                                            
                                    elif rank_Mx2 < nvar:
                                        U2 = U[:,rank_Mx2:]  
                                        if np.linalg.norm(U2.T@Mp2) <= 1.e-12: 
                                            print("\033[1;31mWarning: infinitely many vGNE solutions detected. CASE NOT FULLY IMPLEMENTED YET. Region is not split.\033[0m")
                                            solve_mpQP2 = False 
                                    else:
                                        # Don't split region
                                        solve_mpQP2 = False                        
                                    
                                    if solve_mpQP2:
                                        # Solve variational GNE
                                        mpQP2 = MPQP(H, f,  F, Ap_ext[:,npar:], bp_ext, -Ap_ext[:,:npar], pmin2, pmax2)
                                    else:
                                        Ap2 = np.vstack((Ap, Ap2))
                                        bp2 = np.hstack((bp, bp2))
                                        Ap2, bp2, _, _, _, _ = polyreduce(Ap2, bp2)
                                        x,r = chebyshev_center(Ap2,bp2)  # compute Chebyshev center
                                        if r>=1.e-6:
                                            self.CRs.append({"Ath": Ap2, "bth": bp2, "z": Gp2, "dim": 0, "x_cheby": x, "r_cheby": r, "combination": comb, "Ath_ext": None, "bth_ext": None, "gain_y": None, "Mx": Mx2, "Mp": Mp2[:,:-1], "M1": Mp2[:,-1],
                                                  "type": "variational"})
                                        self.gains_CRs.append(gains)

                                if solve_mpQP2:
                                    mpQP2.solve()
                                        
                                    #Intersects each critical region of mpQP2 with (Ap,bp)
                                    for k in range(len(mpQP2.CRs)):
                                        Ap2 = mpQP2.CRs[k].Ath
                                        bp2 = mpQP2.CRs[k].bth
                                        # Intersect the two polyhedra
                                        Ap2 = np.vstack((Ap, Ap2))
                                        bp2 = np.hstack((bp, bp2))
                                        Ap2, bp2, _, _, _, _ = polyreduce(Ap2, bp2)
                                        x,r = chebyshev_center(Ap2,bp2)  # compute Chebyshev center
                                        if r>=1.e-6:
                                            # explicit solution x=Gp@[p;y2;1], y2=mpQP2.CRs[k].z[p;1]
                                            gain2 = Gp[:,npar:npar+n2].reshape(nvar,n2)@mpQP2.CRs[k].z
                                            gain2[:,0:npar] += Gp[:,:npar]
                                            gain2[:,-1] += Gp[:,-1] 
                                            
                                            CR = {"Ath": Ap2, "bth": bp2, "z": gain2, "dim": 0, "x_cheby": x, "r_cheby": r, "combination": comb, "Ath_ext": None, "bth_ext": None, "gain_y": None, "Mx": Mx, "Mp": Mp[:,:-1], "M1": Mp[:,-1],}
                                            if self.min_norm or self.welfare:
                                                CR["type"] = self.split_method
                                            else:
                                                # self.variational is True
                                                if len(mpQP2.CRs[k].AS)==0:
                                                    # unconstrained region of mpQP2
                                                    CR["type"] = "variational"
                                                    CR["Mx"]=Mx2
                                                    CR["Mp"]=Mp2[:,:-1]
                                                    CR["M1"]=Mp2[:,-1],
                                                else:
                                                    # keep infinitely-many solutions, as defined in entire region before splitting
                                                    CR["type"] = "infinitely-many"
                                                    ii = list(range(npar)) + [npar+n2]
                                                    gain = Gp[:,ii].reshape(nvar,npar+1) 
                                                    gain_y = Gp[:,npar:npar+n2].reshape(nvar,n2) 
                                                    CR["z"]=gain
                                                    CR["dim"]=n2
                                                    CR["gain_y"] = gain_y
                                                    # intersect (Ap_ext,bp_ext) with the new region in p-space to define Ath_ext, bth_ext
                                                    Ath_ext = np.vstack((Ap_ext, np.hstack((CR["Ath"],np.zeros((CR["Ath"].shape[0],n2))))))
                                                    bth_ext = np.hstack((bp_ext, CR["bth"]))
                                                    Ath_ext, bth_ext, _, _, _, _ = polyreduce(Ath_ext, bth_ext)
                                                    CR["Ath_ext"]=Ath_ext
                                                    CR["bth_ext"]=bth_ext
                                            
                                            self.CRs.append(CR)
                                            self.gains_CRs.append(gains)                                    
                               
                            if not solve_mpQP2:
                                # Keep entire region, no splitting
                                ii = list(range(npar)) + [npar+n2]
                                gain = Gp[:,ii].reshape(nvar,npar+1) # explicit solution x=gain@[p;1]+gain_y@y2
                                gain_y = Gp[:,npar:npar+n2].reshape(nvar,n2)                                 
                                self.CRs.append({"Ath": Ap, "bth": bp, "z": gain, "dim": n2, "x_cheby": x_proj, "r_cheby": r_proj, "combination": comb, "Ath_ext": Ap_ext, "bth_ext": bp_ext, "gain_y": gain_y, "Mx": Mx, "Mp": Mp[:,:-1], "M1": Mp[:,-1], "type": "infinitely-many"})
                                self.gains_CRs.append(gains)
        self.nr = len(self.CRs)
        elapsed_time = time.time() - elapsed_time
        vprint(f"\nNash equilibria explicit solution computed in {elapsed_time:.2f} seconds.")
        self.elapsed_time = elapsed_time
        return
    
    def statistics(self):
        """ Statistics on the explicit solution
        """
       
        is_unique = [self.CRs[i]["type"]=='unique' for i in range(len(self.CRs))] 
        is_variational = [self.CRs[i]["type"]=='variational' for i in range(len(self.CRs))] 
        is_variational_split = [self.CRs[i]["type"]=='variational-split' for i in range(len(self.CRs))] 
        is_infmany = [self.CRs[i]["type"]=='infinitely-many' for i in range(len(self.CRs))]
        is_welfare = [self.CRs[i]["type"]=='welfare' for i in range(len(self.CRs))]
        is_minnorm = [self.CRs[i]["type"]=='min-norm' for i in range(len(self.CRs))]
        
        msg = f"\n\033[1mTotal number of critical regions in \u211D^{self.npar} for Nash equilibria:{len(self.CRs): 4d}\033[0m\n"
        msg += "-"*65

        if any(is_unique)>0:
            msg += f"\nNumber of critical regions with unique solution:            {np.sum(is_unique): 4d}"
        if any(is_variational)>0:
            msg += f"\nNumber of critical regions with variational GNE solution:   {np.sum(is_variational): 4d}"
        if any(is_infmany)>0:
            msg += f"\nNumber of critical regions with infinitely-many solutions:  {np.sum(is_infmany): 4d}"
        if any(is_variational_split)>0:
            msg += f"\nNumber of critical regions with variational GNE (+split):   {np.sum(is_variational_split): 4d}"
        if any(is_minnorm)>0:
            msg += f"\nNumber of critical regions with min-norm GNE solution:      {np.sum(is_minnorm): 4d}"
        if any(is_welfare)>0:
            msg += f"\nNumber of critical regions with welfare GNE solution:       {np.sum(is_welfare): 4d}"
        return msg

    def plot_2d(self, show_centers = False, show_circles = False, show_legend = False, colors = None):
        """ Plots the critical regions for Nash equilibria in the 2-dimensional parameter space
        """
        if not self.npar==2:
            raise ValueError("plot_2d can be used only for 2-dimensional parameter space.")
        
        if show_legend and not show_centers:
            show_centers = True  # need to show centers to have legend entries
            print("Warning: show_centers set to True to enable legend display.")
            
        if colors is None:
            colors = np.random.rand(self.nr,3)
        else:
            colors = np.array(colors)
            if colors.shape[0]<self.nr:
                # not enough colors provided, pad with random colors
                n_missing = self.nr - colors.shape[0]
                random_colors = np.random.rand(n_missing,3)
                colors = np.vstack((colors, random_colors))
        
        ax = plt.gca()
        for i in range(self.nr):
            thecolor = colors[i]
            polyplot(A=self.CRs[i]["Ath"], b=self.CRs[i]["bth"], lb=self.pmin, ub=self.pmax, alpha=0.3, color=thecolor)
            
            if show_centers:
                match self.CRs[i]["type"]:
                    case "unique":
                        label = "1"
                    case "variational":
                        label = "$\lambda$"
                    case "infinitely-many":
                        label = "$\infty$"
                    case "min-norm":
                        label = "min"
                    case "welfare":
                        label = "welfare"
                x_cheby = self.CRs[i]["x_cheby"]
                ax.scatter(x_cheby[0], x_cheby[1], color=thecolor, marker='o', s=60, zorder=10)
                ax.scatter(x_cheby[0], x_cheby[1], color=thecolor, marker='s', s=25, label=f"$CR_{{{i+1}}}$ ({label})", zorder=10)

            if show_circles:
                circle = plt.Circle((x_cheby[0], x_cheby[1]), self.CRs[i]["r_cheby"], fill=False, linewidth=1., color=thecolor, 
                            zorder=2, linestyle='--')
                ax.add_patch(circle)

        ax.grid()
        ax.set_xlabel("$p_1$")
        ax.set_ylabel("$p_2$")
        ax.set_title("Critical regions for Nash equilibria")

        if show_legend:
            ax.legend(loc="upper right")

    def check_nash_equilibria(self):
        """ Check if solutions are indeed Nash equilibria by evaluating the best responses at the Chebyshev centers
        """
        
        CRs = self.CRs
        npar = self.npar
        dim = self.dim
        Q = self.Q
        c = self.c
        F = self.F
        A = self.A
        b = self.b
        S = self.S  
                
        for k in range(self.nr):
            p = CRs[k]["x_cheby"][:npar]
            comb = CRs[k]["combination"]
            print(f"\n\033[37;44mRegion #{k} ({CRs[k]['type']}): center p = {np.round(p, decimals=4)} (mpQP combination: {comb})\033[0m")

            x = (CRs[k]["z"][:,:-1].reshape(-1,npar)@p.reshape(npar,1) + CRs[k]["z"][:,-1].reshape(-1,1)).reshape(-1) # predicted multiparametric solution
            
            if CRs[k]["dim"]>0:
                # Convert polyhedron in (p,y2)-space to interval {Ay*y2<=by} in y2-space after fixing p
                Ay = CRs[k]["Ath_ext"][:,npar:]  # A[p,y2]
                by = CRs[k]["bth_ext"].reshape(-1) - (CRs[k]["Ath_ext"][:,:npar]@p).reshape(-1)
                Ay, by, _, _, _, _ = polyreduce(Ay, by)
                y2, _ = chebyshev_center(Ay, by)  # compute Chebyshev center in y2-space
                x += (CRs[k]["gain_y"]@y2).reshape(-1) 
                
            for i in range(self.N):
                isi, nisi = get_indices(i, dim, self.nvar)
                sol = daqp.solve(Q[i][isi][:,isi].reshape(dim[i],dim[i]),
                        (c[i][isi] + F[i][isi, :] @ p + Q[i][isi][:,nisi]@x[nisi]).reshape(-1),
                        A[:, isi], b + S @ p -A[:,nisi]@x[nisi])
                xi = sol[0]
                lam = sol[3]["lam"]

                print(f"agent #{i}: explicit / QP = {np.round(x[isi].reshape(-1), decimals=4)} <-> {np.round(xi.reshape(-1), decimals=4)}", end="")
                if CRs[k]["type"]=="variational":
                    print(f", lambda = {np.round(lam.reshape(-1), decimals=4)}") #, X_BRexp({i}) = {x_BR[i]: .4f}")
                else:
                    print("")
            
    def find_critical_region(self, p, tol=1e-9):
        """ Find the index (or indices) of the critical region containing a given parameter p.
        """
        p = np.array(p).flatten()        

        viol = [np.max(region['Ath']@ p-region['bth']) for region in self.CRs]
        return [i for i,v in enumerate(viol) if v <= tol]

    def save(self, filename):
        """ Save NashMPQP object to a file
        """
        with gzip.open(filename, "wb") as f:
            dill.dump(self, f)
        
    @classmethod
    def load(cls,filename):
        """ Load NashMPQP object from a file
        """
        with gzip.open(filename, "rb") as f:
            obj = dill.load(f)
        if not isinstance(obj, cls):
            raise TypeError(f"Expected {cls.__name__}, got {type(obj).__name__}")
        return obj
