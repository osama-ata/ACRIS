"""
acris/vector_db.py

DuckDB + Vector Similarity Search (VSS) integration for ACRIS risk case semantic search.

This module provides functions to initialize the DuckDB database with VSS extension, manage risk case embeddings, and perform semantic similarity queries using Sentence Transformers.

Follows ACRIS coding standards: PEP 8, type hints, Google-style docstrings, and robust error handling.
"""  # noqa: E501

import os

import duckdb
import numpy as np
from duckdb import DuckDBPyConnection
from sentence_transformers import SentenceTransformer

DUCKDB_PATH = os.environ.get('ACRIS_DUCKDB_PATH', 'acris.duckdb')
EMBEDDING_DIM = 384  # For 'all-MiniLM-L6-v2'

_con: DuckDBPyConnection | None = None
_model: SentenceTransformer | None = None


def get_connection() -> duckdb.DuckDBPyConnection:
	"""Get or create a DuckDB connection with VSS extension loaded."""
	global _con
	if _con is None:
		_con = duckdb.connect(DUCKDB_PATH)
		_con.execute('INSTALL vss;')
		_con.execute('LOAD vss;')
		_con.execute(f"""
            CREATE TABLE IF NOT EXISTS risk_cases (
                id INTEGER PRIMARY KEY AUTOINCREMENT,
                description TEXT NOT NULL,
                embedding VECTOR(FLOAT, {EMBEDDING_DIM}) NOT NULL
            )
        """)
		_con.execute('CREATE INDEX IF NOT EXISTS ON risk_cases USING vss(embedding)')
	return _con


def get_model() -> SentenceTransformer:
	"""Get or load the SentenceTransformer embedding model."""
	global _model
	if _model is None:
		_model = SentenceTransformer('all-MiniLM-L6-v2')
	return _model


def add_risk_case(description: str) -> int:
	"""
	Add a new risk case with its embedding to the database.

	Args:
	    description: The risk case description text.

	Returns:
	    The ID of the inserted risk case.
	"""
	con = get_connection()
	model = get_model()
	emb = model.encode([description], output_value='sentence_embedding', convert_to_numpy=True)[0]
	emb = np.asarray(emb, dtype=np.float32)
	result = con.execute(
		"""
        INSERT INTO risk_cases (description, embedding)
        VALUES (?, ?)
        RETURNING id
        """,
		(description, emb.tolist()),
	).fetchone()
	if result is None or result[0] is None:
		raise RuntimeError('Failed to insert risk case.')
	return int(result[0])


def find_similar_cases(query: str, top_k: int = 5) -> list[tuple[int, str, float]]:
	"""
	Find risk cases most similar to the query string.

	Args:
	    query: The query text.
	    top_k: Number of similar cases to return.

	Returns:
	    List of tuples: (id, description, similarity_score)
	"""
	con = get_connection()
	model = get_model()
	query_emb = model.encode([query], output_value='sentence_embedding', convert_to_numpy=True)[0]
	query_emb = np.asarray(query_emb, dtype=np.float32)
	rows = con.execute(
		"""
        SELECT id, description, vss_distance(embedding, ?) AS score
        FROM risk_cases
        ORDER BY score ASC
        LIMIT ?
        """,
		(query_emb.tolist(), top_k),
	).fetchall()
	return [(int(row[0]), str(row[1]), float(row[2])) for row in rows]


def rebuild_vss_index() -> None:
	"""
	Rebuild the VSS index on the risk_cases table. Call after bulk updates.
	"""
	con = get_connection()
	con.execute('DROP INDEX IF EXISTS risk_cases_embedding_idx')
	con.execute('CREATE INDEX ON risk_cases USING vss(embedding)')


def get_all_risk_cases() -> list[tuple[int, str]]:
	"""
	Retrieve all risk cases (id, description) from the database.

	Returns:
	    List of (id, description) tuples.
	"""
	con = get_connection()
	rows = con.execute('SELECT id, description FROM risk_cases').fetchall()
	return [(int(row[0]), str(row[1])) for row in rows]


# Example usage (for testing only; remove or comment out in production)
if __name__ == '__main__':
	print('Adding example risk cases...')
	add_risk_case('Risk of fall from height')
	add_risk_case('Fire hazard in storage area')
	print("Querying similar cases for 'fall prevention':")
	results = find_similar_cases('fall prevention')
	for rid, desc, score in results:
		print(f'ID: {rid}, Desc: {desc}, Score: {score:.4f}')
