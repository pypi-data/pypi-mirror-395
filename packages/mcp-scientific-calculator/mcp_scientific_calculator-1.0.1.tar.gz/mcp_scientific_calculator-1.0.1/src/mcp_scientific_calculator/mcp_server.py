"""
Scientific Calculator MCP Server - Production Ready
完全符合 MCP 规范的科学计算器服务器
支持通过标准输入输出（STDIO）进行 JSON-RPC 2.0 通信

This implementation strictly follows:
https://modelcontextprotocol.io/docs/develop/build-server
"""

import json
import sys
import logging
from typing import Any, Dict, List
from dataclasses import dataclass, asdict
from .calculator import CALCULATOR_TOOLS
import numpy as np

# 配置日志到 stderr（不污染 stdout JSON-RPC 输出）
logging.basicConfig(
    level=logging.WARNING,
    format='[%(levelname)s] %(message)s',
    stream=sys.stderr,
    force=True
)
logger = logging.getLogger(__name__)


@dataclass
class JSONRPCRequest:
    """JSON-RPC 2.0 请求"""
    jsonrpc: str = "2.0"
    method: str = None
    params: Dict[str, Any] = None
    id: Any = None


@dataclass
class JSONRPCResponse:
    """JSON-RPC 2.0 响应"""
    jsonrpc: str = "2.0"
    result: Any = None
    error: Dict[str, Any] = None
    id: Any = None


