"""
Polynomial terms generation for Cointegrating Polynomial Regressions.

This module provides functions to generate polynomial powers of integrated
regressors and the corresponding correction terms required for FM-OLS
estimation.

Author: Dr Merwan Roudane
Email: merwanroudane920@gmail.com
"""

import numpy as np
from typing import Union, List, Dict, Optional, Any
from dataclasses import dataclass


@dataclass
class PolyTermsResult:
    """
    Result container for polynomial terms generation.
    
    Attributes
    ----------
    X : np.ndarray
        Matrix of polynomial terms (T x sum of orders)
    Mstar : np.ndarray
        Correction terms vector (before multiplying by Delta+)
    P : np.ndarray
        Index vector with cumulative column counts for each regressor
    """
    X: np.ndarray
    Mstar: np.ndarray
    P: np.ndarray


def gen_power_reg(x: np.ndarray, all_powers: str, powvec: Union[int, np.ndarray]) -> np.ndarray:
    """
    Generate matrix of powers of a scalar input regressor.
    
    Parameters
    ----------
    x : np.ndarray
        Single regressor vector of shape (T,) or (T, 1)
    all_powers : str
        If 'yes', all powers from 1 to powvec (which is scalar) are returned.
        If 'no', only the powers specified in powvec (which is a vector) are returned.
    powvec : int or np.ndarray
        If all_powers == 'yes': scalar indicating maximum power
        If all_powers == 'no': vector of specific powers to include
    
    Returns
    -------
    np.ndarray
        Matrix of shape (T, NumPow) with specified powers
    
    Examples
    --------
    >>> x = np.array([1, 2, 3, 4, 5])
    >>> gen_power_reg(x, 'yes', 3)  # Returns [x, x^2, x^3]
    >>> gen_power_reg(x, 'no', np.array([1, 3]))  # Returns [x, x^3]
    """
    x = np.asarray(x).flatten()
    T = len(x)
    
    if isinstance(powvec, (int, np.integer)):
        powvec_arr = np.array([powvec])
    else:
        powvec_arr = np.asarray(powvec).flatten()
    
    if all_powers == 'yes':
        max_pow = int(powvec_arr[0])
        power_reg = np.zeros((T, max_pow))
        power_reg[:, 0] = x
        for j in range(1, max_pow):
            power_reg[:, j] = power_reg[:, j - 1] * x
    elif all_powers == 'no':
        num_pow = len(powvec_arr)
        power_reg = np.zeros((T, num_pow))
        for j, p in enumerate(powvec_arr):
            power_reg[:, j] = x ** p
    else:
        raise ValueError(f"all_powers must be 'yes' or 'no', got {all_powers}")
    
    return power_reg


def gen_cpr_corr_vec(x: np.ndarray, all_powers: str, powvec: Union[int, np.ndarray]) -> np.ndarray:
    """
    Generate correction terms for FM-OLS estimation in CPR.
    
    Parameters
    ----------
    x : np.ndarray
        Single regressor vector of shape (T,) or (T, 1)
    all_powers : str
        If 'yes', correction terms for powers 1 to powvec are returned.
        If 'no', correction terms for specified powers in powvec are returned.
    powvec : int or np.ndarray
        Power specification (scalar max or vector of specific powers)
    
    Returns
    -------
    np.ndarray
        Column vector of correction terms corresponding to powers
        (1: T, 2: 2*sum(x_t), 3: 3*sum(x_t^2), etc.)
    
    Notes
    -----
    The correction term for power p is: p * sum(x_t^{p-1})
    These terms are used in the FM-OLS correction, multiplied by Delta+.
    """
    x = np.asarray(x).flatten()
    T = len(x)
    
    if isinstance(powvec, (int, np.integer)):
        powvec_arr = np.array([powvec])
    else:
        powvec_arr = np.asarray(powvec).flatten()
    
    if len(powvec_arr) == 0:
        return np.array([])
    
    if all_powers == 'yes':
        numpow = int(powvec_arr[0])
        maxpower = numpow
        selected_powers = np.arange(1, maxpower + 1)
    elif all_powers == 'no':
        numpow = len(powvec_arr)
        maxpower = int(np.max(powvec_arr))
        selected_powers = powvec_arr
    else:
        raise ValueError(f"all_powers must be 'yes' or 'no', got {all_powers}")
    
    # Compute powers of regressor
    # sum_matrix[:, j] = x^j
    sum_matrix = np.ones((T, maxpower))
    if maxpower >= 2:
        sum_matrix[:, 1] = x
        for j in range(2, maxpower):
            sum_matrix[:, j] = sum_matrix[:, j - 1] * x
    
    # Compute sums of powers: sum(x^0), sum(x^1), ..., sum(x^{maxpower-1})
    sum_vec = np.sum(sum_matrix, axis=0)
    
    # Multiply by "p" scalar (the power index)
    prevec = np.arange(1, maxpower + 1)
    full_vec = prevec * sum_vec
    
    # Select relevant elements
    if all_powers == 'yes':
        corr_term = full_vec
    else:
        corr_term = np.array([full_vec[int(p) - 1] for p in selected_powers])
    
    return corr_term


