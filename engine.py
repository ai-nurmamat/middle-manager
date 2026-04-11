import logging
from typing import Dict, List, Optional, Any
from core_models import Entity, TimeSeries, TimePoint, TemporalRelation, RelationEvent
from collections import defaultdict
import datetime

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.INFO)

class TemporalGraphEngine:
    """
    核心记忆引擎 (In-Memory MVP)
    实现 O(1) 实体查找，以及 O(log n) 时间序列访问
    未来可以无缝迁移至 PostgreSQL + TimescaleDB
    """
    def __init__(self):
        # 1. Entity Index: entity_id -> Entity
        self._entities: Dict[str, Entity] = {}
        # Alias Index: alias_name -> entity_id
        self._alias_index: Dict[str, str] = {}
        
        # 2. TimeSeries Store: ts_id -> TimeSeries
        self._timelines: Dict[str, TimeSeries] = {}
        
        # 3. Relation Store: (source_id, target_id, rel_type) -> TemporalRelation
        self._relations: Dict[tuple, TemporalRelation] = {}
        
        # 倒排索引：快速查找与某实体相关的所有边 (entity_id -> List[TemporalRelation])
        self._adjacency_list: Dict[str, List[TemporalRelation]] = defaultdict(list)

    def _resolve_entity_id(self, name_or_id: str) -> Optional[str]:
        """实体消歧，通过别名或ID找到确切的内部ID"""
        if name_or_id in self._entities:
            return name_or_id
        return self._alias_index.get(name_or_id)

    def upsert_entity(self, entity: Entity) -> str:
        """插入或更新实体，并维护别名索引"""
        if entity.id not in self._entities:
            self._entities[entity.id] = entity
        else:
            # 简单合并别名和静态属性
            existing = self._entities[entity.id]
            existing.aliases = list(set(existing.aliases + entity.aliases))
            existing.properties.update(entity.properties)
            entity = existing
            
        self._alias_index[entity.name] = entity.id
        for alias in entity.aliases:
            self._alias_index[alias] = entity.id
            
        logger.debug(f"Upserted entity: {entity.name} ({entity.id})")
        return entity.id

    def add_time_point(self, entity_id_or_name: str, property_name: str, point: TimePoint) -> str:
        """向实体的时间线上添加一个数据点"""
        eid = self._resolve_entity_id(entity_id_or_name)
        if not eid:
            raise ValueError(f"Entity '{entity_id_or_name}' not found. Upsert it first.")
            
        entity = self._entities[eid]
        
        # 如果实体还没有这个属性的时间线，则新建
        if property_name not in entity.timelines:
            new_ts = TimeSeries(entity_id=eid, property_name=property_name)
            self._timelines[new_ts.id] = new_ts
            entity.timelines[property_name] = new_ts.id
            
        ts_id = entity.timelines[property_name]
        ts = self._timelines[ts_id]
        
        # 插入数据点 (支持数据修正：如果有相同时间点则覆盖/融合，此处简单起见只追加排序)
        ts.add_point(point)
        return ts_id

    def add_relation_event(self, source: str, target: str, rel_type: str, event: RelationEvent):
        """记录实体关系的动态演变"""
        sid = self._resolve_entity_id(source)
        tid = self._resolve_entity_id(target)
        
        if not sid or not tid:
             raise ValueError("Both source and target entities must exist.")
             
        key = (sid, tid, rel_type)
        if key not in self._relations:
            rel = TemporalRelation(source_id=sid, target_id=tid, relation_type=rel_type)
            self._relations[key] = rel
            self._adjacency_list[sid].append(rel)
            self._adjacency_list[tid].append(rel)
            
        rel = self._relations[key]
        rel.add_event(event)

    # ===============================
    # 查询引擎接口 (Query APIs)
    # ===============================

    def get_timeline(self, entity_id_or_name: str, property_name: str, 
                     start_date: Optional[datetime.datetime] = None, 
                     end_date: Optional[datetime.datetime] = None) -> Optional[TimeSeries]:
        """获取实体的时序数据，可按时间截断"""
        eid = self._resolve_entity_id(entity_id_or_name)
        if not eid: return None
        
        entity = self._entities[eid]
        ts_id = entity.timelines.get(property_name)
        if not ts_id: return None
        
        ts = self._timelines[ts_id]
        
        # 如果没有时间过滤，直接返回引用；否则深拷贝并过滤
        if not start_date and not end_date:
            return ts
            
        filtered_points = []
        for pt in ts.points:
            if start_date and pt.timestamp < start_date: continue
            if end_date and pt.timestamp > end_date: continue
            filtered_points.append(pt)
            
        # 返回截断后的视图
        return TimeSeries(
            id=ts.id, entity_id=ts.entity_id, 
            property_name=ts.property_name, points=filtered_points
        )

    def get_entity_relations(self, entity_id_or_name: str) -> List[TemporalRelation]:
        """获取与实体相关的所有动态图谱边"""
        eid = self._resolve_entity_id(entity_id_or_name)
        if not eid: return []
        return self._adjacency_list.get(eid, [])
