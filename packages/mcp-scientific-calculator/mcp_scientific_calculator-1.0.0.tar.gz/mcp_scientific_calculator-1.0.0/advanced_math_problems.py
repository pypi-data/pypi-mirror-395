"""
Advanced University Mathematics Problems - MCP Solver Test
10个复杂的大学级别数学问题，需要MCP工具多步求解
"""

import json

ADVANCED_PROBLEMS = [
    {
        "id": 1,
        "title": "二阶线性非齐次微分方程的求解",
        "problem": "求解微分方程 y'' + 4y' + 3y = e^(-x)，初始条件 y(0) = 0, y'(0) = 1",
        "solution_steps": [
            {
                "step": 1,
                "description": "求解特征方程：r² + 4r + 3 = 0",
                "tool": "symbolic_tool",
                "params": {"operation": "solve", "equation": "r**2 + 4*r + 3", "variable": "r"},
                "expected_output": "[-3, -1]"
            },
            {
                "step": 2,
                "description": "写出齐次解：y_h = C₁e^(-x) + C₂e^(-3x)",
                "note": "特征根为 r₁ = -1, r₂ = -3"
            },
            {
                "step": 3,
                "description": "用待定系数法求特解，设 y_p = Axe^(-x)，代入原方程",
                "note": "因为 e^(-x) 是齐次解，所以特解形式为 Axe^(-x)"
            },
            {
                "step": 4,
                "description": "求导求二阶导数，得到 y_p' 和 y_p''",
                "tool": "symbolic_tool",
                "params": {"operation": "derivative", "expression": "A*x*exp(-x)", "variable": "x", "order": 1},
                "note": "第一阶导数"
            },
            {
                "step": 5,
                "description": "代入原方程，化简得到 A = 1/2",
                "tool": "symbolic_tool",
                "params": {"operation": "derivative", "expression": "A*x*exp(-x)", "variable": "x", "order": 2},
                "note": "第二阶导数用于代入微分方程"
            },
            {
                "step": 6,
                "description": "通解：y = C₁e^(-x) + C₂e^(-3x) + (1/2)xe^(-x)",
                "note": "齐次解 + 特解"
            },
            {
                "step": 7,
                "description": "利用初值条件 y(0) = 0, y'(0) = 1 确定 C₁, C₂",
                "tool": "symbolic_tool",
                "params": {"operation": "solve", "equation": "C1 + C2", "variable": "C1"},
                "note": "从 y(0) = 0 得第一个方程"
            }
        ],
        "difficulty": "advanced"
    },
    {
        "id": 2,
        "title": "矩阵特征值与特征向量的应用",
        "problem": "已知矩阵 A = [[2, 1, 0], [1, 2, 1], [0, 1, 2]]，求 A 的所有特征值和对应的特征向量，并将 A 对角化",
        "solution_steps": [
            {
                "step": 1,
                "description": "计算特征多项式 det(A - λI)",
                "tool": "numpy_tool",
                "params": {"operation": "eigenvalues", "matrix_a": "[[2, 1, 0], [1, 2, 1], [0, 1, 2]]"},
                "expected_note": "应得到特征值 λ₁ = 1, λ₂ = 2, λ₃ = 3"
            },
            {
                "step": 2,
                "description": "特征值求解得：λ₁ = 1, λ₂ = 2, λ₃ = 3",
                "note": "所有特征值都是实数"
            },
            {
                "step": 3,
                "description": "对每个特征值求对应的特征向量",
                "tool": "numpy_tool",
                "params": {"operation": "eigenvectors", "matrix_a": "[[2, 1, 0], [1, 2, 1], [0, 1, 2]]"},
                "note": "通过求解 (A - λᵢI)v = 0"
            },
            {
                "step": 4,
                "description": "构造矩阵 P = [v₁, v₂, v₃] 和对角矩阵 D",
                "tool": "numpy_tool",
                "params": {"operation": "inverse", "matrix_a": "[[2, 1, 0], [1, 2, 1], [0, 1, 2]]"},
                "note": "P 由特征向量组成"
            },
            {
                "step": 5,
                "description": "验证 A = PDP⁻¹",
                "note": "对角化完成"
            }
        ],
        "difficulty": "advanced"
    },
    {
        "id": 3,
        "title": "傅里叶级数展开与应用",
        "problem": "求函数 f(x) = x² 在 [-π, π] 上的傅里叶级数展开式，并利用该展开式求证 Σ(1/n²) = π²/6",
        "solution_steps": [
            {
                "step": 1,
                "description": "计算傅里叶系数 a₀ = (1/π)∫₋π^π x² dx",
                "tool": "symbolic_tool",
                "params": {"operation": "integral", "expression": "x**2", "variable": "x", "lower_limit": "-pi", "upper_limit": "pi"},
                "expected_output": "2*pi**3/3"
            },
            {
                "step": 2,
                "description": "计算傅里叶系数 aₙ = (1/π)∫₋π^π x²cos(nx) dx",
                "tool": "symbolic_tool",
                "params": {"operation": "integral", "expression": "x**2*cos(n*x)", "variable": "x", "lower_limit": "-pi", "upper_limit": "pi"},
                "note": "需要分部积分两次"
            },
            {
                "step": 3,
                "description": "由于 f(x) 是偶函数，bₙ = 0",
                "note": "只有 aₙ 系数"
            },
            {
                "step": 4,
                "description": "得到傅里叶级数 f(x) = π²/3 + 4Σ((-1)ⁿ/n²)cos(nx)",
                "note": "系数化简后的形式"
            },
            {
                "step": 5,
                "description": "在 x = 0 处求值",
                "tool": "symbolic_tool",
                "params": {"operation": "solve", "equation": "pi**2/3 + 4*sum((-1)**n/n**2)", "variable": "n"},
                "note": "利用级数求和公式"
            },
            {
                "step": 6,
                "description": "得到 f(0) = 0，利用级数求和推导 Σ(1/n²) = π²/6",
                "note": "经典的巴塞尔问题"
            }
        ],
        "difficulty": "advanced"
    },
    {
        "id": 4,
        "title": "多元函数极值问题",
        "problem": "求函数 f(x,y,z) = x² + 2y² + 3z² + 2xy + xz 在约束条件 x + y + z = 1 下的极小值",
        "solution_steps": [
            {
                "step": 1,
                "description": "构造拉格朗日函数 L = x² + 2y² + 3z² + 2xy + xz - λ(x + y + z - 1)",
                "note": "使用拉格朗日乘数法"
            },
            {
                "step": 2,
                "description": "求偏导数：∂L/∂x = 2x + 2y + z - λ = 0",
                "tool": "symbolic_tool",
                "params": {"operation": "derivative", "expression": "x**2 + 2*y**2 + 3*z**2 + 2*x*y + x*z", "variable": "x"},
                "expected_output": "2*x + 2*y + z"
            },
            {
                "step": 3,
                "description": "求偏导数：∂L/∂y = 4y + 2x - λ = 0",
                "tool": "symbolic_tool",
                "params": {"operation": "derivative", "expression": "x**2 + 2*y**2 + 3*z**2 + 2*x*y + x*z", "variable": "y"},
                "expected_output": "4*y + 2*x"
            },
            {
                "step": 4,
                "description": "求偏导数：∂L/∂z = 6z + x - λ = 0",
                "tool": "symbolic_tool",
                "params": {"operation": "derivative", "expression": "x**2 + 2*y**2 + 3*z**2 + 2*x*y + x*z", "variable": "z"},
                "expected_output": "6*z + x"
            },
            {
                "step": 5,
                "description": "联立方程组，加上约束 x + y + z = 1，求解 x, y, z 和 λ",
                "note": "共5个方程，5个未知数"
            },
            {
                "step": 6,
                "description": "计算 Hessian 矩阵的受限二阶导数判定极值类型",
                "note": "正定则为极小值"
            },
            {
                "step": 7,
                "description": "代入原函数计算极小值",
                "note": "最终答案"
            }
        ],
        "difficulty": "advanced"
    },
    {
        "id": 5,
        "title": "复变函数的留数定理应用",
        "problem": "计算实积分 ∫₀^∞ (x²)/(x⁶ + 1) dx",
        "solution_steps": [
            {
                "step": 1,
                "description": "识别被积函数的极点：x⁶ + 1 = 0 的解",
                "tool": "symbolic_tool",
                "params": {"operation": "solve", "equation": "x**6 + 1", "variable": "x"},
                "expected_note": "6个复根 e^(iπ(2k+1)/6)"
            },
            {
                "step": 2,
                "description": "选择上半平面的极点：3个极点",
                "note": "k = 0, 1, 2"
            },
            {
                "step": 3,
                "description": "计算各极点处的留数",
                "note": "使用留数公式计算"
            },
            {
                "step": 4,
                "description": "应用留数定理：∮ = 2πi × Σ留数",
                "note": "围道积分等于留数之和乘以 2πi"
            },
            {
                "step": 5,
                "description": "利用对称性关系简化计算",
                "note": "由于对称性，实积分等于围道积分的一半"
            },
            {
                "step": 6,
                "description": "最终得到 ∫₀^∞ (x²)/(x⁶ + 1) dx = π/(3√3)",
                "note": "经过留数定理计算"
            }
        ],
        "difficulty": "advanced"
    },
    {
        "id": 6,
        "title": "求解偏微分方程——热方程",
        "problem": "求解热方程 ∂u/∂t = α²∂²u/∂x²，其中 0 < x < L, t > 0，边界条件 u(0,t) = u(L,t) = 0，初始条件 u(x,0) = x(L-x)",
        "solution_steps": [
            {
                "step": 1,
                "description": "使用分离变量法，设 u(x,t) = X(x)T(t)",
                "note": "将偏微分方程分离为两个常微分方程"
            },
            {
                "step": 2,
                "description": "代入偏微分方程得 T'/T = α²X''/X = -λ（分离常数）",
                "note": "两边都等于常数"
            },
            {
                "step": 3,
                "description": "求解空间方程 X'' + (λ/α²)X = 0 及边界条件 X(0) = X(L) = 0",
                "note": "特征值问题"
            },
            {
                "step": 4,
                "description": "得到特征函数 Xₙ(x) = sin(nπx/L) 和特征值 λₙ = (nπα/L)²",
                "note": "n = 1, 2, 3, ..."
            },
            {
                "step": 5,
                "description": "求解时间方程 T' + λₙα²T = 0 得 Tₙ(t) = Aₙe^(-(nπα/L)²t)",
                "note": "一阶线性常微分方程"
            },
            {
                "step": 6,
                "description": "写出通解 u(x,t) = ΣAₙsin(nπx/L)e^(-(nπα/L)²t)",
                "note": "叠加原理"
            },
            {
                "step": 7,
                "description": "利用初始条件 u(x,0) = x(L-x) 确定系数 Aₙ",
                "tool": "symbolic_tool",
                "params": {"operation": "integral", "expression": "x*(L-x)*sin(n*pi*x/L)", "variable": "x", "lower_limit": "0", "upper_limit": "L"},
                "note": "傅里叶级数系数"
            }
        ],
        "difficulty": "advanced"
    },
    {
        "id": 7,
        "title": "多元微分学——曲面的切平面与法线",
        "problem": "设曲面 S: z = f(x,y) = x³ + y³ - 3xy，求点 P(1,2,z₀) 处的切平面方程和法线方程",
        "solution_steps": [
            {
                "step": 1,
                "description": "计算 z₀ = f(1,2) = 1³ + 2³ - 3·1·2",
                "tool": "symbolic_tool",
                "params": {"operation": "solve", "equation": "1**3 + 2**3 - 3*1*2", "variable": "x"},
                "expected_output": "3"
            },
            {
                "step": 2,
                "description": "计算偏导数 ∂f/∂x = 3x² - 3y",
                "tool": "symbolic_tool",
                "params": {"operation": "derivative", "expression": "x**3 + y**3 - 3*x*y", "variable": "x"},
                "expected_output": "3*x**2 - 3*y"
            },
            {
                "step": 3,
                "description": "计算偏导数 ∂f/∂y = 3y² - 3x",
                "tool": "symbolic_tool",
                "params": {"operation": "derivative", "expression": "x**3 + y**3 - 3*x*y", "variable": "y"},
                "expected_output": "3*y**2 - 3*x"
            },
            {
                "step": 4,
                "description": "在点 (1,2,3) 处求偏导数值：fₓ(1,2) = 3 - 6 = -3, fᵧ(1,2) = 12 - 3 = 9",
                "note": "代入坐标计算"
            },
            {
                "step": 5,
                "description": "写出切平面方程：z - 3 = -3(x-1) + 9(y-2)",
                "note": "点法式方程"
            },
            {
                "step": 6,
                "description": "化简切平面方程：3x - 9y + z + 12 = 0",
                "note": "一般式"
            },
            {
                "step": 7,
                "description": "写出法线方程：(x-1)/3 = (y-2)/(-9) = (z-3)/1",
                "note": "参数方程形式"
            }
        ],
        "difficulty": "intermediate"
    },
    {
        "id": 8,
        "title": "线性微分方程组的求解",
        "problem": "求解微分方程组 dy₁/dt = 3y₁ + y₂, dy₂/dt = y₁ + 3y₂，初始条件 y₁(0) = 1, y₂(0) = 0",
        "solution_steps": [
            {
                "step": 1,
                "description": "写出系数矩阵 A = [[3, 1], [1, 3]]",
                "note": "矩阵形式 dy/dt = Ay"
            },
            {
                "step": 2,
                "description": "求特征多项式 det(A - λI) = (3-λ)² - 1",
                "tool": "symbolic_tool",
                "params": {"operation": "solve", "equation": "(3-x)**2 - 1", "variable": "x"},
                "expected_output": "[2, 4]"
            },
            {
                "step": 3,
                "description": "得到特征值 λ₁ = 4, λ₂ = 2",
                "note": "两个实特征值"
            },
            {
                "step": 4,
                "description": "对 λ₁ = 4 求特征向量，解 (A - 4I)v = 0",
                "note": "v₁ = [1, 1]ᵀ"
            },
            {
                "step": 5,
                "description": "对 λ₂ = 2 求特征向量，解 (A - 2I)v = 0",
                "note": "v₂ = [1, -1]ᵀ"
            },
            {
                "step": 6,
                "description": "写出通解 y(t) = C₁e⁴ᵗ[1, 1]ᵀ + C₂e²ᵗ[1, -1]ᵀ",
                "note": "基本解矩阵"
            },
            {
                "step": 7,
                "description": "代入初始条件 y(0) = [1, 0]ᵀ 求 C₁ = 1/2, C₂ = 1/2",
                "note": "从 C₁ + C₂ = 1 和 C₁ - C₂ = 0"
            }
        ],
        "difficulty": "advanced"
    },
    {
        "id": 9,
        "title": "格林定理与曲线积分",
        "problem": "计算曲线积分 ∮_C (x²y)dx + (x+y²)dy，其中 C 为由 y = x² 和 y = 1 围成的闭合曲线（逆时针方向）",
        "solution_steps": [
            {
                "step": 1,
                "description": "验证积分路径的交点：由 x² = 1 得 x = ±1，y = 1",
                "note": "积分区域为 -1 ≤ x ≤ 1, x² ≤ y ≤ 1"
            },
            {
                "step": 2,
                "description": "应用格林定理，确定 P = x²y, Q = x + y²",
                "note": "∮_C = ∬_D (∂Q/∂x - ∂P/∂y)dxdy"
            },
            {
                "step": 3,
                "description": "计算 ∂Q/∂x = 1",
                "tool": "symbolic_tool",
                "params": {"operation": "derivative", "expression": "x + y**2", "variable": "x"},
                "expected_output": "1"
            },
            {
                "step": 4,
                "description": "计算 ∂P/∂y = x²",
                "tool": "symbolic_tool",
                "params": {"operation": "derivative", "expression": "x**2*y", "variable": "y"},
                "expected_output": "x**2"
            },
            {
                "step": 5,
                "description": "利用格林定理：∮_C = ∬_D (1 - x²)dxdy",
                "note": "被积函数为 1 - x²"
            },
            {
                "step": 6,
                "description": "建立二重积分 ∫₋₁¹ ∫_{x²}¹ (1 - x²)dydx",
                "note": "积分顺序：y 从 x² 到 1，x 从 -1 到 1"
            },
            {
                "step": 7,
                "description": "先对 y 积分：∫₋₁¹ (1 - x²)(1 - x²)dx = ∫₋₁¹ (1 - x²)²dx",
                "tool": "symbolic_tool",
                "params": {"operation": "integral", "expression": "(1 - x**2)**2", "variable": "x", "lower_limit": "-1", "upper_limit": "1"},
                "note": "计算结果"
            },
            {
                "step": 8,
                "description": "展开并积分得最终结果",
                "note": "∫₋₁¹ (1 - 2x² + x⁴)dx = [x - (2x³)/3 + x⁵/5]₋₁¹"
            }
        ],
        "difficulty": "advanced"
    },
    {
        "id": 10,
        "title": "变分法——泛函极值问题",
        "problem": "在所有满足 y(0) = 0, y(1) = 1 的光滑曲线中，求使泛函 J[y] = ∫₀¹ (y'² + 2xy)dx 取极值的曲线 y(x)",
        "solution_steps": [
            {
                "step": 1,
                "description": "写出被积函数 F(x, y, y') = y'² + 2xy",
                "note": "识别泛函的形式"
            },
            {
                "step": 2,
                "description": "列出欧拉-拉格朗日方程 ∂F/∂y - d/dx(∂F/∂y') = 0",
                "note": "变分法的基本方程"
            },
            {
                "step": 3,
                "description": "计算 ∂F/∂y = 2x",
                "tool": "symbolic_tool",
                "params": {"operation": "derivative", "expression": "y_prime**2 + 2*x*y", "variable": "y"},
                "expected_output": "2*x"
            },
            {
                "step": 4,
                "description": "计算 ∂F/∂y' = 2y'，再对 x 求导得 d/dx(∂F/∂y') = 2y''",
                "tool": "symbolic_tool",
                "params": {"operation": "derivative", "expression": "y_prime**2 + 2*x*y", "variable": "y_prime"},
                "expected_output": "2*y_prime"
            },
            {
                "step": 5,
                "description": "得到欧拉-拉格朗日方程 2x - 2y'' = 0，即 y'' = x",
                "note": "简化后的常微分方程"
            },
            {
                "step": 6,
                "description": "第一次积分得 y' = x²/2 + C₁",
                "tool": "symbolic_tool",
                "params": {"operation": "integral", "expression": "x", "variable": "x"},
                "expected_output": "x**2/2"
            },
            {
                "step": 7,
                "description": "第二次积分得 y = x³/6 + C₁x + C₂",
                "tool": "symbolic_tool",
                "params": {"operation": "integral", "expression": "x**2/2 + C1", "variable": "x"},
                "expected_output": "x**3/6 + C1*x"
            },
            {
                "step": 8,
                "description": "利用边界条件 y(0) = 0 得 C₂ = 0",
                "note": "第一个边界条件"
            },
            {
                "step": 9,
                "description": "利用边界条件 y(1) = 1 得 1/6 + C₁ = 1，即 C₁ = 5/6",
                "tool": "symbolic_tool",
                "params": {"operation": "solve", "equation": "1/6 + C1 - 1", "variable": "C1"},
                "expected_output": "[5/6]"
            },
            {
                "step": 10,
                "description": "得到极值曲线 y(x) = x³/6 + 5x/6",
                "note": "最终答案：使泛函取极值的曲线"
            }
        ],
        "difficulty": "advanced"
    }
]


def save_problems_to_json(filename: str = "advanced_math_problems.json"):
    """将问题保存为 JSON 文件"""
    with open(filename, 'w', encoding='utf-8') as f:
        json.dump(ADVANCED_PROBLEMS, f, ensure_ascii=False, indent=2)
    print(f"已保存 {len(ADVANCED_PROBLEMS)} 个问题到 {filename}")


if __name__ == "__main__":
    print("10个复杂的大学级别数学问题")
    print("="*80)
    for problem in ADVANCED_PROBLEMS:
        print(f"\n问题 {problem['id']}: {problem['title']}")
        print(f"难度: {problem['difficulty'].upper()}")
        print(f"问题描述: {problem['problem']}")
        print(f"解题步骤数: {len(problem['solution_steps'])}")
    
    print(f"\n总计: {len(ADVANCED_PROBLEMS)} 个问题")
    print("="*80)
    
    # 保存为 JSON
    save_problems_to_json()