def gen_var_poly_terms(x: np.ndarray, orders: Union[int, List[int], List[np.ndarray]], 
                       stochastic: bool = True) -> PolyTermsResult:
    """
    Construct polynomial regressors and correction terms for CPR.
    
    Parameters
    ----------
    x : np.ndarray
        Matrix of integrated regressors (T x m)
    orders : int, list of int, or list of arrays
        Polynomial orders specification:
        - If scalar: all regressors have the same max order
        - If list of int: different max orders for each regressor
        - If list of arrays: specific powers for each regressor
    stochastic : bool, optional
        If True (default), compute correction terms for stochastic case.
        If False, only generate polynomial terms (deterministic case).
    
    Returns
    -------
    PolyTermsResult
        Dataclass with:
        - X: (T x k) matrix of polynomial terms
        - Mstar: (k,) vector of correction terms (empty if stochastic=False)
        - P: Index vector with cumulative column counts
    
    Examples
    --------
    >>> x = np.random.randn(100, 2)
    >>> # All regressors with max power 2
    >>> result = gen_var_poly_terms(x, 2)
    >>> # Different max powers
    >>> result = gen_var_poly_terms(x, [2, 3])
    >>> # Specific powers for each regressor
    >>> result = gen_var_poly_terms(x, [np.array([1, 2]), np.array([1, 3])])
    """
    x = np.atleast_2d(x)
    if x.ndim == 1:
        x = x.reshape(-1, 1)
    T, m = x.shape
    
    # Determine if orders is a cell array (list of arrays) or scalar/vector
    is_cell = isinstance(orders, list) and len(orders) > 0 and isinstance(orders[0], np.ndarray)
    
    if stochastic:
        if not is_cell:
            # Convert to array
            if isinstance(orders, (int, np.integer)):
                orderind = np.ones(m, dtype=int) * int(orders)
            else:
                orderind = np.array(orders, dtype=int).flatten()
            
            X_parts = []
            Mstar_parts = []
            
            if m == 1 and not isinstance(orders, (int, np.integer)):
                # Single regressor with specific powers
                X = gen_power_reg(x[:, 0], 'no', orderind)
                Mstar = gen_cpr_corr_vec(x[:, 0], 'no', orderind)
                P = np.array([0, len(orderind)])
            else:
                for i in range(m):
                    X_i = gen_power_reg(x[:, i], 'yes', orderind[i])
                    X_parts.append(X_i)
                    Mstar_i = gen_cpr_corr_vec(x[:, i], 'yes', orderind[i])
                    Mstar_parts.append(Mstar_i)
                
                X = np.hstack(X_parts)
                Mstar = np.concatenate(Mstar_parts)
                P = np.concatenate([[0], np.cumsum(orderind)])
        else:
            # Cell array: individually different orders
            X_parts = []
            Mstar_parts = []
            P = [0]
            
            for i in range(m):
                orderind = np.asarray(orders[i]).flatten()
                X_i = gen_power_reg(x[:, i], 'no', orderind)
                X_parts.append(X_i)
                Mstar_i = gen_cpr_corr_vec(x[:, i], 'no', orderind)
                Mstar_parts.append(Mstar_i)
                P.append(P[-1] + len(orderind))
            
            X = np.hstack(X_parts)
            Mstar = np.concatenate(Mstar_parts)
            P = np.array(P)
    else:
        # Deterministic polynomial case
        if not is_cell:
            if isinstance(orders, (int, np.integer)):
                orderind = np.ones(m, dtype=int) * int(orders)
            else:
                orderind = np.array(orders, dtype=int).flatten()
            
            X_parts = []
            for i in range(m):
                X_i = gen_power_reg(x[:, i], 'yes', orderind[i])
                X_parts.append(X_i)
            
            X = np.hstack(X_parts)
            P = np.concatenate([[0], np.cumsum(orderind)])
        else:
            X_parts = []
            P = [0]
            
            for i in range(m):
                orderind = np.asarray(orders[i]).flatten()
                X_i = gen_power_reg(x[:, i], 'no', orderind)
                X_parts.append(X_i)
                P.append(P[-1] + len(orderind))
            
            X = np.hstack(X_parts)
            P = np.array(P)
        
        Mstar = np.array([])
    
    return PolyTermsResult(X=X, Mstar=Mstar, P=P)
