# How to Query Your RAG System

You've indexed 95 embeddings! Here's how to ask questions.

## Method 1: Using curl (Command Line)

```bash
curl -X POST "http://localhost:8000/query" \
  -H "Content-Type: application/json" \
  -d '{"query": "How do I change my name after marriage?"}'
```

## Method 2: Using the Swagger UI (Easiest!)

1. Start the API server:
   ```bash
   uvicorn src.api.main:app --reload
   ```

2. Open your browser to: http://localhost:8000/docs

3. Click on the `/query` endpoint
4. Click "Try it out"
5. Enter your question in the JSON body:
   ```json
   {
     "query": "How do I change my name after marriage?"
   }
   ```
6. Click "Execute"

## Method 3: Using Python

```python
import requests

response = requests.post(
    "http://localhost:8000/query",
    json={"query": "How do I change my name after marriage?"}
)

print(response.json())
```

## Method 4: Using httpie (if installed)

```bash
http POST localhost:8000/query query="How do I change my name after marriage?"
```

## Example Questions to Try

- "How do I change my name after marriage?"
- "What documents do I need to change my name?"
- "How do I update my driving licence?"
- "What is the process for changing my passport?"
- "Do I need a marriage certificate to change my name?"

## Response Format

You'll get a response like:
```json
{
  "answer": "Stub answer based on retrieval",
  "confidence": 0.95,
  "sources": [
    {
      "doc_name": "your_document",
      "chunk_id": "1",
      "content": "Relevant text from your document...",
      "score": 0.89
    }
  ]
}
```

The `sources` array shows the chunks that were retrieved from your PDF!
