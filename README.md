# JanusGraph Expanded Package (Cassandra + Elasticsearch)

This package adds:
- Groovy-compatible schema init submitted via gremlinpython.
- Elasticsearch mixed-index example and full-text search script.
- Production deployment guide (docs/PRODUCTION_GUIDE.md).
- Advanced Python scripts for traversals, transactions (session), paging, and a simple bulk loader.

## Quick start (dev)
1. Create a virtual environment:
    ```
    python3 -m venv venv
    source venv/bin/activate
    ```
2. Install Python deps:
    ```
    pip install gremlinpython
    ```

3. Ensure Docker and Docker Compose are installed.
4. From this directory, run:
   ```
   docker compose up -d
   ```
5. Wait for services:
   - Cassandra (9042)
   - Elasticsearch (9200)
   - JanusGraph Gremlin Server (8182)
6. Initialize schema:
   ```
   python3 scripts/schema_init_groovy.py
   python3 scripts/create_mixed_index.py
   python3 scripts/create_and_reindex_mixed_index_batch.py
   ```
7. Load sample data and try searches:
   ```
   python3 scripts/fulltext_search.py
   python3 scripts/advanced_traversals.py
   python3 scripts/import_and_summary.py
   ```

## Compatibility notes
- JanusGraph 0.6.3 has known tested compatibility with Cassandra 4.x and Elasticsearch 7.x series. See JanusGraph release notes for exact tested versions. 
