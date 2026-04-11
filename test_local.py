#!/usr/bin/env python3
import json
import sys

from engine import TemporalGraphEngine
from pipeline import ingest_report
from query_engine import TemporalQueryEngine
import datetime

def test_local():
    # 1. 初始化引擎并注入数据
    db = TemporalGraphEngine()
    
    sample_text = """
    根据2023年Q3研报，宁德时代（CATL）毛利率达到28.5%，主要由于规模效应。
    相比之下，比亚迪的储能毛利率同期仅为22%。同时，宁德时代开始重点布局固态电池。
    """
    ingest_report(db, report_id="rpt_001", text=sample_text, publish_date=datetime.datetime(2023, 10, 15))
    
    sample_text_2 = """根据2022年Q3研报，宁德时代毛利率为27.0%。比亚迪储能毛利率为20.0%"""
    ingest_report(db, report_id="rpt_000", text=sample_text_2, publish_date=datetime.datetime(2022, 10, 15))
    
    query_engine = TemporalQueryEngine(db)

    print("\n" + "="*50)
    print("Test 1: Trend Query (宁德时代 - 毛利率)")
    print("="*50)
    res1 = query_engine.query_trend("宁德时代", "毛利率")
    print(json.dumps(res1, indent=2, ensure_ascii=False))
    
    print("\n" + "="*50)
    print("Test 2: Compare Entities (宁德时代 vs 比亚迪 - 储能毛利率)")
    print("="*50)
    res2 = query_engine.compare_entities(["宁德时代", "比亚迪"], "储能毛利率")
    print(json.dumps(res2, indent=2, ensure_ascii=False))

    print("\n" + "="*50)
    print("Test 3: Discover Relations (CATL)")
    print("="*50)
    res3 = query_engine.discover_relations("CATL") # 使用别名
    print(json.dumps(res3, indent=2, ensure_ascii=False))

if __name__ == "__main__":
    test_local()
