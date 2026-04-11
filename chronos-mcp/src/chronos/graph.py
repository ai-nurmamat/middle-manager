import uuid
from typing import Dict, List, Optional, Any, Set
from pydantic import BaseModel, Field
import datetime
from collections import defaultdict

class SourceEvidence(BaseModel):
    """溯源证据，保证数据来源可追溯"""
    source_id: str
    text_snippet: str
    timestamp: datetime.datetime

class FourDTuple(BaseModel):
    """
    万物皆 Tuple: S-P-O-T
    (Subject, Predicate, Object, Time)
    彻底颠覆传统图谱和传统时序数据库的隔离，用一种结构表达一切。
    """
    id: str = Field(default_factory=lambda: f"tup_{uuid.uuid4().hex[:8]}")
    subject: str = Field(..., description="主体，如 '宁德时代'")
    predicate: str = Field(..., description="谓语，如 '毛利率', '投资', '发布'")
    object: str = Field(..., description="客体，如 '28.5%', '固态电池', '海豹'")
    time: datetime.datetime = Field(..., description="事件/状态发生的时间")
    
    # 元数据
    unit: Optional[str] = Field(None, description="当 object 是数值时的单位")
    evidence: Optional[SourceEvidence] = None

class UniversalHypergraph:
    """
    万能的四维超图记忆引擎 (纯内存实现，随时可换为 Postgres+Timescale)
    """
    def __init__(self):
        self.tuples: Dict[str, FourDTuple] = {}
        
        # 索引，O(1) 访问
        self._s_index: Dict[str, List[str]] = defaultdict(list)
        self._p_index: Dict[str, List[str]] = defaultdict(list)
        self._o_index: Dict[str, List[str]] = defaultdict(list)

    def insert(self, tup: FourDTuple) -> str:
        """写入 Tuple 并建立索引"""
        self.tuples[tup.id] = tup
        self._s_index[tup.subject].append(tup.id)
        self._p_index[tup.predicate].append(tup.id)
        self._o_index[tup.object].append(tup.id)
        return tup.id

    def query(self, 
              subject: Optional[str] = None, 
              predicate: Optional[str] = None, 
              object: Optional[str] = None,
              start_time: Optional[datetime.datetime] = None,
              end_time: Optional[datetime.datetime] = None) -> List[FourDTuple]:
        """
        全维图谱查询。可以按主、谓、宾任意组合查询，并按时间过滤。
        """
        # 取交集
        candidates: Optional[Set[str]] = None
        
        if subject:
            s_set = set(self._s_index.get(subject, []))
            candidates = s_set if candidates is None else candidates.intersection(s_set)
        if predicate:
            p_set = set(self._p_index.get(predicate, []))
            candidates = p_set if candidates is None else candidates.intersection(p_set)
        if object:
            o_set = set(self._o_index.get(object, []))
            candidates = o_set if candidates is None else candidates.intersection(o_set)
            
        if candidates is None:
            candidates = set(self.tuples.keys())
            
        results = []
        for cid in candidates:
            t = self.tuples[cid]
            if start_time and t.time < start_time: continue
            if end_time and t.time > end_time: continue
            results.append(t)
            
        # 强制按时间排序
        results.sort(key=lambda x: x.time)
        return results
