"""
Scientific Calculator - Pure Functions Module
直接可调用的计算函数，不依赖MCP装饰器
"""

import sympy as sp
import numpy as np
from scipy import integrate, optimize, interpolate, special, linalg as sp_linalg
try:
    import pandas as pd
except Exception:
    pd = None
from scipy.integrate import odeint
from scipy.fftpack import fft, rfft
from typing import Optional
import json

# ============================================================================
# SYMBOLIC MATHEMATICS (SymPy)
# ============================================================================

def symbolic_simplify(expression: str) -> str:
    """简化数学表达式"""
    try:
        expr = sp.sympify(expression)
        result = sp.simplify(expr)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def symbolic_expand(expression: str) -> str:
    """展开数学表达式"""
    try:
        expr = sp.sympify(expression)
        result = sp.expand(expr)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def symbolic_factor(expression: str) -> str:
    """因式分解"""
    try:
        expr = sp.sympify(expression)
        result = sp.factor(expr)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def symbolic_derivative(expression: str, variable: str, order: int = 1) -> str:
    """求导数"""
    try:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        result = sp.diff(expr, var, order)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def symbolic_integral(expression: str, variable: str, lower_limit: Optional[str] = None, upper_limit: Optional[str] = None) -> str:
    """不定积分或定积分"""
    try:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        
        if lower_limit and upper_limit:
            lower = sp.sympify(lower_limit)
            upper = sp.sympify(upper_limit)
            result = sp.integrate(expr, (var, lower, upper))
        else:
            result = sp.integrate(expr, var)
        
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def symbolic_limit(expression: str, variable: str, point: str) -> str:
    """求极限"""
    try:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        point_val = sp.sympify(point)
        result = sp.limit(expr, var, point_val)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def solve_equation(equation: str, variable: str) -> str:
    """解方程"""
    try:
        expr = sp.sympify(equation)
        var = sp.Symbol(variable)
        result = sp.solve(expr, var)
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def taylor_series(expression: str, variable: str, point: str, n: int) -> str:
    """泰勒级数展开"""
    try:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        point_val = sp.sympify(point)
        result = sp.series(expr, var, point_val, n).removeO()
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


def symbolic_matrix_operations(operation: str, matrix_data: str) -> str:
    """符号矩阵运算"""
    try:
        if operation == "determinant":
            mat = sp.Matrix(json.loads(matrix_data))
            result = mat.det()
        elif operation == "inverse":
            mat = sp.Matrix(json.loads(matrix_data))
            result = mat.inv()
        elif operation == "rank":
            mat = sp.Matrix(json.loads(matrix_data))
            result = mat.rank()
        elif operation == "trace":
            mat = sp.Matrix(json.loads(matrix_data))
            result = mat.trace()
        else:
            return "Error: Unknown operation"
        
        return str(result)
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# NUMERICAL COMPUTING (NumPy)
# ============================================================================

def numpy_array_operations(operation: str, array_data: str, axis: Optional[str] = None) -> str:
    """NumPy数组运算"""
    try:
        arr = np.array(json.loads(array_data))
        
        if operation == "sum":
            result = np.sum(arr, axis=int(axis) if axis else None)
        elif operation == "mean":
            result = np.mean(arr, axis=int(axis) if axis else None)
        elif operation == "std":
            result = np.std(arr, axis=int(axis) if axis else None)
        elif operation == "max":
            result = np.max(arr, axis=int(axis) if axis else None)
        elif operation == "min":
            result = np.min(arr, axis=int(axis) if axis else None)
        else:
            return "Error: Unknown operation"
        
        if isinstance(result, np.ndarray):
            return str(result.tolist())
        else:
            return str(float(result))
    except Exception as e:
        return f"Error: {str(e)}"


