import datetime
from chronos.graph import UniversalHypergraph, FourDTuple


def test_hypergraph_insert_and_query():
    graph = UniversalHypergraph()

    tup1 = FourDTuple(
        subject="CATL",
        predicate="毛利率",
        object="28.5",
        time=datetime.datetime(2023, 9, 30),
    )

    tup2 = FourDTuple(
        subject="CATL",
        predicate="投资",
        object="固态电池",
        time=datetime.datetime(2023, 10, 15),
    )

    graph.insert(tup1)
    graph.insert(tup2)

    # Test query by subject
    res1 = graph.query(subject="CATL")
    assert len(res1) == 2

    # Test query by predicate
    res2 = graph.query(predicate="投资")
    assert len(res2) == 1
    assert res2[0].object == "固态电池"

    # Test query by multiple dimensions
    res3 = graph.query(subject="CATL", predicate="毛利率")
    assert len(res3) == 1
    assert res3[0].object == "28.5"

    # Test time sorting
    assert res1[0].time < res1[1].time


def test_sleep_consolidation():
    from chronos.sleep import SleepConsolidator

    graph = UniversalHypergraph()

    tup1 = FourDTuple(
        subject="宁王",
        predicate="毛利",
        object="27.0",
        time=datetime.datetime(2022, 9, 30),
    )
    graph.insert(tup1)

    # Query before sleep
    res_before = graph.query(subject="宁王", predicate="毛利")
    assert len(res_before) == 1

    # Run sleep
    consolidator = SleepConsolidator(graph)
    consolidator.sleep_and_reflect()

    # Query after sleep using unified ontology
    res_after = graph.query(subject="宁德时代", predicate="毛利率")
    assert len(res_after) == 1
    assert res_after[0].object == "27.0"

    # Old aliases should be gone from index
    assert len(graph.query(subject="宁王")) == 0
