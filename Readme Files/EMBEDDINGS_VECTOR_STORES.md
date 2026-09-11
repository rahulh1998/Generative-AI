# Lesson 5 — Embeddings, Documents & Vector Stores

## Objective

Understand the foundation of semantic search and RAG:

- Documents
- `page_content`
- Metadata
- Embeddings
- Vectors
- Embedding models
- Vector Stores
- Vector Databases
- Similarity Search
- Retrievers
- Top-K retrieval
- Metadata filtering
- Chroma and FAISS
- How everything connects to RAG

---

## 1. Document

A LangChain `Document` represents a piece of information that can be retrieved and passed to an LLM.

```text
Document
├── page_content
└── metadata
```

Example:

```python
from langchain_core.documents import Document

doc = Document(
    page_content="Passengers can cancel their booking before departure.",
    metadata={
        "source": "cancellation_policy.pdf",
        "page": 12,
        "category": "cancellation"
    }
)
```

**Key idea:** A Document is **content + information about that content**.

---

## 2. `page_content`

`page_content` contains the actual text.

```python
doc.page_content
```

This is the text that is generally sent to the embedding model.

---

## 3. Metadata

Metadata is information **about the document or chunk**.

```python
metadata = {
    "source": "cancellation_policy.pdf",
    "page": 12,
    "category": "cancellation",
    "version": "2026"
}
```

Useful for:

- Filtering
- Citations
- Source tracking
- Debugging
- Access control
- Document versioning
- Multi-tenant applications

Production example:

```python
{
    "tenant_id": "company_a",
    "document_id": "123",
    "source": "policy.pdf",
    "page": 10,
    "department": "finance"
}
```

---

## 4. Embeddings

An **embedding** is a numerical representation of the semantic meaning of data.

```text
"I want to cancel my flight."
        ↓
Embedding Model
        ↓
[0.12, -0.43, 0.81, 0.21, ...]
```

An embedding is **not an answer**. It is a representation that makes semantic comparison and search possible.

---

## 5. Vector

A vector is an ordered collection of numbers.

```text
[0.12, -0.43, 0.81, 0.21]
```

Real embedding models may produce hundreds or thousands of dimensions, such as:

```text
384
768
1024
1536
3072
```

The dimension depends on the embedding model.

---

## 6. Embedding Model

An embedding model converts text/data into vectors.

```text
Text
 ↓
Embedding Model
 ↓
Vector
```

Examples:

- Sentence Transformers
- BGE
- E5
- OpenAI embedding models
- Ollama embedding models

### LLM vs Embedding Model

**LLM:**

```text
Question → LLM → Answer
```

**Embedding model:**

```text
Text → Embedding Model → Vector
```

They solve different problems.

---

## 7. Why Embeddings Are Needed

Keyword search looks for matching words.

Query:

```text
"How can I get my money back?"
```

Document:

```text
"Passengers may be eligible for reimbursement after cancellation."
```

The wording is different, but the meaning is similar.

Embeddings allow search based on **semantic meaning**, not only exact keywords.

Mental model:

```text
Meaning
   ↓
Embedding
   ↓
Vector representation
   ↓
Mathematical similarity
```

---

## 8. Vector Store

A **Vector Store** stores vectors and allows us to search for similar vectors.

Conceptually:

```text
Document
   ↓
Embedding Model
   ↓
Vector
   ↓
Vector Store
```

A vector store generally maintains:

```text
Vector
  ↕
Document
  +
Metadata
```

Example:

```text
Vector                     Document
────────────────────────────────────────────
[0.12, 0.43, ...]     →    "Cancel your flight..."
[0.82, 0.21, ...]     →    "Buy extra baggage..."
[0.31, 0.92, ...]     →    "Change your booking..."
```

---

## 9. Vector Database

A **Vector Database** is a database designed to store and efficiently search vector data.

It may provide:

- Vector storage
- Similarity search
- Indexing
- Metadata filtering
- Persistence
- Scaling
- Access control
- Distributed search

Examples:

- Chroma
- Qdrant
- Pinecone
- Weaviate
- Milvus
- pgvector

---

## 10. Vector Store vs Vector Database

These terms are often used interchangeably.

A useful mental distinction:

**Vector Store:** application-level abstraction/interface for storing and retrieving vectors.

**Vector Database:** underlying database technology providing vector storage/search.

Conceptually:

```text
LangChain
    ↓
Vector Store Interface
    ↓
Chroma / Qdrant / Pinecone / etc.
```

---

## 11. Similarity Search

Similarity search finds vectors closest to a query vector.