def numpy_linear_algebra(matrix_a, operation: str, matrix_b=None) -> str:
    """
    NumPy线性代数运算
    
    支持的操作:
    - eigenvalues: 计算特征值
    - eigenvectors: 计算特征向量
    - determinant: 计算行列式
    - inverse: 计算逆矩阵
    - solve: 解线性方程组 Ax = b
    - norm: 计算矩阵范数
    - rank: 计算矩阵秩
    - trace: 计算矩阵迹
    """
    try:
        # 处理输入格式：支持 JSON 字符串、NumPy 数组或列表
        if isinstance(matrix_a, str):
            try:
                mat1 = np.array(json.loads(matrix_a), dtype=float)
            except:
                mat1 = np.array(eval(matrix_a), dtype=float)
        else:
            mat1 = np.array(matrix_a, dtype=float)
        
        # 处理第二个矩阵
        if matrix_b is not None:
            if isinstance(matrix_b, str):
                try:
                    mat2 = np.array(json.loads(matrix_b), dtype=float)
                except:
                    mat2 = np.array(eval(matrix_b), dtype=float)
            else:
                mat2 = np.array(matrix_b, dtype=float)
        
        # 执行操作
        if operation == "eigenvalues":
            eigenvalues, eigenvectors = np.linalg.eig(mat1)
            result = {
                "eigenvalues": eigenvalues.tolist(),
                "eigenvectors": eigenvectors.tolist()
            }
            return json.dumps(result, ensure_ascii=False)
        
        elif operation == "eigenvectors":
            eigenvalues, eigenvectors = np.linalg.eig(mat1)
            result = {
                "eigenvalues": eigenvalues.tolist(),
                "eigenvectors": eigenvectors.tolist()
            }
            return json.dumps(result, ensure_ascii=False)
        
        elif operation == "determinant":
            result = float(np.linalg.det(mat1))
            return str(result)
        
        elif operation == "inverse":
            result = np.linalg.inv(mat1)
            return json.dumps(result.tolist(), ensure_ascii=False)
        
        elif operation == "solve":
            if matrix_b is None:
                return "Error: solve operation requires two matrices"
            result = np.linalg.solve(mat1, mat2)
            return json.dumps(result.tolist(), ensure_ascii=False)
        
        elif operation == "norm":
            result = float(np.linalg.norm(mat1))
            return str(result)
        
        elif operation == "rank":
            result = int(np.linalg.matrix_rank(mat1))
            return str(result)
        
        elif operation == "trace":
            result = float(np.trace(mat1))
            return str(result)
        
        else:
            return f"Error: Unknown operation '{operation}'"
    
    except Exception as e:
        return f"Error: {str(e)}"


def numpy_trigonometric(function: str, values: str, use_degrees: bool = False) -> str:
    """三角函数计算"""
    try:
        vals = np.array(json.loads(values))
        
        if use_degrees:
            vals = np.deg2rad(vals)
        
        func_map = {
            "sin": np.sin, "cos": np.cos, "tan": np.tan,
            "arcsin": np.arcsin, "arccos": np.arccos, "arctan": np.arctan,
            "sinh": np.sinh, "cosh": np.cosh, "tanh": np.tanh
        }
        
        if function not in func_map:
            return f"Error: Unknown function '{function}'"
        
        result = func_map[function](vals)
        
        if use_degrees and function.startswith("arc"):
            result = np.rad2deg(result)
        
        return str(result.tolist())
    except Exception as e:
        return f"Error: {str(e)}"


def numpy_polynomial(operation: str, coefficients: str, x_values: Optional[str] = None) -> str:
    """多项式运算"""
    try:
        coef = json.loads(coefficients)
        poly = np.poly1d(coef)
        
        if operation == "eval" and x_values:
            x = np.array(json.loads(x_values))
            result = poly(x)
            return str(result.tolist() if isinstance(result, np.ndarray) else result)
        elif operation == "derivative":
            result = np.polyder(poly)
            return str(result.coefficients.tolist())
        elif operation == "integral":
            result = np.polyint(poly)
            return str(result.coefficients.tolist())
        else:
            return "Error: Unknown operation"
    except Exception as e:
        return f"Error: {str(e)}"


# ============================================================================
# SCIENTIFIC COMPUTING (SciPy)
# ============================================================================

def scipy_integrate_function(expression: str, variable: str, lower: str, upper: str) -> str:
    """数值积分"""
    try:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        func = sp.lambdify(var, expr, modules=['numpy'])
        
        lower_val = float(sp.sympify(lower))
        upper_val = float(sp.sympify(upper))
        
        result, error = integrate.quad(func, lower_val, upper_val)
        
        return json.dumps({"result": result, "error": error}, ensure_ascii=False)
    except Exception as e:
        return f"Error: {str(e)}"


