import os
import json
import datetime
from typing import List
from openai import OpenAI
from chronos_graph import UniversalHypergraph, FourDTuple, SourceEvidence

# ===================================================================
# 万能结构化提取器 (Universal Extractor)
# 彻底放弃 Pydantic 硬编码。
# 给 LLM 绝对的自由，它会根据文本创造 Entity、创造 Predicate。
# 支持 Minimax M2.7、DeepSeek、OpenAI 等任意兼容 API。
# ===================================================================

class UniversalExtractor:
    def __init__(self, api_key: str, base_url: str, model: str):
        self.client = OpenAI(api_key=api_key, base_url=base_url)
        self.model = model

    def extract_to_graph(self, text: str, source_id: str, publish_date: datetime.datetime, graph: UniversalHypergraph):
        """
        利用 LLM Function Calling / Constrained Decoding 的理念，
        让模型直接吐出 [Subject, Predicate, Object, Time] 列表。
        """
        prompt = f"""
        你是一个顶级的时序知识图谱构建专家。
        你的任务是将下方文本中所有具有【商业价值、分析价值】的信息，彻底转化为 4D Tuples 数组。
        
        【四维元组规则 (S, P, O, T)】：
        1. Subject (主体): 公司名、产品名、人名等实体。如 "宁德时代"
        2. Predicate (谓语): 属性名、关系名、动作名。无需预先定义！你自由发挥。如 "毛利率", "投资", "市盈率", "竞争对手"
        3. Object (客体): 数值、字符串、或另一个实体。如 "28.5", "固态电池", "比亚迪"
        4. Unit (单位): 如果 Object 是数值，提炼出单位，如 "%", "亿元"。否则为空。
        5. Time (时间): 该事实成立或发生的时间 (YYYY-MM-DD)。
        6. Snippet (片段): 证明该元组的一句原文。
        
        文本时间基准：该文本发布于 {publish_date.strftime('%Y-%m-%d')}。
        
        【严格要求】：只返回合法的 JSON 数组，无需任何解释。
        格式示例：
        [
          {{"S": "宁德时代", "P": "毛利率", "O": "28.5", "U": "%", "T": "2023-09-30", "Snippet": "宁德时代毛利率为28.5%"}},
          {{"S": "宁德时代", "P": "研发", "O": "固态电池", "U": "", "T": "2023-10-15", "Snippet": "开始研发固态电池"}}
        ]
        """
        
        try:
            response = self.client.chat.completions.create(
                model=self.model,
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": text}
                ],
                response_format={ "type": "json_object" } # 约束输出 JSON
            )
            
            raw_json = response.choices[0].message.content
            # 处理可能的 JSON 包装
            data = json.loads(raw_json)
            if isinstance(data, dict) and "tuples" in data:
                tuples = data["tuples"]
            elif isinstance(data, list):
                tuples = data
            else:
                # 尝试从 dict 中提取
                tuples = list(data.values())[0] if isinstance(data, dict) else []
                
            # 注入到图谱
            for t in tuples:
                evidence = SourceEvidence(
                    source_id=source_id,
                    text_snippet=t.get("Snippet", ""),
                    timestamp=publish_date
                )
                # 容错处理时间解析
                time_str = t.get("T", publish_date.strftime('%Y-%m-%d'))
                try:
                    dt = datetime.datetime.strptime(time_str[:10], "%Y-%m-%d")
                except:
                    dt = publish_date
                    
                tup = FourDTuple(
                    subject=t.get("S", ""),
                    predicate=t.get("P", ""),
                    object=str(t.get("O", "")),
                    time=dt,
                    unit=t.get("U", ""),
                    evidence=evidence
                )
                graph.insert(tup)
                
            print(f"✅ Extracted {len(tuples)} tuples from {source_id}.")
            
        except Exception as e:
            print(f"❌ Extraction failed: {e}")

class MockExtractor:
    """为了方便你在本地直接跑通，无需真实 API Key 提供的 Mock 版本"""
    def extract_to_graph(self, text: str, source_id: str, publish_date: datetime.datetime, graph: UniversalHypergraph):
        # 简单根据关键字返回，模拟自进化 Schema
        if "2022" in text:
            tuples = [
                {"S": "宁德时代", "P": "毛利率", "O": "27.0", "U": "%", "T": "2022-09-30", "Snippet": "宁德时代毛利率为27.0%"},
                {"S": "比亚迪", "P": "储能毛利", "O": "20.0", "U": "%", "T": "2022-09-30", "Snippet": "比亚迪储能毛利率为20.0%"},
                {"S": "宁王", "P": "竞品", "O": "比亚迪", "U": "", "T": "2022-10-15", "Snippet": "宁王与比亚迪竞争加剧"}
            ]
        else:
            tuples = [
                {"S": "CATL", "P": "毛利", "O": "28.5", "U": "%", "T": "2023-09-30", "Snippet": "CATL毛利达到28.5%"},
                {"S": "比亚迪", "P": "储能毛利", "O": "22.0", "U": "%", "T": "2023-09-30", "Snippet": "比亚迪的储能毛利同期仅为22%"},
                {"S": "CATL", "P": "重仓", "O": "全固态电池", "U": "", "T": "2023-10-15", "Snippet": "CATL开始重仓全固态电池"}
            ]
            
        for t in tuples:
            evidence = SourceEvidence(source_id=source_id, text_snippet=t["Snippet"], timestamp=publish_date)
            dt = datetime.datetime.strptime(t["T"], "%Y-%m-%d")
            tup = FourDTuple(subject=t["S"], predicate=t["P"], object=t["O"], time=dt, unit=t["U"], evidence=evidence)
            graph.insert(tup)
        print(f"✅ Mock Extracted {len(tuples)} tuples from {source_id}.")
