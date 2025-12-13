import numpy as np
import ast

def parse_matrix(matrix_str):
  
    try:
  
        matrix_list = ast.literal_eval(matrix_str)
        if isinstance(matrix_list, list):
             return np.array(matrix_list)
    
        if isinstance(matrix_list, tuple):
             return np.array(matrix_list)
    except:
        pass
    
   
    try:
        if not matrix_str.strip().startswith("[["):
             matrix_str = f"[{matrix_str}]"
        matrix_list = ast.literal_eval(matrix_str)
        return np.array(matrix_list)
    except Exception as e:
        raise ValueError(f"Invalid matrix format: {e}")

def mul(m1_str, m2_str):
    m1 = parse_matrix(m1_str)
    m2 = parse_matrix(m2_str)
    return np.matmul(m1, m2)

def det(m_str):
    m = parse_matrix(m_str)
    return np.linalg.det(m)

def inv(m_str):
    m = parse_matrix(m_str)
    return np.linalg.inv(m)

def eig(m_str):
    m = parse_matrix(m_str)
    w, v = np.linalg.eig(m)
    return f"Eigenvalues:\n{w}\n\nEigenvectors:\n{v}"

def transpose(m_str):
    m = parse_matrix(m_str)
    return m.T

def rank(m_str):
    m = parse_matrix(m_str)
    return np.linalg.matrix_rank(m)
