import datetime
from .graph import UniversalHypergraph, FourDTuple

# ===================================================================
# 认知巩固机制 (Cognitive Consolidation / "Sleep" Mechanism)
# 最颠覆性的设计：由于我们放任 LLM 发明 Ontology（本体），
# 会导致 "宁王" 和 "CATL"、"毛利" 和 "毛利率" 遍布图谱。
# 后台睡眠线程会定期将这些噪音节点合并为统一概念，实现知识图谱的自我进化。
# ===================================================================

class SleepConsolidator:
    def __init__(self, graph: UniversalHypergraph):
        self.graph = graph
        # 记录映射关系 (原始名称 -> 规范名称)
        self.entity_aliases = {
            "CATL": "宁德时代",
            "宁王": "宁德时代",
            "比亚迪": "比亚迪",
            "全固态电池": "固态电池"
        }
        self.predicate_aliases = {
            "毛利": "毛利率",
            "储能毛利": "储能毛利率",
            "重仓": "投资",
            "竞品": "竞争对手"
        }

    def sleep_and_reflect(self):
        """
        触发图谱整理。
        实际生产中：这里调用 LLM 将所有 subject/predicate 取出，
        让模型使用聚类算法返回一份合并映射表。
        这里为了演示核心逻辑，使用上方预定义的 alias 词典进行映射重写。
        """
        print("\n💤 [Consolidation] The engine goes to sleep... reflecting on memory.")
        updated_count = 0
        
        # 遍历全图，归一化噪音
        for t_id, tup in self.graph.tuples.items():
            # 1. 规范化 Subject
            if tup.subject in self.entity_aliases:
                norm_sub = self.entity_aliases[tup.subject]
                if tup.subject != norm_sub:
                    # 更新索引
                    self.graph._s_index[tup.subject].remove(t_id)
                    tup.subject = norm_sub
                    self.graph._s_index[norm_sub].append(t_id)
                    updated_count += 1
            
            # 2. 规范化 Predicate
            if tup.predicate in self.predicate_aliases:
                norm_pred = self.predicate_aliases[tup.predicate]
                if tup.predicate != norm_pred:
                    self.graph._p_index[tup.predicate].remove(t_id)
                    tup.predicate = norm_pred
                    self.graph._p_index[norm_pred].append(t_id)
                    updated_count += 1
                    
            # 3. 规范化 Object (如果客体是实体的话)
            if tup.object in self.entity_aliases:
                norm_obj = self.entity_aliases[tup.object]
                if tup.object != norm_obj:
                    self.graph._o_index[tup.object].remove(t_id)
                    tup.object = norm_obj
                    self.graph._o_index[norm_obj].append(t_id)
                    updated_count += 1
                    
        print(f"✨ [Consolidation] Woke up! Consolidated {updated_count} noisy aliases into a unified schema.\n")
