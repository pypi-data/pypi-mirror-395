"""
Joint Auto Wighted Graph Fusion from Bahrami et al., 2020

https://www.sciencedirect.com/science/article/pii/S1566253520303687

By James McIntyre
Tufts' Jean Mayer USDA Human Nutrition Research Center on Aging (HNRCA)
Precision Nutrition Group

"""

import numpy as np
from scipy.sparse._csr import csr_matrix
from scipy.sparse.csgraph import laplacian
from sklearn.neighbors import kneighbors_graph
import scipy.sparse as sp
from scipy.sparse.linalg import inv, spsolve



def custom_distance(x, y, eps=1e-8):
    """Custom kernel for creating the label affinity matrix from eq. 19
    Using pearson correlation between two nodes as the similarity metric
    

    Args:
        x (array): array of labels, shape (1, n_classes), binary one-hot encoded, all 0s for unlabeled samples
        y (array): array of labels, shape (1, n_classes), binary one-hot encoded, all 0s for unlabeled samples

    Returns:
        correlation (float): pearson correlation value from eq 19
    """

    # center each vector: f_qi - mean(f_i)
    xc = x - x.mean()
    yc = y - y.mean()

    # get num and denom for eq 19
    num = np.dot(xc, yc)
    denom = np.dot(np.linalg.norm(xc), np.linalg.norm(yc)) + eps  # avoid /0
    corr = num / denom             # Pearson correlation in [-1, 1]

    # return the correlation value as distance
    return 1-corr



def fme_solve(X_concat, Y, L_tilde, U, mu=1.0, gamma=1.0, lambd=1.0):
    """Single FME step (Eqs. 6–8)

    Args:
        X (csr matrix): concatenated features across all views (rows = samples)
        Y (array): label matrix (one-hot for labeled, zeros for unlabeled)
        L_tilde (csr matrix): fused Laplacian
        U (csr matrix), diagonal matrix with 1 for labelled rows and 0 for unlabelled 
        mu (float, optional): _description_. Defaults to 1.
        gamma (float, optional): _description_. Defaults to 1.

    Returns:
        _type_: _description_
    """

    N, D = X_concat.shape
    # treat data as X (d x N)
    X = X_concat.T  # D x N

    # H_c (N x N), X_c = X H_c (d x N)
    I = sp.identity(N)
    ones = sp.csr_matrix(np.ones(N)).T
    Hc = I - (1.0 / N) * (ones @ ones.T)

    # X_c (centered matrix)
    Xc = X@Hc

    # M = X_c^T X_c (γ X_c^T X_c + I)^(-1)   (N x N)
    XtX = Xc.T @ Xc           
    A1  = (gamma * XtX + I).tocsc()
    # Solve A1 * Z = XtX  (matrix right-hand side)
    M = spsolve(A1, XtX.tocsc())    # Z has shape (N, N) dense or sparse

    # F from Eq. (8): (U + L_hat + μγH_c - μγ^2 M) F = U Y
    A2 = (U + lambd * L_tilde + (mu * gamma * Hc) - (mu * gamma**2 * M)).tocsc()
    F  = spsolve(A2, U @ Y)   # solves A2 * F = UY

    # Q from Eq. (6): Q = γ [γ XH_cX^T + I]^(-1) XH_cF
    Q = gamma * inv(gamma * X@Hc@X.T + sp.identity(D)) @ X @ Hc @ F

    # # b from Eq. (7): b = 1/N (F^T 1 - Q^T X 1)
    b = 1/N * ( F.T @ ones - Q.T@X@ones )    # C x 1

    # change to csr matrices for memory optimization
    return F, csr_matrix(Q), csr_matrix(b)



