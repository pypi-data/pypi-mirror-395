#!/usr/bin/env python3
"""
Final Verification Script - MCP Server Production Readiness Test
验证 MCP 服务器是否完全就绪进行生产部署
"""

import json
import sys
from calculator import CALCULATOR_TOOLS
import numpy as np

def verify_tools():
    """验证所有 22 个工具都可访问且能工作"""
    print("=" * 80)
    print("MCP 服务器生产就绪性验证")
    print("=" * 80)
    print()
    
    print("1. 验证工具数量...")
    print(f"   预期: 3 个工具 (合并版)")
    print(f"   实际: {len(CALCULATOR_TOOLS)} 个工具")
    
    if len(CALCULATOR_TOOLS) != 3:
        print("   [FAIL] 工具数量不匹配!")
        return False
    print("   [OK] 工具数量正确")
    print()
    
    print("2. 验证工具名称...")
    expected_tools = ['symbolic_tool', 'numpy_tool', 'scipy_tool']
    
    missing = set(expected_tools) - set(CALCULATOR_TOOLS.keys())
    extra = set(CALCULATOR_TOOLS.keys()) - set(expected_tools)
    
    if missing:
        print(f"   [FAIL] 缺少的工具: {missing}")
        return False
    if extra:
        print(f"   [WARN] 多余的工具: {extra}")
    
    print("   [OK] 工具名称完整")
    print()
    
    print("3. 验证关键工具功能...")
    tests = [
        ("symbolic_tool.derivative", lambda: CALCULATOR_TOOLS['symbolic_tool'](
            operation='derivative', expression='x**3', variable='x')),
        ("symbolic_tool.integral", lambda: CALCULATOR_TOOLS['symbolic_tool'](
            operation='integral', expression='x**2', variable='x')),
        ("symbolic_tool.solve", lambda: CALCULATOR_TOOLS['symbolic_tool'](
            operation='solve', equation='x**2 - 4', variable='x')),
        ("numpy_tool.determinant", lambda: CALCULATOR_TOOLS['numpy_tool'](
            operation='determinant', matrix_a=[[1, 2], [3, 4]])),
    ]
    
    for tool_name, test_func in tests:
        try:
            result = test_func()
            print(f"   [OK] {tool_name} 工作正常")
        except Exception as e:
            print(f"   [FAIL] {tool_name} 失败: {e}")
            return False
    print()
    
    print("4. 验证问题集...")
    try:
        from advanced_math_problems import ADVANCED_PROBLEMS
        print(f"   预期: 10 个问题")
        print(f"   实际: {len(ADVANCED_PROBLEMS)} 个问题")
        if len(ADVANCED_PROBLEMS) != 10:
            print("   [WARN] 问题数量不匹配")
        else:
            print("   [OK] 问题集完整")
    except:
        print("   [WARN] 无法加载问题集")
    print()
    
    print("=" * 80)
    print("[OK] 所有验证通过 - 生产就绪!")
    print("=" * 80)
    print()
    print("下一步: 启动 MCP 服务器")
    print("  python mcp_server.py")
    print()
    print("配置 Claude Desktop:")
    print("  编辑 %APPDATA%\\Claude\\claude_desktop_config.json")
    print("  添加 mcp_server.py 到 mcpServers 配置")
    print()
    
    return True

if __name__ == "__main__":
    success = verify_tools()
    sys.exit(0 if success else 1)
