import os
import sys
import datetime
from engine import TemporalGraphEngine
from pipeline import ingest_report
from query_engine import TemporalQueryEngine

# ==========================================
# 简单的 MCP 协议封装 (模拟层)
# 提供 JSON-RPC 格式供外部大模型工具调用
# ==========================================

# 1. 初始化引擎并注入数据 (系统启动阶段)
db = TemporalGraphEngine()
# 模拟摄入了一篇研报
sample_text = """
根据2023年Q3研报，宁德时代（CATL）毛利率达到28.5%，主要由于规模效应。
相比之下，比亚迪的储能毛利率同期仅为22%。同时，宁德时代开始重点布局固态电池。
"""
ingest_report(db, report_id="rpt_001", text=sample_text, publish_date=datetime.datetime(2023, 10, 15))
# 模拟摄入另一篇过往研报形成时间线
sample_text_2 = """根据2022年Q3研报，宁德时代毛利率为27.0%。比亚迪储能毛利率为20.0%"""
ingest_report(db, report_id="rpt_000", text=sample_text_2, publish_date=datetime.datetime(2022, 10, 15))

query_engine = TemporalQueryEngine(db)

def mcp_server_loop():
    """
    一个极其轻量级的 CLI 交互循环，模拟 MCP Server 接收 JSON-RPC 请求
    在真实的 MCP 协议中，这会通过 stdio (jsonlines) 或 SSE 进行通讯
    """
    import json
    
    print(json.dumps({"status": "ready", "message": "Chronos-MCP Server Started. Waiting for input..."}))
    
    for line in sys.stdin:
        line = line.strip()
        if not line: continue
        
        try:
            req = json.loads(line)
            tool_name = req.get("tool")
            args = req.get("args", {})
            
            result = None
            if tool_name == "query_trend":
                result = query_engine.query_trend(args["entity"], args["property"])
            elif tool_name == "compare_entities":
                result = query_engine.compare_entities(args["entities"], args["property"])
            elif tool_name == "discover_relations":
                result = query_engine.discover_relations(args["entity"])
            else:
                result = {"error": f"Unknown tool: {tool_name}"}
                
            # MCP Response 格式
            response = {
                "id": req.get("id"),
                "result": result
            }
            print(json.dumps(response))
            sys.stdout.flush()
            
        except Exception as e:
             print(json.dumps({"error": str(e)}))
             sys.stdout.flush()

if __name__ == "__main__":
    # 如果作为脚本运行，直接执行交互循环
    # 测试可以直接 pipe JSON 进去
    mcp_server_loop()
