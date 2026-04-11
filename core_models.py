import datetime
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field
import uuid

# ==========================================
# 核心数据结构定义 (Core Data Structures)
# ==========================================

class SourceEvidence(BaseModel):
    """数据来源证据，解决AI幻觉，提供可追溯性"""
    source_id: str = Field(..., description="来源文档ID，如研报ID、新闻URL")
    text_snippet: str = Field(..., description="提取该数据的原始文本片段")
    confidence: float = Field(..., ge=0.0, le=1.0, description="提取置信度")
    timestamp: datetime.datetime = Field(..., description="来源发布的时间")

class TimePoint(BaseModel):
    """时间线上的一个数据点"""
    timestamp: datetime.datetime = Field(..., description="数据发生的业务时间(Valid Time)")
    value: Union[float, str, int] = Field(..., description="属性值")
    unit: Optional[str] = Field(None, description="单位，如 %, 亿")
    evidence: List[SourceEvidence] = Field(default_factory=list, description="支撑该数据点的证据")

class TimeSeries(BaseModel):
    """实体的属性时间线"""
    id: str = Field(default_factory=lambda: f"ts_{uuid.uuid4().hex[:8]}")
    entity_id: str = Field(..., description="归属实体的ID")
    property_name: str = Field(..., description="属性名称，如 '毛利率', '净利润'")
    points: List[TimePoint] = Field(default_factory=list, description="按时间排序的数据点")
    
    def add_point(self, point: TimePoint):
        """添加数据点并保持时间有序"""
        self.points.append(point)
        self.points.sort(key=lambda x: x.timestamp)

class Entity(BaseModel):
    """金融市场中的核心节点"""
    id: str = Field(..., description="实体唯一标识，如股票代码 '300750'")
    name: str = Field(..., description="实体名称，如 '宁德时代'")
    type: str = Field(..., description="实体类型，如 'stock', 'concept', 'industry'")
    aliases: List[str] = Field(default_factory=list, description="别名，用于实体消歧")
    properties: Dict[str, str] = Field(default_factory=dict, description="静态元数据，如 IPO日期")
    
    # 时序属性索引: property_name -> TimeSeries.id
    timelines: Dict[str, str] = Field(default_factory=dict)

class RelationEvent(BaseModel):
    """关系在时间线上的演化事件"""
    timestamp: datetime.datetime = Field(..., description="关系发生/变化的时间")
    description: str = Field(..., description="关系事件描述")
    strength: float = Field(default=1.0, description="关系强度/权重")
    evidence: List[SourceEvidence] = Field(default_factory=list)

class TemporalRelation(BaseModel):
    """实体间的动态关系 (边)"""
    id: str = Field(default_factory=lambda: f"rel_{uuid.uuid4().hex[:8]}")
    source_id: str = Field(..., description="源实体ID")
    target_id: str = Field(..., description="目标实体ID")
    relation_type: str = Field(..., description="关系类型，如 'competitor', 'supplier_of'")
    events: List[RelationEvent] = Field(default_factory=list, description="关系的历史演化")
    
    def add_event(self, event: RelationEvent):
        self.events.append(event)
        self.events.sort(key=lambda x: x.timestamp)
