# sayou-loader

[![Build Status](https://img.shields.io/github/actions/workflow/status/sayouzone/sayou-fabric/ci.yml?branch=main)](https://github.com/sayouzone/sayou-fabric/actions)
[![License: Apache 2.0](https://img.shields.io/badge/License-Apache%202.0-blue.svg)](https://www.apache.org/licenses/LICENSE-2.0)
[![Docs](https://img.shields.io/badge/docs-mkdocs-blue.svg)](https://sayouzone.github.io/sayou-fabric/library-guides/loader/)

`sayou-loader` is the **data persistence layer** of the Sayou Data Platform. It handles the final step of the ETL pipeline: saving the constructed Knowledge Graph or Vector Embeddings to permanent storage.

It prioritizes **Safety** and **Flexibility**. Whether you are saving to a local JSON file for debugging or a Neo4j cluster for production, `sayou-loader` provides a consistent interface with a built-in safety net.

## Philosophy

**"Safe Landing."**
After expensive processing (Parsing -> Chunking -> Embedding), data must not be lost.
`sayou-loader` implements a **Smart Fallback** mechanism. If the target database (e.g., Neo4j) is unreachable or the specific loader is missing, it automatically falls back to local file storage, ensuring data integrity.

## 🚀 Key Features

* **Unified Interface:** Single `load()` method for all destination types (File, GraphDB, VectorDB).
* **Smart Fallback:** Automatically saves to disk if the primary storage strategy fails or is unavailable.
* **Format Agnostic:** Handles Dictionaries, Lists, Strings, and Bytes seamlessly.
* **Extensible:** Tier 3 Plugin architecture makes it easy to add support for new databases (e.g., Pinecone, Milvus, PostgreSQL).

## 📦 Installation

```python
pip install sayou-loader
```

## ⚡ Quickstart

The `LoaderPipeline` intelligently routes data to the correct destination handler.

```python
from sayou.loader.pipeline import LoaderPipeline

def run_demo():
    # 1. Data to Save (e.g., Knowledge Graph)
    data = {"nodes": [{"id": "1", "label": "Test"}], "edges": []}

    # 2. Initialize Pipeline
    pipeline = LoaderPipeline()
    pipeline.initialize()

    # 3. Save to Local File
    pipeline.run(
        data=data,
        destination="./output/graph.json",
        target_type="file"
    )
    
    # 4. Save to Neo4j (If configured, otherwise Fallback to File)
    pipeline.run(
        data=data,
        destination="bolt://localhost:7687",
        target_type="neo4j" # or custom plugin type
    )

if __name__ == "__main__":
    run_demo()
```

## 🤝 Contributing

Contributions for new Database Plugins (e.g., ChromaDB, ElasticSearch) are highly appreciated.

## 📜 License

Apache 2.0 License © 2025 Sayouzone