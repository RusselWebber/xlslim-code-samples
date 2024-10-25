import numpy as np
from scipy.optimize import linprog, OptimizeResult

def scipy_optimise(engine: str,
    time_limit: float,
    obj_coeff: np.ndarray,
    constraints: np.ndarray,
    rhs: np.ndarray,
    varbounds: np.ndarray,
) -> OptimizeResult:
    return linprog(c = obj_coeff, 
                   A_ub = constraints, 
                   b_ub = rhs, 
                   bounds = varbounds.tolist(), 
                   method = engine, 
                   options = {'time_limit': time_limit})

def report_x_values(result: OptimizeResult, idx:int) -> float:
    return result.x[idx]

def report_slack(result: OptimizeResult) -> list[float]:
    return result.slack.tolist()

def report_marginals(result: OptimizeResult) -> list[float]:
    return result.ineqlin.marginals.tolist()