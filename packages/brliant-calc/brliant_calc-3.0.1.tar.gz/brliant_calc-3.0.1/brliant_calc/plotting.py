import matplotlib.pyplot as plt
import numpy as np
import ast
import operator


OPERATORS = {
    ast.Add: operator.add,
    ast.Sub: operator.sub,
    ast.Mult: operator.mul,
    ast.Div: operator.truediv,
    ast.Pow: operator.pow,
    ast.USub: operator.neg,
    ast.UAdd: operator.pos,
}

FUNCTIONS = {
    "sin": np.sin, "cos": np.cos, "tan": np.tan,
    "arcsin": np.arcsin, "arccos": np.arccos, "arctan": np.arctan,
    "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh,
    "exp": np.exp, "log": np.log, "log10": np.log10,
    "sqrt": np.sqrt, "abs": np.abs,
    "pi": np.pi, "e": np.e,
}

def evaluate_ast(node, variables):
    
    if isinstance(node, ast.Constant): 
        return node.value
    elif isinstance(node, ast.Name):
        if node.id in variables:
            return variables[node.id]
        if node.id in FUNCTIONS and isinstance(FUNCTIONS[node.id], (int, float, np.float64)):
             return FUNCTIONS[node.id] 
        raise ValueError(f"Unknown variable or constant: {node.id}")
    elif isinstance(node, ast.BinOp):
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](evaluate_ast(node.left, variables), evaluate_ast(node.right, variables))
        raise ValueError(f"Unsupported operator: {op_type}")
    elif isinstance(node, ast.UnaryOp):
        op_type = type(node.op)
        if op_type in OPERATORS:
            return OPERATORS[op_type](evaluate_ast(node.operand, variables))
        raise ValueError(f"Unsupported unary operator: {op_type}")
    elif isinstance(node, ast.Call):
        if not isinstance(node.func, ast.Name):
             raise ValueError("Function calls must be simple names")
        func_name = node.func.id
        if func_name in FUNCTIONS:
            args = [evaluate_ast(arg, variables) for arg in node.args]
            return FUNCTIONS[func_name](*args)
        raise ValueError(f"Unknown function: {func_name}")
    else:
        raise ValueError(f"Unsupported expression type: {type(node)}")

def plot(func_str, x_range="0,10", user_vars=None):
    try:
        start, end = map(float, x_range.split(","))
        x = np.linspace(start, end, 1000)
        
        variables = {"x": x}
        if user_vars:
            for var, val in user_vars.items():
                if isinstance(val, (int, float)):
                    variables[var] = val
        
        tree = ast.parse(func_str, mode='eval')
        
        y = evaluate_ast(tree.body, variables)
        
        if np.isscalar(y):
            y = np.full_like(x, y)
            
        plt.figure(figsize=(10, 6))
        plt.plot(x, y)
        plt.title(f"Plot of {func_str}")
        plt.xlabel("x")
        plt.ylabel("y")
        plt.grid(True)
        plt.show()
        return "Plot displayed."
    except Exception as e:
        return f"Error plotting function: {e}"