class MCPCalculatorServer:
    """符合 MCP 规范的计算器服务器"""
    
    def __init__(self):
        self.version = "1.0.0"
        self.name = "Scientific Calculator"
        self.tools = self._build_tool_definitions()
        
    def _build_tool_definitions(self) -> List[Dict[str, Any]]:
        """构建工具定义列表"""
        tools = []
        
        # Consolidated tool definitions (3 tools)
        tool_definitions = {
            "symbolic_tool": {
                "description": "统一符号计算入口：simplify/expand/factor/derivative/integral/limit/solve/taylor/matrix",
                "params": [
                    {"name": "operation", "type": "string", "description": "操作类型，如 derivative, integral, solve 等"},
                    {"name": "expression", "type": "string", "description": "表达式", "optional": True},
                    {"name": "variable", "type": "string", "description": "变量", "optional": True},
                    {"name": "order", "type": "integer", "description": "阶数（导数/泰勒）", "optional": True},
                    {"name": "lower_limit", "type": "string", "description": "积分下限", "optional": True},
                    {"name": "upper_limit", "type": "string", "description": "积分上限", "optional": True},
                    {"name": "equation", "type": "string", "description": "方程", "optional": True},
                    {"name": "point", "type": "string", "description": "极限或泰勒展开点", "optional": True},
                    {"name": "matrix_data", "type": "string", "description": "符号矩阵（JSON）", "optional": True}
                ]
            },
            "numpy_tool": {
                "description": "统一 NumPy 入口：数组归约、线性代数、三角、多项式",
                "params": [
                    {"name": "operation", "type": "string", "description": "操作类型，如 eigenvalues, sum, poly_eval 等"},
                    {"name": "array_data", "type": "string", "description": "数组数据（JSON）", "optional": True},
                    {"name": "axis", "type": "string", "description": "轴参数", "optional": True},
                    {"name": "matrix_a", "type": "string", "description": "矩阵A（JSON）", "optional": True},
                    {"name": "matrix_b", "type": "string", "description": "矩阵B（JSON）", "optional": True},
                    {"name": "values", "type": "string", "description": "三角函数输入（JSON）", "optional": True},
                    {"name": "use_degrees", "type": "boolean", "description": "角度制", "optional": True},
                    {"name": "coefficients", "type": "string", "description": "多项式系数（JSON）", "optional": True},
                    {"name": "x_values", "type": "string", "description": "多项式自变量数组（JSON）", "optional": True}
                ]
            },
            "scipy_tool": {
                "description": "统一 SciPy 入口：积分、优化、插值、特殊函数、ODE、统计、FFT、特征分解",
                "params": [
                    {"name": "operation", "type": "string", "description": "操作类型，如 integrate, optimize_minimize, fft 等"},
                    {"name": "expression", "type": "string", "description": "表达式/函数", "optional": True},
                    {"name": "variable", "type": "string", "description": "变量", "optional": True},
                    {"name": "lower", "type": "string", "description": "积分下限", "optional": True},
                    {"name": "upper", "type": "string", "description": "积分上限", "optional": True},
                    {"name": "initial_value", "type": "string", "description": "初值/起点", "optional": True},
                    {"name": "method", "type": "string", "description": "算法方法", "optional": True},
                    {"name": "x_data", "type": "string", "description": "插值 x 数据（JSON）", "optional": True},
                    {"name": "y_data", "type": "string", "description": "插值 y 数据（JSON）", "optional": True},
                    {"name": "x_eval", "type": "string", "description": "插值求值点（JSON）", "optional": True},
                    {"name": "function", "type": "string", "description": "特殊函数名/统计操作名", "optional": True},
                    {"name": "parameters", "type": "string", "description": "特殊函数参数（JSON）", "optional": True},
                    {"name": "initial_conditions", "type": "string", "description": "ODE 初值（JSON）", "optional": True},
                    {"name": "t_values", "type": "string", "description": "ODE 时间点（JSON）", "optional": True},
                    {"name": "variables", "type": "string", "description": "ODE 变量名", "optional": True},
                    {"name": "data", "type": "string", "description": "统计或 FFT 数据（JSON）", "optional": True},
                    {"name": "params", "type": "string", "description": "统计附加参数（JSON）", "optional": True},
                    {"name": "data_series", "type": "string", "description": "FFT 数据（JSON）", "optional": True},
                    {"name": "matrix_a", "type": "string", "description": "矩阵（JSON）用于特征分解", "optional": True}
                ]
            },
        }
        
        # 构建工具列表
        for tool_name, definition in tool_definitions.items():
            tools.append({
                "name": tool_name,
                "description": definition["description"],
                "params": {
                    "type": "object",
                    "properties": {
                        param["name"]: {
                            "type": param["type"],
                            "description": param["description"]
                        }
                        for param in definition["params"]
                    },
                    "required": [
                        p["name"] for p in definition["params"] 
                        if not p.get("optional", False)
                    ]
                }
            })
        
        return tools
    
    def call_tool(self, tool_name: str, params: Dict[str, Any]) -> str:
        """调用计算器工具"""
        if tool_name not in CALCULATOR_TOOLS:
            raise ValueError(f"Unknown tool: {tool_name}")
        
        try:
            # 获取工具函数
            tool_func = CALCULATOR_TOOLS[tool_name]
            
            # 调用工具函数
            result = tool_func(**params)
            
            return str(result)
            
        except TypeError as e:
            return f"Parameter Error: {str(e)}"
        except Exception as e:
            return f"Execution Error: {str(e)}"
    
    def handle_rpc_request(self, request_dict: Dict[str, Any]) -> Dict[str, Any]:
        """处理 JSON-RPC 请求"""
        try:
            # 验证 JSON-RPC 2.0 格式
            if request_dict.get("jsonrpc") != "2.0":
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32600,
                        "message": "Invalid Request"
                    },
                    "id": request_dict.get("id")
                }
            
            method = request_dict.get("method")
            params = request_dict.get("params", {})
            req_id = request_dict.get("id")
            
            # 处理特殊方法
            if method == "initialize":
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "protocolVersion": "2024-11-05",
                        "capabilities": {},
                        "serverInfo": {
                            "name": self.name,
                            "version": self.version
                        }
                    },
                    "id": req_id
                }
            
            elif method == "tools/list":
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "tools": self.tools
                    },
                    "id": req_id
                }
            
            elif method == "tools/call":
                tool_name = params.get("name")
                tool_params = params.get("arguments", {})
                
                result = self.call_tool(tool_name, tool_params)
                
                return {
                    "jsonrpc": "2.0",
                    "result": {
                        "content": [
                            {
                                "type": "text",
                                "text": result
                            }
                        ]
                    },
                    "id": req_id
                }
            
            else:
                return {
                    "jsonrpc": "2.0",
                    "error": {
                        "code": -32601,
                        "message": f"Method not found: {method}"
                    },
                    "id": req_id
                }
        
        except Exception as e:
            logger.error(f"RPC Error: {e}")
            return {
                "jsonrpc": "2.0",
                "error": {
                    "code": -32603,
                    "message": f"Internal error: {str(e)}"
                },
                "id": request_dict.get("id")
            }
    
    def run(self):
        """运行 MCP 服务器（STDIO 模式）"""
        logger.info(f"Starting {self.name} v{self.version}")
        logger.info(f"Registered {len(self.tools)} tools")
        
        try:
            while True:
                # 从标准输入读取 JSON-RPC 请求
                line = sys.stdin.readline()
                
                if not line:
                    # EOF
                    break
                
                try:
                    request = json.loads(line)
                    response = self.handle_rpc_request(request)
                    
                    # 写入 JSON-RPC 响应到标准输出
                    sys.stdout.write(json.dumps(response, ensure_ascii=False) + '\n')
                    sys.stdout.flush()
                    
                except json.JSONDecodeError as e:
                    # 发送 JSON 解析错误
                    error_response = {
                        "jsonrpc": "2.0",
                        "error": {
                            "code": -32700,
                            "message": "Parse error"
                        }
                    }
                    sys.stdout.write(json.dumps(error_response) + '\n')
                    sys.stdout.flush()
        
        except KeyboardInterrupt:
            logger.info("Server interrupted")
        except Exception as e:
            logger.error(f"Server error: {e}")
            sys.exit(1)


def main():
    """启动 MCP 服务器"""
    server = MCPCalculatorServer()
    server.run()


if __name__ == "__main__":
    main()
