from typedb.driver import TransactionType, Credentials, DriverOptions, TypeDB, QueryOptions
from typedb_graph_utils.networkx_builder import NetworkXBuilder
from typedb_graph_utils.matplotlib_visualizer import MatplotlibVisualizer

DB_ADDRESS = "127.0.0.1:1729"
DB_CREDENTIALS = Credentials("admin", "password")
DRIVER_OPTIONS = DriverOptions(is_tls_enabled=False)
QUERY_OPTIONS = QueryOptions()
QUERY_OPTIONS.include_query_structure = True
DB_NAME = "typedb-graph-tutorial-py"


def setup(driver, schema, data):
    if DB_NAME in list(db.name for db in driver.databases.all()):
        driver.databases.get(DB_NAME).delete()
    driver.databases.create(DB_NAME)
    with driver.transaction(DB_NAME, TransactionType.SCHEMA) as tx:
        tx.query(schema).resolve()
        tx.commit()
    with driver.transaction(DB_NAME, TransactionType.WRITE) as tx:
        rows = list(tx.query(data).resolve())
        assert 1 == len(rows)
        tx.commit()


def run_query(driver, query):
    with driver.transaction(DB_NAME, TransactionType.READ) as tx:
        answers = list(tx.query(query, QUERY_OPTIONS).resolve())
    return answers


def build_graph_for_answers(answers, builder):
    for (i, answer) in enumerate(answers):
        builder.add_answer(i, answer)
    return builder.finish()


def test_friendships():
    SCHEMA = """
    define
      attribute name value string;
      relation friendship, relates friend @card(2);
      entity person, plays friendship:friend, owns name @key;
    """

    DATA = """
    insert
      $john isa person, has name "John";
      $james isa person, has name "James";
      $jeff isa person, has name "Jeff";
      $f12 isa friendship, links (friend: $john, friend: $james);
      $f23 isa friendship, links (friend: $james, friend: $jeff);
      $f31 isa friendship, links (friend: $jeff, friend: $john);
    """

    QUERY = """
    match 
      $f isa friendship, links (friend: $p1, friend: $p2);
      $p1 has name $n1;
      $p2 has name $n2;
      $n1 < $n2;
    """
    driver = TypeDB.driver(DB_ADDRESS, DB_CREDENTIALS, DRIVER_OPTIONS)
    setup(driver, SCHEMA, DATA)
    answers = run_query(driver, QUERY)
    assert 3 == len(answers), "TypeDB answer count mismatch"
    assert answers[0].query_structure() is not None, "TypeDB no query structure"
    graph = build_graph_for_answers(answers, NetworkXBuilder(answers[0].query_structure()))
    assert 9 == len(graph.nodes), "nx node count mismatch"
    assert 9 == len(graph.edges), "nx edge count mismatch"
    return graph


def test_expression_disjunction():
    QUERY = """
    match 
      { let $y = 3; } or { let $y = 5; };
      { let $x = 2 + $y; } or { let $x = 2 * $y; };
    """
    driver = TypeDB.driver(DB_ADDRESS, DB_CREDENTIALS, DRIVER_OPTIONS)
    answers = run_query(driver, QUERY)
    assert 4 == len(answers), "TypeDB answer count mismatch"
    assert answers[0].query_structure() is not None, "TypeDB no query structure"
    graph = build_graph_for_answers(answers, NetworkXBuilder(answers[0].query_structure()))
    assert 11 == len(
        graph.nodes), "nx node count mismatch"  # 2 + 4 expr nodes,  4 values for x + 2 values for y  - The value 5 is shared
    assert 10 == len(graph.edges), "nx edge count mismatch"
    return graph


def run_readme_example():
    # Must manually ensure they're in sync
    from typedb.driver import TransactionType, Credentials, DriverOptions, TypeDB, QueryOptions
    from typedb_graph_utils import NetworkXBuilder, MatplotlibVisualizer

    driver = TypeDB.driver("127.0.0.1:1729", Credentials("admin", "password"), DriverOptions(is_tls_enabled=False))
    DB_NAME = "typedb_graph_utils_readme"
    if DB_NAME in [db.name for db in driver.databases.all()]:
        driver.databases.get(DB_NAME).delete()
    driver.databases.create(DB_NAME)
    with driver.transaction(DB_NAME, TransactionType.READ) as tx:
        answers = list(tx.query("match let $x = 1;", QueryOptions(include_query_structure=True)).resolve())

    builder = NetworkXBuilder(answers[0].query_structure())
    for (i, answer) in enumerate(answers):
        builder.add_answer(i, answer)
    graph = builder.finish()
    MatplotlibVisualizer.draw(graph)


if __name__ == "__main__":
    MatplotlibVisualizer.draw(test_friendships())

    MatplotlibVisualizer.draw(test_expression_disjunction())

    run_readme_example()