def scipy_optimize_minimize(expression: str, variable: str, initial_value: str, method: str = "BFGS") -> str:
    """函数最小化"""
    try:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        func = sp.lambdify(var, expr, modules=['numpy'])
        
        x0 = float(sp.sympify(initial_value))
        result = optimize.minimize(func, x0, method=method)
        
        return json.dumps({
            "x": result.x.tolist() if isinstance(result.x, np.ndarray) else float(result.x),
            "fun": float(result.fun),
            "success": bool(result.success)
        }, ensure_ascii=False)
    except Exception as e:
        return f"Error: {str(e)}"


def scipy_optimize_root(expression: str, variable: str, initial_value: str) -> str:
    """求方程根"""
    try:
        expr = sp.sympify(expression)
        var = sp.Symbol(variable)
        func = sp.lambdify(var, expr, modules=['numpy'])
        
        x0 = float(sp.sympify(initial_value))
        result = optimize.root_scalar(func, bracket=[x0-10, x0+10], method='brentq')
        
        return json.dumps({
            "root": float(result.root),
            "iterations": int(result.iterations),
            "function_calls": int(result.function_calls)
        }, ensure_ascii=False)
    except Exception as e:
        return f"Error: {str(e)}"


def scipy_interpolate(operation: str, x_data: str, y_data: str, x_eval: Optional[str] = None) -> str:
    """数据插值"""
    try:
        x = np.array(json.loads(x_data))
        y = np.array(json.loads(y_data))
        
        if operation == "linear":
            f = interpolate.interp1d(x, y, kind='linear')
        elif operation == "cubic":
            f = interpolate.interp1d(x, y, kind='cubic')
        elif operation == "spline":
            f = interpolate.interp1d(x, y, kind='quadratic')
        else:
            return "Error: Unknown operation"
        
        if x_eval:
            x_new = np.array(json.loads(x_eval))
            y_new = f(x_new)
            return json.dumps({"x": x_new.tolist(), "y": y_new.tolist()}, ensure_ascii=False)
        
        return "Error: x_eval required"
    except Exception as e:
        return f"Error: {str(e)}"


def scipy_special_functions(function: str, parameters: str) -> str:
    """特殊函数计算"""
    try:
        params = json.loads(parameters)
        
        func_map = {
            "gamma": lambda x: special.gamma(x),
            "bessel_j": lambda n, x: special.j0(x) if n == 0 else special.j1(x),
            "bessel_y": lambda n, x: special.y0(x) if n == 0 else special.y1(x),
            "erf": lambda x: special.erf(x),
            "erfc": lambda x: special.erfc(x),
        }
        
        if function not in func_map:
            return f"Error: Unknown function '{function}'"
        
        result = func_map[function](*params)
        return str(float(result) if not isinstance(result, np.ndarray) else result.tolist())
    except Exception as e:
        return f"Error: {str(e)}"


def scipy_solve_ode(expression: str, initial_conditions: str, t_values: str, variables: str = "y") -> str:
    """
    求解常微分方程（一阶或二阶）
    
    Args:
        expression: ODE 表达式，例如 'lambda t, y: -2*y'
        initial_conditions: 初始条件（JSON 数组格式）
        t_values: 时间点（JSON 数组格式）
        variables: 变量名（默认 'y'）
    """
    try:
        # 解析输入
        if isinstance(initial_conditions, str):
            y0 = np.array(json.loads(initial_conditions), dtype=float)
        else:
            y0 = np.array(initial_conditions, dtype=float)
        
        if isinstance(t_values, str):
            t = np.array(json.loads(t_values), dtype=float)
        else:
            t = np.array(t_values, dtype=float)
        
        # 确保 t 是升序的
        if len(t) > 1 and t[0] > t[-1]:
            t = t[::-1]
            reverse_order = True
        else:
            reverse_order = False
        
        # 评估 ODE 函数表达式
        try:
            # 尝试作为 lambda 函数字符串
            ode_func = eval(expression)
        except:
            # 如果失败，尝试作为符号表达式
            var_list = [sp.Symbol(v.strip()) for v in variables.split(",")]
            t_sym = sp.Symbol('t')
            expr = sp.sympify(expression)
            
            if len(var_list) == 1:
                ode_func = sp.lambdify([t_sym, var_list[0]], expr, modules=['numpy'])
                ode_func_wrapped = lambda y, t: ode_func(t, y)
            else:
                return "Error: System ODEs not yet fully supported"
        
        # 调用 odeint
        if isinstance(y0, (int, float)):
            y0 = np.array([y0])
        
        solution = odeint(ode_func, y0, t)
        
        if reverse_order:
            solution = solution[::-1]
            t = t[::-1]
        
        # 返回结果
        result = {
            "t": t.tolist(),
            "y": solution.tolist() if solution.ndim > 1 else solution.tolist()
        }
        
        return json.dumps(result, ensure_ascii=False)
    
    except Exception as e:
        import traceback
        return f"Error: {str(e)}"


