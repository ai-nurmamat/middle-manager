import json
import datetime
from .graph import UniversalHypergraph
from .llm import MockExtractor, UniversalExtractor
from .sleep import SleepConsolidator

# ===================================================================
# Chronos-V2 MCP Gateway (时空网关)
# 摒弃写死 "趋势查询" "关系查询" 这种硬编码的业务接口。
# 让大模型通过最原生的 `query_graph` 自行穿梭在四维图谱里。
# ===================================================================

class MCPGateway:
    def __init__(self):
        self.graph = UniversalHypergraph()
        self.extractor = MockExtractor()
        self.consolidator = SleepConsolidator(self.graph)
        
    def inject_knowledge(self, text: str, source_id: str, publish_date_str: str):
        """接收非结构化文本，提取成 S-P-O-T 图谱。支持流式调用。"""
        dt = datetime.datetime.strptime(publish_date_str, "%Y-%m-%d")
        self.extractor.extract_to_graph(text, source_id, dt, self.graph)
        return {"status": "success", "message": f"Knowledge injected from {source_id}"}
        
    def trigger_sleep(self):
        """触发记忆整理与自进化"""
        self.consolidator.sleep_and_reflect()
        return {"status": "success", "message": "Graph ontology consolidated."}
        
    def query_graph(self, subject=None, predicate=None, object=None):
        """
        极简、全能的万维图谱查询接口。
        大模型想看趋势：传 (subject="宁德时代", predicate="毛利率") -> 返回所有时间点
        大模型想找竞争：传 (subject="宁德时代", predicate="竞争对手") -> 返回所有客体
        大模型想查谁在投资固态电池：传 (predicate="投资", object="固态电池") -> 返回所有主体
        """
        res = self.graph.query(subject=subject, predicate=predicate, object=object)
        
        # 序列化为 LLM 易读的格式
        output = []
        for t in res:
            output.append({
                "S": t.subject,
                "P": t.predicate,
                "O": f"{t.object}{t.unit or ''}",
                "Time": t.time.strftime("%Y-%m-%d"),
                "Source": t.evidence.source_id if t.evidence else "N/A"
            })
        return output

# 测试演示脚本
def demo():
    mcp = MCPGateway()
    
    # 1. 知识注入 (包含大量未对齐的脏数据：宁王、CATL、重仓、毛利)
    text_2022 = "根据2022年研报，宁德时代毛利率为27.0%。比亚迪储能毛利为20.0%。宁王与比亚迪竞品加剧。"
    text_2023 = "根据2023年研报，CATL毛利达到28.5%，比亚迪储能毛利同期为22%。CATL开始重仓全固态电池。"
    
    mcp.inject_knowledge(text_2022, "rpt_2022", "2022-10-15")
    mcp.inject_knowledge(text_2023, "rpt_2023", "2023-10-15")
    
    print("\n--- [Query Before Sleep] 尝试查询 '宁德时代' 的 '毛利率' ---")
    res1 = mcp.query_graph(subject="宁德时代", predicate="毛利率")
    print(json.dumps(res1, indent=2, ensure_ascii=False))
    print("-> 发现问题：由于实体和谓语未归一化，只搜到了 2022 年的数据 (因为2023年被LLM抽取为 'CATL' 的 '毛利')")
    
    # 2. 触发系统睡眠
    mcp.trigger_sleep()
    
    print("--- [Query After Sleep] 再次查询 '宁德时代' 的 '毛利率' ---")
    res2 = mcp.query_graph(subject="宁德时代", predicate="毛利率")
    print(json.dumps(res2, indent=2, ensure_ascii=False))
    print("-> 惊人发现：系统通过自进化统一了本体，现在直接搜出了完整的时间线趋势！\n")
    
    print("--- [Super Query] 谁投资了固态电池？ ---")
    res3 = mcp.query_graph(predicate="投资", object="固态电池")
    print(json.dumps(res3, indent=2, ensure_ascii=False))
    print("-> 强大的多维图谱：利用 (P, O) 反向查找 Subject，并附带时间。")

if __name__ == "__main__":
    demo()
