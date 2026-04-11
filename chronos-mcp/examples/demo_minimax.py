import os
import json
import datetime
from chronos import UniversalHypergraph, UniversalExtractor, MCPGateway

def demo_with_real_llm():
    """
    这是一个使用真实 LLM (例如 Minimax M2.7 或 OpenAI) 的示例。
    请确保在运行前设置了环境变量：
    export MINIMAX_API_KEY="your_api_key"
    export MINIMAX_BASE_URL="https://api.minimax.chat/v1"
    export MINIMAX_MODEL="abab6.5-chat"
    """
    
    api_key = os.environ.get("MINIMAX_API_KEY")
    base_url = os.environ.get("MINIMAX_BASE_URL", "https://api.minimax.chat/v1")
    model = os.environ.get("MINIMAX_MODEL", "abab6.5-chat")
    
    if not api_key:
        print("⚠️ Please set MINIMAX_API_KEY environment variable to run this demo.")
        print("Example: export MINIMAX_API_KEY='your_api_key'")
        return

    print(f"🚀 Initializing Chronos Engine with model: {model}")
    mcp = MCPGateway()
    
    # 替换网关中默认的 MockExtractor 为真实的 UniversalExtractor
    mcp.extractor = UniversalExtractor(api_key=api_key, base_url=base_url, model=model)
    
    # 注入真实非结构化文本
    text_1 = """
    【招商证券】2023年三季报点评：宁德时代Q3营收1054亿元，同比增长8.28%。
    值得注意的是，公司毛利率达到22.4%，环比提升。
    同期，特斯拉宣布暂停在墨西哥的超级工厂建设计划，引发供应链担忧。
    """
    
    print("\n[1/3] Injecting knowledge from Text 1...")
    mcp.inject_knowledge(text_1, "report_zs_2023q3", "2023-10-20")
    
    text_2 = """
    【中信建投】新能源行业快报：受宁德时代降价影响，二线电池厂承压。
    其中，中创新航Q3毛利率降至14%。此外，宁王开始联合商飞布局eVTOL（低空经济）。
    """
    
    print("\n[2/3] Injecting knowledge from Text 2...")
    mcp.inject_knowledge(text_2, "report_zx_2023q4", "2023-11-05")
    
    print("\n[3/3] Querying the extracted graph...")
    print("\n👉 Query: 谁的毛利率被提及了？ (Predicate='毛利率')")
    res1 = mcp.query_graph(predicate="毛利率")
    print(json.dumps(res1, indent=2, ensure_ascii=False))
    
    print("\n👉 Query: 宁德时代的动作？ (Subject='宁德时代')")
    res2 = mcp.query_graph(subject="宁德时代")
    print(json.dumps(res2, indent=2, ensure_ascii=False))
    
    print("\n💤 Going to sleep to consolidate noisy aliases (e.g. 宁王 -> 宁德时代)...")
    mcp.trigger_sleep()
    
    print("\n👉 Query after sleep: 宁德时代的全部动作？")
    res3 = mcp.query_graph(subject="宁德时代")
    print(json.dumps(res3, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    demo_with_real_llm()