def scipy_statistics(operation: str, data: str, params: Optional[str] = None) -> str:
    """统计分析"""
    try:
        from scipy import stats
        
        data_arr = np.array(json.loads(data))
        
        if operation == "describe":
            result = stats.describe(data_arr)
            return f"n={result.nobs}, mean={result.mean}, variance={result.variance}, skewness={result.skewness}, kurtosis={result.kurtosis}"
        elif operation == "mean":
            return str(float(np.mean(data_arr)))
        elif operation == "std":
            return str(float(np.std(data_arr)))
        elif operation == "ttest":
            popmean = json.loads(params) if params else 0
            result = stats.ttest_1samp(data_arr, popmean)
            return f"statistic={result.statistic}, pvalue={result.pvalue}"
        elif operation == "pearsonr" and params:
            data2 = np.array(json.loads(params))
            result = stats.pearsonr(data_arr, data2)
            return f"correlation={result[0]}, pvalue={result[1]}"
        else:
            return "Error: Unknown operation"
    except Exception as e:
        return f"Error: {str(e)}"


def scipy_fft(operation: str, data: str) -> str:
    """快速傅里叶变换"""
    try:
        data_arr = np.array(json.loads(data))
        
        if operation == "fft":
            result = fft(data_arr)
        elif operation == "rfft":
            result = rfft(data_arr)
        else:
            return f"Error: Unknown operation '{operation}'"
        
        if np.iscomplexobj(result):
            result_str = [f"{r.real:.6f}+{r.imag:.6f}j" if r.imag >= 0 else f"{r.real:.6f}{r.imag:.6f}j" for r in result]
            return str(result_str)
        else:
            return str(result.tolist())
    except Exception as e:
        return f"Error: {str(e)}"


def scipy_matrix_eigensystem(matrix_a, operation: str = "eigenvalues") -> str:
    """
    矩阵特征值分解系统 (scipy 风格的包装)
    这是 numpy_linear_algebra 的 scipy 风格别名
    """
    return numpy_linear_algebra(matrix_a, operation)


# Consolidated dispatcher tools

def symbolic_tool(
    operation: str,
    expression: str = None,
    variable: str = None,
    order: int = 1,
    lower_limit: str = None,
    upper_limit: str = None,
    equation: str = None,
    point: str = None,
    matrix_data: str = None,
    point_value: str = None,
):
    """统一的符号工具入口，按 operation 选择具体符号计算。"""
    op = operation.strip().lower()
    if op in ("simplify", "symbolic_simplify"):
        return symbolic_simplify(expression)
    if op in ("expand", "symbolic_expand"):
        return symbolic_expand(expression)
    if op in ("factor", "symbolic_factor"):
        return symbolic_factor(expression)
    if op in ("derivative", "diff", "symbolic_derivative"):
        return symbolic_derivative(expression, variable, order)
    if op in ("integral", "integrate", "symbolic_integral"):
        return symbolic_integral(expression, variable, lower_limit, upper_limit)
    if op in ("limit", "symbolic_limit"):
        return symbolic_limit(expression, variable, point or point_value)
    if op in ("solve", "solve_equation"):
        return solve_equation(equation or expression, variable)
    if op in ("taylor", "taylor_series"):
        return taylor_series(expression, variable, point or "0", order)
    if op in ("matrix", "symbolic_matrix_operations"):
        return symbolic_matrix_operations(variable or "determinant", matrix_data)
    return f"Error: Unknown symbolic operation '{operation}'"


