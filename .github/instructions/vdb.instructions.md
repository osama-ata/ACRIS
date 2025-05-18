---
applyTo: "**/*.py"
---

# Integrating DuckDB with Vector Similarity Search (VSS) in ACRIS

## Overview

Here’s a step-by-step guide to integrate DuckDB with the Vector Similarity Search (VSS) extension into your ACRIS repository:

---

## 1. Install Dependencies

Add dependencies to your project (edit requirements.txt or install directly):

```bash
uv add duckdb sentence-transformers numpy
```

---

## 2. Install and Load DuckDB VSS Extension

DuckDB 0.10.0+ supports VSS. The extension is loaded at runtime in Python code.

---

## 3. Prepare Your Embedding Model

Use a model like sentence-transformers to generate embeddings for your risk case texts.

```python
from sentence_transformers import SentenceTransformer

model = SentenceTransformer('all-MiniLM-L6-v2')
texts = [
    "Risk of fall from height",
    "Fire hazard in storage area",
    # add your risk cases here
]
embeddings = model.encode(texts)
```

---

## 4. Create and Initialize DuckDB Database

Create a new module, e.g., acris/vector_db.py.

```python
import duckdb

# Connect to a database file (or use ':memory:' for in-memory)
con = duckdb.connect('acris.duckdb')
con.execute("INSTALL vss;")
con.execute("LOAD vss;")
```

---

## 5. Create a Table for Risk Cases with Embeddings

```python
con.execute("""
CREATE TABLE IF NOT EXISTS risk_cases (
    id INTEGER PRIMARY KEY,
    description TEXT,
    embedding VECTOR(FLOAT, 384)  -- 384 if using MiniLM-L6-v2
)
""")
```

---

## 6. Insert Embeddings and Data

```python
for idx, (desc, emb) in enumerate(zip(texts, embeddings)):
    con.execute(
        "INSERT INTO risk_cases (id, description, embedding) VALUES (?, ?, ?)",
        (idx, desc, emb.tolist())
    )
```

---

## 7. Build the VSS Index

```python
con.execute("CREATE INDEX IF NOT EXISTS ON risk_cases USING vss(embedding)")
```

---

## 8. Query for Semantic Similarity

To search for similar risk cases semantically:

```python
query_text = "fall prevention"
query_emb = model.encode([query_text])[0]
result = con.execute(
    """
    SELECT id, description, vss_distance(embedding, ?) AS score
    FROM risk_cases
    ORDER BY score LIMIT 5
    """,
    (query_emb.tolist(),)
).fetchall()

for row in result:
    print(row)
```

---

## 9. Integrate with the ACRIS Workflow

- Place the above logic in a new module (e.g., acris/vector_db.py).
- Add functions for:
  - Adding new risk cases (with embedding)
  - Querying similar cases
  - Rebuilding the VSS index if data updates

Example interface (in acris/vector_db.py):

```python
def add_risk_case(description: str, model, con):
    emb = model.encode([description])[0]
    con.execute(
        "INSERT INTO risk_cases (description, embedding) VALUES (?, ?)",
        (description, emb.tolist())
    )

def find_similar_cases(query: str, model, con, top_k=5):
    query_emb = model.encode([query])[0]
    return con.execute(
        """
        SELECT id, description, vss_distance(embedding, ?) AS score
        FROM risk_cases
        ORDER BY score LIMIT ?
        """,
        (query_emb.tolist(), top_k)
    ).fetchall()
```

---

## 10. Update Documentation

Document the setup in your README.md:

```markdown
### Vector Semantic Search with DuckDB

- Install requirements: `pip install duckdb sentence-transformers numpy`
- On first run, the VSS extension is installed and loaded automatically.
- See `acris/vector_db.py` for integration details.
```

---

## Summary Table

| Step | Action                                 |
| ---- | -------------------------------------- |
| 1    | Install Python dependencies            |
| 2    | Install/load DuckDB VSS extension      |
| 3    | Prepare embedding model                |
| 4    | Connect to DuckDB                      |
| 5    | Create table for risk cases + vectors  |
| 6    | Insert data and embeddings             |
| 7    | Create VSS index                       |
| 8    | Query for similar cases                |
| 9    | Integrate into ACRIS modules/workflows |
| 10   | Update documentation                   |

---