def joint_fusion(X_list, Y, K = 30, gamma = 1.0, mu = 1.0, lambd = 1.0, p = 2, tol = 0.001 , max_iter = 1000):
    """Joint Auto Weighted Graph Fusion 
    as described in (Bahrami et al., 2020)
    https://www.sciencedirect.com/science/article/pii/S1566253520303687

    Args:
        X_list (list of arrays): list of feature matrices to concatenate, each in the shape (n_samples, n_features).
        Y (array): array of labels, shape (n_samples, n_classes), binary one-hot encoded, all 0s for unlabeled samples.
        K (int, optional): number of neighbors for label affinity matrix, None for fully connected. Defaults to 30.
        gamma (float, optional): Flexible Manifold Embedding regularization parameter. Defaults to 1. 
        mu (float, optional): Weight of Flexible Manifold Embedding projection term. Defaults to 1.
        lamd (float, optional): Weight of the graph smoothness term. Defaults to 1.
        p (float, optional): Exponent in the auto-weighting scheme for view coefficients. Must be > 1. Defaults to 2.
        tol (float, optional): Convergence tolerance for the change in view weights during the main loop. Loop stops when below this value. Defaults to 0.001.
        max_iter (int, optional): Maximum iterations allowed before stopping

    Returns:
        F (array): Soft label matrix for unlabeled points
        Q (csr_matrix): Projection matrix for labelling unseen points
        b (csr_matrix): bias matrix for labelling unseen points
    """
    

    # create X_c by concatenating all features
    X_concat = sp.csr_matrix(np.concatenate(X_list, axis=1))

    
    # set up U (diagonal with 1 for labelled nodes and 0 for unlabelled)
    unlabelled_bool = np.all(Y==0, axis=1)
    labelled_bool = (~unlabelled_bool).astype(int)
    U = sp.diags(labelled_bool)


    ########################################
    ### 1. Construct V similarity graphs ###
    ########################################


    # fully connected if K is none
    if K is None: K=len(Y)
    # initialize Aff matrix list
    W_list = []
    # loop through feature 'views'
    for X in X_list:
        # construct distance matrix
        similarity_graph = kneighbors_graph(X, n_neighbors=K, mode='distance', metric='cosine', include_self=True, n_jobs=-1)
        # get similarity from distance
        similarity_graph.data = 1-similarity_graph.data
        # make symmetric 
        similarity_graph = 0.5 * (similarity_graph + similarity_graph.T)
        # append similarity matrix to list of matrices
        W_list.append(similarity_graph)


    #######################################
    ### 2. Compute V laplacian matrices ###
    #######################################


    # Initialize Laplacian matrix list
    L_list = []
    # loop through affinity matrix 'views'
    for W in W_list:
        L = laplacian(W)
        L_list.append(L)
    # append a placeholder for the label laplacian to the list
    L_list.append(np.nan)

    
    ##################################################
    ### 3. Initialize the coefficient of each view ###
    ##################################################


    # intialize coefficients for each view (at 1/V+1)
    # +1 here is for the label view
    av = [1/(len(W_list)+1)]*(len(W_list)+1)
    av = np.array(av)
    assert len(av) == len(L_list), "Coefficient list length mismatch"


    ############################################
    ### 4. Intialize soft label matrix F = Y ###
    ############################################
    

    F = Y.copy()


    ##############
    ### Repeat ###
    ##############


    # set a maximum iteration
    under_max_iter = True
    current_iter = 0

    # set up dummy previous a for convergence check
    a_prev = np.array([1]*len(av))
    # repeat until convergence
    while np.abs(av - a_prev).sum() > tol and under_max_iter:

        current_iter += 1

        
        ##################################################    
        ### Generate correlation graph from F (eq. 19) ###
        ##################################################


        # Using the same K as before
        # distance matrix using custom distance function ( pearson correlation between two nodes as the similarity metric)
        W_corr = kneighbors_graph(F, n_neighbors=K, mode='distance', metric=custom_distance, include_self=True, n_jobs=-1)
        # change distance back to similarity, this is so the K cut off doesnt cut off the wrong side (larger similarities)
        W_corr.data = 1 - W_corr.data
        # make symmetric 
        W_corr = 0.5 * (W_corr + W_corr.T)
        # get the laplacian of the label correlation graph
        L_corr = laplacian(W_corr)
        # append the label laplacian to the list
        L_list[-1] = L_corr


        ################################################################
        ### Fuse the V+1 laplacian graphs to obtain L_tilde (eq. 20) ###
        ################################################################
        

        # weighted sum of laplaians with coefficients
        # Excluding p from the corr matrices, as eq 20 shows
        Vcount = len(L_list) - 1
        a_corr = av[-1]
        L_corr = L_list[-1]
        L_tilde = sum(av[v]**p * L_list[v] for v in range(Vcount)) + a_corr * L_corr


        ###########################################
        ### Calculate Q, b and F (eqs. 6, 7, 8) ###
        ###########################################


        F, Q, b = fme_solve(X_concat, Y, L_tilde, U, mu=mu, gamma=gamma, lambd=lambd)

        
        ######################################
        ### Update coefficients a (eq. 18) ###
        ######################################


        # save coefficients from last loop
        a_prev = av.copy()

        # eq 18
        Cvs = []
        for v, L in enumerate(L_list):
            Cv = float((F.T@L@F).trace())
            Cvs.append(Cv)
        
        for v, a in enumerate(av):
            pp = 1/(p-1)
            num = 1/(Cvs[v]**pp)
            denom = sum((1/Cv)**pp for Cv in Cvs)
            av[v] = num/denom
            
        if current_iter > max_iter:
            under_max_iter = False
            print('maximum iterations reached')


    ##################################################################
    ### 5. Use soft label matrix as the label of unlabeled samples ###
    ##################################################################


    # return soft label matrix, F, the projection matrix Q, and bias vector b
    return F, Q, b





################################################################################################
### 6. Use projection matrix Q and the bias vector b to estimate the label of unseen samples ###
################################################################################################


def predict(new_sample, Q, b):
    """Generate new sample prediction from Q and b using eq. 21

    Args:
        new_sample (csr_matrix): csr matrix of shape 1 x n_features (concatenated)
        Q (csr_matrix): Projection matrix
        b (csr_matrix): _description_

    Returns:
        array: soft label matrix from new unseen sample
    """

    # predict new sample's label using eq. 21
    prediction = new_sample @ Q + b.T

    # return the soft label prediction
    return prediction.data