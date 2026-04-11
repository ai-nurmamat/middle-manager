#!/usr/bin/env python3
import json
import sys
import subprocess
import time

def test_mcp():
    """测试 MCP 服务器的功能"""
    
    # 启动 MCP Server 进程
    process = subprocess.Popen(
        [sys.executable, "mcp_server.py"],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True
    )
    
    # 忽略前面的日志输出，只读取 JSON 输出
    while True:
        line = process.stdout.readline().strip()
        if not line:
            time.sleep(0.1)
            continue
            
        try:
            parsed = json.loads(line)
            if parsed.get("status") == "ready":
                print("Server Output:", line)
                break
        except json.JSONDecodeError:
            # 可能是 logging 模块的输出
            print("LOG:", line)
    
    # 测试 1: 趋势查询
    req1 = {
        "id": "1",
        "tool": "query_trend",
        "args": {"entity": "宁德时代", "property": "毛利率"}
    }
    
    print("\n--- Test 1: Trend Query ---")
    print(f"Request: {json.dumps(req1, ensure_ascii=False)}")
    process.stdin.write(json.dumps(req1) + "\n")
    process.stdin.flush()
    print("Response:", process.stdout.readline().strip())
    
    # 测试 2: 关系发现
    req2 = {
        "id": "2",
        "tool": "discover_relations",
        "args": {"entity": "CATL"} # 测试别名查询
    }
    
    print("\n--- Test 2: Discover Relations (using alias) ---")
    print(f"Request: {json.dumps(req2, ensure_ascii=False)}")
    process.stdin.write(json.dumps(req2) + "\n")
    process.stdin.flush()
    print("Response:", process.stdout.readline().strip())
    
    process.terminate()

if __name__ == "__main__":
    test_mcp()