```text
Query Vector
     ↓
Similarity Search
     ↓
Document A → 0.91
Document B → 0.76
Document C → 0.31
```

Common similarity/distance approaches:

- Cosine similarity
- Dot product
- Euclidean distance

---

## 12. Cosine Similarity

Cosine similarity measures the angle between vectors.

```text
Similar direction
      ↓
High similarity

Different direction
      ↓
Low similarity
```

It is a common similarity measure for text embeddings.

---

## 13. Top-K Retrieval

`k` specifies how many results should be returned.

```python
results = vectorstore.similarity_search(
    query,
    k=5
)
```

This means:

> Return the top 5 most relevant documents.

Choosing `k` is an important RAG design decision.

Too few:

- May miss useful context

Too many:

- More irrelevant context
- More tokens
- Higher latency
- Potentially worse answers

---

## 14. Retriever

A Retriever is an abstraction responsible for retrieving relevant documents for a query.

```text
Query
 ↓
Retriever
 ↓
Relevant Documents
```

Example:

```python
retriever = vectorstore.as_retriever(
    search_kwargs={"k": 3}
)

docs = retriever.invoke(
    "How can I cancel my flight?"
)
```

---

## 15. Vector Store vs Retriever

### Vector Store

Deals with:

```text
Store vectors
Search vectors
```

### Retriever

Deals with:

```text
Query
 ↓
Retrieve relevant documents
```

Conceptually:

```text
User Query
    ↓
Retriever
    ↓
Vector Store
    ↓
Similarity Search
    ↓
Documents
```

The Retriever provides a higher-level abstraction.

---

## 16. `embed_documents()` vs `embed_query()`

### Documents

```python
embeddings.embed_documents([
    "LangChain is a framework for LLM applications.",
    "LangGraph is used for stateful workflows."
])
```

Used to embed documents.

### Query

```python
embeddings.embed_query(
    "What is LangGraph?"
)
```

Used to embed a query.

Mental model:

```text
Documents → embed_documents()
Query     → embed_query()
```

---

## 17. Document Ingestion / Indexing

Before retrieval can happen, documents need to be indexed.

```text
Raw Documents
     ↓
Load
     ↓
Split into chunks
     ↓
Create Documents
     ↓
Generate Embeddings
     ↓
Store in Vector DB
```

This is the **ingestion/indexing pipeline**.

---

## 18. Query-Time Retrieval

When a user asks a question:

```text
User Query
    ↓
Query Embedding
    ↓
Vector Search
    ↓
Top-K Documents
    ↓
LLM
```

The documents are retrieved at query time.

---

## 19. Complete RAG Architecture

```text
              DOCUMENT INGESTION
                     │
                     ↓
              Raw Documents
                     │
                     ↓
                  Chunking
                     │
                     ↓
              Embedding Model
                     │
                     ↓
                  Vectors
                     │
                     ↓
              Vector Database
                     │
                     │
              ───────┼────────
                     │
                     ↑
                 User Query
                     │
                     ↓
              Query Embedding
                     │
                     ↓
                 Retriever
                     │
                     ↓
            Relevant Documents
                     │
                     ↓
                   Prompt
                     │
                     ↓
                    LLM
                     │
                     ↓
                  Answer
```

---

## 20. Why Documents Are Embedded Beforehand

Suppose there are 1 million document chunks.

We don't want to calculate embeddings for all 1 million documents every time a user asks a question.

Instead, embeddings are generated during ingestion:

```text
Documents
 ↓
Embeddings
 ↓
Vector DB
```

At query time:

```text
Question
 ↓
Query Embedding
 ↓
Search Vector DB
```

This makes retrieval much more efficient.

---

## 21. Metadata Filtering

Vector similarity is not always enough.

For enterprise RAG, documents may belong to different companies or users.

Example:

```python
{
    "tenant_id": "company_a"
}
```

Retrieval can be restricted using metadata:

```text
Query
 ↓
Metadata Filter
 ↓
Vector Search
 ↓
Relevant Documents
```

This is important for security and multi-tenancy.

---

## 22. Embedding Dimensions

Every embedding model has a fixed output dimension.

Example:

```text
Model A → 384 dimensions
Model B → 768 dimensions
Model C → 1536 dimensions
```

A vector might look like:

```text
[x1, x2, x3, ... x384]
```

The vector database/index must support the appropriate dimension.

---

## 23. Changing the Embedding Model

Changing embedding models can require re-indexing.

```text
Old Model
   ↓
Old Vectors
```

Switch to:

```text
New Model
   ↓
New Vectors
```

Do not blindly mix incompatible vector representations.

Production systems should track:

