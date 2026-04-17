"""
Chronos-MCP Gateway.

This module provides a streamlined interface for LLMs to inject and query
the Universal Hypergraph, decoupling the memory engine from any specific API framework.
"""

import json
import datetime
from typing import Optional, Dict, Any, List, Union

from .graph import UniversalHypergraph
from .llm import MockExtractor, UniversalExtractor
from .sleep import SleepConsolidator


class MCPGateway:
    """
    The MCP Gateway encapsulates the graph engine, the extractor, and the sleep
    consolidator into a unified controller.
    """

    def __init__(self) -> None:
        self.graph = UniversalHypergraph()
        self.extractor: Union[MockExtractor, UniversalExtractor] = MockExtractor()
        self.consolidator = SleepConsolidator(self.graph)

    def inject_knowledge(
        self, text: str, source_id: str, publish_date_str: str
    ) -> Dict[str, str]:
        """
        Receive unstructured text and extract S-P-O-T tuples into the graph.

        Args:
            text (str): Unstructured text payload.
            source_id (str): A unique ID for the source.
            publish_date_str (str): The publish date in YYYY-MM-DD format.

        Returns:
            Dict[str, str]: A status dictionary.
        """
        dt = datetime.datetime.strptime(publish_date_str, "%Y-%m-%d")
        self.extractor.extract_to_graph(text, source_id, dt, self.graph)
        return {"status": "success", "message": f"Knowledge injected from {source_id}"}

    def trigger_sleep(self) -> Dict[str, str]:
        """
        Trigger the cognitive consolidation process to merge aliases and self-evolve the graph.

        Returns:
            Dict[str, str]: A status dictionary.
        """
        self.consolidator.sleep_and_reflect()
        return {"status": "success", "message": "Graph ontology consolidated."}

    def query_graph(
        self,
        subject: Optional[str] = None,
        predicate: Optional[str] = None,
        object: Optional[str] = None,
    ) -> List[Dict[str, str]]:
        """
        A minimalist, universal graph query interface.

        LLMs can use this to traverse the graph across any dimension:
        - Trend analysis: (subject="CATL", predicate="margin") -> returns all time points.
        - Relationship discovery: (predicate="invests_in", object="Solid State") -> returns subjects.

        Args:
            subject (Optional[str]): Subject filter.
            predicate (Optional[str]): Predicate filter.
            object (Optional[str]): Object filter.

        Returns:
            List[Dict[str, str]]: A list of serialized 4D Tuples.
        """
        res = self.graph.query(subject=subject, predicate=predicate, object=object)

        # Serialize to a format easily readable by LLMs
        output = []
        for t in res:
            output.append(
                {
                    "S": t.subject,
                    "P": t.predicate,
                    "O": f"{t.object}{t.unit or ''}",
                    "Time": t.time.strftime("%Y-%m-%d"),
                    "Source": t.evidence.source_id if t.evidence else "N/A",
                }
            )
        return output


def demo() -> None:
    """Run a local mock demonstration of the MCP Gateway."""
    mcp = MCPGateway()

    # 1. Knowledge Injection (with noisy data: '宁王', 'CATL', '重仓', '毛利')
    text_2022 = "根据2022年研报，宁德时代毛利率为27.0%。比亚迪储能毛利为20.0%。宁王与比亚迪竞品加剧。"
    text_2023 = "根据2023年研报，CATL毛利达到28.5%，比亚迪储能毛利同期为22%。CATL开始重仓全固态电池。"

    mcp.inject_knowledge(text_2022, "rpt_2022", "2022-10-15")
    mcp.inject_knowledge(text_2023, "rpt_2023", "2023-10-15")

    print("\n--- [Query Before Sleep] 尝试查询 '宁德时代' 的 '毛利率' ---")
    res1 = mcp.query_graph(subject="宁德时代", predicate="毛利率")
    print(json.dumps(res1, indent=2, ensure_ascii=False))
    print(
        "-> 发现问题：由于实体和谓语未归一化，只搜到了 2022 年的数据 (因为2023年被LLM抽取为 'CATL' 的 '毛利')"
    )

    # 2. Trigger Consolidation
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
