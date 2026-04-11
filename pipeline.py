import json
from typing import Dict, Any
from core_models import Entity, TimePoint, SourceEvidence, RelationEvent
from engine import TemporalGraphEngine
import datetime
import uuid

# ==========================================
# 数据注入管道 (Data Ingestion Pipeline)
# 模拟从 LLM 抽取的非结构化文本到时序图谱的转换
# ==========================================

def simulate_llm_extraction(text: str) -> Dict[str, Any]:
    """
    模拟使用 LLM 提取信息的函数。
    在实际生产中，这里是调用 Claude 3.5 Sonnet 等模型，
    使用 JSON Schema 强制返回结构化数据。
    """
    if "2022" in text:
        return {
            "entities": [
                {"id": "300750", "name": "宁德时代", "type": "stock", "aliases": ["CATL", "宁王"]},
                {"id": "002594", "name": "比亚迪", "type": "stock", "aliases": ["BYD"]},
            ],
            "timelines": [
                {
                    "entity_name": "宁德时代",
                    "property_name": "毛利率",
                    "value": 27.0,
                    "unit": "%",
                    "timestamp": "2022-09-30",
                    "confidence": 0.95,
                    "snippet": "宁德时代毛利率为27.0%"
                },
                {
                    "entity_name": "比亚迪",
                    "property_name": "储能毛利率",
                    "value": 20.0,
                    "unit": "%",
                    "timestamp": "2022-09-30",
                    "confidence": 0.9,
                    "snippet": "比亚迪储能毛利率为20.0%"
                }
            ],
            "relations": []
        }
    
    # 默认返回 2023 的数据
    return {
        "entities": [
            {"id": "300750", "name": "宁德时代", "type": "stock", "aliases": ["CATL", "宁王"]},
            {"id": "002594", "name": "比亚迪", "type": "stock", "aliases": ["BYD"]},
            {"id": "c_solid_state", "name": "固态电池", "type": "concept", "aliases": ["全固态电池"]}
        ],
        "timelines": [
            {
                "entity_name": "宁德时代",
                "property_name": "毛利率",
                "value": 28.5,
                "unit": "%",
                "timestamp": "2023-09-30", # Q3 末尾
                "confidence": 0.95,
                "snippet": "宁德时代（CATL）毛利率达到28.5%"
            },
            {
                "entity_name": "比亚迪",
                "property_name": "储能毛利率",
                "value": 22.0,
                "unit": "%",
                "timestamp": "2023-09-30",
                "confidence": 0.9,
                "snippet": "比亚迪的储能毛利率同期仅为22%"
            }
        ],
        "relations": [
            {
                "source": "宁德时代",
                "target": "比亚迪",
                "type": "competitor",
                "timestamp": "2023-09-30",
                "description": "毛利率对比差距",
                "snippet": "相比之下，比亚迪..."
            },
            {
                "source": "宁德时代",
                "target": "固态电池",
                "type": "invests_in",
                "timestamp": "2023-09-30",
                "description": "开始重点布局固态电池",
                "snippet": "同时，宁德时代开始重点布局固态电池"
            }
        ]
    }

def ingest_report(engine: TemporalGraphEngine, report_id: str, text: str, publish_date: datetime.datetime):
    """
    处理研报并写入内存图谱
    Zero-ETL 核心：将 LLM 提取的 JSON 直接转化为内存对象 (TimePoint / RelationEvent)
    """
    extracted = simulate_llm_extraction(text)
    
    # 1. 建立实体
    for e_data in extracted.get("entities", []):
        entity = Entity(
            id=e_data["id"], name=e_data["name"], type=e_data["type"], aliases=e_data.get("aliases", [])
        )
        engine.upsert_entity(entity)
        
    # 2. 写入时序数据点
    for ts_data in extracted.get("timelines", []):
        evidence = SourceEvidence(
            source_id=report_id, text_snippet=ts_data["snippet"], 
            confidence=ts_data["confidence"], timestamp=publish_date
        )
        point = TimePoint(
            timestamp=datetime.datetime.strptime(ts_data["timestamp"], "%Y-%m-%d"),
            value=ts_data["value"], unit=ts_data.get("unit"), evidence=[evidence]
        )
        engine.add_time_point(ts_data["entity_name"], ts_data["property_name"], point)
        
    # 3. 写入动态关系
    for rel_data in extracted.get("relations", []):
        evidence = SourceEvidence(
            source_id=report_id, text_snippet=rel_data["snippet"], 
            confidence=0.85, timestamp=publish_date
        )
        event = RelationEvent(
            timestamp=datetime.datetime.strptime(rel_data["timestamp"], "%Y-%m-%d"),
            description=rel_data["description"], evidence=[evidence]
        )
        engine.add_relation_event(rel_data["source"], rel_data["target"], rel_data["type"], event)

    print(f"✅ Report {report_id} ingested successfully.")