```text
embedding_model
embedding_dimension
embedding_version
```

---

## 24. Chroma

Chroma is useful for:

- Local development
- Learning
- Prototyping
- Small applications

Example:

```python
from langchain_chroma import Chroma

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="learning"
)
```

---

## 25. FAISS

FAISS is a similarity-search library developed by Meta.

Useful for:

- Local experimentation
- Research
- High-performance vector similarity search

It is better thought of as a vector search/indexing library rather than a complete enterprise database by itself.

---

## 26. Chroma vs FAISS

| Feature | Chroma | FAISS |
|---|---|---|
| Local development | Excellent | Excellent |
| Similarity search | Yes | Yes |
| Metadata | Supported | Requires additional handling |
| Persistence | Supported | Requires more setup |
| LangChain support | Yes | Yes |
| Production architecture | Depends on setup | Requires additional engineering |

For this course, **Chroma is the starting point**.

---

## 27. Complete Example

```python
from langchain_core.documents import Document
from langchain_huggingface import HuggingFaceEmbeddings
from langchain_chroma import Chroma

documents = [
    Document(
        page_content="LangChain is a framework for building LLM applications.",
        metadata={"source": "langchain.txt"}
    ),
    Document(
        page_content="LangGraph is used to build stateful AI workflows.",
        metadata={"source": "langgraph.txt"}
    ),
    Document(
        page_content="RAG retrieves relevant information before generating an answer.",
        metadata={"source": "rag.txt"}
    )
]

embeddings = HuggingFaceEmbeddings(
    model_name="sentence-transformers/all-MiniLM-L6-v2"
)

vectorstore = Chroma.from_documents(
    documents=documents,
    embedding=embeddings,
    collection_name="learning"
)

results = vectorstore.similarity_search(
    "What is used to build stateful AI workflows?",
    k=2
)

for doc in results:
    print("CONTENT:", doc.page_content)
    print("METADATA:", doc.metadata)
```

---

## 28. What Happens Internally?

### When documents are added

```text
Document
   ↓
Embedding Model
   ↓
Vector
   ↓
Vector Store
```

### When a query is executed

```text
Query
   ↓
Embedding Model
   ↓
Query Vector
   ↓
Similarity Search
   ↓
Top-K Vectors
   ↓
Associated Documents
```

---

## 29. Production Considerations

### Embedding Model

Consider:

- Quality
- Latency
- Cost
- Language support
- Vector dimensions

### Vector Database

Consider:

- Scale
- Persistence
- Filtering
- Indexing
- Availability
- Latency
- Multi-tenancy

### Retrieval

Consider:

- Top-K
- Similarity threshold
- Metadata filters
- Hybrid search
- Reranking

### Data

Consider:

- Chunk size
- Chunk overlap
- Document versions
- Metadata quality
- Access permissions

---

## 30. Senior Engineer Mental Model

Do not just memorize:

```python
Chroma.from_documents(...)
```

Understand the architecture:

> **Documents contain information → embedding models convert that information into vectors → vector stores/indexes store and search those vectors → retrievers return relevant documents → the LLM uses those documents as context.**

---

## 🧪 Practice Assignment

Build a small vector store containing 10 documents about:

- Python
- LangChain
- LangGraph
- RAG
- Agents
- Vector Databases
- Embeddings
- LLMs
- Prompt Engineering
- Tool Calling

Add metadata:

```python
{
    "topic": "LangChain",
    "source": "learning_notes"
}
```

Test:

```text
What is used to build stateful AI workflows?

How can I search documents based on meaning?

What is used to give LLMs access to external systems?
```

For every query, print:

```text
Query
↓
Retrieved Documents
↓
Metadata
```

---

## ✅ Lesson 5 Checklist

- [ ] Understand `Document`
- [ ] Understand `page_content`
- [ ] Understand metadata
- [ ] Understand embeddings
- [ ] Understand vectors
- [ ] Understand embedding models
- [ ] Understand vector stores
- [ ] Understand vector databases
- [ ] Understand similarity search
- [ ] Understand cosine similarity
- [ ] Understand Top-K
- [ ] Understand retrievers
- [ ] Understand `embed_documents()`
- [ ] Understand `embed_query()`
- [ ] Understand metadata filtering
- [ ] Understand Chroma
- [ ] Understand FAISS
- [ ] Understand the RAG retrieval pipeline
- [ ] Complete the practical exercise

---

## 🔑 One-Line Summary

**Lesson 5:** Learn how raw text becomes embeddings/vectors, how vectors are stored and searched, and how a Retriever turns that search into relevant documents for a RAG application.
