import datetime
from typing import Dict, List, Any
from engine import TemporalGraphEngine

# ==========================================
# 查询分析层 (Analytics Query Engine)
# 提供供 MCP / LLM 调用的高阶分析工具
# ==========================================

class TemporalQueryEngine:
    """基于底层 TemporalGraphEngine 的高阶业务查询接口"""
    def __init__(self, db: TemporalGraphEngine):
        self.db = db

    def query_trend(self, entity_name: str, property_name: str) -> Dict[str, Any]:
        """趋势分析"""
        ts = self.db.get_timeline(entity_name, property_name)
        if not ts or not ts.points:
            return {"error": f"No data found for {entity_name}.{property_name}"}
            
        points = [{"time": p.timestamp.strftime("%Y-%m-%d"), "value": p.value, "unit": p.unit} 
                  for p in ts.points]
                  
        # 简单趋势计算
        start_val = points[0]["value"]
        end_val = points[-1]["value"]
        change = round(float(end_val) - float(start_val), 2)
        
        return {
            "entity": entity_name,
            "property": property_name,
            "points": points,
            "summary": {
                "start": start_val,
                "end": end_val,
                "change": f"{change}{ts.points[0].unit or ''}",
                "direction": "up" if change > 0 else ("down" if change < 0 else "flat")
            }
        }

    def compare_entities(self, entities: List[str], property_name: str) -> Dict[str, Any]:
        """多实体横向对比"""
        result = {}
        for entity in entities:
            ts = self.db.get_timeline(entity, property_name)
            if not ts: continue
            
            # 以年份/季度为键进行对齐
            for p in ts.points:
                time_key = p.timestamp.strftime("%Y-%m")
                if time_key not in result:
                    result[time_key] = {}
                result[time_key][entity] = f"{p.value}{p.unit or ''}"
                
        return {
            "comparison": property_name,
            "data": result
        }

    def discover_relations(self, entity_name: str) -> Dict[str, Any]:
        """发现实体的动态图谱关系及近期事件"""
        relations = self.db.get_entity_relations(entity_name)
        if not relations:
             return {"error": f"No relations found for {entity_name}"}
             
        res = []
        for rel in relations:
            # 找到对方实体的名字 (简单起见，从实体索引里反查)
            sid = rel.source_id
            tid = rel.target_id
            other_id = tid if sid == self.db._resolve_entity_id(entity_name) else sid
            other_entity = self.db._entities.get(other_id)
            other_name = other_entity.name if other_entity else other_id
            
            recent_events = [{"time": e.timestamp.strftime("%Y-%m-%d"), "desc": e.description} 
                             for e in rel.events[-3:]] # 最近三个事件
            
            res.append({
                "related_to": other_name,
                "relation_type": rel.relation_type,
                "recent_events": recent_events
            })
            
        return {"entity": entity_name, "relations": res}
