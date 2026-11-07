# /query-hybrid-memory

Query the local persistent hybrid vector & knowledge graph memory store for cross-session context.

## Steps
1. Initialize `HybridVectorGraphMemoryEngine`.
2. Compute local 128-dim normalized embedding and query semantic vector store.
3. Traverse relational knowledge graph for 1-hop and 2-hop connected entities.
4. Verify HMAC-SHA256 cryptographic signatures to protect against memory tampering.
5. Consolidate into dense Markdown context (<300 tokens) with `[stated]` tags.