def numpy_tool(
    operation: str,
    array_data: str = None,
    axis: str = None,
    matrix_a=None,
    matrix_b=None,
    values: str = None,
    use_degrees: bool = False,
    coefficients: str = None,
    x_values: str = None,
    dataframe: str = None,
    columns: str = None,
    image_data: str = None,
    threshold: float = 0.5,
):
    """统一的 NumPy 工具入口，覆盖数组、线性代数、三角、多项式运算。"""
    op = operation.strip().lower()

    # Array reductions
    if op in ("sum", "mean", "std", "max", "min"):
        return numpy_array_operations(op, array_data, axis)

    # Linear algebra
    if op in (
        "eigenvalues",
        "eigenvectors",
        "eigvals",
        "eig",
        "determinant",
        "inverse",
        "solve",
        "norm",
        "rank",
        "trace",
    ):
        mapped = {"eigvals": "eigenvalues", "eig": "eigenvalues"}.get(op, op)
        return numpy_linear_algebra(matrix_a, mapped, matrix_b)

    # Matrix products and decompositions
    if op in ("matmul", "mm", "dot", "hadamard"):
        if matrix_a is None or matrix_b is None:
            return "Error: matmul/dot/hadamard require matrix_a and matrix_b"
        mat1 = np.array(json.loads(matrix_a) if isinstance(matrix_a, str) else matrix_a, dtype=float)
        mat2 = np.array(json.loads(matrix_b) if isinstance(matrix_b, str) else matrix_b, dtype=float)
        if op in ("matmul", "mm", "dot"):
            result = np.matmul(mat1, mat2)
        else:  # hadamard
            result = np.multiply(mat1, mat2)
        return json.dumps(result.tolist(), ensure_ascii=False)

    if op == "svd":
        mat = np.array(json.loads(matrix_a) if isinstance(matrix_a, str) else matrix_a, dtype=float)
        U, S, Vh = np.linalg.svd(mat)
        return json.dumps({"U": U.tolist(), "S": S.tolist(), "Vh": Vh.tolist()}, ensure_ascii=False)

    if op == "qr":
        mat = np.array(json.loads(matrix_a) if isinstance(matrix_a, str) else matrix_a, dtype=float)
        Q, R = np.linalg.qr(mat)
        return json.dumps({"Q": Q.tolist(), "R": R.tolist()}, ensure_ascii=False)

    if op == "cholesky":
        mat = np.array(json.loads(matrix_a) if isinstance(matrix_a, str) else matrix_a, dtype=float)
        L = np.linalg.cholesky(mat)
        return json.dumps(L.tolist(), ensure_ascii=False)

    # Trigonometry
    if op in ("sin", "cos", "tan", "arcsin", "arccos", "arctan", "sinh", "cosh", "tanh"):
        return numpy_trigonometric(op, values, use_degrees)

    # Polynomial
    if op in ("poly_eval", "poly_derivative", "poly_integral"):
        poly_op = {
            "poly_eval": "eval",
            "poly_derivative": "derivative",
            "poly_integral": "integral",
        }[op]
        return numpy_polynomial(poly_op, coefficients, x_values)

    # Pandas (dataframe-based analytics)
    if op.startswith("pandas_"):
        if pd is None:
            return "Error: pandas is not installed"
        if dataframe is None:
            return "Error: pandas_* operations require 'dataframe' JSON input"
        try:
            df = pd.DataFrame(json.loads(dataframe))
        except Exception as e:
            return f"Error: invalid dataframe input ({e})"

        if op == "pandas_describe":
            return df.describe().to_json()
        if op == "pandas_corr":
            return df.corr(numeric_only=True).to_json()
        if op == "pandas_value_counts":
            if columns is None:
                return "Error: pandas_value_counts requires 'columns'"
            try:
                cols = json.loads(columns) if isinstance(columns, str) else columns
                series = df[cols[0]] if isinstance(cols, list) else df[columns]
                return series.value_counts().to_json()
            except Exception as e:
                return f"Error: value_counts failed ({e})"
        if op == "pandas_group_sum":
            if columns is None:
                return "Error: pandas_group_sum requires 'columns' as {group,agg}"
            try:
                spec = json.loads(columns) if isinstance(columns, str) else columns
                group_col = spec.get("group")
                agg_col = spec.get("agg")
                if not group_col or not agg_col:
                    return "Error: group_sum needs group and agg fields"
                result = df.groupby(group_col)[agg_col].sum()
                return result.to_json()
            except Exception as e:
                return f"Error: group_sum failed ({e})"
        return f"Error: Unknown pandas operation '{operation}'"

    # Image processing (numpy-based; expects JSON array HxWxC or HxW)
    if op in ("image_stats", "image_normalize", "image_threshold"):
        if image_data is None:
            return "Error: image_* operations require 'image_data' as JSON array"
        try:
            img = np.array(json.loads(image_data), dtype=float)
        except Exception as e:
            return f"Error: invalid image_data ({e})"
        if op == "image_stats":
            return json.dumps({
                "shape": list(img.shape),
                "min": float(np.min(img)),
                "max": float(np.max(img)),
                "mean": float(np.mean(img)),
                "std": float(np.std(img)),
            }, ensure_ascii=False)
        if op == "image_normalize":
            eps = 1e-8
            norm = (img - np.min(img)) / (np.max(img) - np.min(img) + eps)
            return json.dumps(norm.tolist(), ensure_ascii=False)
        if op == "image_threshold":
            mask = (img >= threshold).astype(float)
            return json.dumps(mask.tolist(), ensure_ascii=False)

    return f"Error: Unknown numpy operation '{operation}'"


