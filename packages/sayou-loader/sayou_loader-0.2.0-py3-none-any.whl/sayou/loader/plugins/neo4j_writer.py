from typing import List

from ..core.exceptions import WriterError
from ..interfaces.base_writer import BaseWriter

try:
    from neo4j import GraphDatabase
except ImportError:
    raise ImportError(
        "Neo4jWriter requires 'neo4j'. Install with 'pip install sayou-loader[neo4j]'"
    )


class Neo4jWriter(BaseWriter):
    """
    Executes Cypher queries against a Neo4j database.
    """

    component_name = "Neo4jWriter"

    def initialize(self, **kwargs):
        uri = kwargs.get("neo4j_uri")
        user = kwargs.get("neo4j_user")
        password = kwargs.get("neo4j_password")

        if not uri:
            raise WriterError("Neo4jWriter requires 'neo4j_uri'.")

        self.driver = GraphDatabase.driver(uri, auth=(user, password))
        self._log(f"Neo4j driver connected to {uri}.")

    def __del__(self):
        if hasattr(self, "driver"):
            self.driver.close()

    def _do_write(self, translated_data: List[str]):
        """[Tier 1 구현] 변환된 Cypher 쿼리를 배치 실행"""

        if not isinstance(translated_data, list):
            raise WriterError("Neo4jWriter expects a 'list' of Cypher strings.")

        # (간단한 예시: 트랜잭션 내에서 쿼리 순차 실행)
        with self.driver.session() as session:
            for query in translated_data:
                try:
                    session.run(query)
                except Exception as e:
                    self._log(f"Cypher query failed: {e} | Query: {query[:50]}...")
                    # (정책에 따라 중단하거나 계속 진행)
