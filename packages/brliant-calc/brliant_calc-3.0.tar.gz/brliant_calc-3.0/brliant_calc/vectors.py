import numpy as np
import math

import numpy as np
import math

def dot_product(v1, v2):
    return np.dot(v1, v2)

def cross_product(v1, v2):
    return np.cross(v1, v2).tolist()

def magnitude(v):
    return np.linalg.norm(v)

def normalize(v):
    norm = np.linalg.norm(v)
    if norm == 0:
        return "Error: Cannot normalize zero vector."
    return (v / norm).tolist()

def angle_between(v1, v2):
    v1_u = normalize(v1)
    v2_u = normalize(v2)
    
    if isinstance(v1_u, str) or isinstance(v2_u, str):
        return "Error: Cannot calculate angle with zero vector."

    return np.degrees(np.arccos(np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)))