def scipy_tool(
    operation: str,
    expression: str = None,
    variable: str = None,
    lower: str = None,
    upper: str = None,
    initial_value: str = None,
    method: str = "BFGS",
    x_data: str = None,
    y_data: str = None,
    x_eval: str = None,
    function: str = None,
    parameters: str = None,
    initial_conditions: str = None,
    t_values: str = None,
    variables: str = "y",
    data: str = None,
    params: str = None,
    data_series: str = None,
    matrix_a=None,
):
    """统一的 SciPy 工具入口，覆盖积分、优化、插值、特殊函数、ODE、统计、FFT、特征分解。"""
    op = operation.strip().lower()

    if op in ("integrate", "integrate_function"):
        return scipy_integrate_function(expression, variable, lower, upper)
    if op in ("optimize_minimize", "minimize"):
        return scipy_optimize_minimize(expression, variable, initial_value, method)
    if op in ("optimize_root", "root"):
        return scipy_optimize_root(expression, variable, initial_value)
    if op in ("interpolate_linear", "interpolate_cubic", "interpolate_spline", "interpolate"):
        kind = {
            "interpolate_linear": "linear",
            "interpolate_cubic": "cubic",
            "interpolate_spline": "spline",
            "interpolate": "linear",
        }[op]
        return scipy_interpolate(kind, x_data, y_data, x_eval)
    if op in ("special", "special_function"):
        return scipy_special_functions(function, parameters)
    if op in ("ode", "solve_ode"):
        return scipy_solve_ode(expression, initial_conditions, t_values, variables)
    if op in ("stats", "statistics"):
        return scipy_statistics(function or operation if function else op, data, params)
    if op in ("fft", "rfft"):
        return scipy_fft(op, data_series or data)
    if op in ("matrix_eigensystem", "eigensystem"):
        return scipy_matrix_eigensystem(matrix_a, "eigenvalues")
    return f"Error: Unknown scipy operation '{operation}'"


# 工具映射表（合并为 3 个对外暴露的入口）
CALCULATOR_TOOLS = {
    "symbolic_tool": symbolic_tool,
    "numpy_tool": numpy_tool,
    "scipy_tool": scipy_tool,
}


if __name__ == "__main__":
    # 测试
    print("测试计算器模块:")
    print(f"1. 导数 x³: {symbolic_derivative('x**3', 'x')}")
    print(f"2. 积分 x²: {symbolic_integral('x**2', 'x')}")
    print(f"3. 解方程 x²-4=0: {solve_equation('x**2 - 4', 'x')}")
    print(f"总工具数: {len(CALCULATOR_TOOLS)}")
