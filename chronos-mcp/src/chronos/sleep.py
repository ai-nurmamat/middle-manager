"""
Cognitive Consolidation Mechanism for Chronos-MCP.

Since the system allows the LLM to invent Ontology on the fly, the graph
inevitably gathers noisy entities (e.g., 'CATL' vs '宁王') and predicates
(e.g., '毛利' vs '毛利率').

This module acts like "sleep" for the engine, running in the background
to consolidate aliases and self-evolve the ontology.
"""

from .graph import UniversalHypergraph


class SleepConsolidator:
    """
    Consolidates the UniversalHypergraph by merging noisy aliases.
    In a full production environment, this would call an LLM or clustering
    algorithm to group synonyms dynamically. Here we use a predefined dictionary
    to demonstrate the core mechanism.
    """

    def __init__(self, graph: UniversalHypergraph) -> None:
        self.graph = graph
        # Map raw noisy names to normalized schema names
        self.entity_aliases = {
            "CATL": "宁德时代",
            "宁王": "宁德时代",
            "比亚迪": "比亚迪",
            "全固态电池": "固态电池",
        }
        self.predicate_aliases = {
            "毛利": "毛利率",
            "储能毛利": "储能毛利率",
            "重仓": "投资",
            "竞品": "竞争对手",
        }

    def sleep_and_reflect(self) -> None:
        """
        Trigger the memory consolidation process.
        Iterates over the entire graph and updates indexes where aliases are found.
        """
        print("\n💤 [Consolidation] The engine goes to sleep... reflecting on memory.")
        updated_count = 0

        # Iterate over all tuples and normalize their dimensions
        for t_id, tup in self.graph.tuples.items():

            # 1. Normalize Subject
            if tup.subject in self.entity_aliases:
                norm_sub = self.entity_aliases[tup.subject]
                if tup.subject != norm_sub:
                    # Update index
                    self.graph._s_index[tup.subject].remove(t_id)
                    tup.subject = norm_sub
                    if norm_sub not in self.graph._s_index:
                        self.graph._s_index[norm_sub] = []
                    self.graph._s_index[norm_sub].append(t_id)
                    updated_count += 1

            # 2. Normalize Predicate
            if tup.predicate in self.predicate_aliases:
                norm_pred = self.predicate_aliases[tup.predicate]
                if tup.predicate != norm_pred:
                    self.graph._p_index[tup.predicate].remove(t_id)
                    tup.predicate = norm_pred
                    if norm_pred not in self.graph._p_index:
                        self.graph._p_index[norm_pred] = []
                    self.graph._p_index[norm_pred].append(t_id)
                    updated_count += 1

            # 3. Normalize Object (if the object happens to be an entity)
            if tup.object in self.entity_aliases:
                norm_obj = self.entity_aliases[tup.object]
                if tup.object != norm_obj:
                    self.graph._o_index[tup.object].remove(t_id)
                    tup.object = norm_obj
                    if norm_obj not in self.graph._o_index:
                        self.graph._o_index[norm_obj] = []
                    self.graph._o_index[norm_obj].append(t_id)
                    updated_count += 1

        print(
            f"✨ [Consolidation] Woke up! Consolidated {updated_count} noisy aliases into a unified schema.\n"
        )
